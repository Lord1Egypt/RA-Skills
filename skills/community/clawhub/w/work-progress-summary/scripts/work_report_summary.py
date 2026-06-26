#!/usr/bin/env python3
"""SQLite-backed work report recorder and reporter."""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence


DEFAULT_DB_DIRNAME = ".work_report_summary"
DEFAULT_DB_NAME = "default"
STATUS_ORDER = ("done", "in_progress", "blocked")
DB_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
HISTORY_ACTIONS = ("create", "update", "delete")


class CliError(Exception):
    """Raise for user-facing CLI validation errors."""


def parse_positive_int(raw_value: str, field_name: str) -> int:
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise CliError("{0} must be an integer.".format(field_name)) from exc
    if value <= 0:
        raise CliError("{0} must be greater than 0.".format(field_name))
    return value


def parse_work_date(raw_value: Optional[str]) -> date:
    if raw_value is None:
        return date.today()
    try:
        return date.fromisoformat(raw_value)
    except ValueError as exc:
        raise CliError("Date must use YYYY-MM-DD.") from exc


def normalize_db_name(raw_value: Optional[str]) -> str:
    value = (raw_value or os.environ.get("WORK_REPORT_SUMMARY_DB_NAME") or DEFAULT_DB_NAME).strip()
    if not value:
        raise CliError("Database name cannot be empty.")
    if not DB_NAME_PATTERN.fullmatch(value):
        raise CliError(
            "Database name must match [A-Za-z0-9._-]+ and cannot contain path separators."
        )
    if value.endswith(".db"):
        return value
    return "{0}.db".format(value)


def resolve_db_path(db_path: Optional[str], db_name: Optional[str]) -> Path:
    if db_path:
        path = Path(db_path).expanduser()
        if path.suffix.lower() != ".db":
            raise CliError("Explicit database path must end with .db.")
        return path

    home_override = os.environ.get("WORK_REPORT_SUMMARY_HOME")
    if home_override:
        base_dir = Path(home_override).expanduser()
    else:
        base_dir = Path.home() / DEFAULT_DB_DIRNAME
    return base_dir / normalize_db_name(db_name)


def now_iso() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def connect_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    ensure_schema(connection)
    return connection


def ensure_schema(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS work_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            work_date TEXT NOT NULL,
            task TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('done', 'in_progress', 'blocked')),
            details TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_work_entries_work_date
        ON work_entries(work_date)
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS work_entry_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_id INTEGER NOT NULL,
            version INTEGER NOT NULL,
            action TEXT NOT NULL CHECK (action IN ('create', 'update', 'delete')),
            source_command TEXT NOT NULL,
            work_date TEXT NOT NULL,
            task TEXT NOT NULL,
            status TEXT NOT NULL CHECK (status IN ('done', 'in_progress', 'blocked')),
            details TEXT NOT NULL DEFAULT '',
            created_at TEXT NOT NULL,
            changed_at TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_work_entry_history_entry_version
        ON work_entry_history(entry_id, version)
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_work_entry_history_entry_id
        ON work_entry_history(entry_id)
        """
    )
    backfill_history_for_existing_entries(connection)


def backfill_history_for_existing_entries(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        INSERT INTO work_entry_history (
            entry_id,
            version,
            action,
            source_command,
            work_date,
            task,
            status,
            details,
            created_at,
            changed_at
        )
        SELECT
            work_entries.id,
            1,
            'create',
            'schema-backfill',
            work_entries.work_date,
            work_entries.task,
            work_entries.status,
            work_entries.details,
            work_entries.created_at,
            work_entries.created_at
        FROM work_entries
        WHERE NOT EXISTS (
            SELECT 1
            FROM work_entry_history
            WHERE work_entry_history.entry_id = work_entries.id
        )
        """
    )


