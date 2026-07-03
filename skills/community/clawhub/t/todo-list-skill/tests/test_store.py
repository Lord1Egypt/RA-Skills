# todos/tests/test_store.py
# 数据层单元测试（19 个用例）
# 版本：v1.1 | 日期：2026-06-11
# 覆盖：DESIGN.md §九 测试计划（test_store.py）

import json
import os
import tempfile
import unittest
from pathlib import Path

# 隔离：使用临时数据库（通过环境变量）
os.environ["TODOS_DB_PATH"] = tempfile.mktemp(suffix=".db")

# 临时修改 DB_PATH
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# 在 import store 之前覆盖路径
from src import store as store_module
# 注意：store_module 现在会读取 env 变量，这里无需再手动覆盖


class TestStoreBase(unittest.TestCase):
    """测试基类：每个测试用独立数据库"""

    def setUp(self):
        self.db_path = tempfile.mktemp(suffix=".db")
        os.environ["TODOS_DB_PATH"] = self.db_path
        store_module.DB_PATH = self.db_path
        # 重置单例（每个测试用新实例）
        store_module.TodosStore._instance = None
        self.store = store_module.TodosStore()
        self.store.init_db()

    def tearDown(self):
        # 清理数据库文件
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)


class TestAdd(TestStoreBase):
    """add 方法测试（6 个）"""

    def test_add_normal(self):
        """[OK] add 正常写入 + audit_log"""
        todo = self.store.add(content="检查止损", priority="high", tags=["etf"])
        self.assertIsNotNone(todo["id"])
        self.assertEqual(todo["content"], "检查止损")
        self.assertEqual(todo["priority"], "high")
        self.assertEqual(todo["status"], "pending")
        # tags 序列化为 JSON
        self.assertEqual(json.loads(todo["tags"]), ["etf"])
        # active_form 自动生成
        self.assertIn("进行中", todo["active_form"])

    def test_add_empty_content(self):
        """[FAIL] add 空 content -> TodoValidationError"""
        from src.exceptions import TodoValidationError
        with self.assertRaises(TodoValidationError) as ctx:
            self.store.add(content="")
        self.assertIn("不能为空", str(ctx.exception))

        with self.assertRaises(TodoValidationError):
            self.store.add(content="   ")

    def test_add_content_too_long(self):
        """[FAIL] add 超长 content -> TodoValidationError"""
        from src.exceptions import TodoValidationError
        with self.assertRaises(TodoValidationError) as ctx:
            self.store.add(content="x" * 501)
        self.assertIn("超过 500 字符", str(ctx.exception))

    def test_add_invalid_priority(self):
        """[NEW] add 非法 priority -> TodoValidationError（友好错误，不抛 IntegrityError）"""
        from src.exceptions import TodoValidationError
        with self.assertRaises(TodoValidationError) as ctx:
            self.store.add(content="测试", priority="urgent")
        self.assertIn("priority 必须是", str(ctx.exception))
        self.assertIn("urgent", str(ctx.exception))

    def test_add_due_at_too_far_future(self):
        """[NEW] add due_at 距今 > 1 年 -> TodoValidationError（DESIGN.md §十 §10.1）"""
        from src.exceptions import TodoValidationError
        from datetime import datetime, timedelta
        future = (datetime.now() + timedelta(days=800)).strftime("%Y-%m-%d %H:%M:%S")
        with self.assertRaises(TodoValidationError) as ctx:
            self.store.add(content="未来2年", due_at=future)
        self.assertIn("due_at 距今超过 365 天", str(ctx.exception))

    def test_add_due_at_invalid_format(self):
        """[NEW] add due_at 格式不合法 -> TodoValidationError"""
        from src.exceptions import TodoValidationError
        with self.assertRaises(TodoValidationError) as ctx:
            self.store.add(content="坏时间", due_at="2025-13-99 99:99:99")
        self.assertIn("格式不合法", str(ctx.exception))


