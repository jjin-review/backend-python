from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import os

# 드라이버 경로 설정
CHROME_DRIVER_PATH = os.path.join(os.path.dirname(__file__), '..', 'chromedriver.exe')

options = Options()
# options.add_argument('--headless')  # 크롬 창 끄기설정
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=options)

url = "https://brand.naver.com/lexon/products/8303249331"
driver.get(url)
driver.implicitly_wait(10)

# 스크롤 내리기
def scroll_to_bottom_slowly(pause_time=0.5, scroll_step=300):
    current_height = 0
    total_height = driver.execute_script("return document.body.scrollHeight")
    while current_height < total_height:
        current_height += scroll_step
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        time.sleep(pause_time)
        total_height = driver.execute_script("return document.body.scrollHeight")

# 해당 페이지 리뷰 가져오기
def collect_reviews_on_page():
    page_reviews = []
    time.sleep(2)

    for i in range(1, 21):
        try:
            base_xpath = f'//*[@id="REVIEW"]/div/div[3]/div[2]/ul/li[{i}]/div/div/div/div[1]/div/div[1]/div[2]/div'
            # 해당 div 아래의 모든 span 태그 가져오기
            spans = driver.find_elements(By.XPATH, base_xpath + "/span")
            if spans:
                review_text = spans[-1].text.strip()  # 마지막 span의 텍스트 추출
                if review_text:
                    page_reviews.append(review_text)
        except NoSuchElementException:
            continue
    return page_reviews

# 번호 넘기기
def go_to_page(page_num):
    try:
        xpath = f'//*[@id="REVIEW"]/div/div[3]/div[2]/div/div/a[{page_num + 1}]'
        page_btn = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].scrollIntoView(true);", page_btn)
        time.sleep(1)
        page_btn.click()
        time.sleep(2)
        return True
    except:
        return False

reviews = []
scroll_to_bottom_slowly()

# 1~3 페이지 리뷰 가져오기
for page in range(1, 4):
    print(f"\n >> {page}페이지 리뷰 수집 중")
    if page != 1:
        go_to_page(page)
    page_reviews = collect_reviews_on_page()
    reviews.extend(page_reviews)

driver.quit()

# 결과
print(f"\n총 {len(reviews)}개의 리뷰를 수집.\n")
for idx, review in enumerate(reviews, 1):
    print(f"{idx}. {review}")
###