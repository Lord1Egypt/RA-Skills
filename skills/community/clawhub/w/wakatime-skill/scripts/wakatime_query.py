#!/usr/bin/env python3
"""
WakaTime official (SaaS) API CLI — stdlib only.

API host is fixed to https://wakatime.com (see https://wakatime.com).

Env: WAKATIME_API_KEY (required).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

# Official WakaTime API — no env override; see https://wakatime.com
WAKATIME_ORIGIN = "https://wakatime.com"

_RUNTIME: dict[str, Any] = {
    "debug": False,
    "prog": "wakatime_query",
}


def _resolve_http_timeout(*, cli_sec: float | None, fallback_sec: float) -> float:
    if cli_sec is not None:
        return cli_sec
    return fallback_sec


def _debug_enabled() -> bool:
    return bool(_RUNTIME.get("debug"))


def _strip_debug_argv(argv: list[str]) -> tuple[bool, list[str]]:
    debug = False
    rest: list[str] = []
    for a in argv:
        if a in ("-d", "--debug"):
            debug = True
        else:
            rest.append(a)
    return debug, rest


def _log_request(method: str, url: str) -> None:
    if _debug_enabled():
        prog = _RUNTIME.get("prog", "wakatime_query")
        print(f"{prog}: {method} {url}", file=sys.stderr)


def _api_root() -> str:
    return f"{WAKATIME_ORIGIN}/api/v1"


def _statusbar_today_url() -> str:
    return f"{WAKATIME_ORIGIN}/api/v1/users/current/statusbar/today"


def _auth_basic_value(api_key: str) -> str:
    if not api_key:
        raise SystemExit("WAKATIME_API_KEY is empty")
    b64 = base64.b64encode(api_key.encode("utf-8")).decode("ascii")
    return f"Basic {b64}"


def _request_headers() -> dict[str, str]:
    key = os.environ.get("WAKATIME_API_KEY", "")
    if not key:
        raise SystemExit("WAKATIME_API_KEY is empty")
    return {"Authorization": _auth_basic_value(key), "Accept": "application/json"}


def _get_json(
    url: str,
    headers: dict[str, str],
    *,
    timeout: float | None = None,
) -> tuple[int, Any]:
    t = _resolve_http_timeout(cli_sec=timeout, fallback_sec=60)
    _log_request("GET", url)
    req = urllib.request.Request(url, method="GET", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=t) as resp:
            body = resp.read().decode("utf-8")
            code = resp.getcode()
            if not body:
                return code, None
            try:
                return code, json.loads(body)
            except json.JSONDecodeError as e:
                snippet = body[:200].replace("\n", " ")
                print(
                    f"Expected JSON in response body (HTTP {code}), parse error: {e}; "
                    f"body starts with: {snippet!r}",
                    file=sys.stderr,
                )
                raise SystemExit(1) from e
    except urllib.error.HTTPError as e:
        try:
            payload = e.read().decode("utf-8")
            data = json.loads(payload) if payload else None
        except json.JSONDecodeError:
            data = payload
        print(json.dumps({"http_status": e.code, "error": data}, indent=2), file=sys.stderr)
        raise SystemExit(1) from e
    except urllib.error.URLError as e:
        print(str(e.reason if hasattr(e, "reason") else e), file=sys.stderr)
        raise SystemExit(2) from e


def cmd_health(api_root: str, hdr: dict[str, str], *, timeout: float) -> None:
    """Connectivity via GET .../users/current/projects (WakaTime has no separate public health)."""
    url = f"{api_root}/users/current/projects"
    _log_request("GET", url)
    req = urllib.request.Request(url, method="GET", headers=hdr)
    code: int | None = None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = resp.getcode()
            resp.read()
    except urllib.error.HTTPError as e:
        try:
            try:
                e.read()
            except OSError:
                pass
        finally:
            try:
                e.close()
            except OSError:
                pass
        print(json.dumps({"healthy": False}))
        raise SystemExit(1) from e
    except urllib.error.URLError:
        print(json.dumps({"healthy": False}))
        raise SystemExit(1)

    healthy = code == 200
    print(json.dumps({"healthy": healthy}))
    raise SystemExit(0 if healthy else 1)


def cmd_projects(api_root: str, hdr: dict[str, str], *, http_timeout: float | None) -> None:
    url = f"{api_root}/users/current/projects"
    _code, data = _get_json(url, hdr, timeout=http_timeout)
    print(json.dumps(data, indent=2))


def cmd_status_bar_today(hdr: dict[str, str], *, http_timeout: float | None) -> None:
    url = _statusbar_today_url()
    _code, data = _get_json(url, hdr, timeout=http_timeout)
    print(json.dumps(data, indent=2))


def cmd_all_time_since_today(api_root: str, hdr: dict[str, str], *, http_timeout: float | None) -> None:
    url = f"{api_root}/users/current/all_time_since_today"
    _code, data = _get_json(url, hdr, timeout=http_timeout)
    print(json.dumps(data, indent=2))


def cmd_stats(api_root: str, hdr: dict[str, str], args: argparse.Namespace) -> None:
    range_seg = urllib.parse.quote(args.stats_range, safe="")
    q: list[tuple[str, str]] = []
    if args.timeout is not None:
        q.append(("timeout", str(args.timeout)))
    if args.writes_only is not None:
        q.append(("writes_only", args.writes_only))
    qs = urllib.parse.urlencode(q) if q else ""
    url = f"{api_root}/users/current/stats/{range_seg}"
    if qs:
        url = f"{url}?{qs}"
    _code, data = _get_json(url, hdr)
    print(json.dumps(data, indent=2))


def cmd_summaries(api_root: str, hdr: dict[str, str], args: argparse.Namespace) -> None:
    params: dict[str, str] = {}

    if args.start and args.end:
        params["start"] = args.start
        params["end"] = args.end
    elif args.range_preset:
        params["range"] = args.range_preset
    else:
        raise SystemExit("summaries: provide --start and --end, or --range")

    if args.project:
        params["project"] = args.project
    if args.branches:
        params["branches"] = args.branches
    if args.timezone:
        params["timezone"] = args.timezone
    if args.timeout is not None:
        params["timeout"] = str(args.timeout)
    if args.writes_only is not None:
        params["writes_only"] = args.writes_only

    qs = urllib.parse.urlencode(params)
    url = f"{api_root}/users/current/summaries"
    if qs:
        url = f"{url}?{qs}"
    _code, data = _get_json(url, hdr)
    print(json.dumps(data, indent=2))


def _add_http_timeout_arg(p: argparse.ArgumentParser, *, fallback: float) -> None:
    p.add_argument(
        "--timeout",
        type=float,
        default=None,
        metavar="SEC",
        dest="http_timeout",
        help=f"HTTP socket timeout seconds (default: {fallback:g})",
    )


def main() -> None:
    dbg, argv_cmd = _strip_debug_argv(sys.argv[1:])

    desc = (
        "WakaTime official API — read-only stats. Host is fixed to https://wakatime.com. "
        "Env: WAKATIME_API_KEY (required). Auth: HTTP Basic with API key only."
    )

    parser = argparse.ArgumentParser(
        prog=_RUNTIME["prog"],
        description=desc,
        epilog="Debug: use -d or --debug anywhere (before or after the subcommand) to print each request URL to stderr.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_health = sub.add_parser(
        "health",
        help='Connectivity check; prints {"healthy": true|false}',
    )
    _add_http_timeout_arg(p_health, fallback=15)

    p_projects = sub.add_parser("projects", help="List projects")
    _add_http_timeout_arg(p_projects, fallback=60)

    p_sbt = sub.add_parser("status-bar", help="Today status bar")
    _add_http_timeout_arg(p_sbt, fallback=60)

    p_all = sub.add_parser("all-time-since", help="All-time total since today")
    _add_http_timeout_arg(p_all, fallback=60)

    p_stats = sub.add_parser("stats", help="Stats for a time range")
    p_stats.add_argument(
        "stats_range",
        metavar="range",
        help="e.g. last_7_days, 2025, 2025-03, all_time",
    )
    p_stats.add_argument(
        "--timeout",
        type=int,
        default=None,
        metavar="N",
        help="API query: keystroke timeout (seconds); not HTTP socket timeout",
    )
    p_stats.add_argument(
        "--writes-only",
        choices=("true", "false"),
        default=None,
        help="writes_only query param",
    )

    p_sum = sub.add_parser(
        "summaries",
        help="Daily summaries for a date range or preset",
        description=(
            "Time window (pick one):\n"
            "  --range RANGE     Preset → query param range= (Title Case or snake_case, e.g. last_7_days).\n"
            "  --start + --end   Fixed dates YYYY-MM-DD (use both).\n"
            "Optional filters (either mode): --project, --branches, --timezone, --timeout, --writes-only.\n"
            "See WakaTime Summaries API: https://wakatime.com/developers#summaries"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p_sum.add_argument("--start", help="Start date (YYYY-MM-DD); use with --end")
    p_sum.add_argument("--end", help="End date (YYYY-MM-DD); use with --start")
    p_sum.add_argument(
        "--range",
        dest="range_preset",
        metavar="RANGE",
        help=(
            'Preset for range= query param (e.g. "Last 7 Days" or last_7_days). '
            "Mutually exclusive with --start/--end. "
            "May combine with --project, --branches, --timezone, --timeout, --writes-only."
        ),
    )
    p_sum.add_argument("--project", metavar="NAME", help="Filter by project name (query: project)")
    p_sum.add_argument(
        "--branches",
        metavar="NAMES",
        help="Comma-separated branch names (query: branches)",
    )
    p_sum.add_argument(
        "--timezone",
        metavar="TZ",
        help="IANA timezone for dates (query: timezone)",
    )
    p_sum.add_argument(
        "--timeout",
        type=int,
        default=None,
        metavar="N",
        help="API query: keystroke timeout in seconds (not HTTP socket; HTTP stays 60s)",
    )
    p_sum.add_argument(
        "--writes-only",
        choices=("true", "false"),
        default=None,
        help="API query: writes_only=true|false",
    )

    args = parser.parse_args(argv_cmd)

    _RUNTIME["debug"] = dbg

    api_root = _api_root()
    h = _request_headers()

    if args.command == "summaries":
        has_dates = bool(args.start or args.end)
        if bool(args.start) ^ bool(args.end):
            parser.error("summaries: --start and --end must be used together")
        if has_dates and args.range_preset:
            parser.error("summaries: do not combine --range with --start/--end")
        if not has_dates and not args.range_preset:
            parser.error("summaries: need --start and --end, or --range")

    http_cli = getattr(args, "http_timeout", None)

    if args.command == "health":
        cmd_health(
            api_root,
            h,
            timeout=_resolve_http_timeout(cli_sec=http_cli, fallback_sec=15),
        )
    elif args.command == "projects":
        cmd_projects(api_root, h, http_timeout=http_cli)
    elif args.command == "status-bar":
        cmd_status_bar_today(h, http_timeout=http_cli)
    elif args.command == "all-time-since":
        cmd_all_time_since_today(api_root, h, http_timeout=http_cli)
    elif args.command == "stats":
        cmd_stats(api_root, h, args)
    elif args.command == "summaries":
        cmd_summaries(api_root, h, args)
    else:
        parser.error(f"unknown command {args.command!r}")


if __name__ == "__main__":  # pragma: no cover
    main()
