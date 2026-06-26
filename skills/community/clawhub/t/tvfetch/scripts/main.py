#!/usr/bin/env python3
"""
Unified CLI entry point for tvfetch skill.

Dispatches to the appropriate scripts/lib/ module based on subcommand.
This replaces the old cli/main.py with a skill-aware entry point.

Usage:
  python main.py fetch BINANCE:BTCUSDT 1D 365
  python main.py stream BINANCE:BTCUSDT --duration 10
  python main.py search bitcoin --type crypto
  python main.py analyze NASDAQ:AAPL 1D 252
  python main.py compare BTC ETH --timeframe 1D --bars 30
  python main.py indicators BTC 1D 100 --indicators "sma:20,rsi:14,macd"
  python main.py cache stats
  python main.py auth show
"""

from __future__ import annotations

import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_DIR))

COMMANDS = {
    "fetch": "scripts.lib.fetch",
    "fetch-multi": "scripts.lib.fetch_multi",
    "stream": "scripts.lib.stream",
    "search": "scripts.lib.search",
    "analyze": "scripts.lib.analyze",
    "compare": "scripts.lib.compare",
    "indicators": "scripts.lib.indicators",
    "cache": "scripts.lib.cache_mgr",
    "auth": "scripts.lib.auth_mgr",
}


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("tvfetch skill — unified CLI")
        print()
        print("Commands:")
        for cmd in COMMANDS:
            print(f"  {cmd}")
        print()
        print("Usage: python main.py <command> [args...]")
        print("Run 'python main.py <command> --help' for command-specific help.")
        return 0

    command = sys.argv[1]
    if command not in COMMANDS:
        print(f"Unknown command: {command}", file=sys.stderr)
        print(f"Available: {', '.join(COMMANDS)}", file=sys.stderr)
        return 1

    # Remove the command name from argv so the module's argparse works correctly
    sys.argv = [sys.argv[0]] + sys.argv[2:]

    # Import and run the module's main()
    import importlib
    module = importlib.import_module(COMMANDS[command])
    return module.main()


if __name__ == "__main__":
    sys.exit(main())
