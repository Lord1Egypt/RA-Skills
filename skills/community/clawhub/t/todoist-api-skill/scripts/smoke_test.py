#!/usr/bin/env python3
"""
Read-only smoke test for the Todoist API skill.

This verifies:
- token discovery
- basic authenticated access
- one paginated read endpoint
- helper exit codes

Usage:
  python3 scripts/smoke_test.py
  python3 scripts/smoke_test.py --token "$TODOIST_API_TOKEN"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://api.todoist.com/api/v1"
USER_AGENT = "todoist-api-skill-smoke/2.0.0"


def emit(data: dict) -> None:
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only smoke test for the Todoist API skill.")
    parser.add_argument("--token", help="Todoist API token. Defaults to TODOIST_API_TOKEN.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"API base URL (default: {DEFAULT_BASE_URL})")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout in seconds (default: 20).")
    args = parser.parse_args(argv)

    token = args.token or os.getenv("TODOIST_API_TOKEN") or os.getenv("TODOIST_TOKEN")
    if not token:
        emit({"ok": False, "error": "Missing Todoist token. Pass --token or set TODOIST_API_TOKEN."})
        return 2

    url = args.base_url.rstrip("/") + "/projects?" + urllib.parse.urlencode({"limit": 1})
    request = urllib.request.Request(
        url=url,
        method="GET",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            payload = json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        try:
            payload = json.loads(exc.read().decode("utf-8", errors="replace"))
        except Exception:
            payload = {"error": f"HTTP {exc.code}"}
        emit({"ok": False, "status": exc.code, "details": payload})
        return 3 if exc.code in {401, 403} else 5
    except urllib.error.URLError as exc:
        emit({"ok": False, "error": f"Network error: {exc.reason}"})
        return 6

    results = payload.get("results", []) if isinstance(payload, dict) else []
    emit(
        {
            "ok": True,
            "checked": {
                "auth": True,
                "projects_endpoint": True,
                "paginated_shape": isinstance(payload, dict) and "results" in payload and "next_cursor" in payload,
            },
            "sample_project_count": len(results),
            "next_cursor": payload.get("next_cursor") if isinstance(payload, dict) else None,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
