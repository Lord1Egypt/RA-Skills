#!/usr/bin/env python3
"""
RSS 크롤러만 빠르게 테스트
"""

import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 환경 변수 로드
from dotenv import load_dotenv
env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
load_dotenv(env_file)

# RSS 크롤러만 임포트
from modules.crawlers.krcert import KRCERTCrawler
from modules.crawlers.dailysecu import DailySecuCrawler
from modules.crawlers.boannews import BoanNewsCrawler

print("="*70)
print("RSS CRAWLERS - QUICK TEST")
print("="*70)

# RSS 크롤러만
crawlers = [
    ("KRCERT", KRCERTCrawler),
    ("데일리시큐", DailySecuCrawler),
    ("보안뉴스", BoanNewsCrawler),
]

total_articles = 0
total_new = 0

for name, crawler_class in crawlers:
    print(f"\n🔄 {name}...")
    
    try:
        crawler = crawler_class()
        result = crawler.run(publisher_service=None)
        
        print(f"   스캔: {result.get('total', 0)}")
        print(f"   새 기사: {result.get('success', 0)}")
        print(f"   중복: {result.get('duplicate', 0)}")
        print(f"   에러: {result.get('error', 0)}")
        
        total_articles += result.get('total', 0)
        total_new += result.get('success', 0)
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")

print("\n" + "="*70)
print(f"📰 Total scanned: {total_articles}")
print(f"✨ Total new articles: {total_new}")
print("="*70)
