#!/usr/bin/env python3
"""
Dreaming v2 — Budget Meter

Tracks daily extraction costs against a $2/day hard cap.
Estimates cost from input size (conservative: $0.003 per 1K input tokens + $0.015 per 1K output tokens).

Usage:
  python3 budget.py --check                     # Check if today's budget allows extraction
  python3 budget.py --log --facts-count 5       # Log a completed extraction
  python3 budget.py --status                    # Show budget status
  python3 budget.py --reset                     # Reset today's budget (emergency only)
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace")))
BUDGET_FILE = WORKSPACE / "memory" / ".dreams" / "extraction-budget.json"
DAILY_CAP = 2.00  # USD

# Sonnet 4.6 pricing (conservative estimates via OpenRouter)
COST_PER_1K_INPUT = 0.003
COST_PER_1K_OUTPUT = 0.015
# Rough estimate: extraction produces ~100 output tokens per fact, plus ~500 overhead
EST_OUTPUT_TOKENS_PER_FACT = 100
EST_OUTPUT_OVERHEAD = 500


def load_budget() -> dict:
    if BUDGET_FILE.exists():
        try:
            return json.loads(BUDGET_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"version": 1, "days": {}}


def save_budget(data: dict):
    BUDGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    BUDGET_FILE.write_text(json.dumps(data, indent=2))


def today_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def get_today_spend(data: dict) -> float:
    day = data.get("days", {}).get(today_key(), {})
    return day.get("total_cost_usd", 0.0)


def estimate_cost(input_chars: int, facts_count: int) -> float:
    input_tokens = input_chars / 4  # rough char-to-token ratio
    output_tokens = facts_count * EST_OUTPUT_TOKENS_PER_FACT + EST_OUTPUT_OVERHEAD
    cost = (input_tokens / 1000 * COST_PER_1K_INPUT) + (output_tokens / 1000 * COST_PER_1K_OUTPUT)
    return round(cost, 4)


def cmd_check(data: dict):
    spent = get_today_spend(data)
    remaining = DAILY_CAP - spent
    if remaining <= 0:
        print(f"BUDGET EXCEEDED — spent ${spent:.2f} / ${DAILY_CAP:.2f} today")
        sys.exit(1)
    print(f"OK — ${remaining:.2f} remaining (spent ${spent:.2f} / ${DAILY_CAP:.2f})")
    sys.exit(0)


def cmd_log(data: dict, facts_count: int):
    key = today_key()
    # Estimate cost from the extraction input file
    input_dir = WORKSPACE / "memory" / ".dreams" / "extraction-input"
    input_file = input_dir / f"{key}.txt"

    input_chars = 0
    if input_file.exists():
        input_chars = len(input_file.read_text())
    # If no file for today, check yesterday (extraction runs at 03:00 for previous day)
    else:
        from datetime import timedelta
        yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).strftime("%Y-%m-%d")
        yesterday_file = input_dir / f"{yesterday}.txt"
        if yesterday_file.exists():
            input_chars = len(yesterday_file.read_text())

    cost = estimate_cost(input_chars, facts_count)

    if "days" not in data:
        data["days"] = {}
    if key not in data["days"]:
        data["days"][key] = {"runs": [], "total_cost_usd": 0.0}

    data["days"][key]["runs"].append({
        "timestamp": datetime.now(timezone.utc).isoformat()[:19] + "Z",
        "facts_extracted": facts_count,
        "input_chars": input_chars,
        "estimated_cost_usd": cost,
    })
    data["days"][key]["total_cost_usd"] = round(
        sum(r["estimated_cost_usd"] for r in data["days"][key]["runs"]), 4
    )

    save_budget(data)
    spent = data["days"][key]["total_cost_usd"]
    print(f"Logged: {facts_count} facts, ~${cost:.4f} estimated cost")
    print(f"Today total: ${spent:.4f} / ${DAILY_CAP:.2f}")

    # Prune entries older than 60 days
    cutoff = (datetime.now(timezone.utc) - __import__("datetime").timedelta(days=60)).strftime("%Y-%m-%d")
    data["days"] = {k: v for k, v in data["days"].items() if k >= cutoff}
    save_budget(data)


def cmd_status(data: dict):
    key = today_key()
    spent = get_today_spend(data)
    remaining = DAILY_CAP - spent

    # Last 7 days
    days = sorted(data.get("days", {}).items(), reverse=True)[:7]
    print(f"Budget status — {key}")
    print(f"  Today: ${spent:.4f} / ${DAILY_CAP:.2f} (${remaining:.4f} remaining)")
    print(f"  Last 7 days:")
    total_week = 0
    total_facts = 0
    for d, info in days:
        day_cost = info.get("total_cost_usd", 0)
        day_facts = sum(r.get("facts_extracted", 0) for r in info.get("runs", []))
        total_week += day_cost
        total_facts += day_facts
        print(f"    {d}: ${day_cost:.4f} ({day_facts} facts)")
    print(f"  Week total: ${total_week:.4f} ({total_facts} facts)")


def cmd_reset(data: dict):
    key = today_key()
    if key in data.get("days", {}):
        del data["days"][key]
        save_budget(data)
    print(f"Reset budget for {key}")


def main():
    parser = argparse.ArgumentParser(description="Dreaming v2 budget meter")
    parser.add_argument("--check", action="store_true", help="Check if budget allows extraction")
    parser.add_argument("--log", action="store_true", help="Log a completed extraction")
    parser.add_argument("--status", action="store_true", help="Show budget status")
    parser.add_argument("--reset", action="store_true", help="Reset today's budget")
    parser.add_argument("--facts-count", type=int, default=0, help="Number of facts extracted (for --log)")
    args = parser.parse_args()

    data = load_budget()

    if args.check:
        cmd_check(data)
    elif args.log:
        cmd_log(data, args.facts_count)
    elif args.status:
        cmd_status(data)
    elif args.reset:
        cmd_reset(data)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
