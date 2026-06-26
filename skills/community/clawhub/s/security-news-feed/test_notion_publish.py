#!/usr/bin/env python3
"""
Notion 발행 테스트 - KRCERT 기사
"""

import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 환경 변수 로드
from dotenv import load_dotenv
env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
load_dotenv(env_file)

from modules.crawlers.krcert import KRCERTCrawler
from modules.publisher_service import PublisherService
from modules.llm_handler import summarize_text, details_text
from config import BOANISSUE_DATABASE_ID

print("="*70)
print("NOTION PUBLISHING TEST - KRCERT")
print("="*70)

# 1. 크롤러로 기사 수집
print("\n🔄 Step 1: 기사 수집 중...")
crawler = KRCERTCrawler()
result = crawler.run(publisher_service=None)

if not result.get('queue'):
    print("❌ 수집된 기사가 없습니다.")
    sys.exit(0)

print(f"✅ {len(result['queue'])}개 기사 수집 완료")

# 2. Publisher Service 초기화
print("\n🔄 Step 2: Publisher Service 초기화...")
publisher = PublisherService(
    enable_notion=True,
    enable_tistory=False,
    notion_database_id=BOANISSUE_DATABASE_ID
)

# 3. 첫 번째 기사만 발행 테스트
test_article = result['queue'][0]

print(f"\n🔄 Step 3: 기사 발행 테스트")
print(f"제목: {test_article['title']}")
print(f"URL: {test_article['url']}")

# GLM-5로 요약 생성
print("\n🔄 Step 4: GLM-5 요약 생성 중...")
try:
    summary = summarize_text(test_article['content'], test_article['title'])
    print(f"✅ 요약 완료 ({len(summary)}자)")
except Exception as e:
    print(f"⚠️ 요약 실패: {e}")
    summary = test_article['content'][:300]

# GLM-5로 상세 분석 생성
print("\n🔄 Step 5: GLM-5 상세 분석 생성 중...")
try:
    details = details_text(test_article['content'], test_article['title'])
    print(f"✅ 상세 분석 완료 ({len(details)}자)")
except Exception as e:
    print(f"⚠️ 상세 분석 실패: {e}")
    details = ""

# Notion 발행
print("\n🔄 Step 6: Notion 발행 중...")
try:
    pub_result = publisher.publish_article(
        title=test_article['title'],
        content=summary,
        url=test_article['url'],
        date=test_article['posting_date'].strftime('%Y-%m-%d'),
        category=test_article['category'],
        details=details,
        database_id=BOANISSUE_DATABASE_ID
    )
    
    if pub_result.get('notion'):
        print("\n✅ Notion 발행 성공!")
    else:
        print("\n❌ Notion 발행 실패")
        
except Exception as e:
    print(f"\n❌ 발행 중 오류: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("TEST COMPLETED")
print("="*70)
