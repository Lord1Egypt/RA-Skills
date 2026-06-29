#!/usr/bin/env python3
"""
🚨 实时盘中警报 v1.0

核心 痛点:
  罗博 6/26 -9.14% 大跌 你 没看到 = 错过 减仓最佳时机
  
监控 5 种 触发条件:
  1. 跌幅 ≥ -3% (减仓 警示)
  2. 跌幅 ≥ -5% (紧急减仓)
  3. 量比 ≥ 3 + 涨幅 < 1% (高位 滞涨)
  4. 跌破 MA20 (趋势破位)
  5. 突破前高 + 放量 (买点机会)

用法:
  python3 realtime_alerts.py                       # 全持仓 单次扫描
  python3 realtime_alerts.py --watch               # 持续 监控 (cron 每 5 分钟)
  python3 realtime_alerts.py --critical-only       # 仅 P0 紧急
"""

import argparse
import json
import os
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

# 持仓 + watchlist
HOLDINGS = {
    '600522': {'name': '中天科技', 'cost': 45.97, 'qty': 42200},
    '000988': {'name': '华工科技', 'cost': 146.40, 'qty': 9400},
    '300757': {'name': '罗博特科', 'cost': 309.50, 'qty': 2500},
    '688234': {'name': '天岳先进', 'cost': 182.35, 'qty': 2024},
    '603259': {'name': '药明康德', 'cost': 0, 'qty': 0, 'watchlist': True},
}

ALERT_STATE_FILE = Path.home() / '.openclaw' / 'workspace' / 'memory' / '_alerts_state.json'


def fetch_quote(code):
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://qt.gtimg.cn/q={sym}"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            text = r.read().decode('gbk', errors='ignore')
        p = text.split('~')
        return {
            'current': float(p[3]),
            'prev_close': float(p[4]),
            'high': float(p[33]),
            'low': float(p[34]),
            'liangbi': float(p[49]) if len(p) > 49 and p[49] else 0,
            'turnover': float(p[38]) if p[38] else 0,
            'timestamp': p[30] if len(p) > 30 else '',
        }
    except: return None


def fetch_ma20(code):
    """日线 MA20"""
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,25,qfq"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday','day']:
            if k in inner and inner[k]:
                closes = [float(row[2]) for row in inner[k][-20:]]
                if closes: return sum(closes) / len(closes)
    except: pass
    return None


def fetch_historic_high(code, days=60):
    """N 日 最高"""
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{days+5},qfq"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday','day']:
            if k in inner and inner[k]:
                arr = inner[k][-days-1:-1]  # 不含今天
                if arr: return max(float(row[3]) for row in arr)
    except: pass
    return None


def check_alerts(code, holding):
    """检查 单股 5 种 触发条件"""
    quote = fetch_quote(code)
    if not quote: return None
    
    current = quote['current']
    prev = quote['prev_close']
    chg_pct = (current - prev) / prev * 100
    liangbi = quote['liangbi']
    
    alerts = []
    
    # 1. 跌幅 ≥ -3% (P1 警示)
    if chg_pct <= -5:
        alerts.append(('🚨🚨', 'P0', f'跌幅 {chg_pct:.2f}% / 紧急减仓'))
    elif chg_pct <= -3:
        alerts.append(('🚨', 'P1', f'跌幅 {chg_pct:.2f}% / 警惕'))
    
    # 2. 涨幅 ≥ +5% (机会信号)
    if chg_pct >= 8:
        alerts.append(('🚀', 'P1', f'涨幅 {chg_pct:.2f}% / 强势/可减仓锁利'))
    elif chg_pct >= 5:
        alerts.append(('🟢', 'P2', f'涨幅 {chg_pct:.2f}% / 关注'))
    
    # 3. 量比 异常
    if liangbi >= 3 and abs(chg_pct) < 1:
        alerts.append(('⚠️', 'P0', f'量比 {liangbi:.2f} 但 涨幅 {chg_pct:.2f}% / 滞涨'))
    elif liangbi >= 3:
        alerts.append(('📊', 'P2', f'量比 {liangbi:.2f} 异常 放量'))
    
    # 4. 跌破 MA20
    ma20 = fetch_ma20(code)
    if ma20 and current < ma20 * 0.99:
        gap = (current - ma20) / ma20 * 100
        alerts.append(('🔴', 'P0', f'跌破 MA20 ({gap:.2f}%) / 趋势 破位'))
    elif ma20 and current < ma20 * 1.01:
        alerts.append(('🟡', 'P2', f'接近 MA20 ¥{ma20:.2f}'))
    
    # 5. 突破前高 + 放量
    high_60 = fetch_historic_high(code, 60)
    if high_60 and current > high_60 * 1.005 and liangbi >= 1.5:
        alerts.append(('🌟', 'P0', f'突破 60 日 前高 + 量比 {liangbi:.2f} / 买点'))
    elif high_60 and current >= high_60 * 0.99:
        alerts.append(('🟢', 'P2', f'接近 60 日 前高 ¥{high_60:.2f}'))
    
    # 持仓 损益
    pnl = None
    if holding.get('qty', 0) > 0:
        pnl_value = (current - holding['cost']) * holding['qty']
        pnl_pct = (current - holding['cost']) / holding['cost'] * 100
        # 单日 浮盈/亏 变化
        today_pnl = (current - prev) * holding['qty']
        pnl = {
            'total_pnl': pnl_value,
            'total_pnl_pct': pnl_pct,
            'today_pnl': today_pnl,
        }
    
    return {
        'code': code,
        'name': holding['name'],
        'current': current,
        'chg_pct': chg_pct,
        'liangbi': liangbi,
        'alerts': alerts,
        'pnl': pnl,
        'timestamp': quote['timestamp'],
    }


