# -*- coding: utf-8 -*-
"""task_logs 表：init 幂等、写入与查询（全程隔离数据目录）。"""
from __future__ import annotations

import unittest

from _support import IsolatedDataRoot


class TestDbSmoke(unittest.TestCase):
    def test_init_db_idempotent_and_crud_smoke(self) -> None:
        with IsolatedDataRoot():
            from db import task_logs_repository as tlr
            from db.connection import get_conn, init_db

            init_db()
            init_db()  # 幂等

            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute("SELECT display_name FROM _jiangchang_tables WHERE table_name = 'task_logs'")
                self.assertEqual(cur.fetchone()[0], "任务日志")
            finally:
                conn.close()

            new_id = tlr.save_task_log(
                task_type="demo_task",
                target_id="tgt-1",
                input_id="42",
                input_title="t",
                status="success",
                error_msg=None,
                result_summary=None,
            )
            self.assertIsInstance(new_id, int)
            self.assertGreater(new_id, 0)

            rows = tlr.list_task_logs(limit=10)
            self.assertTrue(any(r[0] == new_id for r in rows))

            row = tlr.get_task_log_by_id(new_id)
            self.assertIsNotNone(row)
            self.assertEqual(int(row[0]), new_id)

            missing = tlr.get_task_log_by_id(999_999)
            self.assertIsNone(missing)


if __name__ == "__main__":
    unittest.main()
