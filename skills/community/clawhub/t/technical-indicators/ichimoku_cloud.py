"""
Ichimoku Cloud (一目均衡表) 技术指标

一目均衡表包含 5 条线和云团 (云状区域):
1. 转换线 (Tenkan-sen): 9 周期最高价和最低价的平均值
2. 基准线 (Kijun-sen): 26 周期最高价和最低价的平均值
3. 先行跨度 A (Senkou Span A): (转换线 + 基准线) / 2, 向前平移 26 周期
4. 先行跨度 B (Senkou Span B): 52 周期最高价和最低价的平均值，向前平移 26 周期
5. 滞后跨度 (Chikou Span): 当前收盘价，向后平移 26 周期

云团 (Kumo): 先行跨度 A 和 B 之间的区域
- 当 Span A > Span B 时，云团为看涨 (通常显示为绿色)
- 当 Span A < Span B 时，云团为看跌 (通常显示为红色)

信号识别:
- 云团突破：价格从云团下方突破到上方 (看涨) 或从上方突破到下方 (看跌)
- 转换线/基准线交叉：转换线上穿基准线 (金叉看涨)，下穿 (死叉看跌)
- 价格相对云团位置：价格在云团上方 (看涨)，下方 (看跌)，内部 (震荡)
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
from datetime import datetime


def calculate_ichimoku(df: pd.DataFrame, 
                       conversion_period: int = 9,
                       base_period: int = 26,
                       span_b_period: int = 52,
                       displacement: int = 26) -> pd.DataFrame:
    """
    计算 Ichimoku Cloud (一目均衡表) 所有组件
    
    Args:
        df: 包含 'high', 'low', 'close' 列的 DataFrame
        conversion_period: 转换线周期 (默认 9)
        base_period: 基准线周期 (默认 26)
        span_b_period: 先行跨度 B 周期 (默认 52)
        displacement: 平移周期 (默认 26)
    
    Returns:
        包含原始数据和 Ichimoku 组件的 DataFrame
    """
    df = df.copy()
    
    # 1. 转换线 (Tenkan-sen): 9 周期最高价和最低价的平均值
    high_9 = df['high'].rolling(window=conversion_period).max()
    low_9 = df['low'].rolling(window=conversion_period).min()
    df['tenkan_sen'] = (high_9 + low_9) / 2
    
    # 2. 基准线 (Kijun-sen): 26 周期最高价和最低价的平均值
    high_26 = df['high'].rolling(window=base_period).max()
    low_26 = df['low'].rolling(window=base_period).min()
    df['kijun_sen'] = (high_26 + low_26) / 2
    
    # 3. 先行跨度 A (Senkou Span A): (转换线 + 基准线) / 2, 向前平移 26 周期
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(displacement)
    
    # 4. 先行跨度 B (Senkou Span B): 52 周期最高价和最低价的平均值，向前平移 26 周期
    high_52 = df['high'].rolling(window=span_b_period).max()
    low_52 = df['low'].rolling(window=span_b_period).min()
    df['senkou_span_b'] = ((high_52 + low_52) / 2).shift(displacement)
    
    # 5. 滞后跨度 (Chikou Span): 当前收盘价，向后平移 26 周期
    df['chikou_span'] = df['close'].shift(-displacement)
    
    return df


def identify_cloud_breakout(df: pd.DataFrame, displacement: int = 26) -> Dict:
    """
    识别云团突破信号
    
    Args:
        df: 包含 Ichimoku 组件的 DataFrame
        displacement: 平移周期
    
    Returns:
        突破信号字典
    """
    if len(df) < displacement + 5:
        return {"error": "数据不足，无法识别突破信号"}
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    # 当前云团状态 (使用 26 周期前的数据，因为云团是向前平移的)
    cloud_top = max(latest['senkou_span_a'], latest['senkou_span_b'])
    cloud_bottom = min(latest['senkou_span_a'], latest['senkou_span_b'])
    
    # 云团颜色 (Span A 相对 Span B 的位置)
    cloud_color = "bullish" if latest['senkou_span_a'] > latest['senkou_span_b'] else "bearish"
    
    # 价格相对云团位置
    current_price = latest['close']
    prev_price = prev['close']
    
    if current_price > cloud_top:
        price_position = "above_cloud"
    elif current_price < cloud_bottom:
        price_position = "below_cloud"
    else:
        price_position = "inside_cloud"
    
    # 检测突破信号
    breakout_signal = None
    
    # 从下向上突破云团
    if prev_price <= cloud_bottom and current_price > cloud_top:
        breakout_signal = "bullish_breakout"
    # 从上向下突破云团
    elif prev_price >= cloud_top and current_price < cloud_bottom:
        breakout_signal = "bearish_breakout"
    # 进入云团
    elif prev_price > cloud_top and current_price < cloud_top and current_price > cloud_bottom:
        breakout_signal = "entering_cloud_from_above"
    elif prev_price < cloud_bottom and current_price > cloud_bottom and current_price < cloud_top:
        breakout_signal = "entering_cloud_from_below"
    
    return {
        "cloud_color": cloud_color,
        "cloud_top": round(cloud_top, 2) if not pd.isna(cloud_top) else None,
        "cloud_bottom": round(cloud_bottom, 2) if not pd.isna(cloud_bottom) else None,
        "price_position": price_position,
        "breakout_signal": breakout_signal,
        "current_price": round(current_price, 2),
        "timestamp": df.index[-1] if hasattr(df.index[-1], 'isoformat') else str(df.index[-1])
    }


def identify_tk_cross(df: pd.DataFrame) -> Dict:
    """
    识别转换线 (Tenkan) 和基准线 (Kijun) 交叉信号
    
    Args:
        df: 包含 Ichimoku 组件的 DataFrame
    
    Returns:
        交叉信号字典
    """
    if len(df) < 2:
        return {"error": "数据不足"}
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    tenkan = latest['tenkan_sen']
    kijun = latest['kijun_sen']
    tenkan_prev = prev['tenkan_sen']
    kijun_prev = prev['kijun_sen']
    
    cross_signal = None
    
    # 金叉：转换线从下向上穿过基准线
    if tenkan_prev <= kijun_prev and tenkan > kijun:
        cross_signal = "golden_cross"
    # 死叉：转换线从上向下穿过基准线
    elif tenkan_prev >= kijun_prev and tenkan < kijun:
        cross_signal = "death_cross"
    
    # 相对位置
    if pd.notna(tenkan) and pd.notna(kijun):
        tk_position = "tenkan_above" if tenkan > kijun else "tenkan_below"
    else:
        tk_position = "unknown"
    
    return {
        "cross_signal": cross_signal,
        "tk_position": tk_position,
        "tenkan_sen": round(tenkan, 2) if pd.notna(tenkan) else None,
        "kijun_sen": round(kijun, 2) if pd.notna(kijun) else None,
        "tenkan_prev": round(tenkan_prev, 2) if pd.notna(tenkan_prev) else None,
        "kijun_prev": round(kijun_prev, 2) if pd.notna(kijun_prev) else None,
        "timestamp": df.index[-1] if hasattr(df.index[-1], 'isoformat') else str(df.index[-1])
    }


def identify_chikou_signal(df: pd.DataFrame, displacement: int = 26) -> Dict:
    """
    识别滞后跨度 (Chikou Span) 信号
    
    Args:
        df: 包含 Ichimoku 组件的 DataFrame
        displacement: 平移周期
    
    Returns:
        滞后跨度信号字典
    """
    if len(df) < displacement * 2:
        return {"error": "数据不足"}
    
    latest = df.iloc[-1]
    
    chikou = latest['chikou_span']
    current_price = latest['close']
    
    # 滞后跨度相对 26 周期前价格的位置
    price_26_ago = df.iloc[-displacement]['close'] if len(df) > displacement else None
    
    # 滞后跨度相对云团的位置 (需要看 26 周期前的云团)
    if len(df) > displacement:
        span_a_26_ago = df.iloc[-displacement]['senkou_span_a']
        span_b_26_ago = df.iloc[-displacement]['senkou_span_b']
        
        if pd.notna(span_a_26_ago) and pd.notna(span_b_26_ago):
            cloud_top_26_ago = max(span_a_26_ago, span_b_26_ago)
            cloud_bottom_26_ago = min(span_a_26_ago, span_b_26_ago)
            
            if chikou > cloud_top_26_ago:
                chikou_position = "above_cloud"
            elif chikou < cloud_bottom_26_ago:
                chikou_position = "below_cloud"
            else:
                chikou_position = "inside_cloud"
        else:
            chikou_position = "unknown"
    else:
        chikou_position = "unknown"
    
    # 信号强度
    signal_strength = "strong" if chikou_position == "above_cloud" else ("weak" if chikou_position == "below_cloud" else "neutral")
    
    return {
        "chikou_span": round(chikou, 2) if pd.notna(chikou) else None,
        "price_26_ago": round(price_26_ago, 2) if price_26_ago is not None else None,
        "chikou_position": chikou_position,
        "signal_strength": signal_strength,
        "timestamp": df.index[-1] if hasattr(df.index[-1], 'isoformat') else str(df.index[-1])
    }


def get_ichimoku_summary(df: pd.DataFrame) -> Dict:
    """
    获取 Ichimoku Cloud 综合分析报告
    
    Args:
        df: 包含 Ichimoku 组件的 DataFrame
    
    Returns:
        综合分析报告
    """
    if len(df) < 52:
        return {"error": "数据不足，需要至少 52 个周期"}
    
    # 计算所有组件
    df = calculate_ichimoku(df)
    
    # 获取最新数据
    latest = df.iloc[-1]
    
    # 云团突破信号
    cloud_signal = identify_cloud_breakout(df)
    
    # TK 交叉信号
    tk_signal = identify_tk_cross(df)
    
    # 滞后跨度信号
    chikou_signal = identify_chikou_signal(df)
    
    # 综合趋势判断
    bullish_signals = 0
    bearish_signals = 0
    
    # 云团颜色
    if cloud_signal.get('cloud_color') == 'bullish':
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # 价格位置
    if cloud_signal.get('price_position') == 'above_cloud':
        bullish_signals += 2
    elif cloud_signal.get('price_position') == 'below_cloud':
        bearish_signals += 2
    
    # TK 交叉
    if tk_signal.get('tk_position') == 'tenkan_above':
        bullish_signals += 1
    else:
        bearish_signals += 1
    
    # 滞后跨度
    if chikou_signal.get('signal_strength') == 'strong':
        bullish_signals += 1
    elif chikou_signal.get('signal_strength') == 'weak':
        bearish_signals += 1
    
    # 总体趋势
    if bullish_signals > bearish_signals + 2:
        overall_trend = "strong_bullish"
    elif bullish_signals > bearish_signals:
        overall_trend = "bullish"
    elif bearish_signals > bullish_signals + 2:
        overall_trend = "strong_bearish"
    else:
        overall_trend = "neutral"
    
    return {
        "timestamp": datetime.now().isoformat(),
        "current_price": round(latest['close'], 2),
        "tenkan_sen": round(latest['tenkan_sen'], 2) if pd.notna(latest['tenkan_sen']) else None,
        "kijun_sen": round(latest['kijun_sen'], 2) if pd.notna(latest['kijun_sen']) else None,
        "senkou_span_a": round(latest['senkou_span_a'], 2) if pd.notna(latest['senkou_span_a']) else None,
        "senkou_span_b": round(latest['senkou_span_b'], 2) if pd.notna(latest['senkou_span_b']) else None,
        "chikou_span": round(latest['chikou_span'], 2) if pd.notna(latest['chikou_span']) else None,
        "cloud_analysis": cloud_signal,
        "tk_cross_analysis": tk_signal,
        "chikou_analysis": chikou_signal,
        "bullish_signals": bullish_signals,
        "bearish_signals": bearish_signals,
        "overall_trend": overall_trend,
        "recommendation": "买入" if overall_trend in ["strong_bullish", "bullish"] else ("卖出" if overall_trend in ["strong_bearish", "bearish"] else "观望")
    }


def get_all_ichimoku_parameters(df: pd.DataFrame) -> Dict:
    """
    获取一目均衡表的 9 个参数
    
    Returns:
        包含 9 个参数的字典:
        - 转换线 (Tenkan-sen)
        - 基准线 (Kijun-sen)
        - 先行跨度 A (Senkou Span A)
        - 先行跨度 B (Senkou Span B)
        - 滞后跨度 (Chikou Span)
        - 云团顶部
        - 云团底部
        - 云团颜色
        - 价格相对云团位置
    """
    df = calculate_ichimoku(df)
    latest = df.iloc[-1]
    
    cloud_signal = identify_cloud_breakout(df)
    
    return {
        "转换线": round(latest['tenkan_sen'], 2) if pd.notna(latest['tenkan_sen']) else None,
        "基准线": round(latest['kijun_sen'], 2) if pd.notna(latest['kijun_sen']) else None,
        "先行跨度 A": round(latest['senkou_span_a'], 2) if pd.notna(latest['senkou_span_a']) else None,
        "先行跨度 B": round(latest['senkou_span_b'], 2) if pd.notna(latest['senkou_span_b']) else None,
        "滞后跨度": round(latest['chikou_span'], 2) if pd.notna(latest['chikou_span']) else None,
        "云团顶部": cloud_signal.get('cloud_top'),
        "云团底部": cloud_signal.get('cloud_bottom'),
        "云团颜色": cloud_signal.get('cloud_color'),
        "价格相对云团位置": cloud_signal.get('price_position')
    }


if __name__ == "__main__":
    # 使用示例
    print("=" * 60)
    print("Ichimoku Cloud (一目均衡表) 使用示例")
    print("=" * 60)
    
    # 创建示例数据
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    prices = 100 + np.cumsum(np.random.randn(100) * 2)
    
    df = pd.DataFrame({
        'date': dates,
        'open': prices + np.random.randn(100) * 0.5,
        'high': prices + np.abs(np.random.randn(100)) * 1.5,
        'low': prices - np.abs(np.random.randn(100)) * 1.5,
        'close': prices,
        'volume': np.random.randint(1000000, 5000000, 100)
    })
    df.set_index('date', inplace=True)
    
    # 计算 Ichimoku
    df_ichimoku = calculate_ichimoku(df)
    
    print("\n1. 计算所有组件:")
    print(df_ichimoku[['close', 'tenkan_sen', 'kijun_sen', 'senkou_span_a', 'senkou_span_b', 'chikou_span']].tail())
    
    print("\n2. 获取 9 个参数:")
    params = get_all_ichimoku_parameters(df)
    for key, value in params.items():
        print(f"   {key}: {value}")
    
    print("\n3. 综合分析报告:")
    summary = get_ichimoku_summary(df)
    print(f"   当前价格：{summary.get('current_price')}")
    print(f"   总体趋势：{summary.get('overall_trend')}")
    print(f"   建议：{summary.get('recommendation')}")
    print(f"   看涨信号数：{summary.get('bullish_signals')}")
    print(f"   看跌信号数：{summary.get('bearish_signals')}")
    
    print("\n4. 云团突破信号:")
    cloud = identify_cloud_breakout(df_ichimoku)
    print(f"   云团颜色：{cloud.get('cloud_color')}")
    print(f"   价格位置：{cloud.get('price_position')}")
    print(f"   突破信号：{cloud.get('breakout_signal')}")
    
    print("\n5. TK 交叉信号:")
    tk = identify_tk_cross(df_ichimoku)
    print(f"   交叉信号：{tk.get('cross_signal')}")
    print(f"   当前位置：{tk.get('tk_position')}")
