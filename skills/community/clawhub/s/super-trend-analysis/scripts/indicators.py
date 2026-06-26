#!/usr/bin/env python3
"""
技术指标计算库
提供移动平均线、MACD、RSI、布林带等指标计算
"""

import pandas as pd
import numpy as np


def calculate_sma(data: pd.Series, period: int) -> pd.Series:
    """
    计算简单移动平均线（SMA）
    
    Args:
        data: 价格数据
        period: 周期
    
    Returns:
        SMA 序列
    """
    return data.rolling(window=period).mean()


def calculate_ema(data: pd.Series, period: int) -> pd.Series:
    """
    计算指数移动平均线（EMA）
    
    Args:
        data: 价格数据
        period: 周期
    
    Returns:
        EMA 序列
    """
    return data.ewm(span=period, adjust=False).mean()


def calculate_macd(data: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> dict:
    """
    计算 MACD 指标
    
    Args:
        data: 价格数据
        fast: 快速 EMA 周期
        slow: 慢速 EMA 周期
        signal: 信号线周期
    
    Returns:
        包含 MACD 各部分的字典
    """
    ema_fast = calculate_ema(data, fast)
    ema_slow = calculate_ema(data, slow)
    
    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal)
    histogram = macd_line - signal_line
    
    return {
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram,
        'ema_fast': ema_fast,
        'ema_slow': ema_slow
    }


def calculate_rsi(data: pd.Series, period: int = 14) -> pd.Series:
    """
    计算相对强弱指标（RSI）
    
    Args:
        data: 价格数据
        period: 周期
    
    Returns:
        RSI 序列
    """
    delta = data.diff()
    
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def calculate_bollinger_bands(data: pd.Series, period: int = 20, std_dev: float = 2) -> dict:
    """
    计算布林带
    
    Args:
        data: 价格数据
        period: 周期
        std_dev: 标准差倍数
    
    Returns:
        包含布林带各部分的字典
    """
    sma = calculate_sma(data, period)
    std = data.rolling(window=period).std()
    
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    band_width = (upper_band - lower_band) / sma * 100
    price_position = (data - lower_band) / (upper_band - lower_band) * 100
    
    return {
        'middle': sma,
        'upper': upper_band,
        'lower': lower_band,
        'width': band_width,
        'position': price_position
    }


def calculate_all_indicators(df: pd.DataFrame, price_col: str = '收盘') -> pd.DataFrame:
    """
    计算所有技术指标并添加到 DataFrame
    
    Args:
        df: 原始数据 DataFrame
        price_col: 价格列名
    
    Returns:
        添加了所有指标的 DataFrame
    """
    data = df.copy()
    prices = data[price_col]
    
    # 移动平均线
    data['MA5'] = calculate_sma(prices, 5)
    data['MA10'] = calculate_sma(prices, 10)
    data['MA20'] = calculate_sma(prices, 20)
    data['MA30'] = calculate_sma(prices, 30)
    data['MA60'] = calculate_sma(prices, 60)
    data['MA120'] = calculate_sma(prices, 120)
    
    data['EMA12'] = calculate_ema(prices, 12)
    data['EMA26'] = calculate_ema(prices, 26)
    
    # MACD
    macd_data = calculate_macd(prices)
    data['MACD'] = macd_data['macd']
    data['Signal'] = macd_data['signal']
    data['Histogram'] = macd_data['histogram']
    
    # RSI
    data['RSI'] = calculate_rsi(prices)
    
    # 布林带
    bb_data = calculate_bollinger_bands(prices)
    data['BB_Middle'] = bb_data['middle']
    data['BB_Upper'] = bb_data['upper']
    data['BB_Lower'] = bb_data['lower']
    data['BB_Width'] = bb_data['width']
    data['BB_Position'] = bb_data['position']
    
    return data


