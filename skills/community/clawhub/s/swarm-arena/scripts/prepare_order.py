#!/usr/bin/env python3
"""prepare_order.py — final order plan with wire-integer conversion.

Takes the sized proposal plus market metadata and produces the execution plan:
rounded float prices/quantities AND the integer wire values (price_int,
size_int, trigger ints) that lighter_signer.place_bracket() consumes.

Bracket (SPEC section 5):
  entry       MARKET + IOC (immediate-or-cancel)
  stop_loss   STOP_LOSS with trigger_price, reduce_only=True
  take_profit TAKE_PROFIT with trigger_price, reduce_only=True

CLI: cat payload.json | python3 prepare_order.py
Input: {"symbol","side","entry_price","stop_loss","take_profit","quantity",
        "leverage","notional","margin","market":{"market_id","price_decimals",
        "size_decimals"}}
"""

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lighter_rest_client import to_int_price, to_int_size  # noqa: E402


def _round(value, decimals):
    return round(float(value), int(decimals))


def _floor(value, decimals):
    factor = 10 ** int(decimals)
    return math.floor(float(value) * factor + 1e-9) / factor


def prepare_order(symbol, side, entry_price, stop_loss, take_profit, quantity,
                  leverage, notional=None, margin=None, market=None):
    market = market or {}
    price_decimals = int(market.get("price_decimals", 2))
    size_decimals = int(market.get("size_decimals", 4))
    side = side.lower()
    if side not in ("long", "short"):
        raise ValueError("side must be long or short")

    entry = _round(entry_price, price_decimals)
    sl = _round(stop_loss, price_decimals)
    tp = _round(take_profit, price_decimals)
    qty = _floor(quantity, size_decimals)
    if qty <= 0:
        raise ValueError("quantity rounds to zero at %d size decimals" % size_decimals)

    # Bracket sanity: long exits below/above entry; short mirrored.
    if side == "long" and not (sl < entry < tp):
        raise ValueError("long bracket must satisfy stop_loss < entry < take_profit")
    if side == "short" and not (tp < entry < sl):
        raise ValueError("short bracket must satisfy take_profit < entry < stop_loss")

    if notional is None:
        notional = qty * entry
    if margin is None:
        margin = notional / max(1, int(leverage))

    return {
        "symbol": symbol.upper(),
        "market_index": market.get("market_id", market.get("market_index")),
        "side": side,
        "is_ask": side == "short",          # entry direction; exits invert it
        "entry_price": entry,
        "stop_loss": sl,
        "take_profit": tp,
        "quantity": qty,
        "leverage": int(leverage),
        "notional": round(float(notional), 6),
        "margin": round(float(margin), 6),
        "wire": {
            "entry": {"order_type": "MARKET", "time_in_force": "IOC",
                      "price_int": to_int_price(entry, price_decimals),
                      "size_int": to_int_size(qty, size_decimals),
                      "reduce_only": False},
            "stop_loss": {"order_type": "STOP_LOSS", "reduce_only": True,
                          "trigger_price_int": to_int_price(sl, price_decimals),
                          "price_int": to_int_price(sl, price_decimals),
                          "size_int": to_int_size(qty, size_decimals)},
            "take_profit": {"order_type": "TAKE_PROFIT", "reduce_only": True,
                            "trigger_price_int": to_int_price(tp, price_decimals),
                            "price_int": to_int_price(tp, price_decimals),
                            "size_int": to_int_size(qty, size_decimals)},
        },
    }


def _read_json(arg):
    if arg and arg != "-":
        with open(arg, "r") as f:
            return json.load(f)
    return json.load(sys.stdin)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Prepare bracket order plan with wire integers")
    parser.add_argument("input", nargs="?", help="JSON payload (default: stdin)")
    args = parser.parse_args(argv)
    p = _read_json(args.input)
    try:
        plan = prepare_order(p.get("symbol"), p.get("side"), p.get("entry_price"),
                             p.get("stop_loss"), p.get("take_profit"), p.get("quantity"),
                             p.get("leverage", 1), p.get("notional"), p.get("margin"),
                             p.get("market"))
    except (ValueError, TypeError) as e:
        print(json.dumps({"error": str(e)}))
        return 1
    print(json.dumps(plan, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
