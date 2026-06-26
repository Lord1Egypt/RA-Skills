#!/usr/bin/env python3
"""
Strategy backtest — CLI stub for backtest / optimize / report flows.

Usage:
    python3 strategy_backtest_tool.py backtest [args]
    python3 strategy_backtest_tool.py optimize [args]
    python3 strategy_backtest_tool.py report [args]
"""

import json
import os
import sys
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DATA_FILE = os.path.join(DATA_DIR, "strategy_backtest_data.json")
LEGACY_DATA_FILE = os.path.join(DATA_DIR, "quant_backtest_data.json")

REF_URLS = [
    "https://www.backtrader.com/docu/",
    "https://github.com/mementum/backtrader",
    "https://news.ycombinator.com/item?id=39462946",
]


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    if os.path.exists(LEGACY_DATA_FILE):
        with open(LEGACY_DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["tool"] = "strategy-backtest"
        save_data(data)
        return data
    return {"records": [], "created": datetime.now().isoformat(), "tool": "strategy-backtest"}


def save_data(data):
    ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def backtest(args):
    """Run a strategy backtest."""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "backtest",
        "input": " ".join(args) if args else "",
        "status": "completed",
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "backtest",
        "message": "Backtest step completed",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:3],
    }


def optimize(args):
    """Optimize strategy parameters."""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "optimize",
        "input": " ".join(args) if args else "",
        "status": "completed",
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "optimize",
        "message": "Optimization step completed",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:3],
    }


def report(args):
    """Generate a backtest report."""
    data = load_data()
    record = {
        "timestamp": datetime.now().isoformat(),
        "command": "report",
        "input": " ".join(args) if args else "",
        "status": "completed",
    }
    data["records"].append(record)
    save_data(data)
    return {
        "status": "success",
        "command": "report",
        "message": "Report step completed",
        "record": record,
        "total_records": len(data["records"]),
        "reference_urls": REF_URLS[:3],
    }


def main():
    cmds = ["backtest", "optimize", "report"]
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(
            json.dumps(
                {
                    "error": f"Usage: strategy_backtest_tool.py <{','.join(cmds)}> [args]",
                    "available_commands": {c: "" for c in cmds},
                    "tool": "strategy-backtest",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "backtest":
        result = backtest(args)
    elif cmd == "optimize":
        result = optimize(args)
    elif cmd == "report":
        result = report(args)
    else:
        result = {"error": f"Unknown command: {cmd}"}

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
