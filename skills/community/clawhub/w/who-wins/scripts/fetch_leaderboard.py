#!/usr/bin/env python3
"""Fetch PinchBench leaderboard data from pinchbench.com.

Usage:
    python fetch_leaderboard.py [--top N] [--sort metric] [--model filter] [--json]

Options:
    --top N        Show top N models (default: 10)
    --sort metric  Sort by: score, cost, time, runs (default: score)
    --model filter Filter models containing this string (case-insensitive)
    --json         Output raw JSON instead of formatted table
"""

import argparse
import json
import re
import subprocess
import sys


URL = "https://pinchbench.com/"


def fetch_entries():
    result = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "15", URL],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"ERROR: curl failed: {result.stderr.strip()}", file=sys.stderr)
        sys.exit(1)
    html = result.stdout

    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html, re.DOTALL)
    for chunk in chunks:
        chunk = chunk.replace("\\n", "\n").replace('\\"', '"')
        m = re.search(r'"entries":\[(\{.*)', chunk)
        if not m:
            continue
        data = m.group(0)
        depth = 0
        end = 0
        for i, c in enumerate(data):
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        arr_str = data[len('"entries":') : end]
        return json.loads(arr_str)

    print("ERROR: could not parse leaderboard data from pinchbench.com", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Fetch PinchBench leaderboard")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--sort", choices=["score", "cost", "time", "runs"], default="score")
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    entries = fetch_entries()

    if args.model:
        entries = [e for e in entries if args.model.lower() in e["model"].lower()]

    sort_keys = {
        "score": lambda e: -e["percentage"],
        "cost": lambda e: e["average_cost_usd"],
        "time": lambda e: e["average_execution_time_seconds"],
        "runs": lambda e: -e["submission_count"],
    }
    entries.sort(key=sort_keys[args.sort])
    entries = entries[: args.top]

    if args.json:
        json.dump(entries, sys.stdout, indent=2)
        return

    print(f"{'#':>3}  {'Model':<45} {'Score':>6}  {'Cost':>7}  {'Time':>6}  {'Runs':>4}")
    print(f"{'─'*3}  {'─'*45} {'─'*6}  {'─'*7}  {'─'*6}  {'─'*4}")
    for i, e in enumerate(entries, 1):
        print(
            f"{i:>3}  {e['model']:<45} {e['percentage']:>5.1f}%  "
            f"${e['average_cost_usd']:>6.2f}  "
            f"{e['average_execution_time_seconds']:>5.0f}s  "
            f"{e['submission_count']:>4}"
        )


if __name__ == "__main__":
    main()
