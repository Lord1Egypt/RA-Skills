#!/usr/bin/env python3
"""recommend_leverage.py — CLIENT-SIDE leverage cap only (SPEC sections 3+5).

Lighter has NO leverage endpoint. This value is never sent to the exchange; it
only scales client-side sizing (margin = notional / leverage).

  confidence < 0.60        -> min_leverage
  0.60 <= confidence < 0.80 -> midpoint of [min, max] (rounded)
  confidence >= 0.80       -> max_leverage
  high_volatility          -> minus 1 (floor: min_leverage)
  learning cap             -> min(result, state.metrics.effective_leverage_cap)

CLI:  echo '{"confidence": 0.72}' | python3 recommend_leverage.py
      python3 recommend_leverage.py --confidence 0.85 --min 2 --max 10
"""

import argparse
import json
import sys

MID_BAND = (0.60, 0.80)


def recommend_leverage(confidence, min_leverage=2, max_leverage=10,
                       high_volatility=False, effective_cap=None):
    min_leverage = max(1, int(min_leverage))
    max_leverage = max(min_leverage, int(max_leverage))
    confidence = float(confidence)

    if confidence < MID_BAND[0]:
        lev, band = min_leverage, "low confidence (<0.60) -> minimum"
    elif confidence < MID_BAND[1]:
        lev, band = int(round((min_leverage + max_leverage) / 2.0)), "mid confidence (0.60-0.79) -> midpoint"
    else:
        lev, band = max_leverage, "high confidence (>=0.80) -> maximum"

    if high_volatility and lev > min_leverage:
        lev = max(min_leverage, lev - 1)
        band += "; high volatility -1"

    capped_by_learning = False
    if effective_cap is not None:
        cap = max(min_leverage, int(effective_cap))
        if lev > cap:
            lev = cap
            capped_by_learning = True

    return {
        "leverage": lev,
        "min_leverage": min_leverage,
        "max_leverage": max_leverage,
        "effective_leverage_cap": effective_cap,
        "capped_by_learning": capped_by_learning,
        "high_volatility": bool(high_volatility),
        "client_side_only": True,
        "reason": band,
    }


def _read_json(arg):
    if arg and arg != "-":
        with open(arg, "r") as f:
            return json.load(f)
    return json.load(sys.stdin)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Client-side leverage recommendation")
    parser.add_argument("input", nargs="?", help="JSON payload (default: stdin)")
    parser.add_argument("--confidence", type=float, default=None)
    parser.add_argument("--min", dest="min_leverage", type=int, default=None)
    parser.add_argument("--max", dest="max_leverage", type=int, default=None)
    parser.add_argument("--high-volatility", action="store_true", default=None)
    parser.add_argument("--cap", type=int, default=None, help="learning effective_leverage_cap")
    args = parser.parse_args(argv)

    payload = {}
    if args.input or not sys.stdin.isatty():
        try:
            payload = _read_json(args.input)
        except Exception:
            payload = {}
    confidence = args.confidence if args.confidence is not None else payload.get("confidence", 0.0)
    result = recommend_leverage(
        confidence,
        min_leverage=args.min_leverage or payload.get("min_leverage", 2),
        max_leverage=args.max_leverage or payload.get("max_leverage", 10),
        high_volatility=(args.high_volatility
                         if args.high_volatility is not None
                         else payload.get("high_volatility", False)),
        effective_cap=args.cap if args.cap is not None else payload.get("effective_leverage_cap"),
    )
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
