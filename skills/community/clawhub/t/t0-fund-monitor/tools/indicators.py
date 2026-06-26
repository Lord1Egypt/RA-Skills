#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术指标计算模块 - 健壮版（带数据验证、异常处理、类型转换）
"""

import pandas as pd
import talib
import numpy as np
import sys
import logging

logger = logging.getLogger(__name__)

def validate_dataframe(df: pd.DataFrame) -> bool:
    """验证 DataFrame 是否有效"""
    if df is None or len(df) == 0:
        return False
    
    required_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in required_cols:
        if col not in df.columns:
            logger.error(f"缺少必要列：{col}")
            return False
        if df[col].isnull().any():
            logger.warning(f"列 {col} 包含空值")
    
    # 检查数据有效性
    if (df['close'] <= 0).any():
        logger.error("收盘价包含非正值")
        return False
    
    if (df['high'] < df['low']).any():
        logger.error("最高价小于最低价")
        return False
    
    return True

def to_float64_array(series) -> np.ndarray:
    """将 pandas Series 转换为 float64 类型的 numpy 数组（TA-Lib 兼容）"""
    return series.values.astype(np.float64)

def calculate_indicators(df: pd.DataFrame, config: dict = None, fast_mode: bool = False) -> pd.DataFrame:
    """计算技术指标（带数据验证和类型转换）"""
    if not validate_dataframe(df):
        return None
    
    try:
        # 确保数据类型正确
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(np.float64)
        
        # 删除空值
        df = df.dropna()
        
        if len(df) < 30:
            logger.error(f"数据量不足 ({len(df)}条)，需要至少 30 条")
            return None
        
        # 转换为 float64 数组（TA-Lib 要求）
        open_arr = to_float64_array(df['open'])
        high_arr = to_float64_array(df['high'])
        low_arr = to_float64_array(df['low'])
        close_arr = to_float64_array(df['close'])
        volume_arr = to_float64_array(df['volume'])
        
        # 快速模式：更敏感参数
        if fast_mode:
            df['MACD_DIF'], df['MACD_DEA'], df['MACD_HIST'] = talib.MACD(
                close_arr, fastperiod=6, slowperiod=13, signalperiod=5
            )
            df['KDJ_K'], df['KDJ_D'] = talib.STOCH(
                high_arr, low_arr, close_arr,
                fastk_period=5, slowk_period=3, slowd_period=3
            )
            df['RSI'] = talib.RSI(close_arr, timeperiod=7)
            df['MA5'] = talib.SMA(close_arr, timeperiod=5)
            df['MA10'] = talib.SMA(close_arr, timeperiod=10)
            df['VMA5'] = talib.SMA(volume_arr, timeperiod=5)
        
        # 标准模式
        else:
            macd_cfg = config.get('macd', {'fast': 12, 'slow': 26, 'signal': 9}) if config else {}
            df['MACD_DIF'], df['MACD_DEA'], df['MACD_HIST'] = talib.MACD(
                close_arr,
                fastperiod=macd_cfg.get('fast', 12),
                slowperiod=macd_cfg.get('slow', 26),
                signalperiod=macd_cfg.get('signal', 9)
            )
            
            kdj_cfg = config.get('kdj', {'n': 9, 'm1': 3, 'm2': 3}) if config else {}
            df['KDJ_K'], df['KDJ_D'] = talib.STOCH(
                high_arr, low_arr, close_arr,
                fastk_period=kdj_cfg.get('n', 9),
                slowk_period=kdj_cfg.get('m1', 3),
                slowd_period=kdj_cfg.get('m2', 3)
            )
            
            rsi_cfg = config.get('rsi', {'period': 14}) if config else {}
            df['RSI'] = talib.RSI(close_arr, timeperiod=rsi_cfg.get('period', 14))
            
            boll_cfg = config.get('bollinger', {'period': 20, 'std': 2}) if config else {}
            df['BOLL_UPPER'], df['BOLL_MIDDLE'], df['BOLL_LOWER'] = talib.BBANDS(
                close_arr,
                timeperiod=boll_cfg.get('period', 20),
                nbdevup=boll_cfg.get('std', 2),
                nbdevdn=boll_cfg.get('std', 2),
                matype=0
            )
            
            df['MA5'] = talib.SMA(close_arr, timeperiod=5)
            df['MA10'] = talib.SMA(close_arr, timeperiod=10)
            df['MA20'] = talib.SMA(close_arr, timeperiod=20)
            df['VMA5'] = talib.SMA(volume_arr, timeperiod=5)
        
        # KDJ_J
        if 'KDJ_K' in df.columns and 'KDJ_D' in df.columns:
            df['KDJ_J'] = 3 * df['KDJ_K'] - 2 * df['KDJ_D']
        
        # 填充 NaN 值
        df = df.ffill().fillna(0)
        
        return df
        
    except Exception as e:
        logger.error(f"计算指标失败：{e}", exc_info=True)
        return None

def get_latest_indicators(df: pd.DataFrame) -> dict:
    """获取最新指标（带异常处理）"""
    if df is None or len(df) < 2:
        return None
    
    try:
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        def safe_float(val, default=0):
            try:
                return float(val) if pd.notna(val) else default
            except:
                return default
        
        return {
            'macd_dif': safe_float(last.get('MACD_DIF'), 0),
            'macd_dea': safe_float(last.get('MACD_DEA'), 0),
            'macd_hist': safe_float(last.get('MACD_HIST'), 0),
            'kdj_k': safe_float(last.get('KDJ_K'), 50),
            'kdj_d': safe_float(last.get('KDJ_D'), 50),
            'kdj_j': safe_float(last.get('KDJ_J'), 50),
            'rsi': safe_float(last.get('RSI'), 50),
            'close': safe_float(last.get('close'), 0),
            'volume': safe_float(last.get('volume'), 0),
            'vma5': safe_float(last.get('VMA5'), 1),
            'ma5': safe_float(last.get('MA5'), 0),
            'prev_macd_dif': safe_float(prev.get('MACD_DIF'), 0),
            'prev_macd_dea': safe_float(prev.get('MACD_DEA'), 0),
        }
    except Exception as e:
        logger.error(f"获取最新指标失败：{e}")
        return None

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print("指标计算模块测试")
