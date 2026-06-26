#!/usr/bin/env python3

import json
import os
import sys
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
from icalendar import Calendar


ENV_CANDIDATES = [
    Path.cwd() / ".env",
    Path.home() / ".openclaw" / ".env",
]


def fail(message: str, code: int = 1, pretty: bool = False) -> int:
    if pretty:
        print(f"Error: {message}", file=sys.stderr)
    else:
        print(json.dumps({"ok": False, "error": message}, indent=2))
    return code


def get_args() -> Tuple[bool, Optional[str]]:
    pretty = False
    url = None

    for arg in sys.argv[1:]:
        if arg == "--pretty":
            pretty = True
        elif url is None:
            url = arg

    return pretty, url


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value



def read_env_file(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}

    if not path.exists() or not path.is_file():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        if not key:
            continue

        values[key] = strip_quotes(value)

    return values



def get_env_value(key: str) -> str:
    value = os.getenv(key, "").strip()
    if value:
        return value

    for env_path in ENV_CANDIDATES:
        file_values = read_env_file(env_path)
        value = file_values.get(key, "").strip()
        if value:
            return value

    return ""



def get_feed_url(cli_url: Optional[str]) -> str:
    if cli_url and cli_url.strip():
        return cli_url.strip()

    env_url = get_env_value("TRIPIT_ICAL_URL")
    if env_url:
        return env_url

    raise ValueError(
        "Missing TripIt iCal URL. Pass it as an argument or set TRIPIT_ICAL_URL in the environment or ~/.openclaw/.env."
    )



def fetch_ics(url: str) -> str:
    response = requests.get(
        url,
        headers={"User-Agent": "TripIt-iCal-Skill/1.1"},
        timeout=30,
    )
    response.raise_for_status()
    return response.text



def ensure_datetime(value: Any) -> Optional[datetime]:
    if value is None:
        return None

    if hasattr(value, "dt"):
        value = value.dt

    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value

    if isinstance(value, date):
        return datetime.combine(value, time.min, tzinfo=timezone.utc)

    return None



