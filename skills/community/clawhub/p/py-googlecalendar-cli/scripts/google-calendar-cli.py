#!/usr/bin/env python3
"""
Google Calendar CLI - manage Google Calendar events from the command line.

Authentication uses OAuth2 refresh tokens. Credentials can be provided via
environment variables or command-line arguments.

Required credentials:
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REFRESH_TOKEN

Optional:
    GOOGLE_CALENDAR_ID  (defaults to "primary")
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
CAL_API_BASE = "https://www.googleapis.com/calendar/v3"


# ── Auth ────────────────────────────────────────────────────────────────────

def obtain_access_token(client_id, client_secret, refresh_token):
    """Exchange a refresh token for a short-lived access token."""
    body = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }).encode()
    req = urllib.request.Request(OAUTH_TOKEN_URL, data=body, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        die(f"Token refresh failed ({e.code}): {e.read().decode()}")
    token = data.get("access_token")
    if not token:
        die("No access_token in token response")
    return token


# ── HTTP helpers ────────────────────────────────────────────────────────────

def api_request(method, url, access_token, body=None):
    """Make an authenticated request to the Calendar API."""
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {access_token}")
    req.add_header("Accept", "application/json")
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        die(f"API error ({e.code}): {e.read().decode()}")


def cal_url(calendar_id, *parts):
    """Build a Calendar API URL."""
    base = f"{CAL_API_BASE}/calendars/{urllib.parse.quote(calendar_id)}"
    for p in parts:
        base += f"/{urllib.parse.quote(p)}"
    return base


# ── Subcommands ─────────────────────────────────────────────────────────────

def cmd_list(access_token, calendar_id, args):
    """List upcoming events."""
    params = {
        "maxResults": args.max,
        "singleEvents": "true",
        "orderBy": "startTime",
    }
    if args.time_min:
        params["timeMin"] = args.time_min
    if args.time_max:
        params["timeMax"] = args.time_max
    if args.query:
        params["q"] = args.query

    url = cal_url(calendar_id, "events") + "?" + urllib.parse.urlencode(params)
    data = api_request("GET", url, access_token)
    events = data.get("items", [])

    if args.json:
        print(json.dumps(events, indent=2))
        return

    if not events:
        print("No upcoming events found.")
        return

    for ev in events:
        start = ev.get("start", {}).get("dateTime", ev.get("start", {}).get("date", "?"))
        end = ev.get("end", {}).get("dateTime", ev.get("end", {}).get("date", ""))
        summary = ev.get("summary", "(no title)")
        eid = ev.get("id", "")
        print(f"  {start}  ->  {end}")
        print(f"    {summary}  [id: {eid}]")
        if ev.get("location"):
            print(f"    Location: {ev['location']}")
        print()


def cmd_add(access_token, calendar_id, args):
    """Create a new event."""
    event = {
        "summary": args.title,
        "start": {},
        "end": {},
    }

    # Decide between date (all-day) and dateTime
    if "T" in args.start:
        event["start"]["dateTime"] = args.start
        event["end"]["dateTime"] = args.end
    else:
        event["start"]["date"] = args.start
        event["end"]["date"] = args.end

    if args.description:
        event["description"] = args.description
    if args.location:
        event["location"] = args.location
    if args.attendees:
        event["attendees"] = [
            {"email": e.strip()} for e in args.attendees.split(",") if e.strip()
        ]

    url = cal_url(calendar_id, "events")
    result = api_request("POST", url, access_token, body=event)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Created: {result.get('summary')}  [id: {result.get('id')}]")
        print(f"Link:    {result.get('htmlLink', 'n/a')}")


def cmd_update(access_token, calendar_id, args):
    """Update an existing event."""
    url = cal_url(calendar_id, "events", args.event_id)
    event = api_request("GET", url, access_token)

    if args.title:
        event["summary"] = args.title
    if args.start:
        if "T" in args.start:
            event.setdefault("start", {})["dateTime"] = args.start
        else:
            event.setdefault("start", {})["date"] = args.start
    if args.end:
        if "T" in args.end:
            event.setdefault("end", {})["dateTime"] = args.end
        else:
            event.setdefault("end", {})["date"] = args.end
    if args.description is not None:
        event["description"] = args.description
    if args.location is not None:
        event["location"] = args.location
    if args.attendees:
        event["attendees"] = [
            {"email": e.strip()} for e in args.attendees.split(",") if e.strip()
        ]

    result = api_request("PUT", url, access_token, body=event)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Updated: {result.get('summary')}  [id: {result.get('id')}]")


def cmd_delete(access_token, calendar_id, args):
    """Delete an event."""
    url = cal_url(calendar_id, "events", args.event_id)
    api_request("DELETE", url, access_token)
    if args.json:
        print(json.dumps({"deleted": args.event_id}))
    else:
        print(f"Deleted event: {args.event_id}")


def cmd_today(access_token, calendar_id, args):
    """Show today's events (convenience shortcut)."""
    now = datetime.now().astimezone()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    args.time_min = start_of_day.isoformat()
    args.time_max = end_of_day.isoformat()
    args.max = 50
    args.query = None
    cmd_list(access_token, calendar_id, args)


