#!/usr/bin/env python3
"""Fetch technical indicators for a ticker: SMA-50, SMA-200, RSI(14), MACD, 52-week high/low."""
import argparse
import json
import sys


def compute_rsi(prices, period=14):
    """Compute RSI from a price series."""
    deltas = prices.diff().dropna()
    gains = deltas.where(deltas > 0, 0.0)
    losses = (-deltas).where(deltas < 0, 0.0)
    avg_gain = gains.rolling(window=period, min_periods=period).mean()
    avg_loss = losses.rolling(window=period, min_periods=period).mean()
    # Use exponential smoothing after initial window
    for i in range(period, len(avg_gain)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gains.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + losses.iloc[i]) / period
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi


def compute_macd(prices, fast=12, slow=26, signal=9):
    """Compute MACD line, signal line, and histogram."""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def main():
    parser = argparse.ArgumentParser(description="Fetch technical indicators for a stock ticker.")
    parser.add_argument("ticker", help="Stock ticker symbol")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run with: uv run --with yfinance", file=sys.stderr)
        sys.exit(1)

    ticker = args.ticker.upper()
    t = yf.Ticker(ticker)

    # Need ~1 year of data for 200-day SMA and 52-week range
    hist = t.history(period="1y")
    if hist.empty:
        print(json.dumps({"error": f"No historical data for {ticker}"}))
        sys.exit(1)

    close = hist["Close"]
    current_price = float(close.iloc[-1])

    # SMA
    sma_50 = float(close.rolling(50).mean().iloc[-1]) if len(close) >= 50 else None
    sma_200 = float(close.rolling(200).mean().iloc[-1]) if len(close) >= 200 else None

    # RSI
    rsi_series = compute_rsi(close, 14)
    rsi_val = float(rsi_series.iloc[-1]) if not rsi_series.dropna().empty else None

    # MACD
    macd_line, signal_line, histogram = compute_macd(close)
    macd_data = {
        "macd_line": round(float(macd_line.iloc[-1]), 4),
        "signal_line": round(float(signal_line.iloc[-1]), 4),
        "histogram": round(float(histogram.iloc[-1]), 4),
    }

    # 52-week high/low
    high_52w = float(hist["High"].max())
    low_52w = float(hist["Low"].min())

    result = {
        "ticker": ticker,
        "current_price": round(current_price, 2),
        "sma_50": round(sma_50, 2) if sma_50 else None,
        "sma_200": round(sma_200, 2) if sma_200 else None,
        "rsi_14": round(rsi_val, 2) if rsi_val else None,
        "macd": macd_data,
        "52_week_high": round(high_52w, 2),
        "52_week_low": round(low_52w, 2),
        "price_vs_52w_high_pct": round((current_price / high_52w - 1) * 100, 2),
        "price_vs_52w_low_pct": round((current_price / low_52w - 1) * 100, 2),
        "sma_50_trend": "above" if sma_50 and current_price > sma_50 else "below" if sma_50 else None,
        "sma_200_trend": "above" if sma_200 and current_price > sma_200 else "below" if sma_200 else None,
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
