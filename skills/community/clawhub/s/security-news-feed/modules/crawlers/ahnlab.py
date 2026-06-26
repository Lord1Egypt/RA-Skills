import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

from ..base_crawler import BaseCrawler
from ..utils import date_re, send_slack_message
from ..notion_handler import Duplicate_check
# from ..llm_handler import summarize_text, details_text # Moved to Processor
from config import BOANISSUE_DATABASE_ID

class AhnLabCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "안랩 ASEC"
        self.base_url = "https://asec.ahnlab.com/ko/"

    def run(self, publisher_service):
        # 1. Scanning Phase
        processing_queue = [] # Not used in Stream mode but kept for compatibility logic
        seen_urls = set()
        scan_total = 0
        scan_success_count = 0
        scan_duplicate_count = 0
        scan_old_count = 0
        scan_error_count = 0
        process_success_count = 0
        process_error_count = 0
        
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(self.base_url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            public_content_section = soup.select_one('section[data-id="231bd9f"]')
            if not public_content_section:
                # print(f"[{self.source_name}-ERROR] 'AhnLab 공개 콘텐츠 섹션을 찾을 수 없습니다.")
                return {
                     "source": self.source_name, "success": 0, "duplicate": 0, "old": 0, "error": 1, "total": 0
                }

            articles = []
            for post_title_tag in public_content_section.select('h3.post-title'):
                try:
                    link_tag = post_title_tag.find('a')
                    if not link_tag or not link_tag.get('href'): continue
                    
                    title = link_tag.get_text(strip=True)
                    url = link_tag['href']
                    
                    parent = post_title_tag.parent
                    date_tag = parent.select_one('li.slider-meta-date')
                    
                    posting_date = None
                    if date_tag:
                        date_text = date_tag.get_text(strip=True)
                        posting_date = date_re(date_text)
                    
                    articles.append({
                        "url": url,
                        "title": title,
                        "date": posting_date
                    })
                except Exception as e:
                    # print(f"[{self.source_name}-WARN] 목록 페이지 파싱 중 오류: {e}")
                    scan_error_count += 1

            scan_total = len(articles)

            for art in articles:
                try:
                    article_url = art["url"]
                    title = art["title"]
                    posting_date = art["date"]

                    # 1. 날짜 체크 (90일)
                    if posting_date:
                        if not self.is_recent(posting_date):
                            scan_old_count += 1
                            continue
                    
                    # 2. 중복 체크
                    if Duplicate_check(article_url, BOANISSUE_DATABASE_ID) == 1:
                        scan_duplicate_count += 1
                        continue
                    
                    # 유효한 게시물 검증 (상세 페이지 파싱에 직접 관함, Phase 2에서 처리해도 됨)
                    # AhnLab?� ?�세 ?�이지 가???�짜�??�시 ?�인?�야 ???�도 ?�음.
                    # ?��?�?'Scanning'??빨리 ?�내?�면 ?�기???�세 ?�이지 ?�청???�는 것�? ?�림.
                    # 그래???�확?�을 ?�해 ?�기???�세 ?�이지 ?�인???�고 Queue???�는 것이 맞음.
                    # 'Scan' ?�이즈에??Network I/O???�용?? LLM??문제??
                    
                    detail_response = requests.get(article_url, headers=headers, timeout=15)
                    detail_response.raise_for_status()
                    detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

                    # ?�짜 ?�확??
                    if not posting_date:
                        date_tag = detail_soup.select_one('li.slider-meta-date')
                        date_text = date_tag.get_text(strip=True) if date_tag else None
                        posting_date = date_re(date_text)
                        
                        if not posting_date:
                            scan_error_count += 1
                            continue
                        
                        if not self.is_recent(posting_date):
                            scan_old_count += 1
                            continue

                    content_tag = detail_soup.select_one('div.entry-content')
                    content = content_tag.get_text('\n', strip=True) if content_tag else ''
                    
                    if not content:
                        scan_error_count += 1
                        continue

                    category_tags = detail_soup.select('a.news-cat_Name')
                    category = ', '.join([tag.get_text(strip=True) for tag in category_tags]) or '기�?'
                    
                    # ---------------------------------------------------------
                    # ?�에 ?�재 (Producer-Consumer)
                    # ---------------------------------------------------------
                    try:
                        # print(f"[{self.source_name}] ???�효 기사 발견! ?�에 ?�록: {title[:30]}...")

                        if publisher_service:
                            publisher_service.publish_article(
                                title=title,
                                content=content, # Raw Content
                                url=article_url,
                                date=posting_date.strftime('%Y-%m-%d'),
                                category=f"AhnLab ASEC/{category}",
                                details=content, # Raw Content
                                database_id=BOANISSUE_DATABASE_ID
                            )
                        
                        scan_success_count += 1
                        
                    except Exception as e:
                        print(f"[{self.source_name}-ERROR] ???�록 �??�류 ({title}): {e}")
                        scan_error_count += 1

                    scan_success_count += 1
                    time.sleep(0.5)

                except Exception as e:
                    # print(f"[{self.source_name}-ERROR] 개별 ??�� ?�캔 �??�류: {e}")
                    scan_error_count += 1
                    
        except Exception as e:
            # print(f"[{self.source_name}-ERROR] ?�캔 �??�류: {e}")
            scan_error_count += 1
        
        return {
            "source": self.source_name,
            "success": process_success_count,
            "duplicate": scan_duplicate_count,
            "old": scan_old_count,
            "error": scan_error_count + process_error_count,
            "total": scan_total
        }

