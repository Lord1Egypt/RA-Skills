#!/usr/bin/env python3
"""
MACD Wind Tunnel Analysis Script - 修正版
多周期MACD风洞结构共振分析

核心逻辑：
1. 风洞结构 = 必要条件（不决定方向）
2. 零轴金叉/死叉 = 决定方向（在更小周期判断）
3. 风洞 + 零轴交叉同时满足 = 完整MACD风洞信号
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional


def calculate_macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """计算MACD指标"""
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line  # 红绿柱体
    
    return pd.DataFrame({
        'macd': macd_line,
        'signal': signal_line,
        'histogram': histogram
    })


def detect_histogram_tunnel(histogram: pd.Series, lookback: int = 40) -> Dict:
    """
    检测MACD红绿柱体是否形成风洞结构
    
    上涨风洞：红柱持续扩大→缩小到绿→再变红（完整三段）
    下跌风洞：绿柱持续扩大→缩小到红→再变绿（完整三段）
    
    注意：风洞结构不决定方向，只判断是否形成风洞
    """
    result = {
        'has_tunnel': False,
        'tunnel_type': None,  # 'up_tunnel', 'down_tunnel'
        'strength': 0,  # 0-10
        'description': ''
    }
    
    if len(histogram) < 20:
        return result
    
    hist = histogram.tail(lookback).values
    
    # 找红柱区域和绿柱区域
    red_indices = np.where(hist > 0)[0]
    green_indices = np.where(hist < 0)[0]
    
    if len(red_indices) == 0 or len(green_indices) == 0:
        result['description'] = '未形成红绿转换'
        return result
    
    # 上涨风洞：红柱→绿柱→红柱（需要完整三段）
    # 特征：开头是红柱，中间变绿，结尾又变红
    first_red = red_indices[0]
    last_red = red_indices[-1]
    first_green = green_indices[0]
    
    # 红柱在前面，绿柱在中间，后面又有红柱
    if first_red < first_green < last_red:
        # 检查红柱是否先扩大
        red_first_part = hist[red_indices[red_indices < first_green]]
        if len(red_first_part) >= 3:
            # 检查是否是扩大趋势
            is_expanding = all(red_first_part[i] < red_first_part[i+1] for i in range(len(red_first_part)-1))
            if is_expanding:
                green_min = hist[green_indices].min()
                if green_min < -0.01:  # 绿柱有深度
                    # 检查最后是否重新变红并扩大
                    red_last_part = hist[last_red:]
                    if len(red_last_part) >= 2 and red_last_part[-1] > red_last_part[0]:
                        result['has_tunnel'] = True
                        result['tunnel_type'] = 'up_tunnel'
                        result['strength'] = min(10, 7 + int(abs(green_min) * 5))
                        result['description'] = f'上涨风洞(绿深:{abs(green_min):.2f})'
                        return result
    
    # 下跌风洞：绿柱→红柱→绿柱（需要完整三段）
    first_green = green_indices[0]
    last_green = green_indices[-1]
    first_red = red_indices[0]
    
    if first_green < first_red < last_green:
        # 检查绿柱是否先扩大
        green_first_part = hist[green_indices[green_indices < first_red]]
        if len(green_first_part) >= 3:
            is_expanding = all(green_first_part[i] > green_first_part[i+1] for i in range(len(green_first_part)-1))
            if is_expanding:
                red_max = hist[red_indices].max()
                if red_max > 0.01:
                    # 检查最后是否重新变绿并扩大
                    green_last_part = hist[last_green:]
                    if len(green_last_part) >= 2 and green_last_part[-1] < green_last_part[0]:
                        result['has_tunnel'] = True
                        result['tunnel_type'] = 'down_tunnel'
                        result['strength'] = min(10, 7 + int(red_max * 5))
                        result['description'] = f'下跌风洞(红高:{red_max:.2f})'
                        return result
    
    result['description'] = '未形成风洞结构'
    return result


def detect_zero_cross_simple(macd_line: pd.Series, lookback: int = 20) -> Dict:
    """
    简化的零轴交叉检测 - 在本周期内判断
    
    返回：方向信号（看涨/看跌）
    """
    result = {
        'has_cross': False,
        'cross_type': None,  # 'golden_cross', 'death_cross'
        'strength': 0,  # 0-15
        'description': ''
    }
    
    if len(macd_line) < 5:
        return result
    
    macd = macd_line.tail(lookback).values
    
    # 从后往前找金叉/死叉
    for i in range(len(macd) - 1, 0, -1):
        # 金叉：MACD从负变正
        if macd[i-1] <= 0 and macd[i] > 0:
            result['has_cross'] = True
            result['cross_type'] = 'golden_cross'
            # 越近越强
            result['strength'] = min(15, 10 + (lookback - i))
            result['description'] = f'MACD零轴金叉(距今{lookback-i}根)'
            return result
        # 死叉：MACD从正变负
        elif macd[i-1] >= 0 and macd[i] < 0:
            result['has_cross'] = True
            result['cross_type'] = 'death_cross'
            result['strength'] = min(15, 10 + (lookback - i))
            result['description'] = f'MACD零轴死叉(距今{lookback-i}根)'
            return result
    
    # 无金叉死叉，看当前位置
    if macd[-1] > 0:
        result['description'] = 'MACD在零轴上方运行'
    else:
        result['description'] = 'MACD在零轴下方运行'
    
    return result


def get_smaller_period(period: str) -> str:
    """获取更小周期用于零轴判断"""
    mapping = {
        'monthly': '8daily',   # 月线用8日线判断
        'weekly': '2daily',    # 周线用2日线判断
        'daily': '90min',     # 日线用90分钟周期
    }
    return mapping.get(period, 'daily')


def analyze_single_period_macd(df: pd.DataFrame, period: str, smaller_df: pd.DataFrame = None, use_approx: bool = False) -> Dict:
    """
    分析单个周期的MACD信号
    
    逻辑：
    1. 检测本周期是否形成风洞结构
    2. 用更小周期判断零轴交叉方向
    3. 风洞+零轴同时满足 = 完整信号
    
    周期对应：
    - 月线 → 用8日线判断零轴
    - 周线 → 用2日线判断零轴
    - 日线 → 用90分钟判断零轴
    """
    result = {
        'period': period,
        'has_tunnel': False,
        'tunnel_type': None,
        'tunnel_strength': 0,
        'has_zero_cross': False,
        'zero_cross_type': None,
        'zero_cross_strength': 0,
        'direction': None,  # 'bullish', 'bearish', None
        'score': 0,
        'description': []
    }
    
    # 1. 检测本周期的风洞结构
    macd_df = calculate_macd(df['close'])
    tunnel = detect_histogram_tunnel(macd_df['histogram'])
    
    result['has_tunnel'] = tunnel['has_tunnel']
    result['tunnel_type'] = tunnel['tunnel_type']
    result['tunnel_strength'] = tunnel['strength']
    if tunnel['description']:
        result['description'].append(tunnel['description'])
    
    # 2. 检测零轴交叉
    # 如果有更小周期数据，用更小周期判断
    # 如果没有更小周期数据，且是日线，用日线自己的MACD判断
    # 月线和周线必须用更小周期
    if smaller_df is not None:
        smaller_macd = calculate_macd(smaller_df['close'])
        zero_cross = detect_zero_cross_simple(smaller_macd['macd'])
    else:
        # 没有更小周期数据的情况
        # 日线：用自己MACD判断
        # 月线/周线：没有更小周期则无法判断
        if period == 'daily':
            # 日线用自己的MACD
            zero_cross = detect_zero_cross_simple(macd_df['macd'])
            zero_cross['description'] += '(日线自身MACD)'
        else:
            # 月线/周线没有更小周期
            zero_cross = {'has_cross': False, 'cross_type': None, 'strength': 0, 'description': '无更小周期数据'}
    
    result['has_zero_cross'] = zero_cross['has_cross']
    result['zero_cross_type'] = zero_cross['cross_type']
    result['zero_cross_strength'] = zero_cross['strength']
    if zero_cross['description']:
        result['description'].append(zero_cross['description'])
    
    # 3. 决定方向
    if result['has_zero_cross']:
        # 有零轴交叉信号
        if result['zero_cross_type'] == 'golden_cross':
            result['direction'] = 'bullish'
            result['score'] = result['zero_cross_strength']
        else:
            result['direction'] = 'bearish'
            result['score'] = result['zero_cross_strength']
        
        # 风洞加分
        if result['has_tunnel']:
            result['score'] = min(15, result['score'] + result['tunnel_strength'])
            result['description'].append(f'✓ 风洞+{"金叉" if result["direction"]=="bullish" else "死叉"}')
    elif result['has_tunnel']:
        # 有风洞，没有零轴信号
        # 日线可以用自己MACD位置判断，月线周线不行
        if period == 'daily':
            # 日线用自己的MACD
            if macd_df['macd'].iloc[-1] > 0:
                result['direction'] = 'bullish'
                result['score'] = min(15, result['tunnel_strength'] + 5)
                result['description'].append('日线MACD在零轴上方')
            else:
                result['direction'] = 'bearish'
                result['score'] = min(15, result['tunnel_strength'] + 5)
                result['description'].append('日线MACD在零轴下方')
        else:
            # 月线/周线没有零轴信号
            result['score'] = result['tunnel_strength'] // 2
            result['description'].append('仅有风洞，无零轴信号')
    else:
        # 没有风洞也没有零轴
        if period == 'daily':
            # 日线用自己的MACD位置
            if macd_df['macd'].iloc[-1] > 0:
                result['direction'] = 'bullish'
                result['score'] = 5
                result['description'].append('日线MACD零轴上方')
            else:
                result['direction'] = 'bearish'
                result['score'] = 5
                result['description'].append('日线MACD零轴下方')
        else:
            result['score'] = 3
            result['description'].append('无明显信号')
    
    return result


def analyze_multi_period_macd(data_dict: Dict[str, pd.DataFrame]) -> Dict:
    """
    多周期MACD分析
    
    周期关系：
    - 日线的更小周期用120分钟（需要额外数据，暂时用周线替代）
    - 周线的更小周期用日线
    - 月线的更小周期用周线
    """
    analysis = {
        'monthly': {},
        'weekly': {},
        'daily': {},
        'resonance_score': 0,  # 0-30分
        'resonance_type': None,  # 'bullish', 'bearish', 'neutral'
        'description': []
    }
    
    # 配置周期关系
    # 月线用8日线判断零轴方向
    # 周线用2日线判断零轴方向
    # 日线用90分钟判断零轴方向
    period_config = {
        'monthly': {'self': 'monthly', 'smaller': '8daily'},
        'weekly': {'self': 'weekly', 'smaller': '2daily'},
        'daily': {'self': 'daily', 'smaller': '90min'}
    }
    
    bullish_count = 0
    bearish_count = 0
    total_score = 0
    
    for period in ['monthly', 'weekly', 'daily']:
        if period not in data_dict:
            continue
        
        config = period_config[period]
        df = data_dict[period]
        
        # 获取更小周期数据
        # 如果没有更小周期数据，用本周期的MACD近似判断（需标注）
        smaller_df = None
        if config['smaller'] and config['smaller'] in data_dict:
            smaller_df = data_dict[config['smaller']]
        
        # 标记是否使用近似判断
        use_approx = smaller_df is None
        result = analyze_single_period_macd(df, period, smaller_df, use_approx=use_approx)
        analysis[period] = result
        
        # 统计
        if result['direction'] == 'bullish':
            bullish_count += 1
            total_score += result['score']
        elif result['direction'] == 'bearish':
            bearish_count += 1
            total_score -= result['score']
    
    # 计算最终得分 - 看跌时返回负数
    # 最终得分范围：-30 到 30
    
    # 多周期共振判断
    if bullish_count >= 2 and bullish_count > bearish_count:
        analysis['resonance_score'] = min(30, int(total_score))
        analysis['resonance_type'] = 'bullish'
        analysis['description'].append(f'多周期共振看涨({int(bullish_count)}个周期)')
    elif bearish_count >= 2 and bearish_count > bullish_count:
        analysis['resonance_score'] = -min(30, int(abs(total_score)))  # 看跌返回负数
        analysis['resonance_type'] = 'bearish'
        analysis['description'].append(f'多周期共振看跌({int(bearish_count)}个周期)')
    elif bullish_count >= 1 and bullish_count > bearish_count:
        analysis['resonance_score'] = min(30, int(total_score))
        analysis['resonance_type'] = 'bullish'
        analysis['description'].append('偏多看涨')
    elif bearish_count >= 1 and bearish_count > bullish_count:
        analysis['resonance_score'] = -min(30, int(abs(total_score)))
        analysis['resonance_type'] = 'bearish'
        analysis['description'].append('偏空看跌')
    else:
        analysis['resonance_score'] = 5
        analysis['resonance_type'] = 'neutral'
        analysis['description'].append('信号不明显')
    
    return analysis


# 测试
if __name__ == '__main__':
    import pandas as pd
    import numpy as np
    
    np.random.seed(42)
    
    # 模拟上涨趋势 + 金叉
    prices = [100.0]
    for i in range(30):
        prices.append(prices[-1] + 0.5)
    for i in range(15):
        prices.append(prices[-1] - 0.4)
    for i in range(25):
        prices.append(prices[-1] + 0.6)
    
    close = pd.Series(prices)
    df = pd.DataFrame({'close': close})
    
    result = analyze_single_period_macd(df, 'daily')
    print("单周期分析:")
    print(f"  风洞: {result['has_tunnel']}, {result['tunnel_type']}")
    print(f"  零轴: {result['has_zero_cross']}, {result['zero_cross_type']}")
    print(f"  方向: {result['direction']}")
    print(f"  得分: {result['score']}")
    print(f"  描述: {result['description']}")
