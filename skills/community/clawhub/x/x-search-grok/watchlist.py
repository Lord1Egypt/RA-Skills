#!/usr/bin/env python3
"""
watchlist.py — Run x_search.py for all items in your watchlist config.

Usage:
  python3 watchlist.py --time 24h --lang zh --output ~/obsidian/X/
  python3 watchlist.py --count 10 --lang en --only accounts
  python3 watchlist.py --config ~/my-watchlist.yaml --time 48h

Config file (default: ~/.x-search.yaml):
  accounts:
    - "@karpathy"
    - "@elonmusk"
  trends:
    - "#AI"
    - "#LLM"
  topics:
    - "Claude MCP"
    - "crude oil price"
"""

import os
import sys
import argparse
import subprocess

try:
    import yaml
except ImportError:
    print("Error: 'pyyaml' not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

DEFAULT_CONFIG = os.path.expanduser("~/.x-search.yaml")
SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "x_search.py")

SAMPLE_CONFIG = """\
# ~/.x-search.yaml — x-search watchlist
#
# NOTE: all accounts share the same execution parameters (--time / --count / --lang).
# For per-account customization, call x_search.py directly:
#   python3 x_search.py account @user --time 48h --lang en

accounts:
  - "@karpathy"
  - "@elonmusk"

trends:
  - "#AI"
  - "#LLM"

topics:
  - "Claude MCP"
  - "crude oil price"
"""


def load_config(path: str) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        print(f"Config not found: {path}", file=sys.stderr)
        print(f"\nCreate it with:\n\n{SAMPLE_CONFIG}", file=sys.stderr)
        sys.exit(1)


def build_base_args(args) -> list[str]:
    base = ["python3", SCRIPT, "--lang", args.lang]
    if args.output:
        base += ["--output", args.output]
    if args.progress_only:
        base += ["--progress-only"]
    return base


def run(cmd: list[str]) -> None:
    print(f"\n→ {' '.join(cmd)}", file=sys.stderr)
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"  ✗ exited with code {result.returncode}", file=sys.stderr)


def _run_section(config: dict, base: list[str], key: str, subcmd: str, items_fn=None) -> None:
    """Run x_search.py for each item in a config section."""
    items = config.get(key, [])
    if not items:
        return
    print(f"\n[{key}] {len(items)} item(s)", file=sys.stderr)
    for item in items:
        cmd = items_fn(base, item) if items_fn else base + [subcmd, str(item)]
        run(cmd)


def run_accounts(config: dict, base: list[str], args) -> None:
    def build_cmd(base, item):
        handle = str(item).lstrip("@")
        cmd = base + ["account", f"@{handle}"]
        if args.time:      cmd += ["--time", args.time]
        if args.count:     cmd += ["--count", str(args.count)]
        if args.post_type: cmd += ["--type", args.post_type]
        return cmd

    _run_section(config, base, "accounts", "account", items_fn=build_cmd)


def run_trends(config: dict, base: list[str]) -> None:
    _run_section(config, base, "trends", "trends")


def run_topics(config: dict, base: list[str]) -> None:
    _run_section(config, base, "topics", "topic")


def main():
    parser = argparse.ArgumentParser(
        description="Run x_search.py for all items in your watchlist.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--config", "-c", default=DEFAULT_CONFIG, metavar="PATH",
                        help=f"Watchlist config file (default: {DEFAULT_CONFIG})")
    parser.add_argument("--only", choices=["accounts", "trends", "topics"],
                        help="Run only one section")
    parser.add_argument("--lang", "-l", default="zh", metavar="LANG",
                        help="Output language (default: zh)")
    parser.add_argument("--output", "-o", default=None, metavar="PATH",
                        help="Output directory or file path")
    parser.add_argument("--time", "-t", default=None, metavar="RANGE",
                        help="Time range for account mode: 24h, 48h, 7d, etc.")
    parser.add_argument("--count", "-n", type=int, default=None, metavar="N",
                        help="Post count for account mode")
    parser.add_argument("--type", dest="post_type", default=None,
                        choices=["post", "reply", "all"],
                        help="Post type filter for account mode")
    parser.add_argument("--progress-only", action="store_true",
                        help="Pass --progress-only to x_search.py (one-line stdout per account)")
    args = parser.parse_args()

    config = load_config(args.config)
    base = build_base_args(args)
    selected = {args.only} if args.only else {"accounts", "trends", "topics"}

    if "accounts" in selected:
        run_accounts(config, base, args)
    if "trends" in selected:
        run_trends(config, base)
    if "topics" in selected:
        run_topics(config, base)


if __name__ == "__main__":
    main()
