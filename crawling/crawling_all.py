from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def crawling_naver_news():

    # ChromeDriver 경로 설정
    chrome_driver_path = r"C:\chromedriver\chromedriver.exe"  # ChromeDriver의 경로를 지정하세요.

    # Chrome 옵션 설정
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")  # 브라우저 창을 열지 않음 (백그라운드 실행)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-javascript")  # 자바스크립트 비활성화

    # WebDriver 설정
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 텍스트 파일로 저장
    # with open("output.txt", "w", encoding="utf-8") as file:

        
    # 웹 페이지 열기
    url = f'https://www.musinsa.com/main/sneaker/ranking'  # 원하는 URL을 입력하세요.
    driver.get(url)
    
    # 페이지가 로드될 때까지 대기 (필요에 따라 시간 조정)
    time.sleep(3)
    
    # 특정 클래스 네임의 태그 찾기
    links = driver.find_elements(By.CLASS_NAME, 'sc-1m4cyao-2.bubXVJ.gtm-select-item')

    # print(links)

    for idx in range(10):

        href = links[idx].get_attribute('href')

        # 새로운 탭에서 링크 열기
        driver.execute_script("window.open(arguments[0]);", href)

        # 새 탭으로 전환
        driver.switch_to.window(driver.window_handles[-1])

        # 페이지가 로드될 때까지 대기
        # time.sleep(3)

        page_source = driver.page_source

        print(page_source)

        print('*' * 100)

        # 현재 탭 닫기
        driver.close()
        
        # 원래 탭으로 돌아가기
        driver.switch_to.window(driver.window_handles[0])

    # 브라우저 닫기
    driver.quit()

crawling_naver_news()