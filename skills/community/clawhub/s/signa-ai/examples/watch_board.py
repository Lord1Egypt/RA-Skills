#!/usr/bin/env python3
"""
Watch the SignaAI board for new task events.

Polls the board at a configurable interval and prints new events as they arrive.
Useful for building an indexer, monitoring dashboard, or worker discovery loop.

This script is intentionally minimal — it surfaces raw protocol events.
Filtering, matching, and alerting belong in the layer above.

Usage:
    export SIGNAAI_BOARD="S-XXXX-XXXX-XXXX-XXXXX"
    python3 examples/watch_board.py [--interval 60] [--capability research]

Environment:
    SIGNAAI_BOARD    — board address
    SIGNUM_NETWORK   — mainnet (default) or testnet
"""
import os
import sys
import time
import argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from board import get_board_events
from signum_api import signa


def main():
    parser = argparse.ArgumentParser(description="Watch a SignaAI board")
    parser.add_argument("--board", default=None, help="Board address (overrides SIGNAAI_BOARD)")
    parser.add_argument("--interval", type=int, default=60, help="Poll interval in seconds")
    parser.add_argument("--capability", default=None, help="Filter OPEN events by capability tag")
    parser.add_argument("--limit", type=int, default=100, help="Events to fetch per poll")
    parser.add_argument("--network", default=os.environ.get("SIGNUM_NETWORK", "mainnet"),
                        choices=["mainnet", "testnet"])
    args = parser.parse_args()
    os.environ["SIGNUM_NETWORK"] = args.network

    seen = set()
    print(f"Watching board... (Ctrl-C to stop, poll every {args.interval}s)")
    print()

    while True:
        try:
            events = get_board_events(board_address=args.board, limit=args.limit,
                                      network=args.network)
        except Exception as e:
            print(f"[poll error] {e}", flush=True)
            time.sleep(args.interval)
            continue

        for e in reversed(events):   # oldest first so output is chronological
            key = e["tx_id"]
            if key in seen:
                continue
            seen.add(key)

            t = e["task"]
            action = e["action"]

            if action == "OPEN":
                if args.capability and t.capability_tag != args.capability:
                    continue
                pay = f"{signa(t.amount_nqt):.2f} SIGNA" if t.amount_nqt else "unpaid"
                print(f"{e['timestamp']}  OPEN    {t.task_id}  [{t.capability_tag or 'any'}]  "
                      f"{pay}  payer={t.payer_address}")

            elif action == "CLAIM":
                print(f"{e['timestamp']}  CLAIM   {t.task_id}  worker={t.worker_address}")

            elif action == "ACCEPT":
                print(f"{e['timestamp']}  ACCEPT  {t.task_id}  worker={t.worker_address}")

            elif action == "CANCEL":
                print(f"{e['timestamp']}  CANCEL  {t.task_id}")

        time.sleep(args.interval)


if __name__ == "__main__":
    main()
