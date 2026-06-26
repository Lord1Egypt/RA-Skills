#!/usr/bin/env python3
"""
Event Monitor — Check for new DETECTION_SENSOR_APP events and output alerts.

Since the receiver only captures DETECTION_SENSOR_APP messages, every new
record is an alert (GPIO triggered on remote sensor = preset target detected).

Designed to be run periodically by OpenClaw cron or system crontab.

Usage:
    python event_monitor.py
    python event_monitor.py --data-dir ./data
"""

import json
import hashlib
import sys
import argparse
import os
from pathlib import Path

DEFAULT_DATA_DIR = os.environ.get(
    "MESH_DATA_DIR",
    str(Path(__file__).resolve().parent.parent / "data"),
)

# ═══════════════════════════════════════════════════════════════
# STATE MANAGEMENT
# ═══════════════════════════════════════════════════════════════


def load_state(data_dir: str) -> dict:
    state_path = Path(data_dir) / "monitor_state.json"
    try:
        if state_path.exists():
            return json.loads(state_path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {"last_offset": 0, "seen_hashes": []}


def save_state(data_dir: str, state: dict) -> None:
    state_path = Path(data_dir) / "monitor_state.json"
    state["seen_hashes"] = state["seen_hashes"][-2000:]
    try:
        state_path.write_text(
            json.dumps(state, ensure_ascii=False), encoding="utf-8"
        )
    except Exception as e:
        print(f"Warning: could not save state: {e}", file=sys.stderr)


# ═══════════════════════════════════════════════════════════════
# CORE
# ═══════════════════════════════════════════════════════════════


def record_hash(record: dict) -> str:
    """Hash for deduplication based on received_at + sender + data."""
    key = json.dumps(
        {
            "received_at": record.get("received_at"),
            "sender": record.get("sender"),
            "data": record.get("data"),
        },
        sort_keys=True,
    )
    return hashlib.md5(key.encode()).hexdigest()[:12]


def read_new_records(data_dir: str, last_offset: int) -> tuple[list[dict], int]:
    """Read new records from JSONL file starting at byte offset.

    If the file is smaller than last_offset (file was rotated), starts from 0.
    """
    jsonl_path = Path(data_dir) / "sensor_data.jsonl"
    if not jsonl_path.exists():
        return [], 0

    try:
        file_size = jsonl_path.stat().st_size
    except OSError:
        return [], last_offset

    if file_size < last_offset:
        last_offset = 0

    records = []
    try:
        with open(jsonl_path, "r", encoding="utf-8") as f:
            f.seek(last_offset)
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
            new_offset = f.tell()
    except Exception:
        return [], last_offset

    return records, new_offset


def check_events(data_dir: str) -> dict:
    """Read new records and convert each one into an alert.

    Every DETECTION_SENSOR_APP record is a high-priority alert.
    """
    state = load_state(data_dir)
    last_offset = state.get("last_offset", 0)
    seen_hashes = set(state.get("seen_hashes", []))

    records, new_offset = read_new_records(data_dir, last_offset)

    alerts = []
    new_hashes = []

    for record in records:
        h = record_hash(record)
        if h in seen_hashes:
            continue
        new_hashes.append(h)

        alerts.append({
            "priority": "high",
            "sender": record.get("sender", "unknown"),
            "text": record.get("data", {}).get("text", ""),
            "received_at": record.get("received_at", ""),
            "channel": record.get("channel", ""),
            "portnum": record.get("portnum", ""),
        })

    state["last_offset"] = new_offset
    state["seen_hashes"] = list(seen_hashes) + new_hashes
    save_state(data_dir, state)

    if alerts:
        summary = f"🚨 {len(alerts)} new detection alert(s) from {len(records)} record(s)"
    else:
        summary = f"No new alerts ({len(records)} record(s) checked)"

    return {
        "alerts": alerts,
        "summary": summary,
        "alert_count": len(alerts),
        "new_records": len(records),
    }


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(description="Meshtastic Detection Event Monitor")
    parser.add_argument(
        "--data-dir", default=DEFAULT_DATA_DIR, help="Data storage directory"
    )
    args = parser.parse_args()

    result = check_events(args.data_dir)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
