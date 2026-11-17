#!/usr/bin/env python3
"""trade_loop.py — one-symbol trading cycle (SPEC section 5).

Order of operations:
  1. halt / circuit-breaker guard
  2. per-symbol cooldown after last close (cooldown_after_close_sec)
  3. duplicate guard (symbol already in state.known_open_positions)
  4. scan (market_scan_from_lighter) -> wait decisions are journaled too
  5. learning adjustment: threshold = max(base, recommended_min_confidence);
     adjusted_confidence = confidence * confidence_multiplier
  6. risk_checks hard gates
  7. execute via live_execution_adapter (mode guard inside)
  8. journal everything; on fill, record state.known_open_positions[symbol]

Module:  from trade_loop import run_trade_loop
CLI:     python3 trade_loop.py config.json ETH
"""

import argparse
import calendar
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import journal_trade                       # noqa: E402
import filelock                            # noqa: E402
from market_scan_from_lighter import scan_symbol   # noqa: E402
from risk_checks import risk_checks        # noqa: E402
from live_execution_adapter import execute_order   # noqa: E402


def _parse_ts(ts):
    if not ts:
        return 0.0
    try:
        return calendar.timegm(time.strptime(ts, "%Y-%m-%dT%H:%M:%SZ"))
    except (ValueError, TypeError):
        return 0.0


def _regime(features_1h):
    trend = (features_1h or {}).get("trend")
    if (features_1h or {}).get("high_volatility"):
        return "high_volatility"
    return {"up": "trend_up", "down": "trend_down"}.get(trend, "range")


def run_trade_loop(symbol, config, state, state_path, trades_path,
                   client=None, offline=None, execute=True):
    symbol = symbol.upper()
    mode = config.get("mode", "paper")
    now = time.time()

    if state.get("halt") or state.get("circuit_breaker"):
        return {"symbol": symbol, "decision": "blocked",
                "reason": "halted" if state.get("halt") else "circuit_breaker"}

    last_close = _parse_ts((state.get("last_close_ts") or {}).get(symbol))
    cooldown = int(config.get("cooldown_after_close_sec", 0) or 0)
    if last_close and cooldown > 0 and now - last_close < cooldown:
        return {"symbol": symbol, "decision": "cooldown",
                "reason": "cooldown %ds remaining" % int(cooldown - (now - last_close))}

    if symbol in (state.get("known_open_positions") or {}):
        return {"symbol": symbol, "decision": "blocked",
                "reason": "position already open on %s" % symbol}

    proposal = scan_symbol(symbol, config, state=state, client=client, offline=offline)
    features_1h = (proposal.get("features") or {}).get("1h") or {}
    signal_result = proposal.get("signal_result") or {}
    metrics = state.get("metrics") or {}

    # persist the account snapshot used for sizing (keeps status meaningful)
    proposal_account = proposal.get("account") or {}
    if proposal_account.get("equity") is not None:
        account = state.setdefault("account", {})
        account["equity"] = proposal_account["equity"]
        if proposal_account.get("available_margin") is not None:
            account["available_margin"] = proposal_account["available_margin"]
        account.setdefault("daily_pnl", 0.0)
        account["updated_at"] = journal_trade.utcnow()

    journal = {
        "ts": proposal.get("ts") or journal_trade.utcnow(),
        "symbol": symbol,
        "mode": mode,
        "signal": signal_result.get("signal", "wait"),
        "signal_reason": signal_result.get("reason") or proposal.get("reason"),
        "confidence": signal_result.get("confidence", 0.0),
        "adjusted_confidence": signal_result.get("confidence", 0.0),
        "regime": _regime(features_1h),
        "confluence": proposal.get("confluence"),
        "market": proposal.get("market"),
        "features_1h": features_1h or None,
    }

    if proposal.get("decision") != "enter":
        journal.update({"decision": "wait" if proposal.get("decision") != "error" else "error",
                        "signal_reason": proposal.get("reason")})
        journal_trade.journal_entry(trades_path, journal)
        return {"symbol": symbol, "decision": journal["decision"], "reason": proposal.get("reason")}

    # --- learning-adjusted gate
    threshold = max(signal_result.get("threshold", 0.55),
                    float(metrics.get("recommended_min_confidence", 0.55) or 0.55))
    mult = float(metrics.get("confidence_multiplier", 1.0) or 1.0)
    adjusted = round(signal_result["confidence"] * mult, 4)
    journal["adjusted_confidence"] = adjusted
    if adjusted < threshold:
        journal.update({"decision": "wait",
                        "signal_reason": "adjusted confidence %.3f below learned threshold %.2f"
                        % (adjusted, threshold)})
        journal_trade.journal_entry(trades_path, journal)
        return {"symbol": symbol, "decision": "wait", "reason": journal["signal_reason"]}

    plan = proposal["order_plan"]
    checks = risk_checks(config, state, {
        "notional": plan["notional"], "margin": plan["margin"], "side": plan["side"],
        "quantity": plan["quantity"], "stop_loss": plan["stop_loss"],
        "take_profit": plan["take_profit"],
    }, account=proposal.get("account"))
    if not checks["ok"]:
        journal.update({"decision": "blocked",
                        "signal_reason": "risk checks failed: %s" % ", ".join(checks["blocked_by"]),
                        "order": _order_view(plan)})
        journal_trade.journal_entry(trades_path, journal)
        return {"symbol": symbol, "decision": "blocked", "reason": journal["signal_reason"]}

    exec_result = {"status": "skipped"} if not execute else execute_order(plan, config)
    journal.update({
        "decision": "executed" if exec_result.get("status") in ("executed", "simulated") else exec_result.get("status", "error"),
        "order": _order_view(plan),
        "exec_result": exec_result,
        "status": "open" if exec_result.get("status") in ("executed", "simulated") else "journaled",
    })
    stored = journal_trade.journal_entry(trades_path, journal)

    if exec_result.get("status") in ("executed", "simulated"):
        state.setdefault("known_open_positions", {})[symbol] = {
            "side": plan["side"],
            "quantity": plan["quantity"],
            "entry_price": exec_result.get("filled_price") or plan["entry_price"],
            "leverage": plan["leverage"],
            "stop_loss": plan["stop_loss"],
            "take_profit": plan["take_profit"],
            "opened_at": journal["ts"],
            "order_indexes": exec_result.get("order_indexes") or {"entry": None, "sl": None, "tp": None},
        }
        if state_path:
            _save_state(state_path, state)
    return {"symbol": symbol, "decision": stored["decision"], "status": exec_result.get("status"),
            "journal_ts": stored["ts"]}


