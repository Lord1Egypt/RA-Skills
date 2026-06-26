#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

DB_ENV_VAR = "TODO_LIST_DB_PATH"
DEFAULT_DB_PATH = Path("~/.work_report_summary/todo_list.db").expanduser()
STATUSES = ("pending", "in_progress", "completed", "archived")
ACTIVE_STATUSES = ("pending", "in_progress", "completed")
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    details TEXT NOT NULL DEFAULT '',
    planned_amount REAL NOT NULL CHECK (planned_amount > 0),
    done_amount REAL NOT NULL DEFAULT 0 CHECK (done_amount >= 0),
    unit TEXT NOT NULL DEFAULT 'items',
    status TEXT NOT NULL CHECK (status IN ('pending', 'in_progress', 'completed', 'archived')),
    progress_note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT,
    archived_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_tasks_status_updated_at
ON tasks (status, updated_at DESC);
"""


class TodoError(RuntimeError):
    """Raised for user-facing CLI errors."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_number(value: Any) -> Any:
    if value is None:
        return None
    number = float(value)
    if number.is_integer():
        return int(number)
    return round(number, 4)


def format_number(value: Any) -> str:
    normalized = normalize_number(value)
    return str(normalized)


def resolve_db_path(explicit_path: str | None) -> Path:
    raw_path = explicit_path or os.environ.get(DB_ENV_VAR) or str(DEFAULT_DB_PATH)
    db_path = Path(raw_path).expanduser()
    if not db_path.is_absolute():
        db_path = Path.cwd() / db_path
    return db_path


