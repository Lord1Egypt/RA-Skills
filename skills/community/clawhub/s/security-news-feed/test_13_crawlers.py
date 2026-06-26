#!/usr/bin/env python3
"""
13개 크롤러 전체 테스트
- 기존 9개: KRCERT, 데일리시큐, 보안뉴스, AhnLab, Boho, Igloo, KISA, NCSC, SKShieldus
- 새로 추가 4개: GoogleNews, arXiv, HackerNews, Hada.io
"""

import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# 환경 변수 로드
from dotenv import load_dotenv
env_file = Path.home() / '.openclaw' / 'workspace' / '.env'
load_dotenv(env_file)

# Security News Module 경로 추가
skill_path = Path(__file__).parent
sys.path.insert(0, str(skill_path))

print("="*70)
print("13 CRAWLERS FULL TEST")
print("="*70)

from modules.crawlers import (
    KRCERTCrawler,
    DailySecuCrawler,
    BoanNewsCrawler,
    AhnLabCrawler,
    BohoCrawler,
    IglooCrawler,
    KISACrawler,
    NCSCCrawler,
    SKShieldusCrawler,
    GoogleNewsCrawler,
    ArxivCrawler,
    HackerNewsCrawler,
    HadaioCrawler,
)

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
    ("GoogleNews", GoogleNewsCrawler),
    ("arXiv", ArxivCrawler),
    ("HackerNews", HackerNewsCrawler),
    ("Hada.io", HadaioCrawler),
]

print(f"\n✅ 총 {len(crawlers)}개 크롤러 로드 완료\n")

total_collected = 0
total_success = 0
results = []

for name, crawler_class in crawlers:
    print(f"\n{'='*70}")
    print(f"[{name}]")
    print(f"{'='*70}")

    try:
        crawler = crawler_class()
        result = crawler.run(publisher_service=None)

        collected = len(result.get('queue', []))
        success = result.get('success', 0)
        duplicate = result.get('duplicate', 0)
        error = result.get('error', 0)

        total_collected += collected
        total_success += success

        results.append({
            'name': name,
            'collected': collected,
            'success': success,
            'duplicate': duplicate,
            'error': error
        })

        print(f"  수집: {collected}개")
        print(f"  성공: {success}개")
        print(f"  중복: {duplicate}개")
        print(f"  에러: {error}개")

        if collected > 0:
            print(f"\n  📰 수집된 기사 미리보기:")
            for i, article in enumerate(result['queue'][:3], 1):
                print(f"    {i}. {article['title'][:50]}...")

    except Exception as e:
        print(f"  ❌ Error: {str(e)[:100]}")
        import traceback
        traceback.print_exc()
        results.append({
            'name': name,
            'collected': 0,
            'success': 0,
            'duplicate': 0,
            'error': 1
        })

print("\n" + "="*70)
print("SUMMARY")
print("="*70)
print(f"총 수집: {total_collected}개")
print(f"총 성공: {total_success}개")
print(f"크롤러 수: {len(crawlers)}개")
print(f"성공률: {total_success/total_collected*100:.1f}%" if total_collected > 0 else "N/A")

print("\n📊 크롤러별 현황:")
for r in results:
    print(f"  {r['name']:15s}: {r['collected']:3d}개 (성공: {r['success']:3d}, 중복: {r['duplicate']:3d}, 에러: {r['error']:1d})")

print("\n" + "="*70)
