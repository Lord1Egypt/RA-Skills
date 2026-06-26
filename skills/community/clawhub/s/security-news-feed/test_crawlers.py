#!/usr/bin/env python3
"""
Security News Aggregator - Quick Test
작동하는 크롤러만 사용해서 빠르게 테스트
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

print("="*70)
print("SECURITY NEWS AGGREGATOR - QUICK TEST")
print("="*70)

# 크롤러 목록
crawlers = [
    KRCERTCrawler(),
    DailySecuCrawler(),
]

total_articles = 0
results = []

for crawler in crawlers:
    print(f"\n🔄 Running {crawler.source_name}...")
    
    try:
        result = crawler.run(publisher_service=None)
        
        print(f"   ✅ Total: {result['total']}")
        print(f"   ✅ Success: {result['success']}")
        print(f"   ⚠️  Duplicates: {result['duplicate']}")
        print(f"   ⚠️  Old: {result['old']}")
        print(f"   ❌ Errors: {result['error']}")
        
        total_articles += result['success']
        results.append({
            'source': crawler.source_name,
            'success': result['success'],
            'total': result['total']
        })
        
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results.append({
            'source': crawler.source_name,
            'success': 0,
            'total': 0,
            'error': str(e)
        })

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

for result in results:
    if 'error' in result:
        print(f"❌ {result['source']}: ERROR - {result['error'][:50]}")
    else:
        print(f"✅ {result['source']}: {result['success']}/{result['total']} articles")

print(f"\n📰 Total articles collected: {total_articles}")
print("="*70)

PYTHON_EOF
