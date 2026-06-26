# modules/tistory_handler.py
"""
Selenium을 사용하여 티스토리 블로그에 글을 자동으로 게시하는 모듈입니다.
티스토리 Open API 종료로 인해 브라우저 자동화 방식을 사용합니다.
"""

import time
import os
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# config.py에서 설정값 가져오기
from config import TISTORY_BLOG_NAME, CHROME_USER_DATA_DIR, CHROME_PROFILE_NAME

def get_driver():
    """
    사용자 프로필을 로드하여 Chrome Driver를 설정합니다.
    이미 로그인된 세션을 유지하기 위함입니다.
    """
    chrome_options = Options()
    
    # 사용자 데이터 디렉토리 설정 (로그인 세션 유지)
    if os.path.exists(CHROME_USER_DATA_DIR):
        chrome_options.add_argument(f"user-data-dir={CHROME_USER_DATA_DIR}")
        chrome_options.add_argument(f"profile-directory={CHROME_PROFILE_NAME}")
    else:
        print(f"[WARNING] Chrome 사용자 데이터 폴더를 찾을 수 없습니다: {CHROME_USER_DATA_DIR}")
        print("로그인이 유지되지 않을 수 있습니다.")

    # 기타 옵션
    chrome_options.add_argument("--start-maximized") # 창 최대화
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 탐지 방지
    chrome_options.add_argument("--no-sandbox") # [FIX] DevToolsActivePort 에러 방지
    chrome_options.add_argument("--disable-dev-shm-usage") # [FIX] 메모리 부족 에러 방지
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 드라이버 실행
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver

def post_to_tistory(title_text, content_text, tags_text, category_name=None, source_url_text=None):
    """
    Selenium을 사용하여 티스토리에 글을 작성합니다.
    """
    print(f"티스토리 자동 포스팅 시작 (Selenium): '{title_text}'")
    
    driver = None
    try:
        driver = get_driver()
        
        # 1. 글쓰기 페이지 이동
        write_url = f"https://{TISTORY_BLOG_NAME}.tistory.com/manage/post"
        driver.get(write_url)
        time.sleep(3) # 페이지 로딩 대기

        # 로그인 확인 (URL이 login으로 리다이렉트되었는지 확인)
        if "login" in driver.current_url:
            print("[ERROR] 티스토리 로그인이 필요합니다. 'setup_login.py'를 실행하여 먼저 로그인해주세요.")
            return False

        # 2. 제목 입력
        # 티스토리 에디터의 제목 입력 필드 찾기 (ID나 Placeholder 등으로 식별)
        try:
            title_area = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "post-title-inp"))
            )
            title_area.click()
            title_area.clear()
            title_area.send_keys(title_text)
        except Exception as e:
            print(f"[ERROR] 제목 입력 필드를 찾을 수 없습니다: {e}")
            return False

        # 3. 본문 입력 (HTML 모드 전환 후 입력이 가장 확실함)
        # 기본모드 -> HTML 모드 전환 버튼 찾기
        try:
            # 더보기(...) 버튼 클릭
            more_button = driver.find_element(By.ID, "mceu_18-open") # 에디터 상단 툴바의 더보기 버튼 ID (변동 가능성 있음)
            # 또는 '기본모드'라고 적힌 버튼 찾기
            mode_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., '기본모드')]"))
            )
            mode_button.click()
            time.sleep(0.5)
            
            html_mode = driver.find_element(By.XPATH, "//div[@data-value='html']")
            html_mode.click()
            time.sleep(0.5)
            
            # HTML 에디터 영역 찾기
            editor_area = driver.find_element(By.CLASS_NAME, "CodeMirror-code")
            
            # 출처 추가
            final_content = content_text
            if source_url_text:
                final_content += f'<br><br><p><b>출처:</b> <a href="{source_url_text}" target="_blank">{source_url_text}</a></p>'
            
            # 클립보드를 이용한 붙여넣기 (가장 안정적)
            pyperclip.copy(final_content)
            editor_area.click()
            
            # Ctrl+V (Mac은 Command+V)
            editor_area.send_keys(Keys.CONTROL, 'v') 
            time.sleep(1)
            
        except Exception as e:
            print(f"[ERROR] HTML 모드 전환 및 본문 입력 실패: {e}")
            # 대체: 기본 에디터에 텍스트만이라도 입력 시도
            try:
                driver.switch_to.default_content()
                iframe = driver.find_element(By.ID, "editor-tistory_ifr")
                driver.switch_to.frame(iframe)
                body = driver.find_element(By.TAG_NAME, "body")
                body.send_keys(final_content)
                driver.switch_to.default_content()
            except:
                return False

        # 4. 태그 입력
        try:
            tag_input = driver.find_element(By.ID, "tagText")
            tag_input.send_keys(tags_text)
            tag_input.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"[WARNING] 태그 입력 실패: {e}")

        # 5. 카테고리 선택 (선택 사항)
        if category_name:
            try:
                category_select = driver.find_element(By.ID, "category-btn")
                category_select.click()
                time.sleep(0.5)
                # 카테고리 검색 또는 클릭 로직 필요 (복잡할 수 있어 일단 생략하거나 기본값 사용)
            except:
                pass

        # 6. 발행 버튼 클릭
        try:
            # 하단 '완료' 버튼
            publish_layer_btn = driver.find_element(By.CLASS_NAME, "btn_apply") # 또는 ID 'publish-layer-btn'
            publish_layer_btn.click()
            time.sleep(1)
            
            # 최종 '발행' 버튼 (공개 설정 레이어 팝업)
            final_publish_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "publish-btn"))
            )
            final_publish_btn.click()
            
            print("[SUCCESS] 티스토리 발행 클릭 완료")
            time.sleep(3) # 발행 완료 대기
            return True
            
        except Exception as e:
            print(f"[ERROR] 발행 버튼 클릭 실패: {e}")
            return False

    except Exception as e:
        print(f"[CRITICAL] Selenium 작업 중 오류 발생: {e}")
        return False
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    # 테스트용
    print("티스토리 포스팅 테스트")
    post_to_tistory("테스트 제목", "<p>테스트 본문입니다.</p>", "테스트,보안", source_url_text="https://example.com")