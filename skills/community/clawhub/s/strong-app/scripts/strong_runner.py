#!/usr/bin/env python3
# SECURITY MANIFEST:
# Environment variables accessed: STRONG_USERNAME, STRONG_PASSWORD (only)
# External endpoints called: https://back.strong.app (only)
# Local files read: none
# Local files written: none
"""
Strong v6 API CLI dispatcher for the OpenClaw skill.

Usage:
    python3 strong_runner.py <command> [--param value ...]

Environment variables:
    STRONG_USERNAME  (required)
    STRONG_PASSWORD  (required)
"""

import argparse
from datetime import datetime, timezone
import json
import os
import sys
import urllib.request
import urllib.error


STRONG_BASE = "https://back.strong.app"

COMMON_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "okhttp/4.12.0",
    "X-Client-Platform": "android",
    "X-Client-Build": "1118",
}


def _output(data):
    """Print result as JSON to stdout."""
    print(json.dumps(data, indent=2, default=str))


def _request(method, path, headers=None, body=None):
    """Send an HTTP request and return parsed JSON."""
    url = f"{STRONG_BASE}{path}"
    all_headers = dict(COMMON_HEADERS)
    if headers:
        all_headers.update(headers)
    data = json.dumps(body).encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=all_headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(error_body)
        except json.JSONDecodeError:
            detail = error_body
        print(
            json.dumps({"error": f"HTTP {exc.code}", "detail": detail}),
            file=sys.stderr,
        )
        sys.exit(1)


