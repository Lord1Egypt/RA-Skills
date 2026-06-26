#!/usr/bin/env python3
"""
Thin AWAL CLI wrapper for x402-layer agents.

This wrapper keeps x402-layer Python-first workflows while allowing agents to
use Coinbase Agentic Wallet (AWAL) commands without embedding secrets.
"""

import argparse
import sys
from typing import List, Tuple
from urllib.parse import urlparse

from awal_bridge import run_awal

def _run_awal(args: List[str]) -> int:
    result = run_awal(args)
    if result["stdout"]:
        print(result["stdout"], end="")
    if result["stderr"]:
        print(result["stderr"], end="", file=sys.stderr)
    return int(result["code"])


def _split_url(url: str) -> Tuple[str, str]:
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError("URL must include scheme and host (e.g. https://api.x402layer.cc/e/gifu)")
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"
    return base_url, path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Coinbase AWAL commands from x402-layer skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python awal_cli.py run status
  python awal_cli.py run auth login agent@example.com
  python awal_cli.py run auth verify <flow_id> <otp>
  python awal_cli.py run balance
  python awal_cli.py run bazaar list

  # Convenience helpers for full URLs (AWAL v1 pay/discover expects base + path)
  python awal_cli.py pay-url https://api.x402layer.cc/e/gifu
  python awal_cli.py discover-url https://api.x402layer.cc/e/gifu?action=purchase

Notes:
  - Wrapper uses AWAL_BIN first, then local `awal` binary in PATH.
  - If `awal` is missing, install Coinbase AWAL skill:
      npx skills add coinbase/agentic-wallet-skills
""",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Pass AWAL args directly (recommended)")
    run_parser.add_argument("awal_args", nargs=argparse.REMAINDER, help="Raw AWAL arguments")

    pay_parser = sub.add_parser("pay-url", help="Pay an x402 endpoint from a full URL")
    pay_parser.add_argument("url", help="Full endpoint URL")
    pay_parser.add_argument("extra_args", nargs=argparse.REMAINDER, help="Additional AWAL pay args")

    discover_parser = sub.add_parser(
        "discover-url",
        help="Discover x402 requirements from a full URL",
    )
    discover_parser.add_argument("url", help="Full endpoint URL")
    discover_parser.add_argument(
        "extra_args",
        nargs=argparse.REMAINDER,
        help="Additional AWAL discover args",
    )

    args = parser.parse_args()

    if args.command == "run":
        raw = list(args.awal_args)
        if raw and raw[0] == "--":
            raw = raw[1:]
        if not raw:
            parser.error("run requires at least one AWAL argument, e.g.: run status")
        return _run_awal(raw)

    try:
        base_url, path = _split_url(args.url)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    extra = list(getattr(args, "extra_args", []))
    if extra and extra[0] == "--":
        extra = extra[1:]

    if args.command == "pay-url":
        return _run_awal(["pay", base_url, path, *extra])

    return _run_awal(["discover", base_url, path, *extra])


if __name__ == "__main__":
    raise SystemExit(main())
