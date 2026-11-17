# -*- coding: utf-8 -*-
"""stop_reason 用户友好文案单元测试。"""
from __future__ import annotations

import unittest

from service.task_rpa import format_stop_reason_for_user


class TestFormatStopReasonForUser(unittest.TestCase):
    def test_max_items(self) -> None:
        msg = format_stop_reason_for_user("max_items", 100)
        self.assertIn("默认采集规模", msg)
        self.assertIn("100", msg)

    def test_end_marker(self) -> None:
        msg = format_stop_reason_for_user("end_marker", 42)
        self.assertIn("没有更多结果", msg)

    def test_no_new_rounds(self) -> None:
        msg = format_stop_reason_for_user("no_new_rounds", 30)
        self.assertIn("连续多次加载没有发现新结果", msg)

    def test_max_scrolls(self) -> None:
        msg = format_stop_reason_for_user("max_scrolls", 80)
        self.assertIn("页面加载保护范围", msg)

    def test_none_or_unknown(self) -> None:
        self.assertEqual(format_stop_reason_for_user(None, 10), "本次采集已完成。")
        self.assertEqual(format_stop_reason_for_user("unknown", 10), "本次采集已完成。")


if __name__ == "__main__":
    unittest.main()
