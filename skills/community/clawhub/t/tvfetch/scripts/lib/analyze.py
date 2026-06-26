#!/usr/bin/env python3
"""
Statistical analysis on fetched OHLCV data.

Computes: return, volatility, Sharpe, max drawdown, trend direction,
moving averages, RSI, and provides a plain-language interpretation.

Usage:
  python analyze.py SYMBOL TIMEFRAME BARS [--mock] [--token TOKEN]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SKILL_DIR))

from scripts.lib.config import get_config
from scripts.lib.validators import resolve_symbol, validate_timeframe, parse_bars, TIMEFRAME_LABELS
from scripts.lib.errors import handle_error, EXIT_OK
from scripts.lib.formatter import print_analysis_result
from scripts.lib.mock import load_fixture

# Approximate trading bars per year for annualization
BARS_PER_YEAR = {
    "1": 525600, "3": 175200, "5": 105120, "10": 52560, "15": 35040,
    "30": 17520, "45": 11680, "60": 8760, "120": 4380, "180": 2920,
    "240": 2190, "1D": 252, "1W": 52, "1M": 12,
}


def _compute_sma(close: pd.Series, period: int) -> float | None:
    """Return latest SMA value, or None if insufficient data."""
    if len(close) < period:
        return None
    return float(close.rolling(period).mean().iloc[-1])


def _compute_rsi(close: pd.Series, period: int = 14) -> float | None:
    """Wilder's RSI. Returns None if insufficient data."""
    if len(close) < period + 1:
        return None
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, float("nan"))
    rsi = 100 - (100 / (1 + rs))
    val = rsi.iloc[-1]
    return float(val) if not pd.isna(val) else None


def _max_drawdown(close: pd.Series) -> tuple[float, str, str]:
    """Returns (max_dd_pct, peak_date, trough_date)."""
    rolling_max = close.cummax()
    drawdown = (close - rolling_max) / rolling_max * 100
    min_idx = drawdown.idxmin()
    peak_idx = close[:min_idx].idxmax()
    return float(drawdown.min()), str(peak_idx.strftime("%Y-%m-%d")), str(min_idx.strftime("%Y-%m-%d"))


def analyze(df: pd.DataFrame, symbol: str, timeframe: str) -> dict:
    """Run full statistical analysis on OHLCV DataFrame."""
    close = df["close"]
    bars = len(df)

    # Basic return
    first_close = float(close.iloc[0])
    latest_close = float(close.iloc[-1])
    period_return = (latest_close - first_close) / first_close * 100

    # Annualized return
    bpy = BARS_PER_YEAR.get(timeframe, 252)
    period_years = bars / bpy if bpy > 0 else 1
    ann_return = ((1 + period_return / 100) ** (1 / period_years) - 1) * 100 if period_years > 0 else 0

    # Volatility
    returns = close.pct_change().dropna()
    daily_vol = float(returns.std()) * 100
    ann_vol = daily_vol * np.sqrt(bpy)

    # Sharpe (risk-free rate = 0)
    sharpe = ann_return / ann_vol if ann_vol > 0 else 0.0

    # Max drawdown
    max_dd, dd_start, dd_end = _max_drawdown(close)

    # Range
    period_high = float(df["high"].max())
    period_high_date = df["high"].idxmax().strftime("%Y-%m-%d")
    period_low = float(df["low"].min())
    period_low_date = df["low"].idxmin().strftime("%Y-%m-%d")

    # Volume
    avg_volume = float(df["volume"].mean())
    total_volume = float(df["volume"].sum())

    # Moving averages
    sma_20 = _compute_sma(close, 20)
    sma_50 = _compute_sma(close, 50)
    sma_200 = _compute_sma(close, 200)

    # RSI
    rsi_14 = _compute_rsi(close, 14)

    # Trend direction
    above_sma20 = latest_close > sma_20 if sma_20 else None
    above_sma50 = latest_close > sma_50 if sma_50 else None
    above_sma200 = latest_close > sma_200 if sma_200 else None

    if above_sma20 and above_sma50:
        trend = "uptrend"
    elif above_sma20 is False and above_sma50 is False:
        trend = "downtrend"
    else:
        trend = "sideways"

    # Interpretation
    interpretation = _build_interpretation(
        symbol, period_return, ann_vol, latest_close,
        sma_20, sma_50, sma_200, rsi_14, max_dd, dd_start, dd_end, trend,
    )

    return {
        "SYMBOL": symbol,
        "TIMEFRAME": timeframe,
        "TIMEFRAME_LABEL": TIMEFRAME_LABELS.get(timeframe, timeframe),
        "BARS": bars,
        "DATE_FROM": df.index[0].strftime("%Y-%m-%d"),
        "DATE_TO": df.index[-1].strftime("%Y-%m-%d"),
        "LATEST_CLOSE": latest_close,
        "PERIOD_RETURN_PCT": round(period_return, 2),
        "ANN_RETURN_PCT": round(ann_return, 2),
        "VOLATILITY_DAILY_PCT": round(daily_vol, 2),
        "ANN_VOLATILITY_PCT": round(ann_vol, 2),
        "SHARPE_RATIO": round(sharpe, 2),
        "MAX_DRAWDOWN_PCT": round(max_dd, 2),
        "MAX_DD_START": dd_start,
        "MAX_DD_END": dd_end,
        "PERIOD_HIGH": period_high,
        "PERIOD_HIGH_DATE": period_high_date,
        "PERIOD_LOW": period_low,
        "PERIOD_LOW_DATE": period_low_date,
        "AVG_VOLUME": round(avg_volume, 2),
        "TOTAL_VOLUME": round(total_volume, 2),
        "SMA_20": round(sma_20, 4) if sma_20 else "N/A",
        "SMA_50": round(sma_50, 4) if sma_50 else "N/A",
        "SMA_200": round(sma_200, 4) if sma_200 else "N/A",
        "RSI_14": round(rsi_14, 1) if rsi_14 else "N/A",
        "TREND": trend,
        "ABOVE_SMA20": above_sma20,
        "ABOVE_SMA50": above_sma50,
        "ABOVE_SMA200": above_sma200,
        "INTERPRETATION": interpretation,
    }


