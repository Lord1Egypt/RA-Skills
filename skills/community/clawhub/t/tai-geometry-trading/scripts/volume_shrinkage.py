#!/usr/bin/env python3
"""
Volume Shrinkage & Volatility Analysis Script
缩量短线与波动率分析

定义：缩量短线 = 当前周期成交量和波动幅度都比前期明显缩减
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """计算ATR（平均真实波幅）"""
    high = df['high']
    low = df['low']
    close = df['close']
    
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    return atr


def analyze_shrinkage(df: pd.DataFrame, lookback: int = 30) -> Dict:
    """
    分析缩量短线
    
    比较近期(最后10天)和前期(11-30天)的：
    1. 波动幅度（用ATR或价格振幅）
    2. 成交量
    
    只有两者都收缩才算缩量短线
    """
    result = {
        'is_shrinkage': False,
        'volume_shrink': 0,   # 成交量收缩比例
        'volatility_shrink': 0,  # 波动率收缩比例
        'score': 0,  # 0-15分
        'description': ''
    }
    
    if len(df) < lookback:
        result['description'] = '数据不足'
        return result
    
    # 分割为近期(最后10天)和前期(11-30天)
    recent = df.tail(10)
    earlier = df.iloc[-lookback:-10]
    
    if len(recent) < 5 or len(earlier) < 5:
        result['description'] = '数据不足'
        return result
    
    # 计算波动幅度（用价格振幅）
    recent_range = (recent['high'].max() - recent['low'].min()) / recent['close'].mean()
    earlier_range = (earlier['high'].max() - earlier['low'].min()) / earlier['close'].mean()
    
    # 计算成交量
    recent_vol = recent['volume'].mean()
    earlier_vol = earlier['volume'].mean()
    
    # 收缩比例
    volume_shrink = recent_vol / earlier_vol if earlier_vol > 0 else 1
    volatility_shrink = recent_range / earlier_range if earlier_range > 0 else 1
    
    result['volume_shrink'] = volume_shrink
    result['volatility_shrink'] = volatility_shrink
    
    # 判断标准：
    # 成交量收缩到前期的80%以下
    # 波动幅度收缩到前期的85%以下
    # 两者都满足才算缩量短线
    
    is_vol_shrink = volume_shrink < 0.8
    is_vol_shrink_60 = volume_shrink < 0.6
    
    is_volatility_shrink = volatility_shrink < 0.85
    is_volatility_shrink_70 = volatility_shrink < 0.7
    
    if is_vol_shrink and is_volatility_shrink:
        # 两者都收缩
        if is_vol_shrink_60 and is_volatility_shrink_70:
            result['is_shrinkage'] = True
            result['score'] = 15
            result['description'] = f'成交量缩至{volume_shrink*100:.0f}%,波动降至{volatility_shrink*100:.0f}%'
        else:
            result['is_shrinkage'] = True
            result['score'] = 12
            result['description'] = f'成交量缩至{volume_shrink*100:.0f}%,波动降至{volatility_shrink*100:.0f}%'
    elif is_vol_shrink or is_volatility_shrink:
        # 只有一个收缩，给部分分数
        result['is_shrinkage'] = False
        result['score'] = 5
        result['description'] = f'成交量{volume_shrink*100:.0f}%,波动{volatility_shrink*100:.0f}%'
    else:
        # 都没有收缩
        result['is_shrinkage'] = False
        result['score'] = 0
        result['description'] = f'成交量{volume_shrink*100:.0f}%,波动{volatility_shrink*100:.0f}%'
    
    return result


def analyze_multi_period_shrinkage(data_dict: Dict[str, pd.DataFrame]) -> Dict:
    """
    多周期缩量短线分析
    周期: 日线, 2日线, 周线, 8日线
    """
    result = {
        'daily': {},
        '2daily': {},
        'weekly': {},
        '8daily': {},
        'total_score': 0,  # 0-15分
        'shrinkage_count': 0,
        'description': []
    }
    
    periods = ['daily', '2daily', 'weekly', '8daily']
    
    for period in periods:
        if period not in data_dict:
            continue
        
        df = data_dict[period]
        
        # 使用不同的回溯周期
        if period == '8daily':
            lookback = 12  # 8日线用12个周期
        elif period == '2daily':
            lookback = 15  # 2日线用15个周期
        elif period == 'weekly':
            lookback = 30  # 周线用30周
        else:
            lookback = 30  # 日线用30天
        
        shrinkage = analyze_shrinkage(df, lookback)
        result[period] = shrinkage
        
        if shrinkage['is_shrinkage']:
            result['shrinkage_count'] += 1
    
    # 计算总分：取最高分，不累加
    max_score = 0
    for period in periods:
        if period in result:
            max_score = max(max_score, result[period].get('score', 0))
    result['total_score'] = max_score
    
    if result['shrinkage_count'] >= 3:
        result['description'].append(f'{result["shrinkage_count"]}周期同时缩量，强信号')
    else:
        result['description'].append(f'{result["shrinkage_count"]}周期缩量')
    
    return result


# 测试
if __name__ == '__main__':
    import numpy as np
    import pandas as pd
    
    # 测试1：缩量
    np.random.seed(42)
    n = 50
    
    # 前期波动大成交量大
    high1 = 100 + np.cumsum(np.random.randn(20) * 2)
    low1 = high1 - np.abs(np.random.randn(20) * 3)
    close1 = (high1 + low1) / 2 + np.random.randn(20)
    vol1 = np.random.rand(20) * 1000000 + 800000
    
    # 近期波动小成交量小
    high2 = [105 + i * 0.1 for i in range(10)]
    low2 = [104 + i * 0.1 for i in range(10)]
    close2 = [(high2[i] + low2[i]) / 2 for i in range(10)]
    vol2 = np.random.rand(10) * 300000 + 300000
    
    df = pd.DataFrame({
        'high': list(high1) + high2,
        'low': list(low1) + low2,
        'close': list(close1) + close2,
        'volume': list(vol1) + vol2
    })
    
    result = analyze_shrinkage(df)
    print("缩量测试:", result)
    
    # 测试2：放量
    vol_large = np.random.rand(30) * 1000000 + 1000000
    df2 = pd.DataFrame({
        'high': 100 + np.cumsum(np.random.randn(30) * 3),
        'low': 95 + np.cumsum(np.random.randn(30) * 3),
        'close': 98 + np.cumsum(np.random.randn(30) * 2),
        'volume': vol_large
    })
    
    result2 = analyze_shrinkage(df2)
    print("放量测试:", result2)
