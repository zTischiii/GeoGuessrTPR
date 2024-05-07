import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json
# Funktionen Programmablauf #1
def accept_cookies(driver):
    try:
        wait = WebDriverWait(driver, 10)
        accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='accept-choices']")))
        accept_button.click()
        print("Cookies wurden akzeptiert.")
    except Exception as e:
        print("Cookie-Zustimmung nicht gefunden oder bereits akzeptiert.")
#Anmelde-Cookie
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
            text_content = navigate_to_party_page(driver)
            return driver, text_content
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
    text_content = navigate_to_party_page(driver)
    return driver, text_content
def navigate_to_party_page(driver):
    driver.get("https://www.geoguessr.com/party")
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[2]/div[2]/main/div/div[2]/div/div/div[2]/div/div/div[1]/div/button")))
    button.click()
    input_field = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[4]/div/div/div/div/span/input")))
    text_content = input_field.get_attribute("value")
    print("Textinhalt des Feldes:", text_content)
    return text_content
# Discord Bot (Intents) <- Müssen ggf. angepasst werden.
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)
@bot.command()
async def party(ctx):
    try:
        # gff. Datenbank oder Cookie
        email = "Email"
        password = "Passwort"
        driver, text_content = geoguessr_sign_in(email, password)
        await ctx.send("Textinhalt des Feldes: " + text_content)
    except Exception as e:
        await ctx.send(f"Ein Fehler ist aufgetreten: {str(e)}")
    finally:
        if driver:
            driver.quit()

    #Bot ID
    bot.run('BotID_die_ich_nicht_preisgebe')
