#!/usr/bin/env python3
"""Read AI Webhook Receiver - Catches meeting summaries pushed from Read AI.

Usage:
    python webhook_receiver.py                # Default port 9010
    python webhook_receiver.py --port 9010    # Custom port
    python webhook_receiver.py --host 0.0.0.0 # Bind to all interfaces (use with caution)
"""

import argparse
import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import Flask, request, jsonify

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TIMEZONE = os.environ.get("READAI_TIMEZONE", "America/Chicago")
TZ = ZoneInfo(TIMEZONE)
BIND_HOST = "127.0.0.1"
DEFAULT_PORT = 9010
DATA_DIR = Path(os.path.expanduser("~/.readai/meetings"))
LOG_DIR = Path(os.path.expanduser("~/.readai/logs"))

DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "webhook.log"),
    ],
)
log = logging.getLogger("readai-webhook")

app = Flask(__name__)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def save_meeting(data: dict, source_ip: str) -> Path:
    """Save incoming webhook meeting data."""
    now = datetime.now(TZ)
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y%m%d_%H%M%S")

    day_dir = DATA_DIR / date_str
    day_dir.mkdir(parents=True, exist_ok=True)

    # Extract title
    title = (
        data.get("title")
        or data.get("meeting_title")
        or data.get("meetingTitle")
        or data.get("name")
        or f"Meeting_{timestamp}"
    )
    safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title)[:60].strip()

    # Save JSON
    json_path = day_dir / f"{timestamp}_{safe_title}.json"
    payload = {
        "received_at": now.isoformat(),
        "source_ip": source_ip,
        "raw_payload": data,
    }
    json_path.write_text(json.dumps(payload, indent=2, default=str))

    # Save markdown
    md_path = day_dir / f"{timestamp}_{safe_title}.md"
    md_path.write_text(format_markdown(data, title, now))

    log.info(f"Saved '{title}' to {day_dir}")
    return json_path


def format_markdown(data: dict, title: str, received_at: datetime) -> str:
    """Format webhook payload as markdown."""
    lines = [f"# {title}", f"*Received: {received_at.strftime('%Y-%m-%d %I:%M %p CT')}*\n"]

    for key, label in [
        ("startTime", "Start"), ("start_time", "Start"), ("start", "Start"),
        ("endTime", "End"), ("end_time", "End"), ("end", "End"),
        ("duration", "Duration"), ("meeting_duration", "Duration"),
    ]:
        val = data.get(key)
        if val:
            lines.append(f"**{label}:** {val}")

    # Participants
    people = data.get("participants") or data.get("attendees") or data.get("people") or []
    if people:
        lines.append("\n## Participants")
        for p in people:
            name = p.get("name", p.get("displayName", str(p))) if isinstance(p, dict) else str(p)
            lines.append(f"- {name}")

    # Summary
    summary = data.get("summary") or data.get("meeting_summary") or data.get("recap") or ""
    if summary:
        lines.append("\n## Summary")
        lines.append(str(summary))

    # Topics
    topics = data.get("topics") or data.get("key_topics") or data.get("keyTopics") or []
    if topics:
        lines.append("\n## Key Topics")
        for t in (topics if isinstance(topics, list) else [topics]):
            text = t.get("title", t.get("name", str(t))) if isinstance(t, dict) else str(t)
            lines.append(f"- {text}")

    # Action Items
    actions = data.get("action_items") or data.get("actionItems") or data.get("tasks") or []
    if actions:
        lines.append("\n## Action Items")
        for item in (actions if isinstance(actions, list) else [actions]):
            if isinstance(item, dict):
                text = item.get("text", item.get("description", item.get("title", str(item))))
                assignee = item.get("assignee", item.get("owner", ""))
                suffix = f" (@{assignee})" if assignee else ""
                lines.append(f"- [ ] {text}{suffix}")
            else:
                lines.append(f"- [ ] {item}")

    # Decisions
    decisions = data.get("decisions") or data.get("key_decisions") or []
    if decisions:
        lines.append("\n## Decisions")
        for d in (decisions if isinstance(decisions, list) else [decisions]):
            lines.append(f"- {d}")

    # Transcript
    transcript = data.get("transcript") or data.get("transcription")
    if transcript:
        lines.append("\n## Transcript")
        if isinstance(transcript, str):
            lines.append(transcript[:3000])
            if len(transcript) > 3000:
                lines.append(f"\n*[Truncated - {len(transcript)} chars]*")
        elif isinstance(transcript, list):
            for entry in transcript[:30]:
                if isinstance(entry, dict):
                    speaker = entry.get("speaker", entry.get("speakerName", "?"))
                    text = entry.get("text", entry.get("content", ""))
                    lines.append(f"**{speaker}:** {text}")
                else:
                    lines.append(str(entry))
            if len(transcript) > 30:
                lines.append(f"\n*[{len(transcript)} entries total]*")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "readai-webhook", "timestamp": datetime.now(TZ).isoformat()})


@app.route("/webhook/readai", methods=["POST"])
def readai_webhook():
    source_ip = request.remote_addr
    data = request.get_json(force=True) if request.is_json else request.form.to_dict()

    if not data:
        return jsonify({"error": "empty payload"}), 400

    log.info(f"Webhook from {source_ip}: {json.dumps(data)[:200]}...")

    try:
        path = save_meeting(data, source_ip)
        return jsonify({"status": "received", "saved": str(path)}), 200
    except Exception as e:
        log.error(f"Failed: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route("/meetings", methods=["GET"])
def list_meetings():
    meetings_by_date = {}
    for i in range(7):
        d = datetime.now(TZ) - timedelta(days=i)
        ds = d.strftime("%Y-%m-%d")
        day_dir = DATA_DIR / ds
        if day_dir.exists():
            count = len(list(day_dir.glob("*.json")))
            if count:
                meetings_by_date[ds] = count
    return jsonify({"meetings_by_date": meetings_by_date, "total": sum(meetings_by_date.values())})


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Read AI Webhook Receiver")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--host", default=BIND_HOST)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    log.info(f"Starting on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == "__main__":
    main()
