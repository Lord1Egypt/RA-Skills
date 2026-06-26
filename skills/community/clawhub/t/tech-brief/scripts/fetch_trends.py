#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点话题采集脚本
从微博、知乎、B站获取科技热点话题
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("请先安装依赖：pip install requests beautifulsoup4 lxml")
    sys.exit(1)

# 关键词配置
KEYWORDS = ['内存', 'RAM', 'DDR5', 'AI', '大模型', 'GPU', '算力', 'H100', 'NVIDIA', 'AMD', 'Intel', '芯片', 'CPU']

# 数据源
TREND_SOURCES = [
    {
        'name': '微博科技热搜',
        'url': 'https://weibo.com/ajax/side/hotSearch',
        'type': 'api',
        'category': 'weibo'
    },
    {
        'name': '知乎热榜',
        'url': 'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10',
        'type': 'api',
        'category': 'zhihu'
    }
]

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def fetch_weibo_trends():
    """获取微博热搜"""
    results = []
    try:
        resp = SESSION.get(
            'https://weibo.com/ajax/side/hotSearch',
            timeout=10,
            headers={
                'Referer': 'https://weibo.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        data = resp.json()
        
        if data.get('ok') == 1:
            realtime = data.get('data', {}).get('realtime', [])
            for item in realtime[:15]:
                word = item.get('word', '')
                raw_word = item.get('raw_word', word)
                
                # 关键词过滤
                if not is_relevant(raw_word):
                    continue
                
                # 热度指标
                num = item.get('num', 0)
                label = item.get('label', '热搜')
                
                results.append({
                    'title': raw_word,
                    'url': f'https://s.weibo.com/weibo?q={raw_word}',
                    'source': '微博',
                    'source_type': 'api',
                    'category': 'trends',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'content_snippet': f'🔥 {num} | {label}',
                    'extra': {'hot': num, 'label': label}
                })
                
    except Exception as e:
        print(f"  ⚠️ 微博热搜获取失败: {e}", file=sys.stderr)
    
    return results


def fetch_zhihu_trends():
    """获取知乎热榜"""
    results = []
    try:
        resp = SESSION.get(
            'https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=10',
            timeout=10,
            headers={
                'Referer': 'https://www.zhihu.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        data = resp.json()
        
        if data.get('data'):
            for item in data['data'][:10]:
                title = item.get('target', {}).get('title', '')
                url = item.get('target', {}).get('url', '')
                excerpt = item.get('target', {}).get('excerpt', '')
                
                # 关键词过滤
                if not is_relevant(title):
                    continue
                
                # 热度指标
                detail_text = item.get('detail_text', '')
                
                # 处理 URL
                if url and '/p/' in url:
                    url = 'https://www.zhihu.com' + url
                
                results.append({
                    'title': title,
                    'url': url,
                    'source': '知乎',
                    'source_type': 'api',
                    'category': 'trends',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'content_snippet': detail_text or excerpt[:80],
                    'extra': {'detail': detail_text}
                })
                
    except Exception as e:
        print(f"  ⚠️ 知乎热榜获取失败: {e}", file=sys.stderr)
    
    return results


def fetch_bilibili_trends():
    """获取B站科技区热门"""
    results = []
    try:
        # B站热门榜
        resp = SESSION.get(
            'https://api.bilibili.com/x/web-interface/popular?ps=20&pn=1',
            timeout=10
        )
        data = resp.json()
        
        if data.get('code') == 0 and data.get('data'):
            for item in data['data'].get('list', [])[:10]:
                title = item.get('title', '')
                bvid = item.get('bvid', '')
                
                # 简单过滤：包含科技关键词或播放量高的
                if not (is_relevant(title) or item.get('play', 0) > 100000):
                    continue
                
                results.append({
                    'title': title,
                    'url': f'https://www.bilibili.com/video/{bvid}',
                    'source': 'B站',
                    'source_type': 'api',
                    'category': 'trends',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'content_snippet': f"播放: {item.get('play', 0)} | 弹幕: {item.get('video_review', 0)}",
                    'extra': {
                        'play': item.get('play', 0),
                        'like': item.get('like', 0)
                    }
                })
                
    except Exception as e:
        print(f"  ⚠️ B站热门获取失败: {e}", file=sys.stderr)
    
    return results


def is_relevant(title):
    """检查标题是否包含相关关键词"""
    if not title:
        return False
    title_lower = title.lower()
    for kw in KEYWORDS:
        if kw.lower() in title_lower:
            return True
    return False


def deduplicate(results):
    """去重"""
    seen = set()
    unique = []
    
    for item in results:
        key = (item['title'], item['source'])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    
    return unique


def fetch_trends(days=7):
    """获取所有热点话题"""
    all_results = []
    
    print("  🔥 正在采集微博热搜...")
    weibo_results = fetch_weibo_trends()
    all_results.extend(weibo_results)
    if weibo_results:
        print(f"     ✓ 微博: {len(weibo_results)} 条")
    
    print("  🔥 正在采集知乎热榜...")
    zhihu_results = fetch_zhihu_trends()
    all_results.extend(zhihu_results)
    if zhihu_results:
        print(f"     ✓ 知乎: {len(zhihu_results)} 条")
    
    print("  🔥 正在采集B站热门...")
    bilibili_results = fetch_bilibili_trends()
    all_results.extend(bilibili_results)
    if bilibili_results:
        print(f"     ✓ B站: {len(bilibili_results)} 条")
    
    # 去重
    all_results = deduplicate(all_results)
    
    return {
        "query_date": datetime.now().strftime('%Y-%m-%d'),
        "date_range": {"days": days},
        "keywords": KEYWORDS,
        "total": len(all_results),
        "results": all_results
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='热点话题采集脚本')
    parser.add_argument('--days', type=int, default=7, help='时间范围（天）')
    args = parser.parse_args()
    
    result = fetch_trends(args.days)
    
    # 输出 JSON
    print("\n=== JSON_OUTPUT_START ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("=== JSON_OUTPUT_END ===")
    
    return result


if __name__ == '__main__':
    main()