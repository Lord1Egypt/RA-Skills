#!/usr/bin/env python3
"""Run MySQL queries with environment-based credentials and read-only defaults."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from typing import Any, Iterable


READ_PREFIXES = (
    "select",
    "show",
    "desc",
    "describe",
    "explain",
    "with",
)

BLOCKED_PATTERNS = (
    r"\bdrop\b",
    r"\btruncate\b",
    r"\bdelete\s+from\s+\S+\s*(;|$)",
    r"\bupdate\s+\S+\s+set\b(?![\s\S]*\bwhere\b)",
)


def load_driver():
    try:
        import pymysql  # type: ignore

        return "pymysql", pymysql
    except ImportError:
        pass

    try:
        import mysql.connector  # type: ignore

        return "mysql.connector", mysql.connector
    except ImportError:
        pass

    raise SystemExit(
        "No Python MySQL driver found. Install pymysql/mysql-connector-python or use the mysql CLI."
    )


def compact_sql(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"--.*?$", " ", sql, flags=re.M)
    return " ".join(sql.strip().split())


def is_read_only(sql: str) -> bool:
    cleaned = compact_sql(sql).lower()
    if not cleaned:
        return False
    return cleaned.startswith(READ_PREFIXES)


def has_blocked_pattern(sql: str) -> str | None:
    cleaned = compact_sql(sql).lower()
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, cleaned, flags=re.I):
            return pattern
    return None


def get_env(name: str, default: str | None = None) -> str | None:
    value = os.environ.get(name)
    return value if value not in (None, "") else default


def connect(args: argparse.Namespace):
    host = args.host or get_env("TEST_MYSQL_HOST")
    port = int(args.port or get_env("TEST_MYSQL_PORT", "3306"))
    user = args.user or get_env("TEST_MYSQL_USER")
    password = args.password or get_env("TEST_MYSQL_PASSWORD")
    database = args.database or get_env("TEST_MYSQL_DATABASE")

    missing = [
        name
        for name, value in (
            ("host", host),
            ("user", user),
            ("password", password),
        )
        if not value
    ]
    if missing:
        raise SystemExit(f"Missing MySQL connection value(s): {', '.join(missing)}")

    driver_name, driver = load_driver()

    if driver_name == "pymysql":
        return driver.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset="utf8mb4",
            cursorclass=driver.cursors.DictCursor,
            connect_timeout=args.connect_timeout,
            read_timeout=args.read_timeout,
            write_timeout=args.write_timeout,
            autocommit=args.autocommit,
        )

    return driver.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        connection_timeout=args.connect_timeout,
        autocommit=args.autocommit,
    )


def print_table(rows: list[dict[str, Any]]) -> None:
    if not rows:
        print("(0 rows)")
        return

    columns = list(rows[0].keys())
    widths = {
        col: max(len(str(col)), *(len(str(row.get(col, ""))) for row in rows))
        for col in columns
    }
    header = " | ".join(str(col).ljust(widths[col]) for col in columns)
    print(header)
    print("-+-".join("-" * widths[col] for col in columns))
    for row in rows:
        print(" | ".join(str(row.get(col, "")).ljust(widths[col]) for col in columns))


def emit_rows(rows: list[dict[str, Any]], fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(rows, ensure_ascii=False, default=str, indent=2))
    elif fmt == "csv":
        if not rows:
            return
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    else:
        print_table(rows)


def fetch_rows(cursor: Any) -> list[dict[str, Any]]:
    if cursor.description is None:
        return []
    rows = cursor.fetchall()
    if isinstance(rows, list):
        return [dict(row) for row in rows]
    return [dict(row) for row in list(rows)]


def iter_statements(sql: str) -> Iterable[str]:
    for statement in sql.split(";"):
        statement = statement.strip()
        if statement:
            yield statement


def main() -> int:
    parser = argparse.ArgumentParser(description="Run MySQL SQL using TEST_MYSQL_* env vars.")
    parser.add_argument("--sql", help="SQL text to execute")
    parser.add_argument("--sql-file", help="Path to a SQL file")
    parser.add_argument("--host")
    parser.add_argument("--port")
    parser.add_argument("--user")
    parser.add_argument("--password")
    parser.add_argument("--database")
    parser.add_argument("--format", choices=("table", "json", "csv"), default="table")
    parser.add_argument("--allow-write", action="store_true")
    parser.add_argument("--autocommit", action="store_true")
    parser.add_argument("--connect-timeout", type=int, default=10)
    parser.add_argument("--read-timeout", type=int, default=30)
    parser.add_argument("--write-timeout", type=int, default=30)
    args = parser.parse_args()

    if args.sql_file:
        with open(args.sql_file, "r", encoding="utf-8") as handle:
            sql = handle.read()
    elif args.sql:
        sql = args.sql
    else:
        sql = sys.stdin.read()

    if not args.allow_write:
        for statement in iter_statements(sql):
            if not is_read_only(statement):
                raise SystemExit("Refusing non-read SQL without --allow-write.")

    blocked = has_blocked_pattern(sql)
    if blocked and not args.allow_write:
        raise SystemExit(f"Refusing broad or destructive SQL pattern: {blocked}")

    conn = connect(args)
    try:
        cursor = conn.cursor()
        last_rows: list[dict[str, Any]] = []
        for statement in iter_statements(sql):
            cursor.execute(statement)
            rows = fetch_rows(cursor)
            if rows:
                last_rows = rows
            elif cursor.rowcount >= 0:
                print(f"affected_rows={cursor.rowcount}")
        if not args.autocommit and args.allow_write:
            conn.commit()
        emit_rows(last_rows, args.format)
    finally:
        conn.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
