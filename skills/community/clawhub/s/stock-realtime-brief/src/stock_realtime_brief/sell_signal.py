#!/usr/bin/env python3
"""
🚨 完整卖出信号体系 v1.0

5 大 卖出信号:
  1. 三段锁利 (浮盈 +20% / +50% / +100%)
  2. RSI 超买 (RSI > 80 / 顶背离)
  3. 量价异常 (量比 >3 + 涨幅 < 1% / 高位放量滞涨)
  4. MACD 顶背离 (股价新高 + MACD 不创新高)
  5. 跌破关键位 (5/10/20 日均线)

用法:
  python3 sell_signal.py                        # 全持仓扫描
  python3 sell_signal.py --code 600522         # 单股
"""

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime


# 你的 4 只持仓 + watchlist
HOLDINGS = {
    '600522': {'name': '中天科技', 'cost': 45.97, 'qty': 42200, 'account': 'mix'},
    '000988': {'name': '华工科技', 'cost': 146.40, 'qty': 9400, 'account': 'mix'},
    '300757': {'name': '罗博特科', 'cost': 309.50, 'qty': 2500, 'account': 'mix'},
    '688234': {'name': '天岳先进', 'cost': 182.35, 'qty': 2024, 'account': 'regular'},
}


def fetch_kline(code: str, period='day', count=60):
    """拿 K 线"""
    if code.startswith(('92','83')):
        sym = 'bj' + code
    elif code.startswith(('0','3')):
        sym = 'sz' + code
    else:
        sym = 'sh' + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},{period},,,{count},qfq"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in [f'qfq{period}', period]:
            if k in inner and inner[k]: return inner[k]
    except: pass
    return []


def fetch_quote(code: str):
    """拿 实时 数据"""
    if code.startswith(('92','83')):
        sym = 'bj' + code
    elif code.startswith(('0','3')):
        sym = 'sz' + code
    else:
        sym = 'sh' + code
    url = f"https://qt.gtimg.cn/q={sym}"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode('gbk', errors='ignore')
        p = text.split('~')
        return {
            'current': float(p[3]),
            'prev_close': float(p[4]),
            'open': float(p[5]),
            'high': float(p[33]),
            'low': float(p[34]),
            'turnover': float(p[38]) if p[38] else 0,
            'liangbi': float(p[49]) if len(p) > 49 and p[49] else 0,
            'pe': p[39] if len(p) > 39 else '',
        }
    except: return None


def calc_rsi(closes: list, period=14) -> float:
    """计算 RSI"""
    if len(closes) < period + 1:
        return 50.0
    gains, losses = [], []
    for i in range(1, period + 1):
        diff = closes[-i] - closes[-i-1]
        if diff > 0:
            gains.append(diff); losses.append(0)
        else:
            gains.append(0); losses.append(-diff)
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0: return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calc_ma(closes: list, n: int) -> float:
    """计算 N 日均线"""
    if len(closes) < n: return 0
    return sum(closes[-n:]) / n


