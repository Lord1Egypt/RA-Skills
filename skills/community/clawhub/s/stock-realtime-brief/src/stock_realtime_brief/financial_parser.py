#!/usr/bin/env python3
"""
📊 财报自动解析 v1.0

数据源: 东财 datacenter API
联动: v2.1 / DCF / 北极星

用法:
  python3 financial_parser.py                  # 全持仓最新
  python3 financial_parser.py --code 600522    # 单股
"""

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime


WATCH_LIST = {
    '600522': '中天科技',
    '000988': '华工科技',
    '300757': '罗博特科',
    '688234': '天岳先进',
    '603259': '药明康德',
}


def fetch_financial(code):
    """东财 业绩报表 API"""
    url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'reportName': 'RPT_LICO_FN_CPD',
        'columns': 'ALL',
        'filter': f'(SECURITY_CODE="{code}")',
        'pageSize': '8',
        'sortColumns': 'REPORTDATE',
        'sortTypes': '-1',
    }
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(full_url, headers={
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://data.eastmoney.com/',
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode('utf-8'))
        if not data.get('success'): return None
        return data.get('result', {}).get('data', [])
    except: return None


def format_quarter(date_str):
    if not date_str: return ''
    d = date_str[:10]
    year = d[:4]
    if '03-31' in d: return f"{year} Q1"
    if '06-30' in d: return f"{year} 半年"
    if '09-30' in d: return f"{year} Q3"
    if '12-31' in d: return f"{year} 全年"
    return d


def f(v, default=0):
    """安全转 float"""
    if v is None: return default
    try: return float(v)
    except: return default


def analyze_financial(code, name):
    print(f"\n{'=' * 65}")
    print(f"📊 财报 解析 - {name} ({code})")
    print('=' * 65)
    
    data = fetch_financial(code)
    if not data:
        print("❌ 数据获取失败")
        return None
    
    print(f"\n📅 最近 5 期 业绩 (按 报告期 倒序):\n")
    print(f"{'期间':<14s} {'营收YoY':>10s} {'净利YoY':>10s} {'ROE':>8s} {'毛利率':>9s} {'EPS':>8s}")
    print('-' * 75)
    
    metrics = []
    for d in data[:5]:
        period = format_quarter(d.get('REPORTDATE', ''))
        rev_yoy = f(d.get('YSTZ'))
        net_yoy = f(d.get('SJLTZ'))
        roe = f(d.get('WEIGHTAVG_ROE'))
        gm = f(d.get('XSMLL'))
        eps = f(d.get('BASIC_EPS'))
        
        metrics.append({
            'period': period,
            'rev_yoy': rev_yoy,
            'net_yoy': net_yoy,
            'roe': roe,
            'gm': gm,
            'eps': eps,
        })
        
        rev_flag = '🚀' if rev_yoy > 30 else '🟢' if rev_yoy > 10 else '🟡' if rev_yoy > 0 else '🔴'
        net_flag = '🚀' if net_yoy > 30 else '🟢' if net_yoy > 10 else '🟡' if net_yoy > 0 else '🔴'
        
        print(f"  {period:<12s} {rev_flag}{rev_yoy:>+7.1f}%  {net_flag}{net_yoy:>+7.1f}%  {roe:>6.2f}%  {gm:>7.2f}%  ¥{eps:>5.2f}")
    
    # v2.1 评分 联动
    print(f"\n💡 v2.1 选股 联动 评分 (基本面 25 分细分):\n")
    if metrics:
        latest = metrics[0]
        scores = {}
        
        # 营收增速 5 分
        rev_yoy = latest['rev_yoy']
        if rev_yoy >= 30: scores['rev'] = 5
        elif rev_yoy >= 20: scores['rev'] = 4
        elif rev_yoy >= 10: scores['rev'] = 3
        elif rev_yoy >= 0: scores['rev'] = 1
        else: scores['rev'] = 0
        print(f"  • 营收增速 {rev_yoy:+.1f}%: {scores['rev']}/5")
        
        # 净利增速 5 分
        net_yoy = latest['net_yoy']
        if net_yoy >= 30: scores['net'] = 5
        elif net_yoy >= 20: scores['net'] = 4
        elif net_yoy >= 10: scores['net'] = 3
        elif net_yoy >= 0: scores['net'] = 1
        else: scores['net'] = 0
        print(f"  • 净利增速 {net_yoy:+.1f}%: {scores['net']}/5")
        
        # ROE 8 分
        roe = latest['roe']
        if roe >= 20: scores['roe'] = 8
        elif roe >= 15: scores['roe'] = 6
        elif roe >= 10: scores['roe'] = 4
        elif roe >= 5: scores['roe'] = 2
        else: scores['roe'] = 0
        print(f"  • ROE {roe:.2f}%: {scores['roe']}/8")
        
        # 毛利率 4 分
        gm = latest['gm']
        if gm >= 50: scores['gm'] = 4
        elif gm >= 40: scores['gm'] = 3
        elif gm >= 30: scores['gm'] = 2
        elif gm >= 20: scores['gm'] = 1
        else: scores['gm'] = 0
        print(f"  • 毛利率 {gm:.2f}%: {scores['gm']}/4")
        
        # 持续性 3 分
        positive = sum(1 for m in metrics if m['net_yoy'] > 0)
        if positive >= 5: scores['cont'] = 3
        elif positive >= 4: scores['cont'] = 2
        elif positive >= 3: scores['cont'] = 1
        else: scores['cont'] = 0
        print(f"  • 持续性 {positive}/5 季正增: {scores['cont']}/3")
        
        total = sum(scores.values())
        print(f"\n  📊 基本面 评分: {total}/25")
        
        if total >= 20: level = '🌟🌟🌟🌟🌟 优秀'
        elif total >= 15: level = '🌟🌟🌟🌟 合格'
        elif total >= 10: level = '🟡 中性'
        else: level = '🔴 不合格'
        print(f"  💎 评级: {level}")
        
        # 趋势 警示
        if len(metrics) >= 3:
            recent_avg = (metrics[0]['net_yoy'] + metrics[1]['net_yoy']) / 2
            earlier_avg = sum(m['net_yoy'] for m in metrics[2:5]) / max(len(metrics[2:5]), 1)
            if recent_avg - earlier_avg > 15:
                print(f"\n  🌟 信号: 净利 增速 加速 ({earlier_avg:.1f}% → {recent_avg:.1f}%)")
            elif earlier_avg - recent_avg > 15:
                print(f"\n  ⚠️ 警示: 净利 增速 下行 ({earlier_avg:.1f}% → {recent_avg:.1f}%)")
    
    return metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--code', help='单股代码')
    args = parser.parse_args()
    
    print(f"📊 财报自动解析 v1.0  /  {datetime.now():%Y-%m-%d %H:%M}")
    
    targets = WATCH_LIST
    if args.code:
        if args.code in WATCH_LIST: targets = {args.code: WATCH_LIST[args.code]}
        else: print(f"❌ 未配置: {args.code}"); sys.exit(1)
    
    all_metrics = {}
    for code, name in targets.items():
        m = analyze_financial(code, name)
        if m: all_metrics[code] = m
    
    # 汇总
    print(f"\n{'=' * 70}")
    print("📊 全持仓 财报 汇总 (最新季度)")
    print('=' * 70)
    print(f"{'股票':<10s} {'期间':<12s} {'营收YoY':>9s} {'净利YoY':>9s} {'ROE':>8s} {'毛利率':>9s}")
    print('-' * 65)
    for code, metrics in all_metrics.items():
        if metrics:
            m = metrics[0]
            name = WATCH_LIST.get(code, code)
            print(f"  {name:<8s} {m['period']:<10s} {m['rev_yoy']:>+7.1f}%  {m['net_yoy']:>+7.1f}% {m['roe']:>6.2f}% {m['gm']:>7.2f}%")


if __name__ == '__main__':
    main()
