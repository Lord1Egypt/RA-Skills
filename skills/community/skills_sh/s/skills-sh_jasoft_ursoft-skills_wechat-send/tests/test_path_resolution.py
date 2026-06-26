from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import wechat_auto


class WeChatAutoTests(unittest.TestCase):
    def test_send_message_pastes_after_frontmost_check(self) -> None:
        with mock.patch.object(
            wechat_auto.WeChatAuto, "ensure_wechat_running"
        ), mock.patch.object(
            wechat_auto.WeChatAuto, "search_contact", return_value=True
        ), mock.patch.object(
            wechat_auto.WeChatAuto, "ensure_wechat_frontmost"
        ) as ensure_frontmost, mock.patch.object(
            wechat_auto, "type_text_via_clipboard"
        ) as paste_text, mock.patch.object(
            wechat_auto, "press_return"
        ):
            wc = wechat_auto.WeChatAuto()
            wc.send_message("文件传输助手", "测试消息")

        ensure_frontmost.assert_called()
        paste_text.assert_called_once_with("测试消息")

    def test_doctor_returns_nonzero_when_required_check_fails(self) -> None:
        checks = [wechat_auto.DoctorCheck("osascript", False, "missing")]
        with mock.patch.object(
            wechat_auto, "collect_doctor_checks", return_value=checks
        ), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
            io.StringIO()
        ):
            exit_code = wechat_auto.run_doctor()
        self.assertEqual(exit_code, 1)

    def test_doctor_returns_zero_when_all_checks_pass(self) -> None:
        checks = [wechat_auto.DoctorCheck("osascript", True, "/usr/bin/osascript")]
        with mock.patch.object(
            wechat_auto, "collect_doctor_checks", return_value=checks
        ), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(
            io.StringIO()
        ):
            exit_code = wechat_auto.run_doctor()
        self.assertEqual(exit_code, 0)


if __name__ == "__main__":
    unittest.main()