def analyze_sell_signals(code: str, holding: dict) -> dict:
    """单股 综合 卖出信号 分析"""
    quote = fetch_quote(code)
    if not quote: return {'error': '数据 获取失败'}
    
    kline = fetch_kline(code, 'day', 60)
    if not kline or len(kline) < 30:
        return {'error': 'K 线 数据 不足'}
    
    # 提取 收盘 / 最高 / 量
    closes = [float(row[2]) for row in kline]
    highs = [float(row[3]) for row in kline]
    volumes = [float(row[5]) for row in kline]
    
    current = quote['current']
    cost = holding['cost']
    
    profit_pct = (current - cost) / cost * 100
    
    # 1. 三段锁利 信号
    lock_signals = []
    if profit_pct >= 100:
        lock_signals.append(('🌟 浮盈 +100% / 应锁 1/3', 'P0'))
    if profit_pct >= 50:
        lock_signals.append(('🟢 浮盈 +50% / 应锁 1/3', 'P1'))
    if profit_pct >= 20:
        lock_signals.append(('🟡 浮盈 +20% / 应锁 1/3', 'P2'))
    
    # 2. RSI 超买 信号
    rsi = calc_rsi(closes)
    rsi_signal = None
    if rsi > 85:
        rsi_signal = (f'🚨 RSI {rsi:.0f} 严重 超买', 'P0')
    elif rsi > 80:
        rsi_signal = (f'⚠️ RSI {rsi:.0f} 超买', 'P1')
    elif rsi > 70:
        rsi_signal = (f'🟡 RSI {rsi:.0f} 偏高', 'P2')
    
    # 3. 量价 异常
    avg_vol_5 = sum(volumes[-5:]) / 5
    avg_vol_20 = sum(volumes[-20:]) / 20
    today_chg = (current - quote['prev_close']) / quote['prev_close'] * 100
    
    volume_signal = None
    if quote['liangbi'] > 3 and abs(today_chg) < 1:
        volume_signal = ('🚨 量比 >3 但 涨幅 <1% / 高位 放量 滞涨', 'P0')
    elif quote['liangbi'] > 2 and today_chg < 0:
        volume_signal = ('⚠️ 放量 下跌 / 主力 出货', 'P1')
    elif volumes[-1] > avg_vol_20 * 3 and today_chg < 2:
        volume_signal = ('🟡 量能 突变 / 警惕', 'P2')
    
    # 4. MACD 顶背离 (简化版)
    # 只看 最近 5 天 是否 创新高 vs 之前 30 天
    macd_signal = None
    recent_5_high = max(highs[-5:])
    prev_30_high = max(highs[-35:-5]) if len(highs) >= 35 else 0
    if recent_5_high > prev_30_high * 1.02:  # 创新高
        # 检查 量能 是否 跟上
        recent_5_vol = sum(volumes[-5:]) / 5
        prev_30_vol = sum(volumes[-35:-5]) / 30 if len(volumes) >= 35 else 0
        if prev_30_vol > 0 and recent_5_vol < prev_30_vol * 0.9:
            macd_signal = ('🚨 股价新高 + 量能萎缩 / 量价背离', 'P0')
    
    # 5. 跌破均线
    ma5 = calc_ma(closes, 5)
    ma10 = calc_ma(closes, 10)
    ma20 = calc_ma(closes, 20)
    
    ma_signals = []
    if current < ma5 and current > ma10:
        ma_signals.append(('🟡 跌破 5 日线', 'P2'))
    if current < ma10:
        ma_signals.append(('⚠️ 跌破 10 日线', 'P1'))
    if current < ma20:
        ma_signals.append(('🚨 跌破 20 日线 / 趋势 破位', 'P0'))
    
    # 综合 决策
    p0_count = sum(1 for sigs in [lock_signals, [rsi_signal] if rsi_signal else [],
                                   [volume_signal] if volume_signal else [],
                                   [macd_signal] if macd_signal else [],
                                   ma_signals]
                   for sig in sigs if sig and sig[1] == 'P0')
    p1_count = sum(1 for sigs in [lock_signals, [rsi_signal] if rsi_signal else [],
                                   [volume_signal] if volume_signal else [],
                                   [macd_signal] if macd_signal else [],
                                   ma_signals]
                   for sig in sigs if sig and sig[1] == 'P1')
    
    if p0_count >= 2:
        decision = '🚨🚨 强烈 减仓 (P0 信号 ≥ 2)'
    elif p0_count == 1:
        decision = '🚨 减仓 1/3 (1 个 P0 信号)'
    elif p1_count >= 2:
        decision = '⚠️ 警惕 / 设 止损 (2+ P1 信号)'
    elif p1_count == 1:
        decision = '🟡 观察 / 准备 减仓'
    else:
        decision = '✅ 持有 / 无 明显 卖出信号'
    
    return {
        'name': holding['name'],
        'current': current,
        'cost': cost,
        'profit_pct': profit_pct,
        'rsi': rsi,
        'ma5': ma5, 'ma10': ma10, 'ma20': ma20,
        'lock_signals': lock_signals,
        'rsi_signal': rsi_signal,
        'volume_signal': volume_signal,
        'macd_signal': macd_signal,
        'ma_signals': ma_signals,
        'p0_count': p0_count,
        'p1_count': p1_count,
        'decision': decision,
    }


