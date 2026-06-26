#!/usr/bin/env python3
"""
初始化模拟账户
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import INITIAL_CAPITAL
from account import Account
from positions import Positions


def init_account():
    """初始化账户"""
    # 创建账户
    account = Account()
    account.reset()
    
    # 清空持仓
    positions = Positions()
    positions.clear()
    
    print("=" * 50)
    print("✅ 模拟交易账户已初始化")
    print("=" * 50)
    print(f"💰 初始资金：¥{INITIAL_CAPITAL:,.2f}")
    print(f"💳 可用资金：¥{account.cash:,.2f}")
    print("=" * 50)


if __name__ == "__main__":
    init_account()
