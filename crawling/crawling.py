# # 뉴스 중간 중간에 tts 되도록 수정해야함
# # 그 외에 자잘한 부분 생각나는데로 기록하고 수정해야함

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
    chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않음 (백그라운드 실행)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # WebDriver 설정
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    section_dict = {100: '정치', 101: '경제', 102: '사회', 103: '생활/문화', 104: '세계', 105: 'IT/과학'}

    # 텍스트 파일로 요약 내용을 저장
    # with open("output.txt", "w", encoding="utf-8") as file:
    for address in [100, 101, 102, 103, 104, 105]:
        
        # 웹 페이지 열기
        url = f'https://news.naver.com/section/{address}'  # 원하는 URL을 입력하세요.
        driver.get(url)
        
        # 페이지가 로드될 때까지 대기 (필요에 따라 시간 조정)
        time.sleep(3)
        
        # 특정 클래스 네임의 <a> 태그 찾기
        links = driver.find_elements(By.CLASS_NAME, 'sa_thumb_link._NLOG_IMPRESSION')  # 클래스 네임을 사용해 <a> 태그를 선택합니다.
        
        # 각 링크로 이동하여 작업 수행
        cnt = 1
        idx = 0
        while cnt <= 5 and idx < len(links):
            # 각 링크의 href 속성 가져오기
            href = links[idx].get_attribute('href')
            
            # 새로운 탭에서 링크 열기
            driver.execute_script("window.open(arguments[0]);", href)
            
            # 새 탭으로 전환
            driver.switch_to.window(driver.window_handles[-1])
            
            # 페이지가 로드될 때까지 대기
            time.sleep(3)
            
            try:
                # 요약 버튼이 있는 div를 찾고 클릭
                summary_button = driver.find_element(By.CLASS_NAME, '_toggle_btn._SUMMARY_BTN')
                summary_button.click()
                
                # 요약 내용이 로드될 때까지 대기
                time.sleep(2)

                # 요약 내용을 추출
                summary_content = driver.find_element(By.CLASS_NAME, '_SUMMARY_CONTENT_BODY')
                summary_text = summary_content.text
                
                # 파일에 요약 내용 저장
                # file.write(f"Page {idx+1} - Summary:\n{summary_text}\n\n")
                with open("output.txt", "w") as f:
                    f.write(f"{section_dict[address]} {cnt} 번 뉴스 요약입니다. {summary_text}")
                    print(summary_text)
                
                print(f"Page {idx+1} - Summary saved.")
                
                cnt += 1
                
            except Exception as e:
                print(f"Page {idx+1} - an error occurred: {str(e)}")
            
            # 현재 탭 닫기
            driver.close()
            
            # 원래 탭으로 돌아가기
            driver.switch_to.window(driver.window_handles[0])
            
            idx += 1

    # 브라우저 닫기
    driver.quit()

crawling_naver_news()