def format_report(code: str, result: dict) -> str:
    if 'error' in result:
        return f"❌ {code}: {result['error']}"
    
    r = result
    report = f"""
╔══════════════════════════════════════════════════════════╗
║  🚨 卖出 信号 分析 - {r['name']} ({code})
╚══════════════════════════════════════════════════════════╝

📊 持仓 状态:
  • 现价: ¥{r['current']:.2f}
  • 成本: ¥{r['cost']:.2f}
  • 浮盈: {r['profit_pct']:+.1f}%

📈 关键 指标:
  • RSI(14): {r['rsi']:.1f}
  • MA5:  ¥{r['ma5']:.2f}
  • MA10: ¥{r['ma10']:.2f}
  • MA20: ¥{r['ma20']:.2f}

🚨 5 大 卖出 信号:

  [信号 1] 三段锁利:
"""
    if r['lock_signals']:
        for sig, pri in r['lock_signals']:
            report += f"    {sig} [{pri}]\n"
    else:
        report += "    ✅ 浮盈 <20% / 无 锁利 触发\n"
    
    report += "\n  [信号 2] RSI 超买:\n"
    if r['rsi_signal']:
        sig, pri = r['rsi_signal']
        report += f"    {sig} [{pri}]\n"
    else:
        report += "    ✅ RSI 正常\n"
    
    report += "\n  [信号 3] 量价 异常:\n"
    if r['volume_signal']:
        sig, pri = r['volume_signal']
        report += f"    {sig} [{pri}]\n"
    else:
        report += "    ✅ 量价 配合\n"
    
    report += "\n  [信号 4] 顶背离 / 量价 背离:\n"
    if r['macd_signal']:
        sig, pri = r['macd_signal']
        report += f"    {sig} [{pri}]\n"
    else:
        report += "    ✅ 无 顶背离\n"
    
    report += "\n  [信号 5] 关键均线:\n"
    if r['ma_signals']:
        for sig, pri in r['ma_signals']:
            report += f"    {sig} [{pri}]\n"
    else:
        report += "    ✅ 站上 所有 均线\n"
    
    report += f"\n📊 综合 信号:\n"
    report += f"  • P0 (关键): {r['p0_count']} 个\n"
    report += f"  • P1 (重要): {r['p1_count']} 个\n"
    
    report += f"\n💎 决策: {r['decision']}\n"
    
    return report


def main():
    parser = argparse.ArgumentParser(description='卖出 信号 v1.0')
    parser.add_argument('--code', help='单股 代码')
    args = parser.parse_args()
    
    print(f"🚨 卖出 信号 综合 分析 v1.0  /  {datetime.now():%Y-%m-%d %H:%M}\n")
    
    if args.code:
        if args.code not in HOLDINGS:
            print(f"❌ 未配置 {args.code}")
            sys.exit(1)
        result = analyze_sell_signals(args.code, HOLDINGS[args.code])
        print(format_report(args.code, result))
    else:
        # 全持仓
        results = {}
        for code, holding in HOLDINGS.items():
            result = analyze_sell_signals(code, holding)
            results[code] = result
            print(format_report(code, result))
        
        # 汇总
        print("\n" + "=" * 60)
        print("📊 全持仓 卖出信号 总结")
        print("=" * 60)
        print(f"{'股票':<10s} {'现价':>8s} {'浮盈':>8s} {'RSI':>5s} {'P0':>4s} {'P1':>4s} 决策")
        print("-" * 70)
        for code, r in results.items():
            if 'error' in r:
                print(f"  {code}: {r['error']}")
                continue
            short_decision = r['decision'].split(' ')[0] + ' ' + r['decision'].split(' ')[1] if ' ' in r['decision'] else r['decision']
            print(f"  {r['name']:<8s} ¥{r['current']:>5.2f} {r['profit_pct']:>+6.1f}% {r['rsi']:>4.0f}  {r['p0_count']:>3d} {r['p1_count']:>3d}  {short_decision}")


if __name__ == '__main__':
    main()
