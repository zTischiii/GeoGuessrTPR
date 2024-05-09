import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json

def accept_cookies(driver):
    try:
        wait = WebDriverWait(driver, 10)
        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='accept-choices']")))
        accept_button.click()
        print("Cookies wurden akzeptiert.")
    except Exception as e:
        print("Cookie-Zustimmung nicht gefunden oder bereits akzeptiert.")

def save_cookie(driver, path):
    with open(path, 'w') as filehandler:
        json.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
    with open(path, 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    for cookie in cookies:
        driver.add_cookie(cookie)

def geoguessr_sign_in(email, password, cookie_path='cookies.json'):
    driver = webdriver.Chrome()
    driver.get("https://www.geoguessr.com")
    if os.path.exists(cookie_path):
        load_cookie(driver, cookie_path)
        driver.refresh()
        time.sleep(3)
        accept_cookies(driver)
        if driver.current_url != "https://www.geoguessr.com/de/signin":
            return driver
    driver.get("https://www.geoguessr.com/de/signin")
    time.sleep(2)
    accept_cookies(driver)
    email_input = driver.find_element(By.CSS_SELECTOR, "input[data-qa='email-field']")
    email_input.send_keys(email)
    password_input = driver.find_element(By.CSS_SELECTOR, "input[data-qa='password-field']")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)
    save_cookie(driver, cookie_path)
    return driver


def navigate_to_party_page(driver, modes):
    driver.get("https://www.geoguessr.com/party")
    wait = WebDriverWait(driver, 10)

    settings_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[2]/div[2]/main/div/div[4]/div[1]/div[3]/button")))
    settings_button.click()
    print("Einstellungen wurden geöffnet.")

    valid_modes = {"bewegen", "herumschauen", "zoomen"}
    for mode in modes:
        if mode not in valid_modes:
            raise ValueError(f"Keine gültige Einstellung: {mode}")

    for mode in modes:
        if mode == "bewegen":
            toggle = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/input")))
            toggle.click()
            print("Bewegen-Schalter umgelegt.")
        elif mode == "herumschauen":
            toggle = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[2]/input")))
            toggle.click()
            print("Herumschauen-Schalter umgelegt.")
        elif mode == "zoomen":
            toggle = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[3]/input")))
            toggle.click()
            print("Zoomen-Schalter umgelegt.")



    # Dummer Slider zum Zeiteinstellen.
    ZeitSlider = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div[2]/div[4]/div[4]/div/div[2]")
    ZeitSlider.click()


    # Zeit Nullen
    action = ActionChains(driver)
    for _ in range(50):
        # Slider mit Pfeiltasten bewegen, weil keine Ahnung wie Pixel bewegen...
        action.send_keys_to_element(ZeitSlider, Keys.ARROW_LEFT)
    action.perform()
    print("Zeit ist genullt.")



    # Einstellungen bestätigen (schließen!)
    confirm_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/button")))
    confirm_button.click()
    print("Einstellungen bestätigt.")

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def party(ctx, *, modes: str):
    if not modes.startswith("(") or not modes.endswith(")"):
        await ctx.send("Bitte geben Sie die Modi in Klammern an, getrennt durch Kommas. Beispiel: !party (bewegen,zoomen)")
        return

    modes = modes.strip("()").split(",")
    try:
        email = "IhreEmail"
        password = "IhrPasswort"
        driver = geoguessr_sign_in(email, password)
        navigate_to_party_page(driver, modes)
        await ctx.send("Party-Seite wurde erfolgreich konfiguriert.")
    except Exception as e:
        await ctx.send(f"Ein Fehler ist aufgetreten: {str(e)}")
    finally:
        if driver:
            driver.quit()

