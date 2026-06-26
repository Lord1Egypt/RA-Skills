#!/usr/bin/env python3
"""
모든 크롤러 상태 빠르게 확인
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
print("ALL CRAWLERS - QUICK STATUS CHECK")
print("="*70)

# RSS 기반 크롤러들 (빠름)
rss_crawlers = [
    ("KRCERT", KRCERTCrawler),
    ("데일리시큐", DailySecuCrawler),
    ("보안뉴스", BoanNewsCrawler),
]

results = []

for name, crawler_class in rss_crawlers:
    print(f"\n🔄 Testing {name}...")
    
    try:
        crawler = crawler_class()
        
        # URL 확인
        url = getattr(crawler, 'rss_url', getattr(crawler, 'urls', 'No URL'))
        if isinstance(url, list):
            url = url[0] if url else 'No URL'
        
        print(f"   URL: {url[:70]}")
        
        # 실행 (타임아웃 30초)
        import signal
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Timeout")
        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)
        
        result = crawler.run(publisher_service=None)
        
        signal.alarm(0)  # 타이머 취소
        
        print(f"   ✅ Total: {result['total']}")
        print(f"   ✅ Success: {result['success']}")
        print(f"   ⚠️  Duplicates: {result['duplicate']}")
        print(f"   ⚠️  Old: {result['old']}")
        print(f"   ❌ Errors: {result['error']}")
        
        results.append({
            'name': name,
            'status': '✅',
            'total': result['total'],
            'success': result['success'],
            'error': result['error']
        })
        
    except TimeoutError:
        print(f"   ❌ Timeout (30s)")
        results.append({
            'name': name,
            'status': '⏱️',
            'total': 0,
            'success': 0,
            'error': 1
        })
        
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:50]}")
        results.append({
            'name': name,
            'status': '❌',
            'total': 0,
            'success': 0,
            'error': 1,
            'error_msg': str(e)[:50]
        })

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

for result in results:
    if result['status'] == '✅':
        print(f"{result['status']} {result['name']}: {result['success']}/{result['total']} articles")
    elif result['status'] == '⏱️':
        print(f"{result['status']} {result['name']}: Timeout")
    else:
        error_msg = result.get('error_msg', 'Unknown error')
        print(f"{result['status']} {result['name']}: {error_msg}")

print("="*70)
