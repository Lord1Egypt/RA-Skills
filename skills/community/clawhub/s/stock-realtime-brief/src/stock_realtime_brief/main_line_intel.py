#!/usr/bin/env python3
"""
🎯 行业主线智能识别 v1.0

核心:
  自动识别 当前 主升浪 主线板块
  • 主线 / 二线 / 退潮 三级分类
  • 资金流 + 量价 + 龙头突破 综合
  • 与持仓 联动 (避免 错过 板块切换)

用法:
  python3 main_line_intel.py                # 全市场扫描 + TOP 主线
  python3 main_line_intel.py --my           # 仅 看 我持仓 关联板块
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime


def fetch_concept_sectors():
    """抓取 东财 概念板块 + 量能 + 资金流"""
    url = "https://push2.eastmoney.com/api/qt/clist/get"
    params = {
        'pn': '1', 'pz': '300', 'po': '1', 'np': '1',
        'fltt': '2', 'invt': '2',
        'fs': 'm:90+t:3+f:!50',
        'fields': 'f12,f14,f3,f2,f5,f6,f8,f62,f184,f105',
    }
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(full_url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://quote.eastmoney.com/',
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
        return data.get('data', {}).get('diff', [])
    except: return []


def classify_sector(sector):
    """单板块 三级分类
    主升 (热)  / 二线 (温) / 退潮 (冷)
    """
    chg = sector.get('f3', 0)
    amount_yi = sector.get('f6', 0) / 1e8
    turnover_pct = sector.get('f8', 0)
    fund_in = sector.get('f62', 0) / 1e8  # 主力净流入
    
    # 主升 评分
    score = 0
    
    # 1. 涨幅 (40 分)
    if chg >= 5: score += 40
    elif chg >= 3: score += 30
    elif chg >= 1: score += 20
    elif chg >= 0: score += 10
    
    # 2. 资金流 (30 分)
    if fund_in >= 50: score += 30
    elif fund_in >= 20: score += 20
    elif fund_in >= 5: score += 10
    elif fund_in > 0: score += 5
    
    # 3. 量能 (20 分)
    if amount_yi >= 1000: score += 20
    elif amount_yi >= 500: score += 15
    elif amount_yi >= 200: score += 10
    elif amount_yi >= 100: score += 5
    
    # 4. 换手 (10 分)
    if turnover_pct >= 5: score += 10
    elif turnover_pct >= 3: score += 7
    elif turnover_pct >= 1: score += 3
    
    if score >= 70: level = '🔥 主升'
    elif score >= 50: level = '🌡 温热'
    elif score >= 30: level = '🟡 中性'
    elif score >= 10: level = '❄️ 偏冷'
    else: level = '🧊 退潮'
    
    return score, level


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--my', action='store_true', help='仅 持仓 关联')
    args = parser.parse_args()
    
    print(f"🎯 行业主线 智能识别 v1.0  /  {datetime.now():%Y-%m-%d %H:%M}")
    print()
    
    sectors = fetch_concept_sectors()
    if not sectors:
        print("❌ 数据 获取失败")
        sys.exit(1)
    
    # 评分 + 排序
    scored = []
    for s in sectors:
        score, level = classify_sector(s)
        scored.append({
            'name': s.get('f14', ''),
            'code': s.get('f12', ''),
            'chg': s.get('f3', 0),
            'amount': s.get('f6', 0) / 1e8,
            'fund_in': s.get('f62', 0) / 1e8,
            'turnover': s.get('f8', 0),
            'score': score,
            'level': level,
        })
    
    scored.sort(key=lambda x: -x['score'])
    
    # 持仓 关联 板块
    my_keywords = ['半导体', 'CPO', '光通信', 'AI', '算力', '碳化硅', 'SiC', '海缆', 'CXO', '医药外包', '硅光', '存储芯片', 'MLCC']
    
    if args.my:
        print("=" * 65)
        print("💎 你 持仓 关联 板块 监控")
        print("=" * 65)
        for kw in my_keywords:
            matched = [s for s in scored if kw in s['name']]
            for s in matched[:2]:
                print(f"\n  {s['level']} {s['name']:<14s}")
                print(f"     涨幅: {s['chg']:+.2f}%  /  成交 {s['amount']:.1f}亿  /  主力 {s['fund_in']:+.1f}亿  /  评分 {s['score']}")
        return
    
    # 主升板块 TOP 10
    print("=" * 70)
    print("🔥 主升 板块 TOP 10 (评分 ≥ 70)")
    print("=" * 70)
    print(f"{'排':>3s} {'板块':<14s} {'涨幅':>7s} {'主力流入':>10s} {'成交':>8s} {'换手':>6s} {'评分':>5s}")
    print("-" * 70)
    main_line = [s for s in scored if s['score'] >= 70][:15]
    if not main_line:
        print("  ⚠️ 当前 无 主升 板块 (大盘 偏弱)")
    else:
        for i, s in enumerate(main_line, 1):
            print(f"  {i:>2}  {s['name'][:10]:<12s} {s['chg']:>+6.2f}% {s['fund_in']:>+8.2f}亿 {s['amount']:>6.1f}亿 {s['turnover']:>5.2f}% {s['score']:>4d}")
    
    # 温热 板块 (50-70)
    print()
    print("=" * 70)
    print("🌡 温热 板块 (评分 50-70 / 可能 启动)")
    print("=" * 70)
    warming = [s for s in scored if 50 <= s['score'] < 70][:15]
    for i, s in enumerate(warming, 1):
        print(f"  {i:>2}  {s['name'][:10]:<12s} {s['chg']:>+6.2f}% {s['fund_in']:>+8.2f}亿 {s['amount']:>6.1f}亿 {s['score']:>4d}")
    
    # 退潮板块
    print()
    print("=" * 70)
    print("🧊 退潮 板块 BOTTOM 10 (避免 / 警惕)")
    print("=" * 70)
    fading = scored[-10:]
    for i, s in enumerate(fading, 1):
        print(f"  {i:>2}  {s['name'][:10]:<12s} {s['chg']:>+6.2f}% {s['fund_in']:>+8.2f}亿 {s['amount']:>6.1f}亿 {s['score']:>4d}")
    
    # 你持仓 关联
    print()
    print("=" * 70)
    print("💎 你 持仓 关联 板块 监控")
    print("=" * 70)
    related_count = 0
    for kw in my_keywords:
        matched = [s for s in scored if kw in s['name']]
        for s in matched[:2]:
            related_count += 1
            print(f"  {s['level']} {s['name']:<14s}  {s['chg']:>+6.2f}%  主力 {s['fund_in']:>+6.1f}亿  评分 {s['score']:>3d}")
    if related_count == 0:
        print("  ⚠️ 未匹配到 持仓 关联 板块")
    
    # 总结
    print()
    print("=" * 70)
    print(f"📊 总结: 主升 {len(main_line)} 个 / 温热 {len(warming)} 个 / 总扫描 {len(scored)} 个板块")
    if main_line:
        top = main_line[0]
        print(f"\n💎 当前 第一 主线: {top['name']} (涨幅 {top['chg']:+.2f}% / 评分 {top['score']})")


if __name__ == '__main__':
    main()
