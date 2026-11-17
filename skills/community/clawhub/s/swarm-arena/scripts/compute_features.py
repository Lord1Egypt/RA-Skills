#!/usr/bin/env python3
"""compute_features.py — indicator features from candles (SPEC section 5).

Computes per timeframe: EMA20, EMA50, EMA12, EMA26, RSI14 (Wilder), ATR14
(Wilder), MACD line/signal/histogram (12/26/9), volume_ratio vs the 20-bar
average, trend (up/down/neutral), momentum, high_volatility flag, and funding
rate passthrough.

Module use:
    from compute_features import compute_features
    feats = compute_features(candles, funding_rate=0.0001)

CLI:
    cat candles.json | python3 compute_features.py
    python3 compute_features.py candles.json
    python3 compute_features.py candles.json --funding-rate 0.0001

Input candle forms (all accepted): {"ts","open","high","low","close","volume"},
Lighter candle dicts {"t","o","h","l","c","v"}, or arrays [ts, o, h, l, c, v].
Candles must be oldest -> newest.
"""

import argparse
import json
import math
import sys

HIGH_VOLATILITY_ATR_MULTIPLE = 1.5  # ATR14 > 1.5x its 20-bar mean => high volatility
VOLUME_AVG_BARS = 20
MOMENTUM_BARS = 10


# ------------------------------------------------------------------ indicators

def ema_series(values, period):
    """EMA seeded with the SMA of the first `period` values (standard)."""
    if len(values) < period or period <= 0:
        return []
    k = 2.0 / (period + 1.0)
    out = [None] * (period - 1)
    ema = sum(values[:period]) / period
    out.append(ema)
    for v in values[period:]:
        ema = v * k + ema * (1.0 - k)
        out.append(ema)
    return out


def rsi_wilder(closes, period=14):
    if len(closes) <= period:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        ch = closes[i] - closes[i - 1]
        gains.append(max(ch, 0.0))
        losses.append(max(-ch, 0.0))
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100.0 - 100.0 / (1.0 + rs)


def atr_wilder(candles, period=14):
    """Returns (atr, atr_series_from_first_tr). TR needs the previous close."""
    if len(candles) <= period:
        return None, []
    trs = []
    for i in range(1, len(candles)):
        h, l, pc = candles[i]["high"], candles[i]["low"], candles[i - 1]["close"]
        trs.append(max(h - l, abs(h - pc), abs(l - pc)))
    atr = sum(trs[:period]) / period
    series = [atr]
    for tr in trs[period:]:
        atr = (atr * (period - 1) + tr) / period
        series.append(atr)
    return atr, series


def macd(closes, fast=12, slow=26, signal=9):
    if len(closes) < slow + signal:
        return None, None, None
    fast_e = ema_series(closes, fast)
    slow_e = ema_series(closes, slow)
    line_series = []
    for f, s in zip(fast_e, slow_e):
        line_series.append(None if (f is None or s is None) else f - s)
    valid = [v for v in line_series if v is not None]
    if len(valid) < signal:
        return valid[-1], None, None
    sig_series = ema_series(valid, signal)
    line = valid[-1]
    sig = sig_series[-1] if sig_series else None
    hist = (line - sig) if sig is not None else None
    return line, sig, hist


# ------------------------------------------------------------------- features

def normalize_candle(raw):
    if isinstance(raw, dict):
        close = raw.get("close", raw.get("c"))
        return {
            "ts": raw.get("ts", raw.get("t")),
            "open": raw.get("open", raw.get("o", close)),
            "high": raw.get("high", raw.get("h", close)),
            "low": raw.get("low", raw.get("l", close)),
            "close": close,
            "volume": raw.get("volume", raw.get("v", 0.0)) or 0.0,
        }
    seq = list(raw) + [None] * (6 - len(raw))
    return {"ts": seq[0], "open": seq[1], "high": seq[2], "low": seq[3],
            "close": seq[4], "volume": seq[5] or 0.0}


def compute_features(candles, funding_rate=None):
    candles = [normalize_candle(c) for c in candles]
    candles = [c for c in candles if c["close"] is not None]
    # Floor: RSI14 and ATR14 both need 15 bars to produce a first value.
    # Above that, compute whatever the history supports and flag partial so
    # callers (and the prompt) can discount confidence on shallow history.
    if len(candles) < 15:
        raise ValueError("need at least 15 candles, got %d" % len(candles))
    partial = len(candles) < 30
    closes = [float(c["close"]) for c in candles]
    volumes = [float(c["volume"]) for c in candles]
    last = closes[-1]

    # With fewer bars than the period, seed the EMA over the bars we have —
    # approximate but monotone-correct, and flagged via "partial"/"bars".
    ema20 = ema_series(closes, min(20, len(closes)))[-1]
    ema50 = ema_series(closes, 50)[-1] if len(closes) >= 50 else None
    ema12 = ema_series(closes, min(12, len(closes)))[-1]
    ema26 = ema_series(closes, 26)[-1] if len(closes) >= 26 else None
    rsi14 = rsi_wilder(closes, 14)
    atr14, atr_series = atr_wilder(candles, 14)
    macd_line, macd_signal, macd_hist = macd(closes)

    vol_window = volumes[-(VOLUME_AVG_BARS + 1):-1] or volumes[-VOLUME_AVG_BARS:]
    vol_avg = (sum(vol_window) / len(vol_window)) if vol_window else 0.0
    volume_ratio = (volumes[-1] / vol_avg) if vol_avg > 0 else 1.0

    if ema50 is None or ema20 is None:
        trend = "neutral"
    elif ema20 > ema50:
        trend = "up"
    elif ema20 < ema50:
        trend = "down"
    else:
        trend = "neutral"

    if len(closes) > MOMENTUM_BARS and closes[-1 - MOMENTUM_BARS] != 0:
        momentum = (last / closes[-1 - MOMENTUM_BARS] - 1.0) * 100.0
    else:
        momentum = 0.0

    high_volatility = False
    if atr14 is not None and len(atr_series) >= 20:
        atr_mean = sum(atr_series[-20:]) / 20.0
        high_volatility = atr_mean > 0 and atr14 > HIGH_VOLATILITY_ATR_MULTIPLE * atr_mean

    return {
        "last_price": last,
        "ema20": ema20,
        "ema50": ema50,
        "ema12": ema12,
        "ema26": ema26,
        "rsi14": rsi14,
        "atr14": atr14,
        "macd": macd_line,
        "macd_signal": macd_signal,
        "macd_histogram": macd_hist,
        "volume_ratio": volume_ratio,
        "trend": trend,
        "momentum": momentum,
        "high_volatility": high_volatility,
        "funding_rate": funding_rate,
        "bars": len(candles),
        "partial": partial,
    }


# ------------------------------------------------------------------------ CLI

def _read_json(arg):
    if arg and arg != "-":
        with open(arg, "r") as f:
            return json.load(f)
    return json.load(sys.stdin)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compute indicator features from candles")
    parser.add_argument("input", nargs="?", help="JSON file with candles (default: stdin)")
    parser.add_argument("--funding-rate", type=float, default=None)
    args = parser.parse_args(argv)
    payload = _read_json(args.input)
    if isinstance(payload, list):
        candles, funding = payload, args.funding_rate
    else:
        candles = payload.get("candles") or payload.get("c") or []
        funding = args.funding_rate if args.funding_rate is not None else payload.get("funding_rate")
    try:
        print(json.dumps(compute_features(candles, funding_rate=funding), indent=2))
    except ValueError as e:
        print(json.dumps({"error": str(e)}))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
