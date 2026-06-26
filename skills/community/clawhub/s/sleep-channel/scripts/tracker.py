#!/usr/bin/env python3
import csv
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

TIMEZONE = ZoneInfo(os.environ.get("SLEEP_TIMEZONE", "UTC"))
WORKSPACE = os.environ.get("WORKSPACE", os.path.join(os.path.expanduser("~"), ".openclaw", "workspace"))
DATA_DIR = os.path.join(WORKSPACE, "data")
STATE_DIR = os.path.join(WORKSPACE, "state")
LOG_FILE = os.path.join(DATA_DIR, "sleep_log.csv")
STATE_FILE = os.path.join(STATE_DIR, "sleep_summary_state.json")
CSV_FIELDS = [
    "entry_id",
    "timestamp_utc",
    "date_local",
    "time_local",
    "timezone",
    "action",
    "emoji",
    "notes",
    "source_channel_id",
    "source_message_id",
    "source_author_id",
    "status",
    "supersedes_entry_id",
]

ACTION_DISPLAY = {
    "bed": "🌙🛏️",
    "sleep": "😴💤",
    "awake": "🌌👀",
    "up": "☀️🚶",
    "rest": "🛌",
    "note": "📝",
}

@dataclass
class ParsedEvent:
    action: str
    emoji: str
    notes: str


def ensure_dirs() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(STATE_DIR, exist_ok=True)