def _build_interpretation(
    symbol, ret, vol, close, sma20, sma50, sma200, rsi, max_dd, dd_start, dd_end, trend
) -> str:
    """Build 3-4 sentence plain-language interpretation."""
    lines = []

    # Return + volatility sentence
    direction = "gained" if ret > 0 else "declined"
    lines.append(
        f"{symbol} has {direction} {abs(ret):.1f}% over the period "
        f"with {vol:.1f}% annualized volatility."
    )

    # Moving average sentence
    above = []
    if sma20 and close > sma20:
        above.append("SMA20")
    if sma50 and close > sma50:
        above.append("SMA50")
    if sma200 and close > sma200:
        above.append("SMA200")

    if len(above) == 3:
        lines.append(f"Price is above all three major moving averages ({', '.join(above)}), indicating sustained {trend}.")
    elif above:
        lines.append(f"Price is above {', '.join(above)}, suggesting {trend} conditions.")
    else:
        lines.append(f"Price is below key moving averages, suggesting {trend} conditions.")

    # RSI sentence
    if rsi is not None:
        if rsi > 70:
            lines.append(f"RSI at {rsi:.1f} indicates overbought conditions — a pullback may be likely.")
        elif rsi < 30:
            lines.append(f"RSI at {rsi:.1f} indicates oversold conditions — a bounce may be possible.")
        else:
            lines.append(f"RSI at {rsi:.1f} is in neutral territory.")

    # Drawdown sentence
    lines.append(f"Maximum drawdown of {max_dd:.1f}% occurred between {dd_start} and {dd_end}.")

    return " ".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze OHLCV data")
    parser.add_argument("symbol")
    parser.add_argument("timeframe", nargs="?", default="1D")
    parser.add_argument("bars", nargs="?", default="500")
    parser.add_argument("--token", help="Auth token")
    parser.add_argument("--mock", action="store_true")
    args = parser.parse_args()

    try:
        symbol = resolve_symbol(args.symbol)
        timeframe = validate_timeframe(args.timeframe)
        bars = parse_bars(args.bars)
    except ValueError as exc:
        return handle_error(exc, args.symbol)

    cfg = get_config(cli_token=args.token)

    if args.mock or cfg.mock_mode:
        result = load_fixture(symbol, timeframe, bars)
        if result is None or not result.bars:
            print("ERROR_TYPE: NoMockData", file=sys.stderr)
            print(f"ERROR_MESSAGE: No fixture for {symbol}/{timeframe}", file=sys.stderr)
            return 1
    else:
        try:
            import tvfetch
            result = tvfetch.fetch(symbol, timeframe, bars, auth_token=cfg.auth_token)
        except Exception as exc:
            return handle_error(exc, symbol, timeframe)

    df = result.df
    if df.empty or len(df) < 2:
        print("ERROR_TYPE: InsufficientData", file=sys.stderr)
        print(f"ERROR_MESSAGE: Need at least 2 bars for analysis, got {len(df)}", file=sys.stderr)
        return 1

    stats = analyze(df, symbol, timeframe)
    print_analysis_result(stats)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
