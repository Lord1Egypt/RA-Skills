#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据模型
"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Trade:
    """交易记录"""
    id: Optional[int] = None
    trade_date: str = ''
    trade_time: str = ''
    code: str = ''
    name: str = ''
    direction: str = ''  # 买入/卖出
    quantity: int = 0
    price: float = 0.0
    amount: float = 0.0
    commission: float = 0.0
    fee: float = 0.0
    stamp_tax: float = 0.0
    transfer_fee: float = 0.0
    created_at: str = ''
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@dataclass
class Position:
    """持仓"""
    code: str = ''
    name: str = ''
    quantity: int = 0
    avg_cost: float = 0.0
    total_cost: float = 0.0
    
    @property
    def market_value(self) -> float:
        """市值"""
        return self.quantity * self.avg_cost
    
    @property
    def profit(self) -> float:
        """盈亏金额"""
        return 0.0  # 需要传入当前价计算


@dataclass
class PnLResult:
    """盈亏结果"""
    code: str = ''
    name: str = ''
    quantity: int = 0
    avg_cost: float = 0.0
    current_price: float = 0.0
    market_value: float = 0.0
    profit: float = 0.0
    profit_pct: float = 0.0
