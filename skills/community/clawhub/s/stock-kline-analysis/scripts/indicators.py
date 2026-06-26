"""
indicators.py — Step 3: Compute technical indicators on a normalised OHLCV frame.

Usage:
    from indicators import add_indicators, add_tf_indicators
    df_daily = add_indicators(df_daily)
    df_weekly, df_monthly = add_tf_indicators(df_weekly, df_monthly)
"""

import numpy as np
import pandas as pd


# ── Helpers ──────────────────────────────────────────────────────────────────

def _rsi14(close: pd.Series) -> pd.Series:
    """Wilder-smoothed RSI-14 via rolling mean (simple, avoids double .diff())."""
    delta = close.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    return 100 - (100 / (1 + gain / loss.replace(0, np.nan)))


# ── Full indicator suite (daily) ─────────────────────────────────────────────

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add MA5/20/60, Bollinger Bands (20,2), MACD (12/26/9), RSI-14, ATR-14
    and dynamic support/resistance to *df* (in-place copy).

    Also writes df.attrs["support"] and df.attrs["resistance"].

    Requires columns: date, open, high, low, close, volume.
    Minimum 20 bars for Bollinger; 60 bars recommended for MA60 + ATR.
    """
    df = df.copy()

    # ── Moving averages ──────────────────────────────────────────────────────
    df["ma5"]  = df["close"].rolling(5).mean()
    df["ma20"] = df["close"].rolling(20).mean()
    df["ma60"] = df["close"].rolling(60).mean()

    # ── Bollinger Bands (20, ±2σ) ────────────────────────────────────────────
    bb_mid         = df["close"].rolling(20).mean()
    bb_std         = df["close"].rolling(20).std(ddof=0)
    df["bb_mid"]   = bb_mid
    df["bb_upper"] = bb_mid + 2 * bb_std
    df["bb_lower"] = bb_mid - 2 * bb_std
    # bb_width expressed as percentage so 12.7 means 12.7%
    df["bb_width"] = (df["bb_upper"] - df["bb_lower"]) / bb_mid * 100

    # ── MACD (12/26/9) ───────────────────────────────────────────────────────
    ema12             = df["close"].ewm(span=12, adjust=False).mean()
    ema26             = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"]        = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"]   = df["macd"] - df["macd_signal"]

    # ── RSI-14 ───────────────────────────────────────────────────────────────
    df["rsi14"] = _rsi14(df["close"])

    # ── ATR-14 (Average True Range) ──────────────────────────────────────────
    hl  = df["high"] - df["low"]
    hcp = (df["high"] - df["close"].shift()).abs()
    lcp = (df["low"]  - df["close"].shift()).abs()
    tr  = pd.concat([hl, hcp, lcp], axis=1).max(axis=1)
    df["atr14"]   = tr.ewm(span=14, adjust=False).mean()
    df["atr_pct"] = df["atr14"] / df["close"] * 100  # ATR as % of price

    # ── Dynamic support / resistance ─────────────────────────────────────────
    recent = df.tail(60)
    df.attrs["support"]    = max(recent["low"].min(),  df["bb_lower"].iloc[-1])
    df.attrs["resistance"] = min(recent["high"].max(), df["bb_upper"].iloc[-1])

    return df


# ── Abbreviated suite for weekly / monthly trend alignment ───────────────────

def add_tf_indicators(*frames: pd.DataFrame | None) -> list[pd.DataFrame | None]:
    """
    Add MA20 and RSI-14 to each timeframe frame (weekly, monthly).
    Skips None frames (failed fetches) transparently.

    Usage:
        df_weekly, df_monthly = add_tf_indicators(df_weekly, df_monthly)
    """
    result = []
    for df in frames:
        if df is None:
            result.append(None)
            continue
        df = df.copy()
        df["ma20"]  = df["close"].rolling(20).mean()
        df["rsi14"] = _rsi14(df["close"])
        result.append(df)
    return result


# ── Quick smoke-test ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from fetch_kline import fetch_all_timeframes

    symbol = sys.argv[1] if len(sys.argv) > 1 else "000063"
    df_d, df_w, df_m = fetch_all_timeframes(symbol)
    df_d = add_indicators(df_d)
    df_w, df_m = add_tf_indicators(df_w, df_m)

    last = df_d.iloc[-1]
    print(f"MA5={last['ma5']:.2f}  MA20={last['ma20']:.2f}  MA60={last['ma60']:.2f}")
    print(f"BB upper={last['bb_upper']:.2f}  mid={last['bb_mid']:.2f}  lower={last['bb_lower']:.2f}  width={last['bb_width']:.1f}%")
    print(f"MACD={last['macd']:.4f}  Signal={last['macd_signal']:.4f}  Hist={last['macd_hist']:.4f}")
    print(f"RSI14={last['rsi14']:.1f}  ATR14={last['atr14']:.2f}  ATR%={last['atr_pct']:.2f}%")
    print(f"Support={df_d.attrs['support']:.2f}  Resistance={df_d.attrs['resistance']:.2f}")
    if df_w is not None:
        print(f"Weekly MA20={df_w['ma20'].iloc[-1]:.2f}  RSI={df_w['rsi14'].iloc[-1]:.1f}")
