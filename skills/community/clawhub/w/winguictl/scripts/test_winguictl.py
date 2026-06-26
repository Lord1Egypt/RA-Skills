#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Unit tests for winguictl."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from constants import VK_CODE_MAP, WIN32_CONTROL_TYPE_MAP
from models import Bounds, ElementInfo, WindowInfo, ActionResult, ElementFormatter
from win32_driver import Win32Driver


class TestConstants:
    """Tests for constants module."""

    def test_vk_code_map_contains_common_keys(self):
        assert "enter" in VK_CODE_MAP
        assert "tab" in VK_CODE_MAP
        assert "esc" in VK_CODE_MAP
        assert "space" in VK_CODE_MAP
        assert "ctrl" in VK_CODE_MAP
        assert "shift" in VK_CODE_MAP
        assert "alt" in VK_CODE_MAP

    def test_vk_code_map_function_keys(self):
        for i in range(1, 13):
            assert f"f{i}" in VK_CODE_MAP

    def test_vk_code_map_letters(self):
        for c in "abcdefghijklmnopqrstuvwxyz":
            assert c in VK_CODE_MAP

    def test_vk_code_map_digits(self):
        for d in "0123456789":
            assert d in VK_CODE_MAP

    def test_win32_control_type_map_common_classes(self):
        assert "Button" in WIN32_CONTROL_TYPE_MAP
        assert "Edit" in WIN32_CONTROL_TYPE_MAP
        assert "ComboBox" in WIN32_CONTROL_TYPE_MAP
        assert "ListBox" in WIN32_CONTROL_TYPE_MAP


class TestModels:
    """Tests for models module."""

    def test_bounds_from_rect(self):
        class MockRect:
            left = 100
            top = 200
            right = 400
            bottom = 500

        bounds = Bounds.from_rect(MockRect())
        assert bounds.x == 100
        assert bounds.y == 200
        assert bounds.width == 300
        assert bounds.height == 300

    def test_bounds_to_dict(self):
        bounds = Bounds(x=10, y=20, width=100, height=200)
        d = bounds.to_dict()
        assert d == {"x": 10, "y": 20, "width": 100, "height": 200}

    def test_window_info_to_dict(self):
        bounds = Bounds(x=0, y=0, width=800, height=600)
        info = WindowInfo(
            window_id="12345",
            title="Test Window",
            bounds=bounds,
            process_id=1234,
            process_name="test.exe",
        )
        d = info.to_dict()
        assert d["window_id"] == "12345"
        assert d["title"] == "Test Window"
        assert d["process_id"] == 1234
        assert d["process_name"] == "test.exe"

    def test_element_info_to_dict(self):
        bounds = Bounds(x=100, y=100, width=50, height=30)
        info = ElementInfo(
            element_id="btn1",
            window_id="12345",
            text="Click Me",
            bounds=bounds,
            control_type="Button",
        )
        d = info.to_dict()
        assert d["element_id"] == "btn1"
        assert d["text"] == "Click Me"
        assert d["control_type"] == "Button"

    def test_action_result_to_dict(self):
        result = ActionResult(ok=True, code="OK", message="Success", data={"key": "value"})
        d = result.to_dict()
        assert d["ok"] is True
        assert d["code"] == "OK"
        assert d["message"] == "Success"
        assert d["data"] == {"key": "value"}


class TestElementFormatter:
    """Tests for ElementFormatter class."""

    def test_format_basic(self):
        formatter = ElementFormatter(text="Hello")
        result = formatter.format()
        assert '- "Hello"' in result

    def test_format_with_rect(self):
        formatter = ElementFormatter(text="Button", rect=(10, 20, 100, 50))
        result = formatter.format()
        assert '- "Button"' in result
        assert "rect=(10,20 100x50)" in result

    def test_format_with_control_type(self):
        formatter = ElementFormatter(text="Submit", control_type="Button")
        result = formatter.format()
        assert 'control_type="Button"' in result

    def test_format_with_hwnd(self):
        formatter = ElementFormatter(text="Window", hwnd=12345)
        result = formatter.format()
        assert 'hwnd="12345"' in result

    def test_format_with_confidence(self):
        formatter = ElementFormatter(text="Match", confidence=0.95)
        result = formatter.format()
        assert "confidence=0.95" in result

    def test_format_ocr(self):
        result = ElementFormatter.format_ocr("Text", 10, 20, 100, 30, confidence=0.9)
        assert '- "Text"' in result
        assert "rect=(10,20 100x30)" in result
        assert "confidence=0.90" in result


