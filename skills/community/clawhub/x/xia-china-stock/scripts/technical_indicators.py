#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多数据源技术指标分析器 - Multi-Source Technical Indicators Analyzer
支持: 妙想API、东方财富、Akshare、智谱搜索、Tavily搜索
使用统一数据源管理器实现自动 fallback
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("请安装依赖: pip install pandas numpy")
    sys.exit(1)

# 导入统一数据源管理器
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from data_source_manager import DataSourceManager
    DATA_SOURCE_MANAGER_AVAILABLE = True
except ImportError:
    print("⚠️ 统一数据源管理器导入失败，使用本地数据源")
    DATA_SOURCE_MANAGER_AVAILABLE = False


# 本地DataSource基类（用于向后兼容）
class DataSource:
    """数据源基类（向后兼容）"""

    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        raise NotImplementedError


class YahooFinanceSource(DataSource):
    """Yahoo Finance数据源"""
    
    def __init__(self):
        try:
            import yfinance as yf
            self.yf = yf
        except ImportError:
            self.yf = None
    
    def is_available(self) -> bool:
        return self.yf is not None
    
    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        if not self.yf:
            return None
        
        try:
            ticker = self.yf.Ticker(symbol)
            df = ticker.history(period=period)
            
            if df.empty:
                return None
            
            # 标准化列名
            df = df.rename(columns={
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            })
            
            return df[['open', 'high', 'low', 'close', 'volume']]
        except Exception as e:
            print(f"Yahoo Finance获取失败: {e}")
            return None


class EastMoneySource(DataSource):
    """东方财富数据源（优先使用，带重试机制）"""
    
    def __init__(self):
        self.session = None
    
    def is_available(self) -> bool:
        try:
            import requests
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
            self.requests = requests
            self.HTTPAdapter = HTTPAdapter
            self.Retry = Retry
            return True
        except ImportError:
            return False
    
    def _create_session(self):
        """创建带重试机制的session"""
        session = self.requests.Session()
        retry = self.Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = self.HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def _convert_symbol(self, symbol: str) -> tuple:
        """
        转换股票代码为东方财富格式
        002475 -> ('0', '002475')  # 深市
        600000 -> ('1', '600000')  # 沪市
        """
        symbol = symbol.replace('.SZ', '').replace('.SH', '').replace('.SS', '')
        
        if symbol.startswith(('6', '9', '5')):
            return ('1', symbol)  # 沪市
        else:
            return ('0', symbol)  # 深市
    
    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        if not hasattr(self, 'requests'):
            return None
        
        session = self._create_session()
        
        try:
            market, code = self._convert_symbol(symbol)
            
            # 计算日期范围
            end_date = datetime.now()
            period_map = {
                '1mo': 30, '3mo': 90, '6mo': 180, '1y': 365
            }
            days = period_map.get(period, 180)
            start_date = end_date - timedelta(days=days)
            
            # 使用更稳定的东方财富接口
            url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
            params = {
                'secid': f'{market}.{code}',
                'fields1': 'f1,f2,f3,f4,f5,f6',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                'klt': '101',  # 日K
                'fqt': '1',    # 前复权
                'beg': start_date.strftime('%Y%m%d'),
                'end': end_date.strftime('%Y%m%d'),
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://quote.eastmoney.com/'
            }
            
            resp = session.get(url, params=params, headers=headers, timeout=15)
            data = resp.json()
            
            if data.get('data') and data['data'].get('klines'):
                klines = data['data']['klines']
                
                records = []
                for line in klines:
                    parts = line.split(',')
                    records.append({
                        'date': parts[0],
                        'open': float(parts[1]),
                        'close': float(parts[2]),
                        'high': float(parts[3]),
                        'low': float(parts[4]),
                        'volume': float(parts[5]),
                        'amount': float(parts[6])
                    })
                
                df = pd.DataFrame(records)
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date')
                
                return df[['open', 'high', 'low', 'close', 'volume']]
            
            return None
            
        except Exception as e:
            print(f"东方财富获取失败: {e}")
            return None
        finally:
            session.close()


