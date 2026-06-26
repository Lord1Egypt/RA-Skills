#!/usr/bin/env python3
"""
Compute technical indicators for a given stock ticker.
Outputs a JSON file with RSI, MACD, Bollinger Bands, moving averages, and more.

Usage: python technical_indicators.py TICKER [--output OUTPUT_DIR]
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf


def sma(data, period):
    """Simple Moving Average."""
    return data.rolling(window=period).mean()


def ema(data, period):
    """Exponential Moving Average."""
    return data.ewm(span=period, adjust=False).mean()


def rsi(data, period=14):
    """Relative Strength Index."""
    delta = data.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def macd(data, fast=12, slow=26, signal=9):
    """MACD indicator."""
    fast_ema = ema(data, fast)
    slow_ema = ema(data, slow)
    macd_line = fast_ema - slow_ema
    signal_line = ema(macd_line, signal)
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def bollinger_bands(data, period=20, std_dev=2):
    """Bollinger Bands."""
    middle = sma(data, period)
    std = data.rolling(window=period).std()
    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)
    return upper, middle, lower


def atr(high, low, close, period=14):
    """Average True Range."""
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    return tr.rolling(window=period).mean()


def stochastic(high, low, close, k_period=14, d_period=3):
    """Stochastic Oscillator."""
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low)
    d = k.rolling(window=d_period).mean()
    return k, d


def compute_indicators(ticker: str) -> dict:
    """Compute all technical indicators for a ticker."""
    import pandas as pd

    stock = yf.Ticker(ticker)
    hist = stock.history(period="1y", interval="1d")

    if hist.empty:
        return {"ticker": ticker, "error": "No price data available"}

    close = hist["Close"]
    high = hist["High"]
    low = hist["Low"]
    volume = hist["Volume"]

    result = {
        "ticker": ticker,
        "computed_at": datetime.now().isoformat(),
        "data_range": {
            "start": hist.index[0].strftime("%Y-%m-%d"),
            "end": hist.index[-1].strftime("%Y-%m-%d"),
            "trading_days": len(hist),
        },
        "current": {
            "price": round(float(close.iloc[-1]), 2),
            "date": hist.index[-1].strftime("%Y-%m-%d"),
        },
    }

    # Moving Averages
    ma_periods = [5, 10, 20, 50, 100, 200]
    result["moving_averages"] = {}
    for p in ma_periods:
        if len(close) >= p:
            sma_val = float(sma(close, p).iloc[-1])
            ema_val = float(ema(close, p).iloc[-1])
            current = float(close.iloc[-1])
            result["moving_averages"][f"SMA_{p}"] = {
                "value": round(sma_val, 2),
                "price_vs_sma": "above" if current > sma_val else "below",
                "distance_pct": round((current / sma_val - 1) * 100, 2),
            }
            result["moving_averages"][f"EMA_{p}"] = {
                "value": round(ema_val, 2),
                "price_vs_ema": "above" if current > ema_val else "below",
                "distance_pct": round((current / ema_val - 1) * 100, 2),
            }

    # MA Alignment (trend indicator)
    if len(close) >= 200:
        sma_20 = float(sma(close, 20).iloc[-1])
        sma_50 = float(sma(close, 50).iloc[-1])
        sma_200 = float(sma(close, 200).iloc[-1])
        if sma_20 > sma_50 > sma_200:
            alignment = "STRONGLY_BULLISH"
        elif sma_20 > sma_50:
            alignment = "BULLISH"
        elif sma_20 < sma_50 < sma_200:
            alignment = "STRONGLY_BEARISH"
        elif sma_20 < sma_50:
            alignment = "BEARISH"
        else:
            alignment = "NEUTRAL"
        result["ma_alignment"] = alignment

    # RSI
    rsi_val = rsi(close)
    current_rsi = float(rsi_val.iloc[-1])
    result["rsi"] = {
        "value": round(current_rsi, 2),
        "signal": "OVERBOUGHT"
        if current_rsi > 70
        else "OVERSOLD"
        if current_rsi < 30
        else "NEUTRAL",
        "recent_values": [round(float(v), 2) for v in rsi_val.tail(5).values],
    }

    # MACD
    macd_line, signal_line, histogram = macd(close)
    result["macd"] = {
        "macd_line": round(float(macd_line.iloc[-1]), 4),
        "signal_line": round(float(signal_line.iloc[-1]), 4),
        "histogram": round(float(histogram.iloc[-1]), 4),
        "signal": "BULLISH"
        if float(macd_line.iloc[-1]) > float(signal_line.iloc[-1])
        else "BEARISH",
        "histogram_direction": "EXPANDING"
        if abs(float(histogram.iloc[-1])) > abs(float(histogram.iloc[-2]))
        else "CONTRACTING",
    }

    # Check for MACD crossover
    if len(macd_line) >= 2:
        prev_diff = float(macd_line.iloc[-2]) - float(signal_line.iloc[-2])
        curr_diff = float(macd_line.iloc[-1]) - float(signal_line.iloc[-1])
        if prev_diff < 0 and curr_diff > 0:
            result["macd"]["crossover"] = "BULLISH_CROSSOVER"
        elif prev_diff > 0 and curr_diff < 0:
            result["macd"]["crossover"] = "BEARISH_CROSSOVER"
        else:
            result["macd"]["crossover"] = "NONE"

    # Bollinger Bands
    upper, middle, lower = bollinger_bands(close)
    current_price = float(close.iloc[-1])
    bb_upper = float(upper.iloc[-1])
    bb_lower = float(lower.iloc[-1])
    bb_width = (bb_upper - bb_lower) / float(middle.iloc[-1]) * 100
    result["bollinger_bands"] = {
        "upper": round(bb_upper, 2),
        "middle": round(float(middle.iloc[-1]), 2),
        "lower": round(bb_lower, 2),
        "width_pct": round(bb_width, 2),
        "position": "ABOVE_UPPER"
        if current_price > bb_upper
        else "BELOW_LOWER"
        if current_price < bb_lower
        else "WITHIN",
        "percent_b": round((current_price - bb_lower) / (bb_upper - bb_lower) * 100, 2)
        if bb_upper != bb_lower
        else 50,
    }

    # ATR (using pandas)

    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr_val = tr.rolling(window=14).mean()
    result["atr"] = {
        "value": round(float(atr_val.iloc[-1]), 2),
        "pct_of_price": round(float(atr_val.iloc[-1]) / current_price * 100, 2),
    }

    # Stochastic
    k, d = stochastic(high, low, close)
    result["stochastic"] = {
        "k": round(float(k.iloc[-1]), 2),
        "d": round(float(d.iloc[-1]), 2),
        "signal": "OVERBOUGHT"
        if float(k.iloc[-1]) > 80
        else "OVERSOLD"
        if float(k.iloc[-1]) < 20
        else "NEUTRAL",
    }

    # Volume analysis
    avg_vol_20 = float(volume.tail(20).mean())
    last_vol = float(volume.iloc[-1])
    result["volume"] = {
        "last": int(last_vol),
        "avg_20d": int(avg_vol_20),
        "ratio_vs_avg": round(last_vol / avg_vol_20, 2) if avg_vol_20 > 0 else None,
        "trend": "ABOVE_AVERAGE"
        if last_vol > avg_vol_20 * 1.2
        else "BELOW_AVERAGE"
        if last_vol < avg_vol_20 * 0.8
        else "NORMAL",
    }

    # Support & Resistance (simple pivot points)
    last_high = float(high.iloc[-1])
    last_low = float(low.iloc[-1])
    last_close = float(close.iloc[-1])
    pivot = (last_high + last_low + last_close) / 3
    result["pivot_points"] = {
        "pivot": round(pivot, 2),
        "r1": round(2 * pivot - last_low, 2),
        "r2": round(pivot + (last_high - last_low), 2),
        "s1": round(2 * pivot - last_high, 2),
        "s2": round(pivot - (last_high - last_low), 2),
    }

    # Overall technical summary
    bullish_signals = 0
    bearish_signals = 0

    if result["rsi"]["signal"] == "OVERSOLD":
        bullish_signals += 1
    elif result["rsi"]["signal"] == "OVERBOUGHT":
        bearish_signals += 1

    if result["macd"]["signal"] == "BULLISH":
        bullish_signals += 1
    else:
        bearish_signals += 1

    if result.get("ma_alignment") in ["STRONGLY_BULLISH", "BULLISH"]:
        bullish_signals += 1
    elif result.get("ma_alignment") in ["STRONGLY_BEARISH", "BEARISH"]:
        bearish_signals += 1

    if result["stochastic"]["signal"] == "OVERSOLD":
        bullish_signals += 1
    elif result["stochastic"]["signal"] == "OVERBOUGHT":
        bearish_signals += 1

    result["overall_technical_signal"] = {
        "bullish_indicators": bullish_signals,
        "bearish_indicators": bearish_signals,
        "summary": "BULLISH"
        if bullish_signals > bearish_signals
        else "BEARISH"
        if bearish_signals > bullish_signals
        else "NEUTRAL",
    }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Compute technical indicators for a stock"
    )
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., NVDA, AAPL)")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    args = parser.parse_args()

    ticker = args.ticker.upper()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Computing technical indicators for {ticker}...")
    data = compute_indicators(ticker)

    output_file = output_dir / f"{ticker}_technical_indicators.json"
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"Indicators saved to {output_file}")

    # Print summary
    if "error" not in data:
        print(f"\nCurrent Price: ${data['current']['price']}")
        print(f"RSI(14): {data['rsi']['value']} ({data['rsi']['signal']})")
        print(f"MACD Signal: {data['macd']['signal']}")
        if "ma_alignment" in data:
            print(f"MA Alignment: {data['ma_alignment']}")
        print(f"Overall: {data['overall_technical_signal']['summary']}")


if __name__ == "__main__":
    main()
