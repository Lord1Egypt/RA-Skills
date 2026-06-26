#!/usr/bin/env python3
"""Get trending topics on X (Twitter) using the X API."""

import json
import os
import re
import signal
import sys
from urllib.request import Request, HTTPRedirectHandler, build_opener
from urllib.error import URLError, HTTPError


class _NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise HTTPError(newurl, code, f"Redirect to {newurl} blocked (auth safety)", headers, fp)


API_BASE = "https://api.x.com/2"
TIMEOUT_S = 30
MAX_TRENDS_MIN = 1
MAX_TRENDS_MAX = 50
MAX_TRENDS_DEFAULT = 20
WOEID_RE = re.compile(r"^\d+$")
FLAGS_WITH_VALUES = {"--woeid", "--max"}


def die(msg: str) -> None:
    print(f"Error: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_args(argv: list[str]) -> dict:
    args = argv[1:]
    options: dict = {
        "woeid": None,
        "max_trends": None,
    }

    if not args or args[0] in ("-h", "--help"):
        print(
            "Usage: python3 trends.py --woeid <WOEID> [--max <1-50>]",
            file=sys.stderr,
        )
        sys.exit(0 if args else 1)

    # Expand --flag=value into --flag value
    expanded: list[str] = []
    for a in args:
        if "=" in a and a.split("=", 1)[0] in FLAGS_WITH_VALUES:
            expanded.extend(a.split("=", 1))
        else:
            expanded.append(a)

    i = 0
    while i < len(expanded):
        arg = expanded[i]

        if arg in FLAGS_WITH_VALUES and (i + 1 >= len(expanded) or expanded[i + 1].startswith("--")):
            die(f"{arg} requires a value.")

        if arg == "--woeid":
            i += 1
            options["woeid"] = expanded[i]
        elif arg == "--max":
            i += 1
            options["max_trends"] = expanded[i]
        elif arg.startswith("--"):
            die(f'Unknown flag "{arg}". Use --help for usage.')
        else:
            die(f'Unexpected argument "{arg}". Use --help for usage.')

        i += 1

    return options


def validate(options: dict) -> None:
    woeid = options["woeid"]
    max_trends = options["max_trends"]

    if woeid is None:
        die("--woeid is required.")

    if not WOEID_RE.match(woeid):
        die(f'--woeid must be a numeric value, got "{woeid}".')
    if int(woeid) == 0:
        die("--woeid must be a positive integer.")

    if max_trends is not None:
        if not WOEID_RE.match(max_trends):
            die(f'--max must be a numeric value, got "{max_trends}".')
        val = int(max_trends)
        if val < MAX_TRENDS_MIN or val > MAX_TRENDS_MAX:
            die(f"--max must be between {MAX_TRENDS_MIN} and {MAX_TRENDS_MAX}, got {val}.")


def build_url(options: dict) -> str:
    woeid = options["woeid"]
    url = f"{API_BASE}/trends/by/woeid/{woeid}"
    params = ["trend.fields=trend_name,tweet_count"]
    max_trends = options["max_trends"]
    if max_trends is not None:
        params.append(f"max_trends={max_trends}")
    return url + "?" + "&".join(params)


def _safe_get(obj: object, key: str, default: object = None) -> object:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return default


def format_response(data: dict) -> dict:
    trends_raw = _safe_get(data, "data", [])
    if not isinstance(trends_raw, list):
        trends_raw = []

    errors_raw = _safe_get(data, "errors", [])
    if not isinstance(errors_raw, list):
        errors_raw = []

    trends = []
    for t in trends_raw:
        if not isinstance(t, dict):
            continue
        entry: dict = {}
        name = t.get("trend_name")
        if name:
            entry["trend_name"] = name
        count = t.get("tweet_count")
        if count is not None:
            entry["tweet_count"] = count
        if entry:
            trends.append(entry)

    errors = []
    for e in errors_raw:
        if isinstance(e, dict):
            msg = e.get("detail") or e.get("title") or ""
            if msg:
                errors.append(msg)

    result: dict = {
        "count": len(trends),
        "trends": trends,
    }
    if errors:
        result["errors"] = errors
    return result


def fetch_trends(options: dict) -> None:
    url = build_url(options)

    token = os.environ.get("X_BEARER_TOKEN", "").strip()
    if not token:
        die("X_BEARER_TOKEN environment variable is not set.")

    req = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "User-Agent": "OpenClaw/x-trends",
        },
        method="GET",
    )

    opener = build_opener(_NoRedirect)
    try:
        with opener.open(req, timeout=TIMEOUT_S) as resp:
            data = json.loads(resp.read())
    except HTTPError as e:
        try:
            error_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        except Exception:
            error_body = ""
        die(f"API error ({e.code}): {error_body}")
    except URLError as e:
        die(f"Network request failed: {e.reason}")
    except TimeoutError:
        die(f"Request timed out after {TIMEOUT_S}s.")
    except json.JSONDecodeError:
        die("Failed to parse API response as JSON.")
    except OSError as e:
        die(f"Connection error: {e}")

    output = format_response(data)
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda *_: (print("\nInterrupted.", file=sys.stderr), sys.exit(130)))
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    options = parse_args(sys.argv)
    validate(options)
    fetch_trends(options)
