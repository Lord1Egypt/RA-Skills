#!/usr/bin/env python3
"""Safe SQL helper for MySQL/PostgreSQL/SQLite with lint and explain."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sqlite3
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error as urlerror
from urllib import request as urlrequest
from urllib.parse import unquote, urlparse


ALLOWED_START = {"select", "with", "show", "describe", "desc", "explain", "pragma"}
BLOCKED_TOKENS = {
    "insert",
    "update",
    "delete",
    "drop",
    "truncate",
    "alter",
    "create",
    "rename",
    "grant",
    "revoke",
    "replace",
    "merge",
    "call",
    "execute",
    "begin",
    "commit",
    "rollback",
    "set",
    "use",
}


@dataclass
class DsnConfig:
    driver: str
    host: str | None = None
    port: int | None = None
    user: str | None = None
    password: str | None = None
    database: str | None = None
    sqlite_path: str | None = None


class SqlEasyError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safe SQL helper for MySQL/PostgreSQL/SQLite.")
    parser.add_argument("--dsn", default=None, help="Database DSN or use SQL_DSN env var.")
    parser.add_argument("--audit-log", default=None, help="Optional JSONL audit log path.")

    def add_conn_args(sub: argparse.ArgumentParser) -> None:
        # Allow --dsn/--audit-log both before and after subcommand.
        sub.add_argument("--dsn", dest="dsn_sub", default=None, help=argparse.SUPPRESS)
        sub.add_argument("--audit-log", dest="audit_log_sub", default=None, help=argparse.SUPPRESS)

    subparsers = parser.add_subparsers(dest="command", required=True)

    p_tables = subparsers.add_parser("tables", help="List all tables.")
    add_conn_args(p_tables)

    p_desc = subparsers.add_parser("describe", help="Describe table columns.")
    add_conn_args(p_desc)
    p_desc.add_argument("table", help="Table name.")
    p_desc.add_argument("--format", choices=["table", "json"], default="table")

    p_sample = subparsers.add_parser("sample", help="Sample table rows.")
    add_conn_args(p_sample)
    p_sample.add_argument("table", help="Table name.")
    p_sample.add_argument("--limit", type=int, default=20)
    p_sample.add_argument("--format", choices=["table", "json", "csv"], default="table")

    p_lint = subparsers.add_parser("lint", help="Run SQL lint checks.")
    add_conn_args(p_lint)
    p_lint.add_argument("--sql", required=True, help="SQL statement.")
    p_lint.add_argument("--format", choices=["table", "json"], default="table")

    p_explain = subparsers.add_parser("explain", help="Explain SQL execution plan.")
    add_conn_args(p_explain)
    p_explain.add_argument("--sql", required=True, help="SQL statement to explain.")
    p_explain.add_argument("--analyze", action="store_true", help="Use EXPLAIN ANALYZE if supported.")
    p_explain.add_argument("--slow-ms", type=int, default=1500, help="Warn if explain is slow.")
    p_explain.add_argument("--format", choices=["table", "json", "csv"], default="table")

    p_query = subparsers.add_parser("query", help="Run a read-only SQL query.")
    add_conn_args(p_query)
    p_query.add_argument("--sql", required=True, help="SQL statement.")
    p_query.add_argument("--limit", type=int, default=200, help="Auto-limit rows if SQL has no LIMIT.")
    p_query.add_argument("--format", choices=["table", "json", "csv"], default="table")
    p_query.add_argument("--allow-write", action="store_true", help="Disable read-only guard (not recommended).")
    p_query.add_argument("--no-lint", action="store_true", help="Skip lint checks.")
    p_query.add_argument("--strict-lint", action="store_true", help="Fail query if lint warnings exist.")
    p_query.add_argument("--summary", action="store_true", help="Print lightweight result summary.")
    p_query.add_argument("--slow-ms", type=int, default=1500, help="Warn if query is slow.")

    p_ask = subparsers.add_parser("ask", help="Ask in natural language and let AI generate SQL.")
    add_conn_args(p_ask)
    p_ask.add_argument("--q", required=True, help="Natural language question.")
    p_ask.add_argument("--model", default=os.getenv("SQL_EASY_MODEL", "gpt-4o-mini"), help="LLM model name.")
    p_ask.add_argument("--api-key", default=os.getenv("OPENAI_API_KEY", ""), help="LLM API key.")
    p_ask.add_argument("--base-url", default=os.getenv("OPENAI_BASE_URL", "https://api.openai.com"), help="LLM API base URL.")
    p_ask.add_argument("--max-tables", type=int, default=30, help="Max tables included in schema prompt.")
    p_ask.add_argument("--max-columns", type=int, default=12, help="Max columns per table in schema prompt.")
    p_ask.add_argument("--limit", type=int, default=200, help="Auto-limit rows if generated SQL has no LIMIT.")
    p_ask.add_argument("--format", choices=["table", "json", "csv"], default="table")
    p_ask.add_argument("--no-lint", action="store_true", help="Skip lint checks.")
    p_ask.add_argument("--strict-lint", action="store_true", help="Fail query if lint warnings exist.")
    p_ask.add_argument("--summary", action="store_true", help="Print lightweight result summary.")
    p_ask.add_argument("--slow-ms", type=int, default=1500, help="Warn if query is slow.")
    p_ask.add_argument("--dry-run", action="store_true", help="Only print generated SQL, do not execute.")
    p_ask.add_argument("--show-prompt", action="store_true", help="Print schema prompt sent to model.")
    p_ask.add_argument("--allow-write", action="store_true", help="Disable read-only guard (not recommended).")

    p_profile = subparsers.add_parser("profile", help="Show table+column overview.")
    add_conn_args(p_profile)
    p_profile.add_argument("--max-tables", type=int, default=50)
    p_profile.add_argument("--with-count", action="store_true", help="Include COUNT(*) for each table.")
    p_profile.add_argument("--format", choices=["table", "json"], default="table")

    args = parser.parse_args()
    if getattr(args, "dsn_sub", None):
        args.dsn = args.dsn_sub
    if getattr(args, "audit_log_sub", None):
        args.audit_log = args.audit_log_sub
    if not args.dsn:
        args.dsn = os.getenv("SQL_DSN")
    if not args.audit_log:
        args.audit_log = os.getenv("SQL_EASY_AUDIT_LOG", "")
    return args


def parse_dsn(dsn: str | None) -> DsnConfig:
    if not dsn:
        raise SqlEasyError(
            "Missing DSN. Set SQL_DSN or pass --dsn. "
            "PowerShell: $env:SQL_DSN='sqlite:///d:/path/demo.db'"
        )

    if dsn.startswith("sqlite:///"):
        raw_path = dsn[len("sqlite:///") :]
        if raw_path in {"", ":memory:"}:
            path = ":memory:"
        else:
            path = str(Path(unquote(raw_path)).expanduser())
        return DsnConfig(driver="sqlite", sqlite_path=path)

    # Convenience: plain *.db path means SQLite.
    if dsn.endswith(".db") and "://" not in dsn:
        return DsnConfig(driver="sqlite", sqlite_path=str(Path(dsn).expanduser()))

    parsed = urlparse(dsn)
    scheme = parsed.scheme.lower()
    if scheme in {"mysql", "mysql+pymysql"}:
        database = parsed.path.lstrip("/")
        if not parsed.username or not database:
            raise SqlEasyError("MySQL DSN must include username and database, e.g. mysql://u:p@127.0.0.1:3306/db")
        return DsnConfig(
            driver="mysql",
            host=parsed.hostname or "127.0.0.1",
            port=parsed.port or 3306,
            user=unquote(parsed.username),
            password=unquote(parsed.password or ""),
            database=database,
        )

    if scheme in {"postgres", "postgresql", "postgresql+psycopg2", "postgresql+psycopg"}:
        database = parsed.path.lstrip("/")
        if not parsed.username or not database:
            raise SqlEasyError("PostgreSQL DSN needs username and database, e.g. postgres://u:p@127.0.0.1:5432/db")
        return DsnConfig(
            driver="postgres",
            host=parsed.hostname or "127.0.0.1",
            port=parsed.port or 5432,
            user=unquote(parsed.username),
            password=unquote(parsed.password or ""),
            database=database,
        )

    raise SqlEasyError(f"Unsupported DSN scheme: {scheme}. Use mysql://..., postgres://..., or sqlite:///...")


class DbClient:
    def __init__(self, cfg: DsnConfig):
        self.cfg = cfg
        self.dialect = cfg.driver
        self.conn = self._connect()

    def _connect(self):
        if self.cfg.driver == "sqlite":
            assert self.cfg.sqlite_path is not None
            conn = sqlite3.connect(self.cfg.sqlite_path)
            conn.row_factory = sqlite3.Row
            return conn

        if self.cfg.driver == "mysql":
            try:
                import pymysql  # type: ignore
            except ImportError as exc:
                raise SqlEasyError("pymysql is required for MySQL. Install with: pip install pymysql") from exc

            return pymysql.connect(
                host=self.cfg.host,
                port=self.cfg.port,
                user=self.cfg.user,
                password=self.cfg.password,
                database=self.cfg.database,
                charset="utf8mb4",
                autocommit=True,
                cursorclass=pymysql.cursors.DictCursor,
            )

        if self.cfg.driver == "postgres":
            return self._connect_postgres()

        raise SqlEasyError(f"Unknown driver: {self.cfg.driver}")

    def _connect_postgres(self):
        conn_info = {
            "host": self.cfg.host,
            "port": self.cfg.port,
            "user": self.cfg.user,
            "password": self.cfg.password,
            "dbname": self.cfg.database,
        }
        try:
            import psycopg  # type: ignore
            from psycopg.rows import dict_row  # type: ignore
        except ImportError:
            psycopg = None

        if psycopg is not None:
            return psycopg.connect(**conn_info, row_factory=dict_row, autocommit=True)

        try:
            import psycopg2  # type: ignore
            import psycopg2.extras  # type: ignore
        except ImportError as exc:
            raise SqlEasyError(
                "PostgreSQL driver missing. Install one of: pip install psycopg or pip install psycopg2-binary"
            ) from exc

        return psycopg2.connect(cursor_factory=psycopg2.extras.RealDictCursor, **conn_info)

    def close(self) -> None:
        self.conn.close()

    def query(self, sql: str) -> list[dict[str, Any]]:
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
            if cur.description is None:
                return []
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
        finally:
            cur.close()
        if not rows:
            return []
        if isinstance(rows[0], dict):
            return [dict(row) for row in rows]
        return [dict(zip(columns, row)) for row in rows]

    def tables(self) -> list[str]:
        if self.dialect == "sqlite":
            rows = self.query(
                """
                SELECT name
                FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
                """
            )
            return [str(r["name"]) for r in rows]

        if self.dialect == "mysql":
            rows = self.query("SHOW TABLES")
            if not rows:
                return []
            first_key = next(iter(rows[0].keys()))
            return [str(r[first_key]) for r in rows]

        rows = self.query(
            """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_type = 'BASE TABLE'
              AND table_schema NOT IN ('pg_catalog', 'information_schema')
            ORDER BY table_schema, table_name
            """
        )
        names: list[str] = []
        for row in rows:
            schema = str(row["table_schema"])
            table_name = str(row["table_name"])
            names.append(table_name if schema == "public" else f"{schema}.{table_name}")
        return names

    def describe(self, table: str) -> list[dict[str, Any]]:
        ident = quote_ident(table, self.dialect)
        if self.dialect == "sqlite":
            rows = self.query(f"PRAGMA table_info({ident})")
            result: list[dict[str, Any]] = []
            for row in rows:
                result.append(
                    {
                        "Field": row["name"],
                        "Type": row["type"],
                        "Null": "NO" if row["notnull"] else "YES",
                        "Key": "PRI" if row["pk"] else "",
                        "Default": row["dflt_value"],
                        "Extra": "",
                    }
                )
            return result

        if self.dialect == "mysql":
            return self.query(f"DESCRIBE {ident}")

        schema_name, table_name = resolve_postgres_table(self, table)
        schema_lit = sql_literal(schema_name)
        table_lit = sql_literal(table_name)

        pk_rows = self.query(
            f"""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
              ON tc.constraint_name = kcu.constraint_name
             AND tc.table_schema = kcu.table_schema
             AND tc.table_name = kcu.table_name
            WHERE tc.constraint_type = 'PRIMARY KEY'
              AND tc.table_schema = {schema_lit}
              AND tc.table_name = {table_lit}
            """
        )
        pk_columns = {str(r["column_name"]) for r in pk_rows}

        col_rows = self.query(
            f"""
            SELECT
              column_name,
              data_type,
              is_nullable,
              column_default
            FROM information_schema.columns
            WHERE table_schema = {schema_lit}
              AND table_name = {table_lit}
            ORDER BY ordinal_position
            """
        )

        result: list[dict[str, Any]] = []
        for row in col_rows:
            col_name = str(row["column_name"])
            result.append(
                {
                    "Field": col_name,
                    "Type": row["data_type"],
                    "Null": "YES" if str(row["is_nullable"]).upper() == "YES" else "NO",
                    "Key": "PRI" if col_name in pk_columns else "",
                    "Default": row["column_default"],
                    "Extra": "",
                }
            )
        return result

    def sample(self, table: str, limit: int) -> list[dict[str, Any]]:
        ident = quote_ident(table, self.dialect)
        limit = max(1, min(limit, 1000))
        return self.query(f"SELECT * FROM {ident} LIMIT {limit}")

    def count_rows(self, table: str) -> int:
        ident = quote_ident(table, self.dialect)
        rows = self.query(f"SELECT COUNT(*) AS cnt FROM {ident}")
        return int(rows[0]["cnt"]) if rows else 0


def sql_literal(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def split_qualified_name(name: str) -> tuple[str | None, str]:
    parts = [p.strip() for p in name.split(".", 1)]
    if len(parts) == 1:
        return None, parts[0]
    return parts[0], parts[1]


def resolve_postgres_table(client: DbClient, table: str) -> tuple[str, str]:
    schema_name, table_name = split_qualified_name(table)
    if schema_name:
        return schema_name, table_name

    table_lit = sql_literal(table_name)
    rows = client.query(
        f"""
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE'
          AND table_schema NOT IN ('pg_catalog', 'information_schema')
          AND table_name = {table_lit}
        ORDER BY CASE WHEN table_schema = 'public' THEN 0 ELSE 1 END, table_schema
        LIMIT 1
        """
    )
    if not rows:
        raise SqlEasyError(f"Table not found in PostgreSQL: {table_name}")
    return str(rows[0]["table_schema"]), str(rows[0]["table_name"])


def quote_ident(name: str, dialect: str) -> str:
    if not name.strip():
        raise SqlEasyError("Empty identifier.")

    parts = [p.strip() for p in name.split(".")]
    if any(not p for p in parts):
        raise SqlEasyError(f"Invalid identifier: {name}")

    if dialect == "mysql":
        return ".".join(f"`{p.replace('`', '``')}`" for p in parts)
    return ".".join(f'"{p.replace("\"", "\"\"")}"' for p in parts)


def normalize_sql(sql: str) -> str:
    cleaned = sql.strip()
    if not cleaned:
        raise SqlEasyError("SQL is empty.")
    if re.search(r";\s*\S", cleaned):
        raise SqlEasyError("Only one SQL statement is allowed.")
    if cleaned.endswith(";"):
        cleaned = cleaned[:-1].strip()
    return cleaned


def ensure_safe_readonly(sql: str) -> None:
    first = first_token(sql)
    if first not in ALLOWED_START:
        raise SqlEasyError(f"Read-only mode only allows starts with {sorted(ALLOWED_START)}.")

    lowered_tokens = set(re.findall(r"\b[a-z_]+\b", sql.lower()))
    blocked_found = sorted(BLOCKED_TOKENS.intersection(lowered_tokens))
    if blocked_found:
        raise SqlEasyError(f"Blocked keywords in read-only mode: {', '.join(blocked_found)}")


def first_token(sql: str) -> str:
    match = re.match(r"^\s*([a-zA-Z_]+)", sql)
    return match.group(1).lower() if match else ""


def maybe_apply_limit(sql: str, limit: int) -> str:
    if limit <= 0:
        return sql
    lowered = sql.lower()
    first = first_token(sql)
    if first in {"select", "with"} and " limit " not in f" {lowered} ":
        return f"{sql} LIMIT {limit}"
    return sql


def lint_sql(sql: str) -> list[dict[str, str]]:
    normalized = " ".join(sql.strip().split())
    lowered = normalized.lower()
    warnings: list[dict[str, str]] = []
    first = first_token(normalized)

    if re.search(r"\bselect\s+\*", lowered):
        warnings.append(
            {
                "rule": "select-star",
                "severity": "warn",
                "message": "Use explicit columns instead of SELECT *.",
            }
        )

    if first in {"select", "with"} and " limit " not in f" {lowered} ":
        warnings.append(
            {
                "rule": "missing-limit",
                "severity": "warn",
                "message": "No LIMIT found; result set may be too large.",
            }
        )

    if " order by " in f" {lowered} " and " limit " not in f" {lowered} ":
        warnings.append(
            {
                "rule": "order-without-limit",
                "severity": "warn",
                "message": "ORDER BY without LIMIT can trigger expensive sorting.",
            }
        )

    if first in {"select", "with"} and " where " not in f" {lowered} " and " group by " not in f" {lowered} ":
        warnings.append(
            {
                "rule": "missing-filter",
                "severity": "warn",
                "message": "No WHERE/GROUP BY found; likely full table scan.",
            }
        )

    if re.search(r"\bfrom\s+[^,\s]+\s*,\s*[^,\s]+", lowered):
        warnings.append(
            {
                "rule": "implicit-cross-join",
                "severity": "warn",
                "message": "Use explicit JOIN ... ON ... instead of comma joins.",
            }
        )

    if re.search(r"\blike\s+'%[^']*'", lowered):
        warnings.append(
            {
                "rule": "leading-wildcard-like",
                "severity": "warn",
                "message": "LIKE with leading wildcard is usually index-unfriendly.",
            }
        )

    return warnings


def build_explain_sql(base_sql: str, dialect: str, analyze: bool) -> str:
    if dialect == "sqlite":
        return f"EXPLAIN QUERY PLAN {base_sql}"
    if analyze:
        return f"EXPLAIN ANALYZE {base_sql}"
    return f"EXPLAIN {base_sql}"


def build_schema_context(client: DbClient, max_tables: int, max_columns: int) -> str:
    tables = client.tables()[: max(1, max_tables)]
    lines: list[str] = []
    for table in tables:
        try:
            columns = client.describe(table)[: max(1, max_columns)]
        except Exception:
            continue
        fields = []
        for col in columns:
            field = str(col.get("Field", ""))
            col_type = str(col.get("Type", ""))
            fields.append(f"{field}:{col_type}")
        lines.append(f"- {table}({', '.join(fields)})")
    return "\n".join(lines)


def build_nl2sql_prompt(question: str, dialect: str, schema_context: str) -> str:
    return (
        "You are an expert SQL generator.\n"
        "Rules:\n"
        "1) Return ONE read-only SQL statement.\n"
        "2) Prefer explicit columns over SELECT *.\n"
        "3) Use only tables/columns from the provided schema.\n"
        "4) If needed, add sensible WHERE/GROUP BY/ORDER BY.\n"
        "5) Output JSON only with keys: sql, assumptions.\n\n"
        f"SQL dialect: {dialect}\n"
        "Schema:\n"
        f"{schema_context}\n\n"
        f"User request: {question}\n"
    )


def call_openai_chat(prompt: str, model: str, api_key: str, base_url: str) -> str:
    if not api_key:
        raise SqlEasyError(
            "Missing OPENAI_API_KEY. Set environment variable or pass --api-key for `ask` command."
        )
    url = base_url.rstrip("/") + "/v1/chat/completions"
    payload = {
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "Generate safe SQL in JSON output only."},
            {"role": "user", "content": prompt},
        ],
    }
    body = json.dumps(payload).encode("utf-8")
    req = urlrequest.Request(
        url=url,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urlrequest.urlopen(req, timeout=60) as resp:
            resp_payload = json.loads(resp.read().decode("utf-8"))
    except urlerror.HTTPError as exc:
        err_text = exc.read().decode("utf-8", errors="replace")
        raise SqlEasyError(f"LLM API HTTP {exc.code}: {err_text}") from exc
    except urlerror.URLError as exc:
        raise SqlEasyError(f"LLM API connection failed: {exc}") from exc

    choices = resp_payload.get("choices") or []
    if not choices:
        raise SqlEasyError("LLM response has no choices.")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if isinstance(content, str):
        return content
    # Some providers return structured content arrays.
    if isinstance(content, list):
        text_parts = [str(part.get("text", "")) for part in content if isinstance(part, dict)]
        return "".join(text_parts)
    raise SqlEasyError("LLM response content is empty.")


def extract_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if stripped.startswith("{") and stripped.endswith("}"):
        try:
            obj = json.loads(stripped)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        candidate = fenced.group(1)
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass

    # Fallback: first {...} block
    generic = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if generic:
        try:
            obj = json.loads(generic.group(0))
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            return None
    return None


def parse_llm_sql_response(raw_text: str) -> tuple[str, list[str]]:
    obj = extract_json_object(raw_text)
    if obj:
        sql = str(obj.get("sql", "")).strip()
        assumptions_raw = obj.get("assumptions", [])
        assumptions = [str(x) for x in assumptions_raw] if isinstance(assumptions_raw, list) else []
        if sql:
            return sql, assumptions

    sql_block = re.search(r"```sql\s*(.*?)```", raw_text, flags=re.DOTALL | re.IGNORECASE)
    if sql_block:
        sql = sql_block.group(1).strip()
        if sql:
            return sql, []

    compact = raw_text.strip()
    if compact.lower().startswith("select ") or compact.lower().startswith("with "):
        return compact, []
    raise SqlEasyError("Failed to parse SQL from model response.")


def generate_sql_from_question(
    client: DbClient,
    question: str,
    model: str,
    api_key: str,
    base_url: str,
    max_tables: int,
    max_columns: int,
) -> tuple[str, list[str], str]:
    schema_context = build_schema_context(client, max_tables=max_tables, max_columns=max_columns)
    if not schema_context.strip():
        raise SqlEasyError("Schema discovery returned empty result; cannot generate SQL safely.")
    prompt = build_nl2sql_prompt(question=question, dialect=client.dialect, schema_context=schema_context)
    raw = call_openai_chat(prompt=prompt, model=model, api_key=api_key, base_url=base_url)
    sql_text, assumptions = parse_llm_sql_response(raw)
    return sql_text, assumptions, prompt


def timed_query(client: DbClient, sql: str) -> tuple[list[dict[str, Any]], int]:
    started = time.perf_counter()
    rows = client.query(sql)
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    return rows, elapsed_ms


def summarize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not rows:
        return []

    summary: list[dict[str, Any]] = []
    total_rows = len(rows)
    for column in rows[0].keys():
        values = [r.get(column) for r in rows]
        non_null = [v for v in values if v is not None]
        null_count = total_rows - len(non_null)
        item: dict[str, Any] = {
            "column": column,
            "type": infer_type(non_null),
            "null_pct": f"{(null_count / total_rows) * 100:.1f}%",
            "distinct": len({str(v) for v in non_null}),
            "min": "",
            "max": "",
            "avg": "",
            "sample": "",
        }

        if item["type"] == "number" and non_null:
            nums = [float(v) for v in non_null]
            item["min"] = format_number(min(nums))
            item["max"] = format_number(max(nums))
            item["avg"] = format_number(sum(nums) / len(nums))
        elif item["type"] == "datetime" and non_null:
            dt_values = [coerce_datetime(v) for v in non_null]
            dt_values = [d for d in dt_values if d is not None]
            if dt_values:
                item["min"] = min(dt_values).isoformat(sep=" ", timespec="seconds")
                item["max"] = max(dt_values).isoformat(sep=" ", timespec="seconds")
        elif non_null:
            item["sample"] = shorten(str(non_null[0]), 36)

        summary.append(item)
    return summary


def infer_type(values: list[Any]) -> str:
    if not values:
        return "unknown"
    if all(is_numeric(v) for v in values):
        return "number"
    if all(coerce_datetime(v) is not None for v in values):
        return "datetime"
    return "text"


def is_numeric(value: Any) -> bool:
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, str):
        return re.fullmatch(r"-?\d+(\.\d+)?", value.strip()) is not None
    return False


def coerce_datetime(value: Any) -> dt.datetime | None:
    if isinstance(value, dt.datetime):
        return value
    if isinstance(value, dt.date):
        return dt.datetime.combine(value, dt.time())
    if not isinstance(value, str):
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        return dt.datetime.fromisoformat(text)
    except ValueError:
        return None


def format_number(value: float) -> str:
    if abs(value) >= 1000:
        return f"{value:,.2f}"
    return f"{value:.4f}".rstrip("0").rstrip(".")


def shorten(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    return text[: width - 3] + "..."


def print_rows(rows: list[dict[str, Any]], fmt: str) -> None:
    if fmt == "json":
        print(json.dumps(rows, ensure_ascii=False, indent=2, default=str))
        return

    if fmt == "csv":
        if not rows:
            return
        writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
        return

    print(render_table(rows))


def render_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "(0 rows)"

    columns = list(rows[0].keys())
    widths: dict[str, int] = {}
    for col in columns:
        max_cell = max(len(cell_to_text(row.get(col))) for row in rows)
        widths[col] = min(40, max(len(col), max_cell))

    def trunc(value: str, width: int) -> str:
        if len(value) <= width:
            return value
        return value[: width - 3] + "..."

    header = " | ".join(trunc(col, widths[col]).ljust(widths[col]) for col in columns)
    sep = "-+-".join("-" * widths[col] for col in columns)
    body = []
    for row in rows:
        line = " | ".join(trunc(cell_to_text(row.get(col)), widths[col]).ljust(widths[col]) for col in columns)
        body.append(line)

    return "\n".join([header, sep, *body, f"({len(rows)} rows)"])


def cell_to_text(v: Any) -> str:
    if v is None:
        return "NULL"
    return str(v)


def dsn_label(cfg: DsnConfig) -> str:
    if cfg.driver == "sqlite":
        return cfg.sqlite_path or ":memory:"
    return f"{cfg.driver}://{cfg.host}:{cfg.port}/{cfg.database}"


def write_audit_log(path: str, event: dict[str, Any]) -> None:
    if not path:
        return
    try:
        target = Path(path).expanduser()
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = dict(event)
        payload["timestamp"] = dt.datetime.now(dt.timezone.utc).isoformat()
        with target.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, ensure_ascii=False, default=str))
            fh.write("\n")
    except OSError as exc:
        print(f"[sql_easy] failed to write audit log: {exc}", file=sys.stderr)


def run() -> int:
    args = parse_args()
    cfg = parse_dsn(args.dsn)
    client = DbClient(cfg)
    audit_event: dict[str, Any] = {
        "command": args.command,
        "dialect": cfg.driver,
        "target": dsn_label(cfg),
        "status": "ok",
    }

    try:
        if args.command == "tables":
            rows = [{"table": t} for t in client.tables()]
            print_rows(rows, "table")
            audit_event["row_count"] = len(rows)
            return 0

        if args.command == "describe":
            rows = client.describe(args.table)
            print_rows(rows, args.format)
            audit_event["table"] = args.table
            audit_event["row_count"] = len(rows)
            return 0

        if args.command == "sample":
            rows = client.sample(args.table, args.limit)
            print_rows(rows, args.format)
            audit_event["table"] = args.table
            audit_event["row_count"] = len(rows)
            return 0

        if args.command == "lint":
            sql = normalize_sql(args.sql)
            warnings = lint_sql(sql)
            print_rows(warnings, args.format)
            audit_event["lint_warnings"] = len(warnings)
            return 0

        if args.command == "explain":
            sql = normalize_sql(args.sql)
            ensure_safe_readonly(sql)
            explain_sql = build_explain_sql(sql, client.dialect, args.analyze)
            rows, elapsed_ms = timed_query(client, explain_sql)
            print_rows(rows, args.format)
            if elapsed_ms >= args.slow_ms:
                print(
                    f"[sql_easy] slow explain detected: {elapsed_ms}ms >= {args.slow_ms}ms",
                    file=sys.stderr,
                )
            audit_event["elapsed_ms"] = elapsed_ms
            audit_event["row_count"] = len(rows)
            return 0

        if args.command == "query":
            sql = normalize_sql(args.sql)
            if not args.allow_write:
                ensure_safe_readonly(sql)

            sql = maybe_apply_limit(sql, args.limit)
            warnings: list[dict[str, str]] = []
            if not args.no_lint:
                warnings = lint_sql(sql)
                if warnings:
                    print("[sql_easy] lint warnings:", file=sys.stderr)
                    print(render_table(warnings), file=sys.stderr)

            if args.strict_lint and warnings:
                raise SqlEasyError("Lint warnings found in strict mode. Fix SQL or disable --strict-lint.")

            rows, elapsed_ms = timed_query(client, sql)
            print_rows(rows, args.format)

            if args.summary:
                summary_rows = summarize_rows(rows)
                if args.format == "table":
                    print("\n-- summary --")
                    print(render_table(summary_rows))
                else:
                    print("[sql_easy] summary:", file=sys.stderr)
                    print(json.dumps(summary_rows, ensure_ascii=False, indent=2, default=str), file=sys.stderr)

            if elapsed_ms >= args.slow_ms:
                print(
                    f"[sql_easy] slow query detected: {elapsed_ms}ms >= {args.slow_ms}ms",
                    file=sys.stderr,
                )

            audit_event["elapsed_ms"] = elapsed_ms
            audit_event["lint_warnings"] = len(warnings)
            audit_event["row_count"] = len(rows)
            return 0

        if args.command == "ask":
            question = args.q.strip()
            if not question:
                raise SqlEasyError("Question is empty.")

            sql_from_model, assumptions, prompt = generate_sql_from_question(
                client=client,
                question=question,
                model=args.model,
                api_key=args.api_key,
                base_url=args.base_url,
                max_tables=args.max_tables,
                max_columns=args.max_columns,
            )

            sql = normalize_sql(sql_from_model)
            if not args.allow_write:
                ensure_safe_readonly(sql)
            sql = maybe_apply_limit(sql, args.limit)

            print("-- generated sql --")
            print(sql)
            if assumptions:
                print("\n-- assumptions --")
                for idx, item in enumerate(assumptions, start=1):
                    print(f"{idx}. {item}")
            if args.show_prompt:
                print("\n-- llm prompt --")
                print(prompt)

            warnings = [] if args.no_lint else lint_sql(sql)
            if warnings:
                print("\n[sql_easy] lint warnings:", file=sys.stderr)
                print(render_table(warnings), file=sys.stderr)

            if args.strict_lint and warnings:
                raise SqlEasyError("Lint warnings found in strict mode. Fix SQL or disable --strict-lint.")

            audit_event["generated_sql"] = sql
            audit_event["lint_warnings"] = len(warnings)
            if assumptions:
                audit_event["assumptions"] = assumptions

            if args.dry_run:
                return 0

            rows, elapsed_ms = timed_query(client, sql)
            print("\n-- result --")
            print_rows(rows, args.format)

            if args.summary:
                summary_rows = summarize_rows(rows)
                if args.format == "table":
                    print("\n-- summary --")
                    print(render_table(summary_rows))
                else:
                    print("[sql_easy] summary:", file=sys.stderr)
                    print(json.dumps(summary_rows, ensure_ascii=False, indent=2, default=str), file=sys.stderr)

            if elapsed_ms >= args.slow_ms:
                print(
                    f"[sql_easy] slow query detected: {elapsed_ms}ms >= {args.slow_ms}ms",
                    file=sys.stderr,
                )

            audit_event["elapsed_ms"] = elapsed_ms
            audit_event["row_count"] = len(rows)
            return 0

        if args.command == "profile":
            table_names = client.tables()[: args.max_tables]
            profile_rows: list[dict[str, Any]] = []
            for table in table_names:
                columns = client.describe(table)
                col_names = [str(c.get("Field", "")) for c in columns]
                row = {
                    "table": table,
                    "columns": len(col_names),
                    "column_list": ", ".join(col_names[:8]) + (" ..." if len(col_names) > 8 else ""),
                }
                if args.with_count:
                    row["row_count"] = client.count_rows(table)
                profile_rows.append(row)
            print_rows(profile_rows, args.format)
            audit_event["row_count"] = len(profile_rows)
            return 0

        raise SqlEasyError(f"Unsupported command: {args.command}")
    except Exception as exc:
        audit_event["status"] = "error"
        audit_event["error"] = str(exc)
        raise
    finally:
        client.close()
        write_audit_log(args.audit_log, audit_event)


def main() -> None:
    try:
        code = run()
    except SqlEasyError as exc:
        print(f"[sql_easy] {exc}", file=sys.stderr)
        raise SystemExit(2) from exc
    except KeyboardInterrupt:
        print("[sql_easy] interrupted", file=sys.stderr)
        raise SystemExit(130)
    raise SystemExit(code)


if __name__ == "__main__":
    main()
