# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00D67A87F5FA83B155BF5B267787DE99DF7127921ED7691B2BFA5C87669D96C7C5ACAD546B44FE227415BD5117CCFF898D3A33FBD4059297079D2F33BFEE8DA7A9E201603B0B5ED8C20B1786C0F7B6469AFE1699E03C3C6752F1B7B594F5ECAF969CB8D34DE10D39E629BF5EFF5342D7057DDBD3BA7A4ADE93EE3B491D2DF530FFD181ED9AC1D080D0D60B34515F263CE6B2BE2B4A2CDFBDC48F75FDEA174C3F8A00F7E8A59A8C3A5A78960B7FB86A627505C4981DFC2B2FD8F69B2E70EA534E268051605D2096A1C76924418FCE5D2E40067CB4E69286C65E05BCFBB75AF49952C693CE73CB9CE9F57986B9EFF76CE3C081A4678F0469186EC09B070DD286553A8ED9F31BC15626C9A710952E215F5645C1BFCDFBA9F305B0FEA597DC7F0D7770A5719E8C77C5F74389E10AA0067E22E6458012914DD655421679480F157778585397204B1AAAC544A77A6530F135D5287E723A22CE29E59D46F3036430A149C9"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
