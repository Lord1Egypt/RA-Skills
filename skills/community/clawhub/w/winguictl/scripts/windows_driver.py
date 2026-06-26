#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Window management driver module.

Provides window enumeration, focus control, state operations (minimize/maximize/restore/close),
position movement, size adjustment, and screenshot capabilities.
Underlying implementation uses pywinauto's HwndWrapper for window operations.
"""

import logging
import os
from pathlib import Path
from typing import Optional

import win32api
import win32con
import win32gui
import win32process
from pywinauto import Desktop
from pywinauto.controls.hwndwrapper import HwndWrapper
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import TimeoutError as PywinautoTimeoutError
from pywinauto.win32_element_info import HwndElementInfo

from models import Bounds, WindowInfo
from win32_utils import Win32API

_logger = logging.getLogger(__name__)

IMMUNE_CLASS_NAMES = frozenset({"IME", "Default IME", "MSCTFIME UI"})

_win32_desktop: Optional[Desktop] = None


def _get_win32_desktop() -> Desktop:
    """Get or create a cached Win32 Desktop instance."""
    global _win32_desktop
    if _win32_desktop is None:
        _win32_desktop = Desktop(backend="win32")
    return _win32_desktop


class WindowsDriver:
    """Driver class for window management operations."""

    @staticmethod
    def _wrap(window_id: int) -> HwndWrapper:
        """Wrap a window handle as an HwndWrapper instance."""
        return HwndWrapper(HwndElementInfo(window_id))

    @staticmethod
    def _window_action(window_id: int, action_name: str, **kwargs) -> bool:
        """Generic method for executing window operations.

        Centralizes the pattern of _wrap + calling wrapper method + exception handling,
        avoiding duplicate try/except boilerplate in each window operation method.

        Args:
            window_id: Window handle
            action_name: Method name on HwndWrapper
            **kwargs: Parameters to pass to the method

        Returns:
            Whether the operation succeeded
        """
        try:
            wrapper = WindowsDriver._wrap(window_id)
            getattr(wrapper, action_name)(**kwargs)
            return True
        except ElementNotFoundError:
            _logger.warning("window not found for action %s: window_id=%s", action_name, window_id)
            return False
        except PywinautoTimeoutError:
            _logger.warning("timeout during window action %s for window_id=%s", action_name, window_id)
            return False
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("window action %s failed for window_id=%s", action_name, window_id)
            return False

    @staticmethod
    def _get_process_name(pid: int) -> Optional[str]:
        """Get process name by process ID."""
        try:
            process_handle = win32api.OpenProcess(
                win32con.PROCESS_QUERY_LIMITED_INFORMATION, False, pid
            )
            if not process_handle:
                return None
            full_path = win32process.GetModuleFileNameEx(process_handle, 0)
            win32api.CloseHandle(process_handle)
            return os.path.basename(full_path) if full_path else None
        except Exception:  # pylint: disable=broad-exception-caught
            return None

    @staticmethod
    def list_windows() -> list[WindowInfo]:
        """List all visible windows, returning window information list.

        Filters out invisible, untitled, and IME system windows,
        and records parent-child hierarchy (parent_hwnd) for each window.
        """
        windows: list[WindowInfo] = []
        foreground_hwnd = win32gui.GetForegroundWindow()
        desktop = _get_win32_desktop()

        for z_order, w in enumerate(desktop.windows()):
            try:
                info = w.element_info
                rect = getattr(info, "rectangle", None)
                if rect is None:
                    continue
                title = getattr(info, "name", "") or ""
                handle = getattr(info, "handle", None)
                pid = getattr(info, "process_id", None)
                class_name = getattr(info, "class_name", "") or ""
                if not handle:
                    continue
                if not w.is_visible():
                    continue
                if not title.strip():
                    continue
                if class_name in IMMUNE_CLASS_NAMES:
                    continue
                parent_hwnd = win32gui.GetParent(handle)
                windows.append(
                    WindowInfo(
                        window_id=str(handle),
                        title=title,
                        bounds=Bounds.from_rect(rect),
                        process_id=int(pid) if pid else None,
                        process_name=WindowsDriver._get_process_name(pid) if pid else None,
                        is_visible=True,
                        is_minimized=w.is_minimized(),
                        is_maximized=w.is_maximized(),
                        is_foreground=foreground_hwnd == handle,
                        z_order=z_order,
                        parent_hwnd=parent_hwnd if parent_hwnd else None,
                    )
                )
            except Exception:  # pylint: disable=broad-exception-caught
                continue
        return windows

    @staticmethod
    def focus_window(window_id: int) -> bool:
        """Bring window to foreground and give it focus."""
        return WindowsDriver._window_action(window_id, "set_focus")

    @staticmethod
    def minimize_window(window_id: int) -> bool:
        """Minimize the window."""
        return WindowsDriver._window_action(window_id, "minimize")

    @staticmethod
    def maximize_window(window_id: int) -> bool:
        """Maximize the window."""
        return WindowsDriver._window_action(window_id, "maximize")

    @staticmethod
    def restore_window(window_id: int) -> bool:
        """Restore the window from minimized/maximized state."""
        return WindowsDriver._window_action(window_id, "restore")

    @staticmethod
    def close_window(window_id: int) -> bool:
        """Close the window."""
        return WindowsDriver._window_action(window_id, "close")

    @staticmethod
    def move_window(window_id: int, x: int, y: int) -> bool:
        """Move the window to the specified coordinates."""
        return WindowsDriver._window_action(window_id, "move_window", x=x, y=y)

    @staticmethod
    def resize_window(window_id: int, width: int, height: int) -> bool:
        """Resize the window while preserving its current position.

        Note: pywinauto's move_window requires both position and size together,
        so we need to get the current position before resizing.
        """
        try:
            wrapper = WindowsDriver._wrap(window_id)
            rect = wrapper.rectangle()
            wrapper.move_window(x=rect.left, y=rect.top, width=width, height=height)
            return True
        except ElementNotFoundError:
            _logger.warning("window not found for resize: window_id=%s", window_id)
            return False
        except PywinautoTimeoutError:
            _logger.warning("timeout during window resize for window_id=%s", window_id)
            return False
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("resize failed for window_id=%s", window_id)
            return False

    @staticmethod
    def screenshot_window(window_id: int, output: str, rect: Optional[tuple[int, int, int, int]] = None) -> str:
        """Capture window screenshot and save to file.

        Args:
            window_id: Window handle
            output: Output file path (supports .png and .bmp)
            rect: Optional crop region (x, y, width, height), relative to window top-left

        Returns:
            Absolute path of the saved file

        Raises:
            ValueError: If crop region is outside window bounds
        """
        output_path = Path(output)
        win_x, win_y, win_width, win_height, data = Win32API.capture_window_bgra(window_id)
        if rect:
            x, y, width, height = rect
            if x < 0 or y < 0 or width <= 0 or height <= 0:
                raise ValueError(f"Invalid crop region: x={x}, y={y}, width={width}, height={height}")
            if x + width > win_width or y + height > win_height:
                raise ValueError(f"Crop region outside window bounds: window is {win_width}x{win_height}, crop region is {x},{y} {width}x{height}")
            cropped = bytearray()
            for row in range(y, y + height):
                src_start = row * win_width * 4 + x * 4
                cropped.extend(data[src_start : src_start + width * 4])
            data = cropped
            win_width = width
            win_height = height
            win_x += x
            win_y += y
        fmt = "PNG" if output_path.suffix.lower() == ".png" else "BMP"
        Win32API.write_image(output_path, win_width, win_height, data, fmt)
        return str(output_path.absolute())
