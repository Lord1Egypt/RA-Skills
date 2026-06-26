import subprocess
import json
from bs4 import BeautifulSoup
from datetime import datetime
import re
import urllib.parse
import warnings
warnings.filterwarnings('ignore')

from ..base_crawler import BaseCrawler
from ..utils import date_re, send_slack_message
from ..notion_handler import Duplicate_check
from config import BOANISSUE_DATABASE_ID

class SKShieldusCrawler(BaseCrawler):
    def __init__(self):
        super().__init__()
        self.source_name = "SK 쉴더스"
        self.base_url = "https://www.skshieldus.com/kor/blog.do"

    def run(self, publisher_service):
        processing_queue = []
        seen_urls = set()
        scan_total = 0
        scan_success_count = 0
        scan_duplicate_count = 0
        scan_old_count = 0
        scan_error_count = 0
        process_success_count = 0
        process_error_count = 0

        try:
            # curl로 HTML 가져오기 (레거시 SSL 지원)
            print(f"[{self.source_name}] curl로 페이지 로드 중...")
            
            curl_command = [
                'curl',
                '-s',  # Silent mode
                '-L',  # Follow redirects
                '-k',  # Allow insecure SSL
                '--connect-timeout', '30',
                '--max-time', '60',
                '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                self.base_url
            ]
            
            result = subprocess.run(curl_command, capture_output=True, text=True, timeout=90)
            
            if result.returncode != 0:
                print(f"[{self.source_name}] curl failed: {result.stderr[:100]}")
                return {
                    "source": self.source_name,
                    "success": 0,
                    "duplicate": 0,
                    "old": 0,
                    "error": 1,
                    "total": 0
                }
            
            html_content = result.stdout
            soup = BeautifulSoup(html_content, 'html.parser')
            
            allowed_path_pattern = re.compile(r"^/blog-security/(eqst-idx-\d+|security-trend-idx-\d+)$")
            
            articles = []
            
            # 다양한 선택자 시도
            selectors = [
                'div.blog-collection-item',
                'div.blog-item',
                'article',
                '.post-item',
            ]
            
            items = []
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    print(f"[{self.source_name}] Found {len(items)} items with selector: {selector}")
                    break
            
            if not items:
                # 대체 선택자로 다시 시도
                items = soup.find_all('a', href=allowed_path_pattern)
                print(f"[{self.source_name}] Found {len(items)} items with href pattern")
            
            for item in items:
                try:
                    # 링크 찾기
                    if item.name == 'a':
                        link_tag = item
                        href = link_tag.get('href', '').strip()
                        
                        # 부모 요소에서 제목 찾기
                        parent = item.find_parent('div', class_=re.compile(r'blog'))
                        title_tag = parent.select_one('.text-middle.text-bold.text-ellipsis') if parent else None
                        title = title_tag.get_text(strip=True) if title_tag else link_tag.get_text(strip=True)
                    else:
                        link_tag = item.select_one('a') or item.find('a')
                        if not link_tag:
                            continue
                        href = link_tag.get('href', '').strip()
                        
                        title_tag = (
                            item.select_one('.text-middle.text-bold.text-ellipsis') or
                            item.select_one('h2') or
                            item.select_one('h3') or
                            item.select_one('.title') or
                            link_tag
                        )
                        title = title_tag.get_text(strip=True) if title_tag else ''
                    
                    if not href or not title:
                        continue
                    
                    # URL 생성
                    article_url = urllib.parse.urljoin(self.base_url, href)
                    
                    if not title or not article_url:
                        continue
                    
                    # 날짜 찾기
                    date_tag = (
                        item.select_one('.blog-item-landscape-header') or
                        item.select_one('.date') or
                        item.select_one('time') or
                        item.select_one('.post-date') or
                        (item.find_parent() and item.find_parent().select_one('.date'))
                    )
                    
                    posting_date = None
                    if date_tag:
                        date_text = date_tag.get_text(strip=True).replace('.', '').replace(' ', '')
                        if len(date_text) >= 8:
                            try:
                                posting_date = datetime.strptime(date_text[:8], "%Y%m%d")
                            except ValueError:
                                pass
                    
                    articles.append({
                        "url": article_url, 
                        "title": title,
                        "date": posting_date
                    })
                    
                except Exception as e:
                    scan_error_count += 1
                    continue
            
            scan_total = len(articles)
            print(f"[{self.source_name}] 총 {scan_total}개의 게시글 발견")
            
            # Processing Phase
            for article in articles:
                try:
                    article_url = article['url']
                    title = article['title']
                    posting_date = article.get('date')
                    
                    # URL 중복 체크
                    if article_url in seen_urls:
                        scan_duplicate_count += 1
                        continue
                    seen_urls.add(article_url)
                    
                    # 날짜 처리
                    # 날짜를 찾지 못하면 상세 페이지에서 다시 시도
                    if posting_date is None:
                        scan_old_count += 1
                        continue
                    
                    if not self.is_recent(posting_date):
                        scan_old_count += 1
                        continue
                    
                    # Notion 중복 체크
                    duplicate_status = Duplicate_check(article_url, BOANISSUE_DATABASE_ID)
                    if duplicate_status == 0:
                        # 상세 페이지도 curl로 가져오기
                        final_content = "내용 없음"
                        
                        try:
                            detail_command = [
                                'curl',
                                '-s',
                                '-L',
                                '-k',
                                '--connect-timeout', '15',
                                '--max-time', '30',
                                '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                                article_url
                            ]
                            
                            detail_result = subprocess.run(detail_command, capture_output=True, text=True, timeout=45)
                            
                            if detail_result.returncode == 0:
                                detail_soup = BeautifulSoup(detail_result.stdout, 'html.parser')
                                
                                # 날짜를 찾지 못했다면 상세 페이지에서 다시 시도
                                if posting_date is None:
                                    detail_date_tag = (
                                        detail_soup.select_one('.date') or
                                        detail_soup.select_one('time') or
                                        detail_soup.select_one('.post-date') or
                                        detail_soup.select_one('.blog-date') or
                                        detail_soup.select_one('[class*="date"]')
                                    )
                                    
                                    if detail_date_tag:
                                        date_text = detail_date_tag.get_text(strip=True).replace('.', '').replace(' ', '')
                                        if len(date_text) >= 8:
                                            try:
                                                posting_date = datetime.strptime(date_text[:8], "%Y%m%d")
                                            except ValueError:
                                                pass
                                
                                # 그래도 날짜를 찾지 못했다면 제외
                                if posting_date is None:
                                    scan_old_count += 1
                                    continue
                                
                                # 본문 추출
                                content_selectors = [
                                    'div.blog-content',
                                    'div.content',
                                    'article',
                                    '.post-content',
                                    '.entry-content',
                                ]
                                
                                for selector in content_selectors:
                                    content_div = detail_soup.select_one(selector)
                                    if content_div:
                                        final_content = content_div.get_text(separator='\n', strip=True)[:1000]
                                        break
                        except Exception as e:
                            print(f"[{self.source_name}-DETAIL] Error: {e}")
                        
                        # 기사 데이터 생성
                        article_data = {
                            'title': title,
                            'content': final_content,
                            'url': article_url,
                            'source': self.source_name,
                            'category': 'SK쉴더스',
                            'posting_date': posting_date,
                        }
                        
                        # Publisher Service에 전달
                        if publisher_service:
                            try:
                                publisher_service.add_article(article_data)
                                process_success_count += 1
                                print(f"✅ [{self.source_name}] {title[:50]}...")
                            except Exception as e:
                                process_error_count += 1
                                print(f"❌ [{self.source_name}-PUBLISH] {title[:30]}: {e}")
                        else:
                            processing_queue.append(article_data)
                            process_success_count += 1
                    
                    else:
                        scan_duplicate_count += 1
                
                except Exception as e:
                    scan_error_count += 1
                    print(f"[{self.source_name}-ARTICLE] Error: {e}")
                    continue
            
            print(f"[{self.source_name}] 크롤링 완료")
            
            return {
                "source": self.source_name,
                "success": process_success_count,
                "duplicate": scan_duplicate_count,
                "old": scan_old_count,
                "error": scan_error_count,
                "total": scan_total,
                "queue": processing_queue
            }
        
        except subprocess.TimeoutExpired:
            print(f"[{self.source_name}-FATAL] Timeout")
            return {
                "source": self.source_name,
                "success": 0,
                "duplicate": 0,
                "old": 0,
                "error": 1,
                "total": 0
            }
        
        except Exception as e:
            print(f"[{self.source_name}-FATAL] Error: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "source": self.source_name,
                "success": 0,
                "duplicate": 0,
                "old": 0,
                "error": 1,
                "total": 0
            }