class TestWin32Driver:
    """Tests for Win32Driver class."""

    def test_infer_control_type_exact_match(self):
        assert Win32Driver.infer_control_type("Button") == "Button"
        assert Win32Driver.infer_control_type("Edit") == "Edit"
        assert Win32Driver.infer_control_type("ComboBox") == "ComboBox"

    def test_infer_control_type_case_insensitive(self):
        assert Win32Driver.infer_control_type("button") == "Button"
        assert Win32Driver.infer_control_type("BUTTON") == "Button"
        assert Win32Driver.infer_control_type("edit") == "Edit"

    def test_infer_control_type_prefix_match_with_delimiter(self):
        assert Win32Driver.infer_control_type("Button.Extra") == "Button"
        assert Win32Driver.infer_control_type("Edit_Something") == "Edit"
        assert Win32Driver.infer_control_type("ComboBoxItem") is None

    def test_infer_control_type_no_match(self):
        assert Win32Driver.infer_control_type("CustomClass") is None
        assert Win32Driver.infer_control_type("") is None
        assert Win32Driver.infer_control_type(None) is None

    def test_infer_control_type_short_prefix_requires_delimiter(self):
        assert Win32Driver.infer_control_type("TButton.Extra") == "Button"
        assert Win32Driver.infer_control_type("TButtonExtra") is None


class TestOutputUtils:
    """Tests for output_utils module."""

    def test_generate_nonce(self):
        from output_utils import generate_nonce

        nonce1 = generate_nonce()
        nonce2 = generate_nonce()
        assert len(nonce1) == 16
        assert len(nonce2) == 16
        assert nonce1 != nonce2

    def test_wrap_with_boundary(self):
        from output_utils import wrap_with_boundary

        content = "test content"
        nonce = "abcd1234"
        result = wrap_with_boundary(content, nonce)
        assert "--- WINGUICTL_CONTENT nonce=abcd1234 ---" in result
        assert "--- END_WINGUICTL_CONTENT nonce=abcd1234 ---" in result
        assert "test content" in result

    def test_emit_action(self):
        from output_utils import emit_action
        import io
        import sys

        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            emit_action(True, "test", {"key": "value"})
            output = sys.stdout.getvalue()
            assert '"ok": true' in output
            assert '"code": "OK"' in output
            assert '"message": "test executed"' in output
        finally:
            sys.stdout = old_stdout


