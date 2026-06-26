#!/usr/bin/env python3
"""
SQL-Audit: Database operation audit trail
Provides identity tracking and SQL logging for compliance purposes.

⚠️  Note: This audit log is stored in a regular database table. It does NOT
    provide cryptographic chaining, signatures, append-only enforcement, or
    external immutable storage. For tamper-evident requirements, implement
    additional controls at the database layer (e.g., triggers, immutable audit).
"""

import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

SKILL_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(SKILL_ROOT))

import yaml

# Safe identifier pattern: alphanumeric + underscore, 1-64 chars
_IDENTIFIER_PATTERN = re.compile(r"^\w{1,64}$")
_VALID_OPERATIONS = frozenset({"SELECT", "INSERT", "UPDATE", "DELETE"})


def _validate_identifier(name: str, field: str) -> str:
    """
    Validate that a string is a safe SQL identifier.
    Raises ValueError if the name contains suspicious characters.
    """
    if not isinstance(name, str):
        raise ValueError(f"{field} must be a string, got {type(name).__name__}")
    if not _IDENTIFIER_PATTERN.match(name):
        raise ValueError(
            f"{field} contains unsafe characters: '{name}'. "
            f"Only alphanumeric characters and underscores are allowed (max 64 chars)."
        )
    return name


class SQLAudit:
    """Audit trail manager for database operations"""

    def __init__(self, config: dict = None, db_connection=None):
        """
        Args:
            config: audit config dict from main config.yaml
            db_connection: active database connection (must be established)
        """
        self.config = config or {}
        self.conn = db_connection
        self._enabled = self.config.get("enabled", False)
        self._log_table = _validate_identifier(
            self.config.get("log_table", "sql_audit_log"), "log_table"
        )
        self._log_select = self.config.get("log_select", False)
        self._mask_values = self.config.get("mask_values", True)
        self._user_info: Dict[str, str] = {}

    def set_user_context(self, user_name: str, user_label: str = "",
                        ip_address: str = "", session_id: str = ""):
        """Set operator identity before each operation"""
        self._user_info = {
            "user_name": user_name or "unknown",
            "user_label": user_label or "",
            "ip_address": ip_address or "",
            "session_id": session_id or "",
        }

    def set_connection(self, conn):
        """Inject active database connection"""
        self.conn = conn

    def is_enabled(self) -> bool:
        return self._enabled

    def get_log_select(self) -> bool:
        """Return whether SELECT statements should be audited."""
        return self._log_select

    def _mask_sql(self, sql: str) -> str:
        """Mask parameter values in SQL to protect sensitive data"""
        if not self._mask_values:
            return sql
        # Replace numeric and string literals with ?
        masked = re.sub(r"'(?:[^'\\]|\\.)*'", "'?'", sql)
        masked = re.sub(r"\b\d+\b", "?", masked)
        return masked

    def _ensure_table(self):
        """Auto-create audit table if not exists"""
        if not self.conn:
            return False
        db_type = self._detect_db_type()
        # log_table already validated as identifier in __init__, safe to interpolate
        log_tbl = self._log_table
        if db_type == "mysql":
            sql = f"""
            CREATE TABLE IF NOT EXISTS {log_tbl} (
                id            BIGINT AUTO_INCREMENT PRIMARY KEY,
                log_time      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                user_name     VARCHAR(128),
                user_label    VARCHAR(128),
                ip_address    VARCHAR(64),
                session_id    VARCHAR(128),
                db_type       VARCHAR(32),
                operation     VARCHAR(16),
                table_name    VARCHAR(128),
                sql_statement TEXT,
                rows_affected INT DEFAULT 0,
                status        VARCHAR(16),
                error_msg     TEXT,
                INDEX idx_user (user_name),
                INDEX idx_log_time (log_time),
                INDEX idx_table (table_name)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """
        elif db_type == "postgres":
            sql = f"""
            CREATE TABLE IF NOT EXISTS {log_tbl} (
                id            BIGSERIAL PRIMARY KEY,
                log_time      TIMESTAMP NOT NULL DEFAULT NOW(),
                user_name     VARCHAR(128),
                user_label    VARCHAR(128),
                ip_address    VARCHAR(64),
                session_id    VARCHAR(128),
                db_type       VARCHAR(32),
                operation     VARCHAR(16),
                table_name    VARCHAR(128),
                sql_statement TEXT,
                rows_affected INT DEFAULT 0,
                status        VARCHAR(16),
                error_msg     TEXT
            )
            CREATE INDEX IF NOT EXISTS idx_audit_user ON {log_tbl}(user_name);
            CREATE INDEX IF NOT EXISTS idx_audit_time ON {log_tbl}(log_time);
            CREATE INDEX IF NOT EXISTS idx_audit_table ON {log_tbl}(table_name);
            """
        elif db_type == "sqlite":
            sql = f"""
            CREATE TABLE IF NOT EXISTS {log_tbl} (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                log_time      TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                user_name     TEXT,
                user_label    TEXT,
                ip_address    TEXT,
                session_id    TEXT,
                db_type       TEXT,
                operation     TEXT,
                table_name    TEXT,
                sql_statement TEXT,
                rows_affected INTEGER DEFAULT 0,
                status        TEXT,
                error_msg     TEXT
            )
            CREATE INDEX IF NOT EXISTS idx_audit_user ON {log_tbl}(user_name);
            CREATE INDEX IF NOT EXISTS idx_audit_time ON {log_tbl}(log_time);
            CREATE INDEX IF NOT EXISTS idx_audit_table ON {log_tbl}(table_name);
            """
        else:
            return False
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print(f"[SQL-Audit] Table creation failed: {e}")
            return False

    def _detect_db_type(self) -> str:
        """Detect database type from connection"""
        conn_type = str(type(self.conn))
        if "mysql" in conn_type:
            return "mysql"
        elif "psycopg" in conn_type or "postgres" in conn_type:
            return "postgres"
        elif "sqlite" in conn_type:
            return "sqlite"
        return "unknown"

    def log(self, operation: str, table_name: str, sql: str,
            rows_affected: int = 0, status: str = "SUCCESS",
            error_msg: str = None):
        """
        Write audit record

        Args:
            operation: SELECT / INSERT / UPDATE / DELETE
            table_name: target table name
            sql: executed SQL statement
            rows_affected: number of rows affected
            status: SUCCESS / FAILED
            error_msg: error message if failed
        """
        if not self._enabled:
            return
        if not self._log_select and operation == "SELECT":
            return
        if not self.conn:
            return

        # Validate operation against allowlist to prevent log injection
        op_upper = operation.upper() if isinstance(operation, str) else ""
        if op_upper not in _VALID_OPERATIONS:
            print(f"[SQL-Audit] Dropped audit record: invalid operation '{operation}'")
            return

        # Validate table_name as safe identifier
        try:
            table_name = _validate_identifier(table_name, "table_name")
        except ValueError:
            print(f"[SQL-Audit] Dropped audit record: unsafe table_name '{table_name}'")
            return

        # Auto-create table on first write
        self._ensure_table()

        sql_masked = self._mask_sql(sql)
        db_type = self._detect_db_type()
        log_tbl = self._log_table  # already validated

        if db_type == "mysql":
            insert_sql = f"""
            INSERT INTO {log_tbl}
            (log_time, user_name, user_label, ip_address, session_id,
             db_type, operation, table_name, sql_statement, rows_affected, status, error_msg)
            VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self._user_info.get("user_name", "unknown"),
                self._user_info.get("user_label", ""),
                self._user_info.get("ip_address", ""),
                self._user_info.get("session_id", ""),
                db_type, op_upper, table_name,
                sql_masked, rows_affected, status, error_msg or ""
            )
        elif db_type == "postgres":
            insert_sql = f"""
            INSERT INTO {log_tbl}
            (log_time, user_name, user_label, ip_address, session_id,
             db_type, operation, table_name, sql_statement, rows_affected, status, error_msg)
            VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self._user_info.get("user_name", "unknown"),
                self._user_info.get("user_label", ""),
                self._user_info.get("ip_address", ""),
                self._user_info.get("session_id", ""),
                db_type, op_upper, table_name,
                sql_masked, rows_affected, status, error_msg or ""
            )
        elif db_type == "sqlite":
            insert_sql = f"""
            INSERT INTO {log_tbl}
            (log_time, user_name, user_label, ip_address, session_id,
             db_type, operation, table_name, sql_statement, rows_affected, status, error_msg)
            VALUES (datetime('now'), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                self._user_info.get("user_name", "unknown"),
                self._user_info.get("user_label", ""),
                self._user_info.get("ip_address", ""),
                self._user_info.get("session_id", ""),
                db_type, op_upper, table_name,
                sql_masked, rows_affected, status, error_msg or ""
            )
        else:
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(insert_sql, params)
            self.conn.commit()
            cursor.close()
        except Exception as e:
            print(f"[SQL-Audit] Write failed: {e}")

    def query_logs(self, user_name: str = None, table_name: str = None,
                   start_time: str = None, end_time: str = None,
                   limit: int = 100) -> list:
        """
        Query audit logs (for compliance review)

        Args:
            user_name: filter by operator
            table_name: filter by target table
            start_time: start datetime (YYYY-MM-DD HH:MM:SS)
            end_time: end datetime (YYYY-MM-DD HH:MM:SS)
            limit: max records returned (capped at 10000 to prevent DoS)
        Returns:
            list of audit records (dict)
        """
        if not self.conn:
            return []

        # ── Strict type enforcement + range clamp for limit ───────────────────
        # Ensures limit is always an integer in a safe range; rejects strings
        # (including injection payloads like "100; DROP TABLE") before any
        # SQL interpolation occurs.
        try:
            limit = int(limit)
        except (TypeError, ValueError):
            raise ValueError(f"limit must be an integer, got {type(limit).__name__}: {limit!r}")
        limit = max(1, min(limit, 10000))  # positive, bounded

        # ── Sanitize all filter values ─────────────────────────────────────────
        if user_name is not None and not isinstance(user_name, str):
            raise ValueError(f"user_name must be a string, got {type(user_name).__name__}")
        if table_name is not None:
            table_name = _validate_identifier(table_name, "table_name")
        # start_time / end_time: basic format guard (YYYY-MM-DD HH:MM:SS or date-only)
        _TIME_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}( \d{2}:\d{2}:\d{2})?$")
        if start_time is not None:
            if not isinstance(start_time, str) or not _TIME_PATTERN.match(start_time):
                raise ValueError(f"start_time has invalid format: {start_time!r}")
        if end_time is not None:
            if not isinstance(end_time, str) or not _TIME_PATTERN.match(end_time):
                raise ValueError(f"end_time has invalid format: {end_time!r}")

        db_type = self._detect_db_type()
        conditions = []
        params = []

        if user_name:
            conditions.append("user_name = %s")
            params.append(user_name)
        if table_name:
            conditions.append("table_name = %s")
            params.append(table_name)
        if start_time:
            conditions.append("log_time >= %s")
            params.append(start_time)
        if end_time:
            conditions.append("log_time <= %s")
            params.append(end_time)

        where_clause = " AND ".join(conditions) if conditions else "1=1"
        # limit is now a guaranteed integer in range [1, 10000] — safe to interpolate
        sql = f"SELECT * FROM {self._log_table} WHERE {where_clause} ORDER BY log_time DESC LIMIT {limit}"

        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(sql, params)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Exception as e:
            print(f"[SQL-Audit] Query failed: {e}")
            return []