def _login():
    """Authenticate and return (access_token, refresh_token, user_id)."""
    username = os.environ.get("STRONG_USERNAME")
    password = os.environ.get("STRONG_PASSWORD")
    if not username or not password:
        print(
            json.dumps(
                {"error": "STRONG_USERNAME and STRONG_PASSWORD must be set."}
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    resp = _request("POST", "/auth/login", body={
        "login": username,
        "password": password,
        "usernameOrEmail": username,
    })
    return resp["accessToken"], resp["refreshToken"], resp["userId"]


def _auth_headers(token):
    """Return Authorization header dict."""
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

def cmd_login(_args):
    access_token, refresh_token, user_id = _login()
    _output({
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "userId": user_id,
    })


def cmd_refresh_token(args):
    access_token, refresh_token, _user_id = _login()
    resp = _request(
        "POST",
        "/auth/login/refresh",
        headers=_auth_headers(access_token),
        body={
            "accessToken": access_token,
            "refreshToken": refresh_token,
        },
    )
    _output(resp)


def cmd_get_profile(_args):
    token, _, user_id = _login()
    resp = _request("GET", f"/api/users/{user_id}", headers=_auth_headers(token))
    _output(resp)


def cmd_list_exercises(_args):
    token, _, user_id = _login()
    resp = _request(
        "GET", f"/api/users/{user_id}/measurements", headers=_auth_headers(token)
    )
    _output(resp)


def cmd_get_exercise(args):
    token, _, user_id = _login()
    resp = _request(
        "GET",
        f"/api/users/{user_id}/measurements/{args.measurement_id}",
        headers=_auth_headers(token),
    )
    _output(resp)


def cmd_list_templates(_args):
    token, _, user_id = _login()
    resp = _request(
        "GET", f"/api/users/{user_id}/templates", headers=_auth_headers(token)
    )
    _output(resp)


def cmd_get_template(args):
    token, _, user_id = _login()
    resp = _request(
        "GET",
        f"/api/users/{user_id}/templates/{args.template_id}",
        headers=_auth_headers(token),
    )
    _output(resp)


def cmd_list_logs(_args):
    token, _, user_id = _login()
    resp = _request(
        "GET", f"/api/users/{user_id}/logs", headers=_auth_headers(token)
    )
    _output(resp)


def cmd_get_log(args):
    token, _, user_id = _login()
    path = f"/api/users/{user_id}/logs/{args.log_id}"
    if args.include_measurement:
        path += "?include=measurement"
    resp = _request("GET", path, headers=_auth_headers(token))
    _output(resp)


def cmd_list_folders(_args):
    token, _, user_id = _login()
    resp = _request(
        "GET", f"/api/users/{user_id}/folders", headers=_auth_headers(token)
    )
    _output(resp)


def cmd_list_tags(_args):
    token, _, user_id = _login()
    resp = _request(
        "GET", f"/api/users/{user_id}/tags", headers=_auth_headers(token)
    )
    _output(resp)


def cmd_list_widgets(_args):
    token, _, user_id = _login()
    resp = _request(
        "GET", f"/api/users/{user_id}/widgets", headers=_auth_headers(token)
    )
    _output(resp)


def cmd_share_template(args):
    token, _, user_id = _login()
    resp = _request(
        "POST",
        f"/api/users/{user_id}/templates/{args.template_id}/link",
        headers=_auth_headers(token),
    )
    _output(resp)


def cmd_share_log(args):
    token, _, user_id = _login()
    resp = _request(
        "POST",
        f"/api/users/{user_id}/logs/{args.log_id}/link",
        headers=_auth_headers(token),
    )
    _output(resp)


def cmd_get_shared_link(args):
    token, _, _ = _login()
    resp = _request(
        "GET",
        f"/api/links/{args.link_id}",
        headers=_auth_headers(token),
    )
    _output(resp)


# ---------------------------------------------------------------------------
# Helpers for augmented (client-side) commands
# ---------------------------------------------------------------------------

def _parse_date(value):
    """Parse a date string into a timezone-aware datetime.

    Accepts ISO-8601 timestamps or plain YYYY-MM-DD dates.
    """
    for fmt in ("%Y-%m-%dT%H:%M:%S.%f%z", "%Y-%m-%dT%H:%M:%S%z",
                 "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S",
                 "%Y-%m-%d"):
        try:
            dt = datetime.strptime(value, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue
    raise ValueError(f"Unable to parse date: {value}")


def _fetch_all_logs():
    """Login, fetch all logs, and return the list."""
    token, _, user_id = _login()
    resp = _request(
        "GET", f"/api/users/{user_id}/logs", headers=_auth_headers(token)
    )
    return token, user_id, resp.get("_embedded", {}).get("log", [])


# ---------------------------------------------------------------------------
# Augmented command handlers (client-side filtering)
# ---------------------------------------------------------------------------

def cmd_get_log_at_date(args):
    """Return logs whose startDate falls on the given date."""
    target = _parse_date(args.date)
    _, _, logs = _fetch_all_logs()
    matched = []
    for log in logs:
        start = log.get("startDate")
        if not start:
            continue
        log_dt = _parse_date(start)
        if log_dt.date() == target.date():
            matched.append(log)
    _output({"_embedded": {"log": matched}, "total": len(matched)})


def cmd_get_logs_in_range(args):
    """Return logs whose startDate is between --from and --to (inclusive)."""
    dt_from = _parse_date(args.date_from)
    dt_to = _parse_date(args.date_to)
    _, _, logs = _fetch_all_logs()
    matched = []
    for log in logs:
        start = log.get("startDate")
        if not start:
            continue
        log_dt = _parse_date(start)
        if dt_from <= log_dt <= dt_to:
            matched.append(log)
    matched.sort(key=lambda l: l.get("startDate", ""))
    _output({"_embedded": {"log": matched}, "total": len(matched)})


def cmd_get_latest_log(_args):
    """Return the most recent workout log by startDate."""
    _, _, logs = _fetch_all_logs()
    if not logs:
        _output({"_embedded": {"log": []}, "total": 0})
        return
    latest = max(logs, key=lambda l: l.get("startDate", ""))
    _output(latest)


def cmd_search_logs_by_name(args):
    """Return logs whose name contains the search string (case-insensitive)."""
    needle = args.name.lower()
    _, _, logs = _fetch_all_logs()
    matched = [
        log for log in logs
        if needle in (log.get("name", {}).get("custom", "") or "").lower()
    ]
    _output({"_embedded": {"log": matched}, "total": len(matched)})


def cmd_search_exercises_by_name(args):
    """Return exercises whose name contains the search string (case-insensitive)."""
    needle = args.name.lower()
    token, _, user_id = _login()
    resp = _request(
        "GET", f"/api/users/{user_id}/measurements", headers=_auth_headers(token)
    )
    exercises = resp.get("_embedded", {}).get("measurement", [])
    matched = [
        ex for ex in exercises
        if needle in (ex.get("name", {}).get("custom", "") or "").lower()
    ]
    _output({"_embedded": {"measurement": matched}, "total": len(matched)})


def cmd_get_exercise_history(args):
    """Return all logs containing a specific exercise (measurement ID)."""
    mid = args.measurement_id
    token, _, user_id = _login()
    resp = _request(
        "GET", f"/api/users/{user_id}/logs", headers=_auth_headers(token)
    )
    logs = resp.get("_embedded", {}).get("log", [])
    matched = []
    for log in logs:
        groups = log.get("_embedded", {}).get("cellSetGroup", [])
        for group in groups:
            cells = group.get("cellSets", [])
            embedded_cells = group.get("_embedded", {}).get("cellSet", [])
            all_cells = cells + embedded_cells
            for cell in all_cells:
                if cell.get("measurementId") == mid:
                    matched.append(log)
                    break
            else:
                continue
            break
    matched.sort(key=lambda l: l.get("startDate", ""))
    _output({"_embedded": {"log": matched}, "total": len(matched)})


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Strong v6 API CLI dispatcher for the OpenClaw skill."
    )
    subs = parser.add_subparsers(dest="command", required=True)

    # --- Auth ---
    subs.add_parser("login", help="Authenticate and obtain tokens")
    subs.add_parser("refresh_token", help="Refresh an expired access token")

    # --- Profile ---
    subs.add_parser("get_profile", help="Fetch the authenticated user's profile")

    # --- Exercises (measurements) ---
    subs.add_parser("list_exercises", help="List all exercises in the user's library")

    p = subs.add_parser("get_exercise", help="Get a single exercise by ID")
    p.add_argument("--measurement_id", required=True, help="Exercise/measurement UUID")

    # --- Templates ---
    subs.add_parser("list_templates", help="List all workout templates")

    p = subs.add_parser("get_template", help="Get a single workout template")
    p.add_argument("--template_id", required=True, help="Template UUID")

    # --- Logs ---
    subs.add_parser("list_logs", help="List all completed workout logs")

    p = subs.add_parser("get_log", help="Get a single workout log")
    p.add_argument("--log_id", required=True, help="Log UUID")
    p.add_argument(
        "--include_measurement",
        action="store_true",
        default=False,
        help="Include exercise/measurement data in the response",
    )

    # --- Folders ---
    subs.add_parser("list_folders", help="List workout template folders")

    # --- Tags ---
    subs.add_parser("list_tags", help="List exercise tags/categories")

    # --- Widgets ---
    subs.add_parser("list_widgets", help="List dashboard widgets")

    # --- Sharing ---
    p = subs.add_parser("share_template", help="Generate a shareable template link")
    p.add_argument("--template_id", required=True, help="Template UUID")

    p = subs.add_parser("share_log", help="Generate a shareable log link")
    p.add_argument("--log_id", required=True, help="Log UUID")

    p = subs.add_parser("get_shared_link", help="Retrieve a shared link by ID")
    p.add_argument("--link_id", required=True, help="Shared link ID")

    # --- Augmented (client-side filtering) ---
    p = subs.add_parser(
        "get_log_at_date",
        help="Get workout logs whose startDate falls on a given date",
    )
    p.add_argument(
        "--date", required=True,
        help="Target date (YYYY-MM-DD or ISO-8601 timestamp)",
    )

    p = subs.add_parser(
        "get_logs_in_range",
        help="Get workout logs between two dates (inclusive)",
    )
    p.add_argument(
        "--from", required=True, dest="date_from",
        help="Start date (YYYY-MM-DD or ISO-8601)",
    )
    p.add_argument(
        "--to", required=True, dest="date_to",
        help="End date (YYYY-MM-DD or ISO-8601)",
    )

    subs.add_parser(
        "get_latest_log",
        help="Get the most recent workout log by startDate",
    )

    p = subs.add_parser(
        "search_logs_by_name",
        help="Search workout logs by name (case-insensitive substring match)",
    )
    p.add_argument(
        "--name", required=True,
        help="Substring to match against log names",
    )

    p = subs.add_parser(
        "search_exercises_by_name",
        help="Search exercises by name (case-insensitive substring match)",
    )
    p.add_argument(
        "--name", required=True,
        help="Substring to match against exercise names",
    )

    p = subs.add_parser(
        "get_exercise_history",
        help="Get all workout logs containing a specific exercise",
    )
    p.add_argument(
        "--measurement_id", required=True,
        help="Exercise/measurement UUID to search for in logs",
    )

    return parser


# ---------------------------------------------------------------------------
# Dispatch table
# ---------------------------------------------------------------------------

COMMANDS = {
    "login": cmd_login,
    "refresh_token": cmd_refresh_token,
    "get_profile": cmd_get_profile,
    "list_exercises": cmd_list_exercises,
    "get_exercise": cmd_get_exercise,
    "list_templates": cmd_list_templates,
    "get_template": cmd_get_template,
    "list_logs": cmd_list_logs,
    "get_log": cmd_get_log,
    "list_folders": cmd_list_folders,
    "list_tags": cmd_list_tags,
    "list_widgets": cmd_list_widgets,
    "share_template": cmd_share_template,
    "share_log": cmd_share_log,
    "get_shared_link": cmd_get_shared_link,
    "get_log_at_date": cmd_get_log_at_date,
    "get_logs_in_range": cmd_get_logs_in_range,
    "get_latest_log": cmd_get_latest_log,
    "search_logs_by_name": cmd_search_logs_by_name,
    "search_exercises_by_name": cmd_search_exercises_by_name,
    "get_exercise_history": cmd_get_exercise_history,
}


def main():
    parser = build_parser()
    args = parser.parse_args()

    handler = COMMANDS.get(args.command)
    if handler is None:
        print(
            json.dumps({"error": f"Unknown command: {args.command}"}),
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        handler(args)
    except Exception as exc:
        print(
            json.dumps({"error": str(exc), "type": type(exc).__name__}),
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
