import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # crawling.py 위치
CHROME_DRIVER_PATH = os.path.join(BASE_DIR, '..', 'chromedriver.exe')

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

url = 'https://brand.naver.com/lexon/products/8303249331'
driver.get(url)

# 리뷰 탭 기다렸다가 클릭
try:
    wait = WebDriverWait(driver, 10)
    review_tab = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//a[@role="tab" and .//span[text()="리뷰"]]')
        )
    )
    review_tab.click()
    time.sleep(2)
except Exception as e:
    print("리뷰 탭을 찾을 수 없습니다:", e)
    driver.quit()
    exit()

# 이후 코드는 동일 (스크롤 등)
for _ in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    try:
        more_button = driver.find_element(By.CLASS_NAME, 'YEtwtZFlfU')
        more_button.click()
        time.sleep(2)
    except:
        pass

# 리뷰 추출 (임시 클래스 기준)
review_elements = driver.find_elements(By.CLASS_NAME, 'YEtwtZFlfU._1Y6hiXQpGe')
review_texts = [el.text.strip() for el in review_elements if el.text.strip()]

driver.quit()

df = pd.DataFrame(review_texts, columns=['Review'])
print(df.head())
