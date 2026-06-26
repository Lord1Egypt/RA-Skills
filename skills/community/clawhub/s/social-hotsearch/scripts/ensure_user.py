#!/usr/bin/env python3
"""Ensure the user is registered with the proxy. Print user_id and remaining quota.

Usage:
    python3 ensure_user.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from social_client import ensure_user, get_usage, ProxyError


def main() -> int:
    try:
        u = ensure_user()
    except ProxyError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2

    user_id = u["user_id"]
    try:
        usage = get_usage(user_id)
    except ProxyError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2

    print(json.dumps({
        "user_id": user_id,
        "is_new": u.get("is_new", False),
        "used": usage["used"],
        "remaining": usage["remaining"],
        "limit": usage["limit"],
        "should_bind_email": usage["should_bind_email"],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
