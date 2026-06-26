"""
TOC Trading System - 股票池服务
"""
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from data.storage import Storage
from tushare_client import TushareClient

class StockPoolService:
    """股票池服务"""
    
    def __init__(self, storage: Storage = None, tushare: TushareClient = None):
        self.storage = storage or Storage()
        self.tushare = tushare or TushareClient()
    
    def add_stock(self, stock_code: str, name: str = None, reason: str = None, 
                  remark: str = None, tags: List[str] = None) -> Tuple[bool, str]:
        """
        添加股票到股票池
        Returns: (success, message)
        """
        # 获取股票信息
        stock_info = self.tushare.get_stock_basic(stock_code)
        if not stock_info and not name:
            return False, f"无法获取股票 {stock_code} 的信息"
        
        code = stock_info.get('code', stock_code)
        stock_name = name or stock_info.get('name', stock_code)
        industry = stock_info.get('industry', '未知')
        
        # 检查是否已存在
        stocks = self.storage.get_stocks()
        for s in stocks:
            if s.get('code') == code and s.get('enabled', True):
                return False, f"{stock_name}({code}) 已在股票池中"
        
        # 添加新股票
        new_stock = {
            'id': str(uuid.uuid4())[:8],
            'code': code,
            'name': stock_name,
            'industry': industry,
            'added_at': datetime.now().isoformat(),
            'reason': reason or '',
            'remark': remark or '',
            'tags': tags or [],
            'enabled': True
        }
        
        stocks.append(new_stock)
        if self.storage.save_stocks(stocks):
            return True, f"✅ 已添加 {stock_name}({code}) 到股票池\n行业：{industry}"
        else:
            return False, "保存失败"
    
    def remove_stock(self, stock_code: str) -> Tuple[bool, str]:
        """
        从股票池移除股票
        """
        stocks = self.storage.get_stocks()
        code = self._normalize_code(stock_code)
        
        for s in stocks:
            if s.get('code') == code and s.get('enabled', True):
                s['enabled'] = False
                s['removed_at'] = datetime.now().isoformat()
                if self.storage.save_stocks(stocks):
                    return True, f"✅ 已移除 {s.get('name')}({code})"
                else:
                    return False, "保存失败"
        
        return False, f"股票 {stock_code} 不在股票池中"
    
    def list_stocks(self, group_by_industry: bool = False) -> List[Dict]:
        """
        列出股票池中的股票（带实时行情）
        """
        stocks = self.storage.get_stocks()
        enabled_stocks = [s for s in stocks if s.get('enabled', True)]
        
        # 获取实时行情
        for stock in enabled_stocks:
            quote = self.tushare.get_realtime_quote(stock['code'])
            if quote:
                stock['price'] = quote.get('price', 0)
                stock['change_pct'] = quote.get('change_pct', 0)
            else:
                stock['price'] = stock.get('price', '-')
                stock['change_pct'] = stock.get('change_pct', '-')
        
        if group_by_industry:
            # 按行业分组
            grouped = {}
            for s in enabled_stocks:
                industry = s.get('industry', '未知')
                if industry not in grouped:
                    grouped[industry] = []
                grouped[industry].append(s)
            return grouped
        else:
            return enabled_stocks
    
    def search_stock(self, keyword: str) -> List[Dict]:
        """搜索股票"""
        results = self.tushare.search_stock(keyword)
        return results
    
    def get_stock_info(self, stock_code: str) -> Optional[Dict]:
        """获取单只股票信息"""
        code = self._normalize_code(stock_code)
        stocks = self.storage.get_stocks()
        for s in stocks:
            if s.get('code') == code and s.get('enabled', True):
                quote = self.tushare.get_realtime_quote(code)
                if quote:
                    s['price'] = quote.get('price', 0)
                    s['change_pct'] = quote.get('change_pct', 0)
                return s
        return None
    
    def format_stock_list(self, stocks: List[Dict], title: str = "📈 股票池") -> str:
        """格式化股票列表为 Markdown 表格"""
        if not stocks:
            return f"{title}\n暂无股票"
        
        lines = [f"{title}\n"]
        lines.append("| 代码 | 名称 | 行业 | 价格 | 涨幅 |")
        lines.append("|------|------|------|------|------|")
        
        for s in stocks:
            code = s.get('code', '-')
            name = s.get('name', '-')
            industry = s.get('industry', '-')
            price = s.get('price', '-')
            change = s.get('change_pct', '-')
            
            if isinstance(price, (int, float)):
                price = f"{price:.2f}"
            if isinstance(change, (int, float)):
                change_str = f"{change:+.2f}%" if change != '-' else '-'
            else:
                change_str = change
            
            lines.append(f"| {code} | {name} | {industry} | {price} | {change_str} |")
        
        return '\n'.join(lines)
    
    def format_grouped_stocks(self, grouped: Dict[str, List]) -> str:
        """格式化行业分组的股票"""
        lines = ["📈 股票池（按行业分组）"]
        
        for industry, stocks in grouped.items():
            lines.append(f"\n### {industry}")
            lines.append("| 代码 | 名称 | 价格 | 涨幅 |")
            lines.append("|------|------|------|------|")
            
            for s in stocks:
                code = s.get('code', '-')
                name = s.get('name', '-')
                price = s.get('price', '-')
                change = s.get('change_pct', '-')
                
                if isinstance(price, (int, float)):
                    price = f"{price:.2f}"
                if isinstance(change, (int, float)):
                    change_str = f"{change:+.2f}%" if change != '-' else '-'
                else:
                    change_str = change
                
                lines.append(f"| {code} | {name} | {price} | {change_str} |")
        
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