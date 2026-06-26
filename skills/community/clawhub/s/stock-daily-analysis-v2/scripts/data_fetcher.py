# -*- coding: utf-8 -*-
"""
数据获取模块 - 基于 akshare 的多市场数据获取
支持 A股、港股、美股行情获取
"""

import logging
import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

import pandas as pd
import akshare as ak

logger = logging.getLogger(__name__)


@dataclass
class StockQuote:
    """统一实时行情数据结构"""
    code: str
    name: str = ""
    price: float = 0.0
    change_pct: float = 0.0
    change_amount: float = 0.0
    volume: int = 0
    amount: float = 0.0
    open_price: float = 0.0
    high: float = 0.0
    low: float = 0.0
    pre_close: float = 0.0
    volume_ratio: Optional[float] = None
    turnover_rate: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    total_mv: Optional[float] = None
    circ_mv: Optional[float] = None


@dataclass
class ChipDistribution:
    """筹码分布数据"""
    profit_ratio: float = 0.0  # 获利比例
    avg_cost: float = 0.0  # 平均成本
    concentration_90: float = 0.0  # 90%筹码集中度
    concentration_70: float = 0.0  # 70%筹码集中度


def _is_us_code(stock_code: str) -> bool:
    """判断是否为美股代码（1-5个大写字母）"""
    code = stock_code.strip().upper()
    return bool(re.match(r'^[A-Z]{1,5}(\.[A-Z])?$', code))


def _is_hk_code(stock_code: str) -> bool:
    """判断是否为港股代码（5位数字）"""
    code = stock_code.lower()
    if code.startswith('hk'):
        numeric_part = code[2:]
        return numeric_part.isdigit() and 1 <= len(numeric_part) <= 5
    return code.isdigit() and len(code) == 5


def _is_etf_code(stock_code: str) -> bool:
    """判断是否为 ETF 代码"""
    etf_prefixes = ('51', '52', '56', '58', '15', '16', '18')
    return stock_code.startswith(etf_prefixes) and len(stock_code) == 6


def normalize_code(stock_code: str) -> tuple:
    """
    标准化股票代码
    
    Returns:
        tuple: (market, code)
        - market: 'a', 'hk', 'us'
        - code: 标准化后的代码
    """
    code = stock_code.strip()
    
    if _is_us_code(code):
        return 'us', code.upper()
    
    if _is_hk_code(code):
        # 去除 hk 前缀，返回5位数字
        if code.lower().startswith('hk'):
            code = code[2:]
        return 'hk', code.zfill(5)
    
    # A股默认处理
    return 'a', code


def get_daily_data(stock_code: str, days: int = 60) -> Optional[pd.DataFrame]:
    """
    获取股票日线数据
    
    Args:
        stock_code: 股票代码
        days: 获取天数
        
    Returns:
        DataFrame 包含 OHLCV 数据，失败返回 None
    """
    market, code = normalize_code(stock_code)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days * 2)
    
    try:
        if market == 'us':
            return _fetch_us_data(code, start_date, end_date)
        elif market == 'hk':
            return _fetch_hk_data(code, start_date, end_date)
        else:
            return _fetch_a_stock_data(code, start_date, end_date)
    except Exception as e:
        logger.error(f"获取 {stock_code} 数据失败: {e}")
        return None


def _fetch_a_stock_data(stock_code: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """获取 A 股数据"""
    start_str = start_date.strftime('%Y%m%d')
    end_str = end_date.strftime('%Y%m%d')
    
    if _is_etf_code(stock_code):
        df = ak.fund_etf_hist_em(
            symbol=stock_code,
            period="daily",
            start_date=start_str,
            end_date=end_str,
            adjust="qfq"
        )
    else:
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date=start_str,
            end_date=end_str,
            adjust="qfq"
        )
    
    return _standardize_columns(df)


