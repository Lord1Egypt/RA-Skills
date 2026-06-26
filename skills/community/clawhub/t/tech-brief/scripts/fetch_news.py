#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻采集脚本
从 RSS 源和科技媒体获取内存、AI、算力相关资讯
"""

import json
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
KEYWORDS = {
    'memory': ['内存', 'RAM', 'DDR5', 'DDR4', '颗粒', '时序', '容量', '海力士', '三星', '美光'],
    'ai': ['AI', '人工智能', '大模型', '机器学习', '深度学习', 'GPT', 'OpenAI', 'ChatGPT'],
    'compute': ['算力', 'GPU', 'CPU', 'H100', 'A100', 'RTX', '芯片', 'NVIDIA', 'AMD', 'Intel']
}

# 数据源配置
RSS_SOURCES = [
    {
        'name': 'TechPowerUp',
        'url': 'https://www.techpowerup.com/rss/',
        'category': 'compute'
    },
    {
        'name': 'Tom\'s Hardware',
        'url': 'https://www.tomshardware.com/feeds/all',
        'category': 'general'
    },
    {
        'name': 'AnandTech',
        'url': 'https://www.anandtech.com/rss/',
        'category': 'general'
    }
]

HTML_SOURCES = [
    {
        'name': '超能网',
        'url': 'https://www.expreview.com/',
        'category': 'memory',
        'selectors': {
            'articles': '.news-list .item, .article-item',
            'title': 'h2 a, h3 a, .title a',
            'link': 'h2 a, h3 a, .title a',
            'date': '.date, .time'
        }
    },
    {
        'name': '快科技',
        'url': 'https://www.mydrivers.com/',
        'category': 'general',
        'selectors': {
            'articles': '.news_list li, .item',
            'title': 'a',
            'link': 'a'
        }
    }
]

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)


def parse_rss_source(source, days=7):
    """解析 RSS 源"""
    results = []
    try:
        resp = SESSION.get(source['url'], timeout=10)
        resp.encoding = 'utf-8'
        
        # 简单 RSS 解析
        import re
        items = re.findall(r'<item>(.*?)</item>', resp.text, re.DOTALL)
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for item in items[:20]:  # 取前20条
            title_match = re.search(r'<title><!\[CDATA\[(.*?)\]\]></title>', item)
            if not title_match:
                title_match = re.search(r'<title>(.*?)</title>', item)
            
            link_match = re.search(r'<link>(.*?)</link>', item)
            pubdate_match = re.search(r'<pubDate>(.*?)</pubDate>', item)
            
            if title_match:
                title = title_match.group(1).strip()
                
                # 关键词过滤
                if not is_relevant(title):
                    continue
                
                # 日期过滤
                pub_date = None
                if pubdate_match:
                    try:
                        from email.utils import parsedate_to_datetime
                        pub_date = parsedate_to_datetime(pubdate_match.group(1)).strftime('%Y-%m-%d')
                        pub_dt = datetime.strptime(pub_date, '%Y-%m-%d')
                        if pub_dt < cutoff_date:
                            continue
                    except:
                        pass
                
                results.append({
                    'title': title,
                    'url': link_match.group(1) if link_match else '',
                    'source': source['name'],
                    'source_type': 'rss',
                    'category': source['category'],
                    'date': pub_date or '',
                    'content_snippet': title[:100]
                })
                
    except Exception as e:
        print(f"  ⚠️ {source['name']} 获取失败: {e}", file=sys.stderr)
    
    return results


def parse_html_source(source, days=7):
    """解析 HTML 页面"""
    results = []
    try:
        resp = SESSION.get(source['url'], timeout=10)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'lxml')
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        selectors = source.get('selectors', {})
        articles = soup.select(selectors.get('articles', 'article'))
        
        for article in articles[:15]:
            title_elem = article.select_one(selectors.get('title', 'h2'))
            link_elem = article.select_one(selectors.get('link', 'a'))
            
            if not title_elem or not link_elem:
                continue
            
            title = title_elem.get_text(strip=True)
            link = link_elem.get('href', '')
            
            if not title or not is_relevant(title):
                continue
            
            # 处理相对链接
            if link and not link.startswith('http'):
                from urllib.parse import urljoin
                link = urljoin(source['url'], link)
            
            results.append({
                'title': title,
                'url': link,
                'source': source['name'],
                'source_type': 'html',
                'category': source['category'],
                'date': '',
                'content_snippet': title[:100]
            })
            
    except Exception as e:
        print(f"  ⚠️ {source['name']} 获取失败: {e}", file=sys.stderr)
    
    return results


def is_relevant(title):
    """检查标题是否包含相关关键词"""
    title_lower = title.lower()
    all_keywords = []
    for kw_list in KEYWORDS.values():
        all_keywords.extend(kw_list)
    
    for kw in all_keywords:
        if kw.lower() in title_lower:
            return True
    return False


def deduplicate(results):
    """去重"""
    seen = set()
    unique = []
    
    for item in results:
        # 用标题+来源作为唯一标识
        key = (item['title'], item['source'])
        if key not in seen:
            seen.add(key)
            unique.append(item)
    
    return unique


def fetch_all_news(days=7):
    """获取所有新闻"""
    all_results = []
    
    print("  📰 正在采集 RSS 源...")
    for source in RSS_SOURCES:
        results = parse_rss_source(source, days)
        all_results.extend(results)
        if results:
            print(f"     ✓ {source['name']}: {len(results)} 条")
    
    print("  📰 正在采集 HTML 源...")
    for source in HTML_SOURCES:
        results = parse_html_source(source, days)
        all_results.extend(results)
        if results:
            print(f"     ✓ {source['name']}: {len(results)} 条")
    
    # 去重
    all_results = deduplicate(all_results)
    
    return {
        "query_date": datetime.now().strftime('%Y-%m-%d'),
        "date_range": {"days": days},
        "keywords": [k for kw in KEYWORDS.values() for k in kw],
        "total": len(all_results),
        "results": all_results
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description='新闻采集脚本')
    parser.add_argument('--days', type=int, default=7, help='时间范围（天）')
    args = parser.parse_args()
    
    result = fetch_all_news(args.days)
    
    # 输出 JSON
    print("\n=== JSON_OUTPUT_START ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("=== JSON_OUTPUT_END ===")
    
    return result


if __name__ == '__main__':
    main()