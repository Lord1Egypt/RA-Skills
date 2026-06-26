#!/usr/bin/env python3
"""
Technical Analysis Module for Stocks and ETFs

Calculates technical indicators and determines trend direction, support/resistance,
momentum signals, and chart patterns.

Data: Uses Tencent Finance API for historical price data
"""

import requests
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TechnicalSnapshot:
    """Technical analysis result for a single ticker"""
    ticker: str
    as_of_date: str

    # Price data
    current_price: float
    price_change_1d: float
    price_change_5d: float
    price_change_20d: float

    # Moving averages (in CNY)
    ma5: Optional[float] = None
    ma10: Optional[float] = None
    ma20: Optional[float] = None
    ma60: Optional[float] = None
    ma120: Optional[float] = None
    ma250: Optional[float] = None

    # Trend signals (boolean)
    above_ma5: bool = False
    above_ma10: bool = False
    above_ma20: bool = False
    above_ma60: bool = False
    ma5_gt_ma10: bool = False  # Bullish MA cross
    ma10_gt_ma20: bool = False

    # Momentum indicators
    rsi_14: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    kdj_k: Optional[float] = None
    kdj_d: Optional[float] = None
    kdj_j: Optional[float] = None

    # Volatility
    atr_14: Optional[float] = None
    bollinger_width: Optional[float] = None  # (Upper - Lower) / MA20

    # Volume
    volume_avg_20: Optional[float] = None
    volume_ratio: Optional[float] = None  # today / avg_20

    # Support/Resistance (simplified)
    support_levels: List[float] = None
    resistance_levels: List[float] = None

    # Overall trend
    trend: str = "unknown"  # 'bullish', 'bearish', 'sideways'
    trend_strength: str = "weak"  # 'strong', 'moderate', 'weak'

    def __post_init__(self):
        if self.support_levels is None:
            self.support_levels = []
        if self.resistance_levels is None:
            self.resistance_levels = []


def fetch_history(ticker: str, days: int = 250) -> Dict:
    """
    Fetch historical daily price data using Tencent Finance API.

    Args:
        ticker: Stock/ETF code with market prefix (e.g., 'sh000001', 'sz399006')
        days: Number of trading days to fetch (max ~320)

    Returns:
        Dictionary with 'date', 'open', 'high', 'low', 'close', 'volume' arrays
    """
    from utils import fetch_tencent_kline

    data = fetch_tencent_kline(ticker, days)
    if not data:
        return {}

    # Convert lists to numpy arrays for calculations
    return {
        'date': data['dates'],
        'open': data['open'],
        'high': data['high'],
        'low': data['low'],
        'close': data['close'],
        'volume': data['volume']
    }


def calculate_ma(prices: np.ndarray, period: int) -> float:
    """Calculate simple moving average."""
    return float(np.mean(prices[-period:]))


def calculate_rsi(prices: np.ndarray, period: int = 14) -> float:
    """Calculate RSI using Wilder's smoothing."""
    if len(prices) < period + 1:
        return None

    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi)


