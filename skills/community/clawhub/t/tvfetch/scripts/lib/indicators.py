#!/usr/bin/env python3
"""
Technical indicators — pure pandas, no external TA dependencies.

Supports: SMA, EMA, RSI, MACD, Bollinger Bands, ATR, Stochastic, OBV, VWAP.

Usage:
  python indicators.py SYMBOL TIMEFRAME BARS --indicators "sma:20,ema:12,rsi:14,macd,bb:20,atr:14,stoch"
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
from scripts.lib.validators import resolve_symbol, validate_timeframe, parse_bars
from scripts.lib.errors import handle_error, EXIT_OK
from scripts.lib.formatter import print_indicator_result
from scripts.lib.mock import load_fixture


# ── Indicator functions ──────────────────────────────────────────────────────

def compute_sma(close: pd.Series, period: int) -> pd.Series:
    """Simple Moving Average."""
    return close.rolling(window=period, min_periods=period).mean()


def compute_ema(close: pd.Series, period: int) -> pd.Series:
    """Exponential Moving Average."""
    return close.ewm(span=period, min_periods=period, adjust=False).mean()


def compute_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Relative Strength Index (Wilder's smoothing method)."""
    delta = close.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, float("nan"))
    return 100 - (100 / (1 + rs))


def compute_macd(
    close: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9,
) -> dict[str, pd.Series]:
    """MACD: line, signal, histogram."""
    ema_fast = compute_ema(close, fast)
    ema_slow = compute_ema(close, slow)
    macd_line = ema_fast - ema_slow
    signal_line = compute_ema(macd_line, signal)
    histogram = macd_line - signal_line
    return {"line": macd_line, "signal": signal_line, "histogram": histogram}


def compute_bollinger(
    close: pd.Series,
    period: int = 20,
    std_dev: float = 2.0,
) -> dict[str, pd.Series]:
    """Bollinger Bands: upper, middle, lower, %B."""
    mid = compute_sma(close, period)
    rolling_std = close.rolling(window=period, min_periods=period).std()
    upper = mid + std_dev * rolling_std
    lower = mid - std_dev * rolling_std
    pct_b = (close - lower) / (upper - lower)
    return {"upper": upper, "mid": mid, "lower": lower, "pct_b": pct_b}


def compute_atr(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    period: int = 14,
) -> pd.Series:
    """Average True Range."""
    prev_close = close.shift(1)
    tr = pd.DataFrame({
        "hl": high - low,
        "hc": (high - prev_close).abs(),
        "lc": (low - prev_close).abs(),
    }).max(axis=1)
    return tr.ewm(com=period - 1, min_periods=period).mean()


def compute_stochastic(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    k_period: int = 14,
    d_period: int = 3,
) -> dict[str, pd.Series]:
    """Stochastic Oscillator: %K and %D."""
    lowest_low = low.rolling(window=k_period, min_periods=k_period).min()
    highest_high = high.rolling(window=k_period, min_periods=k_period).max()
    denom = highest_high - lowest_low
    k = ((close - lowest_low) / denom.replace(0, float("nan"))) * 100
    d = k.rolling(window=d_period).mean()
    return {"k": k, "d": d}


def compute_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """On-Balance Volume."""
    direction = np.sign(close.diff())
    direction.iloc[0] = 0
    return (volume * direction).cumsum()


def compute_vwap(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    volume: pd.Series,
) -> pd.Series:
    """Volume Weighted Average Price (intraday approximation)."""
    typical_price = (high + low + close) / 3
    cum_tp_vol = (typical_price * volume).cumsum()
    cum_vol = volume.cumsum()
    return cum_tp_vol / cum_vol.replace(0, float("nan"))


# ── Spec parser ──────────────────────────────────────────────────────────────

def parse_indicator_spec(spec: str) -> list[tuple[str, dict]]:
    """
    Parse indicator specification string.
    Format: "sma:20,ema:12,rsi:14,macd,bb:20:2,atr:14,stoch,obv,vwap"
    Returns: [(name, {params}), ...]
    """
    indicators = []
    for part in spec.split(","):
        part = part.strip().lower()
        if not part:
            continue
        pieces = part.split(":")
        name = pieces[0]
        params = pieces[1:]
        indicators.append((name, params))
    return indicators


