# todos/tests/test_cli.py
# CLI 单元测试（15 个用例）
# 版本：v1.0 | 日期：2026-06-11

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# 测试前设置 env
os.environ["TODOS_DB_PATH"] = tempfile.mktemp(suffix=".db")

from src import store as store_module
from src.cli import (
    EXIT_DATAERR,
    EXIT_OK,
    EXIT_SOFTWARE,
    EXIT_USAGE,
    build_parser,
    main,
)


class CLIBase(unittest.TestCase):
    """CLI 测试基类"""

    def setUp(self):
        self.db_path = tempfile.mktemp(suffix=".db")
        os.environ["TODOS_DB_PATH"] = self.db_path
        store_module.DB_PATH = self.db_path
        store_module.TodosStore._instance = None
        # 初始化数据库
        from src.store import TodosStore
        TodosStore().init_db()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def run_cli(self, *args, expect_exit: int | None = None) -> tuple[str, str, int]:
        """运行 CLI 并捕获输出"""
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            try:
                exit_code = main(list(args))
            except SystemExit as e:
                exit_code = e.code if isinstance(e.code, int) else 1
        if expect_exit is not None:
            self.assertEqual(exit_code, expect_exit, f"stdout={out.getvalue()}, stderr={err.getvalue()}")
        return out.getvalue(), err.getvalue(), exit_code


class TestAddCommand(CLIBase):
    """add 子命令测试（3 个）"""

    def test_add_normal(self):
        """[OK] add 正常添加"""
        out, err, code = self.run_cli("add", "检查止损", "--priority", "high", expect_exit=EXIT_OK)
        self.assertIn("检查止损", out)
        self.assertIn("[ ]", out)  # pending 状态
        self.assertIn("!!", out)  # high 优先级

    def test_add_with_due_and_tag(self):
        """[OK] add 带 due 和 tag"""
        from datetime import datetime, timedelta
        due = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        out, err, code = self.run_cli(
            "add", "开会", "--due", due, "--tag", "work,meeting",
            expect_exit=EXIT_OK,
        )
        self.assertIn("开会", out)
        self.assertIn("due:", out)
        self.assertIn("work", out)

    def test_add_invalid_priority(self):
        """[FAIL] add 非法 priority -> argparse EXIT_USAGE"""
        # argparse 在 choices 校验时就拒绝
        out, err, code = self.run_cli("add", "测试", "--priority", "urgent", expect_exit=EXIT_USAGE)
        self.assertIn("invalid choice", err)


class TestListCommand(CLIBase):
    """list 子命令测试（3 个）"""

    def test_list_default(self):
        """[OK] list 默认"""
        self.run_cli("add", "待办1", expect_exit=EXIT_OK)
        self.run_cli("add", "待办2", expect_exit=EXIT_OK)
        out, _, _ = self.run_cli("list", expect_exit=EXIT_OK)
        self.assertIn("待办1", out)
        self.assertIn("待办2", out)
        self.assertIn("共 2 条", out)

    def test_list_by_priority(self):
        """[OK] list --priority high"""
        self.run_cli("add", "高优", "--priority", "high", expect_exit=EXIT_OK)
        self.run_cli("add", "中优", expect_exit=EXIT_OK)
        out, _, _ = self.run_cli("list", "--priority", "high", expect_exit=EXIT_OK)
        self.assertIn("高优", out)
        self.assertNotIn("中优", out)

    def test_list_json_format(self):
        """[OK] list --format json"""
        self.run_cli("add", "测试", expect_exit=EXIT_OK)
        out, _, _ = self.run_cli("list", "--format", "json", expect_exit=EXIT_OK)
        data = json.loads(out)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["content"], "测试")


class TestDoneCommand(CLIBase):
    """done 子命令测试（2 个）"""

    def test_done_by_id(self):
        """[OK] done 1 -> 状态 completed"""
        self.run_cli("add", "待办", expect_exit=EXIT_OK)
        out, _, _ = self.run_cli("done", "1", expect_exit=EXIT_OK)
        self.assertIn("[OK]", out)  # status icon changed to [OK]
        # 验证后续 list 看不到
        out2, _, _ = self.run_cli("list", expect_exit=EXIT_OK)
        self.assertNotIn("待办", out2)

    def test_done_not_found(self):
        """[FAIL] done 不存在 ID → EXIT_DATAERR"""
        out, err, code = self.run_cli("done", "999", expect_exit=EXIT_DATAERR)
        self.assertIn("未找到", err)