# ── CLI ─────────────────────────────────────────────────────────────────────

def die(msg):
    sys.stderr.write(f"Error: {msg}\n")
    sys.exit(1)


def resolve_cred(arg_val, env_name, required=True):
    """Return arg_val if set, else env var, else die."""
    val = arg_val or os.getenv(env_name)
    if required and not val:
        die(f"{env_name} not set. Pass --{env_name.lower().replace('_', '-')} or export {env_name}")
    return val


def build_parser():
    parser = argparse.ArgumentParser(
        prog="google-calendar-cli",
        description="Google Calendar CLI -- manage events from the terminal.",
        epilog=(
            "credentials:\n"
            "  Provide credentials via environment variables or flags:\n"
            "    GOOGLE_CLIENT_ID      --client-id\n"
            "    GOOGLE_CLIENT_SECRET   --client-secret\n"
            "    GOOGLE_REFRESH_TOKEN   --refresh-token\n"
            "    GOOGLE_CALENDAR_ID     --calendar-id  (default: primary)\n"
            "\n"
            "examples:\n"
            "  %(prog)s list\n"
            "  %(prog)s list --from 2025-01-01T00:00:00Z --to 2025-01-31T23:59:59Z\n"
            "  %(prog)s today\n"
            "  %(prog)s add --title 'Team standup' \\\n"
            "      --start 2025-06-01T09:00:00-07:00 --end 2025-06-01T09:30:00-07:00\n"
            "  %(prog)s update --event-id abc123 --title 'New title'\n"
            "  %(prog)s delete --event-id abc123\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Global credential flags
    parser.add_argument("--client-id", help="Google OAuth client ID (or GOOGLE_CLIENT_ID)")
    parser.add_argument("--client-secret", help="Google OAuth client secret (or GOOGLE_CLIENT_SECRET)")
    parser.add_argument("--refresh-token", help="Google OAuth refresh token (or GOOGLE_REFRESH_TOKEN)")
    parser.add_argument("--calendar-id", help="Calendar ID (or GOOGLE_CALENDAR_ID, default: primary)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted text")

    sub = parser.add_subparsers(dest="command", title="commands")

    # list
    p_list = sub.add_parser("list", help="List upcoming events")
    p_list.add_argument("--from", dest="time_min", metavar="ISO",
                        help="Start of time range (ISO 8601)")
    p_list.add_argument("--to", dest="time_max", metavar="ISO",
                        help="End of time range (ISO 8601)")
    p_list.add_argument("--max", type=int, default=10,
                        help="Maximum number of events (default: 10)")
    p_list.add_argument("--query", "-q", help="Free-text search query")

    # today
    sub.add_parser("today", help="Show today's events")

    # add
    p_add = sub.add_parser("add", help="Create a new event")
    p_add.add_argument("--title", required=True, help="Event title/summary")
    p_add.add_argument("--start", required=True, metavar="ISO",
                       help="Start time (ISO 8601, or YYYY-MM-DD for all-day)")
    p_add.add_argument("--end", required=True, metavar="ISO",
                       help="End time (ISO 8601, or YYYY-MM-DD for all-day)")
    p_add.add_argument("--description", help="Event description")
    p_add.add_argument("--location", help="Event location")
    p_add.add_argument("--attendees", metavar="EMAILS",
                       help="Comma-separated attendee emails")

    # update
    p_upd = sub.add_parser("update", help="Update an existing event")
    p_upd.add_argument("--event-id", required=True, help="Event ID to update")
    p_upd.add_argument("--title", help="New title")
    p_upd.add_argument("--start", metavar="ISO", help="New start time")
    p_upd.add_argument("--end", metavar="ISO", help="New end time")
    p_upd.add_argument("--description", help="New description")
    p_upd.add_argument("--location", help="New location")
    p_upd.add_argument("--attendees", metavar="EMAILS",
                       help="Comma-separated attendee emails")

    # delete
    p_del = sub.add_parser("delete", help="Delete an event")
    p_del.add_argument("--event-id", required=True, help="Event ID to delete")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Resolve credentials
    client_id = resolve_cred(args.client_id, "GOOGLE_CLIENT_ID")
    client_secret = resolve_cred(args.client_secret, "GOOGLE_CLIENT_SECRET")
    refresh_token = resolve_cred(args.refresh_token, "GOOGLE_REFRESH_TOKEN")
    calendar_id = resolve_cred(args.calendar_id, "GOOGLE_CALENDAR_ID", required=False) or "primary"

    # Get a fresh access token
    access_token = obtain_access_token(client_id, client_secret, refresh_token)

    # Dispatch
    commands = {
        "list": cmd_list,
        "today": cmd_today,
        "add": cmd_add,
        "update": cmd_update,
        "delete": cmd_delete,
    }
    commands[args.command](access_token, calendar_id, args)


if __name__ == "__main__":
    main()
