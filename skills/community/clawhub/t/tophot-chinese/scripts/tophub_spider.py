#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
今日热榜爬虫 — 只获取热榜列表（title、description、url），不抓取正文内容。
用法: python tophub_spider.py <网站名称> [--output 保存路径] [--top 数量]
示例: python tophub_spider.py 知乎 --output ./output --top 10
"""

import json
import os
import re
import sys
import time
import argparse
import requests
from datetime import datetime
from tqdm import tqdm
from pypinyin import pinyin, Style


BASE_URL = 'https://tophub.today'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'tophub_hot.json')


def to_pinyin(text):
    """中文转拼音（全小写，空格连接）"""
    result = pinyin(text, style=Style.NORMAL)
    return '_'.join([item[0] for item in result])


def safe_filename(title):
    """将标题转为安全文件名，所有符号替换为下划线"""
    # 替换所有非字母、数字、中文的字符为下划线
    name = re.sub(r'[^\w\u4e00-\u9fff]', '_', title)
    # 合并连续下划线
    name = re.sub(r'_+', '_', name)
    # 去掉首尾下划线
    name = name.strip('_')
    # 限制长度
    if len(name) > 100:
        name = name[:100]
    return name or 'untitled'


# ========== 热榜数据获取 ==========

def create_session():
    """创建并初始化session"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': BASE_URL,
    })
    session.get(BASE_URL, timeout=15)
    time.sleep(3)
    return session


def get_hot_days(session, days=1):
    """获取热门榜单数据"""
    try:
        response = session.post(
            f"{BASE_URL}/hot/days",
            data={'days': days},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=20
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 200:
                return result.get('data', [])
    except Exception as e:
        print(f"请求失败: {e}")
    return []


def get_category_data(session, category_id):
    """通过API获取分类数据"""
    nodeid_map = {
        'tech': '36',
        'ent': '5',
        'finance': '102',
        'developer': '2399',
        'ai': '31294',
    }

    nodeid = nodeid_map.get(category_id, '')
    if not nodeid:
        return []

    try:
        response = session.post(
            f"{BASE_URL}/hot/days",
            data={'days': 1, 'nodeid': nodeid},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=20
        )
        if response.status_code == 200:
            result = response.json()
            if result.get('status') == 200:
                return result.get('data', [])
    except:
        pass
    return []


def fetch_hot_data(session):
    """获取所有热榜数据并按站点分组"""
    all_items = []

    # 综合热榜
    print("获取综合热榜...", end=" ")
    for days in [1, 7, 30]:
        data = get_hot_days(session, days)
        all_items.extend(data)
        time.sleep(1)
    print(f"{len(all_items)} 条")

    # 分类热榜
    categories = ['tech', 'ent', 'finance', 'developer', 'ai']
    print("获取分类热榜...", end=" ")
    cat_count = 0
    for cat_id in categories:
        data = get_category_data(session, cat_id)
        all_items.extend(data)
        cat_count += len(data)
        time.sleep(1)
    print(f"{cat_count} 条")

    # 按站点分组
    sites = {}
    for item in all_items:
        site = item.get('sitename', '未知')
        if site not in sites:
            sites[site] = []
        sites[site].append({
            'title': item.get('title', ''),
            'description': item.get('description', ''),
            'url': item.get('url', ''),
        })

    # 去重
    for site in sites:
        seen = set()
        unique = []
        for item in sites[site]:
            url = item.get('url', '')
            if url and url not in seen:
                seen.add(url)
                unique.append(item)
        sites[site] = unique

    return sites


def load_cached_data():
    """加载缓存的热榜数据"""
    if not os.path.exists(DATA_FILE):
        return None

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 合并 by_site 和 category_data
    sites = {}
    for site, items in data.get('hot_data', {}).get('by_site', {}).items():
        sites[site] = items
    for site, items in data.get('category_data', {}).items():
        if site in sites:
            # 去重合并
            existing_urls = {i['url'] for i in sites[site]}
            for item in items:
                if item['url'] not in existing_urls:
                    sites[site].append(item)
        else:
            sites[site] = items

    return sites


def save_hot_cache(sites):
    """保存热榜缓存"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'source': BASE_URL,
        'hot_data': {'by_site': sites},
        'category_data': {},
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


# ========== 主流程 ==========

def run(site_name, output_dir, top_n):
    """主流程：获取热榜 → 逐条保存为 JSON（只含 title/description/url，不抓正文）"""

    # 1. 获取热榜数据（优先从网络拉取，失败用缓存）
    print("初始化连接...")
    try:
        session = create_session()
        sites = fetch_hot_data(session)
        save_hot_cache(sites)
    except Exception as e:
        print(f"在线获取失败({e})，尝试使用缓存...")
        sites = load_cached_data()
        if not sites:
            print("无缓存数据，退出")
            return

    # 2. 列出可用站点（若未匹配到）
    if site_name not in sites:
        print(f"\n未找到站点 '{site_name}'")
        print("可用的站点:")
        for s in sorted(sites.keys()):
            print(f"  - {s} ({len(sites[s])} 条)")
        return

    items = sites[site_name]
    print(f"\n{site_name}: 共 {len(items)} 条")

    # 3. 截取 top_n
    if top_n and top_n < len(items):
        items = items[:top_n]
        print(f"取前 {top_n} 条")

    # 4. 创建保存目录：output_dir/站点拼音/
    site_pinyin = to_pinyin(site_name)
    save_dir = os.path.join(output_dir, site_pinyin)
    os.makedirs(save_dir, exist_ok=True)
    print(f"保存目录: {save_dir}")

    # 5. 逐条保存（只保存热榜信息，不抓取正文）
    for item in tqdm(items, desc=f"保存 {site_name}", unit="条"):
        title = item.get('title', '')

        file_data = {
            'title': title,
            'description': item.get('description', ''),
            'url': item.get('url', ''),
            'created_at': datetime.now().isoformat(),
            'content': '',
        }

        filename = safe_filename(title) + '.json'
        filepath = os.path.join(save_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(file_data, f, ensure_ascii=False, indent=2)

    print(f"\n完成! 共保存 {len(items)} 条热榜条目")
    print(f"保存目录: {save_dir}")
    print(f"\n如需抓取正文内容，请使用:")
    print(f"  python fetch_site_content.py {save_dir}/<文件名>.json")


def main():
    parser = argparse.ArgumentParser(description='今日热榜爬虫 + 内容抓取')
    parser.add_argument('site', nargs='?', help='网站名称 (如: 知乎、微信、微博)')
    parser.add_argument('--output', '-o', default=os.path.join(BASE_DIR, 'site_contents'), help='保存路径 (默认: ./site_contents)')
    parser.add_argument('--top', '-n', type=int, default=None, help='获取前N条 (默认: 全部)')

    args = parser.parse_args()

    if not args.site:
        print("用法: python tophub_spider.py <网站名称> [--output 路径] [--top 数量]")
        print("示例: python tophub_spider.py 知乎 --top 10")
        print("      python tophub_spider.py 微信 -o /tmp/data -n 5")

        # 尝试列出可用站点
        sites = load_cached_data()
        if sites:
            print("\n可用的站点:")
            for s in sorted(sites.keys()):
                print(f"  - {s} ({len(sites[s])} 条)")
        return

    run(args.site, args.output, args.top)


if __name__ == '__main__':
    main()
