"""
SuperTrend (超级趋势) 技术指标

SuperTrend 是基于 ATR (平均真实波幅) 的趋势跟踪指标。

计算步骤:
1. 计算 ATR (Average True Range)
2. 计算基本带:
   - 上带 = (最高价 + 最低价) / 2 + multiplier × ATR
   - 下带 = (最高价 + 最低价) / 2 - multiplier × ATR
3. 确定 SuperTrend 值:
   - 如果收盘价 > 上带，SuperTrend = 下带 (看涨)
   - 如果收盘价 < 下带，SuperTrend = 上带 (看跌)
4. 趋势反转信号:
   - SuperTrend 从上方切换到下方：买入信号
   - SuperTrend 从下方切换到上方：卖出信号

参数:
- period: ATR 周期 (默认 10)
- multiplier: 乘数 (默认 3)

特点:
- 简单直观，易于理解
- 在趋势市场中表现良好
- 在震荡市场中可能产生假信号
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, List, Tuple
from datetime import datetime


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    计算 ATR (Average True Range)
    
    Args:
        df: 包含 'high', 'low', 'close' 列的 DataFrame
        period: ATR 周期 (默认 14)
    
    Returns:
        ATR 序列
    """
    high = df['high']
    low = df['low']
    close = df['close']
    
    # 计算真实波幅 (True Range)
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # 计算 ATR (使用 Wilder 的平滑方法)
    atr = tr.ewm(span=period, adjust=False).mean()
    
    return atr


def calculate_supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> pd.DataFrame:
    """
    计算 SuperTrend 指标
    
    Args:
        df: 包含 'high', 'low', 'close' 列的 DataFrame
        period: ATR 周期 (默认 10)
        multiplier: 乘数 (默认 3)
    
    Returns:
        包含 SuperTrend 相关列的 DataFrame
    """
    df = df.copy()
    
    # 计算 ATR
    df['atr'] = calculate_atr(df, period)
    
    # 计算中轴 (HL2)
    df['hl2'] = (df['high'] + df['low']) / 2
    
    # 计算基本带
    df['upper_band'] = df['hl2'] + (multiplier * df['atr'])
    df['lower_band'] = df['hl2'] - (multiplier * df['atr'])
    
    # 计算 SuperTrend
    df['supertrend'] = np.nan
    df['trend'] = np.nan  # 1 = 上涨趋势，-1 = 下跌趋势
    
    # 初始化 - 使用 iloc 进行位置索引，避免 DatetimeIndex 问题
    df = df.reset_index(drop=True)
    df.loc[0, 'supertrend'] = df.loc[0, 'upper_band']
    df.loc[0, 'trend'] = -1
    
    # 迭代计算 SuperTrend
    for i in range(1, len(df)):
        prev_trend = df.loc[i-1, 'trend']
        prev_supertrend = df.loc[i-1, 'supertrend']
        
        current_close = df.loc[i, 'close']
        current_upper = df.loc[i, 'upper_band']
        current_lower = df.loc[i, 'lower_band']
        
        if prev_trend == 1:  # 之前是上涨趋势
            if current_close < prev_supertrend:
                # 趋势反转
                df.loc[i, 'supertrend'] = current_upper
                df.loc[i, 'trend'] = -1
            else:
                # 保持上涨趋势
                df.loc[i, 'supertrend'] = max(prev_supertrend, current_lower)
                df.loc[i, 'trend'] = 1
        else:  # 之前是下跌趋势
            if current_close > prev_supertrend:
                # 趋势反转
                df.loc[i, 'supertrend'] = current_lower
                df.loc[i, 'trend'] = 1
            else:
                # 保持下跌趋势
                df.loc[i, 'supertrend'] = min(prev_supertrend, current_upper)
                df.loc[i, 'trend'] = -1
    
    # 清理临时列
    df.drop(['atr', 'hl2', 'upper_band', 'lower_band'], axis=1, inplace=True, errors='ignore')
    
    return df