def _fetch_hk_data(stock_code: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """获取港股数据"""
    start_str = start_date.strftime('%Y%m%d')
    end_str = end_date.strftime('%Y%m%d')
    
    df = ak.stock_hk_hist(
        symbol=stock_code,
        period="daily",
        start_date=start_str,
        end_date=end_str,
        adjust="qfq"
    )
    
    return _standardize_columns(df)


def _fetch_us_data(stock_code: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """获取美股数据"""
    df = ak.stock_us_daily(symbol=stock_code, adjust="qfq")
    
    if df is None or df.empty:
        return pd.DataFrame()
    
    # 按日期过滤
    df['date'] = pd.to_datetime(df['date'])
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    # 标准化列名
    df = df.rename(columns={
        'date': '日期',
        'open': '开盘',
        'high': '最高',
        'low': '最低',
        'close': '收盘',
        'volume': '成交量'
    })
    
    # 计算涨跌幅和成交额
    if '收盘' in df.columns:
        df['涨跌幅'] = df['收盘'].pct_change() * 100
        df['涨跌幅'] = df['涨跌幅'].fillna(0)
    
    if '成交量' in df.columns and '收盘' in df.columns:
        df['成交额'] = df['成交量'] * df['收盘']
    
    return _standardize_columns(df)


def _standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """标准化 DataFrame 列名"""
    if df is None or df.empty:
        return pd.DataFrame()
    
    column_mapping = {
        '日期': 'date',
        '开盘': 'open',
        '收盘': 'close',
        '最高': 'high',
        '最低': 'low',
        '成交量': 'volume',
        '成交额': 'amount',
        '涨跌幅': 'pct_chg',
    }
    
    df = df.rename(columns=column_mapping)
    
    # 确保日期格式正确
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    
    # 数值转换
    for col in ['open', 'high', 'low', 'close', 'volume', 'amount', 'pct_chg']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 去除空值行
    df = df.dropna(subset=['close', 'volume'])
    
    # 按日期排序
    df = df.sort_values('date', ascending=True).reset_index(drop=True)
    
    return df


def get_realtime_quote(stock_code: str) -> Optional[StockQuote]:
    """
    获取实时行情
    
    Args:
        stock_code: 股票代码
        
    Returns:
        StockQuote 对象，失败返回 None
    """
    market, code = normalize_code(stock_code)
    
    try:
        if market == 'us':
            return None  # 美股暂不支持实时行情
        elif market == 'hk':
            return _get_hk_realtime_quote(code)
        else:
            return _get_a_stock_realtime_quote(code)
    except Exception as e:
        logger.warning(f"获取实时行情失败 {stock_code}: {e}")
        return None


def _get_a_stock_realtime_quote(stock_code: str) -> Optional[StockQuote]:
    """获取 A 股实时行情"""
    try:
        df = ak.stock_zh_a_spot_em()
        row = df[df['代码'] == stock_code]
        
        if row.empty:
            return None
        
        row = row.iloc[0]
        
        return StockQuote(
            code=stock_code,
            name=str(row.get('名称', '')),
            price=float(row.get('最新价', 0)) if pd.notna(row.get('最新价')) else 0,
            change_pct=float(row.get('涨跌幅', 0)) if pd.notna(row.get('涨跌幅')) else 0,
            change_amount=float(row.get('涨跌额', 0)) if pd.notna(row.get('涨跌额')) else 0,
            volume=int(row.get('成交量', 0)) if pd.notna(row.get('成交量')) else 0,
            amount=float(row.get('成交额', 0)) if pd.notna(row.get('成交额')) else 0,
            open_price=float(row.get('今开', 0)) if pd.notna(row.get('今开')) else 0,
            high=float(row.get('最高', 0)) if pd.notna(row.get('最高')) else 0,
            low=float(row.get('最低', 0)) if pd.notna(row.get('最低')) else 0,
            volume_ratio=float(row.get('量比', 0)) if pd.notna(row.get('量比')) else None,
            turnover_rate=float(row.get('换手率', 0)) if pd.notna(row.get('换手率')) else None,
            pe_ratio=float(row.get('市盈率-动态', 0)) if pd.notna(row.get('市盈率-动态')) else None,
            pb_ratio=float(row.get('市净率', 0)) if pd.notna(row.get('市净率')) else None,
            total_mv=float(row.get('总市值', 0)) if pd.notna(row.get('总市值')) else None,
            circ_mv=float(row.get('流通市值', 0)) if pd.notna(row.get('流通市值')) else None,
        )
    except Exception as e:
        logger.warning(f"获取 A 股实时行情失败: {e}")
        return None


def _get_hk_realtime_quote(stock_code: str) -> Optional[StockQuote]:
    """获取港股实时行情"""
    try:
        df = ak.stock_hk_spot_em()
        row = df[df['代码'] == stock_code]
        
        if row.empty:
            return None
        
        row = row.iloc[0]
        
        return StockQuote(
            code=stock_code,
            name=str(row.get('名称', '')),
            price=float(row.get('最新价', 0)) if pd.notna(row.get('最新价')) else 0,
            change_pct=float(row.get('涨跌幅', 0)) if pd.notna(row.get('涨跌幅')) else 0,
            change_amount=float(row.get('涨跌额', 0)) if pd.notna(row.get('涨跌额')) else 0,
            volume=int(row.get('成交量', 0)) if pd.notna(row.get('成交量')) else 0,
            amount=float(row.get('成交额', 0)) if pd.notna(row.get('成交额')) else 0,
            volume_ratio=float(row.get('量比', 0)) if pd.notna(row.get('量比')) else None,
            turnover_rate=float(row.get('换手率', 0)) if pd.notna(row.get('换手率')) else None,
            pe_ratio=float(row.get('市盈率', 0)) if pd.notna(row.get('市盈率')) else None,
            pb_ratio=float(row.get('市净率', 0)) if pd.notna(row.get('市净率')) else None,
        )
    except Exception as e:
        logger.warning(f"获取港股实时行情失败: {e}")
        return None


def get_chip_distribution(stock_code: str) -> Optional[ChipDistribution]:
    """
    获取筹码分布数据（仅 A 股）
    
    Args:
        stock_code: 股票代码
        
    Returns:
        ChipDistribution 对象，失败返回 None
    """
    market, code = normalize_code(stock_code)
    
    if market != 'a' or _is_etf_code(code):
        return None
    
    try:
        df = ak.stock_cyq_em(symbol=code)
        
        if df is None or df.empty:
            return None
        
        latest = df.iloc[-1]
        
        return ChipDistribution(
            profit_ratio=float(latest.get('获利比例', 0)) if pd.notna(latest.get('获利比例')) else 0,
            avg_cost=float(latest.get('平均成本', 0)) if pd.notna(latest.get('平均成本')) else 0,
            concentration_90=float(latest.get('90%集中度', 0)) if pd.notna(latest.get('90%集中度')) else 0,
            concentration_70=float(latest.get('70%集中度', 0)) if pd.notna(latest.get('70%集中度')) else 0,
        )
    except Exception as e:
        logger.warning(f"获取筹码分布失败 {stock_code}: {e}")
        return None


def get_stock_name(stock_code: str) -> str:
    """获取股票名称"""
    quote = get_realtime_quote(stock_code)
    if quote and quote.name:
        return quote.name
    
    # 默认返回代码
    return stock_code
