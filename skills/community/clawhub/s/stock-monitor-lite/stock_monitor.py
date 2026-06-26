#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票监控预警技能 V1.0
功能：实时监控 + 智能预警 + 深度分析
数据源：新浪财经API + 东方财富API
"""

import sys
import json
import logging
from datetime import datetime
import requests
import time
import pandas as pd

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 确保UTF-8输出
sys.stdout.reconfigure(encoding='utf-8')

# 新浪财经API
SINA_BASE_URL = "http://hq.sinajs.cn"

# 标的类型定义
STOCK_TYPE = {
    "INDIVIDUAL": "individual",  # 个股
    "ETF": "etf",                # ETF
    "GOLD": "gold"               # 黄金/贵金属
}

# 从配置文件读取监控列表
def load_watchlist():
    """从配置文件读取监控列表"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config.get('config', {}).get('watchlist', [])
    except Exception as e:
        logging.error(f"读取配置文件失败: {e}")
        # 返回默认监控列表
        return [
            {
                "code": "002050", 
                "name": "三花智控", 
                "market": "sz",
                "type": "individual",
                "cost": 48.59,
                "alerts": {
                    "cost_pct_above": 15.0,    # 盈利15%
                    "cost_pct_below": -12.0,   # 止损12%
                    "change_pct_above": 4.0,   # 日内异动 ±4%
                    "change_pct_below": -4.0,
                    "volume_surge": 2.0,       # 成交量是5日均量2倍
                    "ma_monitor": True,        # 均线金叉死叉
                    "rsi_monitor": True,       # RSI超买超卖
                    "gap_monitor": True,       # 跳空缺口
                    "trailing_stop": True      # 动态止盈
                }
            },
            {
                "code": "002196", 
                "name": "方正电机", 
                "market": "sz",
                "type": "individual",
                "cost": 14.97,
                "alerts": {
                    "cost_pct_above": 15.0,
                    "cost_pct_below": -12.0,
                    "change_pct_above": 4.0,
                    "change_pct_below": -4.0,
                    "volume_surge": 2.0,       # 成交量是5日均量2倍
                    "ma_monitor": True,        # 均线金叉死叉
                    "rsi_monitor": True,       # RSI超买超卖
                    "gap_monitor": True,       # 跳空缺口
                    "trailing_stop": True      # 动态止盈
                }
            },
            {
                "code": "002896", 
                "name": "中大力德", 
                "market": "sz",
                "type": "individual",
                "cost": 81.26,
                "alerts": {
                    "cost_pct_above": 15.0,
                    "cost_pct_below": -12.0,
                    "change_pct_above": 4.0,
                    "change_pct_below": -4.0,
                    "volume_surge": 2.0,       # 成交量是5日均量2倍
                    "ma_monitor": True,        # 均线金叉死叉
                    "rsi_monitor": True,       # RSI超买超卖
                    "gap_monitor": True,       # 跳空缺口
                    "trailing_stop": True      # 动态止盈
                }
            },
            {
                "code": "600126", 
                "name": "杭钢股份", 
                "market": "sh",
                "type": "individual",
                "cost": 9.26,
                "alerts": {
                    "cost_pct_above": 15.0,
                    "cost_pct_below": -12.0,
                    "change_pct_above": 4.0,
                    "change_pct_below": -4.0,
                    "volume_surge": 2.0,       # 成交量是5日均量2倍
                    "ma_monitor": True,        # 均线金叉死叉
                    "rsi_monitor": True,       # RSI超买超卖
                    "gap_monitor": True,       # 跳空缺口
                    "trailing_stop": True      # 动态止盈
                }
            },
            {
                "code": "600410", 
                "name": "华胜天成", 
                "market": "sh",
                "type": "individual",
                "cost": 31.44,
                "alerts": {
                    "cost_pct_above": 15.0,
                    "cost_pct_below": -12.0,
                    "change_pct_above": 4.0,
                    "change_pct_below": -4.0,
                    "volume_surge": 2.0,       # 成交量是5日均量2倍
                    "ma_monitor": True,        # 均线金叉死叉
                    "rsi_monitor": True,       # RSI超买超卖
                    "gap_monitor": True,       # 跳空缺口
                    "trailing_stop": True      # 动态止盈
                }
            }
        ]

# 加载监控列表
WATCHLIST = load_watchlist()

