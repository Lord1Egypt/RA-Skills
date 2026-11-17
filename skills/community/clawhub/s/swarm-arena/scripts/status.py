#!/usr/bin/env python3
"""status.py — human + JSON status view (SPEC section 6).

Shows: mode, halt, circuit breaker, consecutive errors, daily loss vs limit,
equity, available margin, daily PnL, open positions (with uPnL placeholder or
live mark), trade stats, adaptive learning metrics, lessons, config summary.

CLI: python3 status.py config.json [--json]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import journal_trade  # noqa: E402


def build_status(config, state, entries):
    metrics = state.get("metrics") or {}
    account = state.get("account") or {}
    closed = [e for e in entries if e.get("status") == "closed"]
    executed = [e for e in entries if e.get("decision") == "executed"]
    wins = [e for e in closed if e.get("outcome") == "win"]
    total_pnl = sum(float(e.get("realised_pnl") or 0) for e in closed)

    positions = {}
    for symbol, pos in (state.get("known_open_positions") or {}).items():
        positions[symbol] = dict(pos)
        positions[symbol]["unrealized_pnl"] = None  # filled by live callers; placeholder here

    return {
        "mode": config.get("mode", "paper"),
        "halt": bool(state.get("halt")),
        "circuit_breaker": bool(state.get("circuit_breaker")),
        "consecutive_errors": int(state.get("consecutive_errors", 0) or 0),
        "daily_loss": float(state.get("daily_loss", 0) or 0),
        "daily_loss_date": state.get("daily_loss_date"),
        "last_run": state.get("last_run"),
        "last_error": state.get("last_error"),
        "equity": account.get("equity"),
        "available_margin": account.get("available_margin"),
        "daily_pnl": account.get("daily_pnl"),
        "positions": positions,
        "trades": {
            "total": len(entries),
            "executed": len(executed),
            "closed": len(closed),
            "wins": len(wins),
            "win_rate": round(len(wins) / len(closed), 4) if closed else 0.0,
            "total_pnl": round(total_pnl, 6),
        },
        "adaptive_metrics": {
            "confidence_multiplier": metrics.get("confidence_multiplier", 1.0),
            "effective_leverage_cap": metrics.get("effective_leverage_cap", config.get("max_leverage")),
            "recommended_min_confidence": metrics.get("recommended_min_confidence", 0.55),
            "leverage_reduction_active": metrics.get("leverage_reduction_active", False),
            "underperforming_symbols": metrics.get("underperforming_symbols", []),
        },
        "lessons": metrics.get("lessons", []),
        "limits": {
            "max_daily_loss": config.get("max_daily_loss"),
            "max_total_exposure": config.get("max_total_exposure"),
            "max_notional_per_trade": config.get("max_notional_per_trade"),
            "max_leverage": config.get("max_leverage"),
            "max_concurrent_positions": config.get("max_concurrent_positions"),
        },
        "config_summary": {
            "allowed_symbols": config.get("allowed_symbols"),
            "risk_pct_per_trade": config.get("risk_pct_per_trade"),
            "allow_short": config.get("allow_short"),
            "require_stop_loss": config.get("require_stop_loss"),
            "require_take_profit": config.get("require_take_profit"),
            "min_reward_risk": config.get("min_reward_risk"),
        },
    }


def _print_human(s):
    flags = []
    if s["halt"]:
        flags.append("HALTED")
    if s["circuit_breaker"]:
        flags.append("CIRCUIT-BREAKER")
    health = " ".join(flags) if flags else "OK"
    print("swarmArena status — mode=%s  health=%s  errors=%d"
          % (s["mode"].upper(), health, s["consecutive_errors"]))
    if s.get("last_run"):
        print("last run: %s" % s["last_run"])
    if s.get("last_error"):
        print("last error: %s (%s)" % (s["last_error"].get("message"),
                                       s["last_error"].get("ts")))
    lim = s["limits"]["max_daily_loss"] or 0
    print("daily loss: $%.2f%s   daily PnL: %s"
          % (s["daily_loss"], (" / $%.2f limit" % lim) if lim else "",
             ("$%.2f" % s["daily_pnl"]) if s.get("daily_pnl") is not None else "n/a"))
    eq = s.get("equity")
    am = s.get("available_margin")
    print("equity: %s   available margin: %s"
          % (("$%.2f" % eq) if eq is not None else "n/a",
             ("$%.2f" % am) if am is not None else "n/a"))
    if s["positions"]:
        print("open positions:")
        for symbol, pos in sorted(s["positions"].items()):
            print("  %-5s %-5s qty=%.8f entry=%.2f SL=%.2f TP=%.2f lev=%sx"
                  % (symbol, pos.get("side"), pos.get("quantity", 0),
                     pos.get("entry_price", 0), pos.get("stop_loss", 0),
                     pos.get("take_profit", 0), pos.get("leverage", "?")))
    else:
        print("open positions: none")
    t = s["trades"]
    print("trades: total=%d executed=%d closed=%d win rate=%.1f%% total PnL=$%.2f"
          % (t["total"], t["executed"], t["closed"], t["win_rate"] * 100, t["total_pnl"]))
    m = s["adaptive_metrics"]
    print("adaptive: confidence x%.2f, leverage cap %s (reduction %s), min confidence %.2f"
          % (m["confidence_multiplier"], m["effective_leverage_cap"],
             "active" if m["leverage_reduction_active"] else "inactive",
             m["recommended_min_confidence"]))
    if m["underperforming_symbols"]:
        print("underperforming symbols (informational): %s" % ", ".join(m["underperforming_symbols"]))
    for lesson in s["lessons"]:
        print("  lesson: %s" % lesson)


def main(argv=None):
    parser = argparse.ArgumentParser(description="swarmArena status")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("--state", default=None)
    parser.add_argument("--trades", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    with open(args.config) as f:
        config = json.load(f)
    base = os.path.dirname(os.path.abspath(args.config))
    state_path = args.state or os.path.join(base, "state.json")
    trades_path = args.trades or os.path.join(base, "trades.json")
    state = {}
    if os.path.exists(state_path):
        with open(state_path) as f:
            state = json.load(f)
    entries = journal_trade.load_journal(trades_path) if os.path.exists(trades_path) else []

    status = build_status(config, state, entries)
    if args.json:
        print(json.dumps(status, indent=2, default=str))
    else:
        _print_human(status)
    return 0


if __name__ == "__main__":
    sys.exit(main())
