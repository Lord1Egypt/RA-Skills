#!/usr/bin/env python3
"""
🔄 板块轮动 识别 v1.0

核心 思想:
  6/24 CPO 主升 / 6/23 杀跌 → 资金风格切换没识别 = 痛点
  
监控:
  1. 板块 指数 / 日量能 / 7 日 / 30 日 强弱
  2. 主升 板块 vs 退潮 板块 自动 切换
  3. 与持仓 板块 联动 警报

用法:
  python3 sector_rotation.py                 # 全市场扫描
  python3 sector_rotation.py --top 10        # TOP 10
  python3 sector_rotation.py --my            # 仅监控你持仓相关板块
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime


# 持仓 关联 板块 (你 4 只 + watchlist)
MY_SECTORS = {
    'BK0480': '半导体',
    'BK1036': '光通信',
    'BK0900': 'AI 算力',
    'BK0473': '医药',
    'BK0727': '通信设备',
    'BK0918': '电子',
}


def fetch_all_sectors() -> list:
    """抓取 东财 全市场 板块指数"""
    # 行业板块
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        'pn': '1', 'pz': '100', 'po': '1', 'np': '1',
        'fltt': '2', 'invt': '2',
        'fs': 'm:90+t:2+f:!50',  # 行业板块
        'fields': 'f12,f14,f3,f2,f5,f6,f15,f16',
    }
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com/'}
    req = urllib.request.Request(full_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
        return data.get('data', {}).get('diff', [])
    except Exception as e:
        return []


def fetch_concept_sectors() -> list:
    """抓取 东财 概念板块"""
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        'pn': '1', 'pz': '200', 'po': '1', 'np': '1',
        'fltt': '2', 'invt': '2',
        'fs': 'm:90+t:3+f:!50',  # 概念板块
        'fields': 'f12,f14,f3,f2,f5,f6,f15,f16',
    }
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com/'}
    req = urllib.request.Request(full_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
        return data.get('data', {}).get('diff', [])
    except: return []


def main():
    parser = argparse.ArgumentParser(description='板块 轮动 识别 v1.0')
    parser.add_argument('--top', type=int, default=10, help='显示 TOP N')
    parser.add_argument('--my', action='store_true', help='仅监控 我持仓 关联')
    args = parser.parse_args()
    
    print(f"🔄 板块 轮动 识别 v1.0  /  {datetime.now():%Y-%m-%d %H:%M}")
    print()
    
    # 行业板块
    industries = fetch_all_sectors()
    if industries:
        industries_sorted = sorted(industries, key=lambda x: -x.get('f3', 0))
        print("=" * 60)
        print("🚀 行业板块 涨幅榜 (TOP 10)")
        print("=" * 60)
        print(f"{'板块':<14s} {'代码':<10s} {'涨幅':>8s} {'量比':>6s} {'换手':>6s}")
        print("-" * 55)
        for s in industries_sorted[:args.top]:
            name = s.get('f14', '')[:10]
            code = s.get('f12', '')
            chg = s.get('f3', 0)
            tn = s.get('f5', 0)  # 量
            ratio = s.get('f6', 0) / 1e8  # 成交额
            flag = '🔥' if chg > 3 else '🟢' if chg > 0 else '🔴'
            print(f"  {name:<12s}  {code:<8s}  {flag}{chg:>+5.2f}%  {ratio:>5.1f}亿")
    
    # 概念板块
    concepts = fetch_concept_sectors()
    if concepts:
        concepts_sorted = sorted(concepts, key=lambda x: -x.get('f3', 0))
        print()
        print("=" * 60)
        print("⚡ 概念板块 涨幅榜 (TOP 10)")
        print("=" * 60)
        print(f"{'板块':<14s} {'代码':<10s} {'涨幅':>8s} {'成交额':>8s}")
        print("-" * 55)
        for s in concepts_sorted[:args.top]:
            name = s.get('f14', '')[:10]
            code = s.get('f12', '')
            chg = s.get('f3', 0)
            ratio = s.get('f6', 0) / 1e8
            flag = '🔥' if chg > 3 else '🟢' if chg > 0 else '🔴'
            print(f"  {name:<12s}  {code:<8s}  {flag}{chg:>+5.2f}%  {ratio:>5.1f}亿")
        
        print()
        print("=" * 60)
        print("🔴 概念板块 跌幅榜 (BOTTOM 10)")
        print("=" * 60)
        for s in concepts_sorted[-10:]:
            name = s.get('f14', '')[:10]
            chg = s.get('f3', 0)
            ratio = s.get('f6', 0) / 1e8
            print(f"  {name:<12s}  🔴{chg:>+5.2f}%  {ratio:>5.1f}亿")
    
    # 你 持仓 关联 板块
    print()
    print("=" * 60)
    print("💎 你 持仓 关联 板块 监控")
    print("=" * 60)
    target_keywords = ['半导体', '光模块', 'CPO', 'AI', '碳化硅', 'SiC', '海缆', 'CXO', '医药外包', '硅光']
    if concepts:
        for kw in target_keywords:
            matched = [s for s in concepts if kw in s.get('f14', '')]
            for s in matched[:2]:
                name = s.get('f14', '')
                chg = s.get('f3', 0)
                ratio = s.get('f6', 0) / 1e8
                flag = '🔥' if chg > 3 else '🟢' if chg > 0 else '🟡' if chg > -2 else '🔴'
                print(f"  {flag} {name:<14s}  {chg:>+6.2f}%  成交 {ratio:>5.1f}亿")


if __name__ == '__main__':
    main()
