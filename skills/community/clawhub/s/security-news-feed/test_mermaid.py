#!/usr/bin/env python3
"""
Mermaid 다이어그램 포함 테스트
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
print("MERMAID DIAGRAM TEST")
print("="*70)

# 1. 기사 수집
print("\n🔄 Step 1: 기사 수집 중...")
crawler = KRCERTCrawler()
result = crawler.run(publisher_service=None)

if not result.get('queue'):
    print("❌ 수집된 기사가 없습니다.")
    sys.exit(0)

test_article = result['queue'][0]
print(f"✅ {test_article['title']}")

# 2. GLM-5 상세 분석 (다이어그램 포함)
print("\n🔄 Step 2: GLM-5 상세 분석 (다이어그램 포함)...")
try:
    details = details_text(test_article['content'], test_article['title'])
    print(f"✅ 상세 분석 완료 ({len(details)}자)")
    
    # Mermaid 다이어그램 확인
    if '```mermaid' in details:
        print("\n✅ Mermaid 다이어그램 포함됨!")
        # 다이어그램 부분만 추출
        start = details.find('```mermaid')
        end = details.find('```', start + 10)
        if start != -1 and end != -1:
            diagram = details[start:end+3]
            print("\n📊 다이어그램 미리보기:")
            print(diagram[:300] + "..." if len(diagram) > 300 else diagram)
    else:
        print("\n⚠️ Mermaid 다이어그램 없음")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("TEST COMPLETED")
print("="*70)
