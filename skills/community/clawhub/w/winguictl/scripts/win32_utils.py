#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Win32 API low-level utility module.

Wraps Win32 API calls for window screenshots, mouse clicks,
dragging, text input, key sending and other low-level operations.
Prefers pywin32 (win32gui/win32api/win32ui) wrapped APIs,
falling back to ctypes only for interfaces not wrapped by pywin32
(e.g. PrintWindow). All methods are static.
"""

import ctypes
import logging
import time
from ctypes import wintypes
from pathlib import Path


import win32api
import win32con
import win32gui
import win32ui
from PIL import Image

from constants import (
    DEFAULT_CLICK_DELAY_MS,
    DEFAULT_DRAG_START_DELAY_MS,
    DEFAULT_DRAG_STEP_INTERVAL_MS,
    DEFAULT_HOTKEY_DELAY_MS,
    DEFAULT_KEY_DELAY_MS,
    SENDINPUT_ABSOLUTE_MAX,
    VK_CODE_MAP,
)
from models import Bounds, Err, Ok, Result

_logger = logging.getLogger(__name__)

# SendInput structures for modern input simulation
class MOUSEINPUT(ctypes.Structure):
    """Mouse input structure for SendInput API."""

    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class KEYBDINPUT(ctypes.Structure):
    """Keyboard input structure for SendInput API."""

    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class InputUnion(ctypes.Union):
    """Union of mouse and keyboard input structures."""

    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
    ]


class INPUT(ctypes.Structure):
    """Input structure for SendInput API."""

    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", InputUnion),
    ]


INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_WHEEL = 0x0800
MOUSEEVENTF_HWHEEL = 0x01000
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

WHEEL_DELTA = 120

PW_RENDERFULLCONTENT = 0x00000002


class Win32API:
    """Win32 API wrapper class for low-level operations."""

    @staticmethod
    def get_window_text(hwnd: int) -> str:
        """Get window title text."""
        return win32gui.GetWindowText(hwnd)

    @staticmethod
    def get_class_name(hwnd: int) -> str:
        """Get window class name."""
        return win32gui.GetClassName(hwnd)

    @staticmethod
    def get_top_level_window(hwnd: int) -> int:
        """Get the top-level parent window of a control.

        Traverses up the parent chain until finding a top-level window
        (a window with no parent or whose parent is the desktop).

        Args:
            hwnd: Control handle

        Returns:
            Top-level window handle (may be the same as input if already top-level)
        """
        current = hwnd
        max_iterations = 1000
        for _ in range(max_iterations):
            parent = win32gui.GetParent(current)
            if parent == 0 or parent is None:
                return current
            current = parent
        _logger.warning("get_top_level_window: max iterations reached for hwnd %d", hwnd)
        return current

    @staticmethod
    def get_hwnd_from_point(x: int, y: int) -> Result[int, str]:
        """Get window handle at the specified screen coordinates.

        Args:
            x: Absolute X coordinate on screen
            y: Absolute Y coordinate on screen

        Returns:
            Ok(hwnd) if found, Err(message) otherwise
        """
        try:
            hwnd = win32gui.WindowFromPoint((x, y))
            if hwnd:
                return Ok(hwnd)
            return Err(f"no window at point ({x}, {y})")
        except win32gui.error as err:
            return Err(f"win32 error getting window from point ({x}, {y}): {err}")
        except Exception as e:  # pylint: disable=broad-exception-caught
            return Err(f"unexpected error getting window from point ({x}, {y}): {e}")

    @staticmethod
    def get_window_bounds(hwnd: int) -> Result[Bounds, str]:
        """Get window screen coordinates and dimensions.

        Args:
            hwnd: Window handle

        Returns:
            Ok(Bounds) on success, Err(message) on failure
        """
        try:
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)
            return Ok(Bounds.from_ltrb(left, top, right, bottom))
        except win32gui.error as err:
            return Err(f"win32 error getting window bounds for hwnd {hwnd}: {err}")
        except Exception as e:  # pylint: disable=broad-exception-caught
            return Err(f"unexpected error getting window bounds for hwnd {hwnd}: {e}")

    @staticmethod
    def get_window_state(hwnd: int) -> tuple[bool, bool]:
        """Get window minimized/maximized state.

        Returns:
            (is_minimized, is_maximized) tuple
        """
        is_minimized = bool(win32gui.IsIconic(hwnd))
        placement = win32gui.GetWindowPlacement(hwnd)
        show_cmd = placement[1]
        is_maximized = show_cmd == win32con.SW_MAXIMIZE
        return is_minimized, is_maximized

    @staticmethod
    def capture_window_bgra(window_id: int) -> tuple[int, int, int, int, bytearray]:
        """Capture window screenshot, returning BGRA pixel data.

        Uses win32gui/win32ui to obtain the window DC and create a bitmap.
        Prefers PrintWindow API (supports background window capture),
        falling back to BitBlt if PrintWindow fails.

        Returns:
            (x, y, width, height, bgra_data) tuple
        """
        left, top, right, bottom = win32gui.GetWindowRect(window_id)
        x, y = int(left), int(top)
        width, height = int(right - left), int(bottom - top)
        if width <= 0 or height <= 0:
            raise RuntimeError(f"invalid window size: {width}x{height}")

        hdc_window = None
        dc = None
        memdc = None
        bmp = None

        try:
            hdc_window = win32gui.GetWindowDC(window_id)
            dc = win32ui.CreateDCFromHandle(hdc_window)
            memdc = dc.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(dc, width, height)
            memdc.SelectObject(bmp)

            result = ctypes.windll.user32.PrintWindow(window_id, memdc.GetSafeHdc(), PW_RENDERFULLCONTENT)
            if not result:
                _logger.warning("PrintWindow failed for hwnd %d, falling back to BitBlt", window_id)
                memdc.BitBlt((0, 0), (width, height), dc, (0, 0), win32con.SRCCOPY)

            bits = bmp.GetBitmapBits(True)
            if not bits:
                raise RuntimeError(f"failed to capture window bitmap for hwnd {window_id}")
            data = bytearray(bits)
        finally:
            if bmp is not None:
                try:
                    win32gui.DeleteObject(bmp.GetHandle())
                except Exception as e:  # pylint: disable=broad-exception-caught
                    _logger.debug("Failed to delete bitmap handle: %s", e)
            if memdc is not None:
                try:
                    memdc.DeleteDC()
                except Exception as e:  # pylint: disable=broad-exception-caught
                    _logger.debug("Failed to delete memory DC: %s", e)
            if dc is not None:
                try:
                    dc.DeleteDC()
                except Exception as e:  # pylint: disable=broad-exception-caught
                    _logger.debug("Failed to delete DC: %s", e)
            if hdc_window is not None:
                try:
                    win32gui.ReleaseDC(window_id, hdc_window)
                except Exception as e:  # pylint: disable=broad-exception-caught
                    _logger.debug("Failed to release window DC: %s", e)
        return x, y, width, height, data

    @staticmethod
    def write_image(output: Path, width: int, height: int, bgra_data: bytearray, fmt: str = "PNG") -> None:
        """Write BGRA pixel data to an image file using Pillow.

        Args:
            output: Output file path
            width: Image width in pixels
            height: Image height in pixels
            bgra_data: BGRA pixel data as bytearray
            fmt: Image format (PNG, BMP, etc.)
        """
        img = Image.frombytes("RGBA", (width, height), bytes(bgra_data), "raw", "BGRA")
        img.save(output, fmt.upper())

    @staticmethod
    def send_click(x: int, y: int) -> None:
        """Perform a left mouse button click at the specified screen coordinates.

        Uses SendInput API for better DPI scaling and multi-monitor support.

        Raises:
            RuntimeError: If SendInput fails to inject all inputs (possible UIPI restriction)
        """
        width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        nx = int(x * SENDINPUT_ABSOLUTE_MAX / width) if width > 0 else 0
        ny = int(y * SENDINPUT_ABSOLUTE_MAX / height) if height > 0 else 0

        inputs = (INPUT * 3)()
        inputs[0].type = INPUT_MOUSE
        inputs[0].union.mi.dx = nx
        inputs[0].union.mi.dy = ny
        inputs[0].union.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
        inputs[1].type = INPUT_MOUSE
        inputs[1].union.mi.dx = nx
        inputs[1].union.mi.dy = ny
        inputs[1].union.mi.dwFlags = MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_ABSOLUTE
        inputs[2].type = INPUT_MOUSE
        inputs[2].union.mi.dx = nx
        inputs[2].union.mi.dy = ny
        inputs[2].union.mi.dwFlags = MOUSEEVENTF_LEFTUP | MOUSEEVENTF_ABSOLUTE

        sent = ctypes.windll.user32.SendInput(3, ctypes.byref(inputs), ctypes.sizeof(INPUT))
        if sent != 3:
            error_code = ctypes.get_last_error()
            raise RuntimeError(f"SendInput failed: only sent {sent} of 3 inputs (error: {error_code})")

    @staticmethod
    def send_drag(x1: int, y1: int, x2: int, y2: int, duration_ms: int = 500) -> None:
        """Drag from (x1,y1) to (x2,y2), moving smoothly over the specified duration.

        Uses SendInput API for better DPI scaling and multi-monitor support.

        Note:
            SendInput failures are logged as warnings but do not raise exceptions,
            as partial failures (e.g., only some intermediate move events) may still
            result in acceptable behavior for drag operations.
        """
        width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        def to_absolute(x: int, y: int) -> tuple[int, int]:
            nx = int(x * SENDINPUT_ABSOLUTE_MAX / width) if width > 0 else 0
            ny = int(y * SENDINPUT_ABSOLUTE_MAX / height) if height > 0 else 0
            return nx, ny

        steps = max(1, duration_ms // DEFAULT_DRAG_STEP_INTERVAL_MS)

        start_x, start_y = to_absolute(x1, y1)
        inputs = (INPUT * 2)()
        inputs[0].type = INPUT_MOUSE
        inputs[0].union.mi.dx = start_x
        inputs[0].union.mi.dy = start_y
        inputs[0].union.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
        inputs[1].type = INPUT_MOUSE
        inputs[1].union.mi.dx = start_x
        inputs[1].union.mi.dy = start_y
        inputs[1].union.mi.dwFlags = MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_ABSOLUTE
        sent = ctypes.windll.user32.SendInput(2, ctypes.byref(inputs), ctypes.sizeof(INPUT))
        if sent != 2:
            _logger.warning("SendDrag: Initial SendInput only sent %d of 2 inputs", sent)
        time.sleep(DEFAULT_DRAG_START_DELAY_MS / 1000)

        for i in range(1, steps + 1):
            t = i / steps
            cx = int(x1 + (x2 - x1) * t)
            cy = int(y1 + (y2 - y1) * t)
            ax, ay = to_absolute(cx, cy)

            move_input = INPUT()
            move_input.type = INPUT_MOUSE
            move_input.union.mi.dx = ax
            move_input.union.mi.dy = ay
            move_input.union.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
            ctypes.windll.user32.SendInput(1, ctypes.byref(move_input), ctypes.sizeof(INPUT))
            time.sleep(duration_ms / 1000 / steps)

        end_x, end_y = to_absolute(x2, y2)
        release_input = INPUT()
        release_input.type = INPUT_MOUSE
        release_input.union.mi.dx = end_x
        release_input.union.mi.dy = end_y
        release_input.union.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE
        ctypes.windll.user32.SendInput(1, ctypes.byref(release_input), ctypes.sizeof(INPUT))

        up_input = INPUT()
        up_input.type = INPUT_MOUSE
        up_input.union.mi.dx = end_x
        up_input.union.mi.dy = end_y
        up_input.union.mi.dwFlags = MOUSEEVENTF_LEFTUP | MOUSEEVENTF_ABSOLUTE
        sent = ctypes.windll.user32.SendInput(1, ctypes.byref(up_input), ctypes.sizeof(INPUT))
        if sent != 1:
            _logger.warning("SendDrag: Final SendInput (button up) failed")

    @staticmethod
    def send_scroll(direction: str, amount: int = 1) -> None:
        """Send mouse wheel scroll events via SendInput.

        Args:
            direction: Scroll direction ("up", "down", "left", "right")
            amount: Number of notches to scroll (default 1)

        Raises:
            ValueError: If direction is invalid
        """
        direction_lower = direction.strip().lower()
        if direction_lower in ("up", "down"):
            flag = MOUSEEVENTF_WHEEL
            delta = WHEEL_DELTA if direction_lower == "up" else -WHEEL_DELTA
        elif direction_lower in ("left", "right"):
            flag = MOUSEEVENTF_HWHEEL
            delta = -WHEEL_DELTA if direction_lower == "left" else WHEEL_DELTA
        else:
            raise ValueError(f"invalid scroll direction: {direction}, expected up/down/left/right")

        for _ in range(amount):
            scroll_input = INPUT()
            scroll_input.type = INPUT_MOUSE
            scroll_input.union.mi.mouseData = delta
            scroll_input.union.mi.dwFlags = flag
            sent = ctypes.windll.user32.SendInput(1, ctypes.byref(scroll_input), ctypes.sizeof(INPUT))
            if sent != 1:
                _logger.warning("SendScroll: SendInput failed for direction=%s", direction)

    @staticmethod
    def move_mouse_to_window_center(window_id: int) -> None:
        """Move mouse cursor to the center of the specified window.

        Args:
            window_id: Window handle
        """
        bounds_result = Win32API.get_window_bounds(window_id)
        if bounds_result.is_err:
            return
        bounds = bounds_result.value
        center_x = bounds.x + bounds.width // 2
        center_y = bounds.y + bounds.height // 2
        win32api.SetCursorPos((center_x, center_y))
        time.sleep(DEFAULT_CLICK_DELAY_MS / 1000)

    @staticmethod
    def send_type_text(text: str) -> None:
        """Type text character by character using Unicode keyboard events via SendInput.

        Supports embedded pywinauto-style special keys, e.g., "abc{ENTER}def".
        Text outside braces is typed as Unicode; text inside braces is treated
        as a virtual key name (see VK_CODE_MAP).
        """
        import re

        # Split text into segments: plain text or {KEY} commands
        # Pattern: either plain text (no braces) or {KEY} (non-empty, no nested braces)
        segments = re.split(r"(\{[^{}]+\})", text)

        for segment in segments:
            if not segment:
                continue
            if segment.startswith("{") and segment.endswith("}"):
                # Special key command
                key_name = segment[1:-1]
                virtual_key = VK_CODE_MAP.get(key_name.lower())
                if virtual_key is None:
                    raise ValueError(f"unsupported key in type text: {segment}")
                inputs = (INPUT * 2)()
                inputs[0].type = INPUT_KEYBOARD
                inputs[0].union.ki.wVk = virtual_key
                inputs[1].type = INPUT_KEYBOARD
                inputs[1].union.ki.wVk = virtual_key
                inputs[1].union.ki.dwFlags = KEYEVENTF_KEYUP
                ctypes.windll.user32.SendInput(2, ctypes.byref(inputs), ctypes.sizeof(INPUT))
                time.sleep(DEFAULT_KEY_DELAY_MS / 1000)
            else:
                # Plain text, type as Unicode
                for ch in segment:
                    code_point = ord(ch)
                    inputs = (INPUT * 2)()
                    inputs[0].type = INPUT_KEYBOARD
                    inputs[0].union.ki.wScan = code_point
                    inputs[0].union.ki.dwFlags = KEYEVENTF_UNICODE
                    inputs[1].type = INPUT_KEYBOARD
                    inputs[1].union.ki.wScan = code_point
                    inputs[1].union.ki.dwFlags = KEYEVENTF_UNICODE | KEYEVENTF_KEYUP
                    ctypes.windll.user32.SendInput(2, ctypes.byref(inputs), ctypes.sizeof(INPUT))

    @staticmethod
    def send_press_key(key: str) -> None:
        """Press and release a single virtual key. Uses pywinauto-style braced key names.

        Key must be wrapped in braces, e.g., "{ENTER}", "{ESC}", "{TAB}".
        See VK_CODE_MAP for supported key names.
        """
        normalized_key = key.strip().lower()
        if not (normalized_key.startswith("{") and normalized_key.endswith("}")):
            raise ValueError(f"key must be wrapped in braces, e.g., '{{ENTER}}', got: {key}")
        normalized_key = Win32API._normalize_key(key)
        virtual_key = VK_CODE_MAP.get(normalized_key)
        if virtual_key is None:
            raise ValueError(f"unsupported key: {key}")
        inputs = (INPUT * 2)()
        inputs[0].type = INPUT_KEYBOARD
        inputs[0].union.ki.wVk = virtual_key
        inputs[1].type = INPUT_KEYBOARD
        inputs[1].union.ki.wVk = virtual_key
        inputs[1].union.ki.dwFlags = KEYEVENTF_KEYUP
        ctypes.windll.user32.SendInput(2, ctypes.byref(inputs), ctypes.sizeof(INPUT))
        time.sleep(DEFAULT_KEY_DELAY_MS / 1000)

    @staticmethod
    def _normalize_key(key: str) -> str:
        """Normalize a key string by stripping pywinauto-style braces if present."""
        normalized = key.strip().lower()
        if normalized.startswith("{") and normalized.endswith("}"):
            normalized = normalized[1:-1]
        return normalized

    @staticmethod
    def send_hotkey(keys: list[str] | str) -> None:
        """Press a key chord. Presses all keys in order, then releases in reverse order.

        Supports two calling conventions:
        1. List of braced keys: ["{CTRL}", "{SHIFT}", "{A}"]
        2. Concatenated braced keys: "{CTRL}{SHIFT}{A}"

        All keys must use pywinauto-style braced key names.
        See VK_CODE_MAP for supported key names.
        """
        import re

        # Parse keys from either list or concatenated string
        if isinstance(keys, str):
            # Extract all {KEY} patterns from the string
            parsed_keys = re.findall(r"\{([^{}]+)\}", keys)
            if not parsed_keys:
                raise ValueError(f"no valid braced keys found in: {keys}")
        else:
            parsed_keys = []
            for key in keys:
                normalized_key = key.strip().lower()
                if not (normalized_key.startswith("{") and normalized_key.endswith("}")):
                    raise ValueError(f"key must be wrapped in braces, e.g., '{{ENTER}}', got: {key}")
                parsed_keys.append(normalized_key[1:-1])

        virtual_keys = []
        for key_name in parsed_keys:
            vk = VK_CODE_MAP.get(key_name.lower())
            if vk is None:
                raise ValueError(f"unsupported key: {{{key_name}}}")
            virtual_keys.append(vk)

        down_inputs = (INPUT * len(virtual_keys))()
        for i, vk in enumerate(virtual_keys):
            down_inputs[i].type = INPUT_KEYBOARD
            down_inputs[i].union.ki.wVk = vk
        ctypes.windll.user32.SendInput(len(virtual_keys), ctypes.byref(down_inputs), ctypes.sizeof(INPUT))
        time.sleep(DEFAULT_HOTKEY_DELAY_MS / 1000)

        up_inputs = (INPUT * len(virtual_keys))()
        for i, vk in enumerate(reversed(virtual_keys)):
            up_inputs[i].type = INPUT_KEYBOARD
            up_inputs[i].union.ki.wVk = vk
            up_inputs[i].union.ki.dwFlags = KEYEVENTF_KEYUP
        ctypes.windll.user32.SendInput(len(virtual_keys), ctypes.byref(up_inputs), ctypes.sizeof(INPUT))
        time.sleep(DEFAULT_HOTKEY_DELAY_MS / 1000)

    @staticmethod
    def set_focus(hwnd: int) -> None:
        """Bring the specified window to the foreground and set focus."""
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetFocus(hwnd)

    @staticmethod
    def validate_window_id(window_id: int) -> Result[Bounds, str]:
        """Validate that window_id refers to a valid window.

        Args:
            window_id: Window handle to validate

        Returns:
            Ok(Bounds) if valid, Err(message) if invalid
        """
        result = Win32API.get_window_bounds(window_id)
        if result.is_err:
            return Err(f"window not found: {window_id}")
        return result
