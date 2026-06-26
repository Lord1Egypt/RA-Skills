"""
scripts/phase_signal_reconciler.py — Sync dream phase signals from JSON files to SQL

OpenClaw owns the JSON state files (phase-signals.json, daily-ingestion.json,
short-term-recall.json). This script reads them after each dream cycle and writes
durable SQL copies — so phase signal history survives if the files are deleted or
the workspace is rebuilt.

Design principle:
  - OpenClaw reads/writes its JSON files unchanged (we never touch them)
  - This script reads the JSON files and UPSERTs into dreams.PhaseSignals
  - SQL is the backup/audit copy; JSON is the live state OpenClaw uses
  - Safe to run multiple times (idempotent UPSERT)

When to run:
  Add to crontab AFTER the dream cycle (e.g., 4:05 AM, between dream and archiver):
  5 8 * * * python /path/to/scripts/phase_signal_reconciler.py

Usage:
    python scripts/phase_signal_reconciler.py
    python scripts/phase_signal_reconciler.py --config /path/to/config.yml
    python scripts/phase_signal_reconciler.py --dry-run
"""

import sys
import os
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
from src.sql_connector import SQLDreamerConnector


def load_config(config_path: str) -> dict:
    with open(config_path) as f:
        return yaml.safe_load(f)


def parse_phase_signals(workspace_dir: Path) -> list[dict]:
    """
    Parse memory/.dreams/phase-signals.json into SQL-ready rows.

    Returns list of dicts matching dreams.PhaseSignals columns.
    """
    path = workspace_dir / "memory" / ".dreams" / "phase-signals.json"
    if not path.exists():
        return []

    with open(path) as f:
        data = json.load(f)

    rows = []
    for key, entry in data.get("entries", {}).items():
        row = {
            "signal_key": key,
            "light_hits": entry.get("lightHits", 0),
            "rem_hits": entry.get("remHits", 0),
            "last_light_at": entry.get("lastLightAt"),
            "last_rem_at": entry.get("lastRemAt"),
            "updated_at": data.get("updatedAt", datetime.now(timezone.utc).isoformat()),
        }
        rows.append(row)

    return rows


def parse_daily_ingestion(workspace_dir: Path) -> list[dict]:
    """
    Parse memory/.dreams/daily-ingestion.json into a summary for SQL logging.
    Returns list of file entries as dicts.
    """
    path = workspace_dir / "memory" / ".dreams" / "daily-ingestion.json"
    if not path.exists():
        return []

    with open(path) as f:
        data = json.load(f)

    return [
        {"file_path": fp, "mtime_ms": info.get("mtimeMs"), "size": info.get("size")}
        for fp, info in data.get("files", {}).items()
    ]


def upsert_phase_signals(conn: SQLDreamerConnector, rows: list[dict], dry_run: bool) -> int:
    """
    UPSERT phase signal rows into dreams.PhaseSignals.
    Uses MERGE for idempotent upsert.
    Returns count of rows processed.
    """
    if not rows:
        return 0

    if dry_run:
        print(f"  [dry-run] would upsert {len(rows)} phase signal rows")
        return len(rows)

    sql = """
        MERGE dreams.PhaseSignals AS target
        USING (SELECT ? AS signal_key) AS source ON target.signal_key = source.signal_key
        WHEN MATCHED THEN
            UPDATE SET
                light_hits   = ?,
                rem_hits     = ?,
                last_light_at = ?,
                last_rem_at   = ?,
                updated_at    = ?
        WHEN NOT MATCHED THEN
            INSERT (signal_key, light_hits, rem_hits, last_light_at, last_rem_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?);
    """
    now = datetime.now(timezone.utc)

    processed = 0
    for row in rows:
        last_light = _parse_ts(row["last_light_at"])
        last_rem = _parse_ts(row["last_rem_at"])
        updated = _parse_ts(row["updated_at"]) or now

        params = (
            row["signal_key"],           # USING source.signal_key
            row["light_hits"],            # UPDATE light_hits
            row["rem_hits"],              # UPDATE rem_hits
            last_light,                   # UPDATE last_light_at
            last_rem,                     # UPDATE last_rem_at
            updated,                      # UPDATE updated_at
            row["signal_key"],            # INSERT signal_key
            row["light_hits"],            # INSERT light_hits
            row["rem_hits"],              # INSERT rem_hits
            last_light,                   # INSERT last_light_at
            last_rem,                     # INSERT last_rem_at
            updated,                      # INSERT updated_at
        )
        conn.execute(sql, params)
        processed += 1

    return processed


def _parse_ts(ts_str) -> datetime | None:
    """Parse ISO timestamp string to datetime, or return None."""
    if not ts_str:
        return None
    try:
        return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def run(config_path: str, dry_run: bool = False) -> None:
    cfg = load_config(config_path)
    workspace_dir = Path(cfg["dreaming"]["workspace_dir"])

    print(f"phase_signal_reconciler: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Workspace: {workspace_dir}")
    if dry_run:
        print("  MODE: dry-run")

    # Parse JSON state files
    phase_signals = parse_phase_signals(workspace_dir)
    daily_ingestion = parse_daily_ingestion(workspace_dir)

    print(f"\n  Phase signals found: {len(phase_signals)}")
    print(f"  Daily ingestion files tracked: {len(daily_ingestion)}")

    if not phase_signals:
        print("  ⚠️  No phase signals to sync — dream cycle may not have run yet")
        return

    with SQLDreamerConnector.from_config(config_path) as conn:
        count = upsert_phase_signals(conn, phase_signals, dry_run)
        print(f"  ✅ Phase signals synced to SQL: {count} rows")

        # Log daily ingestion summary as an activity record
        if not dry_run and daily_ingestion:
            for entry in daily_ingestion:
                sql = """
                    MERGE dreams.DreamCorpus AS target
                    USING (SELECT ? AS key_name, ? AS cycle_date) AS source
                        ON target.key_name = source.key_name AND target.cycle_date = source.cycle_date
                    WHEN NOT MATCHED THEN
                        INSERT (cycle_date, category, key_name, ingested_at)
                        VALUES (?, 'daily_ingestion_file', ?, ?);
                """
                today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                conn.execute(sql, (
                    entry["file_path"], today,
                    today, entry["file_path"], datetime.now(timezone.utc)
                ))
            print(f"  ✅ Daily ingestion records synced: {len(daily_ingestion)} files")

    print("\n✅ phase_signal_reconciler complete")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync dream phase signals from JSON to SQL")
    parser.add_argument("--config", default="config/config.yml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(args.config, dry_run=args.dry_run)