class TestList(TestStoreBase):
    """list 方法测试（4 个）"""

    def test_list_default(self):
        """[OK] list 默认 -> 只返 pending + in_progress"""
        self.store.add(content="待办1", priority="medium")
        self.store.add(content="待办2", priority="medium")
        completed = self.store.add(content="已完成", priority="medium")
        self.store.done(str(completed["id"]))

        results = self.store.list()
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r["status"] in ("pending", "in_progress") for r in results))

    def test_list_overdue(self):
        """[OK] list --overdue -> 正确筛选"""
        # 创建已过期的 TODO（due_at 设为昨天）
        from datetime import datetime, timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.store.add(content="已过期", due_at=yesterday)

        overdue = self.store.list(overdue=True)
        self.assertEqual(len(overdue), 1)
        self.assertEqual(overdue[0]["content"], "已过期")

    def test_list_by_tag(self):
        """[OK] list --tag etf -> JSON 数组包含"""
        self.store.add(content="ETF相关", tags=["etf", "投资"])
        self.store.add(content="工作相关", tags=["work"])

        results = self.store.list(tag="etf")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "ETF相关")

    def test_list_by_priority(self):
        """[NEW] list --priority high -> 正确筛选（DESIGN.md §九 测试计划）"""
        self.store.add(content="高优1", priority="high")
        self.store.add(content="高优2", priority="high")
        self.store.add(content="中优", priority="medium")
        self.store.add(content="低优", priority="low")

        results = self.store.list(priority="high")
        self.assertEqual(len(results), 2)
        self.assertTrue(all(r["priority"] == "high" for r in results))


class TestDone(TestStoreBase):
    """done 方法测试（3 个）"""

    def test_done_by_id(self):
        """✅ done(id) → 状态 completed + completed_at"""
        todo = self.store.add(content="待办")
        result = self.store.done(str(todo["id"]))
        self.assertEqual(result["status"], "completed")
        self.assertIsNotNone(result["completed_at"])

    def test_done_by_content_fuzzy(self):
        """✅ done(content) 模糊匹配 → 找到则完成"""
        self.store.add(content="检查515050止损")
        result = self.store.done("检查515050")
        self.assertEqual(result["status"], "completed")

    def test_done_ambiguous(self):
        """❌ done 多个匹配 → TodoAmbiguousError"""
        self.store.add(content="检查止损")
        self.store.add(content="检查持仓")
        from src.exceptions import TodoAmbiguousError
        with self.assertRaises(TodoAmbiguousError) as ctx:
            self.store.done("检查")
        self.assertEqual(len(ctx.exception.candidates), 2)


class TestDelete(TestStoreBase):
    """delete 方法测试（1 个）"""

    def test_del_soft_delete(self):
        """[OK] delete(id) -> soft delete, move to archive"""
        todo = self.store.add(content="待删除")
        self.store.delete(str(todo["id"]))

        # todos 表中不存在
        remaining = self.store.list(all=True)
        self.assertEqual(len(remaining), 0)

        # archive 表中存在
        conn = self.store._get_connection()
        archived = conn.execute("SELECT * FROM todos_archive WHERE id = ?", (todo["id"],)).fetchone()
        conn.close()
        self.assertIsNotNone(archived)
        self.assertEqual(archived["status"], "cancelled")


class TestUpdate(TestStoreBase):
    """update 方法测试（2 个）"""

    def test_update_priority(self):
        """[OK] update priority -> field updated + updated_at is set"""
        todo = self.store.add(content="待办")
        self.assertIsNotNone(todo["updated_at"])

        result = self.store.update(todo["id"], priority="high")
        self.assertEqual(result["priority"], "high")
        self.assertIsNotNone(result["updated_at"])
        self.assertEqual(result["id"], todo["id"])

    def test_update_content_too_long(self):
        """❌ update 超长 content → TodoValidationError"""
        from src.exceptions import TodoValidationError
        todo = self.store.add(content="待办")
        with self.assertRaises(TodoValidationError):
            self.store.update(todo["id"], content="x" * 501)