def initialize_log() -> None:
    ensure_dirs()
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def read_rows() -> list[dict]:
    initialize_log()
    with open(LOG_FILE, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_rows(rows: list[dict]) -> None:
    with open(LOG_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def parse_event(text: str) -> ParsedEvent:
    raw = normalize_ws(text)
    lowered = raw.lower()

    if any(phrase in lowered for phrase in ["fell asleep", "falling asleep", "asleep around", "finally asleep", "passed out", "went to sleep"]):
        return ParsedEvent("sleep", ACTION_DISPLAY["sleep"], raw)

    if any(phrase in lowered for phrase in ["awake now", "got up", "i'm up", "im up", "up now", "woke up for the day", "starting my day", "getting out of bed"]):
        return ParsedEvent("up", ACTION_DISPLAY["up"], raw)

    if any(phrase in lowered for phrase in ["still awake", "awake again", "woke back up", "laying in bed", "lying in bed", "can't sleep", "cant sleep"]):
        return ParsedEvent("awake", ACTION_DISPLAY["awake"], raw)

    # "woke up" without "now" (e.g. "Woke up at 5:30 am") → up
    if any(phrase in lowered for phrase in ["woke up", "woke at"]):
        return ParsedEvent("up", ACTION_DISPLAY["up"], raw)

    # standalone "awake" → awake
    if lowered == "awake" or lowered.startswith("awake ") or lowered.endswith(" awake"):
        return ParsedEvent("awake", ACTION_DISPLAY["awake"], raw)

    if any(phrase in lowered for phrase in ["going to bed", "heading to bed", "getting in bed", "trying to sleep", "going to try to sleep", "bed now", "in bed now"]):
        return ParsedEvent("bed", ACTION_DISPLAY["bed"], raw)

    if any(phrase in lowered for phrase in ["resting", "nap", "napping", "try to sleep more", "going back to sleep"]):
        return ParsedEvent("rest", ACTION_DISPLAY["rest"], raw)

    return ParsedEvent("note", ACTION_DISPLAY["note"], raw)


def next_entry_id(rows: list[dict]) -> str:
    max_num = 0
    for row in rows:
        m = re.match(r"slp-(\d+)", row.get("entry_id", ""))
        if m:
            max_num = max(max_num, int(m.group(1)))
    return f"slp-{max_num + 1:06d}"


def format_time_local(dt_local: datetime) -> str:
    try:
        return dt_local.strftime("%-I:%M%p").lower()
    except ValueError:
        return dt_local.strftime("%I:%M%p").lstrip("0").lower()



def build_row(rows: list[dict], text: str, channel_id: str = "", message_id: str = "", author_id: str = "", timestamp_utc: str | None = None, supersedes_entry_id: str = "") -> dict:
    event = parse_event(text)
    if not timestamp_utc:
        raise ValueError("timestamp_utc is required — source Discord message timestamp must be provided")
    dt_utc = datetime.fromisoformat(timestamp_utc.replace("Z", "+00:00"))
    dt_local = dt_utc.astimezone(TIMEZONE)
    return {
        "entry_id": next_entry_id(rows),
        "timestamp_utc": dt_utc.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "date_local": dt_local.strftime("%Y-%m-%d"),
        "time_local": format_time_local(dt_local),
        "timezone": str(TIMEZONE),
        "action": event.action,
        "emoji": event.emoji,
        "notes": event.notes,
        "source_channel_id": channel_id,
        "source_message_id": message_id,
        "source_author_id": author_id,
        "status": "active",
        "supersedes_entry_id": supersedes_entry_id,
    }


def dedupe_exists(rows: list[dict], source_message_id: str) -> bool:
    if not source_message_id:
        return False
    return any(row.get("source_message_id") == source_message_id for row in rows)


def add_entry(text: str, channel_id: str = "", message_id: str = "", author_id: str = "", timestamp_utc: str | None = None) -> dict:
    rows = read_rows()
    if dedupe_exists(rows, message_id):
        for row in rows:
            if row.get("source_message_id") == message_id:
                return row
    row = build_row(rows, text, channel_id, message_id, author_id, timestamp_utc)
    rows.append(row)
    write_rows(rows)
    return row


def correct_latest(text: str, channel_id: str = "", message_id: str = "", author_id: str = "", timestamp_utc: str | None = None) -> dict:
    rows = read_rows()
    active_rows = [r for r in rows if r.get("status") == "active"]
    latest = active_rows[-1] if active_rows else None
    if latest:
        latest["status"] = "superseded"
    row = build_row(rows, text, channel_id, message_id, author_id, timestamp_utc, supersedes_entry_id=latest.get("entry_id", "") if latest else "")
    rows.append(row)
    write_rows(rows)
    return row


def delete_latest() -> dict | None:
    rows = read_rows()
    active_rows = [r for r in rows if r.get("status") == "active"]
    latest = active_rows[-1] if active_rows else None
    if latest:
        latest["status"] = "deleted"
        write_rows(rows)
    return latest


def render_summary() -> str:
    rows = [r for r in read_rows() if r.get("status") == "active"]
    if not rows:
        return "# Sleep log\n\n_No entries yet._"

    rows.sort(key=lambda r: r["timestamp_utc"])
    local_dates = sorted({r["date_local"] for r in rows})
    latest_id = rows[-1]["entry_id"]

    lines = ["# Sleep log", ""]
    for date in local_dates:
        lines.append(f"## {date}")
        for row in [r for r in rows if r["date_local"] == date]:
            line = f"- {row['emoji']} {row['time_local']} — {row['notes']}"
            if row["entry_id"] == latest_id:
                line = f"- **{row['emoji']} {row['time_local']} — {row['notes']}**"
            lines.append(line)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def get_state() -> dict:
    ensure_dirs()
    if not os.path.exists(STATE_FILE):
        return {"summary_message_id": "", "channel_id": ""}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def set_state(summary_message_id: str = "", channel_id: str = "") -> dict:
    ensure_dirs()
    state = get_state()
    if summary_message_id:
        state["summary_message_id"] = summary_message_id
    if channel_id:
        state["channel_id"] = channel_id
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)
        f.write("\n")
    return state


def print_json(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def usage() -> int:
    print("Usage: tracker.py add|correct-latest|delete-latest|render|state-get|state-set [args...]", file=sys.stderr)
    return 1


def main() -> int:
    initialize_log()
    if len(sys.argv) < 2:
        return usage()

    cmd = sys.argv[1]
    if cmd == "add":
        if len(sys.argv) < 3:
            return usage()
        text = sys.argv[2]
        channel_id = sys.argv[3] if len(sys.argv) > 3 else ""
        message_id = sys.argv[4] if len(sys.argv) > 4 else ""
        author_id = sys.argv[5] if len(sys.argv) > 5 else ""
        timestamp_utc = sys.argv[6] if len(sys.argv) > 6 else None
        row = add_entry(text, channel_id, message_id, author_id, timestamp_utc)
        print_json(row)
        return 0

    if cmd == "correct-latest":
        if len(sys.argv) < 3:
            return usage()
        text = sys.argv[2]
        channel_id = sys.argv[3] if len(sys.argv) > 3 else ""
        message_id = sys.argv[4] if len(sys.argv) > 4 else ""
        author_id = sys.argv[5] if len(sys.argv) > 5 else ""
        timestamp_utc = sys.argv[6] if len(sys.argv) > 6 else None
        row = correct_latest(text, channel_id, message_id, author_id, timestamp_utc)
        print_json(row)
        return 0

    if cmd == "delete-latest":
        row = delete_latest()
        print_json(row or {"deleted": False})
        return 0

    if cmd == "render":
        print(render_summary())
        return 0

    if cmd == "state-get":
        print_json(get_state())
        return 0

    if cmd == "state-set":
        summary_message_id = sys.argv[2] if len(sys.argv) > 2 else ""
        channel_id = sys.argv[3] if len(sys.argv) > 3 else ""
        print_json(set_state(summary_message_id, channel_id))
        return 0

    return usage()


if __name__ == "__main__":
    raise SystemExit(main())
