# -*- coding: utf-8 -*-
"""数据管理展示元数据：幂等初始化、中文名称、PRAGMA 字段顺序、校验规则。"""
from __future__ import annotations

import sqlite3
import unittest

from _support import IsolatedDataRoot, get_skill_root


class TestDisplayMetadata(unittest.TestCase):
    def test_init_db_metadata_idempotent(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db

            init_db()
            init_db()

            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute("SELECT COUNT(*) FROM _jiangchang_tables WHERE table_name = 'task_logs'")
                self.assertEqual(int(cur.fetchone()[0]), 1)
                cur.execute("SELECT COUNT(*) FROM _jiangchang_columns WHERE table_name = 'task_logs'")
                self.assertEqual(int(cur.fetchone()[0]), 10)
            finally:
                conn.close()

    def test_task_logs_has_chinese_table_and_column_names(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db

            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    "SELECT display_name FROM _jiangchang_tables WHERE table_name = 'task_logs'"
                )
                self.assertEqual(cur.fetchone()[0], "任务日志")

                cur.execute(
                    """
                    SELECT column_name, display_name
                    FROM _jiangchang_columns
                    WHERE table_name = 'task_logs'
                    ORDER BY column_name
                    """
                )
                by_name = dict(cur.fetchall())
                self.assertEqual(by_name["status"], "状态")
                self.assertEqual(by_name["error_msg"], "错误信息")
                self.assertEqual(by_name["created_at"], "创建时间")
            finally:
                conn.close()

    def test_task_logs_physical_order_matches_pragma_cid(self) -> None:
        with IsolatedDataRoot():
            from db.connection import init_db
            from db.display_metadata import TASK_LOGS_COLUMN_METADATA, list_physical_column_names
            from db.connection import get_conn

            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                physical = list_physical_column_names(cur, "task_logs")
                expected = [str(item["column_name"]) for item in TASK_LOGS_COLUMN_METADATA]
                self.assertEqual(
                    physical,
                    expected,
                )
                cur.execute("PRAGMA table_info('task_logs')")
                cid_order = [row[1] for row in sorted(cur.fetchall(), key=lambda row: int(row[0]))]
                self.assertEqual(cid_order, expected)
            finally:
                conn.close()

    def test_init_db_sets_task_logs_display_order_null(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db

            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT column_name, display_order
                    FROM _jiangchang_columns
                    WHERE table_name = 'task_logs'
                    """
                )
                for column_name, display_order in cur.fetchall():
                    self.assertIsNone(
                        display_order,
                        msg=f"{column_name} display_order should be NULL",
                    )
            finally:
                conn.close()

    def test_reinit_clears_stale_display_order(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db

            init_db()
            conn = get_conn()
            try:
                conn.execute(
                    """
                    UPDATE _jiangchang_columns
                    SET display_order = 99
                    WHERE table_name = 'task_logs' AND column_name = 'id'
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
                    """
                    SELECT display_order FROM _jiangchang_columns
                    WHERE table_name = 'task_logs' AND column_name = 'id'
                    """
                )
                self.assertIsNone(cur.fetchone()[0])
            finally:
                conn.close()

    def test_legacy_display_order_does_not_change_pragma_physical_order(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata import list_physical_column_names

            init_db()
            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute(
                    """
                    UPDATE _jiangchang_columns
                    SET display_order = 1
                    WHERE table_name = 'task_logs' AND column_name = 'updated_at'
                    """
                )
                cur.execute(
                    """
                    UPDATE _jiangchang_columns
                    SET display_order = 99
                    WHERE table_name = 'task_logs' AND column_name = 'id'
                    """
                )
                conn.commit()
                physical = list_physical_column_names(cur, "task_logs")
                self.assertEqual(physical[0], "id")
                self.assertEqual(physical[-1], "updated_at")
            finally:
                conn.close()

    def test_metadata_tables_are_not_user_tables(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata import iter_user_tables

            init_db()
            conn = get_conn()
            try:
                tables = list(iter_user_tables(conn.cursor()))
                self.assertEqual(tables, ["task_logs"])
            finally:
                conn.close()

    def test_template_database_validation_passes(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata_validator import validate_template_database

            init_db()
            conn = get_conn()
            try:
                report = validate_template_database(conn)
                self.assertTrue(report.ok, msg="; ".join(report.errors))
            finally:
                conn.close()

    def test_validate_missing_both_metadata_tables(self) -> None:
        conn = sqlite3.connect(":memory:")
        try:
            conn.execute("CREATE TABLE demo_items (id INTEGER PRIMARY KEY, title TEXT)")
            from db.display_metadata_validator import validate_display_metadata

            report = validate_display_metadata(conn)
            self.assertFalse(report.ok)
            self.assertIn("缺少数据管理元数据表 _jiangchang_tables", report.errors)
            self.assertIn("缺少数据管理元数据表 _jiangchang_columns", report.errors)
        finally:
            conn.close()

    def test_validate_missing_jiangchang_tables_only(self) -> None:
        from db.display_metadata import _JIANGCHANG_COLUMNS_DDL
        from db.display_metadata_validator import validate_display_metadata

        conn = sqlite3.connect(":memory:")
        try:
            conn.execute(_JIANGCHANG_COLUMNS_DDL)
            report = validate_display_metadata(conn)
            self.assertFalse(report.ok)
            self.assertIn("缺少数据管理元数据表 _jiangchang_tables", report.errors)
            self.assertNotIn("缺少数据管理元数据表 _jiangchang_columns", report.errors)
        finally:
            conn.close()

    def test_validate_missing_jiangchang_columns_only(self) -> None:
        from db.display_metadata import _JIANGCHANG_TABLES_DDL
        from db.display_metadata_validator import validate_display_metadata

        conn = sqlite3.connect(":memory:")
        try:
            conn.execute(_JIANGCHANG_TABLES_DDL)
            report = validate_display_metadata(conn)
            self.assertFalse(report.ok)
            self.assertIn("缺少数据管理元数据表 _jiangchang_columns", report.errors)
            self.assertNotIn("缺少数据管理元数据表 _jiangchang_tables", report.errors)
        finally:
            conn.close()

    def test_missing_table_metadata_is_reported(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata_validator import validate_display_metadata

            init_db()
            conn = get_conn()
            try:
                conn.execute("CREATE TABLE demo_items (id INTEGER PRIMARY KEY, title TEXT)")
                conn.execute("DELETE FROM _jiangchang_tables WHERE table_name = 'demo_items'")
                conn.commit()
                report = validate_display_metadata(conn)
                self.assertFalse(report.ok)
                self.assertTrue(any("demo_items" in err for err in report.errors))
            finally:
                conn.close()

    def test_missing_column_metadata_is_reported(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata_validator import validate_display_metadata

            init_db()
            conn = get_conn()
            try:
                conn.execute(
                    "DELETE FROM _jiangchang_columns WHERE table_name = 'task_logs' AND column_name = 'status'"
                )
                conn.commit()
                report = validate_display_metadata(conn)
                self.assertFalse(report.ok)
                self.assertTrue(any("task_logs.status" in err for err in report.errors))
            finally:
                conn.close()

    def test_metadata_reference_to_missing_column_is_reported(self) -> None:
        with IsolatedDataRoot():
            from db.connection import get_conn, init_db
            from db.display_metadata_validator import validate_display_metadata

            init_db()
            conn = get_conn()
            try:
                conn.execute(
                    """
                    INSERT INTO _jiangchang_columns
                    (table_name, column_name, display_name, visible, searchable, editable)
                    VALUES ('task_logs', 'not_exists', '不存在', 1, 1, 1)
                    """
                )
                conn.commit()
                report = validate_display_metadata(conn)
                self.assertFalse(report.ok)
                self.assertTrue(any("not_exists" in err for err in report.errors))
            finally:
                conn.close()

    def test_ordering_test_table_not_alphabetized(self) -> None:
        conn = sqlite3.connect(":memory:")
        try:
            conn.executescript(
                """
                CREATE TABLE ordering_test (
                    z_field TEXT,
                    id INTEGER PRIMARY KEY,
                    a_field TEXT,
                    created_at INTEGER,
                    updated_at INTEGER
                );
                """
            )
            from db.display_metadata import list_physical_column_names

            physical = list_physical_column_names(conn.cursor(), "ordering_test")
            self.assertEqual(physical, ["z_field", "id", "a_field", "created_at", "updated_at"])
        finally:
            conn.close()

    def test_skill_frontmatter_validation_for_template(self) -> None:
        from db.display_metadata_validator import validate_skill_frontmatter

        report = validate_skill_frontmatter(get_skill_root(), allow_template_placeholders=True)
        self.assertTrue(report.ok, msg="; ".join(report.errors))

    def test_skill_frontmatter_rejects_english_placeholder_name(self) -> None:
        import os
        import tempfile

        from db.display_metadata_validator import validate_skill_frontmatter

        with tempfile.TemporaryDirectory() as tmp:
            skill_md = """---
name: My Skill
description: demo
metadata:
  openclaw:
    slug: query-demo-info
---
"""
            with open(os.path.join(tmp, "SKILL.md"), "w", encoding="utf-8") as f:
                f.write(skill_md)
            report = validate_skill_frontmatter(tmp, allow_template_placeholders=False)
            self.assertFalse(report.ok)
            self.assertTrue(any("name" in err for err in report.errors))

    def test_column_order_warning_for_created_at_in_middle(self) -> None:
        from db.display_metadata_validator import column_order_warnings

        warnings = column_order_warnings(
            "bad_order",
            ["created_at", "id", "title", "updated_at"],
        )
        self.assertTrue(any("id" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