class AkshareSource(DataSource):
    """Akshare数据源（国内A股优化，带重试机制）"""
    
    def __init__(self):
        self.ak = None
    
    def is_available(self) -> bool:
        try:
            import akshare as ak
            self.ak = ak
            return True
        except ImportError:
            return False
    
    def _convert_symbol(self, symbol: str) -> str:
        """转换股票代码"""
        return symbol.replace('.SZ', '').replace('.SH', '').replace('.SS', '')
    
    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        if not self.ak:
            return None
        
        code = self._convert_symbol(symbol)
        
        # 尝试多个akshare接口
        methods = [
            self._fetch_via_em_hist,
            self._fetch_via_sina,
        ]
        
        for method in methods:
            try:
                df = method(code, period)
                if df is not None and not df.empty:
                    return df
            except Exception:
                continue
        
        return None
    
    def _fetch_via_em_hist(self, code: str, period: str) -> Optional[pd.DataFrame]:
        """通过东方财富历史数据接口"""
        import time
        
        # 日期范围
        period_days = {'1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}
        days = period_days.get(period, 180)
        
        # 重试机制
        for attempt in range(3):
            try:
                df = self.ak.stock_zh_a_hist(
                    symbol=code,
                    period="daily",
                    adjust="qfq",
                    start_date=(datetime.now() - timedelta(days=days*2)).strftime('%Y%m%d'),
                    end_date=datetime.now().strftime('%Y%m%d')
                )
                
                if df is not None and not df.empty:
                    # 筛选日期范围
                    cutoff = datetime.now() - timedelta(days=days)
                    df['日期'] = pd.to_datetime(df['日期'])
                    df = df[df['日期'] >= cutoff]
                    df = df.set_index('日期')
                    
                    # 标准化列名
                    df = df.rename(columns={
                        '开盘': 'open',
                        '收盘': 'close',
                        '最高': 'high',
                        '最低': 'low',
                        '成交量': 'volume'
                    })
                    
                    return df[['open', 'high', 'low', 'close', 'volume']]
                    
            except Exception as e:
                if attempt < 2:
                    time.sleep(0.5)
                    continue
                print(f"Akshare东方财富接口失败: {e}")
        
        return None
    
    def _fetch_via_sina(self, code: str, period: str) -> Optional[pd.DataFrame]:
        """通过新浪接口（备用）"""
        try:
            df = self.ak.stock_zh_a_daily(symbol=f"sh{code}" if code.startswith('6') else f"sz{code}", adjust="qfq")
            
            if df is not None and not df.empty:
                period_days = {'1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}
                days = period_days.get(period, 180)
                cutoff = datetime.now() - timedelta(days=days)
                
                df = df.reset_index()
                # 新浪接口日期列可能叫 'date' 或 '日期'
                date_col = 'date' if 'date' in df.columns else '日期'
                df[date_col] = pd.to_datetime(df[date_col])
                df = df[df[date_col] >= cutoff]
                df = df.set_index(date_col)
                
                return df[['open', 'high', 'low', 'close', 'volume']]
        except Exception as e:
            print(f"Akshare新浪接口失败: {e}")
        
        return None


class EfinanceSource(DataSource):
    """Efinance数据源（东方财富稳定接口）"""
    
    def __init__(self):
        self.ef = None
    
    def is_available(self) -> bool:
        try:
            import efinance as ef
            self.ef = ef
            return True
        except ImportError:
            return False
    
    def _convert_symbol(self, symbol: str) -> str:
        """转换股票代码"""
        return symbol.replace('.SZ', '').replace('.SH', '').replace('.SS', '')
    
    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        if not self.ef:
            return None
        
        try:
            code = self._convert_symbol(symbol)
            
            # 计算日期范围
            period_days = {'1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}
            days = period_days.get(period, 180)
            
            # 使用efinance获取日K数据
            df = self.ef.stock.get_quote_history(
                code,
                beg=(datetime.now() - timedelta(days=days*2)).strftime('%Y%m%d'),
                end=datetime.now().strftime('%Y%m%d'),
                klt=101,  # 日K
                fqt=1    # 前复权
            )
            
            if df is not None and not df.empty:
                # 筛选日期范围
                cutoff = datetime.now() - timedelta(days=days)
                df['日期'] = pd.to_datetime(df['日期'])
                df = df[df['日期'] >= cutoff]
                df = df.set_index('日期')
                
                # 标准化列名
                df = df.rename(columns={
                    '开盘': 'open',
                    '收盘': 'close',
                    '最高': 'high',
                    '最低': 'low',
                    '成交量': 'volume'
                })
                
                return df[['open', 'high', 'low', 'close', 'volume']]
            
            return None
            
        except Exception as e:
            print(f"Efinance获取失败: {e}")
            return None


class TechnicalAnalyzer:
    """技术指标分析器 - 支持多数据源（使用统一数据源管理器）"""
    
    def __init__(self, symbol: str, period: str = "6mo", source: str = "auto"):
        self.symbol = symbol
        self.period = period
        self.df = None
        self.indicators = {}
        self.signals = []
        self.source_name = None
        
        # 使用统一数据源管理器
        if DATA_SOURCE_MANAGER_AVAILABLE:
            self.source_manager = DataSourceManager()
            self.use_manager = True
        else:
            # 回退到本地数据源
            self.sources = []
            self._init_local_sources()
            self.use_manager = False
    
    def _init_local_sources(self):
        """初始化本地数据源（回退方案）"""
        # 1. 优先使用东方财富（国内A股专用）
        em = EastMoneySource()
        if em.is_available():
            self.sources.append(('东方财富', em))
        
        # 2. Efinance（东方财富稳定接口）
        ef = EfinanceSource()
        if ef.is_available():
            self.sources.append(('Efinance', ef))
        
        # 3. Akshare（聚合多数据源）
        ak = AkshareSource()
        if ak.is_available():
            self.sources.append(('Akshare', ak))
        
        # 4. 最后使用 Yahoo Finance
        yf = YahooFinanceSource()
        if yf.is_available():
            self.sources.append(('Yahoo Finance', yf))
    
    def fetch_data(self):
        """获取历史数据（使用统一数据源管理器或本地数据源）"""
        if self.use_manager:
            # 使用统一数据源管理器
            df, source_name = self.source_manager.fetch_with_fallback(self.symbol, self.period)
            if df is not None and not df.empty:
                self.df = df
                self.source_name = source_name
                return True
            return False
        else:
            # 使用本地数据源（回退方案）
            for name, source in self.sources:
                df = source.fetch(self.symbol, self.period)
                if df is not None and not df.empty:
                    self.df = df
                    self.source_name = name
                    print(f"数据来源: {name}")
                    return True
            
            print("所有数据源均获取失败")
            return False
    
    def calculate_ma(self):
        """计算移动平均线 MA"""
        close = self.df['close']
        
        # 常用均线
        ma_periods = [5, 10, 20, 60, 120, 250]
        
        for period in ma_periods:
            if len(close) >= period:
                self.df[f'MA{period}'] = close.rolling(window=period).mean()
        
        # EMA
        self.df['EMA12'] = close.ewm(span=12, adjust=False).mean()
        self.df['EMA26'] = close.ewm(span=26, adjust=False).mean()
        
        # 当前价格
        current_price = close.iloc[-1]
        
        # 均线关系判断
        ma_status = {}
        for period in [5, 10, 20, 60]:
            col = f'MA{period}'
            if col in self.df.columns:
                ma_val = self.df[col].iloc[-1]
                ma_status[f'MA{period}'] = {
                    'value': round(ma_val, 2),
                    'position': '上方' if current_price > ma_val else '下方',
                    'distance': round((current_price - ma_val) / ma_val * 100, 2)
                }
        
        self.indicators['MA'] = {
            'current_price': round(current_price, 2),
            'status': ma_status
        }
        
        # 均线排列信号
        if all([f'MA{p}' in self.df.columns for p in [5, 10, 20]]):
            ma5 = self.df['MA5'].iloc[-1]
            ma10 = self.df['MA10'].iloc[-1]
            ma20 = self.df['MA20'].iloc[-1]
            
            if ma5 > ma10 > ma20:
                self.signals.append(('MA多头排列', '看涨', '🟢'))
            elif ma5 < ma10 < ma20:
                self.signals.append(('MA空头排列', '看跌', '🔴'))
        
        return self.indicators['MA']
    
    def calculate_macd(self):
        """计算 MACD"""
        close = self.df['close']
        
        # MACD参数: 12, 26, 9
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        
        dif = ema12 - ema26
        dea = dif.ewm(span=9, adjust=False).mean()
        macd = (dif - dea) * 2
        
        self.df['DIF'] = dif
        self.df['DEA'] = dea
        self.df['MACD'] = macd
        
        # 当前值
        current_dif = dif.iloc[-1]
        current_dea = dea.iloc[-1]
        current_macd = macd.iloc[-1]
        
        # 前一日值
        prev_dif = dif.iloc[-2] if len(dif) > 1 else current_dif
        prev_dea = dea.iloc[-2] if len(dea) > 1 else current_dea
        
        self.indicators['MACD'] = {
            'DIF': round(current_dif, 4),
            'DEA': round(current_dea, 4),
            'MACD': round(current_macd, 4)
        }
        
        # 信号判断
        if current_dif > current_dea and prev_dif <= prev_dea:
            self.signals.append(('MACD金叉', '买入信号', '🟢'))
        elif current_dif < current_dea and prev_dif >= prev_dea:
            self.signals.append(('MACD死叉', '卖出信号', '🔴'))
        elif current_macd > 0:
            self.signals.append(('MACD多头', '偏多', '🟡'))
        else:
            self.signals.append(('MACD空头', '偏空', '🟠'))
        
        return self.indicators['MACD']
    
    def calculate_rsi(self):
        """计算 RSI"""
        close = self.df['close']
        delta = close.diff()
        
        # 多个周期RSI
        rsi_periods = [6, 14, 24]
        rsi_values = {}
        
        for period in rsi_periods:
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            col = f'RSI{period}'
            self.df[col] = rsi
            rsi_values[f'RSI{period}'] = round(rsi.iloc[-1], 2)
        
        self.indicators['RSI'] = rsi_values
        
        # RSI信号
        rsi14 = rsi_values['RSI14']
        
        if rsi14 > 80:
            self.signals.append(('RSI超买', '严重超买', '🔴'))
        elif rsi14 > 70:
            self.signals.append(('RSI偏强', '超买区间', '🟠'))
        elif rsi14 < 20:
            self.signals.append(('RSI超卖', '严重超卖', '🟢'))
        elif rsi14 < 30:
            self.signals.append(('RSI偏弱', '超卖区间', '🟡'))
        else:
            self.signals.append(('RSI中性', '正常区间', '⚪'))
        
        return rsi_values
    
    def calculate_kdj(self):
        """计算 KDJ"""
        low = self.df['low']
        high = self.df['high']
        close = self.df['close']
        
        # 9日KDJ
        n = 9
        low_n = low.rolling(window=n).min()
        high_n = high.rolling(window=n).max()
        
        rsv = (close - low_n) / (high_n - low_n) * 100
        rsv = rsv.fillna(50)
        
        # K, D, J
        k = rsv.ewm(com=2, adjust=False).mean()
        d = k.ewm(com=2, adjust=False).mean()
        j = 3 * k - 2 * d
        
        self.df['K'] = k
        self.df['D'] = d
        self.df['J'] = j
        
        current_k = k.iloc[-1]
        current_d = d.iloc[-1]
        current_j = j.iloc[-1]
        
        prev_k = k.iloc[-2] if len(k) > 1 else current_k
        prev_d = d.iloc[-2] if len(d) > 1 else current_d
        
        self.indicators['KDJ'] = {
            'K': round(current_k, 2),
            'D': round(current_d, 2),
            'J': round(current_j, 2)
        }
        
        # KDJ信号
        if current_k > current_d and prev_k <= prev_d:
            self.signals.append(('KDJ金叉', '买入信号', '🟢'))
        elif current_k < current_d and prev_k >= prev_d:
            self.signals.append(('KDJ死叉', '卖出信号', '🔴'))
        
        if current_j > 100:
            self.signals.append(('J值超买', 'J>100', '🔴'))
        elif current_j < 0:
            self.signals.append(('J值超卖', 'J<0', '🟢'))
        
        return self.indicators['KDJ']
    
    def calculate_bollinger(self):
        """计算布林带"""
        close = self.df['close']
        
        # 20日均线 + 2倍标准差
        period = 20
        std_dev = 2
        
        mid = close.rolling(window=period).mean()
        std = close.rolling(window=period).std()
        
        upper = mid + std_dev * std
        lower = mid - std_dev * std
        
        self.df['BOLL_MID'] = mid
        self.df['BOLL_UPPER'] = upper
        self.df['BOLL_LOWER'] = lower
        
        current_price = close.iloc[-1]
        current_mid = mid.iloc[-1]
        current_upper = upper.iloc[-1]
        current_lower = lower.iloc[-1]
        
        # 布林带宽度
        bandwidth = (current_upper - current_lower) / current_mid * 100 if current_mid > 0 else 0
        
        # 价格位置 (0=下轨, 100=上轨)
        price_position = (current_price - current_lower) / (current_upper - current_lower) * 100
        
        self.indicators['BOLL'] = {
            'upper': round(current_upper, 2),
            'mid': round(current_mid, 2),
            'lower': round(current_lower, 2),
            'bandwidth': round(bandwidth, 2),
            'price_position': round(price_position, 2)
        }
        
        # 布林带信号
        if current_price >= current_upper:
            self.signals.append(('触及上轨', '强势/压力位', '🟠'))
        elif current_price <= current_lower:
            self.signals.append(('触及下轨', '弱势/支撑位', '🟡'))
        
        if bandwidth < 10:
            self.signals.append(('布林收口', '变盘信号', '⚠️'))
        elif bandwidth > 25:
            self.signals.append(('布林开口', '波动加大', '📊'))
        
        return self.indicators['BOLL']
    
    def calculate_volume_indicators(self):
        """计算成交量指标"""
        close = self.df['close']
        volume = self.df['volume']
        
        # 成交量均线
        vol_ma5 = volume.rolling(window=5).mean()
        vol_ma10 = volume.rolling(window=10).mean()
        
        current_vol = volume.iloc[-1]
        current_vol_ma5 = vol_ma5.iloc[-1]
        current_vol_ma10 = vol_ma10.iloc[-1]
        
        # 量比 (当日成交量/5日均量)
        vol_ratio = current_vol / current_vol_ma5 if current_vol_ma5 > 0 else 1
        
        self.indicators['VOLUME'] = {
            'volume': int(current_vol),
            'vol_ma5': int(current_vol_ma5),
            'vol_ma10': int(current_vol_ma10),
            'vol_ratio': round(vol_ratio, 2)
        }
        
        # 量价关系信号
        if len(close) > 1:
            price_change = (close.iloc[-1] - close.iloc[-2]) / close.iloc[-2] * 100
            
            if price_change > 2 and vol_ratio > 2:
                self.signals.append(('放量上涨', '资金流入', '🟢'))
            elif price_change < -2 and vol_ratio > 2:
                self.signals.append(('放量下跌', '资金流出', '🔴'))
            elif abs(price_change) < 1 and vol_ratio < 0.5:
                self.signals.append(('缩量横盘', '观望', '⚪'))
        
        return self.indicators['VOLUME']
    
    def analyze_trend(self):
        """综合趋势判断"""
        # 统计信号
        bullish = sum(1 for s in self.signals if s[1] in ['看涨', '买入信号', '偏多', '资金流入'])
        bearish = sum(1 for s in self.signals if s[1] in ['看跌', '卖出信号', '偏空', '资金流出'])
        neutral = len(self.signals) - bullish - bearish
        
        # 计算趋势分数 (-100 到 100)
        score = (bullish - bearish) * 15
        score = max(-100, min(100, score))
        
        if score >= 60:
            trend = '强烈看多'
            emoji = '🟢🟢🟢'
        elif score >= 30:
            trend = '偏多'
            emoji = '🟢🟢'
        elif score >= 10:
            trend = '轻微偏多'
            emoji = '🟢'
        elif score <= -60:
            trend = '强烈看空'
            emoji = '🔴🔴🔴'
        elif score <= -30:
            trend = '偏空'
            emoji = '🔴🔴'
        elif score <= -10:
            trend = '轻微偏空'
            emoji = '🔴'
        else:
            trend = '震荡/中性'
            emoji = '⚪'
        
        return {
            'score': score,
            'trend': trend,
            'emoji': emoji,
            'bullish_signals': bullish,
            'bearish_signals': bearish,
            'neutral_signals': neutral
        }
    
    def run_analysis(self):
        """运行完整分析"""
        if not self.fetch_data():
            return None
        
        # 计算所有指标
        self.calculate_ma()
        self.calculate_macd()
        self.calculate_rsi()
        self.calculate_kdj()
        self.calculate_bollinger()
        self.calculate_volume_indicators()
        
        # 综合趋势
        trend = self.analyze_trend()
        
        return {
            'symbol': self.symbol,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'source': self.source_name,
            'price': self.indicators['MA']['current_price'],
            'indicators': self.indicators,
            'signals': self.signals,
            'trend': trend
        }
    
    def generate_report(self, format: str = 'markdown') -> str:
        """生成分析报告"""
        result = self.run_analysis()
        if not result:
            return "分析失败"
        
        if format == 'json':
            return json.dumps(result, ensure_ascii=False, indent=2)
        
        # Markdown格式
        md = f"""# {result['symbol']} 技术指标分析

**日期**: {result['date']}  
**当前价格**: {result['price']}  
**数据来源**: {result['source']}

---

## 📊 均线系统 (MA)

| 均线 | 数值 | 位置 | 距离 |
|------|------|------|------|
"""
        ma_data = result['indicators']['MA']['status']
        for ma, data in ma_data.items():
            md += f"| {ma} | {data['value']} | {data['position']} | {data['distance']:+.2f}% |\n"
        
        md += f"""
---

## 📈 MACD

| 指标 | 数值 |
|------|------|
| DIF | {result['indicators']['MACD']['DIF']} |
| DEA | {result['indicators']['MACD']['DEA']} |
| MACD柱 | {result['indicators']['MACD']['MACD']} |

---

## 📉 RSI

| 周期 | 数值 | 状态 |
|------|------|------|
| RSI(6) | {result['indicators']['RSI']['RSI6']} | {'超买' if result['indicators']['RSI']['RSI6'] > 70 else '超卖' if result['indicators']['RSI']['RSI6'] < 30 else '正常'} |
| RSI(14) | {result['indicators']['RSI']['RSI14']} | {'超买' if result['indicators']['RSI']['RSI14'] > 70 else '超卖' if result['indicators']['RSI']['RSI14'] < 30 else '正常'} |
| RSI(24) | {result['indicators']['RSI']['RSI24']} | {'超买' if result['indicators']['RSI']['RSI24'] > 70 else '超卖' if result['indicators']['RSI']['RSI24'] < 30 else '正常'} |

---

## 🎯 KDJ

| 指标 | 数值 |
|------|------|
| K | {result['indicators']['KDJ']['K']} |
| D | {result['indicators']['KDJ']['D']} |
| J | {result['indicators']['KDJ']['J']} |

---

## 📐 布林带 (BOLL)

| 指标 | 数值 |
|------|------|
| 上轨 | {result['indicators']['BOLL']['upper']} |
| 中轨 | {result['indicators']['BOLL']['mid']} |
| 下轨 | {result['indicators']['BOLL']['lower']} |
| 带宽 | {result['indicators']['BOLL']['bandwidth']}% |
| 价格位置 | {result['indicators']['BOLL']['price_position']}% |

---

## 📊 成交量

| 指标 | 数值 |
|------|------|
| 当日成交量 | {result['indicators']['VOLUME']['volume']:,} |
| 5日均量 | {result['indicators']['VOLUME']['vol_ma5']:,} |
| 量比 | {result['indicators']['VOLUME']['vol_ratio']} |

---

## 🚨 信号汇总

| 信号 | 判断 | 标记 |
|------|------|------|
"""
        for signal in result['signals']:
            md += f"| {signal[0]} | {signal[1]} | {signal[2]} |\n"
        
        trend = result['trend']
        md += f"""
---

## 🎯 综合判断

**趋势分数**: {trend['score']}  
**趋势方向**: {trend['emoji']} {trend['trend']}

- 看多信号: {trend['bullish_signals']} 个
- 看空信号: {trend['bearish_signals']} 个
- 中性信号: {trend['neutral_signals']} 个

---

*⚠️ 以上分析仅供参考，不构成投资建议*
"""
        
        return md


def main():
    parser = argparse.ArgumentParser(description='多数据源技术指标分析器')
    parser.add_argument('symbol', help='股票代码 (如 002475, 600000, AAPL)')
    parser.add_argument('--period', default='6mo', help='数据周期 (1mo, 3mo, 6mo, 1y)')
    parser.add_argument('--source', default='auto', 
                        choices=['auto', 'eastmoney', 'akshare', 'yahoo'],
                        help='数据源选择')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='输出格式')
    parser.add_argument('--output', help='输出文件路径')
    
    args = parser.parse_args()
    
    analyzer = TechnicalAnalyzer(args.symbol, args.period, args.source)
    report = analyzer.generate_report(args.format)
    
    if args.output:
        Path(args.output).write_text(report, encoding='utf-8')
        print(f"报告已保存到: {args.output}")
    else:
        print(report)


if __name__ == '__main__':
    main()
