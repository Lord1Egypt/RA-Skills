#!/usr/bin/env python3
"""trailing_stop.py — ATR trailing stop + breakeven rule (SPEC section 5).

Rules for each known open position older than minimum_hold_sec:
  breakeven   once unrealized PnL >= +0.5%, move the stop to entry price
  trail       stop tracks price ∓ 1.5 x ATR(1h) — long: ratchet UP only,
              short: ratchet DOWN only. NEVER moves against the position.

Paper mode updates state.known_open_positions[symbol].stop_loss in place.
Live modes cancel + re-place the reduce-only SL order via the signer and store
the new order index. A failed re-place leaves the OLD stop untouched (cancel
happens only after the new order is accepted).

CLI: python3 trailing_stop.py config.json
"""

import argparse
import calendar
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from lighter_rest_client import LighterRestClient, LighterAPIError, to_int_price, to_int_size  # noqa: E402
from compute_features import compute_features  # noqa: E402

TRAIL_ATR_MULT = 1.5
BREAKEVEN_TRIGGER_PCT = 0.005  # +0.5% unrealized PnL arms breakeven


def _parse_ts(ts):
    if not ts:
        return 0.0
    try:
        return calendar.timegm(time.strptime(ts, "%Y-%m-%dT%H:%M:%SZ"))
    except (ValueError, TypeError):
        return 0.0


def _new_stop(pos, last_price, atr, price_decimals):
    """Candidate stop; returns (price, reason) or (None, why-not)."""
    side = pos.get("side")
    entry = float(pos["entry_price"])
    current_sl = float(pos["stop_loss"])
    qty = float(pos["quantity"])
    if atr is None or atr <= 0 or qty <= 0:
        return None, "no ATR"
    unrealized_pct = ((last_price - entry) / entry) * (1 if side == "long" else -1)

    candidates = []
    if unrealized_pct >= BREAKEVEN_TRIGGER_PCT:
        candidates.append((entry, "breakeven"))
    trail = (last_price - TRAIL_ATR_MULT * atr) if side == "long" \
        else (last_price + TRAIL_ATR_MULT * atr)
    candidates.append((trail, "atr_trail"))

    if side == "long":
        valid = [(p, r) for p, r in candidates if p > current_sl and p < last_price]
        if not valid:
            return None, "no upward ratchet"
        best = max(valid, key=lambda c: c[0])
    else:
        valid = [(p, r) for p, r in candidates if p < current_sl and p > last_price]
        if not valid:
            return None, "no downward ratchet"
        best = min(valid, key=lambda c: c[0])
    return round(best[0], int(price_decimals)), best[1]


def run_trailing_stops(config, state, trades_path=None, client=None):
    mode = config.get("mode", "paper")
    client = client or LighterRestClient(base_url=config.get("base_url"),
                                         gateway=config.get("gateway"))
    gateway_cfg = config.get("gateway")
    min_hold = int(config.get("minimum_hold_sec", 0) or 0)
    now = time.time()
    actions, errors = [], []

    for symbol, pos in list((state.get("known_open_positions") or {}).items()):
        if min_hold and now - _parse_ts(pos.get("opened_at")) < min_hold:
            continue
        try:
            market = client.get_market(symbol)
            last = market.get("mark_price") or market.get("last_trade_price")
            candles = client.get_candles(market["market_id"], "1h", 60)
            atr = compute_features(candles).get("atr14")
        except LighterAPIError as e:
            errors.append("%s: %s" % (symbol, e))
            continue
        except ValueError:
            atr = None
        if not last:
            errors.append("%s: no price" % symbol)
            continue
        new_sl, reason = _new_stop(pos, last, atr, market["price_decimals"])
        if new_sl is None:
            continue

        if mode in ("live", "autonomous_live"):
            import lighter_signer
            old_index = (pos.get("order_indexes") or {}).get("sl")
            market_id = market["market_id"]
            size_int = to_int_size(pos["quantity"], market["size_decimals"])
            trigger_int = to_int_price(new_sl, market["price_decimals"])
            placed = lighter_signer.create_stop_loss(market_id, pos["side"],
                                                     size_int, trigger_int,
                                                     gateway=gateway_cfg)
            if not placed.get("ok"):
                errors.append("%s: SL re-place failed: %s" % (symbol, placed.get("error")))
                continue
            if old_index:
                cancel = lighter_signer.cancel_order(market_id, old_index,
                                                     gateway=gateway_cfg)
                if not cancel.get("ok"):
                    errors.append("%s: old SL cancel failed: %s (both stops live!)"
                                  % (symbol, cancel.get("error")))
            pos.setdefault("order_indexes", {})["sl"] = placed.get("order_index")

        pos["stop_loss"] = new_sl
        pos["trailing_active"] = reason == "atr_trail"
        pos["breakeven_armed"] = True
        actions.append({"symbol": symbol, "new_stop_loss": new_sl, "reason": reason,
                        "last_price": last})
    return {"actions": actions, "errors": errors}


def main(argv=None):
    parser = argparse.ArgumentParser(description="ATR trailing stop manager")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("--state", default=None)
    args = parser.parse_args(argv)
    with open(args.config) as f:
        config = json.load(f)
    base = os.path.dirname(os.path.abspath(args.config))
    state_path = args.state or os.path.join(base, "state.json")
    if not os.path.exists(state_path):
        print(json.dumps({"actions": [], "errors": [], "note": "no state.json yet"}))
        return 0
    import filelock
    with filelock.held(state_path):  # no-op when already held by autonomous_runner
        with open(state_path) as f:
            state = json.load(f)
        result = run_trailing_stops(config, state)
        tmp = state_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(state, f, indent=2)
            f.write("\n")
        os.replace(tmp, state_path)
    print(json.dumps(result, indent=2, default=str))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
