#!/usr/bin/env python3
"""Small wrapper for Wolfram|Alpha LLM API.

- Endpoint: https://www.wolframalpha.com/api/v1/llm-api
- Auth: Bearer token by default (`Authorization: Bearer <AppID>`). Use `--auth query` to send `appid` as a URL parameter.

Env:
  - WOLFRAM_APP_ID: Wolfram|Alpha AppID

Examples:
  python3 wa_llm.py --input "10 densest elemental metals" --maxchars 800
  python3 wa_llm.py --input "convert 70 F to C" --units metric
"""

from __future__ import annotations

import argparse
import os
import sys
import urllib.parse
import urllib.request
from typing import List, Tuple, Optional

import hashlib
import json
import time
from pathlib import Path


BASE_URL = "https://www.wolframalpha.com/api/v1/llm-api"


def build_url(params: List[Tuple[str, str]]) -> str:
    query = urllib.parse.urlencode(params, doseq=True)
    return f"{BASE_URL}?{query}"


def http_get(url: str, timeout_s: float, authorization: Optional[str] = None) -> Tuple[int, str]:
    req = urllib.request.Request(url, method="GET")
    if authorization:
        req.add_header("Authorization", authorization)
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            status = getattr(resp, "status", 200)
            body = resp.read().decode("utf-8", errors="replace")
            return status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else str(e)
        return e.code, body


def main() -> int:
    p = argparse.ArgumentParser(description="Query Wolfram|Alpha LLM API")
    p.add_argument("--input", required=True, help="Natural language / keyword query (single line recommended)")
    p.add_argument("--maxchars", type=int, default=2500, help="Max chars of response (default: 2500; WA default is ~6800)")

    # Disambiguation
    p.add_argument("--assumption", action="append", default=[], help="Assumption value (repeatable)")

    # Context / localization
    p.add_argument("--units", default=None, help="Units system or units preference")
    p.add_argument("--currency", default=None, help="Currency code (e.g., USD, EUR)")
    p.add_argument("--countrycode", default=None, help="Country code")
    p.add_argument("--languagecode", default=None, help="Language code")
    p.add_argument("--timezone", default=None, help="Timezone")

    loc = p.add_mutually_exclusive_group()
    loc.add_argument("--ip", default=None, help="Location as IP address")
    loc.add_argument("--latlong", default=None, help="Location as 'lat,long'")
    loc.add_argument("--location", default=None, help="Location as semantic string (e.g., 'Boston, MA')")

    # Timeouts (WA-side, not client-side). Values are passed through as-is.
    p.add_argument("--scantimeout", default=None)
    p.add_argument("--parsetimeout", default=None)
    p.add_argument("--formattimeout", default=None)
    p.add_argument("--totaltimeout", default=None)

    # Client behavior
    p.add_argument("--http-timeout", type=float, default=30.0, help="HTTP timeout seconds (client-side)")

    # Auth mode
    p.add_argument(
        "--auth",
        choices=["query", "bearer"],
        default="bearer",
        help="Auth mode: send AppID as query param (query) or as Authorization: Bearer (bearer)",
    )

    # Cache
    p.add_argument(
        "--cache",
        choices=["off", "on"],
        default="on",
        help="Enable a small local cache to save WA quota for repeated requests",
    )
    p.add_argument(
        "--cache-ttl",
        type=int,
        default=604800,
        help="Cache TTL seconds (default 604800 = 7d)",
    )

    args = p.parse_args()

    appid = os.environ.get("WOLFRAM_APP_ID")
    if not appid:
        print("ERROR: WOLFRAM_APP_ID env var is not set.", file=sys.stderr)
        return 2

    params: List[Tuple[str, str]] = [("input", args.input)]

    if args.maxchars is not None:
        params.append(("maxchars", str(args.maxchars)))

    for a in args.assumption or []:
        params.append(("assumption", a))

    passthrough = [
        ("units", args.units),
        ("currency", args.currency),
        ("countrycode", args.countrycode),
        ("languagecode", args.languagecode),
        ("timezone", args.timezone),
        ("ip", args.ip),
        ("latlong", args.latlong),
        ("location", args.location),
        ("scantimeout", args.scantimeout),
        ("parsetimeout", args.parsetimeout),
        ("formattimeout", args.formattimeout),
        ("totaltimeout", args.totaltimeout),
    ]
    for k, v in passthrough:
        if v is not None and str(v) != "":
            params.append((k, str(v)))

    # Auth
    authorization: Optional[str] = None
    if args.auth == "query":
        params.insert(0, ("appid", appid))
    else:
        authorization = f"Bearer {appid}"

    url = build_url(params)

    # Cache key should include full URL + auth mode (but not the secret itself).
    cache_enabled = args.cache == "on"
    # Prefer a stable, explicit cache path (avoid surprising XDG overrides).
    cache_dir = Path.home() / ".cache" / "openclaw-wolfram-alpha"
    cache_key_material = json.dumps({"url": url, "auth": args.auth}, sort_keys=True).encode("utf-8")
    cache_key = hashlib.sha256(cache_key_material).hexdigest()
    cache_path = cache_dir / f"{cache_key}.json"

    if cache_enabled:
        try:
            if cache_path.exists():
                data = json.loads(cache_path.read_text(encoding="utf-8"))
                age = time.time() - float(data.get("ts", 0))
                if age <= int(args.cache_ttl):
                    sys.stdout.write(str(data.get("body", "")))
                    return int(data.get("exit_code", 0))
        except Exception:
            # Cache is best-effort; ignore failures.
            pass

    status, body = http_get(url, timeout_s=float(args.http_timeout), authorization=authorization)

    # Print body to stdout so callers can pipe/consume it.
    sys.stdout.write(body)

    # Non-2xx => signal failure for scripting.
    exit_code = 0
    if status >= 400:
        print(f"\n\n[wa_llm] HTTP {status} for URL: {url}", file=sys.stderr)
        exit_code = 1

    if cache_enabled:
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
            payload = {"ts": time.time(), "status": status, "body": body, "exit_code": exit_code}
            cache_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
