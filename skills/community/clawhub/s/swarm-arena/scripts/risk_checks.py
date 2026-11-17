#!/usr/bin/env python3
"""risk_checks.py — hard pre-trade risk gates (SPEC sections 5+7).

Hard blocks (only limits set > 0 are enforced):
  daily_loss_limit    state.daily_loss >= config.max_daily_loss
  total_exposure      current exposure + new notional > config.max_total_exposure
  per_trade_notional  new notional > config.max_notional_per_trade
  available_margin    required margin > account.available_margin
  zero_notional       notional or quantity <= 0
  halt                state.halt is true
  circuit_breaker     state.circuit_breaker is true
  allow_short         config.allow_short false and side is short
  stop_loss_required  config.require_stop_loss and order lacks stop_loss
  take_profit_required config.require_take_profit and order lacks take_profit

CLI: cat payload.json | python3 risk_checks.py
Input: {"config": {...}, "state": {...}, "order": {"notional","margin","side",
        "stop_loss","take_profit","quantity"}, "account": {"available_margin"}}
"""

import argparse
import json
import sys


def _num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def risk_checks(config, state, order, account=None):
    config = config or {}
    state = state or {}
    order = order or {}
    account = account or (state.get("account") or {})
    checks = []

    def add(name, ok, detail=""):
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    add("halt", not state.get("halt"), "halt flag set" if state.get("halt") else "")
    add("circuit_breaker", not state.get("circuit_breaker"),
        "circuit breaker tripped" if state.get("circuit_breaker") else "")

    side = (order.get("side") or "").lower()
    add("allow_short", side != "short" or config.get("allow_short", True),
        "shorts disabled by config" if side == "short" and not config.get("allow_short", True) else "")

    notional = _num(order.get("notional"))
    quantity = _num(order.get("quantity"))
    margin = _num(order.get("margin"))

    add("zero_notional", notional > 0 and quantity > 0,
        "notional=%s quantity=%s" % (notional, quantity) if not (notional > 0 and quantity > 0) else "")

    max_daily_loss = _num(config.get("max_daily_loss"))
    if max_daily_loss > 0:
        daily_loss = _num(state.get("daily_loss"))
        add("daily_loss_limit", daily_loss < max_daily_loss,
            "daily loss %.2f of limit %.2f" % (daily_loss, max_daily_loss))
    else:
        add("daily_loss_limit", True, "disabled")

    max_exposure = _num(config.get("max_total_exposure"))
    if max_exposure > 0:
        exposure = 0.0
        for sym, pos in (state.get("known_open_positions") or {}).items():
            exposure += abs(_num(pos.get("quantity")) * _num(pos.get("entry_price")))
        exposure_after = exposure + notional
        add("total_exposure", exposure_after <= max_exposure,
            "exposure %.2f -> %.2f of cap %.2f" % (exposure, exposure_after, max_exposure))
    else:
        add("total_exposure", True, "disabled")

    max_notional = _num(config.get("max_notional_per_trade"))
    if max_notional > 0:
        add("per_trade_notional", notional <= max_notional,
            "notional %.2f of cap %.2f" % (notional, max_notional))
    else:
        add("per_trade_notional", True, "disabled")

    available = account.get("available_margin")
    if available is not None and _num(available) > 0:
        add("available_margin", margin <= _num(available),
            "needs %.2f, have %.2f" % (margin, _num(available)))
    else:
        add("available_margin", True, "unknown balance (skipped)")

    add("stop_loss_required",
        not config.get("require_stop_loss", True) or _num(order.get("stop_loss")) > 0,
        "missing stop_loss" if config.get("require_stop_loss", True) and _num(order.get("stop_loss")) <= 0 else "")
    add("take_profit_required",
        not config.get("require_take_profit", True) or _num(order.get("take_profit")) > 0,
        "missing take_profit" if config.get("require_take_profit", True) and _num(order.get("take_profit")) <= 0 else "")

    blocked_by = [c["name"] for c in checks if not c["ok"]]
    return {"ok": not blocked_by, "blocked_by": blocked_by, "checks": checks}


def _read_json(arg):
    if arg and arg != "-":
        with open(arg, "r") as f:
            return json.load(f)
    return json.load(sys.stdin)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Hard pre-trade risk gates")
    parser.add_argument("input", nargs="?", help="JSON payload (default: stdin)")
    args = parser.parse_args(argv)
    payload = _read_json(args.input)
    result = risk_checks(payload.get("config"), payload.get("state"),
                         payload.get("order"), payload.get("account"))
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    sys.exit(main())