class TestRestore(TestStoreBase):
    """restore 方法测试（1 个）"""

    def test_restore_from_archive(self):
        """[OK] restore: archive -> todos"""
        todo = self.store.add(content="待恢复")
        todo_id = todo["id"]
        self.store.delete(str(todo_id))

        # 已移入 archive
        result = self.store.restore(todo_id)
        self.assertEqual(result["content"], "待恢复")
        self.assertEqual(result["status"], "pending")
        # archive 中不存在
        conn = self.store._get_connection()
        archived = conn.execute("SELECT * FROM todos_archive WHERE id = ?", (todo_id,)).fetchone()
        conn.close()
        self.assertIsNone(archived)


class TestArchiveCleanup(TestStoreBase):
    """archive_cleanup 方法测试（1 个）"""

    def test_archive_cleanup_30_days(self):
        """✅ archive_cleanup → 30 天前清理 + 返回数量"""
        # 手动插入旧 archive
        conn = self.store._get_connection()
        from datetime import datetime, timedelta
        old_date = (datetime.now() - timedelta(days=31)).strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            """INSERT INTO todos_archive
               (id, content, active_form, status, priority, tags, created_at, updated_at, archived_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (999, "旧数据", "旧数据进行中", "completed", "low", "[]", old_date, old_date, old_date),
        )
        conn.commit()
        conn.close()

        # 清理
        count = self.store.archive_cleanup(days=30)
        self.assertEqual(count, 1)

        # 验证已删除
        conn = self.store._get_connection()
        remaining = conn.execute("SELECT * FROM todos_archive WHERE id = 999").fetchone()
        conn.close()
        self.assertIsNone(remaining)


class TestStats(TestStoreBase):
    """stats 方法测试（1 个）"""

    def test_stats_correct(self):
        """[OK] stats -> correct counts"""
        self.store.add(content="高优", priority="high")
        self.store.add(content="中优1", priority="medium")
        self.store.add(content="中优2", priority="medium")
        self.store.add(content="低优", priority="low")
        completed = self.store.add(content="已完成", priority="medium")
        self.store.done(str(completed["id"]))

        stats = self.store.stats()
        self.assertEqual(stats["total"], 5)
        self.assertEqual(stats["pending"], 4)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["high_priority"], 1)
        self.assertEqual(stats["medium_priority"], 3)  # includes completed
        self.assertEqual(stats["low_priority"], 1)


class TestGetByRawInput(TestStoreBase):
    """get_by_raw_input 方法测试（1 个）"""

    def test_get_by_raw_input_boundary(self):
        """[NEW] get_by_raw_input 边界：无匹配 -> []"""
        self.store.add(content="检查止损", raw_input="帮我记一下：检查止损")

        # 有匹配
        results = self.store.get_by_raw_input("检查止损")
        self.assertEqual(len(results), 1)

        # 无匹配
        results = self.store.get_by_raw_input("不存在的输入")
        self.assertEqual(results, [])

        # None 输入
        results = self.store.get_by_raw_input("不存在的输入")
        self.assertIsInstance(results, list)


class TestCheckOverdue(TestStoreBase):
    """check_overdue 方法测试（1 个）"""

    def test_check_overdue_marks_expired(self):
        """[NEW] check_overdue -> 批量标记 overdue + 写 audit_log"""
        from datetime import datetime, timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.store.add(content="已过期1", due_at=yesterday)
        self.store.add(content="已过期2", due_at=yesterday)
        self.store.add(content="未过期", due_at=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"))
        self.store.add(content="无日期")

        overdue = self.store.check_overdue()
        self.assertEqual(len(overdue), 2)
        self.assertTrue(all(o["status"] == "overdue" for o in overdue))


if __name__ == "__main__":
    unittest.main(verbosity=2)