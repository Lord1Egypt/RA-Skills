#!/usr/bin/env python3
"""Test client for Wellness Bridge.

Usage:
  python3 scripts/bridge_test_client.py --url https://<tunnel-host> --token <token> --source apple_health

Sends a minimal payload to /ingest.
No third-party deps.
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from datetime import datetime


def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Tunnel base URL, e.g. https://xxxxx.trycloudflare.com")
    ap.add_argument("--token", required=True)
    ap.add_argument("--source", default="apple_health", choices=["apple_health", "health_connect"])
    ap.add_argument("--date", default=datetime.utcnow().strftime("%Y-%m-%d"))
    ap.add_argument("--tz", default="Asia/Shanghai")
    args = ap.parse_args()

    payload = {
        "date": args.date,
        "source": args.source,
        "timezone": args.tz,
        "generated_at": now_iso(),
        "activity": {"steps": 1234},
    }

    data = json.dumps(payload).encode("utf-8")
    url = args.url.rstrip("/") + "/ingest"

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Bearer {args.token}")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8", errors="replace")
        print(body)


if __name__ == "__main__":
    main()
