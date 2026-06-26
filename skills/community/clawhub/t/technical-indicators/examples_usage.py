"""
技术指标 L2 使用示例

本文件演示如何使用三个高级技术指标:
1. Ichimoku Cloud (一目均衡表)
2. VWAP (成交量加权平均价)
3. SuperTrend (超级趋势)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 导入指标模块
from ichimoku_cloud import (
    calculate_ichimoku,
    get_all_ichimoku_parameters,
    get_ichimoku_summary,
    identify_cloud_breakout,
    identify_tk_cross
)

from vwap import (
    calculate_vwap,
    calculate_vwap_intraday,
    identify_vwap_position,
    get_vwap_summary
)

from supertrend import (
    calculate_supertrend,
    get_supertrend_summary,
    identify_trend_reversal
)


# ============================================================
# 示例 1: Ichimoku Cloud (一目均衡表)
# ============================================================

def example_ichimoku():
    """Ichimoku Cloud 使用示例"""
    print("=" * 70)
    print("示例 1: Ichimoku Cloud (一目均衡表)")
    print("=" * 70)
    
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
    
    # 方法 1: 获取 9 个参数
    print("\n【获取 9 个参数】")
    params = get_all_ichimoku_parameters(df)
    for key, value in params.items():
        print(f"  {key}: {value}")
    
    # 方法 2: 获取综合分析报告
    print("\n【综合分析报告】")
    summary = get_ichimoku_summary(df)
    print(f"  当前价格：{summary['current_price']}")
    print(f"  总体趋势：{summary['overall_trend']}")
    print(f"  操作建议：{summary['recommendation']}")
    print(f"  看涨信号：{summary['bullish_signals']}")
    print(f"  看跌信号：{summary['bearish_signals']}")
    
    # 方法 3: 识别云团突破
    print("\n【云团突破信号】")
    df_ichimoku = calculate_ichimoku(df)
    cloud = identify_cloud_breakout(df_ichimoku)
    print(f"  云团颜色：{cloud['cloud_color']}")
    print(f"  价格位置：{cloud['price_position']}")
    print(f"  突破信号：{cloud['breakout_signal']}")
    
    # 方法 4: 识别 TK 交叉
    print("\n【TK 交叉信号】")
    tk = identify_tk_cross(df_ichimoku)
    print(f"  交叉信号：{tk['cross_signal']}")
    print(f"  当前位置：{tk['tk_position']}")
    
    return df


# ============================================================
# 示例 2: VWAP (成交量加权平均价)
# ============================================================

def example_vwap_daily():
    """VWAP 使用示例 (日线数据)"""
    print("\n" + "=" * 70)
    print("示例 2: VWAP (成交量加权平均价) - 日线数据")
    print("=" * 70)
    
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
    
    # 计算 VWAP
    df_vwap = calculate_vwap(df)
    
    print("\n【VWAP 计算结果 (最后 5 条)】")
    print(df_vwap[['close', 'volume', 'vwap']].tail())
    
    # 获取价格相对 VWAP 位置
    print("\n【价格相对 VWAP 位置】")
    position = identify_vwap_position(df_vwap)
    print(f"  位置：{position['position_cn']}")
    print(f"  偏离度：{position['deviation_percent']}%")
    print(f"  穿越信号：{position['cross_signal_cn']}")
    
    # 获取综合报告
    print("\n【综合分析报告】")
    summary = get_vwap_summary(df)
    print(f"  当前价格：{summary['current_price']}")
    print(f"  当前 VWAP: {summary['current_vwap']}")
    print(f"  趋势：{summary['trend_cn']}")
    print(f"  建议：{summary['recommendation']}")
    
    return df


def example_vwap_intraday():
    """VWAP 使用示例 (日内分钟数据)"""
    print("\n" + "=" * 70)
    print("示例 3: VWAP (成交量加权平均价) - 日内分钟数据")
    print("=" * 70)
    
    # 创建日内数据
    np.random.seed(42)
    n_minutes = 240
    base_time = pd.Timestamp('2024-03-14 09:30:00')
    times = [base_time + pd.Timedelta(minutes=i) for i in range(n_minutes)]
    
    base_price = 100
    prices = base_price + np.cumsum(np.random.randn(n_minutes) * 0.3) + np.linspace(0, 2, n_minutes)
    
    volume_pattern = np.sin(np.linspace(0, np.pi, n_minutes)) + 1
    volumes = (volume_pattern * np.random.uniform(0.8, 1.2, n_minutes) * 10000).astype(int)
    
    df = pd.DataFrame({
        'datetime': times,
        'open': prices + np.random.randn(n_minutes) * 0.2,
        'high': prices + np.abs(np.random.randn(n_minutes)) * 0.5,
        'low': prices - np.abs(np.random.randn(n_minutes)) * 0.5,
        'close': prices,
        'volume': volumes
    })
    
    # 计算日内 VWAP
    df_vwap = calculate_vwap_intraday(df)
    
    print("\n【日内 VWAP 计算结果 (最后 5 条)】")
    print(df_vwap[['datetime', 'close', 'volume', 'vwap']].tail())
    
    # 分析
    position = identify_vwap_position(df_vwap)
    print(f"\n  当前位置：{position['position_cn']}")
    print(f"  偏离度：{position['deviation_percent']}%")
    
    return df


# ============================================================
# 示例 4: SuperTrend (超级趋势)
# ============================================================

def example_supertrend():
    """SuperTrend 使用示例"""
    print("\n" + "=" * 70)
    print("示例 4: SuperTrend (超级趋势)")
    print("=" * 70)
    
    # 创建示例数据 (上涨趋势)
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    
    base_price = 100
    trend = np.linspace(0, 20, 100)  # 上升趋势
    noise = np.cumsum(np.random.randn(100) * 1.5)
    prices = base_price + trend + noise
    
    df = pd.DataFrame({
        'date': dates,
        'open': prices + np.random.randn(100) * 0.5,
        'high': prices + np.abs(np.random.randn(100)) * 1.5,
        'low': prices - np.abs(np.random.randn(100)) * 1.5,
        'close': prices,
        'volume': np.random.randint(1000000, 5000000, 100)
    })
    df.set_index('date', inplace=True)
    
    # 计算 SuperTrend
    df_st = calculate_supertrend(df, period=10, multiplier=3.0)
    
    print("\n【SuperTrend 计算结果 (最后 10 条)】")
    print(df_st[['close', 'supertrend', 'trend']].tail(10))
    
    # 识别趋势反转
    print("\n【趋势反转信号】")
    reversal = identify_trend_reversal(df_st)
    print(f"  当前趋势：{reversal['current_trend_cn']}")
    print(f"  反转信号：{reversal['reversal_signal_cn']}")
    
    # 获取综合报告
    print("\n【综合分析报告】")
    summary = get_supertrend_summary(df, period=10, multiplier=3.0)
    print(f"  当前价格：{summary['current_price']}")
    print(f"  SuperTrend 值：{summary['supertrend_value']}")
    print(f"  趋势：{summary['trend_cn']}")
    print(f"  趋势强度：{summary['trend_strength_cn']}")
    print(f"  建议：{summary['recommendation']}")
    print(f"  置信度：{summary['confidence']}")
    
    return df


# ============================================================
# 示例 5: 综合使用所有指标
# ============================================================

def example_combined():
    """综合使用所有指标"""
    print("\n" + "=" * 70)
    print("示例 5: 综合使用所有指标")
    print("=" * 70)
    
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
    
    # 获取所有指标信号
    print("\n【多指标综合分析】")
    print("-" * 70)
    
    # Ichimoku
    ichimoku = get_ichimoku_summary(df)
    print(f"Ichimoku: 趋势={ichimoku['overall_trend']}, 建议={ichimoku['recommendation']}")
    
    # VWAP
    vwap = get_vwap_summary(df)
    print(f"VWAP:     趋势={vwap['trend_cn']}, 建议={vwap['recommendation']}")
    
    # SuperTrend
    supertrend = get_supertrend_summary(df)
    print(f"SuperTrend: 趋势={supertrend['trend_cn']}, 建议={supertrend['recommendation']}")
    
    # 综合判断
    print("\n【综合判断】")
    bullish_count = 0
    bearish_count = 0
    
    if ichimoku['overall_trend'] in ['bullish', 'strong_bullish']:
        bullish_count += 1
    elif ichimoku['overall_trend'] in ['bearish', 'strong_bearish']:
        bearish_count += 1
    
    if vwap['trend'] == 'bullish':
        bullish_count += 1
    elif vwap['trend'] == 'bearish':
        bearish_count += 1
    
    if supertrend['trend'] == 'bullish':
        bullish_count += 1
    elif supertrend['trend'] == 'bearish':
        bearish_count += 1
    
    print(f"  看涨指标数：{bullish_count}")
    print(f"  看跌指标数：{bearish_count}")
    
    if bullish_count >= 2:
        final_recommendation = "买入/持有"
    elif bearish_count >= 2:
        final_recommendation = "卖出/观望"
    else:
        final_recommendation = "观望"
    
    print(f"  最终建议：{final_recommendation}")
    
    return df


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("技术指标 L2 使用示例")
    print("=" * 70)
    
    # 运行所有示例
    example_ichimoku()
    example_vwap_daily()
    example_vwap_intraday()
    example_supertrend()
    example_combined()
    
    print("\n" + "=" * 70)
    print("所有示例运行完成!")
    print("=" * 70)