def _order_view(plan):
    return {
        "entry_price": plan.get("entry_price"), "stop_loss": plan.get("stop_loss"),
        "take_profit": plan.get("take_profit"), "leverage": plan.get("leverage"),
        "quantity": plan.get("quantity"), "notional": plan.get("notional"),
        "side": plan.get("side"),
    }


def _save_state(path, state):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")
    os.replace(tmp, path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="One-symbol trading cycle")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("symbol", help="market symbol, e.g. ETH")
    parser.add_argument("--state", default=None, help="state.json (default: beside config)")
    parser.add_argument("--trades", default=None, help="trades.json (default: beside config)")
    parser.add_argument("--offline", default=None, help="fixture JSON (no exchange calls)")
    parser.add_argument("--no-execute", action="store_true", help="stop before execution")
    args = parser.parse_args(argv)

    with open(args.config) as f:
        config = json.load(f)
    base = os.path.dirname(os.path.abspath(args.config))
    state_path = args.state or os.path.join(base, "state.json")
    trades_path = args.trades or os.path.join(base, "trades.json")
    offline = None
    if args.offline:
        with open(args.offline) as f:
            offline = json.load(f)
    with filelock.held(state_path):  # no-op when already held by autonomous_runner
        state = {}
        if os.path.exists(state_path):
            with open(state_path) as f:
                state = json.load(f)
        result = run_trade_loop(args.symbol, config, state, state_path, trades_path,
                                offline=offline, execute=not args.no_execute)
    print(json.dumps(result, indent=2, default=str))
    return 0 if result.get("decision") == "executed" else 2


if __name__ == "__main__":
    sys.exit(main())