class DataCache:
    """数据缓存类"""
    def __init__(self, max_age=300):  # 5分钟缓存
        self.cache = {}
        self.max_age = max_age
    
    def get(self, key):
        """获取缓存数据"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.max_age:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key, data):
        """设置缓存数据"""
        self.cache[key] = (data, time.time())
    
    def clear(self):
        """清空缓存"""
        self.cache.clear()

# 创建全局缓存实例
data_cache = DataCache()

class StockAlert:
    def __init__(self):
        self.prev_data = {}
        self.alert_log = []
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0"})
        self.data_cache = data_cache
        
    def fetch_eastmoney_kline(self, symbol, market, lmt=2):
        """获取最新日K线数据 (收盘后也能获取收盘价)"""
        # 尝试从缓存获取
        cache_key = f"kline_{symbol}_{market}_{lmt}"
        cached_data = self.data_cache.get(cache_key)
        if cached_data:
            return cached_data
        
        secid = f"{market}.{symbol}"
        url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        params = {
            'secid': secid,
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'klt': '101',  # 日线
            'fqt': '0',
            'end': '20500101',
            'lmt': str(lmt)  # 取最近n天
        }
        try:
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()
            klines = data.get('data', {}).get('klines', [])
            if len(klines) >= 1:
                # 格式: 日期,开盘,收盘,最高,最低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率
                today = klines[-1].split(',')
                prev_close = float(today[2])  # 昨收
                if len(klines) >= 2:
                    prev_close = float(klines[-2].split(',')[2])  # 前一天收盘
                result = {
                    'name': data.get('data', {}).get('name', symbol),
                    'price': float(today[2]),      # 收盘
                    'prev_close': prev_close,
                    'volume': int(float(today[5])),
                    'amount': float(today[6]),
                    'date': today[0],
                    'time': '15:00:00',
                    'klines': klines  # 保存原始K线数据供技术指标计算
                }
                # 缓存结果
                self.data_cache.set(cache_key, result)
                return result
        except Exception as e:
            logging.error(f"东财K线获取失败 {symbol}: {e}")
        return None
    
    def calculate_macd(self, klines, fast_period=12, slow_period=26, signal_period=9):
        """计算MACD指标"""
        if not klines or len(klines) < slow_period + signal_period:
            return None
        
        # 提取收盘价
        closes = []
        for k in klines:
            p = k.split(',')
            if len(p) >= 3:
                closes.append(float(p[2]))
        
        if len(closes) < slow_period + signal_period:
            return None
        
        # 计算EMA
        ema_fast = pd.Series(closes).ewm(span=fast_period, adjust=False).mean()
        ema_slow = pd.Series(closes).ewm(span=slow_period, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        histogram = macd_line - signal_line
        
        return {
            'macd_line': macd_line.iloc[-1],
            'signal_line': signal_line.iloc[-1],
            'histogram': histogram.iloc[-1],
            'macd_crossover': macd_line.iloc[-1] > signal_line.iloc[-1] and macd_line.iloc[-2] <= signal_line.iloc[-2],
            'macd_crossunder': macd_line.iloc[-1] < signal_line.iloc[-1] and macd_line.iloc[-2] >= signal_line.iloc[-2]
        }
    
    def calculate_bollinger_bands(self, klines, period=20, std_dev=2):
        """计算布林带"""
        if not klines or len(klines) < period:
            return None
        
        # 提取收盘价
        closes = []
        for k in klines:
            p = k.split(',')
            if len(p) >= 3:
                closes.append(float(p[2]))
        
        if len(closes) < period:
            return None
        
        # 计算布林带
        rolling_mean = pd.Series(closes).rolling(window=period).mean()
        rolling_std = pd.Series(closes).rolling(window=period).std()
        upper_band = rolling_mean + (rolling_std * std_dev)
        lower_band = rolling_mean - (rolling_std * std_dev)
        
        return {
            'upper_band': upper_band.iloc[-1],
            'middle_band': rolling_mean.iloc[-1],
            'lower_band': lower_band.iloc[-1],
            'price_position': (closes[-1] - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1]) if (upper_band.iloc[-1] - lower_band.iloc[-1]) > 0 else 0.5
        }
    
    def calculate_atr(self, klines, period=14):
        """计算平均真实波动范围(ATR)"""
        if not klines or len(klines) < period:
            return None
        
        # 提取高低收盘价
        highs = []
        lows = []
        closes = []
        for k in klines:
            p = k.split(',')
            if len(p) >= 5:
                highs.append(float(p[3]))  # 最高
                lows.append(float(p[4]))   # 最低
                closes.append(float(p[2])) # 收盘
        
        if len(highs) < period:
            return None
        
        # 计算真实波动范围
        tr = []
        for i in range(1, len(highs)):
            true_range = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
            tr.append(true_range)
        
        # 计算ATR
        atr = pd.Series(tr).rolling(window=period).mean().iloc[-1]
        
        return {'atr': atr}
    
    def calculate_obv(self, klines):
        """计算能量潮指标(OBV)"""
        if not klines or len(klines) < 2:
            return None
        
        # 提取收盘价和成交量
        closes = []
        volumes = []
        for k in klines:
            p = k.split(',')
            if len(p) >= 6:
                closes.append(float(p[2])) # 收盘
                volumes.append(float(p[5])) # 成交量
        
        if len(closes) < 2:
            return None
        
        # 计算OBV
        obv = [0]
        for i in range(1, len(closes)):
            if closes[i] > closes[i-1]:
                obv.append(obv[-1] + volumes[i])
            elif closes[i] < closes[i-1]:
                obv.append(obv[-1] - volumes[i])
            else:
                obv.append(obv[-1])
        
        return {'obv': obv[-1], 'obv_change': obv[-1] - obv[-2] if len(obv) > 1 else 0}

    def fetch_volume_ma5(self, symbol, market):
        """获取5日平均成交量"""
        # 尝试从缓存获取
        cache_key = f"volume_ma5_{symbol}_{market}"
        cached_data = self.data_cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # 使用 fetch_eastmoney_kline 获取数据
        kline_data = self.fetch_eastmoney_kline(symbol, market, lmt=6)
        if kline_data and 'klines' in kline_data:
            klines = kline_data['klines']
            if len(klines) >= 2:
                # 计算前5日平均成交量(不含今天)
                volumes = []
                for k in klines[:-1]:  # 排除最后一天(今天)
                    p = k.split(',')
                    if len(p) >= 6:
                        volumes.append(float(p[5]))  # 成交量
                result = sum(volumes) / len(volumes) if volumes else 0
                # 缓存结果
                self.data_cache.set(cache_key, result)
                return result
        return 0

    def fetch_ma_data(self, symbol, market):
        """获取均线数据 (MA5, MA10, MA20) 和 RSI"""
        # 尝试从缓存获取
        cache_key = f"ma_data_{symbol}_{market}"
        cached_data = self.data_cache.get(cache_key)
        if cached_data:
            return cached_data
        
        # 使用 fetch_eastmoney_kline 获取数据
        kline_data = self.fetch_eastmoney_kline(symbol, market, lmt=30)
        if kline_data and 'klines' in kline_data:
            klines = kline_data['klines']
            if len(klines) >= 20:
                closes = []
                for k in klines:
                    p = k.split(',')
                    if len(p) >= 3:
                        closes.append(float(p[2]))  # 收盘价
                
                if len(closes) >= 20:
                    # 计算均线
                    ma5 = sum(closes[-5:]) / 5
                    ma10 = sum(closes[-10:]) / 10
                    ma20 = sum(closes[-20:]) / 20
                    
                    # 判断均线趋势
                    prev_ma5 = sum(closes[-6:-1]) / 5
                    prev_ma10 = sum(closes[-11:-1]) / 10
                    
                    # 计算RSI(14)
                    rsi = self._calculate_rsi(closes, 14)
                    
                    result = {
                        'MA5': ma5,
                        'MA10': ma10,
                        'MA20': ma20,
                        'MA5_trend': 'up' if ma5 > prev_ma5 else 'down',
                        'MA10_trend': 'up' if ma10 > prev_ma10 else 'down',
                        'golden_cross': prev_ma5 <= prev_ma10 and ma5 > ma10,
                        'death_cross': prev_ma5 >= prev_ma10 and ma5 < ma10,
                        'RSI': rsi,
                        'RSI_overbought': rsi > 70 if rsi else False,
                        'RSI_oversold': rsi < 30 if rsi else False
                    }
                    # 缓存结果
                    self.data_cache.set(cache_key, result)
                    return result
        return None
    
    def _calculate_rsi(self, closes, period=14):
        """计算RSI指标"""
        if len(closes) < period + 1:
            return None
        
        gains = []
        losses = []
        
        for i in range(1, period + 1):
            change = closes[-i] - closes[-i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return round(rsi, 2)

    def fetch_sina_realtime(self, stocks):
        """获取实时行情 (优先实时，收盘后用日K)"""
        stock_list = [s for s in stocks if s['market'] != 'fx']
        results = {}
        
        # 1. A股/ETF - 尝试实时接口
        if stock_list:
            codes = [f"{s['market']}{s['code']}" for s in stock_list]
            url = f"https://hq.sinajs.cn/list={','.join(codes)}"
            try:
                resp = self.session.get(url, headers={'Referer': 'https://finance.sina.com.cn'}, timeout=10)
                resp.encoding = 'gb18030'
                for line in resp.text.strip().split(';'):
                    if 'hq_str_' not in line or '=' not in line: continue
                    key = line.split('=')[0].split('_')[-1]
                    if len(key) < 8: continue
                    data_str = line[line.index('"')+1 : line.rindex('"')]
                    p = data_str.split(',')
                    if len(p) > 30 and float(p[3]) > 0:
                        # 新浪数据格式: 名称,今日开盘,昨日收盘,当前价,今日最高,今日最低,竞买价,竞卖价,成交量,成交额...
                        # 保存昨日最高最低价用于跳空检测 (用昨日收盘近似，或用均线数据补充)
                        results[key[2:]] = {
                            'name': p[0], 
                            'price': float(p[3]), 
                            'prev_close': float(p[2]),
                            'open': float(p[1]),      # 今日开盘
                            'high': float(p[4]),      # 今日最高
                            'low': float(p[5]),       # 今日最低
                            'volume': int(p[8]), 
                            'amount': float(p[9]), 
                            'date': p[30], 
                            'time': p[31],
                            'prev_high': float(p[2]) * 1.02,  # 估算昨日最高 (昨收+2%)
                            'prev_low': float(p[2]) * 0.98    # 估算昨日最低 (昨收-2%)
                        }
            except Exception as e: 
                logging.error(f"实时行情获取失败: {e}")
            
            # 2. 如果实时接口返回空或0，用日K线补数据
            for stock in stock_list:
                code = stock['code']
                if code not in results or results[code]['price'] <= 0:
                    kline_data = self.fetch_eastmoney_kline(code, 1 if stock['market'] == 'sh' else 0)
                    if kline_data:
                        results[code] = kline_data
                        logging.info(f"  {stock['name']}: 使用日K收盘价 {kline_data['price']}")

        return results
    
    def check_alerts(self, stock_config, data):
        """检查预警条件 (支持成本百分比、单日涨跌幅、分级预警)"""
        alerts = []
        alert_weights = []  # 用于计算预警级别
        code = stock_config['code']
        cfg = stock_config.get('alerts', {})
        cost = stock_config.get('cost', 0)
        stock_type = stock_config.get('type', 'individual')
        price, prev_close = data['price'], data['prev_close']
        change_pct = (price - prev_close) / prev_close * 100 if prev_close else 0
        
        # 1. 基于成本的百分比预警 (权重: 高)
        if cost > 0:
            cost_change_pct = (price - cost) / cost * 100
            
            if 'cost_pct_above' in cfg and cost_change_pct >= cfg['cost_pct_above']:
                target_price = cost * (1 + cfg['cost_pct_above']/100)
                if not self._alerted_recently(code, 'cost_above'):
                    alerts.append(('cost_above', f"🎯 盈利 {cfg['cost_pct_above']:.0f}% (目标价 ¥{target_price:.2f})"))
                    alert_weights.append(3)  # 高权重
            
            if 'cost_pct_below' in cfg and cost_change_pct <= cfg['cost_pct_below']:
                target_price = cost * (1 + cfg['cost_pct_below']/100)
                if not self._alerted_recently(code, 'cost_below'):
                    alerts.append(('cost_below', f"🛑 亏损 {abs(cfg['cost_pct_below']):.0f}% (止损价 ¥{target_price:.2f})"))
                    alert_weights.append(3)  # 高权重
        
        # 2. 基于固定价格的预警 (权重: 中)
        if 'price_above' in cfg and price >= cfg['price_above'] and not self._alerted_recently(code, 'above'):
            alerts.append(('above', f"🚀 价格突破 ¥{cfg['price_above']}"))
            alert_weights.append(2)
        if 'price_below' in cfg and price <= cfg['price_below'] and not self._alerted_recently(code, 'below'):
            alerts.append(('below', f"📉 价格跌破 ¥{cfg['price_below']}"))
            alert_weights.append(2)
        
        # 3. 单日涨跌幅预警 (权重: 根据幅度)
        if 'change_pct_above' in cfg and change_pct >= cfg['change_pct_above'] and not self._alerted_recently(code, 'pct_up'):
            alerts.append(('pct_up', f"📈 日内大涨 {change_pct:+.2f}%"))
            # 异动越大权重越高
            if change_pct >= 7:
                alert_weights.append(3)  # 涨停附近
            elif change_pct >= 5:
                alert_weights.append(2)  # 大涨
            else:
                alert_weights.append(1)  # 一般异动
                
        if 'change_pct_below' in cfg and change_pct <= cfg['change_pct_below'] and not self._alerted_recently(code, 'pct_down'):
            alerts.append(('pct_down', f"📉 日内大跌 {change_pct:+.2f}%"))
            if change_pct <= -7:
                alert_weights.append(3)  # 跌停附近
            elif change_pct <= -5:
                alert_weights.append(2)  # 大跌
            else:
                alert_weights.append(1)  # 一般异动
        
        # 4. 成交量异动检测 (仅股票和ETF)
        if stock_type != 'gold' and 'volume_surge' in cfg:
            current_volume = data.get('volume', 0)
            if current_volume > 0:
                # 尝试获取5日均量
                ma5_volume = self.fetch_volume_ma5(code, 1 if stock_config['market'] == 'sh' else 0)
                if ma5_volume > 0:
                    volume_ratio = current_volume / ma5_volume
                    threshold = cfg['volume_surge']
                    
                    if volume_ratio >= threshold and not self._alerted_recently(code, 'volume_surge'):
                        alerts.append(('volume_surge', f"📊 放量 {volume_ratio:.1f}倍 (5日均量)"))
                        alert_weights.append(2)  # 中等权重
                    elif volume_ratio <= 0.5 and not self._alerted_recently(code, 'volume_shrink'):
                        alerts.append(('volume_shrink', f"📉 缩量 {volume_ratio:.1f}倍 (5日均量)"))
                        alert_weights.append(1)  # 低权重
        
        # 5. 均线系统 (MA金叉死叉)
        if stock_type != 'gold' and cfg.get('ma_monitor', True):
            ma_data = self.fetch_ma_data(code, 1 if stock_config['market'] == 'sh' else 0)
            if ma_data:
                # 金叉: MA5上穿MA10 (短期转强)
                if ma_data.get('golden_cross') and not self._alerted_recently(code, 'ma_golden'):
                    alerts.append(('ma_golden', f"🌟 均线金叉 (MA5¥{ma_data['MA5']:.2f}上穿MA10¥{ma_data['MA10']:.2f})"))
                    alert_weights.append(3)  # 高权重
                
                # 死叉: MA5下穿MA10 (短期转弱)
                if ma_data.get('death_cross') and not self._alerted_recently(code, 'ma_death'):
                    alerts.append(('ma_death', f"⚠️ 均线死叉 (MA5¥{ma_data['MA5']:.2f}下穿MA10¥{ma_data['MA10']:.2f})"))
                    alert_weights.append(3)  # 高权重
                
                # RSI超买超卖检测
                if cfg.get('rsi_monitor', True):
                    rsi = ma_data.get('RSI')
                    if rsi:
                        if ma_data.get('RSI_overbought') and not self._alerted_recently(code, 'rsi_high'):
                            alerts.append(('rsi_high', f"🔥 RSI超买 ({rsi})，可能回调"))
                            alert_weights.append(2)
                        elif ma_data.get('RSI_oversold') and not self._alerted_recently(code, 'rsi_low'):
                            alerts.append(('rsi_low', f"❄️ RSI超卖 ({rsi})，可能反弹"))
                            alert_weights.append(2)
        
        # 6. 新技术指标预警
        if stock_type != 'gold':
            # 获取K线数据用于技术指标计算
            kline_data = self.fetch_eastmoney_kline(code, 1 if stock_config['market'] == 'sh' else 0, lmt=40)
            if kline_data and 'klines' in kline_data:
                klines = kline_data['klines']
                
                # MACD指标预警
                if cfg.get('macd_monitor', True):
                    macd_data = self.calculate_macd(klines)
                    if macd_data:
                        if macd_data.get('macd_crossover') and not self._alerted_recently(code, 'macd_golden'):
                            alerts.append(('macd_golden', f"📈 MACD金叉 (MACD线¥{macd_data['macd_line']:.2f}上穿信号线¥{macd_data['signal_line']:.2f})"))
                            alert_weights.append(3)  # 高权重
                        elif macd_data.get('macd_crossunder') and not self._alerted_recently(code, 'macd_death'):
                            alerts.append(('macd_death', f"📉 MACD死叉 (MACD线¥{macd_data['macd_line']:.2f}下穿信号线¥{macd_data['signal_line']:.2f})"))
                            alert_weights.append(3)  # 高权重
                
                # 布林带指标预警
                if cfg.get('bollinger_monitor', True):
                    bollinger_data = self.calculate_bollinger_bands(klines)
                    if bollinger_data:
                        if price >= bollinger_data['upper_band'] and not self._alerted_recently(code, 'bollinger_upper'):
                            alerts.append(('bollinger_upper', f"🚨 价格触及布林带上轨 (¥{bollinger_data['upper_band']:.2f})，可能超买"))
                            alert_weights.append(2)  # 中等权重
                        elif price <= bollinger_data['lower_band'] and not self._alerted_recently(code, 'bollinger_lower'):
                            alerts.append(('bollinger_lower', f"❄️ 价格触及布林带下轨 (¥{bollinger_data['lower_band']:.2f})，可能超卖"))
                            alert_weights.append(2)  # 中等权重
                
                # OBV指标预警
                if cfg.get('obv_monitor', True):
                    obv_data = self.calculate_obv(klines)
                    if obv_data:
                        obv_change_pct = (obv_data['obv_change'] / abs(obv_data['obv'])) * 100 if obv_data['obv'] != 0 else 0
                        if abs(obv_change_pct) >= 10 and not self._alerted_recently(code, 'obv_surge'):
                            direction = "放量上涨" if obv_data['obv_change'] > 0 else "放量下跌"
                            alerts.append(('obv_surge', f"📊 OBV指标{direction} ({obv_change_pct:+.1f}%)"))
                            alert_weights.append(2)  # 中等权重
                
                # ATR波动率预警
                if cfg.get('atr_monitor', True):
                    atr_data = self.calculate_atr(klines)
                    if atr_data:
                        # 这里可以根据ATR值设置预警条件，例如ATR突然增大
                        pass
        
        # 7. 跳空缺口检测 (需要昨日数据)
        if stock_type != 'gold' and cfg.get('gap_monitor', True):
            prev_high = data.get('prev_high', 0)
            prev_low = data.get('prev_low', 0)
            current_open = data.get('open', price)  # 当前价近似开盘价
            
            # 向上跳空: 今日开盘 > 昨日最高
            if prev_high > 0 and current_open > prev_high * 1.01:  # 1%以上算跳空
                gap_pct = (current_open - prev_high) / prev_high * 100
                if not self._alerted_recently(code, 'gap_up'):
                    alerts.append(('gap_up', f"⬆️ 向上跳空 {gap_pct:.1f}%"))
                    alert_weights.append(2)
            
            # 向下跳空: 今日开盘 < 昨日最低
            elif prev_low > 0 and current_open < prev_low * 0.99:
                gap_pct = (prev_low - current_open) / prev_low * 100
                if not self._alerted_recently(code, 'gap_down'):
                    alerts.append(('gap_down', f"⬇️ 向下跳空 {gap_pct:.1f}%"))
                    alert_weights.append(2)
        
        # 8. 动态止盈/移动止损 (当盈利达到一定幅度后启动)
        if cost > 0 and cfg.get('trailing_stop', True):
            profit_pct = (price - cost) / cost * 100
            
            # 当盈利 >= 10% 时，启动移动止盈
            if profit_pct >= 10:
                # 计算回撤幅度 (从最高点回撤)
                high_since_cost = data.get('high', price)
                drawdown = (high_since_cost - price) / high_since_cost * 100 if high_since_cost > cost else 0
                
                # 回撤5%提醒减仓
                if drawdown >= 5 and not self._alerted_recently(code, 'trailing_stop_5'):
                    alerts.append(('trailing_stop_5', f"📉 利润回撤 {drawdown:.1f}%，建议减仓保护利润"))
                    alert_weights.append(2)
                
                # 回撤10%提醒清仓
                elif drawdown >= 10 and not self._alerted_recently(code, 'trailing_stop_10'):
                    alerts.append(('trailing_stop_10', f"🚨 利润回撤 {drawdown:.1f}%，建议清仓止损"))
                    alert_weights.append(3)
        
        # 9. 计算预警级别
        level = self._calculate_alert_level(alerts, alert_weights, stock_type)
        
        return alerts, level
    
    def _calculate_alert_level(self, alerts, weights, stock_type):
        """计算预警级别: info(提醒) / warning(警告) / critical(紧急)"""
        if not alerts:
            return None
        
        total_weight = sum(weights)
        alert_count = len(alerts)
        
        # 紧急: 多条件共振 或 高权重单一条件
        if total_weight >= 5 or alert_count >= 3:
            return "critical"
        
        # 警告: 中等权重 或 2个条件
        if total_weight >= 3 or alert_count >= 2:
            return "warning"
        
        # 提醒: 单一低权重条件
        return "info"
    
    def _alerted_recently(self, code, atype):
        import time
        now = time.time()
        self.alert_log = [l for l in self.alert_log if now - l['t'] < 1800] # 30分钟有效期
        for l in self.alert_log:
            if l['c'] == code and l['a'] == atype: return True
        return False
    
    def record_alert(self, code, atype):
        import time
        self.alert_log.append({'c': code, 'a': atype, 't': time.time()})

class StockAnalyser:
    """股票智能分析器 - 结合多维度数据给出建议"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def fetch_eastmoney_news(self, symbol: str, name: str, limit: int = 5):
        """获取东方财富个股新闻"""
        url = f"https://searchapi.eastmoney.com/api/suggest/get"
        params = {
            "input": name,
            "type": 14,
            "count": limit
        }
        try:
            resp = self.session.get(url, params=params, timeout=10)
            data = resp.json()
            news_list = []
            for item in data.get("QuotationCodeTable", {}).get("Data", []):
                news_list.append({
                    "title": item.get("Title", ""),
                    "url": item.get("Url", ""),
                    "time": item.get("ShowTime", "")
                })
            return news_list
        except Exception as e:
            logging.error(f"获取新闻失败: {e}")
            return []
    
    def analyze_sentiment(self, news_list):
        """简单情感分析"""
        positive_words = ['利好', '增长', '突破', '买入', '增持', '涨停', '超预期', '业绩大增']
        negative_words = ['利空', '减持', '下跌', '卖出', '亏损', '暴雷', '跌停', '不及预期']
        
        sentiment = {"positive": 0, "negative": 0, "neutral": 0, "summary": []}
        
        for news in news_list:
            title = news.get("title", "")
            p_count = sum(1 for w in positive_words if w in title)
            n_count = sum(1 for w in negative_words if w in title)
            
            if p_count > n_count:
                sentiment["positive"] += 1
            elif n_count > p_count:
                sentiment["negative"] += 1
            else:
                sentiment["neutral"] += 1
        
        # 生成情感摘要
        if sentiment["positive"] > sentiment["negative"]:
            sentiment["overall"] = "偏多"
        elif sentiment["negative"] > sentiment["positive"]:
            sentiment["overall"] = "偏空"
        else:
            sentiment["overall"] = "中性"
            
        return sentiment
    
    def generate_insight(self, stock, price_data, alerts):
        """生成综合分析报告"""
        code = stock['code']
        name = stock['name']
        
        # 1. 获取新闻
        news_list = self.fetch_eastmoney_news(code, name)
        sentiment = self.analyze_sentiment(news_list)
        
        # 2. 构建报告
        report = f"""📊 <b>{name} ({code}) 深度分析</b>

💰 <b>价格异动:</b>
• 当前: {price_data.get('price', 'N/A')} ({price_data.get('change_pct', 0):+.2f}%)
• 触发: {', '.join([a[1] for a in alerts])}

📰 <b>舆情分析 ({sentiment.get('overall', '未知')}):</b>
• 最近新闻: {len(news_list)} 条
• 正面: {sentiment.get('positive', 0)} | 负面: {sentiment.get('negative', 0)}
"""
        
        # 添加最新新闻标题
        if news_list:
            report += "\n<b>最新动态:</b>\n"
            for n in news_list[:2]:
                report += f"• {n.get('title', '无标题')[:30]}...\n"
        
        # 4. 给出建议
        suggestion = self._generate_suggestion(sentiment, alerts)
        report += f"\n💡 <b>建议:</b>\n{suggestion}"
        
        return report
    
    def _generate_suggestion(self, sentiment, alerts):
        """基于数据生成建议"""
        alert_types = [a[0] for a in alerts]
        overall = sentiment.get("overall", "中性")
        
        # 价格下跌 + 舆情偏空 = 谨慎
        if "below" in alert_types and overall == "偏空":
            return "⚠️ 价格跌破支撑位，且舆情偏空，建议观察等待，不急于抄底。"
        
        # 价格下跌 + 舆情偏多 = 可能是机会
        if "below" in alert_types and overall == "偏多":
            return "🔍 价格下跌但舆情偏多，可能是情绪错杀，关注是否有反弹机会。"
        
        # 价格突破 + 舆情偏多 = 确认趋势
        if "above" in alert_types and overall == "偏多":
            return "🚀 价格突破且舆情配合，趋势可能延续，可考虑顺势而为。"
        
        # 大涨
        if "pct_up" in alert_types:
            return "📈 短期涨幅较大，注意获利了结风险。"
        
        # 大跌
        if "pct_down" in alert_types:
            return "📉 短期跌幅较大，关注是否超跌反弹，但勿急于抄底。"
        
        return "⏳ 建议保持观察，等待更明确信号。"

