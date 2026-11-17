#!/usr/bin/env python3
"""live_execution_adapter.py — the ONLY path from a prepared order to the venue.

Mode guard (SPEC section 4):
  paper            -> simulated fill at the plan's entry price, zero writes
  approval         -> never executes; returns status "pending_approval"
  live             -> executes, unless execution.require_human_approval_for_live_orders
                      is true, in which case it returns "pending_approval"
  autonomous_live  -> executes immediately (consent was locked at onboarding)

Every real execution is the full bracket via lighter_signer.place_bracket():
entry MARKET/IOC + STOP_LOSS(reduce_only) + TAKE_PROFIT(reduce_only).

Module:  from live_execution_adapter import execute_order
CLI:     cat order_plan.json | python3 live_execution_adapter.py config.json
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def execute_order(plan, config, prompt_fn=None):
    """Execute (or simulate/route) a prepare_order plan. Returns exec_result dict."""
    mode = config.get("mode", "paper")
    symbol = plan.get("symbol")

    if mode == "paper":
        return {
            "status": "simulated",
            "filled_price": plan.get("entry_price"),
            "quantity": plan.get("quantity"),
            "order_indexes": {"entry": None, "sl": None, "tp": None},
            "note": "paper mode: no order sent to Lighter",
        }

    if mode == "approval":
        return {
            "status": "pending_approval",
            "order_indexes": {"entry": None, "sl": None, "tp": None},
            "note": "approval mode: proposal emitted, nothing executed",
        }

    if mode == "live" and (config.get("execution") or {}).get("require_human_approval_for_live_orders"):
        prompt_fn = prompt_fn or _default_prompt
        summary = ("%s %s %.8f @ %.2f (SL %.2f / TP %.2f, lev %s, notional $%.2f)"
                   % (symbol, plan.get("side"), plan.get("quantity", 0.0),
                      plan.get("entry_price", 0.0), plan.get("stop_loss", 0.0),
                      plan.get("take_profit", 0.0), plan.get("leverage"),
                      plan.get("notional", 0.0)))
        answer = prompt_fn("APPROVE live order? %s [y/N]: " % summary)
        if answer.strip().lower() not in ("y", "yes"):
            return {"status": "rejected_by_operator", "order_indexes": {"entry": None, "sl": None, "tp": None}}

    if mode not in ("live", "autonomous_live"):
        return {"status": "blocked", "error": "unknown mode %r" % mode,
                "order_indexes": {"entry": None, "sl": None, "tp": None}}

    wire = plan.get("wire") or {}
    entry = wire.get("entry") or {}
    sl = wire.get("stop_loss") or {}
    tp = wire.get("take_profit") or {}
    if not (entry.get("size_int") and entry.get("price_int") and sl.get("trigger_price_int") and tp.get("trigger_price_int")):
        return {"status": "blocked", "error": "plan missing wire integers",
                "order_indexes": {"entry": None, "sl": None, "tp": None}}

    import lighter_signer
    result = lighter_signer.place_bracket(
        market_index=plan.get("market_index"),
        side=plan.get("side"),
        size_int=entry["size_int"],
        entry_price_int=entry["price_int"],
        sl_trigger_int=sl["trigger_price_int"],
        tp_trigger_int=tp["trigger_price_int"],
        gateway=config.get("gateway"),
    )
    return {
        "status": "executed" if result.get("ok") else "error",
        "filled_price": plan.get("entry_price"),
        "quantity": plan.get("quantity"),
        "order_indexes": result.get("order_indexes") or {"entry": None, "sl": None, "tp": None},
        "bracket": {k: v for k, v in result.items() if k in ("entry", "stop_loss", "take_profit")},
        "error": result.get("error"),
        "executed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def _default_prompt(message):
    if sys.stdin.isatty():
        return input(message)
    return ""


def _read_json(arg):
    if arg and arg != "-":
        with open(arg, "r") as f:
            return json.load(f)
    return json.load(sys.stdin)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Mode-guarded order execution adapter")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("plan", nargs="?", help="order plan JSON file (default: stdin)")
    args = parser.parse_args(argv)
    with open(args.config) as f:
        config = json.load(f)
    plan = _read_json(args.plan)
    result = execute_order(plan, config)
    print(json.dumps(result, indent=2, default=str))
    return 0 if result.get("status") in ("executed", "simulated") else 2


if __name__ == "__main__":
    sys.exit(main())
