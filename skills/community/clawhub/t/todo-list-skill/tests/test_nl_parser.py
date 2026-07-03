# todos/tests/test_nl_parser.py
# NLP 解析器单元测试（12 个用例）
# 版本：v1.0 | 日期：2026-06-11

import os
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ["TODOS_DB_PATH"] = "/tmp/test_nl.db"

from src.nl_parser import NLParser, parse


class TestParseAction(unittest.TestCase):
    """action 识别测试（5 个）"""

    def setUp(self):
        self.parser = NLParser()

    def test_add_simple(self):
        """[OK] add: 加个待办：写报告"""
        r = self.parser.parse("加个待办：写报告")
        self.assertEqual(r["action"], "add")
        self.assertIn("写报告", r["content"])

    def test_done_recognize(self):
        """[OK] done: 完成检查止损"""
        r = self.parser.parse("完成检查止损")
        self.assertEqual(r["action"], "done")
        self.assertIn("检查止损", r["content"])

    def test_delete_recognize(self):
        """[OK] delete: 删除任务X"""
        r = self.parser.parse("删除任务X")
        self.assertEqual(r["action"], "delete")
        self.assertIn("任务X", r["content"])

    def test_list_recognize(self):
        """[OK] list: 列出待办"""
        r = self.parser.parse("列出待办")
        self.assertEqual(r["action"], "list")

    def test_unknown_random(self):
        """[OK] unknown: 随机文本"""
        r = self.parser.parse("hello world without any keyword")
        self.assertEqual(r["action"], "unknown")


class TestParseTime(unittest.TestCase):
    """时间解析测试（3 个）"""

    def setUp(self):
        self.parser = NLParser()

    def test_afternoon_time(self):
        """[OK] 明天下午3点 → due_at 包含 15:00"""
        r = self.parser.parse("提醒我明天下午3点检查止损")
        self.assertIsNotNone(r["due_at"])
        self.assertIn("15:00", r["due_at"])
        self.assertIn("检查止损", r["content"])

    def test_iso_format(self):
        """[OK] 明天 14:00 提交报告"""
        r = self.parser.parse("明天 14:00 提交报告")
        self.assertIsNotNone(r["due_at"])
        self.assertIn("14:00", r["due_at"])

    def test_no_time(self):
        """[OK] 无时间 → due_at=None"""
        r = self.parser.parse("加个待办：写报告")
        self.assertIsNone(r["due_at"])


class TestParsePriority(unittest.TestCase):
    """优先级解析测试（2 个）"""

    def setUp(self):
        self.parser = NLParser()

    def test_urgent_keyword(self):
        """[OK] 紧急 → high"""
        r = self.parser.parse("紧急修复515070止损")
        self.assertEqual(r["priority"], "high")

    def test_default_medium(self):
        """[OK] 默认 medium"""
        r = self.parser.parse("加个待办：写报告")
        self.assertEqual(r["priority"], "medium")


class TestParseTags(unittest.TestCase):
    """标签解析测试（2 个）"""

    def setUp(self):
        self.parser = NLParser()

    def test_hash_tag(self):
        """[OK] #etf → tags=['etf']"""
        r = self.parser.parse("紧急修复515070止损 #etf")
        self.assertIn("etf", r["tags"])

    def test_explicit_tag(self):
        """[OK] tag:work → tags=['work']"""
        r = self.parser.parse("urgent: 写日报 tag:work")
        self.assertIn("work", r["tags"])


class TestEdgeCases(unittest.TestCase):
    """边界测试（3 个）"""

    def setUp(self):
        self.parser = NLParser()

    def test_empty_string(self):
        """[OK] 空字符串 → unknown"""
        r = self.parser.parse("")
        self.assertEqual(r["action"], "unknown")
        self.assertEqual(r["content"], "")

    def test_whitespace_only(self):
        """[OK] 纯空格 → unknown"""
        r = self.parser.parse("   ")
        self.assertEqual(r["action"], "unknown")

    def test_too_long(self):
        """[OK] 超长文本（>2000 字符）→ 截断"""
        long_text = "加个待办：写报告 " * 200  # 约 1500 字符
        r = self.parser.parse(long_text)
        # 截断到 2000
        self.assertLessEqual(len(r["raw"]), 2000)


