#!/usr/bin/env python3
"""compute_signal.py — weighted long/short scoring (SPEC section 5).

Long and short are scored INDEPENDENTLY; each component contributes its weight
when it supports that direction:

  component         weight  long when                       short when
  4h trend          2.0     trend_4h == "up"                trend_4h == "down"
  1h trend          2.0     trend_1h == "up"                trend_1h == "down"
  RSI zone (1h)     1.5     45 <= rsi <= 68                 32 <= rsi <= 55
  MACD cross (1h)   1.0     macd > macd_signal              macd < macd_signal
  5m timing         0.5     5m trend up or price>ema20      5m trend down or price<ema20
  volume (1h)       1.0     volume_ratio >= 0.8             volume_ratio >= 0.8
  EMA20 pos (1h)    1.0     price > ema20                   price < ema20
  funding bias      0.5     funding_rate < 0                funding_rate > 0

confidence = score / 9.5. Entry when the best side's confidence >= threshold
(0.55, raised to 0.70 under high_volatility on the 1h). Otherwise "wait".
A perfect tie between sides resolves to "wait".

Module:  from compute_signal import compute_signal
CLI:     cat features.json | python3 compute_signal.py
         python3 compute_signal.py features.json
Input:   {"features": {"5m": {...}, "1h": {...}, "4h": {...}}}
         (also accepts {"5m": ..., "1h": ..., "4h": ...} at top level)
"""

import argparse
import json
import sys

WEIGHTS = {
    "trend_4h": 2.0,
    "trend_1h": 2.0,
    "rsi_zone": 1.5,
    "macd_cross": 1.0,
    "timing_5m": 0.5,
    "volume": 1.0,
    "ema20_position": 1.0,
    "funding_bias": 0.5,
}
TOTAL_WEIGHT = sum(WEIGHTS.values())  # 9.5

BASE_THRESHOLD = 0.55
HIGH_VOL_THRESHOLD = 0.70

RSI_LONG = (45.0, 68.0)
RSI_SHORT = (32.0, 55.0)
VOLUME_MIN_RATIO = 0.8


def _side_supports(direction, f5, f1, f4):
    """Which components fire for one direction. Returns list of names."""
    fired = []
    t4 = f4.get("trend")
    t1 = f1.get("trend")
    rsi = f1.get("rsi14")
    macd, macd_sig = f1.get("macd"), f1.get("macd_signal")
    price = f1.get("last_price")
    ema20 = f1.get("ema20")
    vol = f1.get("volume_ratio")
    funding = f1.get("funding_rate")
    p5, ema5, t5 = f5.get("last_price"), f5.get("ema20"), f5.get("trend")

    if t4 == ("up" if direction == "long" else "down"):
        fired.append("trend_4h")
    if t1 == ("up" if direction == "long" else "down"):
        fired.append("trend_1h")
    if rsi is not None:
        lo, hi = RSI_LONG if direction == "long" else RSI_SHORT
        if lo <= rsi <= hi:
            fired.append("rsi_zone")
    if macd is not None and macd_sig is not None:
        if (direction == "long" and macd > macd_sig) or (direction == "short" and macd < macd_sig):
            fired.append("macd_cross")
    if direction == "long":
        if t5 == "up" or (p5 is not None and ema5 is not None and p5 > ema5):
            fired.append("timing_5m")
    else:
        if t5 == "down" or (p5 is not None and ema5 is not None and p5 < ema5):
            fired.append("timing_5m")
    if vol is not None and vol >= VOLUME_MIN_RATIO:
        fired.append("volume")
    if price is not None and ema20 is not None:
        if (direction == "long" and price > ema20) or (direction == "short" and price < ema20):
            fired.append("ema20_position")
    if funding is not None:
        # Negative funding pays longs / taxes shorts; positive does the reverse.
        if (direction == "long" and funding < 0) or (direction == "short" and funding > 0):
            fired.append("funding_bias")
    return fired


def compute_signal(features_by_tf, threshold=None):
    f5 = features_by_tf.get("5m") or {}
    f1 = features_by_tf.get("1h") or {}
    f4 = features_by_tf.get("4h") or {}
    high_vol = bool(f1.get("high_volatility"))
    threshold = float(threshold) if threshold is not None else (HIGH_VOL_THRESHOLD if high_vol else BASE_THRESHOLD)

    fired_long = _side_supports("long", f5, f1, f4)
    fired_short = _side_supports("short", f5, f1, f4)
    score_long = sum(WEIGHTS[c] for c in fired_long)
    score_short = sum(WEIGHTS[c] for c in fired_short)
    conf_long = score_long / TOTAL_WEIGHT
    conf_short = score_short / TOTAL_WEIGHT

    if conf_long > conf_short:
        side, confidence, fired = "long", conf_long, fired_long
    elif conf_short > conf_long:
        side, confidence, fired = "short", conf_short, fired_short
    else:
        side, confidence, fired = "wait", conf_long, fired_long

    if side != "wait" and confidence < threshold:
        reason = "confidence %.3f below threshold %.2f (%s components: %s)" % (
            confidence, threshold, side, ", ".join(fired) or "none")
        side = "wait"
    elif side == "wait":
        reason = "no directional edge (long %.3f / short %.3f, threshold %.2f)" % (
            conf_long, conf_short, threshold)
    else:
        reason = "%s %.3f >= %.2f via %s" % (side, confidence, threshold, ", ".join(fired))

    return {
        "signal": side,
        "confidence": round(confidence, 4),
        "score_long": score_long,
        "score_short": score_short,
        "confidence_long": round(conf_long, 4),
        "confidence_short": round(conf_short, 4),
        "max_score": TOTAL_WEIGHT,
        "threshold": threshold,
        "high_volatility": high_vol,
        "components": {"long": fired_long, "short": fired_short},
        "reason": reason,
    }


def _read_json(arg):
    if arg and arg != "-":
        with open(arg, "r") as f:
            return json.load(f)
    return json.load(sys.stdin)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Weighted signal scoring (long/short independent)")
    parser.add_argument("input", nargs="?", help="JSON file with per-timeframe features (default: stdin)")
    parser.add_argument("--threshold", type=float, default=None, help="override entry threshold")
    args = parser.parse_args(argv)
    payload = _read_json(args.input)
    features = payload.get("features", payload)
    result = compute_signal(features, threshold=args.threshold)
    print(json.dumps(result, indent=2))
    return 0 if result["signal"] != "wait" else 2


if __name__ == "__main__":
    sys.exit(main())