class TestDeleteCommand(CLIBase):
    """delete 子命令测试（1 个）"""

    def test_delete_by_id(self):
        """[OK] delete 1 → 软删除"""
        self.run_cli("add", "待删除", expect_exit=EXIT_OK)
        out, _, _ = self.run_cli("delete", "1", expect_exit=EXIT_OK)
        self.assertIn("已删除", out)
        # 验证 list 看不到
        out2, _, _ = self.run_cli("list", expect_exit=EXIT_OK)
        self.assertNotIn("待删除", out2)


class TestUpdateCommand(CLIBase):
    """update 子命令测试（2 个）"""

    def test_update_priority(self):
        """[OK] update --priority"""
        self.run_cli("add", "待办", expect_exit=EXIT_OK)
        out, _, _ = self.run_cli("update", "1", "--priority", "high", expect_exit=EXIT_OK)
        self.assertIn("!!", out)  # high 优先级图标
        # 验证 list 看到 high
        out2, _, _ = self.run_cli("list", "--priority", "high", expect_exit=EXIT_OK)
        self.assertIn("待办", out2)

    def test_update_no_field(self):
        """[FAIL] update 不带字段 → EXIT_USAGE"""
        out, err, code = self.run_cli("update", "1", expect_exit=EXIT_USAGE)
        self.assertIn("至少指定一个", err)


class TestStatsCommand(CLIBase):
    """stats 子命令测试（1 个）"""

    def test_stats_basic(self):
        """[OK] stats 显示统计"""
        self.run_cli("add", "高优", "--priority", "high", expect_exit=EXIT_OK)
        self.run_cli("add", "中优", expect_exit=EXIT_OK)
        out, _, _ = self.run_cli("stats", expect_exit=EXIT_OK)
        self.assertIn("总数:", out)
        self.assertIn("待办:", out)
        self.assertIn("高优先级:", out)


class TestInitAndCheckOverdue(CLIBase):
    """init + check-overdue 测试（2 个）"""

    def test_init(self):
        """[OK] init 子命令"""
        # init 已经在 setUp 隐式调用
        # 重复调用应不报错
        out, _, _ = self.run_cli("init", expect_exit=EXIT_OK)

    def test_check_overdue(self):
        """[OK] check-overdue 子命令"""
        from datetime import datetime, timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.run_cli("add", "已过期", "--due", yesterday, expect_exit=EXIT_OK)
        out, _, _ = self.run_cli("check-overdue", expect_exit=EXIT_OK)
        self.assertIn("标记了", out)
        self.assertIn("已过期", out)


class TestErrorHandling(CLIBase):
    """错误处理测试（5 个）"""

    def test_no_command(self):
        """[FAIL] 无子命令 -> SystemExit"""
        with self.assertRaises(SystemExit):
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                main([])

    def test_add_due_at_too_far(self):
        """[NEW] add due_at 距今 > 1 年 -> 友好错误（DESIGN.md §十 §10.1）"""
        from datetime import datetime, timedelta
        future = (datetime.now() + timedelta(days=800)).strftime("%Y-%m-%d %H:%M:%S")
        out, err, code = self.run_cli("add", "测试", "--due", future, expect_exit=EXIT_USAGE)
        self.assertIn("校验失败", err)
        self.assertIn("due_at 距今超过", err)

    def test_done_ambiguous_shows_candidates(self):
        """[NEW] done 多个匹配 -> 显示候选列表"""
        self.run_cli("add", "检查止损", expect_exit=EXIT_OK)
        self.run_cli("add", "检查持仓", expect_exit=EXIT_OK)
        out, err, code = self.run_cli("done", "检查", expect_exit=EXIT_DATAERR)
        self.assertIn("找到", err)
        self.assertIn("检查止损", err)
        self.assertIn("检查持仓", err)

    def test_delete_ambiguous(self):
        """[NEW] delete 多个匹配 -> 显示候选"""
        self.run_cli("add", "任务A", expect_exit=EXIT_OK)
        self.run_cli("add", "任务B", expect_exit=EXIT_OK)
        out, err, code = self.run_cli("delete", "任务", expect_exit=EXIT_DATAERR)
        self.assertIn("找到", err)
        self.assertIn("任务A", err)
        self.assertIn("任务B", err)

    def test_update_not_found(self):
        """[NEW] update 不存在 ID -> EXIT_DATAERR"""
        out, err, code = self.run_cli(
            "update", "99999", "--priority", "high",
            expect_exit=EXIT_DATAERR,
        )
        self.assertIn("99999", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)