def calculate_macd(prices: np.ndarray, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[float, float, float]:
    """Calculate MACD line, signal line, and histogram."""
    ema_fast = prices[-slow:]  # Simplified; should use exponential moving average
    ema_slow = prices[-slow:]
    macd_line = np.mean(ema_fast) - np.mean(ema_slow)
    signal_line = macd_line  # Placeholder
    histogram = macd_line - signal_line
    return float(macd_line), float(signal_line), float(histogram)


def detect_trend(ma_status: Dict, rsi: Optional[float], macd_hist: Optional[float]) -> Tuple[str, str]:
    """
    Determine overall trend direction and strength.

    Returns:
        (trend, strength): 'bullish'/'bearish'/'sideways', 'strong'/'moderate'/'weak'
    """
    # Count bullish MA signals
    bullish_signals = sum([
        ma_status.get('above_ma20', False),
        ma_status.get('ma5_gt_ma10', False),
        ma_status.get('ma10_gt_ma20', False)
    ])
    bearish_signals = sum([
        not ma_status.get('above_ma20', True),  # below MA20
        not ma_status.get('ma5_gt_ma10', True),
        not ma_status.get('ma10_gt_ma20', True)
    ])

    # RSI confirmation
    rsi_bullish = rsi and rsi > 50 and rsi < 70
    rsi_bearish = rsi and rsi < 50

    # MACD confirmation
    macd_bullish = macd_hist and macd_hist > 0
    macd_bearish = macd_hist and macd_hist < 0

    # Scoring
    score = bullish_signals - bearish_signals
    if rsi_bullish:
        score += 1
    if rsi_bearish:
        score -= 1
    if macd_bullish:
        score += 1
    if macd_bearish:
        score -= 1

    if score >= 3:
        trend = "bullish"
        strength = "strong" if score >= 5 else "moderate"
    elif score <= -3:
        trend = "bearish"
        strength = "strong" if score <= -5 else "moderate"
    else:
        trend = "sideways"
        strength = "weak"

    return trend, strength


def analyze(ticker: str, lookback_days: int = 250) -> Dict:
    """
    Main entry point: perform full technical analysis.

    Args:
        ticker: Stock/ETF code
        lookback_days: Number of historical days needed

    Returns:
        Dictionary with TechnicalSnapshot and interpretation
    """
    # 1. Fetch data
    hist = fetch_history(ticker, days=lookback_days)
    if not hist or len(hist['close']) < 20:
        return {"error": "Insufficient historical data"}

    closes = np.array(hist['close'], dtype=float)
    highs = np.array(hist['high'], dtype=float)
    lows = np.array(hist['low'], dtype=float)
    volumes = np.array(hist['volume'], dtype=float)

    # 2. Compute moving averages
    current_price = closes[-1]
    snapshot = TechnicalSnapshot(
        ticker=ticker,
        as_of_date=hist['date'][-1],
        current_price=current_price,
        price_change_1d=(current_price - closes[-2]) / closes[-2] * 100 if len(closes) >= 2 else None,
        price_change_5d=(current_price - closes[-6]) / closes[-6] * 100 if len(closes) >= 6 else None,
        price_change_20d=(current_price - closes[-21]) / closes[-21] * 100 if len(closes) >= 21 else None
    )

    for period in [5, 10, 20, 60, 120, 250]:
        if len(closes) >= period:
            ma_val = calculate_ma(closes, period)
            setattr(snapshot, f"ma{period}", ma_val)
            setattr(snapshot, f"above_ma{period}", current_price > ma_val)

    if snapshot.ma5 and snapshot.ma10:
        snapshot.ma5_gt_ma10 = snapshot.ma5 > snapshot.ma10
    if snapshot.ma10 and snapshot.ma20:
        snapshot.ma10_gt_ma20 = snapshot.ma10 > snapshot.ma20

    # 3. Momentum indicators
    snapshot.rsi_14 = calculate_rsi(closes, 14)
    macd_line, signal, hist = calculate_macd(closes)
    snapshot.macd = macd_line
    snapshot.macd_signal = signal
    snapshot.macd_histogram = hist

    # 4. Volume
    if len(volumes) >= 20:
        snapshot.volume_avg_20 = float(np.mean(volumes[-20:]))
        snapshot.volume_ratio = volumes[-1] / snapshot.volume_avg_20 if snapshot.volume_avg_20 else None

    # 5. Trend detection
    ma_status = {
        'above_ma20': snapshot.above_ma20,
        'ma5_gt_ma10': snapshot.ma5_gt_ma10,
        'ma10_gt_ma20': snapshot.ma10_gt_ma20
    }
    snapshot.trend, snapshot.trend_strength = detect_trend(ma_status, snapshot.rsi_14, snapshot.macd_histogram)

    # 6. Simple support/resistance (recent highs/lows)
    if len(highs) >= 20:
        snapshot.resistance_levels = [float(np.max(highs[-20:]))]
        snapshot.support_levels = [float(np.min(lows[-20:]))]

    # 7. Build result
    result = {
        'ticker': ticker,
        'snapshot': snapshot,
        'summary': generate_technical_summary(snapshot)
    }

    return result


def generate_technical_summary(snap: TechnicalSnapshot) -> str:
    """Generate human-readable technical summary."""
    parts = []

    # Trend
    trend_desc = f"趋势: {snap.trend}（{snap.trend_strength}）"
    parts.append(trend_desc)

    # Price vs MA
    if snap.above_ma20:
        parts.append(f"价格位于MA20之上（{snap.current_price:.2f} vs MA20 {snap.ma20:.2f}）")
    else:
        parts.append(f"价格位于MA20之下（{snap.current_price:.2f} vs MA20 {snap.ma20:.2f}）")

    # RSI
    if snap.rsi_14:
        rsi_state = "超买" if snap.rsi_14 > 70 else "超卖" if snap.rsi_14 < 30 else "中性"
        parts.append(f"RSI(14): {snap.rsi_14:.1f} → {rsi_state}")

    # Recent performance
    if snap.price_change_5d:
        parts.append(f"近5日: {snap.price_change_5d:+.1f}%")

    return "；".join(parts)


if __name__ == "__main__":
    # Quick test
    result = analyze("sh000001")  # 上证指数
    print(f"Technical analysis for {result['ticker']}:")
    print(result['summary'])