class TestCLI:
    """Tests for CLI argument parsing."""

    def test_build_parser(self):
        from winguictl import build_parser

        parser = build_parser()
        assert parser.prog == "winguictl"

    def test_window_list_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["window", "list"])
        assert args.command == "window"
        assert args.window_command == "list"

    def test_window_focus_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["window", "--window-id", "12345", "focus"])
        assert args.command == "window"
        assert args.window_command == "focus"
        assert args.window_id == 12345

    def test_snapshot_uia_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["snapshot", "--window-id", "12345", "uia"])
        assert args.command == "snapshot"
        assert args.snapshot_command == "uia"
        assert args.window_id == 12345

    def test_find_text_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["find", "--window-id", "12345", "text", "Submit"])
        assert args.command == "find"
        assert args.find_command == "text"
        assert args.text == "Submit"

    def test_action_click_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(
            ["action", "--window-id", "12345", "click", "--relative-x", "100",
             "--relative-y", "200"]
        )
        assert args.command == "action"
        assert args.action_command == "click"
        assert args.relative_x == 100
        assert args.relative_y == 200

    def test_action_type_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["action", "--window-id", "12345", "type", "--text", "Hello"])
        assert args.command == "action"
        assert args.action_command == "type"
        assert args.text == "Hello"

    def test_control_click_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["control", "--hwnd", "12345", "click"])
        assert args.command == "control"
        assert args.control_command == "click"
        assert args.hwnd == 12345

    def test_uia_control_click_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(
            ["uia-control", "--window-id", "12345", "--element-id", "btn1", "click"]
        )
        assert args.command == "uia-control"
        assert args.uia_control_command == "click"
        assert args.window_id == 12345
        assert args.element_id == "btn1"

    def test_screenshot_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["screenshot", "--window-id", "12345", "--output", "test.png"])
        assert args.command == "screenshot"
        assert args.window_id == 12345
        assert args.output == "test.png"

    def test_dry_run_flag(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(
            ["action", "--window-id", "12345", "click", "--relative-x", "100",
             "--relative-y", "200", "--dry-run"]
        )
        assert args.dry_run is True


class TestWin32API:
    """Tests for Win32API class."""

    def test_send_hotkey_list_format(self):
        """Test send_hotkey with list of braced keys."""
        from win32_utils import Win32API
        # Should not raise
        Win32API.send_hotkey(["{CTRL}", "{A}"])

    def test_send_hotkey_string_format(self):
        """Test send_hotkey with concatenated braced keys."""
        from win32_utils import Win32API
        # Should not raise
        Win32API.send_hotkey("{CTRL}{SHIFT}{A}")

    def test_send_hotkey_single_key_string(self):
        """Test send_hotkey with single braced key string."""
        from win32_utils import Win32API
        # Should not raise
        Win32API.send_hotkey("{ENTER}")

    def test_send_hotkey_invalid_string_no_braces(self):
        """Test send_hotkey rejects string without braces."""
        from win32_utils import Win32API
        with pytest.raises(ValueError, match="no valid braced keys found"):
            Win32API.send_hotkey("CTRL")

    def test_send_hotkey_invalid_list_no_braces(self):
        """Test send_hotkey rejects list with unbraced keys."""
        from win32_utils import Win32API
        with pytest.raises(ValueError, match="key must be wrapped in braces"):
            Win32API.send_hotkey(["CTRL", "A"])

    def test_send_hotkey_unsupported_key(self):
        """Test send_hotkey rejects unsupported key."""
        from win32_utils import Win32API
        with pytest.raises(ValueError, match="unsupported key"):
            Win32API.send_hotkey("{UNKNOWN_KEY}")

    def test_send_press_key_requires_braces(self):
        """Test send_press_key requires braced format."""
        from win32_utils import Win32API
        with pytest.raises(ValueError, match="key must be wrapped in braces"):
            Win32API.send_press_key("ENTER")

    def test_send_press_key_braced_format(self):
        """Test send_press_key accepts braced format."""
        from win32_utils import Win32API
        # Should not raise
        Win32API.send_press_key("{ENTER}")

    def test_send_type_text_with_embedded_keys(self):
        """Test send_type_text with embedded special keys."""
        from win32_utils import Win32API
        # Should not raise
        Win32API.send_type_text("abc{ENTER}def{TAB}ghi")

    def test_send_type_text_plain_text(self):
        """Test send_type_text with plain text only."""
        from win32_utils import Win32API
        # Should not raise
        Win32API.send_type_text("hello world")

    def test_normalize_key_strips_braces(self):
        """Test _normalize_key strips braces."""
        from win32_utils import Win32API
        assert Win32API._normalize_key("{ENTER}") == "enter"
        assert Win32API._normalize_key("enter") == "enter"
        assert Win32API._normalize_key("{CTRL}") == "ctrl"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])


