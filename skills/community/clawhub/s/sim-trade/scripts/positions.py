#!/usr/bin/env python3
"""
持仓管理模块
"""
import json
import os
from config import POSITIONS_FILE


class Positions:
    def __init__(self):
        self.positions = {}
        self.load()
    
    def load(self):
        """加载持仓数据"""
        if os.path.exists(POSITIONS_FILE):
            with open(POSITIONS_FILE, 'r', encoding='utf-8') as f:
                self.positions = json.load(f)
    
    def save(self):
        """保存持仓数据"""
        with open(POSITIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.positions, f, ensure_ascii=False, indent=2)
    
    def buy(self, code, name, price, quantity):
        """买入持仓"""
        if code not in self.positions:
            self.positions[code] = {
                'name': name,
                'quantity': 0,
                'avg_cost': 0.0,
                'total_cost': 0.0
            }
        
        pos = self.positions[code]
        old_quantity = pos['quantity']
        old_total_cost = pos['total_cost']
        
        # 计算新的平均成本
        new_quantity = old_quantity + quantity
        new_total_cost = old_total_cost + (price * quantity)
        new_avg_cost = new_total_cost / new_quantity if new_quantity > 0 else 0.0
        
        pos['quantity'] = new_quantity
        pos['avg_cost'] = new_avg_cost
        pos['total_cost'] = new_total_cost
        
        self.save()
        return pos
    
    def sell(self, code, quantity):
        """卖出持仓"""
        if code not in self.positions:
            return None
        
        pos = self.positions[code]
        if pos['quantity'] < quantity:
            return None
        
        # 计算卖出后的成本
        sold_cost = pos['avg_cost'] * quantity
        pos['quantity'] -= quantity
        pos['total_cost'] = pos['avg_cost'] * pos['quantity']
        
        # 如果持仓为0，删除记录
        if pos['quantity'] == 0:
            del self.positions[code]
        
        self.save()
        return pos
    
    def get_position(self, code):
        """获取持仓"""
        return self.positions.get(code)
    
    def get_all_positions(self):
        """获取所有持仓"""
        return self.positions
    
    def get_total_market_value(self, prices):
        """计算总市值"""
        total = 0.0
        for code, pos in self.positions.items():
            price = prices.get(code, pos.get('avg_cost', 0))
            total += pos['quantity'] * price
        return total
    
    def get_total_profit(self, prices):
        """计算总浮动盈亏"""
        total = 0.0
        for code, pos in self.positions.items():
            price = prices.get(code, pos.get('avg_cost', 0))
            profit = (price - pos['avg_cost']) * pos['quantity']
            total += profit
        return total
    
    def clear(self):
        """清空所有持仓"""
        self.positions = {}
        self.save()


if __name__ == "__main__":
    # 测试
    positions = Positions()
    print(positions.get_all_positions())
