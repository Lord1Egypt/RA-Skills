#!/usr/bin/env python3
"""
交易执行模块
支持市价单和限价单
"""
import sys
import os
import json
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import FEE_RATE, STAMP_TAX_SELL, SLIPPAGE, TRADES_FILE, DATA_DIR
from account import Account
from positions import Positions
from quote import get_quote_tencent as get_quote


def calculate_fee(price, quantity, is_sell=False):
    """计算手续费"""
    amount = price * quantity
    fee = amount * FEE_RATE
    stamp_tax = amount * STAMP_TAX_SELL if is_sell else 0
    return fee, stamp_tax


def trade(direction, code, quantity, price=None, order_type='market'):
    """
    执行交易
    """
    account = Account()
    positions = Positions()
    
    name = code
    current_price = price
    
    # 如果是市价单，获取当前市场价格
    if order_type == 'market':
        quote = get_quote(code)
        if quote:
            name = quote['name']
            current_price = quote['price']
            print(f"📊 当前价格：¥{current_price} ({quote.get('change_pct', 0):+.2f}%)")
        else:
            print(f"❌ 无法获取 {code} 的行情价格，请使用限价单（--price）")
            return False
    
    if current_price is None or current_price <= 0:
        print(f"❌ 缺少有效价格信息")
        return False
    
    # 添加滑点
    exec_price = current_price + SLIPPAGE if direction == 'buy' else current_price - SLIPPAGE
    
    quantity = int(quantity)
    
    if direction == 'buy':
        amount = exec_price * quantity
        fee, stamp_tax = calculate_fee(exec_price, quantity, False)
        total_cost = amount + fee
        
        if account.get_available_cash() < total_cost:
            print(f"❌ 资金不足：需要 ¥{total_cost:,.2f}，可用 ¥{account.get_available_cash():,.2f}")
            return False
        
        account.deduct(total_cost)
        positions.buy(code, name, exec_price, quantity)
        account.add_fee(fee)
        record_trade(code, name, 'buy', exec_price, quantity, fee, 0)
        
        print(f"✅ 买入成功")
        print(f"   股票：{name} ({code})")
        print(f"   价格：¥{exec_price:.2f}")
        print(f"   数量：{quantity}")
        print(f"   手续费：¥{fee:.2f}")
        print(f"   总成本：¥{total_cost:.2f}")
        
    elif direction == 'sell':
        pos = positions.get_position(code)
        if not pos or pos['quantity'] < quantity:
            print(f"❌ 持仓不足：需要 {quantity} 股，当前持有 {pos['quantity'] if pos else 0} 股")
            return False
        
        amount = exec_price * quantity
        fee, stamp_tax = calculate_fee(exec_price, quantity, True)
        total_income = amount - fee - stamp_tax
        
        positions.sell(code, quantity)
        account.add(total_income)
        account.add_fee(fee)
        account.add_stamp_tax(stamp_tax)
        record_trade(code, name, 'sell', exec_price, quantity, fee, stamp_tax)
        
        profit = (exec_price - pos['avg_cost']) * quantity
        profit_pct = (exec_price / pos['avg_cost'] - 1) * 100 if pos['avg_cost'] > 0 else 0
        
        print(f"✅ 卖出成功")
        print(f"   股票：{name} ({code})")
        print(f"   价格：¥{exec_price:.2f}")
        print(f"   数量：{quantity}")
        print(f"   手续费：¥{fee:.2f}")
        print(f"   印花税：¥{stamp_tax:.2f}")
        print(f"   净收入：¥{total_income:.2f}")
        print(f"   盈亏：¥{profit:.2f} ({profit_pct:+.2f}%)")
    
    return True


def record_trade(code, name, direction, price, quantity, fee, stamp_tax):
    """记录交易"""
    os.makedirs(DATA_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    amount = price * quantity
    total_cost = amount + fee + stamp_tax
    line = f"{timestamp}|{code}|{name}|{direction}|{price}|{quantity}|{fee:.2f}|{stamp_tax:.2f}|{total_cost:.2f}\n"
    with open(TRADES_FILE, 'a', encoding='utf-8') as f:
        f.write(line)


def main():
    if len(sys.argv) < 4:
        print("用法：")
        print("  python3 trade.py buy <股票代码> <数量> [--price <价格>]")
        print("  python3 trade.py sell <股票代码> <数量> [--price <价格>]")
        print("")
        print("示例：")
        print("  python3 trade.py buy 600900 100           # 市价买入")
        print("  python3 trade.py buy 600900 100 --price 27.00  # 限价买入")
        print("  python3 trade.py sell 600900 50           # 市价卖出")
        sys.exit(1)
    
    direction = sys.argv[1].lower()
    code = sys.argv[2]
    quantity = int(sys.argv[3])
    
    price = None
    if '--price' in sys.argv:
        idx = sys.argv.index('--price')
        if idx + 1 < len(sys.argv):
            price = float(sys.argv[idx + 1])
    
    order_type = 'limit' if price else 'market'
    
    if direction not in ['buy', 'sell']:
        print("❌ 方向错误，请使用 'buy' 或 'sell'")
        sys.exit(1)
    
    trade(direction, code, quantity, price, order_type)


if __name__ == "__main__":
    main()