class TestWaitUtils:
    """Tests for WaitUtils class."""

    def test_check_window_exists_found(self):
        """Test check_window_exists when window is found."""
        from wait_utils import WaitUtils
        from models import WindowInfo, Bounds

        mock_windows = [
            WindowInfo(
                window_id="12345",
                title="Test Window",
                bounds=Bounds(x=0, y=0, width=800, height=600),
                process_id=1234,
                process_name="test.exe",
            )
        ]

        with patch("wait_utils.WindowsDriver.list_windows", return_value=mock_windows):
            with patch("wait_utils.Win32API.get_class_name", return_value="TestClass"):
                result = WaitUtils.check_window_exists("Test Window", exact=True)
                assert result is not None
                assert result["window_id"] == "12345"
                assert result["title"] == "Test Window"

    def test_check_window_exists_not_found(self):
        """Test check_window_exists when window is not found."""
        from wait_utils import WaitUtils

        with patch("wait_utils.WindowsDriver.list_windows", return_value=[]):
            result = WaitUtils.check_window_exists("Nonexistent", exact=True)
            assert result is None

    def test_check_window_exists_partial_match(self):
        """Test check_window_exists with partial match."""
        from wait_utils import WaitUtils
        from models import WindowInfo, Bounds

        mock_windows = [
            WindowInfo(
                window_id="12345",
                title="Test Window - App",
                bounds=Bounds(x=0, y=0, width=800, height=600),
                process_id=1234,
                process_name="test.exe",
            )
        ]

        with patch("wait_utils.WindowsDriver.list_windows", return_value=mock_windows):
            with patch("wait_utils.Win32API.get_class_name", return_value="TestClass"):
                result = WaitUtils.check_window_exists("Test Window", exact=False)
                assert result is not None

    def test_check_text_exists_found(self):
        """Test check_text_exists when text is found."""
        from wait_utils import WaitUtils

        with patch("wait_utils.FindDriver.find_text", return_value="  Found Text  "):
            result = WaitUtils.check_text_exists(12345, "Found", exact=False)
            assert result == "Found Text"

    def test_check_text_exists_not_found(self):
        """Test check_text_exists when text is not found."""
        from wait_utils import WaitUtils

        with patch("wait_utils.FindDriver.find_text", return_value=""):
            result = WaitUtils.check_text_exists(12345, "NotThere", exact=False)
            assert result is None

    def test_check_uia_exists_found(self):
        """Test check_uia_exists when element is found."""
        from wait_utils import WaitUtils

        with patch("wait_utils.FindDriver.find_uia", return_value="  Element Info  "):
            result = WaitUtils.check_uia_exists(12345, text="Button")
            assert result == "Element Info"

    def test_check_uia_exists_not_found(self):
        """Test check_uia_exists when element is not found."""
        from wait_utils import WaitUtils

        with patch("wait_utils.FindDriver.find_uia", return_value=""):
            result = WaitUtils.check_uia_exists(12345, text="Nonexistent")
            assert result is None

    def test_check_ocr_exists_found(self):
        """Test check_ocr_exists when text is found."""
        from wait_utils import WaitUtils
        from models import ElementInfo, Bounds

        mock_matches = [
            ElementInfo(
                element_id="ocr1",
                window_id="12345",
                text="Found",
                bounds=Bounds(x=100, y=100, width=50, height=20),
            )
        ]

        with patch("wait_utils.OCRDriver.find_ocr_text", return_value=mock_matches):
            result = WaitUtils.check_ocr_exists(12345, "Found", exact=False)
            assert len(result) == 1
            assert result[0].text == "Found"

    def test_check_ocr_exists_not_found(self):
        """Test check_ocr_exists when text is not found."""
        from wait_utils import WaitUtils

        with patch("wait_utils.OCRDriver.find_ocr_text", return_value=[]):
            result = WaitUtils.check_ocr_exists(12345, "NotThere", exact=False)
            assert result == []

    def test_check_image_exists_found(self):
        """Test check_image_exists when image is found."""
        from wait_utils import WaitUtils
        from models import ElementInfo, Bounds

        mock_matches = [
            ElementInfo(
                element_id="img1",
                window_id="12345",
                text="",
                bounds=Bounds(x=100, y=100, width=50, height=50),
            )
        ]

        with patch("wait_utils.FindDriver.find_image", return_value=mock_matches):
            result = WaitUtils.check_image_exists(12345, "button.png", threshold=0.9)
            assert len(result) == 1

    def test_check_image_exists_not_found(self):
        """Test check_image_exists when image is not found."""
        from wait_utils import WaitUtils

        with patch("wait_utils.FindDriver.find_image", return_value=[]):
            result = WaitUtils.check_image_exists(12345, "nonexistent.png")
            assert result == []


class TestPollResult:
    """Tests for PollResult class."""

    def test_poll_result_found(self):
        """Test PollResult when condition is met."""
        from wait_utils import PollResult

        result = PollResult(found=True, data="test data", elapsed_ms=500)
        assert result.found is True
        assert result.data == "test data"
        assert result.elapsed_ms == 500
        assert result.timed_out is False

    def test_poll_result_timeout(self):
        """Test PollResult when timeout occurs."""
        from wait_utils import PollResult

        result = PollResult(found=False, elapsed_ms=30000, timed_out=True)
        assert result.found is False
        assert result.data is None
        assert result.timed_out is True


