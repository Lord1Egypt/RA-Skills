#!/usr/bin/env python3
"""size_position.py — risk-based position sizing (SPEC section 5).

  risk_usd  = equity * risk_pct
  stop_distance_pct = |entry - stop| / entry
  notional  = risk_usd / stop_distance_pct      (capped at max_notional)
  margin    = notional / leverage
  quantity  = notional / entry                  (rounded DOWN to size_decimals)

Suppressed (returns suppressed=true, quantity=0) when the result is below the
market's min_quote_amount or min_base_amount — a trade that small is noise.

CLI: echo '{"equity": 10000, "entry_price": 2400, "stop_loss": 2364, ...}' \
       | python3 size_position.py
"""

import argparse
import json
import math
import sys


def _floor_step(value, decimals):
    factor = 10 ** int(decimals)
    return math.floor(float(value) * factor + 1e-9) / factor


def size_position(equity, risk_pct, entry_price, stop_loss, leverage,
                  price_decimals=2, size_decimals=4,
                  min_base_amount=0.0, min_quote_amount=0.0,
                  max_notional=0.0):
    entry_price = float(entry_price)
    stop_loss = float(stop_loss)
    equity = float(equity)
    leverage = max(1, int(leverage))
    if entry_price <= 0:
        return {"quantity": 0.0, "notional": 0.0, "margin": 0.0, "suppressed": True,
                "reason": "entry price must be positive"}
    if entry_price == stop_loss:
        return {"quantity": 0.0, "notional": 0.0, "margin": 0.0, "suppressed": True,
                "reason": "zero stop distance"}

    risk_usd = equity * float(risk_pct)
    stop_distance_pct = abs(entry_price - stop_loss) / entry_price
    notional = risk_usd / stop_distance_pct

    scaled_down = False
    if max_notional and max_notional > 0 and notional > max_notional:
        notional = float(max_notional)
        scaled_down = True

    quantity = _floor_step(notional / entry_price, size_decimals)
    notional = round(quantity * entry_price, 6)  # recompute after rounding down
    margin = notional / leverage

    suppressed, reason = False, ""
    if min_quote_amount and notional < float(min_quote_amount):
        suppressed, reason = True, "notional %.4f below market min_quote_amount %.4f" % (notional, float(min_quote_amount))
    elif min_base_amount and quantity < float(min_base_amount):
        suppressed, reason = True, "quantity %.8f below market min_base_amount %.8f" % (quantity, float(min_base_amount))
    if suppressed:
        quantity, margin = 0.0, 0.0

    return {
        "quantity": quantity,
        "notional": round(notional, 6),
        "margin": round(margin, 6),
        "risk_usd": round(risk_usd, 6),
        "stop_distance_pct": round(stop_distance_pct, 8),
        "leverage": leverage,
        "scaled_down_to_max_notional": scaled_down,
        "suppressed": suppressed,
        "reason": reason or ("sized %.8f units ($%.2f notional, $%.2f margin)" % (quantity, notional, margin)),
    }


def _read_json(arg):
    if arg and arg != "-":
        with open(arg, "r") as f:
            return json.load(f)
    return json.load(sys.stdin)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Risk-based position sizing")
    parser.add_argument("input", nargs="?", help="JSON payload (default: stdin)")
    args = parser.parse_args(argv)
    payload = _read_json(args.input)
    result = size_position(
        equity=payload.get("equity", 0.0),
        risk_pct=payload.get("risk_pct", payload.get("risk_pct_per_trade", 0.01)),
        entry_price=payload.get("entry_price"),
        stop_loss=payload.get("stop_loss"),
        leverage=payload.get("leverage", 1),
        price_decimals=payload.get("price_decimals", 2),
        size_decimals=payload.get("size_decimals", 4),
        min_base_amount=payload.get("min_base_amount", 0.0),
        min_quote_amount=payload.get("min_quote_amount", 0.0),
        max_notional=payload.get("max_notional", payload.get("max_notional_per_trade", 0.0)),
    )
    print(json.dumps(result, indent=2))
    return 0 if not result["suppressed"] else 2


if __name__ == "__main__":
    sys.exit(main())