class StockMonitorSkill:
    """股票监控预警技能 - OpenClaw集成"""
    
    def __init__(self):
        self.alert_system = StockAlertWithRunOnce()
        self.analyser = StockAnalyser()
    
    def generate_report(self):
        """生成股票监控报告"""
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"📊 【股票监控】{current_time}\n\n"
        
        # 执行监控
        alerts = self.alert_system.run_once()
        
        if alerts:
            for alert in alerts:
                report += alert + "\n\n"
        else:
            report += "✅ 暂无预警信息，所有标的运行正常\n"
        
        # 总结
        report += "💡 数据来源：新浪财经、东方财富\n"
        report += "⚠️ 仅供参考，不构成投资建议"
        
        return report
    
    def run(self):
        """运行监控"""
        return self.generate_report()

# 兼容原有的 run_once 方法
class StockAlertWithRunOnce(StockAlert):
    def run_once(self, smart_mode=True):
        """执行监控 (支持智能频率)"""
        stocks_to_check = WATCHLIST
        data_map = self.fetch_sina_realtime(stocks_to_check)
        triggered = []
        
        for stock in stocks_to_check:
            code = stock['code']
            if code not in data_map: continue
            
            data = data_map[code]
            
            # 数据有效性检查
            if data['price'] <= 0 or data['prev_close'] <= 0:
                continue
            
            alerts, level = self.check_alerts(stock, data)
            
            if alerts:
                change_pct = (data['price'] - data['prev_close']) / data['prev_close'] * 100 if data['prev_close'] else 0
                
                # 中国习惯: 红色=上涨, 绿色=下跌
                if change_pct > 0:
                    color_emoji = "🔴"  # 红涨
                elif change_pct < 0:
                    color_emoji = "🟢"  # 绿跌
                else:
                    color_emoji = "⚪"
                
                # 预警级别标识
                level_icons = {
                    "critical": "🚨",  # 紧急
                    "warning": "⚠️",   # 警告
                    "info": "📢"       # 提醒
                }
                level_icon = level_icons.get(level, "📢")
                level_text = {"critical": "【紧急】", "warning": "【警告】", "info": "【提醒】"}.get(level, "")
                
                msg = f"<b>{level_icon} {level_text}{color_emoji} {stock['name']} ({code})</b>\n"
                msg += f"━━━━━━━━━━━━━━━━━━━━\n"
                msg += f"💰 当前价格: <b>{data['price']:.2f}</b> ({change_pct:+.2f}%)\n"
                
                # 显示持仓盈亏
                cost = stock.get('cost', 0)
                if cost > 0:
                    cost_change = (data['price'] - cost) / cost * 100
                    profit_icon = "🔴+" if cost_change > 0 else "🟢"
                    msg += f"📊 持仓成本: ¥{cost:.2f} | 盈亏: {profit_icon}{cost_change:.2f}%\n"
                
                msg += f"\n🎯 触发预警 ({len(alerts)}项):\n"
                for _, text in alerts: 
                    msg += f"  • {text}\n"
                    self.record_alert(code, _)
                
                # 集成智能分析
                try:
                    insight = self.analyser.generate_insight(stock, {
                        'price': data['price'],
                        'change_pct': change_pct
                    }, alerts)
                    msg += f"\n{insight}"
                except Exception as e:
                    logging.error(f"分析失败: {e}")
                
                triggered.append(msg)
        
        return triggered
    
    @property
    def analyser(self):
        return StockAnalyser()

# 主函数
def main():
    """主函数"""
    skill = StockMonitorSkill()
    print(skill.run())

if __name__ == "__main__":
    main()