def normalize_item(raw_item: Any, index: int) -> Dict[str, str]:
    if isinstance(raw_item, str):
        task = raw_item.strip()
        if not task:
            raise CliError("Item {0} must not be empty.".format(index))
        return {"task": task, "status": "done", "details": ""}

    if not isinstance(raw_item, dict):
        raise CliError("Item {0} must be either a string or an object.".format(index))

    task = str(raw_item.get("task", "")).strip()
    if not task:
        raise CliError("Item {0} must include a non-empty task.".format(index))

    status = str(raw_item.get("status", "done")).strip().lower() or "done"
    if status not in STATUS_ORDER:
        raise CliError(
            "Item {0} status must be one of: {1}.".format(index, ", ".join(STATUS_ORDER))
        )

    details = str(raw_item.get("details", "") or "").strip()
    return {"task": task, "status": status, "details": details}


def normalize_task_text(raw_value: str) -> str:
    value = raw_value.strip()
    if not value:
        raise CliError("Task must be non-empty.")
    return value


def normalize_status_value(raw_value: str) -> str:
    value = raw_value.strip().lower()
    if value not in STATUS_ORDER:
        raise CliError("Status must be one of: {0}.".format(", ".join(STATUS_ORDER)))
    return value


def parse_items_json(raw_items: str, *, allow_empty: bool = False) -> List[Dict[str, str]]:
    try:
        payload = json.loads(raw_items)
    except json.JSONDecodeError as exc:
        raise CliError("items-json must be valid JSON.") from exc

    if not isinstance(payload, list):
        raise CliError("items-json must be a JSON array.")
    if not payload and not allow_empty:
        raise CliError("items-json must be a non-empty JSON array.")

    return [normalize_item(item, index) for index, item in enumerate(payload, start=1)]


def row_to_entry(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "id": row["id"],
        "date": row["work_date"],
        "task": row["task"],
        "status": row["status"],
        "details": row["details"],
        "created_at": row["created_at"],
    }


def history_row_to_version(row: sqlite3.Row) -> Dict[str, Any]:
    return {
        "history_id": row["history_id"],
        "entry_id": row["entry_id"],
        "version": row["version"],
        "action": row["action"],
        "source_command": row["source_command"],
        "date": row["work_date"],
        "task": row["task"],
        "status": row["status"],
        "details": row["details"],
        "created_at": row["created_at"],
        "changed_at": row["changed_at"],
    }


def fetch_entry_row(connection: sqlite3.Connection, entry_id: int) -> sqlite3.Row:
    row = connection.execute(
        """
        SELECT id, work_date, task, status, details, created_at
        FROM work_entries
        WHERE id = ?
        """,
        (entry_id,),
    ).fetchone()
    if row is None:
        raise CliError("Entry id {0} was not found.".format(entry_id))
    return row


def status_counts(entries: Iterable[Dict[str, Any]]) -> Dict[str, int]:
    counter = Counter(entry["status"] for entry in entries)
    return {status: counter.get(status, 0) for status in STATUS_ORDER}


def history_action_counts(versions: Iterable[Dict[str, Any]]) -> Dict[str, int]:
    counter = Counter(version["action"] for version in versions)
    return {action: counter.get(action, 0) for action in HISTORY_ACTIONS}


def next_entry_version(connection: sqlite3.Connection, entry_id: int) -> int:
    row = connection.execute(
        """
        SELECT COALESCE(MAX(version), 0) AS max_version
        FROM work_entry_history
        WHERE entry_id = ?
        """,
        (entry_id,),
    ).fetchone()
    return int(row["max_version"]) + 1


