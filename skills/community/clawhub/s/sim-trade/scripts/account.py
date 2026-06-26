#!/usr/bin/env python3
"""
账户管理模块
"""
import json
import os
from config import ACCOUNT_FILE, INITIAL_CAPITAL


class Account:
    def __init__(self):
        self.load()
    
    def load(self):
        """加载账户数据"""
        if os.path.exists(ACCOUNT_FILE):
            with open(ACCOUNT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.initial_capital = data.get('initial_capital', INITIAL_CAPITAL)
                self.cash = data.get('cash', self.initial_capital)
                self.frozen_cash = data.get('frozen_cash', 0.0)
                self.total_fee = data.get('total_fee', 0.0)
                self.total_stamp_tax = data.get('total_stamp_tax', 0.0)
        else:
            self.initial_capital = INITIAL_CAPITAL
            self.cash = INITIAL_CAPITAL
            self.frozen_cash = 0.0
            self.total_fee = 0.0
            self.total_stamp_tax = 0.0
    
    def save(self):
        """保存账户数据"""
        data = {
            'initial_capital': self.initial_capital,
            'cash': self.cash,
            'frozen_cash': self.frozen_cash,
            'total_fee': self.total_fee,
            'total_stamp_tax': self.total_stamp_tax
        }
        with open(ACCOUNT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def freeze(self, amount):
        """冻结资金（限价委托）"""
        if self.cash >= amount:
            self.cash -= amount
            self.frozen_cash += amount
            self.save()
            return True
        return False
    
    def unfreeze(self, amount):
        """解冻资金"""
        if self.frozen_cash >= amount:
            self.frozen_cash -= amount
            self.cash += amount
            self.save()
    
    def deduct(self, amount):
        """扣除资金（成交）"""
        self.cash -= amount
        self.save()
    
    def add(self, amount):
        """增加资金（卖出成交）"""
        self.cash += amount
        self.save()
    
    def add_fee(self, fee):
        """增加手续费"""
        self.total_fee += fee
        self.save()
    
    def add_stamp_tax(self, tax):
        """增加印花税"""
        self.total_stamp_tax += tax
        self.save()
    
    def get_available_cash(self):
        """获取可用资金"""
        return self.cash
    
    def get_total_assets(self, market_value=0):
        """获取总资产"""
        return self.cash + market_value
    
    def get_total_cost(self):
        """获取总成本（手续费+印花税）"""
        return self.total_fee + self.total_stamp_tax
    
    def reset(self):
        """重置账户"""
        self.cash = self.initial_capital
        self.frozen_cash = 0.0
        self.total_fee = 0.0
        self.total_stamp_tax = 0.0
        self.save()


def init_account():
    """初始化账户"""
    account = Account()
    account.reset()
    print(f"✅ 模拟账户已初始化")
    print(f"💰 初始资金：¥{account.initial_capital:,.2f}")
    return account


if __name__ == "__main__":
    init_account()
