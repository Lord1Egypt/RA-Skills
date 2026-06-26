#!/usr/bin/env python3
"""
显示持仓信息
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from positions import Positions
from quote import get_quote_tencent as get_quote


def show_positions():
    """显示所有持仓"""
    positions = Positions()
    
    # 获取所有持仓的当前价格
    prices = {}
    for code in positions.get_all_positions():
        quote = get_quote(code)
        if quote:
            prices[code] = quote
    
    all_positions = positions.get_all_positions()
    
    if not all_positions:
        print("=" * 60)
        print("📭 当前无持仓")
        print("=" * 60)
        return
    
    # 计算汇总
    total_market = 0.0
    total_profit = 0.0
    
    print("=" * 70)
    print("💼 模拟交易持仓")
    print("=" * 70)
    print(f"{'代码':<8} {'名称':<10} {'数量':>6} {'成本价':>8} {'当前价':>8} {'浮动盈亏':>12} {'盈亏%':>8}")
    print("-" * 70)
    
    for code, pos in all_positions.items():
        name = pos['name'][:8]
        quantity = pos['quantity']
        avg_cost = pos['avg_cost']
        
        quote = prices.get(code)
        if quote:
            current_price = quote['price']
            change = quote.get('change', 0)
        else:
            current_price = avg_cost
            change = 0
        
        market_value = quantity * current_price
        profit = (current_price - avg_cost) * quantity
        profit_pct = (current_price / avg_cost - 1) * 100 if avg_cost > 0 else 0
        
        total_market += market_value
        total_profit += profit
        
        print(f"{code:<8} {name:<10} {quantity:>6} {avg_cost:>8.2f} {current_price:>8.2f} {profit:>+12.2f} {profit_pct:>+7.2f}%")
    
    print("-" * 70)
    print(f"📊 总市值：      ¥{total_market:,.2f}")
    print(f"📈 总浮动盈亏： ¥{total_profit:,+.2f}")
    
    if total_market > 0:
        total_profit_pct = (total_profit / (total_market - total_profit)) * 100
        print(f"📈 盈亏比例：   {total_profit_pct:+.2f}%")
    print("=" * 70)


if __name__ == "__main__":
    show_positions()
