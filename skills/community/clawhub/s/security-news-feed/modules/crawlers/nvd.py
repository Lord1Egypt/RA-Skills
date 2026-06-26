import requests
from datetime import datetime, timedelta

from ..base_crawler import BaseCrawler
from ..utils import send_slack_message
from ..llm_handler import CVE_details_text, translate_text
from config import BOANISSUE_DATABASE_ID

class NVDCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "NVD CVE"
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    def run(self, publisher_service, enable_notion=True, enable_tistory=True):
        print(f"--- {self.source_name} 크롤링 시작 ---")
        
        # 최근 7일간의 CVE 조회
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        pub_start_date = start_date.strftime('%Y-%m-%dT%H:%M:%S.000')
        pub_end_date = end_date.strftime('%Y-%m-%dT%H:%M:%S.000')

        params = {
            'pubStartDate': pub_start_date,
            'pubEndDate': pub_end_date,
            'cvssV3Severity': 'CRITICAL' # CRITICAL 등급만 필터링
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            vulnerabilities = data.get('vulnerabilities', [])
            print(f"[{self.source_name}] 검색된 Critical CVE 개수: {len(vulnerabilities)}")

            if not vulnerabilities:
                print(f"[{self.source_name}] 새로운 Critical CVE가 없습니다.")
                return {
                    "source": self.source_name,
                    "success": 0,
                    "duplicate": 0,
                    "old": 0,
                    "error": 0,
                    "total": 0
                }

            all_descriptions_for_summary = []

            for vuln in vulnerabilities:
                cve = vuln.get('cve', {})
                cve_id = cve.get('id', '제목 없음')
                descriptions = cve.get('descriptions', [])
                description_en = next((desc['value'] for desc in descriptions if desc['lang'] == 'en'), '내용 없음')
                
                # [NEW] 제목(설명) 번역
                # GLM API rate limit을 피하기 위해 번역 건너뜀
                description_ko = description_en  # 번역 생략
                
                all_descriptions_for_summary.append(f"CVE ID: {cve_id}\n설명(영문): {description_en}\n설명(한글): {description_ko}\n")

            combined_cve_text = "\n---\n".join(all_descriptions_for_summary)

            if all_descriptions_for_summary:
                print(f"총 {len(vulnerabilities)}개의 CVE 수집 완료")
                
                # GLM API rate limit 피하기 위해 LLM 호출 생략
                # 간단한 리포트 생성
                raw_generated_blog_title = f"주간 Critical CVE 리포트 ({datetime.now().strftime('%Y-%m-%d')})"
                generated_blog_body = f"## Critical CVE 목록\n\n{combined_cve_text}"

                date_str = datetime.now().strftime('%Y-%m-%d')
                
                # 주간 리포트이므로 URL은 NVD 검색 결과 페이지 등으로 대체하거나 생략
                report_url = f"https://nvd.nist.gov/vuln/search/results?form_type=Advanced&results_type=overview&search_type=all&pub_start_date={start_date.strftime('%m/%d/%Y')}&pub_end_date={end_date.strftime('%m/%d/%Y')}&cvssV3Severity=CRITICAL"

                if publisher_service:
                    publisher_service.publish_article(
                        title=raw_generated_blog_title,
                        content=generated_blog_body[:200] + "...", # 요약 내용 (Notion 리스트용)
                        url=report_url,
                        date=date_str,
                        category="Weekly CVE",
                        details=generated_blog_body,
                        database_id=BOANISSUE_DATABASE_ID,
                        enable_notion=enable_notion,
                        enable_tistory=enable_tistory
                    )

        except Exception as e:
            print(f"[{self.source_name}-ERROR] 크롤링 중 오류: {e}")
            send_slack_message(f"[ERROR] {self.source_name} 크롤링 중 오류: {e}")
            
            return {
                "source": self.source_name,
                "success": 0,
                "duplicate": 0,
                "old": 0,
                "error": 1,
                "total": 0
            }

