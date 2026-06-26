from datetime import datetime, timedelta
from ..base_crawler import BaseCrawler
from ..notion_handler import get_recent_entries
from ..llm_handler import generate_weekly_tech_blog_post
from ..utils import send_slack_message
from config import BOANISSUE_DATABASE_ID

class WeeklyTechCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "주간 기술 키워드"

    def run(self, publisher_service, enable_notion=True, enable_tistory=True):
        print(f"--- {self.source_name} 생성 시작 ---")
        try:
            # 최근 7일간의 Notion 데이터 가져오기 (제목 + 요약문 + URL)
            combined_text = get_recent_entries(BOANISSUE_DATABASE_ID)
            
            if not combined_text:
                print(f"[{self.source_name}] 최근 7일간 수집된 데이터가 없습니다.")
                return

            print(f"[{self.source_name}] 데이터 수집 완료 (길이: {len(combined_text)}자)")
            if len(combined_text) < 100:
                print(f"[DEBUG] 수집된 데이터가 너무 적습니다:\n{combined_text}")

            # 블로그 포스트 생성
            blog_title, blog_body = generate_weekly_tech_blog_post(combined_text)
            
            if not blog_title or "죄송합니다" in blog_title or "Sorry" in blog_title:
                 print(f"[ERROR] LLM 생성 실패. 원본 데이터 길이: {len(combined_text)}")
                 print(f"[DEBUG] 원본 데이터 미리보기 (앞 1000자):\n{combined_text[:1000]}")
                 send_slack_message(f"[ERROR] 주간 이슈 생성 실패 (LLM 거부): {blog_title}")
                 return

            date_str = datetime.now().strftime('%Y-%m-%d')
            
            # 블로그 포스트 발행 (Notion & Tistory)
            if publisher_service:
                publisher_service.publish_article(
                    title=blog_title,
                    content="주간 보안 이슈 심층 분석 리포트입니다.",
                    url="",
                    date=date_str,
                    category="주간이슈",
                    details=blog_body,
                    database_id=BOANISSUE_DATABASE_ID,
                    enable_notion=enable_notion,
                    enable_tistory=enable_tistory
                )

        except Exception as e:
            print(f"[{self.source_name}-ERROR] 생성 중 오류: {e}")
            send_slack_message(f"[ERROR] {self.source_name} 생성 중 오류: {e}")
