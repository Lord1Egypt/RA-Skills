#!/usr/bin/env python3
"""update_metrics.py — bounded learning adaptations to state.metrics.

Applies review output to state.metrics within HARD BOUNDS (SPEC sections 5+7):
  confidence_multiplier      floor 0.70; recovers +0.05/review toward 1.0;
                             drops 0.10 per losing streak >= 3
  effective_leverage_cap     can only drop (losing streak >= 3 -> -1, floor
                             min_leverage); recovers +1 per winning review;
                             NEVER above config.max_leverage
  recommended_min_confidence 0.55 base; +0.05 per losing streak >= 3, cap 0.75;
                             recovers -0.05 toward 0.55 on winning reviews
  underperforming_symbols    informational list (per-symbol pnl <= -$100)
  lessons                    review lesson tags appended (capped at 20 kept)

Learning can NEVER: raise leverage above max_leverage, change to a riskier
mode, remove SL/TP requirements, or suppress journaling.

CLI: python3 update_metrics.py config.json
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import journal_trade   # noqa: E402
from review_trades import review, SYMBOL_LOSS_INFO_USD  # noqa: E402

CONFIDENCE_MULTIPLIER_FLOOR = 0.70
CONFIDENCE_MULTIPLIER_RECOVER = 0.05
CONFIDENCE_MULTIPLIER_DROP = 0.10
MIN_CONFIDENCE_BASE = 0.55
MIN_CONFIDENCE_CAP = 0.75
MIN_CONFIDENCE_STEP = 0.05
STREAK_TRIGGER = 3
MAX_LESSONS_KEPT = 20


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


def update_metrics(config, state, review_result):
    metrics = state.setdefault("metrics", {})
    min_leverage = int(config.get("min_leverage", 2))
    max_leverage = int(config.get("max_leverage", 10))

    metrics.setdefault("confidence_multiplier", 1.0)
    metrics.setdefault("effective_leverage_cap", max_leverage)
    metrics.setdefault("recommended_min_confidence", MIN_CONFIDENCE_BASE)
    metrics.setdefault("leverage_reduction_active", False)
    metrics.setdefault("lessons", [])

    streak = review_result.get("current_streak") or {}
    losing = streak.get("kind") == "loss" and streak.get("count", 0) >= STREAK_TRIGGER
    winning_review = review_result.get("total_pnl", 0) > 0 and not losing

    if losing:
        metrics["confidence_multiplier"] = _clamp(
            metrics["confidence_multiplier"] - CONFIDENCE_MULTIPLIER_DROP,
            CONFIDENCE_MULTIPLIER_FLOOR, 1.0)
        metrics["effective_leverage_cap"] = max(
            min_leverage, int(metrics["effective_leverage_cap"]) - 1)
        metrics["recommended_min_confidence"] = _clamp(
            metrics["recommended_min_confidence"] + MIN_CONFIDENCE_STEP,
            MIN_CONFIDENCE_BASE, MIN_CONFIDENCE_CAP)
        metrics["leverage_reduction_active"] = True
    elif winning_review:
        metrics["confidence_multiplier"] = _clamp(
            metrics["confidence_multiplier"] + CONFIDENCE_MULTIPLIER_RECOVER,
            CONFIDENCE_MULTIPLIER_FLOOR, 1.0)
        metrics["effective_leverage_cap"] = min(
            max_leverage, int(metrics["effective_leverage_cap"]) + 1)
        metrics["recommended_min_confidence"] = _clamp(
            metrics["recommended_min_confidence"] - MIN_CONFIDENCE_STEP,
            MIN_CONFIDENCE_BASE, MIN_CONFIDENCE_CAP)
        if metrics["effective_leverage_cap"] >= max_leverage:
            metrics["leverage_reduction_active"] = False

    # absolute bounds — learning may never exceed them regardless of path
    metrics["confidence_multiplier"] = _clamp(metrics["confidence_multiplier"],
                                              CONFIDENCE_MULTIPLIER_FLOOR, 1.0)
    metrics["effective_leverage_cap"] = _clamp(int(metrics["effective_leverage_cap"]),
                                               min_leverage, max_leverage)
    metrics["recommended_min_confidence"] = _clamp(metrics["recommended_min_confidence"],
                                                   MIN_CONFIDENCE_BASE, MIN_CONFIDENCE_CAP)

    metrics["win_rate"] = review_result.get("win_rate", 0.0)
    metrics["avg_pnl"] = review_result.get("avg_pnl", 0.0)
    metrics["total_pnl"] = review_result.get("total_pnl", 0.0)
    metrics["underperforming_symbols"] = sorted(
        sym for sym, b in (review_result.get("per_symbol") or {}).items()
        if b.get("pnl", 0) <= SYMBOL_LOSS_INFO_USD)

    for tag in review_result.get("lesson_tags") or []:
        stamped = "%s: %s" % (journal_trade.utcnow()[:10], tag)
        if stamped[11:] not in [l[11:] for l in metrics["lessons"] if len(l) > 11]:
            metrics["lessons"].append(stamped)
    metrics["lessons"] = metrics["lessons"][-MAX_LESSONS_KEPT:]
    metrics["trades_since_review"] = 0
    metrics["last_review"] = review_result.get("generated_at")
    return metrics


def main(argv=None):
    parser = argparse.ArgumentParser(description="Apply bounded learning adaptations")
    parser.add_argument("config", help="path to config.json")
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
    entries = journal_trade.load_journal(trades_path) if os.path.exists(trades_path) else []
    result = review(entries)
    metrics = update_metrics(config, state, result)
    tmp = state_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2)
        f.write("\n")
    os.replace(tmp, state_path)
    print(json.dumps({"metrics": metrics, "review": {
        "closed_trades": result["closed_trades"], "win_rate": result["win_rate"],
        "total_pnl": result["total_pnl"],
        "current_streak": result["current_streak"]}}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
