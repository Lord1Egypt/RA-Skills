#!/usr/bin/env python3
"""
flush_to_obsidian.py - Write queued weather summaries to Obsidian.
Uses Yakitrak obsidian-cli: create "note" --vault "V" --content "..." --append
"""

import json
import os
import sys
import subprocess
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import env_loader

STATE_DIR = env_loader.STATE_DIR
QUEUE_FILE = os.path.join(STATE_DIR, "summary_queue.jsonl")
DONE_FILE = os.path.join(STATE_DIR, "summary_queue.done.jsonl")
WRITTEN_IDS_FILE = os.path.join(STATE_DIR, "written_ids.json")
LAST_FLUSH_FILE = os.path.join(STATE_DIR, "last_flush.txt")

OBSIDIAN_BIN = os.environ.get("OBSIDIAN_BIN", "obsidian-cli")
OBSIDIAN_VAULT = os.environ.get("OBSIDIAN_VAULT", "")
NOTE_PATH = os.environ.get("OBSIDIAN_NOTE_PATH", "Inbox/WeatherPanel Note AI PC.md")


def load_written_ids():
    if os.path.exists(WRITTEN_IDS_FILE):
        for enc in ["utf-8", "gbk"]:
            try:
                with open(WRITTEN_IDS_FILE, "r", encoding=enc) as f:
                    return set(json.load(f))
            except (json.JSONDecodeError, UnicodeDecodeError, IOError):
                continue
    return set()


def save_written_ids(ids):
    with open(WRITTEN_IDS_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted(ids), f)


def read_queue():
    records = []
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    return records


def write_to_obsidian(content, timestamp):
    """Yakitrak: obsidian-cli create "path" --vault "V" --content "..." --append"""
    formatted = (
        f"\n---\n"
        f"## WeatherPanel Note AI PC Summary - {timestamp[:19].replace('T', ' ')} UTC\n\n"
        f"{content}\n"
        f"<!-- weatherpanel-note-aipc-{timestamp} -->\n"
    )

    cmd = [OBSIDIAN_BIN, "create", NOTE_PATH]
    if OBSIDIAN_VAULT:
        cmd.extend(["--vault", OBSIDIAN_VAULT])
    cmd.extend(["--content", formatted, "--append"])

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30, encoding="utf-8",
        )
        if result.returncode != 0:
            print(f"[flush] Obsidian error: {result.stderr}", file=sys.stderr)
            return False
        return True
    except subprocess.TimeoutExpired:
        print("[flush] Obsidian timeout", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"[flush] '{OBSIDIAN_BIN}' not found", file=sys.stderr)
        return False


def main():
    os.makedirs(STATE_DIR, exist_ok=True)

    print(f"[flush] BIN={OBSIDIAN_BIN} VAULT={OBSIDIAN_VAULT or '(empty)'} NOTE={NOTE_PATH}")

    records = read_queue()
    if not records:
        print("[flush] No pending records.")
        sys.exit(0)

    written_ids = load_written_ids()
    pending = [r for r in records if r.get("id") not in written_ids]

    if not pending:
        print("[flush] All records already written.")
        sys.exit(0)

    print(f"[flush] {len(pending)} pending record(s)...")

    success_count = 0
    for rec in pending:
        rid = rec["id"]
        if write_to_obsidian(rec.get("content", ""), rec.get("timestamp", "")):
            written_ids.add(rid)
            success_count += 1
            print(f"[flush] Written: {rid}")
            with open(DONE_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        else:
            print(f"[flush] FAILED: {rid}", file=sys.stderr)

    save_written_ids(written_ids)

    remaining = [r for r in records if r.get("id") not in written_ids]
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        for r in remaining:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    now = datetime.now(timezone.utc).isoformat()
    with open(LAST_FLUSH_FILE, "w", encoding="utf-8") as f:
        f.write(now)

    print(f"[flush] Done. {success_count}/{len(pending)} written.")


if __name__ == "__main__":
    main()
