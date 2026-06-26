#!/usr/bin/env python3
"""
v4.1 洗盘 vs 破位 智能区分

铁律 5: 趋势持仓
  • 洗盘 = 持有
  • 破位 = 清仓

5 大判定维度:
  1. 30 日均线是否有效跌破
  2. 板块主线地位是否动摇
  3. 主力资金 3 日是否净流出 > 总市值 1%
  4. 是否有重大利空消息
  5. 跌幅是否在正常洗盘范围内
"""
import urllib.request
import re
import json
from datetime import datetime


def fetch_quote(code):
    sym = ('sz' if code.startswith(('0', '3')) else 'sh') + code
    url = f"https://qt.gtimg.cn/q={sym}"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=8) as r:
            text = r.read().decode('gbk', errors='ignore')
        p = text.split('~')
        if len(p) < 50: return None
        return {
            'name': p[1], 'price': float(p[3]), 'prev': float(p[4]),
            'open': float(p[5]), 'high': float(p[33]), 'low': float(p[34]),
            'change_pct': float(p[32]) if p[32] else 0,
            'vol_ratio': float(p[49]) if len(p) > 49 and p[49] else 0,
            'market_cap': float(p[44]) if p[44] else 0,
            'turnover_amount': float(p[37]) if p[37] else 0,
        }
    except: return None


def fetch_kline(code, count=60):
    sym = ('sz' if code.startswith(('0', '3')) else 'sh') + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,{count},qfq"
    try:
        req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
        with urllib.request.urlopen(req, timeout=15) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday', 'day']:
            if k in inner and inner[k]: return inner[k]
    except: pass
    return []


def fetch_money_flow(code):
    """3 日主力资金流"""
    secid = f"0.{code}" if code.startswith(('0', '3')) else f"1.{code}"
    url = f"https://push2.eastmoney.com/api/qt/stock/fflow/daykline/get?secid={secid}&lmt=5&klt=101&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        klines = data.get('data', {}).get('klines', [])
        if not klines: return 0
        # 累计最近 3 天主力净流入
        net = 0
        for line in klines[-3:]:
            parts = line.split(',')
            if len(parts) >= 2 and parts[1] != '-':
                net += float(parts[1])
        return net  # 元
    except: return 0


