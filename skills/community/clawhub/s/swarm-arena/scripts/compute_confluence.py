#!/usr/bin/env python3
"""compute_confluence.py — 9-check confluence model (SPEC section 5).

confidence = passed / 9. Minimum to enter: 0.55 (0.70 in high volatility).

  check                   passes when
  trend_alignment         4h trend AND 1h trend both match the signal direction
  momentum_confirmation   1h momentum sign matches direction
  volume_confirmation     1h volume_ratio >= 0.75
  rsi_zone                long: 40 <= rsi <= 70 | short: 30 <= rsi <= 60
  macd_alignment          1h MACD histogram sign matches direction
  reward_risk_ok          |tp-entry| / |entry-sl| >= min_reward_risk
  exposure_capacity_ok    exposure_after < 90% of max_total_exposure
  position_capacity_ok    open_positions < max_concurrent_positions
  timeframe_confluence    5m trend or 5m price-vs-ema20 agrees with direction

Module:  from compute_confluence import compute_confluence
CLI:     cat payload.json | python3 compute_confluence.py
Input:   {"signal": <compute_signal output>, "features": {"5m":..,"1h":..,"4h":..},
          "context": {"entry_price","stop_loss","take_profit","min_reward_risk",
                      "current_exposure","max_total_exposure","proposed_notional",
                      "open_positions","max_concurrent_positions"}}
"""

import argparse
import json
import sys

MIN_CONFIDENCE = 0.55
HIGH_VOL_MIN_CONFIDENCE = 0.70
VOLUME_CONFIRM_RATIO = 0.75
RSI_ZONE_LONG = (40.0, 70.0)
RSI_ZONE_SHORT = (30.0, 60.0)
EXPOSURE_HEADROOM = 0.90
CHECK_NAMES = [
    "trend_alignment", "momentum_confirmation", "volume_confirmation",
    "rsi_zone", "macd_alignment", "reward_risk_ok", "exposure_capacity_ok",
    "position_capacity_ok", "timeframe_confluence",
]


def compute_confluence(signal, features_by_tf, context=None):
    context = context or {}
    direction = signal.get("signal") if isinstance(signal, dict) else signal
    if direction not in ("long", "short"):
        return {"passed": [], "failed": list(CHECK_NAMES), "count": 0,
                "total": 9, "confidence": 0.0, "direction": direction,
                "min_confidence": MIN_CONFIDENCE, "enter": False,
                "reason": "no directional signal"}

    f1 = features_by_tf.get("1h") or {}
    f4 = features_by_tf.get("4h") or {}
    f5 = features_by_tf.get("5m") or {}
    high_vol = bool(f1.get("high_volatility"))
    min_conf = HIGH_VOL_MIN_CONFIDENCE if high_vol else MIN_CONFIDENCE
    up = direction == "long"
    results = {}

    results["trend_alignment"] = (
        f4.get("trend") == ("up" if up else "down")
        and f1.get("trend") == ("up" if up else "down"))

    mom = f1.get("momentum")
    results["momentum_confirmation"] = mom is not None and ((up and mom > 0) or (not up and mom < 0))

    vol = f1.get("volume_ratio")
    results["volume_confirmation"] = vol is not None and vol >= VOLUME_CONFIRM_RATIO

    rsi = f1.get("rsi14")
    lo, hi = RSI_ZONE_LONG if up else RSI_ZONE_SHORT
    results["rsi_zone"] = rsi is not None and lo <= rsi <= hi

    hist = f1.get("macd_histogram")
    if hist is None and f1.get("macd") is not None and f1.get("macd_signal") is not None:
        hist = f1["macd"] - f1["macd_signal"]
    results["macd_alignment"] = hist is not None and ((up and hist > 0) or (not up and hist < 0))

    entry = context.get("entry_price")
    sl = context.get("stop_loss")
    tp = context.get("take_profit")
    min_rr = float(context.get("min_reward_risk", 1.5))
    if entry and sl and tp and entry != sl:
        risk = abs(entry - sl)
        reward = abs(tp - entry)
        results["reward_risk_ok"] = risk > 0 and (reward / risk) >= min_rr
    else:
        results["reward_risk_ok"] = False

    max_exposure = float(context.get("max_total_exposure", 0) or 0)
    if max_exposure > 0:
        exposure_after = float(context.get("current_exposure", 0) or 0) + float(context.get("proposed_notional", 0) or 0)
        results["exposure_capacity_ok"] = exposure_after < EXPOSURE_HEADROOM * max_exposure
    else:
        results["exposure_capacity_ok"] = True

    open_positions = int(context.get("open_positions", 0) or 0)
    max_positions = int(context.get("max_concurrent_positions", 0) or 0)
    results["position_capacity_ok"] = max_positions <= 0 or open_positions < max_positions

    t5 = f5.get("trend")
    p5, ema5 = f5.get("last_price"), f5.get("ema20")
    price_ok = p5 is not None and ema5 is not None and ((up and p5 > ema5) or (not up and p5 < ema5))
    results["timeframe_confluence"] = t5 == ("up" if up else "down") or price_ok

    passed = [n for n in CHECK_NAMES if results[n]]
    failed = [n for n in CHECK_NAMES if not results[n]]
    confidence = len(passed) / 9.0
    enter = confidence >= min_conf
    return {
        "passed": passed,
        "failed": failed,
        "count": len(passed),
        "total": 9,
        "confidence": round(confidence, 4),
        "min_confidence": min_conf,
        "high_volatility": high_vol,
        "direction": direction,
        "enter": enter,
        "reason": ("confluence %.3f >= %.2f" % (confidence, min_conf)) if enter
                  else ("confluence %.3f below %.2f (failed: %s)" % (confidence, min_conf, ", ".join(failed))),
    }


def _read_json(arg):
    if arg and arg != "-":
        with open(arg, "r") as f:
            return json.load(f)
    return json.load(sys.stdin)


def main(argv=None):
    parser = argparse.ArgumentParser(description="9-check confluence model")
    parser.add_argument("input", nargs="?", help="JSON payload (default: stdin)")
    args = parser.parse_args(argv)
    payload = _read_json(args.input)
    result = compute_confluence(payload.get("signal", {}), payload.get("features", {}),
                                payload.get("context", {}))
    print(json.dumps(result, indent=2))
    return 0 if result["enter"] else 2


if __name__ == "__main__":
    sys.exit(main())
