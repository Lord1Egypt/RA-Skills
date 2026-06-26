#!/usr/bin/env python3
"""
전체 크롤러 통합 테스트
"""

import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 환경 변수 로드
from dotenv import load_dotenv
env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
load_dotenv(env_file)

# 크롤러 임포트
from modules.crawlers.krcert import KRCERTCrawler
from modules.crawlers.dailysecu import DailySecuCrawler
from modules.crawlers.boannews import BoanNewsCrawler

print("="*70)
print("SECURITY NEWS - FULL INTEGRATION TEST")
print("="*70)

# RSS 기반 크롤러들
crawlers = [
    KRCERTCrawler(),
    DailySecuCrawler(),
    BoanNewsCrawler(),
]

total_articles = 0
total_new = 0

for crawler in crawlers:
    print(f"\n🔄 {crawler.source_name}...")
    
    try:
        result = crawler.run(publisher_service=None)
        
        print(f"   스캔: {result['total']}")
        print(f"   새 기사: {result['success']}")
        print(f"   중복: {result['duplicate']}")
        print(f"   구 기사: {result['old']}")
        print(f"   에러: {result['error']}")
        
        total_articles += result['total']
        total_new += result['success']
        
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "="*70)
print("FINAL RESULTS")
print("="*70)
print(f"📰 총 스캔: {total_articles}개")
print(f"✨ 새 기사: {total_new}개")
print("="*70)
