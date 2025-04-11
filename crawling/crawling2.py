from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

CHROME_DRIVER_PATH = os.path.join(os.path.dirname(__file__), '..', 'chromedriver.exe')
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

driver.get("https://brand.naver.com/lexon/products/8303249331")
driver.implicitly_wait(10)

with open("page_source.html", "w", encoding="utf-8") as f:
    f.write(driver.page_source)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

try:
    review_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//a[@role="tab" and .//span[text()="리뷰"]]'))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", review_tab)
    review_tab.click()
    print("리뷰 탭 클릭 성공!")
except Exception as e:
    print("리뷰 탭을 찾을 수 없습니다:", e)
