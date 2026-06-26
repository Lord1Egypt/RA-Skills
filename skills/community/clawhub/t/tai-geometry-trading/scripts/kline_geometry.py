#!/usr/bin/env python3
"""
K-line Pattern Geometry Analysis Script
K线形态几何结构分析
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


def calculate_ohlc_features(df: pd.DataFrame) -> pd.DataFrame:
    """计算OHLC相关特征"""
    features = pd.DataFrame(index=df.index)
    
    # 基础特征
    features['body'] = abs(df['close'] - df['open'])  # 实体
    features['upper_shadow'] = df['high'] - df[['close', 'open']].max(axis=1)  # 上影线
    features['lower_shadow'] = df[['close', 'open']].min(axis=1) - df['low']  # 下影线
    features['range'] = df['high'] - df['low']  # 振幅
    
    # 实体占比
    features['body_ratio'] = features['body'] / features['range']
    
    # 趋势判断
    features['is_bullish'] = df['close'] > df['open']
    features['is_bearish'] = df['close'] < df['open']
    
    return features


def detect_trend_line(df: pd.DataFrame, window: int = 20) -> Dict:
    """
    检测趋势线结构
    通过连接高低点判断趋势方向
    """
    result = {
        'type': None,  # 'uptrend', 'downtrend', 'sideways'
        'strength': 0,  # 0-10
        'description': ''
    }
    
    if len(df) < window:
        return result
    
    recent = df.tail(window)
    
    # 简化判断：通过收盘价线性回归斜率
    x = np.arange(len(recent))
    y = recent['close'].values
    slope = np.polyfit(x, y, 1)[0]
    
    # 归一化斜率
    avg_price = y.mean()
    normalized_slope = slope / avg_price * 100
    
    if normalized_slope > 2:
        result['type'] = 'uptrend'
        result['strength'] = min(10, int(normalized_slope * 2))
        result['description'] = f'上升趋势结构，斜率{normalized_slope:.2f}%'
    elif normalized_slope < -2:
        result['type'] = 'downtrend'
        result['strength'] = min(10, int(-normalized_slope * 2))
        result['description'] = f'下降趋势结构，斜率{normalized_slope:.2f}%'
    else:
        result['type'] = 'sideways'
        result['strength'] = 3
        result['description'] = '横盘整理结构'
    
    return result


def detect_patterns(df: pd.DataFrame, window: int = 60) -> Dict:
    """
    检测常见K线形态
    """
    result = {
        'patterns': [],
        'score': 0,  # 0-15分
        'description': []
    }
    
    if len(df) < window:
        return result
    
    recent = df.tail(window)
    features = calculate_ohlc_features(recent)
    
    # 检测各种形态
    detected = []
    
    # 1. 头肩顶/底
    pattern = detect_head_shoulders(recent)
    if pattern['detected']:
        detected.append(pattern)
        result['score'] += pattern['score']
    
    # 2. 双重顶/底
    pattern = detect_double_top_bottom(recent)
    if pattern['detected']:
        detected.append(pattern)
        result['score'] += pattern['score']
    
    # 3. 三角形整理
    pattern = detect_triangle(recent)
    if pattern['detected']:
        detected.append(pattern)
        result['score'] += pattern['score']
    
    # 4. 旗形整理
    pattern = detect_flag(recent)
    if pattern['detected']:
        detected.append(pattern)
        result['score'] += pattern['score']
    
    # 5. 突破形态
    pattern = detect_breakout(recent)
    if pattern['detected']:
        detected.append(pattern)
        result['score'] += pattern['score']
    
    result['patterns'] = detected
    result['score'] = min(15, result['score'])  # 最高15分
    
    # 描述
    if result['score'] >= 12:
        result['description'].append('形态结构清晰，有利趋势延续')
    elif result['score'] >= 8:
        result['description'].append('存在一定形态结构，中性偏多')
    elif result['score'] >= 5:
        result['description'].append('形态结构不明显')
    else:
        result['description'].append('无明显形态结构')
    
    return result


def detect_head_shoulders(df: pd.DataFrame) -> Dict:
    """检测头肩顶/底"""
    result = {
        'detected': False,
        'type': None,  # 'head_shoulders', 'inverse_head_shoulders'
        'score': 0,
        'description': ''
    }
    
    if len(df) < 30:
        return result
    
    # 简化实现：检测高低点
    highs = df['high'].values
    lows = df['low'].values
    
    # 找局部极值点
    local_highs = []
    local_lows = []
    
    for i in range(2, len(df) - 2):
        if highs[i] > highs[i-1] and highs[i] > highs[i-2] and highs[i] > highs[i+1] and highs[i] > highs[i+2]:
            local_highs.append((i, highs[i]))
        if lows[i] < lows[i-1] and lows[i] < lows[i-2] and lows[i] < lows[i+1] and lows[i] < lows[i+2]:
            local_lows.append((i, lows[i]))
    
    # 头肩顶：左肩、头、右肩依次降低
    if len(local_highs) >= 3:
        last_three = local_highs[-3:]
        if last_three[0][1] > last_three[1][1] < last_three[2][1]:
            result['detected'] = True
            result['type'] = 'inverse_head_shoulders'
            result['score'] = 10
            result['description'] = '检测到头肩底形态'
        elif last_three[0][1] < last_three[1][1] > last_three[2][1]:
            result['detected'] = True
            result['type'] = 'head_shoulders'
            result['score'] = 10
            result['description'] = '检测到头肩顶形态'
    
    return result


def detect_double_top_bottom(df: pd.DataFrame) -> Dict:
    """检测双重顶/底"""
    result = {
        'detected': False,
        'type': None,  # 'double_top', 'double_bottom'
        'score': 0,
        'description': ''
    }
    
    if len(df) < 20:
        return result
    
    highs = df['high'].values
    lows = df['low'].values
    
    # 简化检测：最近两个高点接近且高于中间低点
    max_price = np.max(highs)
    max_idx = np.argmax(highs)
    
    # 寻找接近高点的其他位置
    near_max = np.where(highs > max_price * 0.98)[0]
    
    if len(near_max) >= 2 and max_idx - near_max[0] > 5:
        result['detected'] = True
        result['type'] = 'double_top'
        result['score'] = 8
        result['description'] = '检测到双重顶形态'
    
    # 双重底
    min_price = np.min(lows)
    min_idx = np.argmin(lows)
    near_min = np.where(lows < min_price * 1.02)[0]
    
    if len(near_min) >= 2 and min_idx - near_min[0] > 5:
        result['detected'] = True
        result['type'] = 'double_bottom'
        result['score'] = 8
        result['description'] = '检测到双重底形态'
    
    return result


def detect_triangle(df: pd.DataFrame) -> Dict:
    """检测三角形整理"""
    result = {
        'detected': False,
        'type': None,  # 'ascending', 'descending', 'symmetrical'
        'score': 0,
        'description': ''
    }
    
    if len(df) < 20:
        return result
    
    highs = df['high'].values
    lows = df['low'].values
    
    # 简化：连接高低点趋势线
    high_slope = np.polyfit(range(len(highs)), highs, 1)[0]
    low_slope = np.polyfit(range(len(lows)), lows, 1)[0]
    
    if high_slope < 0 and low_slope > 0:
        result['detected'] = True
        result['type'] = 'symmetrical'
        result['score'] = 6
        result['description'] = '检测到对称三角形整理'
    elif high_slope < 0 and low_slope >= 0:
        result['detected'] = True
        result['type'] = 'ascending'
        result['score'] = 7
        result['description'] = '检测到上升三角形整理'
    elif high_slope <= 0 and low_slope > 0:
        result['detected'] = True
        result['type'] = 'descending'
        result['score'] = 7
        result['description'] = '检测到下降三角形整理'
    
    return result


def detect_flag(df: pd.DataFrame) -> Dict:
    """检测旗形整理"""
    result = {
        'detected': False,
        'type': None,  # 'bullish_flag', 'bearish_flag'
        'score': 0,
        'description': ''
    }
    
    if len(df) < 15:
        return result
    
    # 简化检测：前期有明显趋势，后续整理
    first_half = df.iloc[:len(df)//2]
    second_half = df.iloc[len(df)//2:]
    
    first_trend = first_half['close'].iloc[-1] - first_half['close'].iloc[0]
    second_range = second_half['high'].max() - second_half['low'].min()
    first_range = first_half['high'].max() - first_half['low'].min()
    
    if abs(first_trend) > first_range * 1.5 and second_range < first_range * 0.6:
        if first_trend > 0:
            result['detected'] = True
            result['type'] = 'bullish_flag'
            result['score'] = 6
            result['description'] = '检测到上升旗形整理'
        else:
            result['detected'] = True
            result['type'] = 'bearish_flag'
            result['score'] = 6
            result['description'] = '检测到下降旗形整理'
    
    return result


def detect_breakout(df: pd.DataFrame) -> Dict:
    """检测突破形态"""
    result = {
        'detected': False,
        'direction': None,  # 'up', 'down'
        'score': 0,
        'description': ''
    }
    
    if len(df) < 20:
        return result
    
    recent = df.tail(10)
    base = df.iloc[:-10]
    
    # 近期突破前期高点/低点
    recent_high = recent['high'].max()
    recent_low = recent['low'].min()
    base_high = base['high'].max()
    base_low = base['low'].min()
    
    if recent_high > base_high:
        result['detected'] = True
        result['direction'] = 'up'
        result['score'] = 5
        result['description'] = '突破前期高点，形成上涨趋势'
    elif recent_low < base_low:
        result['detected'] = True
        result['direction'] = 'down'
        result['score'] = 5
        result['description'] = '跌破前期低点，形成下跌趋势'
    
    return result


def analyze_geometry_structure(df: pd.DataFrame) -> Dict:
    """
    综合几何结构分析
    返回 0-25 分
    """
    result = {
        'trend_line': {},
        'patterns': {},
        'total_score': 0,  # 0-25分
        'description': []
    }
    
    # 趋势线分析 (10分)
    trend = detect_trend_line(df)
    result['trend_line'] = trend
    result['total_score'] += trend['strength']
    result['description'].append(trend['description'])
    
    # 形态分析 (15分)
    patterns = detect_patterns(df)
    result['patterns'] = patterns
    result['total_score'] += patterns['score']
    result['description'].extend(patterns['description'])
    
    # 限制总分25分
    result['total_score'] = min(25, result['total_score'])
    
    return result


# 测试代码
if __name__ == '__main__':
    # 生成测试数据
    np.random.seed(42)
    n = 100
    
    # 模拟上涨趋势
    close = pd.Series(np.cumsum(np.random.randn(n) * 2 + 1) + 100)
    high = close + np.random.rand(n) * 5
    low = close - np.random.rand(n) * 5
    open_price = close - np.random.rand(n) * 3
    
    df = pd.DataFrame({
        'open': open_price,
        'high': high,
        'low': low,
        'close': close
    })
    
    print("K-line Geometry Structure Analysis Test")
    print("=" * 50)
    
    result = analyze_geometry_structure(df)
    print(f"\nTotal Score: {result['total_score']}/25")
    print(f"Description: {result['description']}")
