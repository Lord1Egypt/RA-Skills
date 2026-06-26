#!/usr/bin/env python3
"""Read-only Traefik API helper."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


DEFAULT_BASE_URL = "http://localhost:8080"

ENDPOINTS = {
    "version": "/api/version",
    "overview": "/api/overview",
    "entrypoints": "/api/entrypoints",
    "routers": "/api/http/routers",
    "services": "/api/http/services",
    "middlewares": "/api/http/middlewares",
    "tcp-routers": "/api/tcp/routers",
    "tcp-services": "/api/tcp/services",
    "udp-routers": "/api/udp/routers",
    "udp-services": "/api/udp/services",
    "rawdata": "/api/rawdata",
    "support-dump": "/api/support-dump",
}


def build_url(base_url: str, endpoint: str) -> str:
    path = ENDPOINTS.get(endpoint, endpoint)
    if not path.startswith("/"):
        path = f"/{path}"
    return urllib.parse.urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))


def fetch(url: str, timeout: float) -> tuple[str, bytes]:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        content_type = response.headers.get("content-type", "")
        return content_type, response.read()


def main() -> int:
    parser = argparse.ArgumentParser(description="Query Traefik's read-only API")
    parser.add_argument(
        "endpoint",
        nargs="?",
        default="overview",
        help=f"Endpoint alias or path. Aliases: {', '.join(sorted(ENDPOINTS))}",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("TRAEFIK_BASE_URL", DEFAULT_BASE_URL),
        help=f"Traefik API base URL (default: {DEFAULT_BASE_URL}, env: TRAEFIK_BASE_URL)",
    )
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--compact", action="store_true", help="Do not pretty-print JSON")
    args = parser.parse_args()

    url = build_url(args.base_url, args.endpoint)
    try:
        content_type, body = fetch(url, args.timeout)
    except urllib.error.HTTPError as exc:
        print(f"HTTP {exc.code} from {url}: {exc.reason}", file=sys.stderr)
        detail = exc.read().decode("utf-8", errors="replace").strip()
        if detail:
            print(detail, file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"Cannot reach {url}: {exc.reason}", file=sys.stderr)
        return 1
    except TimeoutError:
        print(f"Timed out reaching {url}", file=sys.stderr)
        return 1

    if "json" not in content_type.lower():
        sys.stdout.buffer.write(body)
        return 0

    data = json.loads(body)
    if args.compact:
        print(json.dumps(data, separators=(",", ":")))
    else:
        print(json.dumps(data, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
