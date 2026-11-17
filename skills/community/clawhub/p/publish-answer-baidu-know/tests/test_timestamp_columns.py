# -*- coding: utf-8 -*-
"""标准时间字段：Unix 秒级时间戳、默认值、trigger 与元数据。"""
from __future__ import annotations

import sqlite3
import time
import unittest

from _support import IsolatedDataRoot


class TestTimestampColumns(unittest.TestCase):
    def test_init_db_creates_integer_timestamp_columns_with_defaults(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata import list_physical_column_names
            from db.display_metadata_validator import _table_column_info

            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                physical = list_physical_column_names(cur, "task_logs")
                self.assertEqual(physical[-2:], ["created_at", "updated_at"])

                info = _table_column_info(cur, "task_logs")
                for column_name in ("created_at", "updated_at"):
                    column = info[column_name]
                    self.assertIn("INT", str(column["type"]).upper())
                    self.assertTrue(str(column["dflt_value"]).lower().find("unixepoch") >= 0)
            finally:
                conn.close()

    def test_insert_without_timestamps_auto_generates_unix_seconds(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db

            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                before = int(time.time())
                cur.execute(
                    "INSERT INTO task_logs (task_type, status) VALUES ('auto-ts', 'success')"
                )
                conn.commit()
                cur.execute(
                    "SELECT created_at, updated_at FROM task_logs ORDER BY id DESC LIMIT 1"
                )
                created_at, updated_at = cur.fetchone()
                after = int(time.time())
                self.assertIsInstance(created_at, int)
                self.assertIsInstance(updated_at, int)
                self.assertGreaterEqual(created_at, before)
                self.assertLessEqual(created_at, after)
                self.assertEqual(created_at, updated_at)
            finally:
                conn.close()

    def test_update_business_field_keeps_created_at_and_refreshes_updated_at(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db

            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO task_logs (task_type, status, created_at, updated_at)
                    VALUES ('update-ts', 'success', 1000, 1000)
                    """
                )
                log_id = int(cur.lastrowid)
                conn.commit()

                cur.execute("UPDATE task_logs SET status = 'failed' WHERE id = ?", (log_id,))
                conn.commit()

                cur.execute(
                    "SELECT created_at, updated_at FROM task_logs WHERE id = ?",
                    (log_id,),
                )
                created_at, updated_at = cur.fetchone()
                self.assertEqual(created_at, 1000)
                self.assertGreater(updated_at, 1000)
            finally:
                conn.close()

    def test_reinit_does_not_rewrite_existing_timestamps(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db

            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    INSERT INTO task_logs (task_type, status, created_at, updated_at)
                    VALUES ('stable-ts', 'success', 1234567890, 1234567891)
                    """
                )
                conn.commit()
            finally:
                conn.close()

            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT created_at, updated_at FROM task_logs WHERE task_type = 'stable-ts'"
                )
                self.assertEqual(cur.fetchone(), (1234567890, 1234567891))
            finally:
                conn.close()

    def test_timestamp_metadata_contract(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata import DATETIME_UNIX_SECONDS

            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT column_name, display_name, display_type, editable, display_order
                    FROM _jiangchang_columns
                    WHERE table_name = 'task_logs'
                      AND column_name IN ('created_at', 'updated_at')
                    """
                )
                by_name = {
                    name: (display_name, display_type, editable, display_order)
                    for name, display_name, display_type, editable, display_order in cur.fetchall()
                }
                self.assertEqual(by_name["created_at"][0], "创建时间")
                self.assertEqual(by_name["updated_at"][0], "更新时间")
                self.assertEqual(by_name["created_at"][1], DATETIME_UNIX_SECONDS)
                self.assertEqual(by_name["updated_at"][1], DATETIME_UNIX_SECONDS)
                self.assertEqual(int(by_name["created_at"][2]), 0)
                self.assertEqual(int(by_name["updated_at"][2]), 0)
                self.assertIsNone(by_name["created_at"][3])
                self.assertIsNone(by_name["updated_at"][3])
            finally:
                conn.close()

    def test_metadata_upsert_keeps_timestamp_display_type(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata import DATETIME_UNIX_SECONDS

            init_db()
            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT display_type FROM _jiangchang_columns
                    WHERE table_name = 'task_logs' AND column_name = 'created_at'
                    """
                )
                self.assertEqual(cur.fetchone()[0], DATETIME_UNIX_SECONDS)
            finally:
                conn.close()

    def test_repository_insert_uses_database_timestamps(self) -> None:
        with IsolatedDataRoot():
            from db import task_logs_repository as tlr
            from db.connection import get_conn, init_db

            init_db()
            before = int(time.time())
            new_id = tlr.save_task_log(task_type="repo-ts", status="success")
            after = int(time.time())

            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT created_at, updated_at FROM task_logs WHERE id = ?",
                    (new_id,),
                )
                created_at, updated_at = cur.fetchone()
                self.assertGreaterEqual(int(created_at), before)
                self.assertLessEqual(int(created_at), after)
                self.assertEqual(created_at, updated_at)
            finally:
                conn.close()

    def test_validator_rejects_missing_display_type(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata_validator import validate_template_database

            init_db()
            conn = get_conn()
            try:
                conn.execute(
                    "UPDATE _jiangchang_columns SET display_type = NULL WHERE table_name = 'task_logs' AND column_name = 'created_at'"
                )
                conn.commit()
                report = validate_template_database(conn)
                self.assertFalse(report.ok)
                self.assertTrue(any("display_type" in err for err in report.errors))
            finally:
                conn.close()

    def test_validator_rejects_wrong_timestamp_type(self) -> None:
        conn = sqlite3.connect(":memory:")
        try:
            from db.display_metadata import init_display_metadata
            from db.display_metadata_validator import validate_display_metadata

            conn.executescript(
                """
                CREATE TABLE demo_items (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    created_at TEXT
                );
                """
            )
            init_display_metadata(conn.cursor())
            conn.execute(
                """
                INSERT INTO _jiangchang_tables (table_name, display_name, visible, readonly)
                VALUES ('demo_items', '演示', 1, 0)
                """
            )
            for column_name, display_name in (
                ("id", "编号"),
                ("title", "标题"),
                ("created_at", "创建时间"),
            ):
                conn.execute(
                    """
                    INSERT INTO _jiangchang_columns
                    (table_name, column_name, display_name, visible, searchable, editable, display_type)
                    VALUES ('demo_items', ?, ?, 1, 0, 0, 'datetime_unix_seconds')
                    """,
                    (column_name, display_name),
                )
            conn.commit()
            report = validate_display_metadata(conn)
            self.assertFalse(report.ok)
            self.assertTrue(any("created_at 字段类型应为 INTEGER" in err for err in report.errors))
        finally:
            conn.close()

    def test_validator_rejects_editable_timestamp(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata_validator import validate_template_database

            init_db()
            conn = get_conn()
            try:
                conn.execute(
                    "UPDATE _jiangchang_columns SET editable = 1 WHERE table_name = 'task_logs' AND column_name = 'updated_at'"
                )
                conn.commit()
                report = validate_template_database(conn)
                self.assertFalse(report.ok)
                self.assertTrue(any("editable 应为 0" in err for err in report.errors))
            finally:
                conn.close()

    def test_validator_does_not_flag_amount_as_timestamp(self) -> None:
        conn = sqlite3.connect(":memory:")
        try:
            from db.display_metadata import init_display_metadata
            from db.display_metadata_validator import validate_display_metadata

            conn.executescript(
                """
                CREATE TABLE demo_items (
                    id INTEGER PRIMARY KEY,
                    amount INTEGER,
                    count INTEGER
                );
                """
            )
            init_display_metadata(conn.cursor())
            conn.execute(
                """
                INSERT INTO _jiangchang_tables (table_name, display_name, visible, readonly)
                VALUES ('demo_items', '演示', 1, 0)
                """
            )
            for column_name, display_name in (
                ("id", "编号"),
                ("amount", "数量"),
                ("count", "计数"),
            ):
                conn.execute(
                    """
                    INSERT INTO _jiangchang_columns
                    (table_name, column_name, display_name, visible, searchable, editable)
                    VALUES ('demo_items', ?, ?, 1, 1, 1)
                    """,
                    (column_name, display_name),
                )
            conn.commit()
            report = validate_display_metadata(conn)
            self.assertFalse(any("amount" in err and "display_type" in err for err in report.errors))
            self.assertFalse(any("count" in err and "display_type" in err for err in report.errors))
        finally:
            conn.close()

    def test_trigger_creation_is_idempotent(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.timestamp_columns import TASK_LOGS_UPDATED_AT_TRIGGER, has_updated_at_trigger

            init_db()
            init_db()
            conn = get_conn()
            try:
                self.assertTrue(has_updated_at_trigger(conn.cursor(), "task_logs"))
                cur = conn.cursor()
                cur.execute(
                    "SELECT COUNT(*) FROM sqlite_master WHERE type = 'trigger' AND name = ?",
                    (TASK_LOGS_UPDATED_AT_TRIGGER,),
                )
                self.assertEqual(int(cur.fetchone()[0]), 1)
            finally:
                conn.close()


if __name__ == "__main__":
    unittest.main()
