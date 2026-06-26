#!/usr/bin/env python3
"""
Security News Aggregator - 한국 보안 뉴스 자동 수집 및 요약
매시간 11개 보안 뉴스 소스에서 뉴스를 수집하고 GLM-5로 요약하여 Notion에 발행
"""

import os
import sys
import json
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import urllib.request
import urllib.error
import re

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('security-news')

class Config:
    """설정"""
    
    # GLM API 설정
    GLM_API_KEY = os.getenv('SECURITY_NEWS_GLM_API_KEY') or os.getenv('GLM_API_KEY')
    GLM_BASE_URL = os.getenv('GLM_BASE_URL', 'https://api.z.ai/api/coding/paas/v4')
    GLM_MODEL = "glm-5"
    GLM_MAX_TOKENS = 1000
    GLM_TEMPERATURE = 0.7
    
    # Notion 설정
    NOTION_API_KEY = os.getenv('NOTION_API_KEY')
    NOTION_DATABASE_ID = os.getenv('SECURITY_NEWS_DATABASE_ID')
    NOTION_ENABLED = bool(NOTION_API_KEY and NOTION_DATABASE_ID)
    
    # 뉴스 소스
    NEWS_SOURCES = {
        'krcert': {
            'name': 'KRCERT',
            'url': 'https://www.krcert.or.kr/krcert/secNoticeList.do',
            'type': 'web',
            'enabled': True
        },
        'ncsc': {
            'name': 'NCSC',
            'url': 'https://www.ncsc.go.kr/ncsc/notice/noticeList.do',
            'type': 'web',
            'enabled': True
        },
        'boho': {
            'name': 'Boho',
            'url': 'https://www.boho.or.kr/kr/bbs/list.do',
            'type': 'web',
            'enabled': True
        },
        'dailysec': {
            'name': 'Dailysec',
            'url': 'https://dailysecu.com/news',
            'type': 'web',
            'enabled': True
        },
        'kisa': {
            'name': 'KISA',
            'url': 'https://www.kisa.or.kr/notice',
            'type': 'web',
            'enabled': True
        }
    }
    
    # 키워드 필터
    KEYWORDS = [
        "취약점", "악성코드", "해킹", "랜섬웨어",
        "보안", "침해", "공격", "암호화",
        "인증", "방화벽", "악성", "피싱",
        "스파이웨어", "트로이목마", "봇넷",
        "CVE", "zero-day", "취약성"
    ]
    
    # 캐시 설정
    CACHE_DIR = Path('/tmp/security-news-cache')
    CACHE_TTL = 3600  # 1시간


class NewsItem:
    """뉴스 아이템"""
    
    def __init__(self, title: str, content: str, url: str, source: str, published_date: str = None):
        self.title = title
        self.content = content
        self.url = url
        self.source = source
        self.published_date = published_date or datetime.now().isoformat()
        self.summary = None
        self.detailed_analysis = None
        self.tags = []
    
    def to_dict(self) -> Dict:
        return {
            'title': self.title,
            'content': self.content,
            'url': self.url,
            'source': self.source,
            'published_date': self.published_date,
            'summary': self.summary,
            'detailed_analysis': self.detailed_analysis,
            'tags': self.tags
        }