def serialize_dt(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.astimezone().isoformat()



def format_dt_human(dt_str: Optional[str]) -> str:
    if not dt_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(dt_str)
        return dt.astimezone().strftime("%Y-%m-%d %H:%M %Z")
    except Exception:
        return dt_str



def short_text(value: str, limit: int = 300) -> str:
    value = value.replace("\r", " ").replace("\n", " ").strip()
    if len(value) <= limit:
        return value
    return value[:limit].rstrip() + "..."



def parse_events(ics_text: str) -> List[Dict[str, Any]]:
    cal = Calendar.from_ical(ics_text)
    events: List[Dict[str, Any]] = []

    for component in cal.walk():
        if component.name != "VEVENT":
            continue

        start = ensure_datetime(component.get("dtstart"))
        end = ensure_datetime(component.get("dtend"))
        raw_description = str(component.get("description", "") or "").strip()

        events.append(
            {
                "uid": str(component.get("uid", "") or "").strip(),
                "summary": str(component.get("summary", "") or "").strip(),
                "location": str(component.get("location", "") or "").strip(),
                "description": raw_description,
                "description_short": short_text(raw_description) if raw_description else "",
                "status": str(component.get("status", "") or "").strip(),
                "start": start,
                "end": end,
            }
        )

    return events



def filter_upcoming(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    result: List[Dict[str, Any]] = []

    for event in events:
        start = event.get("start")
        end = event.get("end")

        if start is None:
            continue

        if start >= now or (end is not None and end >= now):
            result.append(event)

    result.sort(key=lambda x: x["start"])
    return result



def same_trip(prev: Dict[str, Any], curr: Dict[str, Any]) -> bool:
    prev_uid = prev.get("uid", "")
    curr_uid = curr.get("uid", "")

    if prev_uid and curr_uid and prev_uid.split("@")[0] == curr_uid.split("@")[0]:
        return True

    prev_end = prev.get("end") or prev.get("start")
    curr_start = curr.get("start")

    if prev_end and curr_start:
        gap_hours = (curr_start - prev_end).total_seconds() / 3600
        if gap_hours <= 36:
            return True

    return False



def group_trips(events: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    if not events:
        return []

    groups: List[List[Dict[str, Any]]] = [[events[0]]]

    for event in events[1:]:
        if same_trip(groups[-1][-1], event):
            groups[-1].append(event)
        else:
            groups.append([event])

    return groups



def make_event_payload(event: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "uid": event.get("uid") or None,
        "summary": event.get("summary") or None,
        "location": event.get("location") or None,
        "status": event.get("status") or None,
        "start": serialize_dt(event.get("start")),
        "end": serialize_dt(event.get("end")),
        "description_short": event.get("description_short") or None,
    }



def make_trip_payload(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not events:
        return {
            "start": None,
            "end": None,
            "item_count": 0,
            "title": None,
            "locations": [],
            "items": [],
        }

    start = events[0].get("start")
    end = events[-1].get("end") or events[-1].get("start")

    locations = []
    seen = set()
    for event in events:
        loc = (event.get("location") or "").strip()
        if loc and loc not in seen:
            seen.add(loc)
            locations.append(loc)

    title = events[0].get("summary") or "Upcoming trip"

    return {
        "start": serialize_dt(start),
        "end": serialize_dt(end),
        "item_count": len(events),
        "title": title,
        "locations": locations,
        "items": [make_event_payload(event) for event in events],
    }



def build_output(upcoming_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    trips = group_trips(upcoming_events)
    next_trip = make_trip_payload(trips[0]) if trips else None

    return {
        "ok": True,
        "source": "tripit_ical",
        "generated_at": serialize_dt(datetime.now(timezone.utc)),
        "counts": {
            "upcoming_events": len(upcoming_events),
            "detected_trips": len(trips),
        },
        "next_trip": next_trip,
        "upcoming_events": [make_event_payload(event) for event in upcoming_events[:20]],
    }



def print_pretty(output: Dict[str, Any]) -> None:
    if not output.get("ok"):
        print(f"Error: {output.get('error', 'Unknown error')}")
        return

    counts = output.get("counts", {})
    next_trip = output.get("next_trip")
    events = output.get("upcoming_events", [])

    print("TripIt iCal summary")
    print(f"Generated : {format_dt_human(output.get('generated_at'))}")
    print(f"Events    : {counts.get('upcoming_events', 0)} upcoming")
    print(f"Trips     : {counts.get('detected_trips', 0)} detected")
    print()

    if next_trip:
        print("Next trip")
        print(f"  Title     : {next_trip.get('title') or 'N/A'}")
        print(f"  Starts    : {format_dt_human(next_trip.get('start'))}")
        print(f"  Ends      : {format_dt_human(next_trip.get('end'))}")
        print(f"  Items     : {next_trip.get('item_count', 0)}")

        locations = next_trip.get("locations") or []
        if locations:
            print(f"  Locations : {', '.join(locations)}")
        print()

        items = next_trip.get("items") or []
        if items:
            print("Trip items")
            for idx, item in enumerate(items, start=1):
                print(f"  {idx}. {item.get('summary') or 'Untitled'}")
                print(f"     Start    : {format_dt_human(item.get('start'))}")
                print(f"     End      : {format_dt_human(item.get('end'))}")
                if item.get("location"):
                    print(f"     Location : {item.get('location')}")
                if item.get("status"):
                    print(f"     Status   : {item.get('status')}")
                if item.get("description_short"):
                    print(f"     Notes    : {item.get('description_short')}")
                print()
    else:
        print("No next trip detected.")
        print()

    if events:
        print("Upcoming events")
        for idx, event in enumerate(events, start=1):
            print(f"  {idx}. {event.get('summary') or 'Untitled'}")
            print(f"     Start    : {format_dt_human(event.get('start'))}")
            print(f"     End      : {format_dt_human(event.get('end'))}")
            if event.get("location"):
                print(f"     Location : {event.get('location')}")
            if event.get("status"):
                print(f"     Status   : {event.get('status')}")
            print()



def main() -> int:
    pretty, cli_url = get_args()

    try:
        url = get_feed_url(cli_url)
        ics_text = fetch_ics(url)
        all_events = parse_events(ics_text)
        upcoming_events = filter_upcoming(all_events)
        output = build_output(upcoming_events)

        if pretty:
            print_pretty(output)
        else:
            print(json.dumps(output, indent=2))

        return 0

    except requests.HTTPError as e:
        return fail(f"HTTP error while fetching TripIt iCal feed: {e}", 2, pretty)
    except requests.RequestException as e:
        return fail(f"Network error while fetching TripIt iCal feed: {e}", 3, pretty)
    except ValueError as e:
        return fail(str(e), 4, pretty)
    except Exception as e:
        return fail(f"Unexpected error: {e}", 5, pretty)


if __name__ == "__main__":
    raise SystemExit(main())
