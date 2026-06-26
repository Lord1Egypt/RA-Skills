"""
TOC Trading System - Tushare 客户端封装
"""
import os
import tushare as ts
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd

class TushareClient:
    """Tushare 数据封装"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        token = os.environ.get('TUSHARE_TOKEN')
        if token:
            ts.set_token(token)
            self.pro = ts.pro_api()
        else:
            self.pro = None
            print("⚠️ TUSHARE_TOKEN 未设置，部分功能不可用")
    
    def is_available(self) -> bool:
        """检查是否可用"""
        return self.pro is not None
    
    def get_stock_basic(self, stock_code: str) -> Optional[Dict]:
        """获取股票基本信息"""
        if not self.is_available():
            return None
        
        try:
            # 如果没有市场后缀，自动推断
            code = stock_code
            if '.' not in code:
                # 简单判断：6开头是上海，0/3开头是深圳
                if code.startswith('6'):
                    code = f"{code}.SH"
                else:
                    code = f"{code}.SZ"
            
            df = self.pro.stock_basic(ts_code=code, fields='ts_code,symbol,name,industry,market,list_date')
            if df is not None and len(df) > 0:
                row = df.iloc[0]
                return {
                    'code': row['ts_code'],
                    'name': row['name'],
                    'industry': row['industry'],
                    'market': row['market'],
                    'list_date': row['list_date']
                }
        except Exception as e:
            print(f"获取股票基本信息失败: {e}")
        return None
    
    def get_realtime_quote(self, stock_code: str) -> Optional[Dict]:
        """获取实时行情（单只）"""
        if not self.is_available():
            return None
        
        try:
            code = stock_code
            if '.' not in code:
                if code.startswith('6'):
                    code = f"{code}.SH"
                else:
                    code = f"{code}.SZ"
            
            df = ts.realtime_quote(ts_code=code)
            if df is not None and len(df) > 0:
                row = df.iloc[0]
                return {
                    'code': row['ts_code'],
                    'name': row['name'],
                    'price': float(row['price']) if row['price'] else 0,
                    'change_pct': float(row['pct_change']) if row['pct_change'] else 0,
                    'volume': int(row['volume']) if row['volume'] else 0,
                    'amount': float(row['amount']) if row['amount'] else 0,
                    'high': float(row['high']) if row['high'] else 0,
                    'low': float(row['low']) if row['low'] else 0,
                    'open': float(row['open']) if row['open'] else 0,
                    'prev_close': float(row['pre_close']) if row['pre_close'] else 0,
                    'bid': float(row['bid']) if row['bid'] else 0,
                    'ask': float(row['ask']) if row['ask'] else 0
                }
        except Exception as e:
            print(f"获取实时行情失败: {e}")
        return None
    
    def get_daily(self, stock_code: str, start_date: str = None, end_date: str = None) -> List[Dict]:
        """获取日线行情"""
        if not self.is_available():
            return []
        
        try:
            code = stock_code
            if '.' not in code:
                if code.startswith('6'):
                    code = f"{code}.SH"
                else:
                    code = f"{code}.SZ"
            
            if end_date is None:
                end_date = datetime.now().strftime('%Y%m%d')
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            
            df = self.pro.daily(ts_code=code, start_date=start_date, end_date=end_date)
            if df is not None and len(df) > 0:
                df = df.sort_values('trade_date', ascending=False)
                return df.to_dict('records')
        except Exception as e:
            print(f"获取日线行情失败: {e}")
        return []
    
    def get_last_trade_date(self) -> str:
        """获取最近交易日"""
        if not self.is_available():
            return datetime.now().strftime('%Y%m%d')
        
        try:
            today = datetime.now().strftime('%Y%m%d')
            df = self.pro.trade_cal(exchange='SSE', end_date=today, is_open='1')
            if df is not None and len(df) > 0:
                return df.iloc[-1]['cal_date']
        except Exception as e:
            print(f"获取交易日历失败: {e}")
        return today
    
    def get_open_price(self, stock_code: str, trade_date: str) -> Optional[float]:
        """获取指定日期开盘价"""
        daily_data = self.get_daily(stock_code, start_date=trade_date, end_date=trade_date)
        if daily_data and len(daily_data) > 0:
            return daily_data[0].get('open')
        return None
    
    def get_yesterday_open(self, stock_code: str) -> Optional[float]:
        """获取昨日开盘价"""
        if not self.is_available():
            return None
        
        try:
            today = datetime.now()
            code = stock_code
            if '.' not in code:
                if code.startswith('6'):
                    code = f"{code}.SH"
                else:
                    code = f"{code}.SZ"
            
            # 获取最近2个交易日
            df = self.pro.daily(ts_code=code, start_date=(today - timedelta(days=7)).strftime('%Y%m%d'))
            if df is not None and len(df) >= 2:
                df = df.sort_values('trade_date', ascending=False)
                # 最新一条是今日或昨日
                latest = df.iloc[0]
                if len(df) >= 2:
                    return df.iloc[1]['open']  # 前一条是昨天
        except Exception as e:
            print(f"获取昨日开盘价失败: {e}")
        return None
    
    def get_limit_list(self, trade_date: str = None) -> List[Dict]:
        """获取涨停列表"""
        if not self.is_available():
            return []
        
        try:
            if trade_date is None:
                trade_date = self.get_last_trade_date()
            
            df = self.pro.limit_list_d(trade_date=trade_date)
            if df is not None and len(df) > 0:
                return df.to_dict('records')
        except Exception as e:
            print(f"获取涨停列表失败: {e}")
        return []
    
    def get_moneyflow(self, trade_date: str = None) -> List[Dict]:
        """获取资金流向"""
        if not self.is_available():
            return []
        
        try:
            if trade_date is None:
                trade_date = self.get_last_trade_date()
            
            df = self.pro.moneyflow(trade_date=trade_date)
            if df is not None and len(df) > 0:
                return df.to_dict('records')
        except Exception as e:
            print(f"获取资金流向失败: {e}")
        return []
    
    def get_hsgt_top(self, trade_date: str = None, direction: str = 'in') -> List[Dict]:
        """获取北向资金top"""
        if not self.is_available():
            return []
        
        try:
            if trade_date is None:
                trade_date = self.get_last_trade_date()
            
            df = self.pro.hsgt_top10(trade_date=trade_date, market_type='2', direction=direction)
            if df is not None and len(df) > 0:
                return df.to_dict('records')
        except Exception as e:
            print(f"获取北向资金top失败: {e}")
        return []
    
    def get_industry_stocks(self, industry: str = None) -> List[Dict]:
        """获取行业分类"""
        if not self.is_available():
            return []
        
        try:
            df = self.pro.index_classify(level='L1', src='SW2021')
            if df is not None and len(df) > 0:
                if industry:
                    df = df[df['industry_name'].str.contains(industry, na=False)]
                return df.to_dict('records')
        except Exception as e:
            print(f"获取行业分类失败: {e}")
        return []
    
    def search_stock(self, keyword: str) -> List[Dict]:
        """搜索股票"""
        if not self.is_available():
            return []
        
        try:
            # 搜索股票基本信息
            df = self.pro.stock_basic(exchange='', list_status='L', 
                                      fields='ts_code,symbol,name,industry')
            if df is not None and len(df) > 0:
                # 按名称或代码模糊搜索
                mask = df['name'].str.contains(keyword, na=False) | \
                       df['symbol'].str.contains(keyword, na=False)
                results = df[mask].head(10)
                return results.to_dict('records')
        except Exception as e:
            print(f"搜索股票失败: {e}")
        return []