#!/usr/bin/env python3
"""
Selenium 크롤러 테스트 (KISA, NCSC)
"""

import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 환경 변수 로드
from dotenv import load_dotenv
env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
load_dotenv(env_file)

# Selenium 크롤러만 임포트
from modules.crawlers.kisa import KISACrawler
from modules.crawlers.ncsc import NCSCCrawler

print("="*70)
print("SELENIUM CRAWLERS TEST")
print("="*70)

crawlers = [
    ("KISA", KISACrawler),
    ("NCSC", NCSCCrawler),
]

results = []

for name, crawler_class in crawlers:
    print(f"\n🔄 {name}...")
    
    try:
        crawler = crawler_class()
        result = crawler.run(publisher_service=None)
        
        print(f"   ✅ Total: {result.get('total', 0)}")
        print(f"   ✅ Success: {result.get('success', 0)}")
        print(f"   ⚠️  Duplicates: {result.get('duplicate', 0)}")
        print(f"   ❌ Errors: {result.get('error', 0)}")
        
        results.append({
            'name': name,
            'status': '✅',
            'total': result.get('total', 0),
            'success': result.get('success', 0)
        })
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        results.append({
            'name': name,
            'status': '❌',
            'error': str(e)[:80]
        })

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

for result in results:
    if result['status'] == '✅':
        print(f"{result['status']} {result['name']}: {result['success']}/{result['total']} articles")
    else:
        print(f"{result['status']} {result['name']}: {result.get('error', 'Unknown')}")

print("="*70)