def load_state():
    if ALERT_STATE_FILE.exists():
        try: return json.loads(ALERT_STATE_FILE.read_text())
        except: pass
    return {}


def save_state(state):
    ALERT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    ALERT_STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def format_output(result, critical_only=False):
    """格式化 警报 报告"""
    r = result
    
    # 过滤
    alerts = r['alerts']
    if critical_only:
        alerts = [a for a in alerts if a[1] in ('P0', 'P1')]
    
    if not alerts:
        return None  # 无 警报 / 跳过
    
    pnl_str = ""
    if r['pnl']:
        p = r['pnl']
        pnl_str = f" | 浮盈 ¥{p['total_pnl']:+,.0f} ({p['total_pnl_pct']:+.1f}%) / 今日 ¥{p['today_pnl']:+,.0f}"
    
    flag = '🚀' if r['chg_pct'] > 0 else '🔴'
    
    output = f"""
🔔 {r['name']} ({r['code']}) {flag} ¥{r['current']:.2f} ({r['chg_pct']:+.2f}%){pnl_str}
"""
    for emoji, priority, msg in alerts:
        output += f"  {emoji} [{priority}] {msg}\n"
    
    return output


def main():
    parser = argparse.ArgumentParser(description='实时盘中警报 v1.0')
    parser.add_argument('--code', help='单股 代码')
    parser.add_argument('--watch', action='store_true', help='循环监控 (cron)')
    parser.add_argument('--critical-only', action='store_true', help='仅 P0/P1')
    args = parser.parse_args()
    
    print(f"🚨 实时盘中警报 v1.0  /  {datetime.now():%Y-%m-%d %H:%M:%S}")
    
    targets = HOLDINGS
    if args.code:
        if args.code in HOLDINGS: targets = {args.code: HOLDINGS[args.code]}
        else: 
            print(f"❌ 未配置 {args.code}")
            sys.exit(1)
    
    state = load_state()
    new_state = {}
    
    p0_count = 0
    p1_count = 0
    has_alerts = False
    
    for code, holding in targets.items():
        result = check_alerts(code, holding)
        if not result: continue
        
        output = format_output(result, args.critical_only)
        if output:
            print(output)
            has_alerts = True
            for _, pri, _ in result['alerts']:
                if pri == 'P0': p0_count += 1
                elif pri == 'P1': p1_count += 1
        
        new_state[code] = {
            'last_check': datetime.now().isoformat(),
            'current': result['current'],
            'chg_pct': result['chg_pct'],
        }
    
    save_state(new_state)
    
    print()
    print("=" * 60)
    if has_alerts:
        print(f"📊 警报 总结: P0 关键 {p0_count} 条 | P1 重要 {p1_count} 条")
        if p0_count > 0:
            print("🚨 立刻 关注 P0 警报 / 可能 需要 立刻 操作!")
    else:
        print("✅ 全持仓 无 警报 / 平稳")


if __name__ == '__main__':
    main()
