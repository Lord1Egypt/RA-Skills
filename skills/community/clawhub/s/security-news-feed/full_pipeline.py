#!/usr/bin/env python3
"""
Security News 전체 파이프라인
1. 9개 크롤러로 기사 수집
2. GLM-5로 요약/분석
3. Notion에 자동 발행
"""

import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')
import time

# 환경 변수 로드
from dotenv import load_dotenv
env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
load_dotenv(env_file)

# 크롤러 임포트
from modules.crawlers.krcert import KRCERTCrawler
from modules.crawlers.dailysecu import DailySecuCrawler
from modules.crawlers.boannews import BoanNewsCrawler
from modules.crawlers.ahnlab import AhnLabCrawler
from modules.crawlers.boho import BohoCrawler
from modules.crawlers.igloo import IglooCrawler
from modules.crawlers.kisa import KISACrawler
from modules.crawlers.ncsc import NCSCCrawler
from modules.crawlers.skshieldus import SKShieldusCrawler

# 발행 및 LLM
from modules.publisher_service import PublisherService
from modules.llm_handler import summarize_text, details_text
from config import BOANISSUE_DATABASE_ID

print("="*70)
print("SECURITY NEWS - FULL PIPELINE")
print("="*70)

# 크롤러 리스트
crawlers = [
    ("KRCERT", KRCERTCrawler),
    ("데일리시큐", DailySecuCrawler),
    ("보안뉴스", BoanNewsCrawler),
    ("AhnLab", AhnLabCrawler),
    ("Boho", BohoCrawler),
    ("Igloo", IglooCrawler),
    ("KISA", KISACrawler),
    ("NCSC", NCSCCrawler),
    ("SKShieldus", SKShieldusCrawler),
]

# Publisher Service 초기화
publisher = PublisherService(
    enable_notion=True,
    enable_tistory=False,
    notion_database_id=BOANISSUE_DATABASE_ID
)

total_collected = 0
total_published = 0
total_failed = 0

# 1. 기사 수집
print("\n" + "="*70)
print("STEP 1: 기사 수집")
print("="*70)

all_articles = []

for name, crawler_class in crawlers:
    print(f"\n🔄 {name}...")
    
    try:
        crawler = crawler_class()
        result = crawler.run(publisher_service=None)
        
        collected = len(result.get('queue', []))
        total_collected += collected
        
        print(f"   ✅ 수집: {collected}개")
        
        if collected > 0:
            all_articles.extend(result['queue'])
        
        # Rate limit 방지를 위한 대기
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")

print(f"\n📊 총 수집: {total_collected}개 기사")

# 2. GLM-5 요약/분석 + Notion 발행
if total_collected > 0:
    print("\n" + "="*70)
    print("STEP 2: GLM-5 요약/분석 + Notion 발행")
    print("="*70)
    
    for i, article in enumerate(all_articles, 1):
        print(f"\n[{i}/{total_collected}] {article['title'][:50]}...")
        
        try:
            # GLM-5 요약
            print("   🔄 요약 생성 중...")
            summary = summarize_text(article['content'], article['title'])
            print(f"   ✅ 요약: {len(summary)}자")
            
            # Rate limit 방지
            time.sleep(1)
            
            # GLM-5 상세 분석
            print("   🔄 상세 분석 생성 중...")
            details = details_text(article['content'], article['title'])
            print(f"   ✅ 분석: {len(details)}자")
            
            # Rate limit 방지
            time.sleep(1)
            
            # Notion 발행
            print("   🔄 Notion 발행 중...")
            pub_result = publisher.publish_article(
                title=article['title'],
                content=summary,
                url=article['url'],
                date=article['posting_date'].strftime('%Y-%m-%d'),
                category=article['category'],
                details=details,
                database_id=BOANISSUE_DATABASE_ID
            )
            
            if pub_result.get('notion'):
                total_published += 1
                print(f"   ✅ 발행 성공!")
            else:
                total_failed += 1
                print(f"   ❌ 발행 실패")
            
            # Rate limit 방지
            time.sleep(2)
            
        except Exception as e:
            total_failed += 1
            print(f"   ❌ Error: {str(e)[:50]}")
            # 실패해도 다음 기사 계속 진행
            continue

# 3. 결과 요약
print("\n" + "="*70)
print("PIPELINE SUMMARY")
print("="*70)
print(f"📰 수집된 기사: {total_collected}개")
print(f"✅ Notion 발행 성공: {total_published}개")
print(f"❌ 발행 실패: {total_failed}개")
print(f"📊 성공률: {total_published/total_collected*100:.1f}%" if total_collected > 0 else "N/A")
print("="*70)
