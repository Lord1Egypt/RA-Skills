
import requests
import json
import logging
import markdown2
from typing import List, Optional, Dict
import time

from config import NOTION_API_TOKEN, TISTORY_BLOG_NAME, GUIDE_DATABASE_ID
from modules.notion_handler import create_notion_page, Duplicate_check, get_data_source_info
from modules.tistory_handler import post_to_tistory
from modules.utils import send_slack_message

def filter_bmp_characters(text):
    """
    Tistory API 등에서 허용하지 않는 BMP(Basic Multilingual Plane) 이외의 문자(이모지 등)를 제거합니다.
    """
    if not text:
        return ""
    return "".join(c for c in text if c <= "\uFFFF")

class PublisherService:
    """
    기사 발행을 담당하는 서비스 클래스
    Notion 및 Tistory 발행 로직을 캡슐화
    """
    
    def __init__(self, 
                 enable_notion: bool = True, 
                 enable_tistory: bool = False,
                 notion_database_id: Optional[str] = None):
        self.enable_notion = enable_notion
        self.enable_tistory = enable_tistory
        self.notion_database_id = notion_database_id

    def publish_article(self, 
                       title: str, 
                       content: str, 
                       url: str, 
                       date: str, 
                       category: str,
                       details: str = "",
                       database_id: Optional[str] = None,
                       files: Optional[List[Dict[str, str]]] = None,
                       skip_duplicate_check: bool = False,
                       enable_notion: Optional[bool] = None,
                       enable_tistory: Optional[bool] = None) -> Dict[str, bool]:
        """
        기사를 설정된 플랫폼에 발행합니다.
        
        Args:
            title: 기사 제목
            content: 기사 본문 (요약문)
            url: 원문 URL
            date: 발행일 (YYYY-MM-DD)
            category: 카테고리 (예: NCSC, BoanNews)
            details: 추가 상세 설명
            database_id: Notion 데이터베이스 ID
            files: 첨부 파일 리스트 [{'path': '경로', 'name': '파일명'}]
            files: 첨부 파일 리스트 [{'path': '경로', 'name': '파일명'}]
            skip_duplicate_check: 중복 체크 스킵 여부
            enable_notion: (Optional) Notion 발행 활성화 여부 Override
            enable_tistory: (Optional) Tistory 발행 활성화 여부 Override
        
        Returns:
            Dict[str, bool]: {'notion': bool, 'tistory': bool}
        """
        
        results = {"notion": False, "tistory": False}
        
        # 설정 Override 확인
        use_notion = enable_notion if enable_notion is not None else self.enable_notion
        use_tistory = enable_tistory if enable_tistory is not None else self.enable_tistory
        
        # database_id는 실제로 database_id (notion_handler에서 data_source_id로 변환)
        database_id_to_use = database_id or self.notion_database_id
        
        print(f"\n📝 기사 발행 시작")
        print(f" 제목: {title}")
        print(f" DB ID: {database_id_to_use}")
        print(f" Notion: {use_notion}, Tistory: {use_tistory}")
        
        # ========== Notion 발행 ==========
        
        if use_notion:
            try:
                print(f" → Notion 발행 중...")
                
                # notion_handler에서 data_source_id를 자동으로 조회하여 처리
                result = create_notion_page(
                    title=title,
                    content=content,
                    url=url,
                    date=date,
                    category_=category,
                    details=details,
                    files=files,
                    DATABASE_ID=database_id_to_use
                )
                
                # result 값 확인 (None 또는 False가 아니면 성공)
                results["notion"] = bool(result)
                
                if results["notion"]:
                    print(f" ✅ Notion 발행 성공: {result}")
                else:
                    print(f" ❌ Notion 발행 실패")
                    send_slack_message(f"[ERROR] Notion 발행 실패 - {title}")
            
            except Exception as e:
                results["notion"] = False
                print(f" ❌ Notion 발행 실패: {e}")
                send_slack_message(f"[ERROR] Notion 발행 실패 - {title}: {e}")
        
        else:
            print(f" ⏭️ Notion 발행 비활성화")
        
        # ========== Tistory 발행 ==========
        
        if use_tistory:
            try:
                print(f" → Tistory 발행 중...")
                
                # Tistory 발행
                result = self._publish_to_tistory(
                    title=title,
                    content=content,
                    url=url,
                    date=date,
                    category=category,
                    details=details
                )
                
                results["tistory"] = result
                
                if result:
                    print(f" ✅ Tistory 발행 성공")
                else:
                    print(f" ❌ Tistory 발행 실패")
                    send_slack_message(f"[ERROR] Tistory 발행 실패 - {title}")
            
            except Exception as e:
                results["tistory"] = False
                print(f" ❌ Tistory 발행 실패: {e}")
                send_slack_message(f"[ERROR] Tistory 발행 실패 - {title}: {e}")
        
        else:
            print(f" ⏭️ Tistory 발행 비활성화")
        
        print(f"📝 기사 발행 완료: {results}\n")
        
        return results
    
    
    def _publish_to_tistory(self,
                           title: str,
                           content: str,
                           url: str,
                           date: str,
                           category: str,
                           details: str) -> bool:
        """
        Tistory에 기사를 발행합니다.
        
        Args:
            title: 기사 제목
            content: 기사 본문 (마크다운)
            url: 출처 URL
            date: 날짜
            category: 카테고리
            details: 상세 설명
        
        Returns:
            bool: 발행 성공 여부
        """
        
        try:
            # 마크다운 → HTML 변환
            html_content = markdown2.markdown(
                content,
                extras=["tables", "fenced-code-blocks"]
            )
            
            # BMP 문자 필터링
            filtered_content = filter_bmp_characters(html_content)
            
            # tistory_handler.post_to_tistory 호출
            success = post_to_tistory(
                title_text=title,
                content_text=filtered_content,
                tags_text=category,
                category_name=category,
                source_url_text=url
            )
            
            return success
        
        except Exception as e:
            print(f" Tistory 발행 내부 오류: {e}")
            return False
    
    
    def check_duplicate(self, url: str, database_id: Optional[str] = None) -> bool:
        """
        기사가 이미 발행되었는지 확인합니다.
        
        2025-09-03 버전 호환: Duplicate_check에서 data_source_id 자동 조회
        
        Args:
            url: 확인할 URL
            database_id: Notion 데이터베이스 ID
        
        Returns:
            bool: True면 중복 (이미 발행됨), False면 새로운 기사
        """
        
        database_id_to_use = database_id or self.notion_database_id
        
        if not database_id_to_use:
            print("[WARNING] database_id가 없어 중복 체크를 건너뜁니다")
            return False
        
        try:
            result = Duplicate_check(url, database_id_to_use)
            return result == 1  # 1이면 중복
        
        except Exception as e:
            print(f"[ERROR] 중복 체크 실패: {e}")
            return False
    
    
    def update_settings(self,
                       enable_notion: Optional[bool] = None,
                       enable_tistory: Optional[bool] = None,
                       notion_database_id: Optional[str] = None):
        """
        발행 설정을 변경합니다.
        
        Args:
            enable_notion: Notion 발행 활성화 여부
            enable_tistory: Tistory 발행 활성화 여부
            notion_database_id: Notion 데이터베이스 ID
        """
        
        if enable_notion is not None:
            self.enable_notion = enable_notion
        
        if enable_tistory is not None:
            self.enable_tistory = enable_tistory
        
        if notion_database_id is not None:
            self.notion_database_id = notion_database_id
            
            # data_source_id 조회 및 적용
            try:
                headers = {
                    "Authorization": f"Bearer {NOTION_API_TOKEN}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2025-09-03"
                }
                data_source_id, _ = get_data_source_info(notion_database_id, headers)
                if data_source_id:
                    self.notion_database_id = data_source_id
            except Exception as e:
                print(f"[WARN] data_source_id 조회 실패: {e}")
        
        # print("[INFO] PublisherService 설정 업데이트")
        # print(f" - Notion: {self.enable_notion}")
        # print(f" - Tistory: {self.enable_tistory}")
        # print(f" - DB ID: {self.notion_database_id}")