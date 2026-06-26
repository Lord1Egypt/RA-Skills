#!/usr/bin/env python3
"""
Auth token management — skill script wrapper.

Usage:
  python auth_mgr.py show           Show current token status
  python auth_mgr.py set TOKEN      Save token to ~/.tvfetch/.env
  python auth_mgr.py test           Validate token (JWT check, no network)
  python auth_mgr.py instructions   How to get your token
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_SKILL_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_SKILL_DIR))

from scripts.lib.config import (
    get_config,
    validate_token,
    DEFAULT_ENV_PATH,
    DEFAULT_TVFETCH_DIR,
    ANONYMOUS_TOKEN,
    _load_env_file,
)


def cmd_show() -> int:
    """Show current auth configuration."""
    cfg = get_config()
    valid, reason = validate_token(cfg.auth_token)
    preview = cfg.auth_token[:30] + "..." if len(cfg.auth_token) > 30 else cfg.auth_token

    print("=== AUTH STATUS ===")
    print(f"MODE: {'anonymous' if cfg.is_anonymous else 'authenticated'}")
    print(f"SOURCE: {cfg.auth_source}")
    print(f"TOKEN: {preview}")
    print(f"VALID: {valid} ({reason})")
    if not cfg.is_anonymous:
        print(f"ENV_FILE: {DEFAULT_ENV_PATH}")
    print("=== END ===")
    return 0


def cmd_set(token: str) -> int:
    """Save token to ~/.tvfetch/.env"""
    # Validate first
    valid, reason = validate_token(token)
    if not valid:
        print(f"WARNING: Token validation issue: {reason}")
        print("Saving anyway — token may still work if TV accepts it.")

    # Ensure directory exists
    DEFAULT_TVFETCH_DIR.mkdir(parents=True, exist_ok=True)

    # Read existing env file, update or add TV_AUTH_TOKEN
    existing = _load_env_file(DEFAULT_ENV_PATH)
    existing["TV_AUTH_TOKEN"] = token

    lines = [f"{k}={v}" for k, v in existing.items()]
    DEFAULT_ENV_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Token saved to {DEFAULT_ENV_PATH}")
    print(f"Token preview: {token[:30]}...")
    print(f"Validation: {reason}")
    return 0


def cmd_test() -> int:
    """Test token validity."""
    cfg = get_config()
    valid, reason = validate_token(cfg.auth_token)

    print("=== AUTH TEST ===")
    print(f"AUTH_STATUS: {'valid' if valid else 'INVALID'}")
    print(f"AUTH_SOURCE: {cfg.auth_source}")
    print(f"REASON: {reason}")

    if cfg.is_anonymous:
        print("NOTE: Using anonymous mode. Daily/weekly/monthly data gets full history.")
        print("NOTE: Set a token for more intraday bars.")
    elif valid:
        print("NOTE: Token looks valid. Actual bar limits depend on your TradingView subscription.")
    else:
        print("NOTE: Token appears invalid or expired. Try getting a fresh token from your browser.")

    print("=== END ===")
    return 0 if valid else 1


def cmd_instructions() -> int:
    """Print how to get an auth token."""
    print("=== HOW TO GET YOUR TRADINGVIEW AUTH TOKEN ===")
    print()
    print("Option A — Browser Console (recommended):")
    print("  1. Log in to tradingview.com")
    print("  2. Open DevTools (F12) -> Console tab")
    print("  3. Run this command:")
    print("     document.cookie.split('; ').find(c=>c.startsWith('auth_token=')).split('=').slice(1).join('=')")
    print("  4. Copy the long JWT string")
    print()
    print("Option B — WebSocket Traffic:")
    print("  1. Open tradingview.com/chart in browser")
    print("  2. DevTools -> Network -> WS filter")
    print("  3. Click the data.tradingview.com connection")
    print("  4. Find the set_auth_token message -> copy the token")
    print()
    print("Save the token:")
    print(f"  python {__file__} set YOUR_TOKEN_HERE")
    print("  # or")
    print("  export TV_AUTH_TOKEN=YOUR_TOKEN_HERE")
    print()
    print("Bar limits by plan:")
    print("  Anonymous/Free:   ~6,500 bars (1min), ~10,800 (1hr), unlimited (daily+)")
    print("  Essential:        10,000 bars intraday")
    print("  Plus/Premium:     20,000 bars intraday")
    print("  Ultimate:         40,000 bars intraday")
    print("  All plans:        Unlimited daily/weekly/monthly")
    print()
    print("=== END ===")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Auth token management")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("show", help="Show token status")
    set_p = sub.add_parser("set", help="Save token")
    set_p.add_argument("token", help="JWT token string")
    sub.add_parser("test", help="Validate token")
    sub.add_parser("instructions", help="How to get token")
    args = parser.parse_args()

    if args.command == "show":
        return cmd_show()
    elif args.command == "set":
        return cmd_set(args.token)
    elif args.command == "test":
        return cmd_test()
    elif args.command == "instructions":
        return cmd_instructions()
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