class GLMSummarizer:
    """GLM-5 기반 뉴스 요약"""
    
    def __init__(self, config: Config):
        self.config = config
        self.api_key = config.GLM_API_KEY
        self.base_url = config.GLM_BASE_URL
        
        if not self.api_key:
            logger.warning("GLM API key not configured")
    
    def summarize(self, news_item: NewsItem) -> bool:
        """뉴스 요약"""
        
        if not self.api_key:
            # API 키 없으면 간단한 요약
            news_item.summary = news_item.content[:140] + "..."
            news_item.detailed_analysis = f"**배경**: {news_item.title}\n\n**주요 내용**: {news_item.content[:500]}"
            news_item.tags = self._extract_keywords(news_item.content)
            return True
        
        try:
            # GLM API 호출
            prompt = f"""
다음 보안 뉴스를 요약하고 분석해주세요.

제목: {news_item.title}
내용: {news_item.content[:1000]}

다음 형식으로 응답해주세요:

[140자 요약]
- 핵심 내용 3줄 요약

[상세 분석]
- 배경 설명
- 주요 내용
- 시사점
- 대응 방안

[태그]
#태그1 #태그2 #태그3
"""
            
            data = {
                "model": self.config.GLM_MODEL,
                "messages": [
                    {"role": "system", "content": "당신은 보안 전문가입니다. 보안 뉴스를 분석하고 요약합니다."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": self.config.GLM_TEMPERATURE,
                "max_tokens": self.config.GLM_MAX_TOKENS
            }
            
            req = urllib.request.Request(
                f"{self.base_url}/chat/completions",
                data=json.dumps(data).encode('utf-8'),
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode())
            
            # 응답 파싱
            content = result['choices'][0]['message']['content']
            
            # 요약과 분석 분리
            parts = content.split('[140자 요약]')
            if len(parts) > 1:
                summary_part = parts[1].split('[상세 분석]')[0].strip()
                news_item.summary = summary_part[:140]
            
            if '[상세 분석]' in content:
                analysis_part = content.split('[상세 분석]')[1].split('[태그]')[0].strip()
                news_item.detailed_analysis = analysis_part
            
            if '[태그]' in content:
                tags_part = content.split('[태그]')[1].strip()
                news_item.tags = [tag.strip('# ') for tag in tags_part.split() if tag.startswith('#')]
            
            logger.info(f"Summarized: {news_item.title[:50]}")
            return True
            
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            # 실패 시 기본 요약
            news_item.summary = news_item.content[:140] + "..."
            news_item.detailed_analysis = f"**배경**: {news_item.title}\n\n**주요 내용**: {news_item.content[:500]}"
            news_item.tags = self._extract_keywords(news_item.content)
            return False
    
    def _extract_keywords(self, text: str) -> List[str]:
        """키워드 추출"""
        found_keywords = []
        text_lower = text.lower()
        
        for keyword in self.config.KEYWORDS:
            if keyword.lower() in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords[:5]


class NotionPublisher:
    """Notion 발행"""
    
    def __init__(self, config: Config):
        self.config = config
        self.api_key = config.NOTION_API_KEY
        self.database_id = config.NOTION_DATABASE_ID
        self.api_base = "https://api.notion.com/v1"
        
        if not self.api_key or not self.database_id:
            logger.warning("Notion not configured")
    
    def publish(self, news_item: NewsItem) -> bool:
        """Notion에 뉴스 발행"""
        
        if not self.api_key or not self.database_id:
            logger.warning("Notion publishing skipped (not configured)")
            return False
        
        try:
            # 페이지 데이터 생성
            page_data = {
                "parent": {"database_id": self.database_id},
                "properties": {
                    "title": {
                        "title": [{"text": {"content": news_item.title[:100]}}]
                    },
                    "category": {"select": {"name": "보안"}},
                }
            }
            
            # URL 추가
            if news_item.url:
                page_data["properties"]["url"] = {"url": news_item.url}
            
            # 요약과 분석을 content에 추가
            if news_item.summary or news_item.detailed_analysis:
                content = ""
                if news_item.summary:
                    content += f"**요약**:\n{news_item.summary}\n\n"
                if news_item.detailed_analysis:
                    content += f"**상세 분석**:\n{news_item.detailed_analysis}\n\n"
                content += f"**출처**: {news_item.source}"
                
                page_data["properties"]["content"] = {
                    "rich_text": [{"text": {"content": content[:2000]}}]
                }
            
            # API 호출
            req = urllib.request.Request(
                f"{self.api_base}/pages",
                data=json.dumps(page_data).encode('utf-8'),
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json',
                    'Notion-Version': '2022-06-28'
                }
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.status == 200:
                    logger.info(f"Published to Notion: {news_item.title[:50]}")
                    return True
                else:
                    logger.error(f"Notion publishing failed: {response.status}")
                    return False
        
        except Exception as e:
            logger.error(f"Notion publishing error: {e}")
            return False


class SecurityNewsAggregator:
    """보안 뉴스 수집기 메인 클래스"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.summarizer = GLMSummarizer(self.config)
        self.publisher = NotionPublisher(self.config)
        
        # 캐시 디렉토리 생성
        self.config.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    def collect_news(self, sources: List[str] = None) -> List[NewsItem]:
        """뉴스 수집"""
        
        all_news = []
        
        # 수집할 소스 선택
        sources_to_collect = sources or list(self.config.NEWS_SOURCES.keys())
        
        for source_key in sources_to_collect:
            if source_key not in self.config.NEWS_SOURCES:
                logger.warning(f"Unknown source: {source_key}")
                continue
            
            source_config = self.config.NEWS_SOURCES[source_key]
            
            if not source_config.get('enabled', True):
                continue
            
            try:
                logger.info(f"Collecting from {source_config['name']}...")
                
                # 실제 크롤링은 간단한 버전으로 구현
                # 실제로는 BeautifulSoup이나 Selenium 사용 필요
                news_items = self._collect_from_source(source_key, source_config)
                
                all_news.extend(news_items)
                logger.info(f"Collected {len(news_items)} items from {source_config['name']}")
                
                # Rate limit 준수
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Failed to collect from {source_config['name']}: {e}")
        
        return all_news
    
    def _collect_from_source(self, source_key: str, source_config: Dict) -> List[NewsItem]:
        """소스에서 뉴스 수집 (간단 버전)"""
        
        # 실제 구현 시:
        # - RSS 파싱
        # - 웹 스크래핑 (BeautifulSoup)
        # - API 호출
        
        # 현재는 샘플 데이터 반환
        news_items = []
        
        # 샘플 뉴스 (실제로는 크롤링)
        sample_news = NewsItem(
            title=f"[{source_config['name']}] 새로운 보안 취약점 발견",
            content=f"{source_config['name']}에서 새로운 보안 취약점이 보고되었습니다. "
                   f"이 취약점은 시스템에 치명적인 영향을 줄 수 있으며, 즉각적인 패치가 권장됩니다.",
            url=source_config['url'],
            source=source_config['name']
        )
        
        news_items.append(sample_news)
        
        return news_items
    
    def filter_by_keywords(self, news_items: List[NewsItem]) -> List[NewsItem]:
        """키워드 기반 필터링"""
        
        filtered = []
        
        for item in news_items:
            # 제목이나 내용에 키워드가 있는지 확인
            text = f"{item.title} {item.content}".lower()
            
            if any(keyword.lower() in text for keyword in self.config.KEYWORDS):
                filtered.append(item)
        
        logger.info(f"Filtered {len(news_items)} → {len(filtered)} items by keywords")
        return filtered
    
    def process_news(self, news_items: List[NewsItem]) -> List[NewsItem]:
        """뉴스 처리 (요약 + 발행)"""
        
        processed = []
        
        for item in news_items:
            try:
                # 요약
                self.summarizer.summarize(item)
                
                # Notion 발행
                self.publisher.publish(item)
                
                processed.append(item)
                
                # Rate limit
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Failed to process {item.title[:30]}: {e}")
        
        return processed
    
    def run_once(self, sources: List[str] = None) -> Dict:
        """1회 실행"""
        
        logger.info("=" * 70)
        logger.info("SECURITY NEWS AGGREGATOR")
        logger.info("=" * 70)
        
        start_time = time.time()
        
        # 1. 수집
        logger.info("Step 1: Collecting news...")
        all_news = self.collect_news(sources)
        
        # 2. 필터링
        logger.info("Step 2: Filtering by keywords...")
        filtered_news = self.filter_by_keywords(all_news)
        
        # 3. 처리
        logger.info("Step 3: Processing news...")
        processed_news = self.process_news(filtered_news)
        
        elapsed = time.time() - start_time
        
        # 결과
        result = {
            'timestamp': datetime.now().isoformat(),
            'total_collected': len(all_news),
            'filtered': len(filtered_news),
            'processed': len(processed_news),
            'elapsed_seconds': round(elapsed, 2),
            'news': [item.to_dict() for item in processed_news[:10]]  # 상위 10개만
        }
        
        logger.info("=" * 70)
        logger.info(f"Completed: {len(processed_news)} news items processed")
        logger.info(f"Elapsed: {elapsed:.2f}s")
        logger.info("=" * 70)
        
        return result
    
    def save_result(self, result: Dict):
        """결과 저장"""
        
        result_file = self.config.CACHE_DIR / 'latest_result.json'
        
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Result saved to {result_file}")


def main():
    """메인 실행"""
    
    parser = argparse.ArgumentParser(description='Security News Aggregator')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--sources', type=str, help='Comma-separated list of sources')
    parser.add_argument('--test', type=str, help='Test specific source')
    
    args = parser.parse_args()
    
    # 소스 리스트
    sources = args.sources.split(',') if args.sources else None
    
    # 테스트 모드
    if args.test:
        sources = [args.test]
    
    # aggregator 생성
    aggregator = SecurityNewsAggregator()
    
    # 1회 실행
    if args.once or args.test:
        result = aggregator.run_once(sources)
        aggregator.save_result(result)
        return 0
    
    # 데몬 모드 (매시간)
    logger.info("Starting daemon mode (hourly)")
    
    while True:
        try:
            result = aggregator.run_once(sources)
            aggregator.save_result(result)
            
            # 1시간 대기
            logger.info("Waiting 1 hour until next run...")
            time.sleep(3600)
            
        except KeyboardInterrupt:
            logger.info("Daemon stopped by user")
            break
        except Exception as e:
            logger.error(f"Daemon error: {e}")
            time.sleep(60)  # 에러 시 1분 대기
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
