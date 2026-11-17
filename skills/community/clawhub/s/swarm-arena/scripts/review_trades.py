#!/usr/bin/env python3
"""review_trades.py — journal statistics for the learning loop (SPEC section 5).

Computes over closed trades: win rate, avg/total PnL, current streak, longest
losing streak, per-symbol breakdown, per-regime breakdown, and lesson tags
(auto-tagged heuristics like repeated stop-outs on one symbol).

Module:  from review_trades import review
CLI:     python3 review_trades.py config.json [--hours 24] [--json]
         python3 review_trades.py --trades trades.json --json
"""

import argparse
import calendar
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import journal_trade  # noqa: E402

STREAK_LESSON_THRESHOLD = 3
SYMBOL_LOSS_INFO_USD = -100.0  # informational flag below this cumulative PnL


def _parse_ts(ts):
    if not ts:
        return 0.0
    try:
        return calendar.timegm(time.strptime(ts, "%Y-%m-%dT%H:%M:%SZ"))
    except (ValueError, TypeError):
        return 0.0


def review(entries, since_ts=0.0):
    closed = [e for e in entries
              if e.get("status") == "closed" and e.get("realised_pnl") is not None
              and _parse_ts(e.get("closed_at")) >= since_ts]
    wins = [e for e in closed if e.get("outcome") == "win"]
    losses = [e for e in closed if e.get("outcome") == "loss"]
    pnls = [float(e["realised_pnl"]) for e in closed]

    streak, streak_kind = 0, None
    for e in reversed(closed):
        kind = e.get("outcome")
        if kind not in ("win", "loss"):
            continue
        if streak_kind is None:
            streak_kind = kind
        if kind == streak_kind:
            streak += 1
        else:
            break

    longest_losing, run = 0, 0
    for e in closed:
        run = run + 1 if e.get("outcome") == "loss" else 0
        longest_losing = max(longest_losing, run)

    per_symbol = {}
    for e in closed:
        sym = e.get("symbol")
        bucket = per_symbol.setdefault(sym, {"trades": 0, "wins": 0, "pnl": 0.0})
        bucket["trades"] += 1
        bucket["wins"] += 1 if e.get("outcome") == "win" else 0
        bucket["pnl"] += float(e["realised_pnl"])
    for bucket in per_symbol.values():
        bucket["win_rate"] = round(bucket["wins"] / bucket["trades"], 4) if bucket["trades"] else 0.0
        bucket["pnl"] = round(bucket["pnl"], 6)

    per_regime = {}
    for e in closed:
        regime = e.get("regime") or "unknown"
        bucket = per_regime.setdefault(regime, {"trades": 0, "wins": 0, "pnl": 0.0})
        bucket["trades"] += 1
        bucket["wins"] += 1 if e.get("outcome") == "win" else 0
        bucket["pnl"] += float(e["realised_pnl"])

    lesson_tags = []
    for sym, bucket in per_symbol.items():
        if bucket["pnl"] <= SYMBOL_LOSS_INFO_USD:
            lesson_tags.append("symbol %s cumulatively losing ($%.2f) — informational" % (sym, bucket["pnl"]))
        sym_losses = [e for e in closed
                      if e.get("symbol") == sym and e.get("close_reason") in ("stop_loss", "trailing_stop")]
        if bucket["trades"] >= 3 and len(sym_losses) / bucket["trades"] >= 0.8:
            lesson_tags.append("symbol %s repeatedly stopped out (%d/%d)" % (sym, len(sym_losses), bucket["trades"]))
    if streak_kind == "loss" and streak >= STREAK_LESSON_THRESHOLD:
        lesson_tags.append("losing streak of %d — defensive metrics apply" % streak)
    for regime, bucket in per_regime.items():
        if bucket["trades"] >= 4 and bucket["pnl"] < 0:
            lesson_tags.append("regime %s net negative over %d trades" % (regime, bucket["trades"]))

    return {
        "closed_trades": len(closed),
        "wins": len(wins),
        "losses": len(losses),
        "breakeven": len(closed) - len(wins) - len(losses),
        "win_rate": round(len(wins) / len(closed), 4) if closed else 0.0,
        "avg_pnl": round(sum(pnls) / len(pnls), 6) if pnls else 0.0,
        "total_pnl": round(sum(pnls), 6),
        "current_streak": {"kind": streak_kind, "count": streak},
        "longest_losing_streak": longest_losing,
        "per_symbol": per_symbol,
        "per_regime": per_regime,
        "lesson_tags": lesson_tags,
        "generated_at": journal_trade.utcnow(),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Trade journal review / stats")
    parser.add_argument("config", nargs="?", help="path to config.json")
    parser.add_argument("--trades", default=None, help="trades.json path")
    parser.add_argument("--hours", type=float, default=None,
                        help="only trades closed within the last N hours")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args(argv)

    trades_path = args.trades
    if trades_path is None:
        if not args.config:
            parser.error("config path or --trades required")
        trades_path = os.path.join(os.path.dirname(os.path.abspath(args.config)), "trades.json")
    entries = journal_trade.load_journal(trades_path) if os.path.exists(trades_path) else []
    since = time.time() - args.hours * 3600 if args.hours else 0.0
    result = review(entries, since_ts=since)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("swarmArena review — %s" % result["generated_at"])
        print("closed: %d  wins: %d  losses: %d  breakeven: %d  win rate: %.1f%%"
              % (result["closed_trades"], result["wins"], result["losses"],
                 result["breakeven"], result["win_rate"] * 100))
        print("total PnL: $%.2f  avg: $%.2f  streak: %s x%d  worst losing streak: %d"
              % (result["total_pnl"], result["avg_pnl"],
                 result["current_streak"]["kind"] or "-",
                 result["current_streak"]["count"], result["longest_losing_streak"]))
        for sym, b in sorted(result["per_symbol"].items()):
            print("  %-5s trades=%d win=%.0f%% pnl=$%.2f"
                  % (sym, b["trades"], b["win_rate"] * 100, b["pnl"]))
        for tag in result["lesson_tags"]:
            print("  lesson: %s" % tag)
    return 0


if __name__ == "__main__":
    sys.exit(main())
