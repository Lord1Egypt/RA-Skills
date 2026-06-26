#!/usr/bin/env python3
"""
전체 크롤러 최종 테스트 (NCSC 포함)
"""

import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 환경 변수 로드
from dotenv import load_dotenv
env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
load_dotenv(env_file)

# 작동하는 크롤러 임포트 (NCSC 포함)
from modules.crawlers.krcert import KRCERTCrawler
from modules.crawlers.dailysecu import DailySecuCrawler
from modules.crawlers.boannews import BoanNewsCrawler
from modules.crawlers.ahnlab import AhnLabCrawler
from modules.crawlers.boho import BohoCrawler
from modules.crawlers.igloo import IglooCrawler
from modules.crawlers.kisa import KISACrawler
from modules.crawlers.ncsc import NCSCCrawler

print("="*70)
print("ALL CRAWLERS - FINAL TEST (8 CRAWLERS)")
print("="*70)

crawlers = [
    ("KRCERT", KRCERTCrawler, "RSS"),
    ("데일리시큐", DailySecuCrawler, "RSS"),
    ("보안뉴스", BoanNewsCrawler, "RSS"),
    ("AhnLab", AhnLabCrawler, "Web"),
    ("Boho", BohoCrawler, "Web"),
    ("Igloo", IglooCrawler, "Web"),
    ("KISA", KISACrawler, "Requests"),
    ("NCSC", NCSCCrawler, "Selenium"),  # 새로 추가!
]

total_articles = 0
total_new = 0
results = []

for name, crawler_class, crawler_type in crawlers:
    print(f"\n🔄 {name} ({crawler_type})...")
    
    try:
        crawler = crawler_class()
        result = crawler.run(publisher_service=None)
        
        print(f"   스캔: {result.get('total', 0)}")
        print(f"   새 기사: {result.get('success', 0)}")
        print(f"   중복: {result.get('duplicate', 0)}")
        print(f"   구 기사: {result.get('old', 0)}")
        print(f"   에러: {result.get('error', 0)}")
        
        total_articles += result.get('total', 0)
        total_new += result.get('success', 0)
        
        results.append({
            'name': name,
            'type': crawler_type,
            'total': result.get('total', 0),
            'success': result.get('success', 0),
            'old': result.get('old', 0),
            'status': '✅'
        })
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")
        results.append({
            'name': name,
            'type': crawler_type,
            'total': 0,
            'success': 0,
            'old': 0,
            'status': '❌',
            'error': str(e)[:50]
        })

print("\n" + "="*70)
print("FINAL SUMMARY")
print("="*70)

for result in results:
    if result['status'] == '✅':
        print(f"{result['status']} {result['name']:15s} ({result['type']:8s}): {result['success']:3d}/{result['total']:3d} articles (old: {result['old']})")
    else:
        print(f"{result['status']} {result['name']:15s} ({result['type']:8s}): {result.get('error', 'Unknown')}")

print("\n" + "="*70)
print(f"📰 Total scanned: {total_articles}")
print(f"✨ Total new articles: {total_new}")
print(f"🎯 Success rate: {len([r for r in results if r['status']=='✅'])}/{len(results)} crawlers ({len([r for r in results if r['status']=='✅'])/len(results)*100:.0f}%)")
print("="*70)