def identify_trend_reversal(df: pd.DataFrame, lookback: int = 5) -> Dict:
    """
    识别 SuperTrend 趋势反转信号
    
    Args:
        df: 包含 SuperTrend 计算结果的 DataFrame
        lookback: 回看周期数
    
    Returns:
        反转信号字典
    """
    if len(df) < 2 or 'trend' not in df.columns:
        return {"error": "数据不足或缺少 trend 列"}
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    current_trend = latest['trend']
    prev_trend = prev['trend']
    
    reversal_signal = None
    reversal_signal_cn = None
    
    # 检测趋势反转
    if prev_trend == -1 and current_trend == 1:
        reversal_signal = "bullish_reversal"
        reversal_signal_cn = "看涨反转 (买入信号)"
    elif prev_trend == 1 and current_trend == -1:
        reversal_signal = "bearish_reversal"
        reversal_signal_cn = "看跌反转 (卖出信号)"
    
    # 检测最近的反转 (在 lookback 周期内)
    recent_reversals = []
    for i in range(2, min(lookback + 1, len(df))):
        curr = df.iloc[-i]
        prev_i = df.iloc[-i-1]
        
        if pd.notna(curr['trend']) and pd.notna(prev_i['trend']):
            if prev_i['trend'] == -1 and curr['trend'] == 1:
                recent_reversals.append({
                    "index": len(df) - i,
                    "type": "bullish",
                    "price": df.iloc[-i]['close']
                })
            elif prev_i['trend'] == 1 and curr['trend'] == -1:
                recent_reversals.append({
                    "index": len(df) - i,
                    "type": "bearish",
                    "price": df.iloc[-i]['close']
                })
    
    return {
        "reversal_signal": reversal_signal,
        "reversal_signal_cn": reversal_signal_cn,
        "current_trend": "bullish" if current_trend == 1 else "bearish",
        "current_trend_cn": "上涨" if current_trend == 1 else "下跌",
        "prev_trend": "bullish" if prev_trend == 1 else "bearish",
        "recent_reversals": recent_reversals,
        "current_price": round(latest['close'], 2) if pd.notna(latest['close']) else None,
        "current_supertrend": round(latest['supertrend'], 2) if pd.notna(latest['supertrend']) else None,
        "timestamp": df.index[-1] if hasattr(df.index[-1], 'isoformat') else str(df.index[-1])
    }


def get_supertrend_levels(df: pd.DataFrame) -> Dict:
    """
    获取 SuperTrend 关键价位
    
    Args:
        df: 包含 SuperTrend 计算结果的 DataFrame
    
    Returns:
        关键价位字典
    """
    if len(df) < 1 or 'supertrend' not in df.columns:
        return {"error": "数据不足"}
    
    latest = df.iloc[-1]
    
    current_price = latest['close']
    current_supertrend = latest['supertrend']
    current_trend = latest['trend']
    
    # 计算价格与 SuperTrend 的距离
    if pd.notna(current_supertrend) and current_supertrend != 0:
        distance = abs(current_price - current_supertrend)
        distance_percent = (distance / current_price) * 100
    else:
        distance = 0
        distance_percent = 0
    
    # 支撑/阻力位
    if current_trend == 1:
        support = current_supertrend
        resistance = None  # 上涨趋势中，SuperTrend 是支撑
    else:
        support = None
        resistance = current_supertrend  # 下跌趋势中，SuperTrend 是阻力
    
    return {
        "current_price": round(current_price, 2) if pd.notna(current_price) else None,
        "supertrend_value": round(current_supertrend, 2) if pd.notna(current_supertrend) else None,
        "trend": "bullish" if current_trend == 1 else "bearish",
        "distance": round(distance, 2),
        "distance_percent": round(distance_percent, 2),
        "support": round(support, 2) if support is not None and pd.notna(support) else None,
        "resistance": round(resistance, 2) if resistance is not None and pd.notna(resistance) else None
    }