class TestWaitUtilsPoll:
    """Tests for WaitUtils polling methods."""

    def test_poll_condition_found(self):
        """Test poll_condition when condition is met immediately."""
        from wait_utils import WaitUtils

        check_count = [0]

        def check_fn():
            check_count[0] += 1
            return "found"

        result = WaitUtils.poll_condition(check_fn, timeout_sec=5.0, interval_sec=0.1)
        assert result.found is True
        assert result.data == "found"
        assert check_count[0] == 1

    def test_poll_condition_timeout(self):
        """Test poll_condition when timeout occurs."""
        from wait_utils import WaitUtils

        def check_fn():
            return None

        result = WaitUtils.poll_condition(check_fn, timeout_sec=0.3, interval_sec=0.1)
        assert result.found is False
        assert result.timed_out is True

    def test_poll_condition_disappear(self):
        """Test poll_condition with disappear=True."""
        from wait_utils import WaitUtils

        check_count = [0]

        def check_fn():
            check_count[0] += 1
            if check_count[0] < 3:
                return "still here"
            return None

        result = WaitUtils.poll_condition(
            check_fn, timeout_sec=5.0, interval_sec=0.01, disappear=True
        )
        assert result.found is True
        assert result.data is None

    def test_poll_list_condition_found(self):
        """Test poll_list_condition when items are found."""
        from wait_utils import WaitUtils
        from models import ElementInfo, Bounds

        mock_matches = [
            ElementInfo(
                element_id="1",
                window_id="12345",
                text="Match",
                bounds=Bounds(x=0, y=0, width=10, height=10),
            )
        ]

        result = WaitUtils.poll_list_condition(
            lambda: mock_matches, timeout_sec=5.0, interval_sec=0.1
        )
        assert result.found is True
        assert len(result.data) == 1

    def test_poll_list_condition_disappear(self):
        """Test poll_list_condition with disappear=True."""
        from wait_utils import WaitUtils

        check_count = [0]

        def check_fn():
            check_count[0] += 1
            if check_count[0] < 2:
                return ["item"]
            return []

        result = WaitUtils.poll_list_condition(
            check_fn, timeout_sec=5.0, interval_sec=0.01, disappear=True
        )
        assert result.found is True


class TestWaitCLI:
    """Tests for wait command CLI argument parsing."""

    def test_wait_sleep_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["wait", "sleep", "1000"])
        assert args.command == "wait"
        assert args.wait_command == "sleep"
        assert args.duration_ms == 1000

    def test_wait_window_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["wait", "window", "Notepad", "--timeout", "10"])
        assert args.command == "wait"
        assert args.wait_command == "window"
        assert args.title == "Notepad"
        assert args.timeout == 10.0

    def test_wait_window_exact_flag(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["wait", "window", "Notepad", "--exact"])
        assert args.exact is True

    def test_wait_window_disappear_flag(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["wait", "window", "Notepad", "--disappear"])
        assert args.disappear is True

    def test_wait_text_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(
            ["wait", "--window-id", "12345", "text", "Hello", "--timeout", "5"]
        )
        assert args.command == "wait"
        assert args.wait_command == "text"
        assert args.window_id == 12345
        assert args.text == "Hello"
        assert args.timeout == 5.0

    def test_wait_uia_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args([
            "wait", "--window-id", "12345", "uia",
            "--text", "Button",
            "--control-type", "Button",
            "--automation-id", "btn1"
        ])
        assert args.command == "wait"
        assert args.wait_command == "uia"
        assert args.window_id == 12345
        assert args.text == "Button"
        assert args.control_type == "Button"
        assert args.automation_id == "btn1"

    def test_wait_ocr_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args([
            "wait", "--window-id", "12345", "ocr", "Text",
            "--confidence-threshold", "0.8"
        ])
        assert args.command == "wait"
        assert args.wait_command == "ocr"
        assert args.text == "Text"
        assert args.confidence_threshold == 0.8

    def test_wait_image_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args([
            "wait", "--window-id", "12345", "image",
            "--image-path", "button.png",
            "--threshold", "0.95"
        ])
        assert args.command == "wait"
        assert args.wait_command == "image"
        assert args.image_path == "button.png"
        assert args.threshold == 0.95


