"""
TOC Trading System - 持仓服务
"""
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from data.storage import Storage
from tushare_client import TushareClient

class PositionService:
    """持仓服务"""
    
    def __init__(self, storage: Storage = None, tushare: TushareClient = None):
        self.storage = storage or Storage()
        self.tushare = tushare or TushareClient()
    
    def buy(self, stock_code: str, quantity: int, price: float, 
            remark: str = None, stock_name: str = None) -> Tuple[bool, str]:
        """
        记录买入
        Args:
            stock_code: 股票代码
            quantity: 数量（手或股）
            price: 买入价格
            remark: 备注
            stock_name: 股票名称（可选）
        Returns: (success, message)
        """
        # 获取股票信息
        stock_info = self.tushare.get_stock_basic(stock_code)
        code = stock_info.get('code', self._normalize_code(stock_code))
        name = stock_name or stock_info.get('name', stock_code)
        
        # 计算股数（1手=100股）
        if quantity >= 100:
            shares = quantity  # 传入的是手数，转为股数
        else:
            shares = quantity * 100  # 传入的是手数
        
        position = {
            'id': str(uuid.uuid4())[:8],
            'stock_code': code,
            'stock_name': name,
            'buy_date': datetime.now().strftime('%Y-%m-%d'),
            'buy_price': float(price),
            'quantity': shares,
            'quantity_unit': '手',
            'remark': remark or '',
            'created_at': datetime.now().isoformat()
        }
        
        positions = self.storage.get_positions()
        positions.append(position)
        
        if self.storage.save_positions(positions):
            cost = shares * float(price)
            return True, f"✅ 买入记录已保存\n股票：{name}\n买入价：{price:.2f}\n数量：{shares//100}手 ({shares}股)\n持仓成本：{cost:,.0f} 元"
        else:
            return False, "保存失败"
    
    def sell(self, stock_code: str, quantity: int = None, price: float = None,
             remark: str = None) -> Tuple[bool, str]:
        """
        记录卖出
        Args:
            stock_code: 股票代码
            quantity: 卖出数量（股），None 表示全部
            price: 卖出价格，None 表示使用实时价格
            remark: 备注
        Returns: (success, message)
        """
        positions = self.storage.get_positions()
        code = self._normalize_code(stock_code)
        
        # 找到对应持仓
        target_pos = None
        for pos in positions:
            if pos.get('stock_code') == code:
                target_pos = pos
                break
        
        if not target_pos:
            return False, f"没有找到 {stock_code} 的持仓"
        
        # 确定卖出数量和价格
        sell_quantity = quantity or target_pos['quantity']
        if price is None:
            quote = self.tushare.get_realtime_quote(code)
            if quote:
                price = quote.get('price')
            else:
                return False, "无法获取当前价格"
        
        sell_amount = sell_quantity * float(price)
        cost = target_pos['quantity'] * target_pos['buy_price']
        
        # 计算收益（按比例）
        sell_ratio = sell_quantity / target_pos['quantity']
        cost_ratio = cost * sell_ratio
        profit = sell_amount - cost_ratio
        profit_rate = (profit / cost_ratio) * 100 if cost_ratio > 0 else 0
        
        # 记录交易
        trade = {
            'id': str(uuid.uuid4())[:8],
            'type': 'sell',
            'stock_code': code,
            'stock_name': target_pos['stock_name'],
            'trade_date': datetime.now().strftime('%Y-%m-%d'),
            'price': float(price),
            'quantity': sell_quantity,
            'amount': sell_amount,
            'profit': profit,
            'profit_rate': profit_rate,
            'created_at': datetime.now().isoformat()
        }
        
        self.storage.add_trade(trade)
        
        # 更新持仓
        remaining = target_pos['quantity'] - sell_quantity
        if remaining <= 0:
            positions.remove(target_pos)
        else:
            target_pos['quantity'] = remaining
        
        self.storage.save_positions(positions)
        
        return True, f"✅ 卖出记录已保存\n股票：{target_pos['stock_name']}\n卖出价：{price:.2f}\n数量：{sell_quantity//100}手 ({sell_quantity}股)\n卖出金额：{sell_amount:,.0f} 元\n收益：{profit:+,.0f} 元 ({profit_rate:+.2f}%)"
    
    def get_positions(self, with_profit: bool = True) -> List[Dict]:
        """
        获取当前持仓
        Args:
            with_profit: 是否计算盈亏
        """
        positions = self.storage.get_positions()
        
        if with_profit:
            for pos in positions:
                quote = self.tushare.get_realtime_quote(pos['stock_code'])
                if quote:
                    current_price = quote.get('price', 0)
                    buy_price = pos['buy_price']
                    quantity = pos['quantity']
                    
                    pos['current_price'] = current_price
                    pos['market_value'] = current_price * quantity
                    pos['cost'] = buy_price * quantity
                    pos['profit'] = (current_price - buy_price) * quantity
                    pos['profit_rate'] = ((current_price - buy_price) / buy_price) * 100 if buy_price > 0 else 0
                else:
                    pos['current_price'] = pos['buy_price']
                    pos['market_value'] = pos['buy_price'] * pos['quantity']
                    pos['cost'] = pos['buy_price'] * pos['quantity']
                    pos['profit'] = 0
                    pos['profit_rate'] = 0
        
        return positions
    
    def get_total_profit(self) -> Tuple[float, float]:
        """获取总盈亏"""
        positions = self.get_positions(with_profit=True)
        total_profit = sum(p.get('profit', 0) for p in positions)
        total_cost = sum(p.get('cost', 0) for p in positions)
        total_rate = (total_profit / total_cost) * 100 if total_cost > 0 else 0
        return total_profit, total_rate
    
    def format_positions(self, positions: List[Dict] = None) -> str:
        """格式化持仓为 Markdown 表格"""
        if positions is None:
            positions = self.get_positions(with_profit=True)
        
        if not positions:
            return "📊 当前持仓\n暂无持仓"
        
        lines = ["📊 当前持仓"]
        lines.append("| 股票 | 买入价 | 当前价 | 数量 | 盈亏 | 盈亏率 |")
        lines.append("|------|--------|--------|------|------|--------|")
        
        for p in positions:
            name = p.get('stock_name', '-')
            buy_price = p.get('buy_price', 0)
            current_price = p.get('current_price', 0)
            quantity = p.get('quantity', 0)
            profit = p.get('profit', 0)
            profit_rate = p.get('profit_rate', 0)
            
            lines.append(f"| {name} | {buy_price:.2f} | {current_price:.2f} | {quantity//100}手 | {profit:+,.0f} | {profit_rate:+.2f}% |")
        
        total_profit, total_rate = self.get_total_profit()
        lines.append(f"\n💰 总盈亏：{total_profit:+,.0f} 元 ({total_rate:+.2f}%)")
        
        return '\n'.join(lines)
    
    def get_trades(self) -> List[Dict]:
        """获取历史交易记录"""
        return self.storage.get_trades()
    
    def format_trades(self) -> str:
        """格式化交易记录"""
        trades = self.get_trades()
        
        if not trades:
            return "📋 历史交易\n暂无交易记录"
        
        lines = ["📋 历史交易"]
        lines.append("| 日期 | 类型 | 股票 | 价格 | 数量 | 金额 | 收益 |")
        lines.append("|------|------|------|------|------|------|------|")
        
        for t in trades:
            date = t.get('trade_date', '-')
            type_ = '买入' if t.get('type') == 'buy' else '卖出'
            name = t.get('stock_name', '-')
            price = t.get('price', 0)
            quantity = t.get('quantity', 0)
            amount = t.get('amount', 0)
            profit = t.get('profit', 0)
            
            if profit != 0:
                profit_str = f"{profit:+,.0f}"
            else:
                profit_str = '-'
            
            lines.append(f"| {date} | {type_} | {name} | {price:.2f} | {quantity//100}手 | {amount:,.0f} | {profit_str} |")
        
        return '\n'.join(lines)
    
    def _normalize_code(self, code: str) -> str:
        """标准化股票代码"""
        code = code.strip().upper()
        if '.' not in code:
            if code.startswith('6'):
                return f"{code}.SH"
            else:
                return f"{code}.SZ"
        return code