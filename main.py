from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json


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
    if os.path.exists(cookie_path):
        driver.get("https://www.geoguessr.com")
        load_cookie(driver, cookie_path)
        driver.refresh()
        time.sleep(3)
        if driver.current_url != "https://www.geoguessr.com/de/signin":
            navigate_to_party_page(driver)
            return driver

    driver.get("https://www.geoguessr.com/de/signin")
    time.sleep(2)
    email_input = driver.find_element(By.CSS_SELECTOR, "input[data-qa='email-field']")
    email_input.send_keys(email)
    password_input = driver.find_element(By.CSS_SELECTOR, "input[data-qa='password-field']")
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)
    save_cookie(driver, cookie_path)
    navigate_to_party_page(driver)
    return driver


def navigate_to_party_page(driver):
    driver.get("https://www.geoguessr.com/party")
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[2]/div[2]/main/div/div[2]/div/div/div[2]/div/div/div[1]/div/button")))
    button.click()

    # Warte, bis das Input-Feld geladen ist, und lese dann den Textinhalt aus
    input_field = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div[2]/div/div[2]/div[4]/div/div/div/div/span/input")))
    text_content = input_field.get_attribute("value")
    print("Textinhalt des Feldes:", text_content)


if __name__ == "__main__":
    email = "ben-hobson@hotmail.co.uk"
    password = "Theappletree1"
    driver = geoguessr_sign_in(email, password)