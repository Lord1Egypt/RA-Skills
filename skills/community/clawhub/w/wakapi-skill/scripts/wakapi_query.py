#!/usr/bin/env python3
"""
Wakapi coding-stats CLI (stdlib only).

Env: WAKAPI_URL (required), WAKAPI_API_KEY (required for authenticated subcommands).
Health uses Wakapi native GET /api/health (no API key).
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

_RUNTIME: dict[str, Any] = {
    "debug": False,
    "prog": "wakapi_query",
}

_WAKAPI_HEALTH_PATH = "/api/health"


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
        prog = _RUNTIME.get("prog", "wakapi_query")
        print(f"{prog}: {method} {url}", file=sys.stderr)


def _normalize_base(url: str) -> str:
    u = url.strip().rstrip("/")
    if not u:
        raise SystemExit(
            "WAKAPI_URL is required for the Wakapi skill. "
            "Example: export WAKAPI_URL=https://wakapi.example.com"
        )
    return u


def _base_url_from_env() -> str:
    return os.environ.get("WAKAPI_URL", "").strip()


def _api_path_prefix() -> str:
    return "/api/compat/wakatime/v1"


def _api_root() -> str:
    base = _normalize_base(_base_url_from_env())
    return base + _api_path_prefix()


def _statusbar_today_url() -> str:
    base = _normalize_base(_base_url_from_env())
    return f"{base}/api/v1/users/current/statusbar/today"


def _wakapi_health_url() -> str:
    base = _normalize_base(_base_url_from_env())
    return base + _WAKAPI_HEALTH_PATH


def _auth_basic_value(api_key: str) -> str:
    if not api_key:
        raise SystemExit("WAKAPI_API_KEY is empty")
    b64 = base64.b64encode(api_key.encode("utf-8")).decode("ascii")
    return f"Basic {b64}"


def _request_headers() -> dict[str, str]:
    key = os.environ.get("WAKAPI_API_KEY", "")
    if not key:
        raise SystemExit("WAKAPI_API_KEY is empty")
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


def _parse_wakapi_health_body(body: str) -> tuple[bool, str | None]:
    """
    Wakapi /api/health returns JSON if request has Content-Type: application/json,
    else plain text 'app=1\\ndb=0|1'. See muety/wakapi routes/api/health.go.
    """
    text = body.strip()
    if not text:
        return False, "empty body"
    if text.startswith("{"):
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            return False, "invalid JSON"
        app = data.get("app")
        db = data.get("db")
        if app == 1 and db == 1:
            return True, None
        return False, f"app={app!r} db={db!r}"
    # plain text
    db_val: int | None = None
    app_val: int | None = None
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("db="):
            try:
                db_val = int(line.split("=", 1)[1].strip())
            except ValueError:
                pass
        if line.startswith("app="):
            try:
                app_val = int(line.split("=", 1)[1].strip())
            except ValueError:
                pass
    if app_val == 1 and db_val == 1:
        return True, None
    return False, f"app={app_val!r} db={db_val!r}"


def cmd_health(*, timeout: float) -> None:
    """GET {WAKAPI_URL}/api/health — Wakapi native health (DB ping); no API key."""
    url = _wakapi_health_url()
    _log_request("GET", url)
    # Wakapi returns JSON when request Content-Type is application/json (see health.go).
    hdr = {"Content-Type": "application/json", "Accept": "application/json"}
    req = urllib.request.Request(url, method="GET", headers=hdr)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            code = resp.getcode()
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        try:
            e.read()
        except OSError:
            pass
        print(json.dumps({"healthy": False}))
        raise SystemExit(1) from e
    except urllib.error.URLError:
        print(json.dumps({"healthy": False}))
        raise SystemExit(1)

    if code != 200:
        print(json.dumps({"healthy": False}))
        raise SystemExit(1)

    ok, detail = _parse_wakapi_health_body(raw)
    out: dict[str, Any] = {"healthy": ok}
    if detail and not ok:
        out["detail"] = detail
    print(json.dumps(out))
    raise SystemExit(0 if ok else 1)


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
        "Wakapi coding stats (compat /api/compat/wakatime/v1) — read-only API. "
        "Env: WAKAPI_URL (required), WAKAPI_API_KEY (required except health uses /api/health). "
        "Auth: HTTP Basic with API key only."
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
        help='Wakapi GET /api/health; prints {"healthy": true|false} (and optional detail)',
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
        help=(
            "Wakapi named interval only, e.g. last_7_days, last_30_days, last_6_months, last_year, "
            "today, yesterday, week, month, year, all_time — not YYYY or YYYY-MM (use summaries --start/--end)"
        ),
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
            "  --range RANGE     Preset → query param range= (Wakapi interval aliases, e.g. today, last_7_days, "
            '"Last 7 Days").\n'
            "  --start + --end   Fixed dates YYYY-MM-DD (use both).\n"
            "Optional filters (either mode): --project, --branches, --timezone, --timeout, --writes-only.\n"
            "Intervals: https://github.com/muety/wakapi/blob/master/models/interval.go"
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
            "Preset for range= (e.g. today, last_7_days, or Title Case from Wakapi). "
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
        # Needs origin only; WAKAPI_API_KEY not required.
        _normalize_base(_base_url_from_env())
        cmd_health(
            timeout=_resolve_http_timeout(cli_sec=http_cli, fallback_sec=15),
        )
    elif args.command == "projects":
        cmd_projects(_api_root(), _request_headers(), http_timeout=http_cli)
    elif args.command == "status-bar":
        cmd_status_bar_today(_request_headers(), http_timeout=http_cli)
    elif args.command == "all-time-since":
        cmd_all_time_since_today(_api_root(), _request_headers(), http_timeout=http_cli)
    elif args.command == "stats":
        cmd_stats(_api_root(), _request_headers(), args)
    elif args.command == "summaries":
        cmd_summaries(_api_root(), _request_headers(), args)
    else:
        parser.error(f"unknown command {args.command!r}")


if __name__ == "__main__":  # pragma: no cover
    main()
