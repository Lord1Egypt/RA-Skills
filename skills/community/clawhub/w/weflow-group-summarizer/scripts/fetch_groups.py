#!/usr/bin/env python3
"""List WeChat group chats from WeFlow sessions API."""

import argparse
import json
import sys
import urllib.request
import urllib.error


def main():
    parser = argparse.ArgumentParser(description="List WeChat group chats")
    parser.add_argument("host", help="WeFlow API host (e.g. http://<windows-ip>:5032)")
    args = parser.parse_args()

    host = args.host.rstrip("/")
    url = f"{host}/api/v1/sessions?limit=1000"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except urllib.error.URLError as e:
        print(f"Connection failed: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    sessions = data.get("sessions", [])
    groups = [s for s in sessions if s.get("username", "").endswith("@chatroom")]

    if not groups:
        print("No group chats found.")
        sys.exit(0)

    for i, g in enumerate(groups, 1):
        name = g.get("displayName", "unknown")
        username = g.get("username", "")
        print(f"{i}. {name} [{username}]")


if __name__ == "__main__":
    main()
