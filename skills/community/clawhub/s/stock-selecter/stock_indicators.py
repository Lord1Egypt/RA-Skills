"""
股票技术指标计算库
封装常用技术指标计算函数，包括MACD、趋势线、背离检测等
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional, List, Dict


def calculate_macd(close_prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[Optional[pd.Series], Optional[pd.Series], Optional[pd.Series]]:
    """
    计算MACD指标
    
    Args:
        close_prices: 收盘价序列
        fast: 快速EMA周期（默认12）
        slow: 慢速EMA周期（默认26）
        signal: 信号线周期（默认9）
    
    Returns:
        (macd_line, signal_line, macd_hist) 三个Series
    """
    if len(close_prices) < slow:
        return None, None, None
    
    try:
        exp1 = close_prices.ewm(span=fast).mean()
        exp2 = close_prices.ewm(span=slow).mean()
        macd_line = exp1 - exp2
        signal_line = macd_line.ewm(span=signal).mean()
        macd_hist = macd_line - signal_line
        return macd_line, signal_line, macd_hist
    except Exception as e:
        print(f"MACD计算错误: {e}")
        return None, None, None


def calculate_sma(data: pd.Series, window: int) -> Optional[pd.Series]:
    """
    计算简单移动平均线
    
    Args:
        data: 数据序列
        window: 窗口期
    
    Returns:
        SMA序列
    """
    if len(data) < window:
        return None
    
    try:
        return data.rolling(window=window).mean()
    except Exception as e:
        print(f"SMA计算错误: {e}")
        return None


def calculate_ema(data: pd.Series, window: int) -> Optional[pd.Series]:
    """
    计算指数移动平均线
    
    Args:
        data: 数据序列
        window: 窗口期
    
    Returns:
        EMA序列
    """
    if len(data) < window:
        return None
    
    try:
        return data.ewm(span=window).mean()
    except Exception as e:
        print(f"EMA计算错误: {e}")
        return None


def analyze_trend(data: pd.Series, min_points: int = 10) -> Tuple[Optional[float], Optional[float]]:
    """
    分析数据的线性趋势
    
    Args:
        data: 数据序列
        min_points: 最少数据点数
    
    Returns:
        (slope斜率, r_squared决定系数)
        slope > 0表示趋势向上，slope < 0表示趋势向下
        r_squared越接近1，拟合度越好
    """
    if len(data) < min_points:
        return None, None
    
    try:
        x = np.arange(len(data))
        y = np.array(data)
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        
        # 计算R²决定系数
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return slope, r_squared
    except Exception as e:
        print(f"趋势分析错误: {e}")
        return None, None


def detect_bottom_divergence(close_prices: pd.Series, macd_hist: pd.Series, 
                           lookback: int = 12, price_threshold: float = 1.02) -> bool:
    """
    检测MACD底背离
    价格创新低但MACD没有创新低
    
    Args:
        close_prices: 收盘价序列
        macd_hist: MACD柱状图序列
        lookback: 回看周期
        price_threshold: 价格接近最低价的阈值（默认1.02表示2%以内）
    
    Returns:
        是否检测到底背离
    """
    if len(close_prices) < lookback or len(macd_hist) < lookback:
        return False
    
    try:
        recent_close = close_prices.iloc[-lookback:]
        recent_hist = macd_hist.iloc[-lookback:]

        # 价格在近1/4区间创了新低
        min_price_idx = recent_close.idxmin()
        price_trough_pos = list(recent_close.index).index(min_price_idx)
        if (lookback - 1 - price_trough_pos) > lookback // 4:
            return False

        # 当前价格接近最低价
        last_price = close_prices.iloc[-1]
        min_price = recent_close.min()
        if last_price > min_price * price_threshold:
            return False

        # MACD在价格新低时没有创新低
        min_hist = recent_hist.min()
        hist_at_trough = recent_hist.iloc[price_trough_pos]

        if min_hist < 0:
            # MACD在价格低点时的值没有创新低
            return hist_at_trough > min_hist * 0.5
        
        return False
    except Exception as e:
        print(f"底背离检测错误: {e}")
        return False


def detect_top_divergence(close_prices: pd.Series, macd_hist: pd.Series, 
                        lookback: int = 12, price_threshold: float = 0.98) -> bool:
    """
    检测MACD顶背离
    价格创新高但MACD没有创新高
    
    Args:
        close_prices: 收盘价序列
        macd_hist: MACD柱状图序列
        lookback: 回看周期
        price_threshold: 价格接近最高价的阈值（默认0.98表示2%以内）
    
    Returns:
        是否检测到顶背离
    """
    if len(close_prices) < lookback or len(macd_hist) < lookback:
        return False
    
    try:
        recent_close = close_prices.iloc[-lookback:]
        recent_hist = macd_hist.iloc[-lookback:]

        # 价格在近1/4区间创新高
        max_price_idx = recent_close.idxmax()
        price_peak_pos = list(recent_close.index).index(max_price_idx)
        if (lookback - 1 - price_peak_pos) > lookback // 4:
            return False

        # 当前价格接近最高价
        last_price = close_prices.iloc[-1]
        max_price = recent_close.max()
        if last_price < max_price * price_threshold:
            return False

        # MACD在价格新高时没有创新高
        max_hist = recent_hist.max()
        hist_at_peak = recent_hist.iloc[price_peak_pos]

        if max_hist > 0:
            # MACD在价格高点时的值没有创新高
            return hist_at_peak < max_hist * 0.5
        
        return False
    except Exception as e:
        print(f"顶背离检测错误: {e}")
        return False


def check_volume_surge(volume: pd.Series, weeks: int = 5, threshold: float = 1.5) -> Tuple[bool, Optional[float]]:
    """
    检查放量情况
    
    Args:
        volume: 成交量序列
        weeks: 对比的周数
        threshold: 放量阈值（默认1.5表示超过平均值的1.5倍）
    
    Returns:
        (是否放量, 放量倍数)
    """
    if len(volume) < weeks + 2:
        return False, None
    
    try:
        recent_vol = volume.iloc[-1]
        avg_vol = volume.iloc[-weeks-1:-1].mean()
        
        if avg_vol <= 0:
            return False, None
        
        ratio = recent_vol / avg_vol
        return ratio > threshold, round(ratio, 2)
    except Exception as e:
        print(f"放量检测错误: {e}")
        return False, None


def calculate_rsi(close_prices: pd.Series, window: int = 14) -> Optional[pd.Series]:
    """
    计算RSI相对强弱指标
    
    Args:
        close_prices: 收盘价序列
        window: RSI周期（默认14）
    
    Returns:
        RSI序列
    """
    if len(close_prices) < window + 1:
        return None
    
    try:
        delta = close_prices.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=window).mean()
        avg_loss = loss.rolling(window=window).mean()
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    except Exception as e:
        print(f"RSI计算错误: {e}")
        return None


def calculate_bollinger_bands(close_prices: pd.Series, window: int = 20, num_std: int = 2) -> Tuple[Optional[pd.Series], Optional[pd.Series], Optional[pd.Series]]:
    """
    计算布林带
    
    Args:
        close_prices: 收盘价序列
        window: 窗口期（默认20）
        num_std: 标准差倍数（默认2）
    
    Returns:
        (upper_band, middle_band, lower_band) 三个Series
    """
    if len(close_prices) < window:
        return None, None, None
    
    try:
        middle_band = close_prices.rolling(window=window).mean()
        std = close_prices.rolling(window=window).std()
        upper_band = middle_band + (std * num_std)
        lower_band = middle_band - (std * num_std)
        
        return upper_band, middle_band, lower_band
    except Exception as e:
        print(f"布林带计算错误: {e}")
        return None, None, None


def calculate_financial_ratios(fina_df: pd.DataFrame) -> Dict[str, Optional[float]]:
    """
    从财务指标DataFrame计算常用财务比率
    
    Args:
        fina_df: 财务指标DataFrame（最新数据在第一行）
    
    Returns:
        包含各种财务比率的字典
    """
    if fina_df is None or fina_df.empty:
        return {}
    
    try:
        latest = fina_df.iloc[0]
        
        # 常用指标
        roe = float(latest["roe"]) if latest.get("roe") and latest["roe"] else None
        roa = float(latest["roa"]) if latest.get("roa") and latest["roa"] else None
        
        gross_margin = float(latest["grossprofit_margin"]) if latest.get("grossprofit_margin") and latest["grossprofit_margin"] else None
        net_margin = float(latest["netprofit_margin"]) if latest.get("netprofit_margin") and latest["netprofit_margin"] else None
        
        debt_ratio = float(latest["debt_ratio"]) if latest.get("debt_ratio") and latest["debt_ratio"] else None
        current_ratio = float(latest["current_ratio"]) if latest.get("current_ratio") and latest["current_ratio"] else None
        
        return {
            "roe": roe,
            "roa": roa,
            "gross_profit_margin": gross_margin,
            "net_profit_margin": net_margin,
            "debt_ratio": debt_ratio,
            "current_ratio": current_ratio,
            "end_date": latest.get("end_date"),
            "ts_code": latest.get("ts_code")
        }
    except Exception as e:
        print(f"财务比率计算错误: {e}")
        return {}


def calculate_growth_rates(income_df: pd.DataFrame, periods: int = 4) -> Dict[str, Optional[float]]:
    """
    计算营收和净利润增长率
    
    Args:
        income_df: 利润表DataFrame（按日期降序排列）
        periods: 计算多少个期间的增长率
    
    Returns:
        包含营收增长率和净利润增长率的字典
    """
    if income_df is None or len(income_df) < 2:
        return {}
    
    try:
        # 限制计算期间
        df = income_df.head(periods).copy()
        
        revenue_growth = None
        profit_growth = None
        
        # 营收增长率（同比）
        if len(df) >= 4 and "total_revenue" in df.columns:
            current = pd.to_numeric(df.iloc[0].get("total_revenue"), errors='coerce')
            previous = pd.to_numeric(df.iloc[3].get("total_revenue"), errors='coerce')
            if current > 0 and previous > 0:
                revenue_growth = (current - previous) / previous * 100
        
        # 净利润增长率（同比）
        if len(df) >= 4 and "netprofit" in df.columns:
            current = pd.to_numeric(df.iloc[0].get("netprofit"), errors='coerce')
            previous = pd.to_numeric(df.iloc[3].get("netprofit"), errors='coerce')
            if current > 0 and previous > 0:
                profit_growth = (current - previous) / previous * 100
        
        return {
            "revenue_growth_yoy": revenue_growth,
            "profit_growth_yoy": profit_growth
        }
    except Exception as e:
        print(f"增长率计算错误: {e}")
        return {}


if __name__ == "__main__":
    # 测试指标计算库
    print("测试股票技术指标计算库...")
    
    # 创建测试数据
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    close_prices = pd.Series(np.cumsum(np.random.randn(100) * 0.5) + 100, index=dates)
    volume = pd.Series(np.random.randint(100000, 500000, 100), index=dates)
    
    print("\n1. 测试MACD计算:")
    macd, signal, hist = calculate_macd(close_prices)
    if macd is not None:
        print(f"   MACD计算成功，最新值: {macd.iloc[-1]:.4f}")
    
    print("\n2. 测试趋势分析:")
    slope, r2 = analyze_trend(close_prices)
    if slope is not None:
        trend = "向上" if slope > 0 else "向下"
        print(f"   趋势: {trend}, 斜率: {slope:.6f}, R²: {r2:.4f}")
    
    print("\n3. 测试放量检测:")
    is_surge, ratio = check_volume_surge(volume, weeks=5, threshold=1.5)
    if is_surge:
        print(f"   检测到放量，倍数: {ratio}x")
    else:
        print("   未检测到放量")
    
    print("\n4. 测试RSI计算:")
    rsi = calculate_rsi(close_prices, window=14)
    if rsi is not None:
        print(f"   RSI计算成功，最新值: {rsi.iloc[-1]:.2f}")
    
    print("\n所有测试完成!")
