#!/usr/bin/env python3
"""SQLite-backed todo skill for OpenClaw."""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as dt
import json
import os
import pathlib
import sqlite3
import sys
import tempfile
import uuid
from typing import Any, Iterable


CONFIG_VERSION = 1
SCHEMA_VERSION = 1
DEFAULT_TIMEZONE = "Asia/Shanghai"
DEFAULT_DB_NAME = "todos.sqlite3"
DATE_FMT = "%Y-%m-%d"
DATETIME_FMT = "%Y-%m-%dT%H:%M"

STATUS_OPEN = "open"
STATUS_DONE = "done"
STATUS_ARCHIVED = "archived"
ALL_STATUSES = {STATUS_OPEN, STATUS_DONE, STATUS_ARCHIVED}

ERROR_PREFIXES = {
    "validation": "ERR_VALIDATION",
    "not_found": "ERR_NOT_FOUND",
    "storage": "ERR_STORAGE",
    "corruption": "ERR_CORRUPTION",
    "not_initialized": "ERR_NOT_INITIALIZED",
}


class TodoError(Exception):
    def __init__(self, kind: str, message: str, exit_code: int) -> None:
        super().__init__(message)
        self.kind = kind
        self.message = message
        self.exit_code = exit_code


class ValidationError(TodoError):
    def __init__(self, message: str) -> None:
        super().__init__("validation", message, 2)


class NotFoundError(TodoError):
    def __init__(self, message: str) -> None:
        super().__init__("not_found", message, 3)


class StorageError(TodoError):
    def __init__(self, message: str) -> None:
        super().__init__("storage", message, 4)


class CorruptionError(TodoError):
    def __init__(self, message: str) -> None:
        super().__init__("corruption", message, 5)


class NotInitializedError(TodoError):
    def __init__(self, message: str) -> None:
        super().__init__("not_initialized", message, 6)


class StrictArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise ValidationError(message)


@dataclasses.dataclass
class BasePaths:
    skill_root: pathlib.Path
    config_file: pathlib.Path

    @classmethod
    def detect(cls) -> "BasePaths":
        script_path = pathlib.Path(__file__).resolve()
        skill_root = script_path.parent.parent
        return cls(skill_root=skill_root, config_file=skill_root / "config.json")


@dataclasses.dataclass
class RuntimePaths:
    data_dir: pathlib.Path
    db_file: pathlib.Path
    legacy_index_file: pathlib.Path


def now_local() -> dt.datetime:
    return dt.datetime.now().astimezone()


def format_local(value: dt.datetime | None) -> str:
    if value is None:
        return "-"
    return value.astimezone().strftime("%Y-%m-%d %H:%M")


