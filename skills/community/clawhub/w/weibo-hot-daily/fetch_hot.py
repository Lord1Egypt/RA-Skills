#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜日报 v2.0 - 自动抓取微博热搜榜
作者: 小天🦞
版本: 2.0.0
"""

import argparse
import json
import csv
import sys
import os
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Optional

# 设置控制台编码
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 微博热搜API地址
WEIBO_HOT_API = "https://weibo.com/ajax/side/hotSearch"

# 分类名称映射
CATEGORY_MAP = {
    'all': '全部',
    'entertainment': '娱乐',
    'sports': '体育',
    'tech': '科技',
    'society': '社会',
    'finance': '财经',
    'international': '国际'
}


class WeiboHotFetcher:
    """微博热搜抓取器"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://weibo.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cookie': 'SUB=_2AkMWJzUjf8NxqwFRmP8RxWjnaY10ywzEieKnc3-_JRMxHRl-yT9kqlcatRB6PaaX1URGBqDAY-2n7xAu7MM5S5jv7p5D'
        }

    def fetch_hot(self, top: int = 50, category: str = 'all') -> List[Dict]:
        """获取热搜榜"""
        url = WEIBO_HOT_API

        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))

            if data.get('ok') != 1:
                print(f"[ERROR] API错误: {data.get('msg', '未知错误')}", file=sys.stderr)
                return []

            realtime = data.get('data', {}).get('realtime', [])
            return [self._parse_topic(t, i+1) for i, t in enumerate(realtime[:top])]

        except urllib.error.URLError as e:
            print(f"[ERROR] 网络错误: {e}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"[ERROR] 未知错误: {e}", file=sys.stderr)
            return []

    def _parse_topic(self, topic: Dict, rank: int) -> Dict:
        """解析热搜数据"""
        return {
            'rank': rank,
            'title': topic.get('word', ''),
            'hot_value': topic.get('num', 0),
            'category': topic.get('category', '其他'),
            'label_name': topic.get('label_name', ''),
            'url': f"https://s.weibo.com/weibo?q={urllib.request.quote(topic.get('word', ''))}"
        }


def format_number(num: int) -> str:
    """格式化数字（万/亿）"""
    if num >= 100000000:
        return f"{num/100000000:.1f}亿"
    if num >= 10000:
        return f"{num/10000:.1f}万"
    return str(num)


def generate_summary(topics: List[Dict], api_key: Optional[str] = None) -> str:
    """生成AI摘要"""
    if not api_key:
        # 简单摘要（不需要API）
        categories = {}
        total_hot = 0

        for t in topics:
            cat = t.get('category', '其他')
            categories[cat] = categories.get(cat, 0) + 1
            total_hot += t.get('hot_value', 0)

        top_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
        cat_str = "、".join([c[0] for c in top_cats])

        return (
            f"[SUMMARY] 今日热搜摘要\n"
            f"共 {len(topics)} 个热搜话题，"
            f"总热度 {format_number(total_hot)}\n"
            f"热门分类：{cat_str}\n"
            f"Top 1：{topics[0]['title']}（热度 {format_number(topics[0]['hot_value'])}）"
        )

    # TODO: 调用OpenAI API生成更详细的摘要
    return "AI摘要功能需要配置OpenAI API Key"


def output_json(topics: List[Dict], output_file: str, summary: str = ""):
    """输出JSON格式"""
    result = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'total': len(topics),
        'summary': summary,
        'topics': topics
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"[OK] 已保存到 {output_file}")


def output_csv(topics: List[Dict], output_file: str):
    """输出CSV格式"""
    if not topics:
        print("[ERROR] 没有数据可导出")
        return

    fieldnames = ['rank', 'title', 'hot_value', 'category', 'label_name', 'url']

    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for t in topics:
            writer.writerow({k: t.get(k, '') for k in fieldnames})

    print(f"[OK] 已保存到 {output_file}")


def print_table(topics: List[Dict]):
    """打印表格到终端"""
    if not topics:
        print("[ERROR] 没有数据")
        return

    print("\n" + "="*80)
    print(f"[HOT] 微博热搜榜 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*80)

    for t in topics:
        print(f"\n#{t['rank']} {t['title']}")
        print(f"   [HOT] {format_number(t['hot_value'])} | [CAT] {t.get('category', '其他')}")
        if t.get('label_name'):
            print(f"   [LABEL] {t['label_name']}")
        print(f"   [LINK] {t['url']}")

    print("\n" + "="*80)


def main():
    parser = argparse.ArgumentParser(description='[HOT] 微博热搜日报 - 抓取微博热搜榜')
    parser.add_argument('--top', type=int, default=50, help='获取话题数量 (默认: 50)')
    parser.add_argument('--category', type=str, default='all', help='分类筛选 (entertainment/sports/tech/society/finance/international)')
    parser.add_argument('--summary', action='store_true', help='生成摘要')
    parser.add_argument('--api-key', type=str, help='OpenAI API Key')
    parser.add_argument('--output', type=str, help='输出文件路径')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='输出格式')
    parser.add_argument('--quiet', action='store_true', help='静默模式')

    args = parser.parse_args()

    # 抓取数据
    fetcher = WeiboHotFetcher()
    topics = fetcher.fetch_hot(top=args.top, category=args.category)

    if not topics:
        print("[ERROR] 未获取到数据")
        sys.exit(1)

    # 生成摘要
    summary = ""
    if args.summary:
        summary = generate_summary(topics, args.api_key)

    # 输出
    if not args.quiet:
        print_table(topics)
        if summary:
            print(f"\n[SUMMARY] 摘要：\n{summary}")

    # 保存文件
    if args.output:
        if args.format == 'csv':
            output_csv(topics, args.output)
        else:
            output_json(topics, args.output, summary)

    return topics


if __name__ == '__main__':
    main()