class TestClipboardDriver:
    """Tests for ClipboardDriver class."""

    def test_copy_text_to_clipboard_success(self):
        """Test copy_text_to_clipboard succeeds."""
        from clipboard_driver import ClipboardDriver

        with patch("clipboard_driver.win32clipboard"):
            with patch("clipboard_driver.pywintypes"):
                result = ClipboardDriver.copy_text_to_clipboard("test text")
                assert result is True

    def test_copy_text_to_clipboard_none(self):
        """Test copy_text_to_clipboard with None text."""
        from clipboard_driver import ClipboardDriver

        result = ClipboardDriver.copy_text_to_clipboard(None)
        assert result is False

    def test_copy_files_to_clipboard_success(self):
        """Test copy_files_to_clipboard succeeds."""
        from clipboard_driver import ClipboardDriver

        with patch("clipboard_driver.win32clipboard"):
            with patch("clipboard_driver.pywintypes"):
                result = ClipboardDriver.copy_files_to_clipboard(["C:\\file1.txt", "C:\\file2.txt"])
                assert result is True

    def test_copy_files_to_clipboard_empty(self):
        """Test copy_files_to_clipboard with empty list."""
        from clipboard_driver import ClipboardDriver

        result = ClipboardDriver.copy_files_to_clipboard([])
        assert result is False

    def test_get_text_from_clipboard_success(self):
        """Test get_text_from_clipboard returns text."""
        from clipboard_driver import ClipboardDriver

        with patch("clipboard_driver.win32clipboard.OpenClipboard"):
            with patch("clipboard_driver.win32clipboard.CloseClipboard"):
                with patch(
                    "clipboard_driver.win32clipboard.IsClipboardFormatAvailable",
                    return_value=True,
                ):
                    with patch(
                        "clipboard_driver.win32clipboard.GetClipboardData",
                        return_value="clipboard text",
                    ):
                        result = ClipboardDriver.get_text_from_clipboard()
                        assert result == "clipboard text"

    def test_get_text_from_clipboard_no_text(self):
        """Test get_text_from_clipboard when no text available."""
        from clipboard_driver import ClipboardDriver

        with patch("clipboard_driver.win32clipboard.OpenClipboard"):
            with patch("clipboard_driver.win32clipboard.CloseClipboard"):
                with patch(
                    "clipboard_driver.win32clipboard.IsClipboardFormatAvailable",
                    return_value=False,
                ):
                    result = ClipboardDriver.get_text_from_clipboard()
                    assert result is None


class TestClipboardCLI:
    """Tests for clipboard command CLI argument parsing."""

    def test_clipboard_copy_text_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["clipboard", "copy-text", "Hello World"])
        assert args.command == "clipboard"
        assert args.clipboard_command == "copy-text"
        assert args.text == "Hello World"

    def test_clipboard_copy_files_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["clipboard", "copy-files", "C:\\file1.txt", "C:\\file2.txt"])
        assert args.command == "clipboard"
        assert args.clipboard_command == "copy-files"
        assert args.files == ["C:\\file1.txt", "C:\\file2.txt"]

    def test_clipboard_get_text_command(self):
        from winguictl import build_parser

        parser = build_parser()
        args = parser.parse_args(["clipboard", "get-text"])
        assert args.command == "clipboard"
        assert args.clipboard_command == "get-text"


class TestPreprocessWindowId:
    """Tests for _preprocess_window_id function."""

    def test_preprocess_window_id_at_start(self):
        from winguictl import _preprocess_window_id

        argv = ["--window-id", "12345", "window", "focus"]
        result = _preprocess_window_id(argv)
        assert result[0] == "window"
        assert result[1] == "--window-id"
        assert result[2] == "12345"
        assert result[3] == "focus"

    def test_preprocess_window_id_at_end(self):
        from winguictl import _preprocess_window_id

        argv = ["window", "focus", "--window-id", "12345"]
        result = _preprocess_window_id(argv)
        assert result[0] == "window"
        assert result[1] == "--window-id"
        assert result[2] == "12345"

    def test_preprocess_window_id_with_equals(self):
        from winguictl import _preprocess_window_id

        argv = ["--window-id=12345", "window", "focus"]
        result = _preprocess_window_id(argv)
        assert result[0] == "window"
        assert result[1] == "--window-id"
        assert result[2] == "12345"

    def test_preprocess_window_id_no_window_id(self):
        from winguictl import _preprocess_window_id

        argv = ["window", "list"]
        result = _preprocess_window_id(argv)
        assert result == argv

    def test_preprocess_window_id_wait_command(self):
        from winguictl import _preprocess_window_id

        argv = ["--window-id", "12345", "wait", "uia", "--text", "Button"]
        result = _preprocess_window_id(argv)
        assert result[0] == "wait"
        assert result[1] == "--window-id"
        assert result[2] == "12345"
