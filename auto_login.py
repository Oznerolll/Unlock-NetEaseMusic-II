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
    browser.add_cookie({"name": "MUSIC_U", "value": "0046FC5BEBF4BA7F2E698919A52EB8DE7B9D7915B5FF1449A03F29E129032F2CE5C8B09B418488BC75256529C6B3FCA1CB916F15FFFA5E57524DF8D53463DA703F64164587AE6D8F6CE8615577980A85C6D12D4D34381E8502FCA0491F42B749421425246E7FA9388E47A4F06D56F5124E0344C94B45551E4D7CA3D95B861619C8E23DCBC20EF350C96E55415B5F447CE935571907F7A2082B4C4C75BC5645016A78473CBEFCCC652ECD56761BF403A0C9D4EF56B97B6545B24BA35ABBA064968204A74479CDC4848BC54BE102D1013B2888B6D1AF07CE5BE2472B605C2B356AA64817A46A186303DB639C5FECD45BF8B8BD1BD880241710EDAD1EEDAA64D5443918AFB95F78BD9DC2E05197662D1D0152531DE8A83745080EB99728E54717332A062B23CA4C7B657991EC227AA1C062D3C32C7A71ED2755F9420D781D050FC4EC167B5675F372B4A19BA2480952C256844017DF3A5C7205FCD3CBAAA16263AB2E"})
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
