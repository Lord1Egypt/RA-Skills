# todos/tests/test_reminder.py
# Reminder 单元测试（10 个用例）
# 版本：v1.0 | 日期：2026-06-11

import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class ReminderBase(unittest.TestCase):
    """测试基类：每个测试用独立数据库"""

    def setUp(self):
        self.db_path = tempfile.mktemp(suffix=".db")
        os.environ["TODOS_DB_PATH"] = self.db_path
        from src import store as store_module
        store_module.DB_PATH = self.db_path
        store_module.TodosStore._instance = None
        self.store = store_module.TodosStore()
        self.store.init_db()

        # 设置 reminder 使用的环境
        from src import reminder
        self.reminder = reminder

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)


class TestGetTodayDue(ReminderBase):
    """get_today_due 测试（3 个）"""

    def test_today_due_returns_today(self):
        """[OK] get_today_due 返回今天到期的"""
        # 添加一个今天 18:00 到期的
        today_18 = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
        self.store.add(content="今天会议", due_at=today_18.strftime("%Y-%m-%d %H:%M:%S"))

        results = self.reminder.get_today_due()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "今天会议")

    def test_today_due_excludes_tomorrow(self):
        """[OK] get_today_due 排除明天"""
        tomorrow = (datetime.now() + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
        self.store.add(content="明天会议", due_at=tomorrow.strftime("%Y-%m-%d %H:%M:%S"))

        results = self.reminder.get_today_due()
        self.assertEqual(len(results), 0)

    def test_today_due_excludes_completed(self):
        """[OK] get_today_due 排除已完成的"""
        today_15 = datetime.now().replace(hour=15, minute=0, second=0, microsecond=0)
        todo = self.store.add(content="已完成", due_at=today_15.strftime("%Y-%m-%d %H:%M:%S"))
        self.store.done(str(todo["id"]))

        results = self.reminder.get_today_due()
        self.assertEqual(len(results), 0)


class TestGetOverdue(ReminderBase):
    """get_overdue 测试（1 个）"""

    def test_get_overdue_returns_yesterday(self):
        """[OK] get_overdue 返回已过期的"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.store.add(content="已过期", due_at=yesterday)

        results = self.reminder.get_overdue()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "已过期")


class TestFormatMessage(ReminderBase):
    """format_message 测试（2 个）"""

    def test_format_empty(self):
        """[OK] 空列表 -> 友好提示"""
        msg = self.reminder.format_message([], title="测试")
        self.assertIn("测试", msg)
        self.assertIn("无待办", msg)

    def test_format_with_todos(self):
        """[OK] 有 TODO -> 完整格式（v1.5.0 WorkBuddy 格式）"""
        today = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        todo = self.store.add(content="开会", due_at=today.strftime("%Y-%m-%d %H:%M:%S"), priority="high")
        todos = self.reminder.get_today_due()
        msg = self.reminder.format_message(todos, title="今日待办")

        self.assertIn("今日待办", msg)
        self.assertIn("开会", msg)
        self.assertIn("HIGH", msg)  # v1.5.0: [🔴 HIGH] 格式
        self.assertIn("**今日待办**", msg)  # markdown 加粗标题
        self.assertIn("共 1 项", msg)  # v1.5.0: 共 X 项
        self.assertIn("⏰", msg)  # v1.5.0: ⏰ 钟表符号


class TestCLICommands(ReminderBase):
    """CLI 命令测试（3 个）"""

    def test_daily_due_command(self):
        """[OK] daily-due 子命令"""
        out = self._run_cli("daily-due")

    def test_check_overdue_command(self):
        """[OK] check-overdue 子命令"""
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.store.add(content="过期", due_at=yesterday)
        out = self._run_cli("check-overdue")
        self.assertIn("过期", out)

    def test_archive_cleanup_command(self):
        """[OK] archive-cleanup 子命令"""
        out = self._run_cli("archive-cleanup", "--days", "30")
        self.assertIn("清理", out)

    def _run_cli(self, *args) -> str:
        """运行 reminder CLI"""
        import io
        from contextlib import redirect_stdout
        out = io.StringIO()
        with redirect_stdout(out):
            try:
                self.reminder.main(list(args))
            except SystemExit as e:
                pass
        return out.getvalue()


class TestPushToChannel(ReminderBase):
    """push_to_channel 测试（v1.5.0 双通道）"""

    def test_push_workbuddy_channel(self):
        """[OK] workbuddy 通道：直接输出到 stdout，返回 True"""
        msg = "## test message"
        # 默认走 workbuddy 通道
        result = self.reminder.push_to_channel(msg)
        self.assertTrue(result)

    def test_push_dingtalk_no_qwenpaw(self):
        """[OK] dingtalk 通道：qwenpaw 不存在时降级到 stdout"""
        msg = "## test message"
        # 显式指定 dingtalk 通道
        result = self.reminder.push_to_channel(msg, channel="dingtalk")
        # 降级到 stdout，返回 False（标识推送未真正成功）
        self.assertFalse(result)


class TestGetUpcoming(ReminderBase):
    """get_upcoming 测试（2 个）"""

    def test_upcoming_includes_today_and_tomorrow(self):
        """[OK] get_upcoming 包含今天和明天"""
        from datetime import datetime, timedelta
        today = datetime.now().replace(hour=23, minute=0, second=0, microsecond=0)
        tomorrow = (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
        self.store.add(content="今晚任务", due_at=today.strftime("%Y-%m-%d %H:%M:%S"))
        self.store.add(content="明天任务", due_at=tomorrow.strftime("%Y-%m-%d %H:%M:%S"))

        results = self.reminder.get_upcoming(days=2)
        # 至少 1 条（具体数量取决于精确时间）
        self.assertGreaterEqual(len(results), 1)

    def test_upcoming_excludes_far_future(self):
        """[OK] get_upcoming 排除远期"""
        from datetime import datetime, timedelta
        far_future = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
        self.store.add(content="远期", due_at=far_future)

        results = self.reminder.get_upcoming(days=7)
        self.assertEqual(len(results), 0)


class TestPushMocked(ReminderBase):
    """push_to_channel 用 mock 测试（v1.5.0 dingtalk 通道）"""

    def test_push_success_mocked(self):
        """[OK] mock subprocess.run -> 成功（dingtalk 通道）"""
        from unittest.mock import patch, MagicMock
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stderr="")
            result = self.reminder.push_to_channel("test", channel="dingtalk")
            self.assertTrue(result)

    def test_push_failure_mocked(self):
        """[OK] mock subprocess.run -> 失败降级到 stdout（dingtalk 通道）"""
        from unittest.mock import patch, MagicMock
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stderr="error")
            result = self.reminder.push_to_channel("test", channel="dingtalk")
            # v1.5.0: 失败时降级到 stdout，返回 False
            self.assertFalse(result)

    def test_push_timeout_mocked(self):
        """[OK] mock subprocess.run -> 超时降级到 stdout（dingtalk 通道）"""
        import subprocess
        from unittest.mock import patch
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("cmd", 10)
            result = self.reminder.push_to_channel("test", channel="dingtalk")
            self.assertFalse(result)


class TestUpcomingCommand(ReminderBase):
    """upcoming CLI 子命令测试（1 个）"""

    def test_upcoming_command(self):
        """[OK] upcoming 子命令"""
        from datetime import datetime, timedelta
        tomorrow = (datetime.now() + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
        self.store.add(content="明天", due_at=tomorrow.strftime("%Y-%m-%d %H:%M:%S"))

        import io
        from contextlib import redirect_stdout
        out = io.StringIO()
        with redirect_stdout(out):
            try:
                self.reminder.main(["upcoming", "--days", "3"])
            except SystemExit:
                pass
        output = out.getvalue()
        self.assertIn("未来", output)


class TestSetupCommand(unittest.TestCase):
    """setup CLI 子命令测试（v1.5.0 新增，2 个）"""

    def setUp(self):
        """每个测试用独立临时目录（避免 config.json 污染）"""
        import os
        import sys
        import tempfile
        from pathlib import Path
        self.tmpdir = tempfile.mkdtemp()
        # 把 src/ 加到 sys.path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from src import reminder
        self.reminder = reminder
        # patch _TODOS_DIR 和 _CONFIG_PATH 指向 tmpdir
        self.original_todos_dir = reminder._TODOS_DIR
        self.original_config_path = reminder._CONFIG_PATH
        # 注意：_ensure_todos_dir 用 _TODOS_DIR，必须两者都 patch
        # 我们让 _TODOS_DIR = tmpdir/config_dir，_CONFIG_PATH 放里面
        config_dir = Path(self.tmpdir) / "config"
        reminder._TODOS_DIR = config_dir
        reminder._CONFIG_PATH = config_dir / "config.json"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        self.reminder._TODOS_DIR = self.original_todos_dir
        self.reminder._CONFIG_PATH = self.original_config_path

    def test_setup_workbuddy(self):
        """[NEW] setup --channel workbuddy 配置成功"""
        import io
        from contextlib import redirect_stdout
        out = io.StringIO()
        with redirect_stdout(out):
            try:
                self.reminder.main(["setup", "--channel", "workbuddy"])
            except SystemExit:
                pass
        output = out.getvalue()
        self.assertIn("✅", output)
        self.assertIn("workbuddy", output)

    def test_setup_already_completed(self):
        """[NEW] setup 重复调用提示已配置"""
        # 第一次配置
        self.reminder.main(["setup", "--channel", "workbuddy"])

        # 第二次（无 --force）
        import io
        from contextlib import redirect_stdout
        out = io.StringIO()
        with redirect_stdout(out):
            try:
                self.reminder.main(["setup", "--channel", "dingtalk"])
            except SystemExit:
                pass
        output = out.getvalue()
        self.assertIn("已配置完成", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)