def parse_json_file(path: pathlib.Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise
    except OSError as exc:
        raise StorageError(f"failed reading file: {path}") from exc
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise CorruptionError(f"invalid JSON in {path}") from exc
    if not isinstance(parsed, dict):
        raise CorruptionError(f"{path.name} must contain a JSON object")
    return parsed


def write_json_file(path: pathlib.Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            delete=False,
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as handle:
            temp_path = pathlib.Path(handle.name)
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_path, path)
    except OSError as exc:
        raise StorageError(f"failed writing file: {path}") from exc


def default_config() -> dict[str, Any]:
    return {
        "version": CONFIG_VERSION,
        "initialized": False,
        "data_dir": "",
        "database_name": DEFAULT_DB_NAME,
        "timezone": DEFAULT_TIMEZONE,
    }


def load_config(base: BasePaths) -> dict[str, Any]:
    if not base.config_file.exists():
        return default_config()
    cfg = parse_json_file(base.config_file)
    if not isinstance(cfg.get("version"), int):
        raise CorruptionError("config.json missing integer version")
    if not isinstance(cfg.get("initialized"), bool):
        raise CorruptionError("config.json missing boolean initialized")
    if not isinstance(cfg.get("data_dir"), str):
        raise CorruptionError("config.json missing string data_dir")
    if not isinstance(cfg.get("database_name"), str):
        raise CorruptionError("config.json missing string database_name")
    if not isinstance(cfg.get("timezone"), str):
        raise CorruptionError("config.json missing string timezone")
    return cfg


def save_config(base: BasePaths, cfg: dict[str, Any]) -> None:
    write_json_file(base.config_file, cfg)


def resolve_runtime_paths(base: BasePaths, cfg: dict[str, Any]) -> RuntimePaths:
    configured = cfg.get("data_dir", "").strip()
    if configured:
        data_dir = pathlib.Path(configured).expanduser()
        if not data_dir.is_absolute():
            raise CorruptionError("config.json data_dir must be an absolute path")
    else:
        data_dir = base.skill_root / "data"
    data_dir = data_dir.resolve()
    database_name = cfg.get("database_name", DEFAULT_DB_NAME).strip() or DEFAULT_DB_NAME
    return RuntimePaths(
        data_dir=data_dir,
        db_file=data_dir / database_name,
        legacy_index_file=data_dir / "index.json",
    )


def init_guidance() -> str:
    script = pathlib.Path(__file__).resolve()
    return (
        "skill is not initialized. Confirm a storage directory with one of:\n"
        f"  python3 {script} init --default\n"
        f"  python3 {script} init --data-dir /absolute/existing/path"
    )


def ensure_initialized(cfg: dict[str, Any]) -> None:
    if not cfg.get("initialized"):
        raise NotInitializedError(init_guidance())


def ensure_data_dir_exists(paths: RuntimePaths) -> None:
    if not paths.data_dir.exists():
        raise StorageError(f"configured data directory does not exist: {paths.data_dir}")
    if not paths.data_dir.is_dir():
        raise StorageError(f"configured data path is not a directory: {paths.data_dir}")


def parse_due_value(raw: str) -> dt.datetime:
    clean = raw.strip()
    if not clean:
        raise ValidationError("due value cannot be empty")
    try:
        if len(clean) == 10:
            parsed_date = dt.datetime.strptime(clean, DATE_FMT).date()
            return dt.datetime.combine(parsed_date, dt.time(23, 59), tzinfo=now_local().tzinfo)
        naive = dt.datetime.strptime(clean, DATETIME_FMT)
        return naive.replace(tzinfo=now_local().tzinfo)
    except ValueError as exc:
        raise ValidationError("due must be YYYY-MM-DD or YYYY-MM-DDTHH:MM") from exc


def make_due_end_of_day(day_offset: int) -> dt.datetime:
    base_day = now_local().date() + dt.timedelta(days=day_offset)
    return dt.datetime.combine(base_day, dt.time(23, 59), tzinfo=now_local().tzinfo)


def parse_priority(value: int) -> int:
    if value < 1 or value > 5:
        raise ValidationError("priority must be between 1 and 5")
    return value


def optional_priority(value: int | None) -> int | None:
    if value is None:
        return None
    return parse_priority(value)


def make_todo_id() -> str:
    return f"todo_{uuid.uuid4().hex[:12]}"


def serialize_dt(value: dt.datetime | None) -> str | None:
    if value is None:
        return None
    return value.astimezone().isoformat(timespec="seconds")


def deserialize_dt(value: str | None, field_name: str) -> dt.datetime | None:
    if value is None:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError as exc:
        raise CorruptionError(f"invalid datetime in {field_name}: {value}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=now_local().tzinfo)
    return parsed


def configure_connection(conn: sqlite3.Connection) -> None:
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")


def initialize_storage(paths: RuntimePaths) -> None:
    paths.data_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(paths.db_file)
    try:
        configure_connection(conn)
        migrate_schema(conn)
        import_legacy_data_if_needed(conn, paths)
        conn.commit()
    except sqlite3.Error as exc:
        raise StorageError(f"failed to initialize database: {paths.db_file}") from exc
    finally:
        conn.close()


@contextlib.contextmanager
def db_conn(paths: RuntimePaths) -> Iterable[sqlite3.Connection]:
    ensure_data_dir_exists(paths)
    if not paths.db_file.exists():
        raise NotInitializedError(init_guidance())
    conn = sqlite3.connect(paths.db_file)
    try:
        configure_connection(conn)
        migrate_schema(conn)
        import_legacy_data_if_needed(conn, paths)
        yield conn
        conn.commit()
    except sqlite3.Error as exc:
        conn.rollback()
        raise StorageError(f"database operation failed: {exc}") from exc
    finally:
        conn.close()


def migrate_schema(conn: sqlite3.Connection) -> None:
    current_version = int(conn.execute("PRAGMA user_version").fetchone()[0])
    if current_version > SCHEMA_VERSION:
        raise CorruptionError(
            f"database schema version {current_version} is newer than this skill supports ({SCHEMA_VERSION})"
        )
    migrations = {
        1: """
            CREATE TABLE IF NOT EXISTS todos (
              id TEXT PRIMARY KEY,
              title TEXT NOT NULL,
              content TEXT NOT NULL,
              due_at TEXT,
              priority INTEGER NOT NULL CHECK(priority >= 1 AND priority <= 5),
              status TEXT NOT NULL DEFAULT 'open',
              created_at TEXT NOT NULL,
              updated_at TEXT NOT NULL,
              completed_at TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_todos_status_due ON todos(status, due_at);
            CREATE INDEX IF NOT EXISTS idx_todos_created_at ON todos(created_at DESC);
            CREATE TABLE IF NOT EXISTS meta (
              key TEXT PRIMARY KEY,
              value TEXT NOT NULL
            );
            INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', '1');
        """,
    }
    while current_version < SCHEMA_VERSION:
        target_version = current_version + 1
        conn.executescript(migrations[target_version])
        conn.execute(f"PRAGMA user_version = {target_version}")
        conn.execute(
            "INSERT OR REPLACE INTO meta(key, value) VALUES ('schema_version', ?)",
            (str(target_version),),
        )
        current_version = target_version


def import_legacy_data_if_needed(conn: sqlite3.Connection, paths: RuntimePaths) -> None:
    count = conn.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
    if count > 0 or not paths.legacy_index_file.exists():
        return

    index = parse_json_file(paths.legacy_index_file)
    months = index.get("months")
    if not isinstance(months, list):
        raise CorruptionError("legacy index.json missing months array")

    for month in months:
        if not isinstance(month, str):
            raise CorruptionError("legacy month key must be string")
        month_file = paths.data_dir / f"todos-{month}.json"
        payload = parse_json_file(month_file)
        todos = payload.get("todos")
        if not isinstance(todos, list):
            raise CorruptionError(f"legacy file {month_file.name} missing todos array")
        for item in todos:
            import_legacy_todo(conn, item)

    conn.execute(
        "INSERT OR REPLACE INTO meta(key, value) VALUES ('legacy_imported_at', ?)",
        (serialize_dt(now_local()) or "",),
    )


def import_legacy_todo(conn: sqlite3.Connection, item: Any) -> None:
    if not isinstance(item, dict):
        raise CorruptionError("legacy todo record must be an object")
    todo_id = str(item.get("id") or make_todo_id())
    title = str(item.get("title") or "").strip()
    if not title:
        raise CorruptionError("legacy todo missing title")
    content = str(item.get("note") or "").strip()
    due_at = None
    due_date = item.get("due_date")
    if isinstance(due_date, str) and due_date.strip():
        due_at = serialize_dt(parse_due_value(due_date.strip()))
    status = str(item.get("status") or STATUS_OPEN)
    if status not in ALL_STATUSES:
        status = STATUS_OPEN if status == "canceled" else STATUS_DONE if status == "done" else STATUS_ARCHIVED
    created_at = serialize_dt(deserialize_dt(str(item.get("created_at")), "legacy created_at") or now_local())
    updated_at = serialize_dt(deserialize_dt(str(item.get("updated_at")), "legacy updated_at") or now_local())
    completed_at = updated_at if status == STATUS_DONE else None
    conn.execute(
        """
        INSERT OR IGNORE INTO todos(
          id, title, content, due_at, priority, status, created_at, updated_at, completed_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            todo_id,
            title,
            content,
            due_at,
            3,
            status,
            created_at or serialize_dt(now_local()),
            updated_at or serialize_dt(now_local()),
            completed_at,
        ),
    )


def make_todo_payload(row: sqlite3.Row) -> dict[str, Any]:
    due_at = deserialize_dt(row["due_at"], "todos.due_at")
    created_at = deserialize_dt(row["created_at"], "todos.created_at")
    updated_at = deserialize_dt(row["updated_at"], "todos.updated_at")
    completed_at = deserialize_dt(row["completed_at"], "todos.completed_at")
    return {
        "id": row["id"],
        "title": row["title"],
        "content": row["content"],
        "due_at": serialize_dt(due_at),
        "priority": row["priority"],
        "status": row["status"],
        "created_at": serialize_dt(created_at),
        "updated_at": serialize_dt(updated_at),
        "completed_at": serialize_dt(completed_at),
    }


def format_todo_line(todo: dict[str, Any]) -> str:
    due_text = format_local(deserialize_dt(todo["due_at"], "todo.due_at"))
    stars = "★" * int(todo["priority"])
    return (
        f"[{todo['status'].upper()}] {todo['id']} | {todo['title']} | "
        f"priority={stars} | due={due_text}"
    )


def print_todos(todos: list[dict[str, Any]], data_dir: pathlib.Path, as_json: bool) -> None:
    if as_json:
        print(json.dumps({"data_dir": str(data_dir), "count": len(todos), "todos": todos}, ensure_ascii=False, indent=2))
        return
    if not todos:
        print("No todos matched.")
        print(f"DataDir: {data_dir}")
        return
    for todo in todos:
        print(format_todo_line(todo))
        print(f"  Content: {todo['content']}")
    print(f"DataDir: {data_dir}")


def print_single_todo(todo: dict[str, Any], data_dir: pathlib.Path, as_json: bool) -> None:
    if as_json:
        print(json.dumps({"data_dir": str(data_dir), "todo": todo}, ensure_ascii=False, indent=2))
        return
    print(format_todo_line(todo))
    print(f"  Content: {todo['content']}")
    print(f"  Created: {format_local(deserialize_dt(todo['created_at'], 'todo.created_at'))}")
    print(f"  Updated: {format_local(deserialize_dt(todo['updated_at'], 'todo.updated_at'))}")
    if todo["completed_at"]:
        print(f"  Completed: {format_local(deserialize_dt(todo['completed_at'], 'todo.completed_at'))}")
    print(f"DataDir: {data_dir}")


def fetch_todo_row(conn: sqlite3.Connection, todo_id: str) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        raise NotFoundError(f"todo not found: {todo_id}")
    return row


def insert_todo(
    conn: sqlite3.Connection,
    *,
    title: str,
    content: str,
    priority: int,
    due_at: dt.datetime | None,
) -> dict[str, Any]:
    clean_title = title.strip()
    clean_content = content.strip()
    if not clean_title:
        raise ValidationError("title cannot be empty")
    if not clean_content:
        raise ValidationError("content cannot be empty")
    priority = parse_priority(priority)
    todo_id = make_todo_id()
    now_value = serialize_dt(now_local())
    conn.execute(
        """
        INSERT INTO todos(id, title, content, due_at, priority, status, created_at, updated_at, completed_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL)
        """,
        (
            todo_id,
            clean_title,
            clean_content,
            serialize_dt(due_at),
            priority,
            STATUS_OPEN,
            now_value,
            now_value,
        ),
    )
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        raise StorageError(f"failed to reload todo after insert: {todo_id}")
    return make_todo_payload(row)


def update_todo_fields(
    conn: sqlite3.Connection,
    todo_id: str,
    *,
    title: str | None = None,
    content: str | None = None,
    priority: int | None = None,
    due_at: dt.datetime | None = None,
    clear_due: bool = False,
) -> dict[str, Any]:
    current = make_todo_payload(fetch_todo_row(conn, todo_id))
    next_title = current["title"] if title is None else title.strip()
    next_content = current["content"] if content is None else content.strip()
    next_priority = current["priority"] if priority is None else parse_priority(priority)
    next_due = current["due_at"] if due_at is None else serialize_dt(due_at)
    if clear_due:
        next_due = None
    if not next_title:
        raise ValidationError("title cannot be empty")
    if not next_content:
        raise ValidationError("content cannot be empty")

    now_value = serialize_dt(now_local())
    conn.execute(
        """
        UPDATE todos
        SET title = ?, content = ?, priority = ?, due_at = ?, updated_at = ?
        WHERE id = ?
        """,
        (next_title, next_content, next_priority, next_due, now_value, todo_id),
    )
    return make_todo_payload(fetch_todo_row(conn, todo_id))


def set_todo_status(conn: sqlite3.Connection, todo_id: str, status: str) -> dict[str, Any]:
    if status not in ALL_STATUSES:
        raise ValidationError(f"invalid status: {status}")
    current = make_todo_payload(fetch_todo_row(conn, todo_id))
    now_value = serialize_dt(now_local())
    completed_at = current["completed_at"]
    if status == STATUS_DONE:
        completed_at = now_value
    elif status == STATUS_OPEN:
        completed_at = None
    conn.execute(
        """
        UPDATE todos
        SET status = ?, updated_at = ?, completed_at = ?
        WHERE id = ?
        """,
        (status, now_value, completed_at, todo_id),
    )
    return make_todo_payload(fetch_todo_row(conn, todo_id))


def parse_status_filter(value: str) -> str:
    if value == "all":
        return value
    if value not in ALL_STATUSES:
        raise ValidationError("status must be open, done, archived, or all")
    return value


def parse_day_range(raw: str, field_name: str, *, end_of_day: bool) -> str:
    try:
        parsed = dt.datetime.strptime(raw, DATE_FMT).date()
    except ValueError as exc:
        raise ValidationError(f"{field_name} must be YYYY-MM-DD") from exc
    clock = dt.time.max if end_of_day else dt.time.min
    return serialize_dt(dt.datetime.combine(parsed, clock, tzinfo=now_local().tzinfo)) or ""


def build_list_query(args: argparse.Namespace) -> tuple[str, tuple[Any, ...], bool]:
    clauses = ["1=1"]
    params: list[Any] = []

    status = parse_status_filter(args.status)
    include_archived = args.include_archived or status in {"archived", "all"}
    if status != "all":
        clauses.append("status = ?")
        params.append(status)

    min_priority = optional_priority(args.min_priority)
    max_priority = optional_priority(args.max_priority)
    if min_priority is not None and max_priority is not None and min_priority > max_priority:
        raise ValidationError("--min-priority cannot be greater than --max-priority")
    if min_priority is not None:
        clauses.append("priority >= ?")
        params.append(min_priority)
    if max_priority is not None:
        clauses.append("priority <= ?")
        params.append(max_priority)

    if args.from_date:
        clauses.append("due_at IS NOT NULL AND due_at >= ?")
        params.append(parse_day_range(args.from_date, "--from", end_of_day=False))
    if args.to_date:
        clauses.append("due_at IS NOT NULL AND due_at <= ?")
        params.append(parse_day_range(args.to_date, "--to", end_of_day=True))

    if args.overdue:
        clauses.append("status = ?")
        params.append(STATUS_OPEN)
        clauses.append("due_at IS NOT NULL AND due_at < ?")
        params.append(serialize_dt(now_local()) or "")

    if args.keyword:
        clauses.append("(title LIKE ? OR content LIKE ?)")
        keyword = f"%{args.keyword.strip()}%"
        params.extend([keyword, keyword])

    if args.no_due:
        clauses.append("due_at IS NULL")

    return " AND ".join(clauses), tuple(params), include_archived


def apply_limit(todos: list[dict[str, Any]], limit: int | None) -> list[dict[str, Any]]:
    if limit is None:
        return todos
    if limit <= 0:
        raise ValidationError("--limit must be greater than 0")
    return todos[:limit]


def cmd_show(args: argparse.Namespace, paths: RuntimePaths) -> int:
    with db_conn(paths) as conn:
        todo = make_todo_payload(fetch_todo_row(conn, args.id))
    print_single_todo(todo, paths.data_dir, args.json)
    return 0


def cmd_init(args: argparse.Namespace, base: BasePaths) -> int:
    if args.default and args.data_dir:
        raise ValidationError("use either --default or --data-dir, not both")
    if not args.default and not args.data_dir:
        raise ValidationError("init requires one of --default or --data-dir /absolute/existing/path")

    if args.default:
        data_dir = (base.skill_root / "data").resolve()
        data_dir.mkdir(parents=True, exist_ok=True)
    else:
        candidate = pathlib.Path(args.data_dir).expanduser()
        if not candidate.is_absolute():
            raise ValidationError("--data-dir must be an absolute path")
        if not candidate.exists():
            raise ValidationError("--data-dir must already exist")
        if not candidate.is_dir():
            raise ValidationError("--data-dir must point to a directory")
        data_dir = candidate.resolve()

    cfg = {
        "version": CONFIG_VERSION,
        "initialized": True,
        "data_dir": str(data_dir),
        "database_name": DEFAULT_DB_NAME,
        "timezone": DEFAULT_TIMEZONE,
    }
    save_config(base, cfg)
    initialize_storage(resolve_runtime_paths(base, cfg))
    print("Todo skill initialized.")
    print(f"Config: {base.config_file}")
    print(f"DataDir: {data_dir}")
    return 0


def cmd_show_config(args: argparse.Namespace, base: BasePaths) -> int:
    cfg = load_config(base)
    runtime = resolve_runtime_paths(base, cfg)
    payload = {
        "initialized": cfg["initialized"],
        "data_dir": str(runtime.data_dir),
        "db_file": str(runtime.db_file),
        "timezone": cfg["timezone"],
        "config_file": str(base.config_file),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_add(args: argparse.Namespace, paths: RuntimePaths) -> int:
    due_at = parse_due_value(args.due) if args.due else None
    with db_conn(paths) as conn:
        todo = insert_todo(
            conn,
            title=args.title,
            content=args.content,
            priority=args.priority,
            due_at=due_at,
        )
    print(f"Added: {format_todo_line(todo)}")
    print(f"  Content: {todo['content']}")
    print(f"DataDir: {paths.data_dir}")
    return 0


def cmd_add_today(args: argparse.Namespace, paths: RuntimePaths) -> int:
    args.due = make_due_end_of_day(0).strftime(DATETIME_FMT)
    return cmd_add(args, paths)


def cmd_add_tomorrow(args: argparse.Namespace, paths: RuntimePaths) -> int:
    args.due = make_due_end_of_day(1).strftime(DATETIME_FMT)
    return cmd_add(args, paths)


def fetch_todos(
    conn: sqlite3.Connection,
    *,
    where_clause: str = "1=1",
    params: tuple[Any, ...] = (),
    include_archived: bool = False,
) -> list[dict[str, Any]]:
    status_filter = "" if include_archived else "AND status != 'archived'"
    query = f"""
        SELECT *
        FROM todos
        WHERE {where_clause} {status_filter}
        ORDER BY
          CASE status WHEN 'open' THEN 0 WHEN 'done' THEN 1 ELSE 2 END,
          due_at IS NULL,
          due_at ASC,
          created_at DESC
    """
    rows = conn.execute(query, params).fetchall()
    return [make_todo_payload(row) for row in rows]


def cmd_list_today(args: argparse.Namespace, paths: RuntimePaths) -> int:
    now_value = now_local()
    day_start = dt.datetime.combine(now_value.date(), dt.time.min, tzinfo=now_value.tzinfo)
    day_end = dt.datetime.combine(now_value.date(), dt.time.max, tzinfo=now_value.tzinfo)
    with db_conn(paths) as conn:
        todos = fetch_todos(
            conn,
            where_clause="due_at IS NOT NULL AND due_at >= ? AND due_at <= ?",
            params=(serialize_dt(day_start), serialize_dt(day_end)),
        )
    print_todos(todos, paths.data_dir, args.json)
    return 0


def cmd_list_all(args: argparse.Namespace, paths: RuntimePaths) -> int:
    with db_conn(paths) as conn:
        where_clause, params, include_archived = build_list_query(args)
        todos = fetch_todos(conn, where_clause=where_clause, params=params, include_archived=include_archived)
        todos = apply_limit(todos, args.limit)
    print_todos(todos, paths.data_dir, args.json)
    return 0


def cmd_done(args: argparse.Namespace, paths: RuntimePaths) -> int:
    with db_conn(paths) as conn:
        todo = set_todo_status(conn, args.id, STATUS_DONE)
    print(f"Done: {format_todo_line(todo)}")
    print(f"DataDir: {paths.data_dir}")
    return 0


def cmd_reopen(args: argparse.Namespace, paths: RuntimePaths) -> int:
    with db_conn(paths) as conn:
        todo = set_todo_status(conn, args.id, STATUS_OPEN)
    print(f"Reopened: {format_todo_line(todo)}")
    print(f"DataDir: {paths.data_dir}")
    return 0


def cmd_archive(args: argparse.Namespace, paths: RuntimePaths) -> int:
    with db_conn(paths) as conn:
        todo = set_todo_status(conn, args.id, STATUS_ARCHIVED)
    print(f"Archived: {format_todo_line(todo)}")
    print(f"DataDir: {paths.data_dir}")
    return 0


def cmd_update(args: argparse.Namespace, paths: RuntimePaths) -> int:
    if (
        args.title is None
        and args.content is None
        and args.priority is None
        and args.due is None
        and not args.clear_due
    ):
        raise ValidationError("provide at least one field to update")
    if args.due and args.clear_due:
        raise ValidationError("use either --due or --clear-due, not both")

    due_at = parse_due_value(args.due) if args.due else None
    with db_conn(paths) as conn:
        todo = update_todo_fields(
            conn,
            args.id,
            title=args.title,
            content=args.content,
            priority=args.priority,
            due_at=due_at,
            clear_due=args.clear_due,
        )
    print(f"Updated: {format_todo_line(todo)}")
    print(f"  Content: {todo['content']}")
    print(f"DataDir: {paths.data_dir}")
    return 0


def cmd_stats(args: argparse.Namespace, paths: RuntimePaths) -> int:
    with db_conn(paths) as conn:
        rows = conn.execute(
            """
            SELECT status, COUNT(*) AS count
            FROM todos
            GROUP BY status
            ORDER BY status
            """
        ).fetchall()
        overdue = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM todos
            WHERE status = ? AND due_at IS NOT NULL AND due_at < ?
            """,
            (STATUS_OPEN, serialize_dt(now_local())),
        ).fetchone()["count"]
        due_today = conn.execute(
            """
            SELECT COUNT(*) AS count
            FROM todos
            WHERE due_at IS NOT NULL AND due_at >= ? AND due_at <= ?
            """,
            (
                parse_day_range(now_local().date().strftime(DATE_FMT), "today", end_of_day=False),
                parse_day_range(now_local().date().strftime(DATE_FMT), "today", end_of_day=True),
            ),
        ).fetchone()["count"]
    payload = {row["status"]: row["count"] for row in rows}
    payload["overdue_open"] = overdue
    payload["due_today"] = due_today
    payload["data_dir"] = str(paths.data_dir)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> StrictArgumentParser:
    parser = StrictArgumentParser(prog="todo.py")
    sub = parser.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init", help="confirm and initialize storage directory")
    init_p.add_argument("--default", action="store_true", help="use <skill>/data")
    init_p.add_argument("--data-dir", default=None, help="absolute existing directory path")
    init_p.set_defaults(handler=cmd_init)

    show_cfg_p = sub.add_parser("show-config", help="show current configuration")
    show_cfg_p.set_defaults(handler=cmd_show_config)

    add_p = sub.add_parser("add", help="add a todo")
    add_p.add_argument("--title", required=True)
    add_p.add_argument("--content", required=True)
    add_p.add_argument("--priority", required=True, type=int)
    add_p.add_argument("--due", default=None, help="YYYY-MM-DD or YYYY-MM-DDTHH:MM")
    add_p.set_defaults(handler=cmd_add)

    add_today_p = sub.add_parser("add-today", help="add a todo due today at 23:59")
    add_today_p.add_argument("--title", required=True)
    add_today_p.add_argument("--content", required=True)
    add_today_p.add_argument("--priority", required=True, type=int)
    add_today_p.set_defaults(handler=cmd_add_today)

    add_tomorrow_p = sub.add_parser("add-tomorrow", help="add a todo due tomorrow at 23:59")
    add_tomorrow_p.add_argument("--title", required=True)
    add_tomorrow_p.add_argument("--content", required=True)
    add_tomorrow_p.add_argument("--priority", required=True, type=int)
    add_tomorrow_p.set_defaults(handler=cmd_add_tomorrow)

    list_today_p = sub.add_parser("list-today", help="list todos due today")
    list_today_p.add_argument("--json", action="store_true")
    list_today_p.set_defaults(handler=cmd_list_today)

    show_p = sub.add_parser("show", help="show one todo")
    show_p.add_argument("--id", required=True)
    show_p.add_argument("--json", action="store_true")
    show_p.set_defaults(handler=cmd_show)

    list_all_p = sub.add_parser("list-all", help="list all todos")
    list_all_p.add_argument("--json", action="store_true")
    list_all_p.add_argument("--status", default="all", help="open|done|archived|all")
    list_all_p.add_argument("--min-priority", type=int, default=None)
    list_all_p.add_argument("--max-priority", type=int, default=None)
    list_all_p.add_argument("--from", dest="from_date", default=None, help="filter due_at from YYYY-MM-DD")
    list_all_p.add_argument("--to", dest="to_date", default=None, help="filter due_at to YYYY-MM-DD")
    list_all_p.add_argument("--keyword", default=None, help="search title and content")
    list_all_p.add_argument("--overdue", action="store_true", help="only open overdue todos")
    list_all_p.add_argument("--no-due", action="store_true", help="only todos without due date")
    list_all_p.add_argument("--limit", type=int, default=None)
    list_all_p.add_argument("--include-archived", action="store_true")
    list_all_p.set_defaults(handler=cmd_list_all)

    done_p = sub.add_parser("done", help="mark a todo as done")
    done_p.add_argument("--id", required=True)
    done_p.set_defaults(handler=cmd_done)

    reopen_p = sub.add_parser("reopen", help="reopen a done or archived todo")
    reopen_p.add_argument("--id", required=True)
    reopen_p.set_defaults(handler=cmd_reopen)

    archive_p = sub.add_parser("archive", help="archive a todo without deleting data")
    archive_p.add_argument("--id", required=True)
    archive_p.set_defaults(handler=cmd_archive)

    update_p = sub.add_parser("update", help="update fields on a todo")
    update_p.add_argument("--id", required=True)
    update_p.add_argument("--title", default=None)
    update_p.add_argument("--content", default=None)
    update_p.add_argument("--priority", type=int, default=None)
    update_p.add_argument("--due", default=None, help="YYYY-MM-DD or YYYY-MM-DDTHH:MM")
    update_p.add_argument("--clear-due", action="store_true")
    update_p.set_defaults(handler=cmd_update)

    stats_p = sub.add_parser("stats", help="show todo counts and urgency summary")
    stats_p.set_defaults(handler=cmd_stats)
    return parser


def run() -> int:
    parser = build_parser()
    args = parser.parse_args()
    base = BasePaths.detect()

    try:
        if args.command in {"init", "show-config"}:
            return int(args.handler(args, base))

        cfg = load_config(base)
        ensure_initialized(cfg)
        paths = resolve_runtime_paths(base, cfg)
        return int(args.handler(args, paths))
    except TodoError as exc:
        prefix = ERROR_PREFIXES[exc.kind]
        print(f"{prefix}: {exc.message}", file=sys.stderr)
        return exc.exit_code


if __name__ == "__main__":
    raise SystemExit(run())
