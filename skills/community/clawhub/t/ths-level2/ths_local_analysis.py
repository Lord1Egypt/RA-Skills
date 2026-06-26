# -*- coding: utf-8 -*-
"""
同花顺Level2 - 本地数据分析（无需Tushare Token）
基于已有持仓数据进行分析
"""
import os
import sys
import json
import io
from datetime import datetime
from pathlib import Path

# 设置UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 持仓数据（来自用户截图）
HOLDINGS = {
    "600276": {"name": "恒瑞医药", "cost": 53.12, "shares": 1000, "market": "SH", "current": 51.63, "change": -2.80},
    "600760": {"name": "中航沈飞", "cost": 48.01, "shares": 1200, "market": "SH", "current": 47.76, "change": -0.53},
    "600999": {"name": "招商证券", "cost": 19.50, "shares": 1600, "market": "SH", "current": 15.17, "change": -22.20},
    "601888": {"name": "中国中免", "cost": 72.27, "shares": 1000, "market": "SH", "current": 70.69, "change": -2.19},
    "002202": {"name": "金风科技", "cost": 28.01, "shares": 2000, "market": "SZ", "current": 28.13, "change": 0.44},
    "300188": {"name": "国投智能", "cost": -1917, "shares": 320, "market": "SZ", "current": 12.33, "change": 0},
}

def analyze_position(code, info):
    """分析持仓"""
    name = info['name']
    cost = info['cost']
    current = info['current']
    shares = info['shares']
    change = info['change']
    
    # 计算盈亏
    if cost < 0:  # 利润仓
        profit = abs(cost)
        profit_pct = 617389
        market_value = current * shares
        status = "利润仓"
    else:
        market_value = current * shares
        cost_value = cost * shares
        profit = market_value - cost_value
        profit_pct = (profit / cost_value) * 100
        status = "持仓中"
    
    # 技术分析信号
    signals = []
    if change > 2:
        signals.append("强势上涨")
    elif change > 0:
        signals.append("温和上涨")
    elif change > -2:
        signals.append("小幅回调")
    else:
        signals.append("深度回调")
    
    if cost > 0 and current < cost * 0.9:
        signals.append("跌破成本10%")
    
    # 策略建议
    if cost > 0:
        if profit_pct < -20:
            suggestion = "考虑止损或补仓"
        elif profit_pct < -10:
            suggestion = "观察反弹"
        elif profit_pct > 10:
            suggestion = "可持有"
        else:
            suggestion = "观望"
    else:
        suggestion = "利润保护"
    
    return {
        'code': code,
        'name': name,
        'current': current,
        'cost': cost,
        'shares': shares,
        'market_value': market_value,
        'profit': profit,
        'profit_pct': profit_pct,
        'day_change': change,
        'signals': signals,
        'suggestion': suggestion,
        'status': status
    }

def main():
    print("=" * 70)
    print(" 同花顺Level2 - 持仓股票分析")
    print(f" 时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 70)
    print()
    
    results = []
    total_market = 0
    total_cost = 0
    
    for code, info in HOLDINGS.items():
        result = analyze_position(code, info)
        results.append(result)
        total_market += result['market_value']
        if result['cost'] > 0:
            total_cost += result['cost'] * result['shares']
        
        # 打印分析结果
        emoji = "🟢" if result['day_change'] > 0 else "🔴" if result['day_change'] < 0 else "⚪"
        print(f"{emoji} {result['name']} ({code}.{info['market']})")
        print(f"   现价: ¥{result['current']:.2f} | 成本: ¥{result['cost']:.2f}" if result['cost'] > 0 else f"   现价: ¥{result['current']:.2f} | 成本: ¥{result['cost']:.2f} (利润仓)")
        print(f"   持仓: {result['shares']}股 | 市值: ¥{result['market_value']/10000:.2f}万")
        print(f"   盈亏: ¥{result['profit']:.2f} ({result['profit_pct']:+.2f}%)" if result['cost'] > 0 else f"   盈亏: 已实现巨额盈利")
        print(f"   今日: {result['day_change']:+.2f}%")
        print(f"   信号: {', '.join(result['signals'])}")
        print(f"   建议: {result['suggestion']}")
        print()
    
    # 汇总
    print("=" * 70)
    print(" 持仓汇总")
    print("=" * 70)
    print(f"总市值: ¥{total_market/10000:.2f}万")
    if total_cost > 0:
        total_profit = total_market - total_cost
        total_profit_pct = (total_profit / total_cost) * 100
        print(f"总成本: ¥{total_cost/10000:.2f}万")
        print(f"总盈亏: ¥{total_profit/10000:.2f}万 ({total_profit_pct:+.2f}%)")
    print()
    
    # 排序输出
    print("=" * 70)
    print(" 按盈亏排序")
    print("=" * 70)
    print(f"{'股票':<10}{'现价':>8}{'盈亏%':>10}{'市值(万)':>10}{'建议':>12}")
    print("-" * 70)
    for r in sorted(results, key=lambda x: x['profit_pct'], reverse=True):
        print(f"{r['name']:<10}{r['current']:>8.2f}{r['profit_pct']:>+9.1f}%{r['market_value']/10000:>10.2f}{r['suggestion']:>12}")
    
    # 保存结果
    output_file = Path(__file__).parent / 'ths_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n✓ 已保存: {output_file}")

if __name__ == '__main__':
    main()