def get_supertrend_summary(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> Dict:
    """
    获取 SuperTrend 综合分析报告
    
    Args:
        df: 包含 'high', 'low', 'close' 列的 DataFrame
        period: ATR 周期
        multiplier: 乘数
    
    Returns:
        综合分析报告
    """
    # 计算 SuperTrend
    df = calculate_supertrend(df, period, multiplier)
    
    # 趋势反转信号
    reversal = identify_trend_reversal(df)
    
    # 关键价位
    levels = get_supertrend_levels(df)
    
    # 最新数据
    latest = df.iloc[-1]
    
    # 趋势强度 (基于价格与 SuperTrend 的距离)
    distance_percent = levels.get('distance_percent', 0)
    
    if distance_percent < 2:
        trend_strength = "weak"
        trend_strength_cn = "弱"
    elif distance_percent < 5:
        trend_strength = "moderate"
        trend_strength_cn = "中等"
    else:
        trend_strength = "strong"
        trend_strength_cn = "强"
    
    # 综合建议
    current_trend = latest['trend']
    
    if reversal.get('reversal_signal') == 'bullish_reversal':
        recommendation = "强烈买入"
        confidence = "high"
    elif reversal.get('reversal_signal') == 'bearish_reversal':
        recommendation = "强烈卖出"
        confidence = "high"
    elif current_trend == 1:
        if trend_strength == "strong":
            recommendation = "持有/买入"
            confidence = "medium"
        else:
            recommendation = "持有"
            confidence = "low"
    else:
        if trend_strength == "strong":
            recommendation = "卖出/观望"
            confidence = "medium"
        else:
            recommendation = "观望"
            confidence = "low"
    
    return {
        "timestamp": datetime.now().isoformat(),
        "parameters": {
            "period": period,
            "multiplier": multiplier
        },
        "current_price": round(latest['close'], 2) if pd.notna(latest['close']) else None,
        "supertrend_value": round(latest['supertrend'], 2) if pd.notna(latest['supertrend']) else None,
        "trend": levels.get('trend'),
        "trend_cn": reversal.get('current_trend_cn'),
        "trend_strength": trend_strength,
        "trend_strength_cn": trend_strength_cn,
        "reversal_signal": reversal.get('reversal_signal'),
        "reversal_signal_cn": reversal.get('reversal_signal_cn'),
        "levels": levels,
        "recommendation": recommendation,
        "confidence": confidence
    }


def scan_supertrend_signals(df: pd.DataFrame, min_strength: str = "moderate") -> List[Dict]:
    """
    扫描 SuperTrend 信号 (用于多股票筛选)
    
    Args:
        df: 包含 SuperTrend 计算结果的 DataFrame
        min_strength: 最小趋势强度 ("weak", "moderate", "strong")
    
    Returns:
        信号列表
    """
    signals = []
    
    reversal = identify_trend_reversal(df)
    levels = get_supertrend_levels(df)
    
    if reversal.get('error'):
        return signals
    
    # 过滤信号强度
    strength_map = {"weak": 0, "moderate": 1, "strong": 2}
    min_strength_val = strength_map.get(min_strength, 1)
    current_strength_val = strength_map.get(levels.get('trend_strength', 'weak'), 0)
    
    # 只返回达到强度要求的信号
    if current_strength_val >= min_strength_val:
        signals.append({
            "type": "trend" if not reversal.get('reversal_signal') else "reversal",
            "direction": reversal.get('current_trend'),
            "reversal_signal": reversal.get('reversal_signal'),
            "strength": levels.get('trend_strength'),
            "price": levels.get('current_price'),
            "supertrend": levels.get('supertrend_value'),
            "recommendation": "买入" if reversal.get('current_trend') == "bullish" else "卖出"
        })
    
    return signals


if __name__ == "__main__":
    # 使用示例
    print("=" * 60)
    print("SuperTrend (超级趋势) 使用示例")
    print("=" * 60)
    
    # 创建示例数据
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    
    # 模拟有趋势的价格
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
    
    print("\n1. SuperTrend 计算结果 (最后 10 条):")
    print(df_st[['close', 'supertrend', 'trend']].tail(10).to_string())
    
    print("\n2. 趋势反转信号:")
    reversal = identify_trend_reversal(df_st)
    for key, value in reversal.items():
        if key != 'recent_reversals' and value is not None:
            print(f"   {key}: {value}")
    
    if reversal.get('recent_reversals'):
        print(f"   最近反转：{len(reversal['recent_reversals'])} 次")
        for r in reversal['recent_reversals'][-3:]:
            print(f"      - {r['type']} @ {r['price']}")
    
    print("\n3. 关键价位:")
    levels = get_supertrend_levels(df_st)
    for key, value in levels.items():
        print(f"   {key}: {value}")
    
    print("\n4. 综合分析报告:")
    summary = get_supertrend_summary(df_st, period=10, multiplier=3.0)
    print(f"   当前价格：{summary.get('current_price')}")
    print(f"   SuperTrend 值：{summary.get('supertrend_value')}")
    print(f"   趋势：{summary.get('trend_cn')}")
    print(f"   趋势强度：{summary.get('trend_strength_cn')}")
    print(f"   反转信号：{summary.get('reversal_signal_cn')}")
    print(f"   建议：{summary.get('recommendation')}")
    print(f"   置信度：{summary.get('confidence')}")
    
    print("\n5. 信号扫描:")
    signals = scan_supertrend_signals(df_st, min_strength="moderate")
    if signals:
        for sig in signals:
            print(f"   类型：{sig['type']}, 方向：{sig['direction']}, 建议：{sig['recommendation']}")
    else:
        print("   无符合强度要求的信号")
    
    # 可视化示例
    print("\n6. 可视化代码示例:")
    print("""
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(df_st.index, df_st['close'], label='Price', linewidth=1)
    ax.plot(df_st.index, df_st['supertrend'], label='SuperTrend', 
            color='red', linewidth=2, linestyle='--')
    
    # 填充趋势颜色
    colors = ['green' if t == 1 else 'red' for t in df_st['trend']]
    ax.scatter(df_st.index, df_st['close'], c=colors, alpha=0.3, s=10)
    
    ax.legend()
    ax.set_title('SuperTrend Analysis')
    plt.show()
    """)
