#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交易逻辑模块
"""

import csv
import os
import sys
from typing import List, Optional, Dict, Any
from datetime import datetime

# 处理相对导入 - 检查是否作为模块导入
try:
    from .models import Trade, Position, PnLResult
    from .db import get_db
    from .fetcher import get_quote
except ImportError:
    from models import Trade, Position, PnLResult
    from db import get_db
    from fetcher import get_quote


class StockTrader:
    """股票交易管理器"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # 自动适配路径：Linux/Mac 用 /tmp 或当前目录，Windows 用相对路径
            import sys
            if sys.platform == 'win32':
                db_path = 'data/trades.db'
            else:
                # Linux/Mac: 使用脚本所在目录
                db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'trades.db')
        self.db = get_db(db_path)
    
    def add_trade(self, trade_data: Dict[str, Any]) -> int:
        """添加交易记录"""
        trade = Trade(
            trade_date=trade_data.get('date', trade_data.get('trade_date', '')),
            trade_time=trade_data.get('time', trade_data.get('trade_time', '')),
            code=trade_data.get('code', ''),
            name=trade_data.get('name', ''),
            direction=trade_data.get('direction', trade_data.get('type', '')),
            quantity=int(trade_data.get('quantity', 0)),
            price=float(trade_data.get('price', 0)),
            amount=float(trade_data.get('amount', 0)),
            commission=float(trade_data.get('commission', 0)),
            fee=float(trade_data.get('fee', 0)),
            stamp_tax=float(trade_data.get('stamp_tax', 0)),
            transfer_fee=float(trade_data.get('transfer_fee', 0)),
        )
        return self.db.add_trade(trade)
    
    def import_csv(self, file_path: str) -> int:
        """
        从CSV文件导入交易记录
        
        CSV格式：
        日期,时间,股票代码,股票名称,买卖方向,成交数量,成交均价,成交金额,佣金,其他费用,印花税,过户费
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        count = 0
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    trade = Trade(
                        trade_date=row.get('日期', '').strip(),
                        trade_time=row.get('时间', '').strip(),
                        code=row.get('股票代码', '').strip(),
                        name=row.get('股票名称', '').strip(),
                        direction=row.get('买卖方向', row.get('direction', '')).strip(),
                        quantity=int(float(row.get('成交数量', 0))),
                        price=float(row.get('成交均价', 0)),
                        amount=float(row.get('成交金额', 0)),
                        commission=float(row.get('佣金', 0)),
                        fee=float(row.get('其他费用', 0)),
                        stamp_tax=float(row.get('印花税', 0)),
                        transfer_fee=float(row.get('过户费', 0)),
                    )
                    if trade.code and trade.quantity:
                        self.db.add_trade(trade)
                        count += 1
                except Exception as e:
                    print(f"导入行失败: {row}, 错误: {e}")
        
        return count
    
    def get_positions(self) -> List[Position]:
        """获取所有持仓"""
        return self.db.get_positions()
    
    def get_position(self, code: str) -> Optional[Position]:
        """获取指定股票的持仓"""
        positions = self.db.get_positions()
        for pos in positions:
            if pos.code == code:
                return pos
        return None
    
    def calculate_pnl(self, code: str, current_price: float) -> Optional[PnLResult]:
        """
        计算指定股票的盈亏
        
        Args:
            code: 股票代码
            current_price: 当前价格
        
        Returns:
            盈亏结果
        """
        position = self.get_position(code)
        
        if not position or position.quantity == 0:
            return None
        
        market_value = position.quantity * current_price
        profit = market_value - position.total_cost
        profit_pct = (profit / position.total_cost * 100) if position.total_cost > 0 else 0
        
        return PnLResult(
            code=code,
            name=position.name,
            quantity=position.quantity,
            avg_cost=position.avg_cost,
            current_price=current_price,
            market_value=market_value,
            profit=profit,
            profit_pct=profit_pct
        )
    
    def get_pnl_with_live_price(self, code: str) -> Optional[PnLResult]:
        """
        获取实时行情并计算盈亏
        """
        quote = get_quote(code)
        
        if 'error' in quote:
            raise ValueError(f"获取行情失败: {quote['error']}")
        
        current_price = float(quote.get('当前价格', 0))
        if current_price == 0:
            raise ValueError("获取到的股价为0")
        
        return self.calculate_pnl(code, current_price)
    
    def export_csv(self, file_path: str, code: Optional[str] = None) -> int:
        """导出交易记录到CSV"""
        trades = self.db.get_trades(code)
        
        with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
            fieldnames = [
                '日期', '时间', '股票代码', '股票名称', '买卖方向',
                '成交数量', '成交均价', '成交金额', '佣金', '其他费用', '印花税', '过户费'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for trade in trades:
                writer.writerow({
                    '日期': trade.trade_date,
                    '时间': trade.trade_time,
                    '股票代码': trade.code,
                    '股票名称': trade.name,
                    '买卖方向': trade.direction,
                    '成交数量': trade.quantity,
                    '成交均价': trade.price,
                    '成交金额': trade.amount,
                    '佣金': trade.commission,
                    '其他费用': trade.fee,
                    '印花税': trade.stamp_tax,
                    '过户费': trade.transfer_fee,
                })
        
        return len(trades)
    
    def list_trades(self, code: Optional[str] = None) -> List[Trade]:
        """列出交易记录"""
        return self.db.get_trades(code)
    
    def delete_trade(self, trade_id: int) -> bool:
        """删除交易记录"""
        return self.db.delete_trade(trade_id)
    
    def clear_all(self) -> int:
        """清空所有交易记录"""
        return self.db.delete_all_trades()


# 便捷函数
def create_trader(db_path: str = 'data/trades.db') -> StockTrader:
    """创建交易管理器实例"""
    return StockTrader(db_path)
