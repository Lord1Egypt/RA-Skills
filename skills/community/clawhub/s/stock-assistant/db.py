#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库操作
"""

import sqlite3
import os
import sys
from typing import List, Optional, Dict, Any
from contextlib import contextmanager

# 处理相对导入 - 检查是否作为模块导入
try:
    from .models import Trade, Position
except ImportError:
    from models import Trade, Position


class Database:
    def __init__(self, db_path: str = 'data/trades.db'):
        self.db_path = db_path
        self._ensure_dir()
        self._init_db()
    
    def _ensure_dir(self):
        """确保数据目录存在"""
        dir_path = os.path.dirname(self.db_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    @contextmanager
    def _get_conn(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    def _init_db(self):
        """初始化数据库表"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            
            # 交易记录表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trade_date TEXT NOT NULL,
                    trade_time TEXT,
                    code TEXT NOT NULL,
                    name TEXT,
                    direction TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    amount REAL NOT NULL,
                    commission REAL DEFAULT 0,
                    fee REAL DEFAULT 0,
                    stamp_tax REAL DEFAULT 0,
                    transfer_fee REAL DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            ''')
            
            # 创建索引
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_trades_code ON trades(code)
            ''')
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_trades_date ON trades(trade_date)
            ''')
    
    def add_trade(self, trade: Trade) -> int:
        """添加交易记录"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO trades (
                    trade_date, trade_time, code, name, direction,
                    quantity, price, amount, commission, fee,
                    stamp_tax, transfer_fee, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                trade.trade_date, trade.trade_time, trade.code, trade.name,
                trade.direction, trade.quantity, trade.price, trade.amount,
                trade.commission, trade.fee, trade.stamp_tax, trade.transfer_fee,
                trade.created_at
            ))
            return cursor.lastrowid
    
    def get_trades(self, code: Optional[str] = None) -> List[Trade]:
        """获取交易记录"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            
            if code:
                cursor.execute(
                    'SELECT * FROM trades WHERE code = ? ORDER BY trade_date DESC, trade_time DESC',
                    (code,)
                )
            else:
                cursor.execute('SELECT * FROM trades ORDER BY trade_date DESC, trade_time DESC')
            
            rows = cursor.fetchall()
            return [self._row_to_trade(row) for row in rows]
    
    def get_trade_by_id(self, trade_id: int) -> Optional[Trade]:
        """根据ID获取交易记录"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM trades WHERE id = ?', (trade_id,))
            row = cursor.fetchone()
            return self._row_to_trade(row) if row else None
    
    def update_trade(self, trade: Trade) -> bool:
        """更新交易记录"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE trades SET
                    trade_date = ?, trade_time = ?, code = ?, name = ?,
                    direction = ?, quantity = ?, price = ?, amount = ?,
                    commission = ?, fee = ?, stamp_tax = ?, transfer_fee = ?
                WHERE id = ?
            ''', (
                trade.trade_date, trade.trade_time, trade.code, trade.name,
                trade.direction, trade.quantity, trade.price, trade.amount,
                trade.commission, trade.fee, trade.stamp_tax, trade.transfer_fee,
                trade.id
            ))
            return cursor.rowcount > 0
    
    def delete_trade(self, trade_id: int) -> bool:
        """删除交易记录"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM trades WHERE id = ?', (trade_id,))
            return cursor.rowcount > 0
    
    def delete_all_trades(self) -> int:
        """删除所有交易记录"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM trades')
            return cursor.rowcount
    
    def get_positions(self) -> List[Position]:
        """计算持仓"""
        trades = self.get_trades()
        
        # 按股票代码分组
        positions: Dict[str, Position] = {}
        
        for trade in trades:
            if trade.code not in positions:
                positions[trade.code] = Position(
                    code=trade.code,
                    name=trade.name,
                    quantity=0,
                    avg_cost=0.0,
                    total_cost=0.0
                )
            
            pos = positions[trade.code]
            
            if trade.direction == '买入':
                # 计算新的平均成本
                total_cost = pos.total_cost + trade.amount + trade.commission + trade.fee
                total_qty = pos.quantity + trade.quantity
                pos.quantity = total_qty
                pos.total_cost = total_cost
                pos.avg_cost = total_cost / total_qty if total_qty > 0 else 0
            elif trade.direction == '卖出':
                pos.quantity -= trade.quantity
                pos.total_cost -= trade.amount - trade.commission - trade.fee
        
        # 过滤掉持仓为0的
        return [p for p in positions.values() if p.quantity > 0]
    
    def _row_to_trade(self, row) -> Trade:
        """将数据库行转换为Trade对象"""
        return Trade(
            id=row['id'],
            trade_date=row['trade_date'],
            trade_time=row['trade_time'],
            code=row['code'],
            name=row['name'],
            direction=row['direction'],
            quantity=row['quantity'],
            price=row['price'],
            amount=row['amount'],
            commission=row['commission'],
            fee=row['fee'],
            stamp_tax=row['stamp_tax'],
            transfer_fee=row['transfer_fee'],
            created_at=row['created_at']
        )


# 全局数据库实例
_db: Optional[Database] = None


def get_db(db_path: str = 'data/trades.db') -> Database:
    """获取数据库实例"""
    global _db
    if _db is None:
        _db = Database(db_path)
    return _db
