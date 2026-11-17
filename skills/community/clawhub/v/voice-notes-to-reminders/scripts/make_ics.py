#!/usr/bin/env python3
"""
make_ics.py — write a standard iCalendar (.ics) file for a timed commitment.

Double-clicking the resulting file adds the event to Outlook OR Google Calendar —
no OAuth, no credentials, works for both. The tool never talks to a calendar API;
it only writes a file the operator accepts. (See reference/security.md — no send paths.)

Stdlib only. Includes a VALARM reminder and the original transcript in the description.

CLI:
    python3 make_ics.py \
        --summary "Follow up with Sally re: incident report" \
        --start 2026-07-15T10:00:00 \
        --tz America/New_York \
        --duration-min 30 \
        --transcript "Set a reminder to follow up with Sally about the incident report next Tuesday" \
        --outdir output/events

Prints the path of the file written. Also importable: build_ics(...) / write_event(...).
"""
import argparse
import hashlib
import os
import re
from datetime import datetime, timedelta

try:
    from zoneinfo import ZoneInfo  # py3.9+
except ImportError:  # pragma: no cover
    ZoneInfo = None


def _fold(line):
    """RFC 5545: fold lines longer than 75 octets."""
    out, limit = [], 73
    while len(line.encode("utf-8")) > 75:
        chunk = line[:limit]
        out.append(chunk)
        line = " " + line[limit:]
    out.append(line)
    return "\r\n".join(out)


def _escape(text):
    return (text.replace("\\", "\\\\").replace(";", r"\;")
                .replace(",", r"\,").replace("\n", r"\n"))


def _slug(text, n=40):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (s[:n] or "event").strip("-")


def _stamp_utc(dt):
    return dt.strftime("%Y%m%dT%H%M%SZ")


def build_ics(summary, start_local, tz_name, duration_min=30,
              transcript="", reminder_min=15, stamp=None):
    """Return .ics text. start_local is a naive datetime in tz_name."""
    if ZoneInfo is None:
        raise RuntimeError("zoneinfo unavailable; upgrade to Python 3.9+")
    tz = ZoneInfo(tz_name)
    start = start_local.replace(tzinfo=tz)
    end = start + timedelta(minutes=duration_min)
    # deterministic UID (no random/now dependency): hash of the salient fields
    uid_seed = f"{summary}|{start.isoformat()}|{transcript}".encode("utf-8")
    uid = hashlib.sha1(uid_seed).hexdigest() + "@voice-notes-to-reminders.local"
    # DTSTAMP just needs to be a valid UTC timestamp; deriving it from `start`
    # keeps the file deterministic (no wall-clock dependency).
    dtstamp = _stamp_utc(stamp) if stamp else _stamp_utc(start.astimezone(ZoneInfo("UTC")))
    desc = _escape(transcript) if transcript else _escape(summary)

    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//NerveX//voice-notes-to-reminders//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTAMP:{dtstamp}",
        f"DTSTART;TZID={tz_name}:{start.strftime('%Y%m%dT%H%M%S')}",
        f"DTEND;TZID={tz_name}:{end.strftime('%Y%m%dT%H%M%S')}",
        _fold(f"SUMMARY:{_escape(summary)}"),
        _fold(f"DESCRIPTION:{desc}"),
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        _fold(f"DESCRIPTION:Reminder: {_escape(summary)}"),
        f"TRIGGER:-PT{int(reminder_min)}M",
        "END:VALARM",
        "END:VEVENT",
        "END:VCALENDAR",
    ]
    return "\r\n".join(lines) + "\r\n"


def write_event(summary, start_local, tz_name, outdir="output/events",
                duration_min=30, transcript="", reminder_min=15):
    os.makedirs(outdir, exist_ok=True)
    fname = f"{start_local.strftime('%Y-%m-%d')}_{_slug(summary)}.ics"
    path = os.path.join(outdir, fname)
    ics = build_ics(summary, start_local, tz_name, duration_min, transcript, reminder_min)
    with open(path, "w", newline="") as f:
        f.write(ics)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", required=True)
    ap.add_argument("--start", required=True, help="ISO local datetime, e.g. 2026-07-15T10:00:00")
    ap.add_argument("--tz", default="America/New_York")
    ap.add_argument("--duration-min", type=int, default=30)
    ap.add_argument("--reminder-min", type=int, default=15)
    ap.add_argument("--transcript", default="")
    ap.add_argument("--outdir", default="output/events")
    args = ap.parse_args()

    start_local = datetime.fromisoformat(args.start)
    path = write_event(args.summary, start_local, args.tz, args.outdir,
                       args.duration_min, args.transcript, args.reminder_min)
    print(path)


if __name__ == "__main__":
    main()