def open_connection(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def ensure_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(SCHEMA)


def status_from_amounts(done_amount: float, planned_amount: float) -> str:
    if done_amount <= 0:
        return "pending"
    if done_amount < planned_amount:
        return "in_progress"
    return "completed"


def validate_positive_number(name: str, value: float) -> float:
    if value <= 0:
        raise TodoError(f"{name} must be greater than zero.")
    return value


def validate_non_negative_number(name: str, value: float) -> float:
    if value < 0:
        raise TodoError(f"{name} must be zero or greater.")
    return value


def normalize_title(title: str) -> str:
    normalized = title.strip()
    if not normalized:
        raise TodoError("title must not be empty.")
    return normalized


def row_to_task(row: sqlite3.Row) -> dict[str, Any]:
    task = dict(row)
    planned_amount = float(task["planned_amount"])
    done_amount = float(task["done_amount"])
    task["planned_amount"] = normalize_number(planned_amount)
    task["done_amount"] = normalize_number(done_amount)
    task["progress_percent"] = normalize_number((done_amount / planned_amount) * 100 if planned_amount else 0)
    task["is_completed"] = done_amount >= planned_amount
    task["is_archived"] = task["status"] == "archived"
    return task


def fetch_task(connection: sqlite3.Connection, task_id: int) -> sqlite3.Row:
    row = connection.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise TodoError(f"Task #{task_id} does not exist.")
    return row


def find_tasks_by_title(connection: sqlite3.Connection, title: str) -> list[sqlite3.Row]:
    normalized_title = normalize_title(title)
    rows = connection.execute("SELECT * FROM tasks WHERE title = ? ORDER BY id ASC", (normalized_title,)).fetchall()
    return list(rows)


def resolve_single_task(
    connection: sqlite3.Connection,
    task_id: int | None = None,
    title: str | None = None,
) -> sqlite3.Row:
    if task_id is not None:
        return fetch_task(connection, task_id)
    if title is None:
        raise TodoError("Either task id or title is required.")

    rows = find_tasks_by_title(connection, title)
    if not rows:
        raise TodoError(f'Task titled "{normalize_title(title)}" does not exist.')
    if len(rows) > 1:
        raise TodoError(f'Multiple tasks match title "{normalize_title(title)}". Use --id instead.')
    return rows[0]


def fetch_tasks_by_ids(connection: sqlite3.Connection, task_ids: list[int]) -> list[sqlite3.Row]:
    if not task_ids:
        return []
    placeholders = ", ".join("?" for _ in task_ids)
    query = f"SELECT * FROM tasks WHERE id IN ({placeholders}) ORDER BY id ASC"
    rows = connection.execute(query, task_ids).fetchall()
    return list(rows)


def json_output(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True)


def render_task_line(task: dict[str, Any]) -> str:
    return (
        f"#{task['id']} [{task['status']}] "
        f"{format_number(task['done_amount'])}/{format_number(task['planned_amount'])} "
        f"{task['unit']} - {task['title']}"
    )


def render_text_result(command: str, payload: dict[str, Any]) -> str:
    if "task" in payload:
        task = payload["task"]
        return "\n".join(
            [
                payload.get("message", command.title()),
                render_task_line(task),
                f"DB: {payload['db_path']}",
            ]
        )

    if command == "archive" and "tasks" in payload:
        lines = [payload.get("message", "Archived tasks."), f"Count: {payload['archived_count']}"]
        lines.extend(render_task_line(task) for task in payload["tasks"])
        lines.append(f"DB: {payload['db_path']}")
        return "\n".join(lines)

    if command == "list":
        lines = [f"Tasks ({payload['status_filter']}): {payload['count']}"]
        lines.extend(render_task_line(task) for task in payload["tasks"])
        lines.append(f"DB: {payload['db_path']}")
        return "\n".join(lines)

    if command == "summary":
        counts = payload["counts"]
        totals = payload["totals"]
        return "\n".join(
            [
                f"Summary scope: {payload['scope']}",
                (
                    "Counts: pending={pending} in_progress={in_progress} "
                    "completed={completed} archived={archived}"
                ).format(**counts),
                (
                    f"Amounts: {format_number(totals['done_amount'])}/"
                    f"{format_number(totals['planned_amount'])} "
                    f"({format_number(totals['completion_percent'])}%)"
                ),
                f"DB: {payload['db_path']}",
            ]
        )

    return payload.get("message", command.title())


def add_task(connection: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    title = normalize_title(args.title)

    planned_amount = validate_positive_number("planned_amount", args.planned_amount)
    done_amount = validate_non_negative_number("done_amount", args.done_amount)
    timestamp = utc_now()
    status = status_from_amounts(done_amount, planned_amount)
    completed_at = timestamp if status == "completed" else None

    cursor = connection.execute(
        """
        INSERT INTO tasks (
            title,
            details,
            planned_amount,
            done_amount,
            unit,
            status,
            progress_note,
            created_at,
            updated_at,
            completed_at,
            archived_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
        """,
        (
            title,
            args.details,
            planned_amount,
            done_amount,
            args.unit,
            status,
            args.note,
            timestamp,
            timestamp,
            completed_at,
        ),
    )
    task = row_to_task(fetch_task(connection, int(cursor.lastrowid)))
    return {
        "db_path": str(resolve_db_path(args.db_path)),
        "message": "Added task.",
        "task": task,
    }


def list_tasks(connection: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    if args.status == "active":
        query = "SELECT * FROM tasks WHERE status IN (?, ?, ?) ORDER BY id ASC"
        params: tuple[Any, ...] = ACTIVE_STATUSES
    elif args.status == "all":
        query = "SELECT * FROM tasks ORDER BY id ASC"
        params = ()
    else:
        query = "SELECT * FROM tasks WHERE status = ? ORDER BY id ASC"
        params = (args.status,)

    rows = connection.execute(query, params).fetchall()
    tasks = [row_to_task(row) for row in rows]
    return {
        "count": len(tasks),
        "db_path": str(resolve_db_path(args.db_path)),
        "status_filter": args.status,
        "tasks": tasks,
    }


def update_progress(connection: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    if all(value is None for value in (args.done_amount, args.increment, args.planned_amount, args.note)):
        raise TodoError("progress requires at least one of --done-amount, --increment, --planned-amount, or --note.")

    existing = fetch_task(connection, args.id)
    if existing["status"] == "archived":
        raise TodoError("Archived tasks cannot be modified.")

    planned_amount = float(existing["planned_amount"])
    done_amount = float(existing["done_amount"])
    completed_at = existing["completed_at"]
    note = existing["progress_note"]

    if args.planned_amount is not None:
        planned_amount = validate_positive_number("planned_amount", args.planned_amount)
    if args.done_amount is not None:
        done_amount = validate_non_negative_number("done_amount", args.done_amount)
    if args.increment is not None:
        done_amount = validate_non_negative_number("done_amount", done_amount + args.increment)
    if args.note is not None:
        note = args.note

    status = status_from_amounts(done_amount, planned_amount)
    timestamp = utc_now()
    if status == "completed":
        completed_at = completed_at or timestamp
    else:
        completed_at = None

    connection.execute(
        """
        UPDATE tasks
        SET planned_amount = ?,
            done_amount = ?,
            status = ?,
            progress_note = ?,
            updated_at = ?,
            completed_at = ?
        WHERE id = ?
        """,
        (planned_amount, done_amount, status, note, timestamp, completed_at, args.id),
    )
    task = row_to_task(fetch_task(connection, args.id))
    return {
        "db_path": str(resolve_db_path(args.db_path)),
        "message": "Updated task progress.",
        "task": task,
    }


def complete_task(connection: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    existing = fetch_task(connection, args.id)
    if existing["status"] == "archived":
        raise TodoError("Archived tasks cannot be completed again.")

    planned_amount = float(existing["planned_amount"])
    done_amount = max(float(existing["done_amount"]), planned_amount)
    timestamp = utc_now()
    completed_at = existing["completed_at"] or timestamp

    connection.execute(
        """
        UPDATE tasks
        SET done_amount = ?,
            status = 'completed',
            updated_at = ?,
            completed_at = ?
        WHERE id = ?
        """,
        (done_amount, timestamp, completed_at, args.id),
    )
    task = row_to_task(fetch_task(connection, args.id))
    return {
        "db_path": str(resolve_db_path(args.db_path)),
        "message": "Marked task complete.",
        "task": task,
    }


def archive_task(connection: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    if args.all_completed:
        rows = connection.execute("SELECT * FROM tasks WHERE status = 'completed' ORDER BY id ASC").fetchall()
        if not rows:
            return {
                "archived_count": 0,
                "db_path": str(resolve_db_path(args.db_path)),
                "message": "No completed tasks to archive.",
                "tasks": [],
            }

        task_ids = [int(row["id"]) for row in rows]
        timestamp = utc_now()
        placeholders = ", ".join("?" for _ in task_ids)
        connection.execute(
            f"""
            UPDATE tasks
            SET status = 'archived',
                updated_at = ?,
                archived_at = ?
            WHERE id IN ({placeholders})
            """,
            [timestamp, timestamp, *task_ids],
        )
        tasks = [row_to_task(row) for row in fetch_tasks_by_ids(connection, task_ids)]
        return {
            "archived_count": len(tasks),
            "db_path": str(resolve_db_path(args.db_path)),
            "message": f"Archived {len(tasks)} completed task(s).",
            "tasks": tasks,
        }

    existing = resolve_single_task(connection, args.id, args.title)
    existing_id = int(existing["id"])
    if existing["status"] == "archived":
        task = row_to_task(existing)
        return {
            "db_path": str(resolve_db_path(args.db_path)),
            "message": "Task was already archived.",
            "task": task,
        }

    timestamp = utc_now()
    connection.execute(
        """
        UPDATE tasks
        SET status = 'archived',
            updated_at = ?,
            archived_at = ?
        WHERE id = ?
        """,
        (timestamp, timestamp, existing_id),
    )
    task = row_to_task(fetch_task(connection, existing_id))
    return {
        "db_path": str(resolve_db_path(args.db_path)),
        "message": "Archived task.",
        "task": task,
    }


def delete_task(connection: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    if not args.confirm:
        raise TodoError("delete requires --confirm because deletion is permanent.")

    existing = resolve_single_task(connection, args.id, args.title)
    task = row_to_task(existing)
    connection.execute("DELETE FROM tasks WHERE id = ?", (existing["id"],))
    task["deleted"] = True
    return {
        "db_path": str(resolve_db_path(args.db_path)),
        "message": "Deleted task.",
        "task": task,
    }


def summarize_tasks(connection: sqlite3.Connection, args: argparse.Namespace) -> dict[str, Any]:
    counts = {status: 0 for status in STATUSES}
    for row in connection.execute("SELECT status, COUNT(*) AS count FROM tasks GROUP BY status").fetchall():
        counts[row["status"]] = int(row["count"])

    if args.include_archived:
        totals_row = connection.execute(
            "SELECT COALESCE(SUM(planned_amount), 0) AS planned_amount, COALESCE(SUM(done_amount), 0) AS done_amount FROM tasks"
        ).fetchone()
        scope = "all"
    else:
        totals_row = connection.execute(
            "SELECT COALESCE(SUM(planned_amount), 0) AS planned_amount, COALESCE(SUM(done_amount), 0) AS done_amount FROM tasks WHERE status IN (?, ?, ?)",
            ACTIVE_STATUSES,
        ).fetchone()
        scope = "active"

    planned_amount = float(totals_row["planned_amount"])
    done_amount = float(totals_row["done_amount"])
    completion_percent = (done_amount / planned_amount) * 100 if planned_amount else 0.0
    return {
        "counts": counts,
        "db_path": str(resolve_db_path(args.db_path)),
        "scope": scope,
        "totals": {
            "planned_amount": normalize_number(planned_amount),
            "done_amount": normalize_number(done_amount),
            "completion_percent": normalize_number(completion_percent),
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track todo items in a local SQLite database.")
    parser.add_argument("--db-path", help=f"Override database path. Default: {DEFAULT_DB_PATH}")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Create a new task.")
    add_parser.add_argument("--title", required=True, help="Task title.")
    add_parser.add_argument("--details", default="", help="Longer task description.")
    add_parser.add_argument("--planned-amount", type=float, default=1.0, help="Target amount of work.")
    add_parser.add_argument("--done-amount", type=float, default=0.0, help="Completed amount at creation time.")
    add_parser.add_argument("--unit", default="items", help="Unit label for planned and done amounts.")
    add_parser.add_argument("--note", default="", help="Initial progress note.")

    list_parser = subparsers.add_parser("list", help="List tasks.")
    list_parser.add_argument(
        "--status",
        choices=("active", "all") + STATUSES,
        default="active",
        help="Which tasks to show.",
    )

    progress_parser = subparsers.add_parser("progress", help="Update task progress.")
    progress_parser.add_argument("--id", type=int, required=True, help="Task id.")
    progress_parser.add_argument("--done-amount", type=float, help="Set the completed amount.")
    progress_parser.add_argument("--increment", type=float, help="Increment the completed amount.")
    progress_parser.add_argument("--planned-amount", type=float, help="Reset the target amount.")
    progress_parser.add_argument("--note", help="Replace the latest progress note.")

    complete_parser = subparsers.add_parser("complete", help="Mark a task complete.")
    complete_parser.add_argument("--id", type=int, required=True, help="Task id.")

    archive_parser = subparsers.add_parser("archive", help="Archive a task.")
    archive_selector = archive_parser.add_mutually_exclusive_group(required=True)
    archive_selector.add_argument("--id", type=int, help="Task id.")
    archive_selector.add_argument("--title", help="Exact task title.")
    archive_selector.add_argument("--all-completed", action="store_true", help="Archive all completed tasks.")

    delete_parser = subparsers.add_parser("delete", help="Delete a task permanently.")
    delete_selector = delete_parser.add_mutually_exclusive_group(required=True)
    delete_selector.add_argument("--id", type=int, help="Task id.")
    delete_selector.add_argument("--title", help="Exact task title.")
    delete_parser.add_argument("--confirm", action="store_true", help="Confirm permanent deletion.")

    summary_parser = subparsers.add_parser("summary", help="Summarize current totals.")
    summary_parser.add_argument("--include-archived", action="store_true", help="Include archived tasks in totals.")

    return parser


def run_command(args: argparse.Namespace) -> dict[str, Any]:
    db_path = resolve_db_path(args.db_path)
    try:
        with open_connection(db_path) as connection:
            ensure_schema(connection)
            if args.command == "add":
                payload = add_task(connection, args)
            elif args.command == "list":
                payload = list_tasks(connection, args)
            elif args.command == "progress":
                payload = update_progress(connection, args)
            elif args.command == "complete":
                payload = complete_task(connection, args)
            elif args.command == "archive":
                payload = archive_task(connection, args)
            elif args.command == "delete":
                payload = delete_task(connection, args)
            elif args.command == "summary":
                payload = summarize_tasks(connection, args)
            else:
                raise TodoError(f"Unsupported command: {args.command}")
            connection.commit()
            return payload
    except sqlite3.Error as exc:
        raise TodoError(f"SQLite error: {exc}") from exc


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        payload = run_command(args)
    except TodoError as exc:
        if getattr(args, "json", False):
            print(json_output({"error": str(exc)}), file=sys.stderr)
        else:
            print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json_output(payload))
    else:
        print(render_text_result(args.command, payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
