#!/usr/bin/env python3
"""
😅 卖飞 / 错过 自动复盘 v1.0

核心:
  自动 识别 用户:
    • 卖出 后 股票 还涨 (卖飞)
    • 加仓 后 股票 大跌 (高位接刀)
    • 错过 突破前高 信号 (没买)
  
自动 复盘 + 沉淀 教训

用法:
  python3 missed_opportunity.py             # 全持仓 + 历史扫描
  python3 missed_opportunity.py --days 30   # 近 30 天
"""

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timedelta


# 你的 卖出/加仓 历史 (示例 / 实际应该从交易记录读)
TRADING_HISTORY = [
    {'date': '2026-06-25', 'action': 'SELL', 'code': '688498', 'name': '源杰科技', 'qty': 290, 'price': 1861.90, 'note': '主仓减仓后底仓全清'},
    {'date': '2026-05-29', 'action': 'SELL', 'code': '600522', 'name': '中天科技', 'qty': 1300, 'price': 30.50, 'note': '卖中天买通富 (失败案例)'},
    {'date': '2026-06-25', 'action': 'BUY', 'code': '688234', 'name': '天岳先进', 'qty': 2024, 'price': 182.35, 'note': '突破前高接回'},
]


def fetch_kline(code, end_date_str=None, days_after=30):
    """拿 K 线"""
    if code.startswith(('0','3')): sym = 'sz' + code
    else: sym = 'sh' + code
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={sym},day,,,200,qfq"
    req = urllib.request.Request(url, headers={'Referer': 'https://gu.qq.com/'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            text = r.read().decode('utf-8', errors='ignore')
        text = re.sub(r'^[\s\S]*?=\s*', '', text).rstrip(';)')
        inner = json.loads(text).get('data', {}).get(sym, {})
        for k in ['qfqday','day']:
            if k in inner and inner[k]:
                return [{'date': r[0], 'close': float(r[2]), 'high': float(r[3]), 'low': float(r[4])} for r in inner[k]]
    except: pass
    return []


def analyze_sell(trade):
    """卖出 后 是否 卖飞?"""
    klines = fetch_kline(trade['code'])
    if not klines: return None
    
    sell_date = trade['date']
    sell_price = trade['price']
    
    # 找 卖出日 之后 N 天 最高价
    after_sell = [k for k in klines if k['date'] > sell_date]
    if not after_sell:
        return {'status': 'too_recent', 'msg': '太近 / 数据 不足'}
    
    # 30 天 内 最高
    after_30 = after_sell[:30]
    max_high_after = max(k['high'] for k in after_30)
    
    # 卖飞 比例
    flying_pct = (max_high_after - sell_price) / sell_price * 100
    miss_value = (max_high_after - sell_price) * trade['qty']
    
    if flying_pct > 30:
        verdict = '🚀 严重卖飞 (>30%)'
    elif flying_pct > 10:
        verdict = '⚠️ 卖飞 (10-30%)'
    elif flying_pct > 5:
        verdict = '🟡 略卖飞 (5-10%)'
    elif flying_pct > 0:
        verdict = '✅ 接近 顶部 卖 (小卖飞 <5%)'
    else:
        verdict = '🌟 完美卖出 (后续 没涨)'
    
    return {
        'sell_date': sell_date,
        'sell_price': sell_price,
        'max_after': max_high_after,
        'flying_pct': flying_pct,
        'miss_value': miss_value,
        'verdict': verdict,
        'qty': trade['qty'],
    }


def analyze_buy(trade):
    """买入 后 是否 高位接刀?"""
    klines = fetch_kline(trade['code'])
    if not klines: return None
    
    buy_date = trade['date']
    buy_price = trade['price']
    
    after_buy = [k for k in klines if k['date'] > buy_date]
    if not after_buy:
        return {'status': 'too_recent'}
    
    after_30 = after_buy[:30]
    if not after_30:
        return {'status': 'too_recent'}
    
    min_low_after = min(k['low'] for k in after_30)
    drop_pct = (min_low_after - buy_price) / buy_price * 100
    drawdown_value = (min_low_after - buy_price) * trade['qty']
    
    if drop_pct < -20:
        verdict = '🚨 严重高位接刀 (<-20%)'
    elif drop_pct < -10:
        verdict = '⚠️ 高位接刀 (10-20%)'
    elif drop_pct < -5:
        verdict = '🟡 短期 回调 (5-10%)'
    elif drop_pct < 0:
        verdict = '🟢 接近 底部 买'
    else:
        verdict = '🌟 完美买入 (一路涨)'
    
    return {
        'buy_date': buy_date,
        'buy_price': buy_price,
        'min_after': min_low_after,
        'drop_pct': drop_pct,
        'drawdown_value': drawdown_value,
        'verdict': verdict,
        'qty': trade['qty'],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=60, help='扫描 历史 天数')
    args = parser.parse_args()
    
    print(f"😅 卖飞 / 错过 自动复盘 v1.0  /  {datetime.now():%Y-%m-%d %H:%M}")
    print()
    
    cutoff = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
    recent_trades = [t for t in TRADING_HISTORY if t['date'] >= cutoff]
    
    print(f"📋 扫描 近 {args.days} 天 / 共 {len(recent_trades)} 笔交易\n")
    
    total_miss = 0
    total_drawdown = 0
    
    for t in recent_trades:
        print("=" * 65)
        print(f"📌 {t['date']} {t['action']} {t['name']} ({t['code']})")
        print(f"   {t['qty']} 股 @¥{t['price']}")
        print(f"   备注: {t['note']}")
        print()
        
        if t['action'] == 'SELL':
            result = analyze_sell(t)
            if result and 'status' not in result:
                print(f"  📊 卖出 后 30 天 最高: ¥{result['max_after']:.2f}")
                print(f"  📈 卖飞 幅度: {result['flying_pct']:+.2f}%")
                print(f"  💸 错失收益: ¥{result['miss_value']:+,.0f}")
                print(f"  🎯 判定: {result['verdict']}")
                if result['flying_pct'] > 0:
                    total_miss += result['miss_value']
        elif t['action'] == 'BUY':
            result = analyze_buy(t)
            if result and 'status' not in result:
                print(f"  📊 买入 后 30 天 最低: ¥{result['min_after']:.2f}")
                print(f"  📉 最大 回撤: {result['drop_pct']:+.2f}%")
                print(f"  💸 最大 浮亏: ¥{result['drawdown_value']:+,.0f}")
                print(f"  🎯 判定: {result['verdict']}")
                if result['drop_pct'] < 0:
                    total_drawdown += result['drawdown_value']
        
        print()
    
    # 总结
    print("=" * 65)
    print("📊 综合 复盘 总结")
    print("=" * 65)
    print(f"\n  💸 总卖飞 错失收益: ¥{total_miss:+,.0f}")
    print(f"  💸 总买入 最大回撤: ¥{total_drawdown:+,.0f}")
    
    # 沉淀 教训
    print()
    print("💎 沉淀 教训:")
    if total_miss > 50000:
        print("  ❌ 卖飞 严重 (>¥5 万) - 复习: Winners 应 留底仓 / Let it run")
    if total_drawdown < -50000:
        print("  ❌ 高位接刀 严重 - 复习: 等回踩 + 三天站稳 + 不追突破日")
    
    print("\n  🌟 经验 (用于 未来 优化):")
    print("  ✅ 减仓 锁利 必须 留 10-20% 底仓 (源杰 教科书)")
    print("  ✅ 高位 接刀 必须 设 -7% 止损 + 不 满仓")
    print("  ✅ 突破日 不追 / 等 缩量回踩 (你框架)")


if __name__ == '__main__':
    main()