def insert_history_snapshot(
    connection: sqlite3.Connection,
    entry: Dict[str, Any],
    *,
    action: str,
    source_command: str,
    changed_at: Optional[str] = None,
) -> Dict[str, Any]:
    if action not in HISTORY_ACTIONS:
        raise CliError("Unsupported history action: {0}".format(action))
    timestamp = changed_at or now_iso()
    version = next_entry_version(connection, int(entry["id"]))
    connection.execute(
        """
        INSERT INTO work_entry_history (
            entry_id,
            version,
            action,
            source_command,
            work_date,
            task,
            status,
            details,
            created_at,
            changed_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            entry["id"],
            version,
            action,
            source_command,
            entry["date"],
            entry["task"],
            entry["status"],
            entry["details"],
            entry["created_at"],
            timestamp,
        ),
    )
    history_row = connection.execute(
        """
        SELECT history_id, entry_id, version, action, source_command, work_date, task, status, details, created_at, changed_at
        FROM work_entry_history
        WHERE entry_id = ? AND version = ?
        """,
        (entry["id"], version),
    ).fetchone()
    return history_row_to_version(history_row)


def fetch_entries_in_range(
    db_path: Path,
    start_date: date,
    end_date: date,
) -> List[Dict[str, Any]]:
    with connect_db(db_path) as connection:
        rows = connection.execute(
            """
            SELECT id, work_date, task, status, details, created_at
            FROM work_entries
            WHERE work_date BETWEEN ? AND ?
            ORDER BY work_date ASC, created_at ASC, id ASC
            """,
            (start_date.isoformat(), end_date.isoformat()),
        ).fetchall()
    return [row_to_entry(row) for row in rows]


def record_entries(
    db_path: Path,
    work_date: date,
    items: Sequence[Dict[str, str]],
) -> Dict[str, Any]:
    created_at = now_iso()
    inserted_items: List[Dict[str, Any]] = []

    with connect_db(db_path) as connection:
        for item in items:
            cursor = connection.execute(
                """
                INSERT INTO work_entries (work_date, task, status, details, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    work_date.isoformat(),
                    item["task"],
                    item["status"],
                    item["details"],
                    created_at,
                ),
            )
            inserted_items.append(
                {
                    "id": cursor.lastrowid,
                    "date": work_date.isoformat(),
                    "task": item["task"],
                    "status": item["status"],
                    "details": item["details"],
                    "created_at": created_at,
                }
            )
            insert_history_snapshot(
                connection,
                inserted_items[-1],
                action="create",
                source_command="record",
                changed_at=created_at,
            )

    return {
        "command": "record",
        "db_path": str(db_path),
        "date": work_date.isoformat(),
        "recorded": len(inserted_items),
        "items": inserted_items,
    }


