#!/usr/bin/env python3
"""approval_runner.py — approval-mode proposal builder (SPEC sections 4+6).

Runs the full scan for a symbol and, when the pipeline says "enter", emits a
PENDING_APPROVAL proposal dict instead of executing. The proposal is journaled
(status "pending_approval") and printed for a human or supervising agent to
approve. Approving is a human act: pipe the proposal to
live_execution_adapter.py with a live-mode config, or rerun with --execute and
a live config.

CLI: python3 approval_runner.py config.json ETH
"""

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import journal_trade                        # noqa: E402
from market_scan_from_lighter import scan_symbol   # noqa: E402
from risk_checks import risk_checks          # noqa: E402


def build_proposal(symbol, config, state, trades_path):
    proposal = scan_symbol(symbol, config, state=state)
    features_1h = (proposal.get("features") or {}).get("1h") or {}
    if proposal.get("decision") != "enter":
        journal_trade.journal_entry(trades_path, {
            "ts": proposal.get("ts"), "symbol": symbol.upper(), "mode": "approval",
            "decision": "wait", "signal": (proposal.get("signal_result") or {}).get("signal", "wait"),
            "signal_reason": proposal.get("reason"),
            "confidence": (proposal.get("signal_result") or {}).get("confidence", 0.0),
            "regime": "high_volatility" if features_1h.get("high_volatility")
                      else {"up": "trend_up", "down": "trend_down"}.get(features_1h.get("trend"), "range"),
            "market": proposal.get("market"), "features_1h": features_1h or None,
        })
        return {"status": "no_proposal", "reason": proposal.get("reason")}

    plan = proposal["order_plan"]
    checks = risk_checks(config, state, {
        "notional": plan["notional"], "margin": plan["margin"], "side": plan["side"],
        "quantity": plan["quantity"], "stop_loss": plan["stop_loss"],
        "take_profit": plan["take_profit"],
    }, account=proposal.get("account"))
    if not checks["ok"]:
        return {"status": "no_proposal",
                "reason": "risk checks failed: %s" % ", ".join(checks["blocked_by"])}

    pending = {
        "status": "PENDING_APPROVAL",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "symbol": symbol.upper(),
        "summary": "%s %.8f %s @ %.2f | SL %.2f TP %.2f | lev %sx | notional $%.2f | margin $%.2f"
                   % (plan["side"].upper(), plan["quantity"], plan["symbol"],
                      plan["entry_price"], plan["stop_loss"], plan["take_profit"],
                      plan["leverage"], plan["notional"], plan["margin"]),
        "confidence": proposal.get("confidence"),
        "confluence": proposal.get("confluence"),
        "order_plan": plan,
        "market": proposal.get("market"),
        "how_to_approve": "human review only: python3 scripts/live_execution_adapter.py "
                          "<live-config.json> proposal.json  (or approve via your supervising agent)",
    }
    journal_trade.journal_entry(trades_path, {
        "ts": pending["created_at"], "symbol": symbol.upper(), "mode": "approval",
        "decision": "pending_approval",
        "signal": (proposal.get("signal_result") or {}).get("signal"),
        "signal_reason": (proposal.get("signal_result") or {}).get("reason"),
        "confidence": proposal.get("confidence"),
        "confluence": proposal.get("confluence"),
        "order": {k: plan[k] for k in ("entry_price", "stop_loss", "take_profit",
                                       "leverage", "quantity", "notional", "side")},
        "status": "pending_approval",
        "market": proposal.get("market"), "features_1h": features_1h or None,
    })
    return pending


def main(argv=None):
    parser = argparse.ArgumentParser(description="Approval-mode proposal builder")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("symbol", help="market symbol, e.g. ETH")
    parser.add_argument("--state", default=None)
    parser.add_argument("--trades", default=None)
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

    result = build_proposal(args.symbol, config, state, trades_path)
    print(json.dumps(result, indent=2, default=str))
    return 0 if result.get("status") == "PENDING_APPROVAL" else 2


if __name__ == "__main__":
    sys.exit(main())
