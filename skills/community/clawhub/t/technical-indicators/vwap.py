"""
VWAP (成交量加权平均价) 技术指标

VWAP = Volume Weighted Average Price

计算公式:
VWAP = Σ(价格 × 成交量) / Σ(成交量)

其中价格通常使用典型价格 (Typical Price):
典型价格 = (最高价 + 最低价 + 收盘价) / 3

VWAP 特点:
- 日内指标，每个交易日重新开始计算
- 反映机构平均建仓成本
- 价格 > VWAP: 看涨，买方主导
- 价格 < VWAP: 看跌，卖方主导

交易信号:
- 价格上穿 VWAP: 买入信号
- 价格下穿 VWAP: 卖出信号
- 价格远离 VWAP: 可能回归
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List
from datetime import datetime


def calculate_vwap(df: pd.DataFrame, reset_daily: bool = True) -> pd.DataFrame:
    """
    计算 VWAP (成交量加权平均价)
    
    Args:
        df: 包含 'high', 'low', 'close', 'volume' 列的 DataFrame
            如果是日内数据，需要包含 datetime 列用于识别交易日
        reset_daily: 是否每个交易日重置 VWAP 计算 (默认 True)
    
    Returns:
        包含 VWAP 列的 DataFrame
    """
    df = df.copy()
    
    # 计算典型价格
    df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3
    
    # 计算典型价格 × 成交量
    df['tp_volume'] = df['typical_price'] * df['volume']
    
    if reset_daily and 'date' in df.columns:
        # 按日期分组计算 VWAP
        # 使用 reset_index 避免日期既是索引又是列的歧义
        df_temp = df.reset_index(drop=True)
        df['cumulative_tp_volume'] = df_temp.groupby('date')['tp_volume'].cumsum().values
        df['cumulative_volume'] = df_temp.groupby('date')['volume'].cumsum().values
    else:
        # 连续计算 VWAP
        df['cumulative_tp_volume'] = df['tp_volume'].cumsum()
        df['cumulative_volume'] = df['volume'].cumsum()
    
    # 计算 VWAP
    df['vwap'] = df['cumulative_tp_volume'] / df['cumulative_volume']
    
    # 清理临时列
    df.drop(['typical_price', 'tp_volume', 'cumulative_tp_volume', 'cumulative_volume'], 
            axis=1, inplace=True, errors='ignore')
    
    return df


def calculate_vwap_intraday(df: pd.DataFrame) -> pd.DataFrame:
    """
    计算日内 VWAP (适用于分钟级数据)
    
    Args:
        df: 包含 'datetime', 'high', 'low', 'close', 'volume' 列的 DataFrame
            datetime 列应该是 datetime 类型
    
    Returns:
        包含 VWAP 列的 DataFrame
    """
    df = df.copy()
    
    # 确保 datetime 是 datetime 类型
    if not pd.api.types.is_datetime64_any_dtype(df['datetime']):
        df['datetime'] = pd.to_datetime(df['datetime'])
    
    # 提取日期用于分组
    df['date'] = df['datetime'].dt.date
    
    # 使用 reset_daily=True 计算
    df = calculate_vwap(df, reset_daily=True)
    
    # 清理临时列
    df.drop(['date'], axis=1, inplace=True, errors='ignore')
    
    return df


def identify_vwap_position(df: pd.DataFrame) -> Dict:
    """
    识别价格相对 VWAP 的位置
    
    Args:
        df: 包含 VWAP 列的 DataFrame
    
    Returns:
        位置分析字典
    """
    if len(df) < 2 or 'vwap' not in df.columns:
        return {"error": "数据不足或缺少 VWAP 列"}
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    current_price = latest['close']
    current_vwap = latest['vwap']
    prev_price = prev['close']
    prev_vwap = prev['vwap']
    
    # 价格相对 VWAP 位置
    if pd.notna(current_price) and pd.notna(current_vwap):
        if current_price > current_vwap * 1.02:  # 高于 VWAP 2%
            position = "significantly_above"
            position_cn = "显著高于 VWAP"
        elif current_price > current_vwap:
            position = "above"
            position_cn = "高于 VWAP"
        elif current_price < current_vwap * 0.98:  # 低于 VWAP 2%
            position = "significantly_below"
            position_cn = "显著低于 VWAP"
        else:
            position = "near"
            position_cn = "接近 VWAP"
    else:
        position = "unknown"
        position_cn = "未知"
    
    # 检测穿越信号
    cross_signal = None
    cross_signal_cn = None
    
    if pd.notna(prev_price) and pd.notna(prev_vwap):
        # 价格上穿 VWAP
        if prev_price <= prev_vwap and current_price > current_vwap:
            cross_signal = "bullish_cross"
            cross_signal_cn = "上穿 VWAP (看涨)"
        # 价格下穿 VWAP
        elif prev_price >= prev_vwap and current_price < current_vwap:
            cross_signal = "bearish_cross"
            cross_signal_cn = "下穿 VWAP (看跌)"
    
    # 计算偏离度
    if pd.notna(current_vwap) and current_vwap != 0:
        deviation = (current_price - current_vwap) / current_vwap * 100
    else:
        deviation = 0
    
    return {
        "position": position,
        "position_cn": position_cn,
        "cross_signal": cross_signal,
        "cross_signal_cn": cross_signal_cn,
        "current_price": round(current_price, 2) if pd.notna(current_price) else None,
        "current_vwap": round(current_vwap, 2) if pd.notna(current_vwap) else None,
        "deviation_percent": round(deviation, 2),
        "timestamp": df.index[-1] if hasattr(df.index[-1], 'isoformat') else str(df.index[-1])
    }


def get_vwap_support_resistance(df: pd.DataFrame, lookback: int = 20) -> Dict:
    """
    获取 VWAP 支撑阻力位
    
    Args:
        df: 包含 VWAP 列的 DataFrame
        lookback: 回看周期数
    
    Returns:
        支撑阻力位字典
    """
    if len(df) < lookback or 'vwap' not in df.columns:
        return {"error": "数据不足"}
    
    recent_df = df.tail(lookback)
    
    vwap_values = recent_df['vwap'].dropna()
    
    if len(vwap_values) == 0:
        return {"error": "无有效 VWAP 数据"}
    
    # VWAP 区间
    vwap_high = vwap_values.max()
    vwap_low = vwap_values.min()
    vwap_avg = vwap_values.mean()
    
    # 当前价格
    current_price = df.iloc[-1]['close']
    
    # 判断支撑/阻力
    if current_price > vwap_avg:
        support = vwap_avg
        resistance = vwap_high
    else:
        support = vwap_low
        resistance = vwap_avg
    
    return {
        "vwap_high": round(vwap_high, 2),
        "vwap_low": round(vwap_low, 2),
        "vwap_avg": round(vwap_avg, 2),
        "current_price": round(current_price, 2),
        "support": round(support, 2),
        "resistance": round(resistance, 2),
        "price_vs_vwap": "above" if current_price > vwap_avg else "below"
    }


def get_vwap_summary(df: pd.DataFrame) -> Dict:
    """
    获取 VWAP 综合分析报告
    
    Args:
        df: 包含必要列的 DataFrame
    
    Returns:
        综合分析报告
    """
    # 计算 VWAP
    df = calculate_vwap(df)
    
    # 位置分析
    position_analysis = identify_vwap_position(df)
    
    # 支撑阻力
    support_resistance = get_vwap_support_resistance(df)
    
    # 趋势判断
    latest = df.iloc[-1]
    current_price = latest['close']
    current_vwap = latest['vwap']
    
    # VWAP 斜率
    if len(df) >= 5:
        vwap_slope = (df['vwap'].iloc[-1] - df['vwap'].iloc[-5]) / 5
    else:
        vwap_slope = 0
    
    # 综合信号
    bullish_signals = 0
    bearish_signals = 0
    
    # 价格位置
    if position_analysis.get('position') in ['above', 'significantly_above']:
        bullish_signals += 1
    elif position_analysis.get('position') in ['below', 'significantly_below']:
        bearish_signals += 1
    
    # 穿越信号
    if position_analysis.get('cross_signal') == 'bullish_cross':
        bullish_signals += 2
    elif position_analysis.get('cross_signal') == 'bearish_cross':
        bearish_signals += 2
    
    # VWAP 斜率
    if vwap_slope > 0:
        bullish_signals += 1
    elif vwap_slope < 0:
        bearish_signals += 1
    
    # 总体判断
    if bullish_signals > bearish_signals + 1:
        trend = "bullish"
        trend_cn = "看涨"
        recommendation = "买入/持有"
    elif bearish_signals > bullish_signals + 1:
        trend = "bearish"
        trend_cn = "看跌"
        recommendation = "卖出/观望"
    else:
        trend = "neutral"
        trend_cn = "中性"
        recommendation = "观望"
    
    return {
        "timestamp": datetime.now().isoformat(),
        "current_price": round(current_price, 2) if pd.notna(current_price) else None,
        "current_vwap": round(current_vwap, 2) if pd.notna(current_vwap) else None,
        "vwap_slope": round(vwap_slope, 4),
        "position_analysis": position_analysis,
        "support_resistance": support_resistance,
        "trend": trend,
        "trend_cn": trend_cn,
        "bullish_signals": bullish_signals,
        "bearish_signals": bearish_signals,
        "recommendation": recommendation
    }


if __name__ == "__main__":
    # 使用示例
    print("=" * 60)
    print("VWAP (成交量加权平均价) 使用示例")
    print("=" * 60)
    
    # 创建示例日内数据 (分钟级)
    np.random.seed(42)
    
    # 模拟一天的交易数据 (假设 240 分钟)
    n_minutes = 240
    base_time = pd.Timestamp('2024-03-14 09:30:00')
    times = [base_time + pd.Timedelta(minutes=i) for i in range(n_minutes)]
    
    # 模拟价格 (开盘后逐渐上升)
    base_price = 100
    prices = base_price + np.cumsum(np.random.randn(n_minutes) * 0.3) + np.linspace(0, 2, n_minutes)
    
    # 模拟成交量 (开盘和收盘较大)
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
    
    print("\n1. VWAP 计算结果 (最后 10 条):")
    print(df_vwap[['datetime', 'close', 'volume', 'vwap']].tail(10).to_string())
    
    print("\n2. 价格相对 VWAP 位置:")
    position = identify_vwap_position(df_vwap)
    for key, value in position.items():
        if value is not None:
            print(f"   {key}: {value}")
    
    print("\n3. VWAP 支撑阻力位:")
    sr = get_vwap_support_resistance(df_vwap)
    for key, value in sr.items():
        print(f"   {key}: {value}")
    
    print("\n4. 综合分析报告:")
    summary = get_vwap_summary(df_vwap)
    print(f"   当前价格：{summary.get('current_price')}")
    print(f"   当前 VWAP: {summary.get('current_vwap')}")
    print(f"   趋势：{summary.get('trend_cn')}")
    print(f"   建议：{summary.get('recommendation')}")
    print(f"   看涨信号：{summary.get('bullish_signals')}")
    print(f"   看跌信号：{summary.get('bearish_signals')}")
    
    # 可视化示例 (需要 matplotlib)
    print("\n5. 可视化代码示例:")
    print("""
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df_vwap['datetime'], df_vwap['close'], label='Price', linewidth=1)
    ax.plot(df_vwap['datetime'], df_vwap['vwap'], label='VWAP', color='red', linewidth=2)
    ax.fill_between(df_vwap['datetime'], df_vwap['vwap'], df_vwap['close'], 
                    where=(df_vwap['close'] > df_vwap['vwap']), 
                    alpha=0.3, color='green', label='Above VWAP')
    ax.fill_between(df_vwap['datetime'], df_vwap['vwap'], df_vwap['close'], 
                    where=(df_vwap['close'] <= df_vwap['vwap']), 
                    alpha=0.3, color='red', label='Below VWAP')
    ax.legend()
    ax.set_title('VWAP Analysis')
    plt.show()
    """)
