#!/usr/bin/env python3
"""Check Twitter login status via twitter-cli.

Usage:
    python whoami.py --json
"""
from __future__ import annotations

import argparse
import sys

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])
from common import print_result, run_twitter_cli


def main() -> None:
    parser = argparse.ArgumentParser(description="Check Twitter login status")
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output result as JSON",
    )
    _ = parser.parse_args()

    result = run_twitter_cli(["whoami"], json_output=True)

    if result.get("ok"):
        data = result.get("data", {})
        user = data.get("user", {})
        print_result({
            "ok": True,
            "data": {
                "logged_in": True,
                "username": user.get("screenName") or user.get("username", ""),
                "name": user.get("name", ""),
                "user_id": user.get("id", ""),
            },
        })
    else:
        # Check error code to distinguish NOT_INSTALLED vs NOT_LOGGED_IN
        error = result.get("error", {})
        code = error.get("code", "UNKNOWN")
        print_result({
            "ok": True,
            "data": {
                "logged_in": False,
                "reason": code,
                "message": error.get("message", "未知错误"),
            },
        })


if __name__ == "__main__":
    main()
