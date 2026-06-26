"""
Tushare数据采集工具
提供行情数据和基本面数据的获取功能
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import json

try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    TUSHARE_AVAILABLE = False
    print("警告: tushare未安装，将使用模拟数据")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class TushareTools:
    """Tushare数据采集工具类"""
    
    def __init__(self, token: Optional[str] = None):
        """
        初始化Tushare工具
        
        Args:
            token: Tushare API Token
        """
        self.token = token or os.getenv("TUSHARE_TOKEN", "")
        self.pro = None
        
        if TUSHARE_AVAILABLE and self.token:
            try:
                ts.set_token(self.token)
                self.pro = ts.pro_api()
                print("✅ Tushare初始化成功")
            except Exception as e:
                print(f"⚠️ Tushare初始化失败: {e}")
    
    def get_stock_basic(self, ts_code: str) -> Dict:
        """
        获取股票基本信息
        
        Args:
            ts_code: 股票代码，如 '600519.SH'
            
        Returns:
            股票基本信息字典
        """
        if self.pro:
            try:
                df = self.pro.stock_basic(
                    ts_code=ts_code,
                    fields='ts_code,symbol,name,area,industry,market,list_date'
                )
                if not df.empty:
                    return df.iloc[0].to_dict()
            except Exception as e:
                print(f"获取股票基本信息失败: {e}")
        
        # 返回模拟数据
        return {
            "ts_code": ts_code,
            "symbol": ts_code.split('.')[0],
            "name": "模拟股票",
            "area": "未知",
            "industry": "未知",
            "market": "主板",
            "list_date": "20100101"
        }
    
    def get_stock_daily(self, ts_code: str, days: int = 60) -> Dict:
        """
        获取日K线数据
        
        Args:
            ts_code: 股票代码
            days: 获取天数
            
        Returns:
            包含K线数据的字典
        """
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=days * 2)).strftime('%Y%m%d')
        
        if self.pro:
            try:
                df = self.pro.daily(
                    ts_code=ts_code,
                    start_date=start_date,
                    end_date=end_date
                )
                if not df.empty:
                    df = df.head(days).sort_values('trade_date')
                    return {
                        "ts_code": ts_code,
                        "data_count": len(df),
                        "latest_date": df.iloc[-1]['trade_date'],
                        "latest_close": float(df.iloc[-1]['close']),
                        "latest_open": float(df.iloc[-1]['open']),
                        "latest_high": float(df.iloc[-1]['high']),
                        "latest_low": float(df.iloc[-1]['low']),
                        "latest_volume": float(df.iloc[-1]['vol']),
                        "latest_amount": float(df.iloc[-1]['amount']),
                        "latest_pct_chg": float(df.iloc[-1]['pct_chg']),
                        "price_list": df['close'].tolist(),
                        "volume_list": df['vol'].tolist(),
                        "date_list": df['trade_date'].tolist()
                    }
            except Exception as e:
                print(f"获取日K线数据失败: {e}")
        
        # 返回模拟数据
        import random
        base_price = 100.0
        prices = [base_price + random.uniform(-5, 5) for _ in range(days)]
        return {
            "ts_code": ts_code,
            "data_count": days,
            "latest_date": end_date,
            "latest_close": prices[-1],
            "latest_open": prices[-1] - random.uniform(-1, 1),
            "latest_high": prices[-1] + random.uniform(0, 2),
            "latest_low": prices[-1] - random.uniform(0, 2),
            "latest_volume": random.uniform(100000, 500000),
            "latest_amount": random.uniform(10000000, 50000000),
            "latest_pct_chg": random.uniform(-3, 3),
            "price_list": prices,
            "volume_list": [random.uniform(100000, 500000) for _ in range(days)],
            "date_list": [(datetime.now() - timedelta(days=days-i)).strftime('%Y%m%d') for i in range(days)]
        }
    
    def get_technical_indicators(self, ts_code: str, days: int = 60) -> Dict:
        """
        计算技术指标
        
        Args:
            ts_code: 股票代码
            days: 数据天数
            
        Returns:
            技术指标字典
        """
        daily_data = self.get_stock_daily(ts_code, days)
        prices = daily_data.get("price_list", [])
        
        if not prices or len(prices) < 20:
            return self._mock_technical_indicators()
        
        # 计算均线
        ma5 = sum(prices[-5:]) / 5 if len(prices) >= 5 else prices[-1]
        ma10 = sum(prices[-10:]) / 10 if len(prices) >= 10 else prices[-1]
        ma20 = sum(prices[-20:]) / 20 if len(prices) >= 20 else prices[-1]
        ma60 = sum(prices[-60:]) / 60 if len(prices) >= 60 else prices[-1]
        
        current_price = prices[-1]
        
        # 判断均线信号
        ma_signal = "金叉" if ma5 > ma20 else "死叉"
        
        # 简化的MACD计算
        ema12 = self._calculate_ema(prices, 12)
        ema26 = self._calculate_ema(prices, 26)
        macd = ema12 - ema26
        macd_signal = "多头" if macd > 0 else "空头"
        
        # 简化的RSI计算
        rsi = self._calculate_rsi(prices, 14)
        if rsi > 70:
            rsi_signal = "超买"
        elif rsi < 30:
            rsi_signal = "超卖"
        else:
            rsi_signal = "中性"
        
        # 趋势判断
        if current_price > ma20 and ma5 > ma20:
            trend = "上涨"
        elif current_price < ma20 and ma5 < ma20:
            trend = "下跌"
        else:
            trend = "震荡"
        
        # 支撑位和阻力位（简化计算）
        recent_prices = prices[-20:]
        support = min(recent_prices) * 0.98
        resistance = max(recent_prices) * 1.02
        
        # 技术评分
        score = 50
        if ma_signal == "金叉":
            score += 15
        if macd_signal == "多头":
            score += 15
        if rsi_signal == "超卖":
            score += 10
        elif rsi_signal == "超买":
            score -= 10
        if trend == "上涨":
            score += 10
        elif trend == "下跌":
            score -= 10
        
        score = max(0, min(100, score))
        
        return {
            "ts_code": ts_code,
            "current_price": round(current_price, 2),
            "ma5": round(ma5, 2),
            "ma10": round(ma10, 2),
            "ma20": round(ma20, 2),
            "ma60": round(ma60, 2),
            "ma_signal": ma_signal,
            "macd": round(macd, 4),
            "macd_signal": macd_signal,
            "rsi": round(rsi, 2),
            "rsi_signal": rsi_signal,
            "trend": trend,
            "support": round(support, 2),
            "resistance": round(resistance, 2),
            "technical_score": score
        }
    
    def get_financial_indicator(self, ts_code: str) -> Dict:
        """
        获取财务指标
        
        Args:
            ts_code: 股票代码
            
        Returns:
            财务指标字典
        """
        if self.pro:
            try:
                # 获取最新财务指标
                df = self.pro.fina_indicator(
                    ts_code=ts_code,
                    fields='ts_code,end_date,roe,roa,debt_to_assets,grossprofit_margin,netprofit_margin,revenue_ps,cfps'
                )
                if not df.empty:
                    latest = df.iloc[0]
                    return {
                        "ts_code": ts_code,
                        "end_date": latest.get('end_date', ''),
                        "roe": float(latest.get('roe', 0) or 0),
                        "roa": float(latest.get('roa', 0) or 0),
                        "debt_ratio": float(latest.get('debt_to_assets', 0) or 0),
                        "gross_margin": float(latest.get('grossprofit_margin', 0) or 0),
                        "net_margin": float(latest.get('netprofit_margin', 0) or 0)
                    }
            except Exception as e:
                print(f"获取财务指标失败: {e}")
        
        # 返回模拟数据
        import random
        return {
            "ts_code": ts_code,
            "end_date": datetime.now().strftime('%Y%m%d'),
            "roe": round(random.uniform(5, 25), 2),
            "roa": round(random.uniform(2, 15), 2),
            "debt_ratio": round(random.uniform(20, 60), 2),
            "gross_margin": round(random.uniform(20, 50), 2),
            "net_margin": round(random.uniform(5, 25), 2)
        }
    
    def get_valuation(self, ts_code: str) -> Dict:
        """
        获取估值指标
        
        Args:
            ts_code: 股票代码
            
        Returns:
            估值指标字典
        """
        if self.pro:
            try:
                df = self.pro.daily_basic(
                    ts_code=ts_code,
                    fields='ts_code,trade_date,pe_ttm,pb,ps_ttm,dv_ratio,total_mv,circ_mv'
                )
                if not df.empty:
                    latest = df.iloc[0]
                    return {
                        "ts_code": ts_code,
                        "trade_date": latest.get('trade_date', ''),
                        "pe_ttm": float(latest.get('pe_ttm', 0) or 0),
                        "pb": float(latest.get('pb', 0) or 0),
                        "ps_ttm": float(latest.get('ps_ttm', 0) or 0),
                        "dv_ratio": float(latest.get('dv_ratio', 0) or 0),
                        "total_mv": float(latest.get('total_mv', 0) or 0),
                        "circ_mv": float(latest.get('circ_mv', 0) or 0)
                    }
            except Exception as e:
                print(f"获取估值指标失败: {e}")
        
        # 返回模拟数据
        import random
        return {
            "ts_code": ts_code,
            "trade_date": datetime.now().strftime('%Y%m%d'),
            "pe_ttm": round(random.uniform(10, 50), 2),
            "pb": round(random.uniform(1, 10), 2),
            "ps_ttm": round(random.uniform(1, 20), 2),
            "dv_ratio": round(random.uniform(0, 5), 2),
            "total_mv": round(random.uniform(10000, 100000), 2),
            "circ_mv": round(random.uniform(5000, 80000), 2)
        }
    
    def get_income_statement(self, ts_code: str) -> Dict:
        """
        获取利润表数据
        
        Args:
            ts_code: 股票代码
            
        Returns:
            利润表数据字典
        """
        if self.pro:
            try:
                df = self.pro.income(
                    ts_code=ts_code,
                    fields='ts_code,end_date,revenue,operate_profit,total_profit,n_income'
                )
                if not df.empty and len(df) >= 2:
                    current = df.iloc[0]
                    previous = df.iloc[1]
                    
                    revenue_growth = 0
                    profit_growth = 0
                    
                    if previous.get('revenue') and previous['revenue'] != 0:
                        revenue_growth = ((current.get('revenue', 0) or 0) - (previous.get('revenue', 0) or 0)) / (previous.get('revenue', 0) or 1) * 100
                    
                    if previous.get('n_income') and previous['n_income'] != 0:
                        profit_growth = ((current.get('n_income', 0) or 0) - (previous.get('n_income', 0) or 0)) / (previous.get('n_income', 0) or 1) * 100
                    
                    return {
                        "ts_code": ts_code,
                        "end_date": current.get('end_date', ''),
                        "revenue": float(current.get('revenue', 0) or 0),
                        "operate_profit": float(current.get('operate_profit', 0) or 0),
                        "total_profit": float(current.get('total_profit', 0) or 0),
                        "net_income": float(current.get('n_income', 0) or 0),
                        "revenue_growth": round(revenue_growth, 2),
                        "profit_growth": round(profit_growth, 2)
                    }
            except Exception as e:
                print(f"获取利润表数据失败: {e}")
        
        # 返回模拟数据
        import random
        return {
            "ts_code": ts_code,
            "end_date": datetime.now().strftime('%Y%m%d'),
            "revenue": round(random.uniform(1000000, 10000000), 2),
            "operate_profit": round(random.uniform(100000, 1000000), 2),
            "total_profit": round(random.uniform(100000, 1000000), 2),
            "net_income": round(random.uniform(50000, 500000), 2),
            "revenue_growth": round(random.uniform(-20, 50), 2),
            "profit_growth": round(random.uniform(-30, 60), 2)
        }
    
    def _calculate_ema(self, prices: List[float], period: int) -> float:
        """计算EMA"""
        if len(prices) < period:
            return prices[-1] if prices else 0
        
        multiplier = 2 / (period + 1)
        ema = sum(prices[:period]) / period
        
        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema
        
        return ema
    
    def _calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """计算RSI"""
        if len(prices) < period + 1:
            return 50
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def _mock_technical_indicators(self) -> Dict:
        """返回模拟的技术指标"""
        import random
        return {
            "ts_code": "000000.XX",
            "current_price": 100.0,
            "ma5": 99.5,
            "ma10": 98.0,
            "ma20": 97.0,
            "ma60": 95.0,
            "ma_signal": "金叉",
            "macd": 0.5,
            "macd_signal": "多头",
            "rsi": 55,
            "rsi_signal": "中性",
            "trend": "震荡",
            "support": 95.0,
            "resistance": 105.0,
            "technical_score": 60
        }
