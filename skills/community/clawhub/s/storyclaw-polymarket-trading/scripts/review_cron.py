#!/usr/bin/env python3
"""
Review cron worker — daily strategy review + auto-improvement.

Runs once per day. For each strategy in dry_run or improving state:
  - Computes rolling win rate over last min_sample_size trades
  - If target met → marks pending_live, notifies user
  - If underperforming → auto-adjusts one parameter, notifies user
  - If insufficient data → reports progress estimate

Usage (from cron):
  USER_ID=abc123 python3 /path/to/review_cron.py [strategy_id]
"""

import sys
import os

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

from strategy_manager import (
    get_user_id, list_strategies, load_strategy, cmd_review,
)


def main():
    user_id = get_user_id()
    args = sys.argv[1:]
    target_id = args[0] if args else None

    if target_id:
        cmd_review(user_id, target_id)
    else:
        strategies = list_strategies(user_id)
        active = [s for s in strategies if s["status"] in ("dry_run", "improving")]
        if not active:
            print("📭 No strategies in review-eligible state")
            return
        for strategy in active:
            cmd_review(user_id, strategy["id"])


if __name__ == "__main__":
    main()
