from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# 경로 설정
CHROME_DRIVER_PATH = os.path.join(os.path.dirname(__file__), '..', 'chromedriver.exe')

options = Options()
# options.add_argument('--headless')  # 디버깅 중일 땐 꺼두기
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

# 네이버 상품 URL
url = "https://brand.naver.com/lexon/products/8303249331"
driver.get(url)
driver.implicitly_wait(10)

# 리뷰 탭 클릭
try:
    review_tab = driver.find_element(By.XPATH, '//a[@role="tab" and .//span[contains(text(), "리뷰")]]')
    driver.execute_script("arguments[0].scrollIntoView(true);", review_tab)
    review_tab.click()
    time.sleep(2)
except Exception as e:
    print("리뷰 탭 클릭 실패:", e)
    driver.quit()
    exit()

# 첫 번째 리뷰 텍스트 가져오기
try:
    # 리뷰가 로딩될 때까지 대기
    time.sleep(3)

    # 리뷰 요소 선택 (text()는 Selenium에서 지원 안 되므로, span 요소를 선택)
    first_review_element = driver.find_element(By.XPATH,
        '//*[@id="REVIEW"]/div/div[3]/div[2]/ul/li[1]/div/div/div/div[1]/div/div[1]/div[2]/div/span')
    print("리뷰 내용:", first_review_element.text)

except Exception as e:
    print("리뷰 텍스트 추출 실패:", e)

driver.quit()