def add_indicators(df: pd.DataFrame, spec: str) -> tuple[pd.DataFrame, dict[str, float], list[str]]:
    """
    Parse indicator spec, compute all indicators, add columns to df.
    Returns: (df_with_indicators, latest_values, signal_strings)
    """
    close = df["close"]
    high = df["high"]
    low = df["low"]
    volume = df["volume"]

    latest = {}
    signals = []
    parsed = parse_indicator_spec(spec)

    for name, params in parsed:
        if name == "sma":
            period = int(params[0]) if params else 20
            col = f"SMA_{period}"
            df[col] = compute_sma(close, period)
            val = df[col].iloc[-1]
            if not pd.isna(val):
                latest[col] = float(val)
                if close.iloc[-1] > val:
                    signals.append(f"BULLISH: Price above {col} ({val:.4f})")
                else:
                    signals.append(f"BEARISH: Price below {col} ({val:.4f})")

        elif name == "ema":
            period = int(params[0]) if params else 12
            col = f"EMA_{period}"
            df[col] = compute_ema(close, period)
            val = df[col].iloc[-1]
            if not pd.isna(val):
                latest[col] = float(val)

        elif name == "rsi":
            period = int(params[0]) if params else 14
            col = f"RSI_{period}"
            df[col] = compute_rsi(close, period)
            val = df[col].iloc[-1]
            if not pd.isna(val):
                latest[col] = float(val)
                if val > 70:
                    signals.append(f"BEARISH: RSI {val:.1f} is overbought (>70)")
                elif val < 30:
                    signals.append(f"BULLISH: RSI {val:.1f} is oversold (<30)")
                else:
                    signals.append(f"NEUTRAL: RSI {val:.1f} (between 30-70)")

        elif name == "macd":
            fast = int(params[0]) if len(params) > 0 else 12
            slow = int(params[1]) if len(params) > 1 else 26
            sig = int(params[2]) if len(params) > 2 else 9
            macd = compute_macd(close, fast, slow, sig)
            df["MACD_LINE"] = macd["line"]
            df["MACD_SIGNAL"] = macd["signal"]
            df["MACD_HIST"] = macd["histogram"]
            for col_name, series in [("MACD_LINE", macd["line"]), ("MACD_SIGNAL", macd["signal"]), ("MACD_HIST", macd["histogram"])]:
                val = series.iloc[-1]
                if not pd.isna(val):
                    latest[col_name] = float(val)
            hist_val = macd["histogram"].iloc[-1]
            if not pd.isna(hist_val):
                if hist_val > 0:
                    signals.append(f"BULLISH: MACD histogram positive ({hist_val:.4f})")
                else:
                    signals.append(f"BEARISH: MACD histogram negative ({hist_val:.4f})")

        elif name in ("bb", "bollinger"):
            period = int(params[0]) if params else 20
            std_dev = float(params[1]) if len(params) > 1 else 2.0
            bb = compute_bollinger(close, period, std_dev)
            df["BB_UPPER"] = bb["upper"]
            df["BB_MID"] = bb["mid"]
            df["BB_LOWER"] = bb["lower"]
            df["BB_PCT_B"] = bb["pct_b"]
            for col_name, series in [("BB_UPPER", bb["upper"]), ("BB_MID", bb["mid"]),
                                       ("BB_LOWER", bb["lower"]), ("BB_PCT_B", bb["pct_b"])]:
                val = series.iloc[-1]
                if not pd.isna(val):
                    latest[col_name] = float(val)
            pctb = bb["pct_b"].iloc[-1]
            if not pd.isna(pctb):
                if pctb > 1:
                    signals.append(f"BEARISH: Price above upper Bollinger Band (%B={pctb:.2f})")
                elif pctb < 0:
                    signals.append(f"BULLISH: Price below lower Bollinger Band (%B={pctb:.2f})")
                else:
                    signals.append(f"NEUTRAL: Price within Bollinger Bands (%B={pctb:.2f})")

        elif name == "atr":
            period = int(params[0]) if params else 14
            col = f"ATR_{period}"
            df[col] = compute_atr(high, low, close, period)
            val = df[col].iloc[-1]
            if not pd.isna(val):
                latest[col] = float(val)

        elif name in ("stoch", "stochastic"):
            k_p = int(params[0]) if params else 14
            d_p = int(params[1]) if len(params) > 1 else 3
            stoch = compute_stochastic(high, low, close, k_p, d_p)
            df["STOCH_K"] = stoch["k"]
            df["STOCH_D"] = stoch["d"]
            for col_name, series in [("STOCH_K", stoch["k"]), ("STOCH_D", stoch["d"])]:
                val = series.iloc[-1]
                if not pd.isna(val):
                    latest[col_name] = float(val)
            k_val = stoch["k"].iloc[-1]
            if not pd.isna(k_val):
                if k_val > 80:
                    signals.append(f"BEARISH: Stochastic %K {k_val:.1f} is overbought (>80)")
                elif k_val < 20:
                    signals.append(f"BULLISH: Stochastic %K {k_val:.1f} is oversold (<20)")

        elif name == "obv":
            df["OBV"] = compute_obv(close, volume)
            val = df["OBV"].iloc[-1]
            if not pd.isna(val):
                latest["OBV"] = float(val)

        elif name == "vwap":
            df["VWAP"] = compute_vwap(high, low, close, volume)
            val = df["VWAP"].iloc[-1]
            if not pd.isna(val):
                latest["VWAP"] = float(val)
                if close.iloc[-1] > val:
                    signals.append(f"BULLISH: Price above VWAP ({val:.4f})")
                else:
                    signals.append(f"BEARISH: Price below VWAP ({val:.4f})")

    return df, latest, signals


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute technical indicators")
    parser.add_argument("symbol")
    parser.add_argument("timeframe", nargs="?", default="1D")
    parser.add_argument("bars", nargs="?", default="500")
    parser.add_argument("--indicators", "-i", required=True, help='Spec: "sma:20,rsi:14,macd,bb:20"')
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
            return 1
    else:
        try:
            import tvfetch
            result = tvfetch.fetch(symbol, timeframe, bars, auth_token=cfg.auth_token)
        except Exception as exc:
            return handle_error(exc, symbol, timeframe)

    df = result.df
    if df.empty:
        print("ERROR_TYPE: InsufficientData", file=sys.stderr)
        return 1

    _, latest_values, signals = add_indicators(df, args.indicators)

    print_indicator_result(
        symbol=symbol,
        timeframe=timeframe,
        latest_close=float(df["close"].iloc[-1]),
        indicators=latest_values,
        signals=signals,
    )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