def analyze_trend_signals(df: pd.DataFrame) -> dict:
    """
    分析趋势信号
    
    Args:
        df: 包含技术指标的 DataFrame
    
    Returns:
        包含各种信号的字典
    """
    latest = df.iloc[-1]
    
    signals = {}
    
    # 均线排列分析
    ma5 = latest['MA5']
    ma10 = latest['MA10']
    ma20 = latest['MA20']
    ma60 = latest['MA60']
    
    if pd.notna(ma5) and pd.notna(ma20) and pd.notna(ma60):
        if ma5 > ma20 > ma60:
            signals['ma_trend'] = 'bullish'
            signals['ma_signal'] = '多头排列'
        elif ma5 < ma20 < ma60:
            signals['ma_trend'] = 'bearish'
            signals['ma_signal'] = '空头排列'
        else:
            signals['ma_trend'] = 'neutral'
            signals['ma_signal'] = '均线缠绕'
    else:
        signals['ma_trend'] = 'unknown'
        signals['ma_signal'] = '数据不足'
    
    # MACD 分析
    macd = latest['MACD']
    signal = latest['Signal']
    histogram = latest['Histogram']
    
    if pd.notna(macd) and pd.notna(signal):
        if macd > signal and histogram > 0:
            signals['macd_trend'] = 'bullish'
            signals['macd_signal'] = 'MACD 金叉，多头强势'
        elif macd < signal and histogram < 0:
            signals['macd_trend'] = 'bearish'
            signals['macd_signal'] = 'MACD 死叉，空头强势'
        else:
            signals['macd_trend'] = 'neutral'
            signals['macd_signal'] = 'MACD 中性'
    else:
        signals['macd_trend'] = 'unknown'
        signals['macd_signal'] = '数据不足'
    
    # RSI 分析
    rsi = latest['RSI']
    
    if pd.notna(rsi):
        if rsi > 70:
            signals['rsi_trend'] = 'overbought'
            signals['rsi_signal'] = f'RSI {rsi:.1f}，超买区域'
        elif rsi < 30:
            signals['rsi_trend'] = 'oversold'
            signals['rsi_signal'] = f'RSI {rsi:.1f}，超卖区域'
        elif rsi > 50:
            signals['rsi_trend'] = 'bullish'
            signals['rsi_signal'] = f'RSI {rsi:.1f}，强势区域'
        else:
            signals['rsi_trend'] = 'bearish'
            signals['rsi_signal'] = f'RSI {rsi:.1f}，弱势区域'
    else:
        signals['rsi_trend'] = 'unknown'
        signals['rsi_signal'] = '数据不足'
    
    # 布林带分析
    bb_position = latest['BB_Position']
    bb_width = latest['BB_Width']
    
    if pd.notna(bb_position):
        if bb_position > 80:
            signals['bb_trend'] = 'overbought'
            signals['bb_signal'] = f'价格接近上轨 ({bb_position:.1f}%)'
        elif bb_position < 20:
            signals['bb_trend'] = 'oversold'
            signals['bb_signal'] = f'价格接近下轨 ({bb_position:.1f}%)'
        else:
            signals['bb_trend'] = 'neutral'
            signals['bb_signal'] = f'价格在通道内 ({bb_position:.1f}%)'
    else:
        signals['bb_trend'] = 'unknown'
        signals['bb_signal'] = '数据不足'
    
    return signals


def calculate_trend_score(signals: dict) -> dict:
    """
    计算趋势综合评分
    
    Args:
        signals: 信号字典
    
    Returns:
        包含评分的字典
    """
    score = 0
    max_score = 100
    
    # 均线得分（30分）
    if signals['ma_trend'] == 'bullish':
        score += 30
    elif signals['ma_trend'] == 'bearish':
        score += 0
    else:
        score += 15
    
    # MACD 得分（30分）
    if signals['macd_trend'] == 'bullish':
        score += 30
    elif signals['macd_trend'] == 'bearish':
        score += 0
    else:
        score += 15
    
    # RSI 得分（20分）
    if signals['rsi_trend'] == 'bullish':
        score += 20
    elif signals['rsi_trend'] == 'oversold':
        score += 15  # 超卖可能反弹
    elif signals['rsi_trend'] == 'overbought':
        score += 5   # 超买可能回调
    elif signals['rsi_trend'] == 'bearish':
        score += 10
    else:
        score += 10
    
    # 布林带得分（20分）
    if signals['bb_trend'] == 'neutral':
        score += 20
    elif signals['bb_trend'] == 'oversold':
        score += 15
    elif signals['bb_trend'] == 'overbought':
        score += 5
    else:
        score += 10
    
    # 判断整体趋势
    if score >= 70:
        overall_trend = '上升趋势'
        trend_emoji = '🟢'
    elif score >= 50:
        overall_trend = '震荡偏强'
        trend_emoji = '🟡'
    elif score >= 30:
        overall_trend = '震荡偏弱'
        trend_emoji = '🟠'
    else:
        overall_trend = '下降趋势'
        trend_emoji = '🔴'
    
    return {
        'score': score,
        'max_score': max_score,
        'overall_trend': overall_trend,
        'trend_emoji': trend_emoji
    }
