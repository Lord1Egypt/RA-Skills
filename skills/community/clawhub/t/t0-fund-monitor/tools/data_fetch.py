#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金数据获取模块 - 多数据源增强版
支持：东方财富、新浪财经、腾讯财经
"""

import akshare as ak
import pandas as pd
import requests
from datetime import datetime
import sys
import time
import re
import logging

logger = logging.getLogger(__name__)

# 请求重试配置
MAX_RETRIES = 2
RETRY_DELAY = 1  # 秒
REQUEST_TIMEOUT = 10  # 秒

# 缓存配置
CACHE_TTL = 60  # 缓存有效期（秒）
price_cache = {}

# HTTP Session（复用连接）
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
})

def get_fund_realtime(code: str, retry: int = 0) -> dict:
    """获取基金实时行情（多数据源自动切换）"""
    try:
        # 检查缓存
        cache_key = f"{code}_{int(time.time()) // CACHE_TTL}"
        if cache_key in price_cache:
            logger.debug(f"使用缓存数据 {code}")
            return price_cache[cache_key]
        
        # 数据源优先级：新浪 > 腾讯 > 东方财富
        result = None
        
        # 方案 1: 新浪财经
        result = _get_from_sina(code)
        if result:
            logger.info(f"✅ {code} [新浪]: {result['price']} ({result['change_pct']}%)")
            price_cache[cache_key] = result
            return result
        
        # 方案 2: 腾讯财经
        result = _get_from_tencent(code)
        if result:
            logger.info(f"✅ {code} [腾讯]: {result['price']} ({result['change_pct']}%)")
            price_cache[cache_key] = result
            return result
        
        # 方案 3: 东方财富（备用）
        result = _get_from_eastmoney(code)
        if result:
            logger.info(f"✅ {code} [东方财富]: {result['price']} ({result['change_pct']}%)")
            price_cache[cache_key] = result
            return result
        
        logger.warning(f"❌ {code} 所有数据源均失败")
        return None
        
    except Exception as e:
        if retry < MAX_RETRIES:
            logger.warning(f"获取行情失败 {code}，重试 {retry+1}/{MAX_RETRIES}: {e}")
            time.sleep(RETRY_DELAY)
            return get_fund_realtime(code, retry + 1)
        else:
            logger.error(f"获取行情失败 {code}: {e}")
            return None

def _get_from_sina(code: str) -> dict:
    """新浪财经数据源"""
    try:
        # 判断市场
        if code.startswith('51') or code.startswith('56'):
            symbol = f"sh{code}"
        elif code.startswith('15') or code.startswith('16'):
            symbol = f"sz{code}"
        else:
            symbol = f"sh{code}"  # 默认上证
        
        url = f"http://hq.sinajs.cn/list={symbol}"
        r = session.get(url, timeout=5)
        
        if r.status_code != 200 or not r.text.strip():
            return None
        
        # 解析数据：var hq_str_sh512880="证券 ETF,1.107,1.106,1.118,1.120,1.107,1.118,1.117,..."
        match = re.search(r'="([^"]+)"', r.text)
        if not match:
            return None
        
        data = match.group(1).split(',')
        if len(data) < 10:
            return None
        
        name = data[0]
        open_price = float(data[1]) if data[1] else 0
        close = float(data[3]) if data[3] else 0  # 当前价
        high = float(data[4]) if data[4] else 0
        low = float(data[5]) if data[5] else 0
        prev_close = float(data[2]) if data[2] else 0
        volume = float(data[8]) if data[8] else 0
        amount = float(data[9]) if data[9] else 0
        
        change = close - prev_close
        change_pct = (change / prev_close * 100) if prev_close else 0
        
        return {
            'code': code,
            'name': name,
            'price': close,
            'change_pct': round(change_pct, 2),
            'change': round(change, 3),
            'volume': volume,
            'amount': amount,
            'high': high,
            'low': low,
            'open': open_price,
            'prev_close': prev_close,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'sina'
        }
    except Exception as e:
        logger.debug(f"新浪数据源失败 {code}: {e}")
        return None

def _get_from_tencent(code: str) -> dict:
    """腾讯财经数据源"""
    try:
        # 判断市场
        if code.startswith('51') or code.startswith('56'):
            symbol = f"sh{code}"
        elif code.startswith('15') or code.startswith('16'):
            symbol = f"sz{code}"
        else:
            symbol = f"sh{code}"
        
        url = f"http://qt.gtimg.cn/q={symbol}"
        r = session.get(url, timeout=5)
        
        if r.status_code != 200 or not r.text.strip():
            return None
        
        # 解析数据：v_sh512880="51~证券 ETF~512880~1.118~1.106~1.107~..."
        match = re.search(r'="([^"]+)"', r.text)
        if not match:
            return None
        
        data = match.group(1).split('~')
        if len(data) < 50:
            return None
        
        name = data[1]
        prev_close = float(data[4]) if data[4] else 0
        close = float(data[3]) if data[3] else 0
        open_price = float(data[5]) if data[5] else 0
        high = float(data[33]) if data[33] else 0
        low = float(data[34]) if data[34] else 0
        volume = float(data[6]) if data[6] else 0
        amount = float(data[37]) if data[37] else 0
        
        # 腾讯直接提供涨跌幅
        change_pct_str = data[32] if len(data) > 32 else ""
        change_pct = float(change_pct_str) if change_pct_str else ((close - prev_close) / prev_close * 100 if prev_close else 0)
        change = close - prev_close
        
        return {
            'code': code,
            'name': name,
            'price': close,
            'change_pct': round(change_pct, 2),
            'change': round(change, 3),
            'volume': volume,
            'amount': amount,
            'high': high,
            'low': low,
            'open': open_price,
            'prev_close': prev_close,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'tencent'
        }
    except Exception as e:
        logger.debug(f"腾讯数据源失败 {code}: {e}")
        return None

def _get_from_eastmoney(code: str) -> dict:
    """东方财富数据源（备用）"""
    try:
        # 尝试历史数据接口
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - pd.Timedelta(days=5)).strftime("%Y%m%d")
        
        df = ak.fund_etf_hist_em(symbol=code, period="daily", start_date=start_date, end_date=end_date)
        
        if df is None or len(df) == 0:
            return None
        
        row = df.iloc[-1]
        change_pct = float(row['涨跌幅'])
        close = float(row['收盘'])
        
        return {
            'code': code,
            'name': code,
            'price': close,
            'change_pct': change_pct,
            'change': float(row['涨跌额']),
            'volume': float(row['成交量']),
            'amount': float(row['成交额']),
            'high': float(row['最高']),
            'low': float(row['最低']),
            'open': float(row['开盘']),
            'prev_close': close / (1 + change_pct/100) if change_pct != 0 else close,
            'timestamp': str(row['日期']),
            'source': 'eastmoney_hist'
        }
    except Exception as e:
        logger.debug(f"东方财富数据源失败 {code}: {e}")
        return None

def get_fund_1min_kline(code: str, periods: int = 60, retry: int = 0) -> pd.DataFrame:
    """获取基金 1 分钟 K 线数据"""
    return get_fund_kline(code, period='1', periods=periods, retry=retry)

def get_fund_5min_kline(code: str, periods: int = 100, retry: int = 0) -> pd.DataFrame:
    """获取基金 5 分钟 K 线数据"""
    return get_fund_kline(code, period='5', periods=periods, retry=retry)

def get_fund_kline(code: str, period: str, periods: int, retry: int = 0) -> pd.DataFrame:
    """获取 K 线数据"""
    try:
        df = ak.fund_etf_hist_min_em(symbol=code, period=period)
        
        if df is None or len(df) == 0:
            return None
        
        required_cols = ['时间', '开盘', '收盘', '最高', '最低', '成交量']
        for col in required_cols:
            if col not in df.columns:
                return None
        
        df = df.rename(columns={
            '时间': 'time',
            '开盘': 'open',
            '收盘': 'close',
            '最高': 'high',
            '最低': 'low',
            '成交量': 'volume',
            '成交额': 'amount'
        })
        
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna(subset=['open', 'high', 'low', 'close'])
        
        if len(df) < 10:
            return None
        
        df['code'] = code
        return df.tail(periods)
        
    except Exception as e:
        if retry < MAX_RETRIES:
            time.sleep(RETRY_DELAY)
            return get_fund_kline(code, period, periods, retry + 1)
        else:
            logger.error(f"获取 K 线失败 {code}: {e}")
            return None

if __name__ == '__main__':
    # 测试
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    test_codes = ['512880', '513050', '159915', '513310', '513080']
    
    print("\n测试多数据源获取...\n")
    for code in test_codes:
        result = get_fund_realtime(code)
        if result:
            print(f"  ✅ {code} {result['name']}: {result['price']} ({result['change_pct']}%) [{result['source']}]")
        else:
            print(f"  ❌ {code} 获取失败")
    print()