def replace_day_entries(
    db_path: Path,
    work_date: date,
    items: Sequence[Dict[str, str]],
) -> Dict[str, Any]:
    created_at = now_iso()
    inserted_items: List[Dict[str, Any]] = []

    with connect_db(db_path) as connection:
        existing_entries = [
            row_to_entry(row)
            for row in connection.execute(
                """
                SELECT id, work_date, task, status, details, created_at
                FROM work_entries
                WHERE work_date = ?
                ORDER BY created_at ASC, id ASC
                """,
                (work_date.isoformat(),),
            ).fetchall()
        ]
        existing_row = connection.execute(
            """
            SELECT COUNT(*) AS entry_count
            FROM work_entries
            WHERE work_date = ?
            """,
            (work_date.isoformat(),),
        ).fetchone()
        previous_entry_count = int(existing_row["entry_count"])

        for entry in existing_entries:
            insert_history_snapshot(
                connection,
                entry,
                action="delete",
                source_command="replace-day",
            )

        connection.execute(
            """
            DELETE FROM work_entries
            WHERE work_date = ?
            """,
            (work_date.isoformat(),),
        )

        for item in items:
            cursor = connection.execute(
                """
                INSERT INTO work_entries (work_date, task, status, details, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    work_date.isoformat(),
                    item["task"],
                    item["status"],
                    item["details"],
                    created_at,
                ),
            )
            inserted_items.append(
                {
                    "id": cursor.lastrowid,
                    "date": work_date.isoformat(),
                    "task": item["task"],
                    "status": item["status"],
                    "details": item["details"],
                    "created_at": created_at,
                }
            )
            insert_history_snapshot(
                connection,
                inserted_items[-1],
                action="create",
                source_command="replace-day",
                changed_at=created_at,
            )

    return {
        "command": "replace-day",
        "db_path": str(db_path),
        "date": work_date.isoformat(),
        "previous_entry_count": previous_entry_count,
        "recorded": len(inserted_items),
        "items": inserted_items,
    }


def update_entry(
    db_path: Path,
    entry_id: int,
    *,
    new_date: Optional[str],
    task: Optional[str],
    status: Optional[str],
    details: Optional[str],
    clear_details: bool,
) -> Dict[str, Any]:
    if details is not None and clear_details:
        raise CliError("Use either --details or --clear-details, not both.")
    if (
        new_date is None
        and task is None
        and status is None
        and details is None
        and not clear_details
    ):
        raise CliError(
            "update-entry requires at least one change: --new-date, --task, --status, --details, or --clear-details."
        )

    with connect_db(db_path) as connection:
        previous_entry = row_to_entry(fetch_entry_row(connection, entry_id))

        updated_date = (
            parse_work_date(new_date).isoformat()
            if new_date is not None
            else previous_entry["date"]
        )
        updated_task = (
            normalize_task_text(task)
            if task is not None
            else previous_entry["task"]
        )
        updated_status = (
            normalize_status_value(status)
            if status is not None
            else previous_entry["status"]
        )
        if clear_details:
            updated_details = ""
        elif details is not None:
            updated_details = details.strip()
        else:
            updated_details = previous_entry["details"]

        connection.execute(
            """
            UPDATE work_entries
            SET work_date = ?, task = ?, status = ?, details = ?
            WHERE id = ?
            """,
            (
                updated_date,
                updated_task,
                updated_status,
                updated_details,
                entry_id,
            ),
        )

        updated_entry = row_to_entry(fetch_entry_row(connection, entry_id))
        history_entry = insert_history_snapshot(
            connection,
            updated_entry,
            action="update",
            source_command="update-entry",
        )

    return {
        "command": "update-entry",
        "db_path": str(db_path),
        "entry_id": entry_id,
        "previous_entry": previous_entry,
        "entry": updated_entry,
        "history_version": history_entry["version"],
    }


def delete_entry(
    db_path: Path,
    entry_id: int,
) -> Dict[str, Any]:
    with connect_db(db_path) as connection:
        deleted_entry = row_to_entry(fetch_entry_row(connection, entry_id))
        history_entry = insert_history_snapshot(
            connection,
            deleted_entry,
            action="delete",
            source_command="delete-entry",
        )
        connection.execute(
            """
            DELETE FROM work_entries
            WHERE id = ?
            """,
            (entry_id,),
        )

    return {
        "command": "delete-entry",
        "db_path": str(db_path),
        "entry_id": entry_id,
        "deleted_entry": deleted_entry,
        "history_version": history_entry["version"],
    }


def build_entry_history(
    db_path: Path,
    entry_id: int,
) -> Dict[str, Any]:
    with connect_db(db_path) as connection:
        history_rows = connection.execute(
            """
            SELECT history_id, entry_id, version, action, source_command, work_date, task, status, details, created_at, changed_at
            FROM work_entry_history
            WHERE entry_id = ?
            ORDER BY version ASC, history_id ASC
            """,
            (entry_id,),
        ).fetchall()
        if not history_rows:
            raise CliError("No history was found for entry id {0}.".format(entry_id))
        current_row = connection.execute(
            """
            SELECT 1
            FROM work_entries
            WHERE id = ?
            """,
            (entry_id,),
        ).fetchone()

    versions = [history_row_to_version(row) for row in history_rows]
    return {
        "command": "entry-history",
        "db_path": str(db_path),
        "entry_id": entry_id,
        "current_exists": current_row is not None,
        "version_count": len(versions),
        "versions": versions,
    }


def build_day_history(
    db_path: Path,
    work_date: date,
) -> Dict[str, Any]:
    with connect_db(db_path) as connection:
        history_rows = connection.execute(
            """
            SELECT history_id, entry_id, version, action, source_command, work_date, task, status, details, created_at, changed_at
            FROM work_entry_history
            WHERE work_date = ?
            ORDER BY entry_id ASC, version ASC, history_id ASC
            """,
            (work_date.isoformat(),),
        ).fetchall()

        grouped_versions: Dict[int, List[Dict[str, Any]]] = {}
        for row in history_rows:
            version = history_row_to_version(row)
            grouped_versions.setdefault(int(version["entry_id"]), []).append(version)

        entries = []
        for entry_id, versions in grouped_versions.items():
            current_row = connection.execute(
                """
                SELECT id, work_date, task, status, details, created_at
                FROM work_entries
                WHERE id = ?
                """,
                (entry_id,),
            ).fetchone()
            entries.append(
                {
                    "entry_id": entry_id,
                    "current_exists": current_row is not None,
                    "current_entry": row_to_entry(current_row) if current_row is not None else None,
                    "version_count": len(versions),
                    "action_counts": history_action_counts(versions),
                    "versions": versions,
                }
            )

    all_versions = [version for entry in entries for version in entry["versions"]]
    return {
        "command": "day-history",
        "db_path": str(db_path),
        "date": work_date.isoformat(),
        "entry_count": len(entries),
        "version_count": len(all_versions),
        "action_counts": history_action_counts(all_versions),
        "entries": entries,
    }


def build_day_report(db_path: Path, work_date: date) -> Dict[str, Any]:
    entries = fetch_entries_in_range(db_path, work_date, work_date)
    return {
        "command": "day-report",
        "db_path": str(db_path),
        "date": work_date.isoformat(),
        "entry_count": len(entries),
        "status_counts": status_counts(entries),
        "entries": entries,
    }


def week_bounds(anchor_date: date) -> Sequence[date]:
    week_start = anchor_date - timedelta(days=anchor_date.weekday())
    week_end = week_start + timedelta(days=6)
    return week_start, week_end


def build_week_report(db_path: Path, anchor_date: date) -> Dict[str, Any]:
    week_start, week_end = week_bounds(anchor_date)
    entries = fetch_entries_in_range(db_path, week_start, week_end)
    grouped_entries = {day.isoformat(): [] for day in iter_week_days(week_start)}
    for entry in entries:
        grouped_entries[entry["date"]].append(entry)

    days = []
    for current_day in iter_week_days(week_start):
        day_entries = grouped_entries[current_day.isoformat()]
        days.append(
            {
                "date": current_day.isoformat(),
                "entry_count": len(day_entries),
                "status_counts": status_counts(day_entries),
                "entries": day_entries,
            }
        )

    return {
        "command": "week-report",
        "db_path": str(db_path),
        "anchor_date": anchor_date.isoformat(),
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "entry_count": len(entries),
        "status_counts": status_counts(entries),
        "days": days,
    }


def iter_week_days(week_start: date) -> Iterable[date]:
    for offset in range(7):
        yield week_start + timedelta(days=offset)


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--db-path",
        default=argparse.SUPPRESS,
        help="Override the full SQLite database path.",
    )
    parser.add_argument(
        "--db-name",
        default=argparse.SUPPRESS,
        help="Database name without path separators.",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=argparse.SUPPRESS,
        help="Pretty-print JSON output.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Record and query daily work reports backed by SQLite."
    )
    add_common_arguments(parser)

    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser("record", help="Insert work items for one day.")
    add_common_arguments(record_parser)
    record_parser.add_argument(
        "--date",
        help="Target day in YYYY-MM-DD format. Defaults to today.",
    )
    record_parser.add_argument(
        "--items-json",
        required=True,
        help="JSON array of string or object items.",
    )

    replace_day_parser = subparsers.add_parser(
        "replace-day",
        help="Replace all entries for one day.",
    )
    add_common_arguments(replace_day_parser)
    replace_day_parser.add_argument(
        "--date",
        required=True,
        help="Target day in YYYY-MM-DD format.",
    )
    replace_day_parser.add_argument(
        "--items-json",
        required=True,
        help="JSON array of string or object items. Use [] to clear the day.",
    )

    update_entry_parser = subparsers.add_parser(
        "update-entry",
        help="Update one existing entry by id.",
    )
    add_common_arguments(update_entry_parser)
    update_entry_parser.add_argument(
        "--entry-id",
        required=True,
        help="Entry id returned by day-report or week-report.",
    )
    update_entry_parser.add_argument(
        "--new-date",
        help="Move this entry to another YYYY-MM-DD date.",
    )
    update_entry_parser.add_argument(
        "--task",
        help="Replace the task text for this entry.",
    )
    update_entry_parser.add_argument(
        "--status",
        help="Replace the status for this entry.",
    )
    update_entry_parser.add_argument(
        "--details",
        help="Replace the details for this entry.",
    )
    update_entry_parser.add_argument(
        "--clear-details",
        action="store_true",
        help="Clear any existing details for this entry.",
    )

    delete_entry_parser = subparsers.add_parser(
        "delete-entry",
        help="Delete one existing entry by id while preserving history.",
    )
    add_common_arguments(delete_entry_parser)
    delete_entry_parser.add_argument(
        "--entry-id",
        required=True,
        help="Entry id returned by day-report or week-report.",
    )

    entry_history_parser = subparsers.add_parser(
        "entry-history",
        help="Read the version history for one entry id.",
    )
    add_common_arguments(entry_history_parser)
    entry_history_parser.add_argument(
        "--entry-id",
        required=True,
        help="Entry id returned by day-report, week-report, or delete-entry.",
    )

    day_report_parser = subparsers.add_parser(
        "day-report",
        help="Read entries for one day.",
    )
    add_common_arguments(day_report_parser)
    day_report_parser.add_argument(
        "--date",
        help="Target day in YYYY-MM-DD format. Defaults to today.",
    )

    day_history_parser = subparsers.add_parser(
        "day-history",
        help="Read version history for one work date.",
    )
    add_common_arguments(day_history_parser)
    day_history_parser.add_argument(
        "--date",
        required=True,
        help="Target work date in YYYY-MM-DD format.",
    )

    week_report_parser = subparsers.add_parser(
        "week-report",
        help="Read the Monday-Sunday week for one anchor date.",
    )
    add_common_arguments(week_report_parser)
    week_report_parser.add_argument(
        "--date",
        help="Anchor day in YYYY-MM-DD format. Defaults to today.",
    )

    return parser


def run_command(arguments: argparse.Namespace) -> Dict[str, Any]:
    db_path = resolve_db_path(
        getattr(arguments, "db_path", None),
        getattr(arguments, "db_name", None),
    )

    if arguments.command == "record":
        return record_entries(
            db_path=db_path,
            work_date=parse_work_date(arguments.date),
            items=parse_items_json(arguments.items_json),
        )
    if arguments.command == "replace-day":
        return replace_day_entries(
            db_path=db_path,
            work_date=parse_work_date(arguments.date),
            items=parse_items_json(arguments.items_json, allow_empty=True),
        )
    if arguments.command == "update-entry":
        return update_entry(
            db_path=db_path,
            entry_id=parse_positive_int(arguments.entry_id, "entry-id"),
            new_date=getattr(arguments, "new_date", None),
            task=getattr(arguments, "task", None),
            status=getattr(arguments, "status", None),
            details=getattr(arguments, "details", None),
            clear_details=getattr(arguments, "clear_details", False),
        )
    if arguments.command == "delete-entry":
        return delete_entry(
            db_path=db_path,
            entry_id=parse_positive_int(arguments.entry_id, "entry-id"),
        )
    if arguments.command == "entry-history":
        return build_entry_history(
            db_path=db_path,
            entry_id=parse_positive_int(arguments.entry_id, "entry-id"),
        )
    if arguments.command == "day-report":
        return build_day_report(
            db_path=db_path,
            work_date=parse_work_date(arguments.date),
        )
    if arguments.command == "day-history":
        return build_day_history(
            db_path=db_path,
            work_date=parse_work_date(arguments.date),
        )
    if arguments.command == "week-report":
        return build_week_report(
            db_path=db_path,
            anchor_date=parse_work_date(arguments.date),
        )

    raise CliError("Unsupported command: {0}".format(arguments.command))


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)

    try:
        result = run_command(arguments)
    except (CliError, sqlite3.Error) as exc:
        print("[ERROR] {0}".format(exc), file=sys.stderr)
        return 1

    json.dump(
        result,
        sys.stdout,
        ensure_ascii=False,
        indent=2 if getattr(arguments, "pretty", False) else None,
    )
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
