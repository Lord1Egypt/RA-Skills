#!/usr/bin/env python3
"""fetch_trade_outcomes.py — resolve outcomes for journaled open trades.

Live modes: reconciles against the venue (position gone -> derive realized PnL
from account trades, matched against the journaled entry price).
Paper (--paper or mode=paper): marks the position against recorded SL/TP using
the current last price; a touch of either level closes the trade at that level.

This is the review-cron half of the learning loop; position_monitor does the
same job inside the scan cycle. Both share position_monitor.run_position_monitor
so close semantics never diverge.

CLI: python3 fetch_trade_outcomes.py config.json [--paper]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from position_monitor import run_position_monitor  # noqa: E402


def main(argv=None):
    parser = argparse.ArgumentParser(description="Resolve open trade outcomes")
    parser.add_argument("config", help="path to config.json")
    parser.add_argument("--state", default=None)
    parser.add_argument("--trades", default=None)
    parser.add_argument("--paper", action="store_true",
                        help="force paper marking even in a live-mode config")
    args = parser.parse_args(argv)
    with open(args.config) as f:
        config = json.load(f)
    if args.paper:
        config = dict(config, mode="paper")
    base = os.path.dirname(os.path.abspath(args.config))
    state_path = args.state or os.path.join(base, "state.json")
    trades_path = args.trades or os.path.join(base, "trades.json")
    if not os.path.exists(state_path):
        print(json.dumps({"closed": [], "still_open": [], "errors": [],
                          "note": "no state.json yet"}))
        return 0
    import filelock
    with filelock.held(state_path):  # no-op when already held by autonomous_runner
        with open(state_path) as f:
            state = json.load(f)
        result = run_position_monitor(config, state, trades_path)
        tmp = state_path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(state, f, indent=2)
            f.write("\n")
        os.replace(tmp, state_path)
    print(json.dumps(result, indent=2, default=str))
    return 0 if not result["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