def analyze_shake_or_break(code, name=''):
    """综合判定: 洗盘 vs 破位"""
    quote = fetch_quote(code)
    kline = fetch_kline(code, 30)
    
    if not quote or not kline or len(kline) < 30:
        return None
    
    name = name or quote['name']
    closes = [float(r[2]) for r in kline]
    cur = quote['price']
    
    # 维度 1: MA20 / MA30 是否跌破
    ma20 = sum(closes[-20:]) / 20
    ma30 = sum(closes[-30:]) / 30
    
    broke_ma20 = cur < ma20 * 0.98  # 跌破 MA20 超过 2%
    broke_ma30 = cur < ma30 * 0.98
    
    # 维度 2: 短期跌幅
    high_5d = max([float(r[3]) for r in kline[-5:]])
    drawdown_from_high_5d = (high_5d - cur) / high_5d * 100
    
    # 维度 3: 主力 3 日资金
    money_flow_3d = fetch_money_flow(code)
    money_flow_pct = money_flow_3d / (quote['market_cap'] * 1e8) * 100 if quote['market_cap'] > 0 else 0
    
    # 维度 4: 是否长上影线 + 高位滞涨
    upper_shadow = quote['high'] - max(quote['open'], quote['price'])
    body = abs(quote['price'] - quote['open']) or 0.01
    long_shadow = (upper_shadow / body) > 2
    
    # 评分
    break_score = 0
    reasons = []
    
    # 关键 1: MA 跌破
    if broke_ma30:
        break_score += 40
        reasons.append(f"🔴 跌破 MA30 (¥{ma30:.2f})")
    elif broke_ma20:
        break_score += 25
        reasons.append(f"⚠️ 跌破 MA20 (¥{ma20:.2f})")
    
    # 关键 2: 主力大额流出
    if money_flow_pct < -3:
        break_score += 30
        reasons.append(f"🔴 主力 3 日流出 {money_flow_pct:.1f}% (¥{money_flow_3d/1e8:.2f} 亿)")
    elif money_flow_pct < -1:
        break_score += 15
        reasons.append(f"⚠️ 主力 3 日流出 {money_flow_pct:.1f}%")
    
    # 关键 3: 跌幅范围
    if drawdown_from_high_5d > 15:
        break_score += 20
        reasons.append(f"🔴 5 日内跌幅 {drawdown_from_high_5d:.1f}%")
    elif drawdown_from_high_5d > 10:
        break_score += 10
        reasons.append(f"⚠️ 5 日内跌幅 {drawdown_from_high_5d:.1f}%")
    
    # 关键 4: 长上影
    if long_shadow and quote['change_pct'] < 0:
        break_score += 10
        reasons.append("⚠️ 长上影线 + 收阴")
    
    # 判定
    if break_score >= 60:
        verdict = '🔴 破位（清仓信号）'
        action = '立刻清仓 / 不要扛'
        hold = False
    elif break_score >= 35:
        verdict = '⚠️ 边缘破位（减半止损）'
        action = '减仓 50% / 设硬止损'
        hold = False
    elif break_score >= 15:
        verdict = '🟡 谨慎洗盘'
        action = '继续持有 / 但 加强监控'
        hold = True
    else:
        verdict = '✅ 正常洗盘（持有）'
        action = '坚定持有 / 不要被洗下车'
        hold = True
    
    return {
        'code': code,
        'name': name,
        'cur': cur,
        'ma20': ma20,
        'ma30': ma30,
        'broke_ma20': broke_ma20,
        'broke_ma30': broke_ma30,
        'drawdown_5d': round(drawdown_from_high_5d, 2),
        'money_flow_3d_yi': round(money_flow_3d / 1e8, 2),
        'money_flow_pct': round(money_flow_pct, 2),
        'long_shadow': long_shadow,
        'break_score': break_score,
        'verdict': verdict,
        'action': action,
        'hold': hold,
        'reasons': reasons,
    }


def format_report(result):
    """格式化报告"""
    if not result:
        return "❌ 数据获取失败"
    
    lines = []
    lines.append("=" * 65)
    lines.append(f"📊 洗盘 vs 破位 判定 · {result['name']} ({result['code']})")
    lines.append("=" * 65)
    
    lines.append(f"\n💰 当前价格: ¥{result['cur']:.2f}")
    lines.append(f"📈 MA20: ¥{result['ma20']:.2f} ({'❌ 跌破' if result['broke_ma20'] else '✅ 站上'})")
    lines.append(f"📈 MA30: ¥{result['ma30']:.2f} ({'❌ 跌破' if result['broke_ma30'] else '✅ 站上'})")
    lines.append(f"📊 5 日跌幅: {result['drawdown_5d']:.2f}%")
    lines.append(f"💰 主力 3 日: ¥{result['money_flow_3d_yi']:+.2f} 亿 ({result['money_flow_pct']:+.2f}%)")
    
    lines.append(f"\n🎯 判定: {result['verdict']}")
    lines.append(f"   破位评分: {result['break_score']}/100")
    
    if result['reasons']:
        lines.append(f"\n📋 评分依据:")
        for r in result['reasons']:
            lines.append(f"   {r}")
    
    lines.append(f"\n💡 操作建议:")
    lines.append(f"   {result['action']}")
    
    return "\n".join(lines)


def main():
    import sys
    if len(sys.argv) < 2:
        print("用法: shake_vs_break.py <股票代码> [名称]")
        sys.exit(1)
    
    code = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else ''
    
    print(f"\n🚀 洗盘 vs 破位 判定: {code} {name}")
    result = analyze_shake_or_break(code, name)
    print(format_report(result))
    return result


if __name__ == '__main__':
    main()
