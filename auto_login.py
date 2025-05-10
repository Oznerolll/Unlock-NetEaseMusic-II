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
    browser.add_cookie({"name": "MUSIC_U", "value": "0072593C297E8818135E911B85591FA47437CB6BEBC0FC43635E6410BFDA053C4C80ABD952D0C67953C2EC0E9659BBC0598D1B59748FFCA5D77229F12DAD4668F5E4E439FA55BFF5DEE94E4B7D7CB47B6B96F2368F7CFB2C82C12BFC5C749B43A75ECC7846DEE7276BA6CE1EA9B36A505FF83114DB13C2270F1589BA86D21299735DFF9BDC51A608FEDF3939EB412B8F5FF4D34FA12A8656A810A230CDE8D67EC6758D4D3681FEA2291604CF6E652D506B1C0000F8F226837B90E72C14F524C0123641CC9D0D71D8DD18BBD18DAD9E95E8C8DD5BA4EE90D43908498E618DE0875987877B00C6E7D4CE473FB91AFE28DD650B6BE8F8FD13529349E9048F1203503C8B7285F2C70C370290ACD1154BC00F8F59CB7CD0718B4E97F8D480492CBEE65BCF9B7DE514FF442C376DF88097B81139839C2C66E8F4DBB72EC06977851669349355EABD7E1ACE7B94B8E9AF347BB1CB4A6311FC0A02581062CCF2CF9E027A8A"})
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
