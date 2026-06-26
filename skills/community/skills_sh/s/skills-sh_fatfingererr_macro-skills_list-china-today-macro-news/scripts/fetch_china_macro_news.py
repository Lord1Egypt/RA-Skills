#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
列出今日中國宏觀新聞消息抓取腳本

基於 news-aggregator-skill 模式，專注於中國宏觀經濟新聞。

用法:
    python fetch_china_macro_news.py --source wallstreetcn --limit 15
    python fetch_china_macro_news.py --source all --limit 10 --deep
    python fetch_china_macro_news.py --keyword "央行,利率,LPR"
"""

import argparse
import json
import re
import sys
import time
import concurrent.futures
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# =============================================================================
# Configuration
# =============================================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 預設宏觀關鍵字
DEFAULT_MACRO_KEYWORDS = [
    # 央行與貨幣政策
    "央行", "PBOC", "利率", "LPR", "MLF", "降息", "降準", "逆回購",
    # 經濟數據
    "GDP", "PMI", "CPI", "PPI", "通膨", "通縮", "工業增加值", "零售",
    # 財政與政策
    "經濟", "宏觀", "財政", "貨幣政策", "穩增長",
    # 貿易
    "貿易", "進出口", "順差", "逆差", "關稅",
    # 就業與消費
    "就業", "失業", "消費",
    # 房地產與投資
    "房地產", "樓市", "投資", "基建", "房價",
    # 外匯
    "人民幣", "匯率", "外匯", "美元",
    # 債券與信貸
    "債券", "國債", "信貸", "社融", "M2", "貸款",
    # 其他重要
    "統計局", "發改委", "國務院"
]


# =============================================================================
# Utility Functions
# =============================================================================

def filter_items(items, keyword=None):
    """根據關鍵字篩選新聞"""
    if not keyword:
        # 使用預設宏觀關鍵字
        keyword = ",".join(DEFAULT_MACRO_KEYWORDS)

    keywords = [k.strip() for k in keyword.split(',') if k.strip()]
    if not keywords:
        return items

    # 建立正則表達式匹配
    pattern = '|'.join([re.escape(k) for k in keywords])
    regex = re.compile(pattern, re.IGNORECASE)

    return [item for item in items if regex.search(item.get('title', ''))]


def fetch_url_content(url):
    """
    深度抓取：下載文章內容並提取正文
    截取前 3000 字元
    """
    if not url or not url.startswith('http'):
        return ""
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # 移除不需要的元素
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.extract()

        # 提取文字
        text = soup.get_text(separator=' ', strip=True)

        # 清理多餘空白
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return text[:3000]
    except Exception:
        return ""


def enrich_items_with_content(items, max_workers=10):
    """並行抓取文章內容"""
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {executor.submit(fetch_url_content, item['url']): item for item in items}
        for future in concurrent.futures.as_completed(future_to_item):
            item = future_to_item[future]
            try:
                content = future.result()
                if content:
                    item['content'] = content
            except Exception:
                item['content'] = ""
    return items


# =============================================================================
# Source Fetchers
# =============================================================================

def fetch_wallstreetcn(limit=15, keyword=None):
    """
    抓取華爾街日報新聞
    主要來源：宏觀/市場新聞即時性強
    """
    try:
        url = "https://api-one.wallstcn.com/apiv1/content/information-flow?channel=global-channel&accept=article&limit=50"
        response = requests.get(url, timeout=10)
        data = response.json()

        items = []
        for item in data.get('data', {}).get('items', []):
            res = item.get('resource')
            if not res:
                continue

            title = res.get('title') or res.get('content_short')
            if not title:
                continue

            # 時間處理
            ts = res.get('display_time', 0)
            time_str = datetime.fromtimestamp(ts).strftime('%H:%M') if ts else ""

            items.append({
                "source": "華爾街日報",
                "title": title,
                "url": res.get('uri', ''),
                "time": time_str
            })

        # 篩選並限制數量
        filtered = filter_items(items, keyword)
        return filtered[:limit]

    except Exception as e:
        sys.stderr.write(f"華爾街日報抓取失敗: {e}\n")
        return []


def fetch_36kr(limit=15, keyword=None):
    """
    抓取 36氪 快訊
    輔助來源：科技財經，涵蓋經濟政策
    """
    try:
        response = requests.get("https://36kr.com/newsflashes", headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        items = []
        for item in soup.select('.newsflash-item'):
            title_elem = item.select_one('.item-title')
            if not title_elem:
                continue

            title = title_elem.get_text(strip=True)
            href = title_elem.get('href', '')

            time_elem = item.select_one('.time')
            time_str = time_elem.get_text(strip=True) if time_elem else ""

            # 處理相對 URL
            if href and not href.startswith('http'):
                href = f"https://36kr.com{href}"

            items.append({
                "source": "36氪",
                "title": title,
                "url": href,
                "time": time_str
            })

        # 篩選並限制數量
        filtered = filter_items(items, keyword)
        return filtered[:limit]

    except Exception as e:
        sys.stderr.write(f"36氪抓取失敗: {e}\n")
        return []


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="列出今日中國宏觀新聞消息抓取")

    parser.add_argument(
        '--source', '-s',
        default='wallstreetcn',
        help='數據源: wallstreetcn, 36kr, all (預設 wallstreetcn)'
    )
    parser.add_argument(
        '--limit', '-l',
        type=int,
        default=15,
        help='每個來源的最大條目數 (預設 15)'
    )
    parser.add_argument(
        '--keyword', '-k',
        help='逗號分隔的關鍵字篩選 (預設使用宏觀關鍵字)'
    )
    parser.add_argument(
        '--deep',
        action='store_true',
        help='深度抓取：下載文章正文內容'
    )
    parser.add_argument(
        '--no-filter',
        action='store_true',
        help='不使用關鍵字篩選，返回所有新聞'
    )

    args = parser.parse_args()

    # 來源映射
    sources_map = {
        'wallstreetcn': fetch_wallstreetcn,
        '36kr': fetch_36kr,
    }

    # 決定要執行哪些來源
    to_run = []
    if args.source == 'all':
        to_run = list(sources_map.values())
    else:
        requested = [s.strip() for s in args.source.split(',')]
        for s in requested:
            if s in sources_map:
                to_run.append(sources_map[s])

    if not to_run:
        sys.stderr.write(f"未知來源: {args.source}\n")
        sys.stderr.write(f"可用來源: {', '.join(sources_map.keys())}\n")
        sys.exit(1)

    # 決定關鍵字
    keyword = None if args.no_filter else args.keyword

    # 執行抓取
    results = []
    for fetch_func in to_run:
        try:
            items = fetch_func(args.limit, keyword)
            results.extend(items)
            sys.stderr.write(f"從 {fetch_func.__name__} 抓取 {len(items)} 條新聞\n")
        except Exception as e:
            sys.stderr.write(f"抓取失敗: {e}\n")

    # 深度抓取
    if args.deep and results:
        sys.stderr.write(f"深度抓取 {len(results)} 條新聞的內容...\n")
        results = enrich_items_with_content(results)

    # 輸出 JSON
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
