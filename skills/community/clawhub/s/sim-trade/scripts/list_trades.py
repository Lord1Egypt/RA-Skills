#!/usr/bin/env python3
"""
显示交易记录
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import TRADES_FILE


def list_trades():
    """显示交易记录"""
    if not os.path.exists(TRADES_FILE):
        print("=" * 60)
        print("📜 暂无交易记录")
        print("=" * 60)
        return
    
    with open(TRADES_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        print("=" * 60)
        print("📜 暂无交易记录")
        print("=" * 60)
        return
    
    # 按时间倒序排列
    lines.reverse()
    
    print("=" * 80)
    print("📜 交易记录")
    print("=" * 80)
    print(f"{'时间':<20} {'代码':<8} {'名称':<10} {'方向':<4} {'价格':>8} {'数量':>6} {'手续费':>8} {'印花税':>8} {'总额':>12}")
    print("-" * 80)
    
    for line in lines:
        parts = line.strip().split('|')
        if len(parts) >= 9:
            timestamp = parts[0]
            code = parts[1]
            name = parts[2][:8]
            direction = parts[3]
            price = float(parts[4])
            quantity = int(parts[5])
            fee = float(parts[6])
            stamp_tax = float(parts[7])
            total = float(parts[8])
            
            direction_icon = "📈" if direction == "buy" else "📉"
            direction_text = "买入" if direction == "buy" else "卖出"
            
            print(f"{timestamp:<20} {code:<8} {name:<10} {direction_icon}{direction_text:<2} {price:>8.2f} {quantity:>6} {fee:>8.2f} {stamp_tax:>8.2f} {total:>12.2f}")
    
    print("-" * 80)
    print(f"共计 {len(lines)} 笔交易")
    print("=" * 80)


if __name__ == "__main__":
    list_trades()