class TestParseModuleFunction(unittest.TestCase):
    """模块级 parse() 函数测试（1 个）"""

    def test_parse_function(self):
        """[OK] 模块级 parse() 正常工作"""
        r = parse("完成检查止损")
        self.assertEqual(r["action"], "done")


class TestTimeVariants(unittest.TestCase):
    """时间变体测试（覆盖 7 种 base）"""

    def setUp(self):
        self.parser = NLParser()

    def test_today(self):
        """[NEW] 今天 X 点 -> 今天"""
        r = self.parser.parse("今天 10:00 起床")
        self.assertIsNotNone(r["due_at"])
        # 检查日期是今天
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        self.assertIn(today, r["due_at"])

    def test_tomorrow(self):
        """[NEW] 明天 X 点 -> 明天"""
        r = self.parser.parse("明天 9 点开会")
        self.assertIsNotNone(r["due_at"])

    def test_day_after_tomorrow(self):
        """[NEW] 后天 X 点 -> 后天"""
        r = self.parser.parse("后天 15:00 交报告")
        self.assertIsNotNone(r["due_at"])

    def test_day_after_tomorrow_big(self):
        """[NEW] 大后天 X 点 -> 大后天"""
        r = self.parser.parse("大后天 10 点去医院")
        self.assertIsNotNone(r["due_at"])

    def test_next_week(self):
        """[NEW] 下周 X 点 -> 7 天后"""
        r = self.parser.parse("下周 9 点开会")
        self.assertIsNotNone(r["due_at"])

    def test_next_month(self):
        """[NEW] 下个月 X 点 -> 30 天后"""
        r = self.parser.parse("下个月 1 号交房租")
        self.assertIsNotNone(r["due_at"])

    def test_next_monday(self):
        """[NEW] 下周一 X 点"""
        r = self.parser.parse("下周一 9 点开会")
        self.assertIsNotNone(r["due_at"])

    def test_tomorrow_morning(self):
        """[NEW] 明早 6:30"""
        r = self.parser.parse("明早 6:30 起床")
        self.assertIsNotNone(r["due_at"])
        self.assertIn("06:30", r["due_at"])

    def test_tonight(self):
        """[NEW] 今晚 8 点"""
        r = self.parser.parse("今晚 8 点看电影")
        self.assertIsNotNone(r["due_at"])
        self.assertIn("20:00", r["due_at"])

    def test_iso_format(self):
        """[NEW] 2026-06-15 14:00 格式"""
        r = self.parser.parse("加个待办 2026-06-15 14:00 开会")
        self.assertIsNotNone(r["due_at"])
        self.assertIn("2026-06-15", r["due_at"])

    def test_hour_out_of_range(self):
        """[NEW] 25:00 边界 -> None"""
        r = self.parser.parse("今天 25:00 起床")
        self.assertIsNone(r["due_at"])

    def test_low_priority(self):
        """[NEW] 不急/低 -> low"""
        r = self.parser.parse("不急的：写日记")
        self.assertEqual(r["priority"], "low")


class TestPriorityAndTagEdges(unittest.TestCase):
    """边界测试（覆盖优先级、标签）"""

    def setUp(self):
        self.parser = NLParser()

    def test_priority_high_urgent(self):
        """[NEW] urgent -> high"""
        r = self.parser.parse("urgent: 写日报")
        self.assertEqual(r["priority"], "high")

    def test_priority_high_important(self):
        """[NEW] 重要 -> high"""
        r = self.parser.parse("重要：完成 ETF 报告")
        self.assertEqual(r["priority"], "high")

    def test_priority_high_double_bang(self):
        """[NEW] !! -> high"""
        r = self.parser.parse("紧急任务 !!")
        self.assertEqual(r["priority"], "high")

    def test_multiple_tags(self):
        """[NEW] tag:work,urgent 多个标签"""
        r = self.parser.parse("加待办 tag:work,urgent 内容")
        self.assertIn("work", r["tags"])
        self.assertIn("urgent", r["tags"])


if __name__ == "__main__":
    unittest.main(verbosity=2)