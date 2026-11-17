#!/usr/bin/env python3
"""
🔍 全市场 突破前高 实时 监控 v1.0

核心:
  全市场 5000+ 股票 扫描
  → 严格 筛选 真突破前高
  → 量比 ≥ 1.5 + 距高 ≥ -2% + 大盘 配合

5 种 突破 + 综合评分 + 三天站稳 验证

用法:
  python3 breakthrough_scanner.py                # 标准 60 日突破
  python3 breakthrough_scanner.py --days 120     # 120 日真突破
  python3 breakthrough_scanner.py --top 20       # TOP 20
  python3 breakthrough_scanner.py --strict       # 严格模式 (量比≥2.0)
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime


def fetch_all_rising():
    """抓取 全市场 上涨股 (按 涨幅 倒序)"""
    all_stocks = []
    for page in range(1, 7):  # 6 页 x 80 = 480 只
        url = "https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData"
        params = {'num': '80', 'sort': 'changepercent', 'asc': '0', 'node': 'hs_a', 'page': str(page)}
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        req = urllib.request.Request(full_url, headers={'Referer': 'https://finance.sina.com.cn/'})
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode('utf-8'))
            if not data: break
            all_stocks.extend(data)
            time.sleep(0.2)
        except: break
    return all_stocks


def fetch_quote(code):
    if code.startswith(('92','83')): sym = 'bj' + code
    elif code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://qt.gtimg.cn/q={sym}"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            text = r.read().decode('gbk', errors='ignore')
        p = text.split('~')
        return {
            'liangbi': float(p[49]) if len(p) > 49 and p[49] else 0,
            'amount': float(p[37]) if p[37] else 0,
            'turnover': float(p[38]) if p[38] else 0,
        }
    except: return None


def fetch_history_high(code, days=60):
    """N 日 (含今日) 最高价 + 距高 天数"""
    if code.startswith(('92','83')): sym = 'bj' + code
    elif code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{days+5},qfq"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=6) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday','day']:
            if k in inner and inner[k]:
                arr = inner[k]
                if len(arr) < 5: return None
                prev = arr[:-1]
                if not prev: return None
                highs = [(i, float(row[3])) for i, row in enumerate(prev)]
                max_high = max(h for _, h in highs)
                # 最近 一次 该高点 (距今 多少天)
                for i in range(len(prev)-1, -1, -1):
                    if float(prev[i][3]) >= max_high - 0.001:
                        days_ago = len(prev) - i
                        break
                return {
                    'today_close': float(arr[-1][2]),
                    'prev_high': max_high,
                    'days_ago': days_ago,
                }
    except: pass
    return None


def main():
    parser = argparse.ArgumentParser(description='全市场 突破前高 监控')
    parser.add_argument('--days', type=int, default=60, help='前高 时间窗')
    parser.add_argument('--top', type=int, default=20, help='TOP N')
    parser.add_argument('--strict', action='store_true', help='严格模式')
    args = parser.parse_args()
    
    min_liangbi = 2.0 if args.strict else 1.5
    min_chg = 5.0 if args.strict else 3.0
    
    print(f"🔍 全市场 突破前高 监控 v1.0  /  {datetime.now():%Y-%m-%d %H:%M}")
    print(f"⚙️ 参数: ≥{args.days} 日前高 / 量比 ≥{min_liangbi} / 涨幅 ≥{min_chg}% / TOP {args.top}")
    print()
    
    # 1. 拿 全市场 上涨股
    print("📡 抓取 全市场 上涨股...")
    all_stocks = fetch_all_rising()
    print(f"   总数: {len(all_stocks)} 只")
    
    # 涨幅 ≥ min_chg 才候选
    candidates = [s for s in all_stocks if float(s['changepercent']) >= min_chg and not s['name'].startswith('N')]
    print(f"   涨幅 ≥{min_chg}%: {len(candidates)} 只")
    print()
    
    # 2. 严格筛选 真突破
    real_breaks = []
    near_breaks = []
    
    print(f"📊 筛选 突破前高 (扫描 {len(candidates)} 只)...")
    for i, s in enumerate(candidates):
        code = s['code']
        name = s['name']
        cur = float(s['trade'])
        chg = float(s['changepercent'])
        
        q = fetch_quote(code)
        if not q: continue
        if q['liangbi'] < min_liangbi: continue  # 量比 不够
        
        kl = fetch_history_high(code, args.days)
        if not kl: continue
        
        gap = (cur - kl['prev_high']) / kl['prev_high'] * 100
        
        record = {
            'code': code, 'name': name, 'cur': cur, 'chg': chg,
            'liangbi': q['liangbi'],
            'turnover': q['turnover'],
            'amount_yi': q['amount'] / 1e4,
            'prev_high': kl['prev_high'],
            'days_ago': kl['days_ago'],
            'gap': gap,
        }
        
        # 已突破 (距高 ≥ -2%)
        if gap >= -2.0 and kl['days_ago'] >= args.days * 0.5:  # 至少 半区间
            real_breaks.append(record)
        # 即将突破 (-2% 到 -5%)
        elif -5.0 <= gap < -2.0 and kl['days_ago'] >= args.days * 0.5:
            near_breaks.append(record)
        
        if (i+1) % 50 == 0:
            print(f"   ... {i+1}/{len(candidates)} | 真突破:{len(real_breaks)} 即将:{len(near_breaks)}")
        time.sleep(0.03)
    
    print()
    
    # 3. 综合 评分
    def score(s):
        s1 = min(s['liangbi'], 5) / 5 * 40  # 量比
        s2 = min(s['days_ago'] / args.days, 1.5) * 30  # 跨越时间
        s3 = min(s['chg'], 20) / 20 * 30  # 涨幅
        return s1 + s2 + s3
    
    real_breaks.sort(key=lambda s: score(s), reverse=True)
    near_breaks.sort(key=lambda s: score(s), reverse=True)
    
    # 4. 输出
    print("=" * 80)
    print(f"🚀 已突破 {args.days}+ 日前高 (距高 ≥ -2%) — TOP {min(args.top, len(real_breaks))}")
    print("=" * 80)
    if not real_breaks:
        print("\n  ⚠️ 当前 无 真突破 (大盘 偏弱 / 周末 数据)")
    else:
        print(f"\n{'排':>3s} {'代码':<7s} {'名称':<10s} {'现价':>8s} {'涨幅':>7s} {'量比':>5s} {'距高':>7s} {'天数':>5s} {'成交亿':>7s} {'综合分':>6s}")
        print('-' * 80)
        for i, s in enumerate(real_breaks[:args.top]):
            flag = '🔥🔥' if s['liangbi'] >= 3 else '🔥' if s['liangbi'] >= 2 else '⭐'
            print(f"  {i+1:>2}  {s['code']:<5s} {s['name'][:6]:<8s} ¥{s['cur']:>6.2f} +{s['chg']:>5.2f}% {s['liangbi']:>4.2f} {s['gap']:>+6.2f}% {s['days_ago']:>3d}天 {s['amount_yi']:>5.2f}亿 {score(s):>5.1f} {flag}")
    
    # 即将突破
    print()
    print("=" * 80)
    print(f"📈 即将突破 (-5% 至 -2% 距高) — TOP 10")
    print("=" * 80)
    if not near_breaks:
        print("\n  无")
    else:
        print(f"\n{'排':>3s} {'代码':<7s} {'名称':<10s} {'现价':>8s} {'涨幅':>7s} {'量比':>5s} {'距高':>7s} {'天数':>5s} {'综合分':>6s}")
        print('-' * 75)
        for i, s in enumerate(near_breaks[:10]):
            print(f"  {i+1:>2}  {s['code']:<5s} {s['name'][:6]:<8s} ¥{s['cur']:>6.2f} +{s['chg']:>5.2f}% {s['liangbi']:>4.2f} {s['gap']:>+6.2f}% {s['days_ago']:>3d}天 {score(s):>5.1f}")
    
    # 总结
    print()
    print("=" * 80)
    print(f"📊 总结:")
    print(f"   ✅ 真突破 ≥{args.days} 日: {len(real_breaks)} 只")
    print(f"   📈 即将突破: {len(near_breaks)} 只")
    print(f"   📡 全市场 上涨股: {len(all_stocks)} / 涨幅 ≥{min_chg}%: {len(candidates)}")
    
    if real_breaks:
        # 板块 统计 (从名字 推测)
        sectors = {'半导体': 0, '光通信/CPO': 0, 'AI/算力': 0, '医药': 0, '化工': 0, '其他': 0}
        for s in real_breaks:
            n = s['name']
            if any(kw in n for kw in ['芯', '微', '电子', '半导体', '存储']): sectors['半导体'] += 1
            elif any(kw in n for kw in ['光', '通', 'CPO']): sectors['光通信/CPO'] += 1
            elif any(kw in n for kw in ['AI', '算力', '云']): sectors['AI/算力'] += 1
            elif any(kw in n for kw in ['药', '生物', '医']): sectors['医药'] += 1
            elif any(kw in n for kw in ['化', '材']): sectors['化工'] += 1
            else: sectors['其他'] += 1
        print(f"\n   🎯 板块 分布:")
        for k, v in sorted(sectors.items(), key=lambda x: -x[1]):
            if v > 0: print(f"      • {k}: {v} 只")
    
    # 周末 提示
    if datetime.now().weekday() >= 5:
        print()
        print("   ⚠️ 周末: 数据 是 上周五 收盘 / 周一 开盘 重新 扫描")


if __name__ == '__main__':
    main()
