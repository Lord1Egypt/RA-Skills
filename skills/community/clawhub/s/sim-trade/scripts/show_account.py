#!/usr/bin/env python3
"""
显示账户信息
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import ACCOUNT_FILE, POSITIONS_FILE
from account import Account
from positions import Positions
from quote import get_quote_tencent as get_quote


def show_account():
    """显示账户信息"""
    account = Account()
    positions = Positions()
    
    # 获取所有持仓的当前价格
    prices = {}
    for code in positions.get_all_positions():
        quote = get_quote(code)
        if quote:
            prices[code] = quote['price']
    
    # 计算市值和盈亏
    market_value = positions.get_total_market_value(prices)
    profit = positions.get_total_profit(prices)
    total_assets = account.get_total_assets(market_value)
    
    # 计算收益率
    profit_pct = (profit / account.initial_capital) * 100 if account.initial_capital > 0 else 0
    
    print("=" * 60)
    print("💰 模拟交易账户")
    print("=" * 60)
    print(f"💵 初始资金：  ¥{account.initial_capital:>12,.2f}")
    print(f"💳 可用资金：  ¥{account.cash:>12,.2f}")
    print(f"📦 持仓市值：  ¥{market_value:>12,.2f}")
    print(f"📈 浮动盈亏：  ¥{profit:>12,.2f} ({profit_pct:+.2f}%)")
    print(f"🏆 总资产：    ¥{total_assets:>12,.2f}")
    print("-" * 60)
    print(f"💸 累计手续费：¥{account.total_fee:>12,.2f}")
    print(f"📜 累计印花税：¥{account.total_stamp_tax:>12,.2f}")
    print(f"📊 总交易成本：¥{account.get_total_cost():>12,.2f}")
    print("=" * 60)
    
    # 如果有持仓，显示持仓详情
    if positions.get_all_positions():
        print("\n📋 持仓明细：")
        print("-" * 60)
        print(f"{'代码':<8} {'名称':<10} {'数量':>6} {'成本价':>8} {'当前价':>8} {'市值':>10} {'盈亏':>10}")
        print("-" * 60)
        
        for code, pos in positions.get_all_positions().items():
            name = pos['name'][:8]
            quantity = pos['quantity']
            avg_cost = pos['avg_cost']
            current_price = prices.get(code, avg_cost)
            pos_market = quantity * current_price
            pos_profit = (current_price - avg_cost) * quantity
            pos_profit_pct = (current_price / avg_cost - 1) * 100 if avg_cost > 0 else 0
            
            print(f"{code:<8} {name:<10} {quantity:>6} {avg_cost:>8.2f} {current_price:>8.2f} {pos_market:>10.2f} {pos_profit:>+9.2f} ({pos_profit_pct:+.2f}%)")
        
        print("-" * 60)


if __name__ == "__main__":
    show_account()
