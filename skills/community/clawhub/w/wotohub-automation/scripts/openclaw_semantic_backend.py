#!/usr/bin/env python3
"""
OpenClaw host semantic backend skeleton.

Purpose:
- give external OpenClaw users a drop-in backend command contract
- keep stdin/stdout JSON protocol stable
- default safely to heuristic semantic output when no host-side direct model runner is available

Important:
This file does NOT assume a private OpenClaw model invocation API.
It is designed as a host-owned adapter point.
Users/operators can replace the internals with their preferred local model call.
"""

import json
import re
import sys


def heuristic_response(raw: str) -> dict:
    raw_l = raw.lower()
    product = {
        'name': None,
        'brand': None,
        'category_labels': [],
        'benefit_labels': [],
        'audience_labels': [],
        'price_tier': 'unknown',
    }
    constraints = {
        'regions': ['us'] if ('美国' in raw or 'us' in raw_l or 'united states' in raw_l) else [],
        'languages': ['en'] if ('英语' in raw or 'english' in raw_l) else [],
        'platforms': ['tiktok'] if 'tiktok' in raw_l else [],
        'min_fans': None,
        'max_fans': None,
        'has_email': True if ('有邮箱' in raw or 'email' in raw_l) else None,
    }
    m = re.search(r'(\d+)\s*万粉以上', raw)
    if m:
        constraints['min_fans'] = int(m.group(1)) * 10000

    marketing = {'goal': 'balanced', 'style_signals': [], 'creator_archetypes': []}
    keyword_clusters = {'core': [], 'benefit': [], 'scenario': [], 'creator': []}

    if '种草' in raw or '曝光' in raw:
        marketing['goal'] = 'awareness'
    if any(k in raw for k in ['转化', '出单', 'roi', '成交']):
        marketing['goal'] = 'conversion'
    if any(k in raw for k in ['真实', '不要太硬广', '朋友推荐']):
        marketing['style_signals'].append('authentic')
        keyword_clusters['creator'].extend(['authentic review', 'lifestyle creator'])

    if any(k in raw for k in ['洁面', '洗面奶']) or 'cleanser' in raw_l:
        product['category_labels'] = ['cleanser', 'skincare']
        keyword_clusters['core'] = ['cleanser', 'face wash']
        keyword_clusters['benefit'] = ['gentle cleanser']
        marketing['creator_archetypes'] = ['skincare_creator']
    elif any(k in raw for k in ['漱口水', '口腔']) or 'mouthwash' in raw_l:
        product['category_labels'] = ['oral care']
        keyword_clusters['core'] = ['mouthwash', 'oral care']
        marketing['creator_archetypes'] = ['oral_care_creator']
    elif any(k in raw for k in ['电动牙刷']) or 'electric toothbrush' in raw_l:
        product['category_labels'] = ['electric toothbrush', 'oral care']
        keyword_clusters['core'] = ['electric toothbrush', 'oral care']
        marketing['creator_archetypes'] = ['oral_care_creator']
    elif any(k in raw for k in ['精华']) or 'serum' in raw_l:
        product['category_labels'] = ['serum', 'skincare']
        keyword_clusters['core'] = ['serum', 'skincare serum']
        marketing['creator_archetypes'] = ['skincare_creator']
    elif any(k in raw for k in ['防晒']) or 'sunscreen' in raw_l:
        product['category_labels'] = ['sunscreen', 'skincare']
        keyword_clusters['core'] = ['sunscreen', 'spf skincare']
        marketing['creator_archetypes'] = ['skincare_creator']

    return {
        'product': product,
        'constraints': constraints,
        'marketing': marketing,
        'keyword_clusters': keyword_clusters,
        'uncertainties': [],
    }


def main():
    req = json.loads(sys.stdin.read() or '{}')
    raw = (((req.get('input') or {}).get('rawText')) or '')
    print(json.dumps(heuristic_response(raw), ensure_ascii=False))


if __name__ == '__main__':
    main()
