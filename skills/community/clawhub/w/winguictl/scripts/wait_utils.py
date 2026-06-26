#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Wait utility functions for condition checking.

Provides helper functions for checking various conditions:
- Window existence
- Text presence
- UIA element presence
- OCR text presence
- Image presence
"""

import logging
import time
from typing import Any, Callable, Generic, Optional, TypeVar

from find_driver import FindDriver
from models import ElementInfo
from ocr_driver import OCRDriver
from win32_utils import Win32API
from windows_driver import WindowsDriver

_logger = logging.getLogger(__name__)

T = TypeVar("T")


class PollResult(Generic[T]):
    """Result of a polling operation.

    Attributes:
        found: Whether the condition was met
        data: The data returned by the check function (if any)
        elapsed_ms: Time elapsed in milliseconds
        timed_out: Whether the operation timed out
    """

    def __init__(self, found: bool, data: Optional[T] = None, elapsed_ms: int = 0, timed_out: bool = False) -> None:
        self.found = found
        self.data = data
        self.elapsed_ms = elapsed_ms
        self.timed_out = timed_out


class WaitUtils:
    """Utility class for checking wait conditions."""

    @staticmethod
    def poll_condition(
        check_fn: Callable[[], Optional[T]],
        timeout_sec: float,
        interval_sec: float,
        disappear: bool = False,
    ) -> PollResult[T]:
        """Poll a condition until it is met or timeout.

        Args:
            check_fn: Function to check the condition, returns data if found, None otherwise
            timeout_sec: Timeout in seconds
            interval_sec: Poll interval in seconds
            disappear: If True, wait for condition to become False (data is None)

        Returns:
            PollResult with found status, data, and elapsed time
        """
        start_time = time.time()
        while True:
            data = check_fn()
            if disappear:
                if data is None:
                    return PollResult(found=True, elapsed_ms=int((time.time() - start_time) * 1000))
            else:
                if data is not None:
                    return PollResult(found=True, data=data, elapsed_ms=int((time.time() - start_time) * 1000))

            if time.time() - start_time >= timeout_sec:
                return PollResult(found=False, elapsed_ms=int((time.time() - start_time) * 1000), timed_out=True)

            time.sleep(interval_sec)

    @staticmethod
    def poll_list_condition(
        check_fn: Callable[[], list[T]],
        timeout_sec: float,
        interval_sec: float,
        disappear: bool = False,
    ) -> PollResult[list[T]]:
        """Poll a condition that returns a list until it is met or timeout.

        Args:
            check_fn: Function to check the condition, returns list of matches
            timeout_sec: Timeout in seconds
            interval_sec: Poll interval in seconds
            disappear: If True, wait for condition to become False (empty list)

        Returns:
            PollResult with found status, data list, and elapsed time
        """
        start_time = time.time()
        while True:
            data = check_fn()
            if disappear:
                if not data:
                    return PollResult(found=True, elapsed_ms=int((time.time() - start_time) * 1000))
            else:
                if data:
                    return PollResult(found=True, data=data, elapsed_ms=int((time.time() - start_time) * 1000))

            if time.time() - start_time >= timeout_sec:
                return PollResult(found=False, elapsed_ms=int((time.time() - start_time) * 1000), timed_out=True)

            time.sleep(interval_sec)

    @staticmethod
    def check_window_exists(title: str, exact: bool, class_name: Optional[str] = None) -> Optional[dict[str, Any]]:
        """Check if window exists and return its info, or None if not found.

        Args:
            title: Window title to match (supports partial match by default)
            exact: Whether to match title exactly
            class_name: Optional window class name filter

        Returns:
            Window info dict if found, None otherwise
        """
        windows = WindowsDriver.list_windows()
        title_lower = title.casefold()
        for win in windows:
            win_title = (win.title or "").strip()
            win_title_lower = win_title.casefold()
            if exact:
                if win_title_lower != title_lower:
                    continue
            else:
                if title_lower not in win_title_lower:
                    continue
            actual_class = Win32API.get_class_name(int(win.window_id))
            if class_name:
                if actual_class and class_name.casefold() not in actual_class.casefold():
                    continue
            return {
                "window_id": win.window_id,
                "title": win.title,
                "class_name": actual_class,
                "process": win.process_name,
                "pid": win.process_id,
            }
        return None

    @staticmethod
    def check_text_exists(window_id: int, text: str, exact: bool) -> Optional[str]:
        """Check if text exists in window and return matched text.

        Args:
            window_id: Window handle
            text: Text to search for
            exact: Whether to match exactly

        Returns:
            Matched text if found, None otherwise
        """
        try:
            result = FindDriver.find_text(window_id, text, exact)
            if result.strip():
                return result.strip()
            return None
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("Failed to check text existence in window %d", window_id)
            return None

    @staticmethod
    def check_uia_exists(
        window_id: int,
        text: Optional[str] = None,
        control_type: Optional[str] = None,
        class_name: Optional[str] = None,
        automation_id: Optional[str] = None,
        exact: bool = False,
    ) -> Optional[str]:
        """Check if UIA element exists in window and return element info.

        Args:
            window_id: Window handle
            text: Optional element text/name filter
            control_type: Optional control type filter
            class_name: Optional window class name filter
            automation_id: Optional automation ID filter
            exact: Whether to match text exactly

        Returns:
            Element info string if found, None otherwise
        """
        try:
            result = FindDriver.find_uia(
                window_id=window_id,
                text=text,
                control_type=control_type,
                class_name=class_name,
                automation_id=automation_id,
                exact=exact,
                skip_actions=True,
                skip_state=True,
            )
            if result.strip():
                return result.strip()
            return None
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("Failed to check UIA element existence in window %d", window_id)
            return None

    @staticmethod
    def check_ocr_exists(window_id: int, text: str, exact: bool, confidence: float = 0.0) -> list[ElementInfo]:
        """Check if OCR text exists in window and return matched elements.

        Args:
            window_id: Window handle
            text: Text to search for
            exact: Whether to match exactly
            confidence: OCR confidence threshold (default: 0.0)

        Returns:
            List of matched ElementInfo objects (empty if not found)
        """
        try:
            matches = OCRDriver.find_ocr_text(window_id, text, exact, confidence)
            return matches
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("Failed to check OCR text existence in window %d", window_id)
            return []

    @staticmethod
    def check_image_exists(window_id: int, image_path: str, threshold: float = 0.9) -> list[ElementInfo]:
        """Check if image exists in window and return matched positions.

        Args:
            window_id: Window handle
            image_path: Path to template image file
            threshold: Match confidence threshold (default: 0.9)

        Returns:
            List of matched ElementInfo objects (empty if not found)
        """
        try:
            matches = FindDriver.find_image(window_id, image_path, threshold)
            return matches
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("Failed to check image existence in window %d", window_id)
            return []
