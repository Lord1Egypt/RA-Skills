#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Clipboard driver for Windows.

Provides functions for clipboard operations:
- Copy files to clipboard
- Copy text to clipboard
- Get text from clipboard
"""  # pylint: disable=invalid-name

import ctypes
import logging
from typing import Optional

import pywintypes
import win32clipboard

_logger = logging.getLogger(__name__)


class DROPFILES(ctypes.Structure):  # pylint: disable=invalid-name,too-few-public-methods
    """DROPFILES structure for clipboard file operations."""

    _fields_ = [
        ("pFiles", ctypes.c_uint),
        ("x", ctypes.c_long),
        ("y", ctypes.c_long),
        ("fNC", ctypes.c_int),
        ("fWide", ctypes.c_bool),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.pFiles = ctypes.sizeof(DROPFILES)
        self.fWide = True


class ClipboardDriver:
    """Driver for Windows clipboard operations."""

    @staticmethod
    def copy_files_to_clipboard(filepaths: list[str]) -> bool:
        """Copy files to clipboard.

        Args:
            filepaths: List of absolute file paths to copy

        Returns:
            True if successful, False otherwise
        """
        if not filepaths:
            _logger.warning("No files provided to copy to clipboard")
            return False

        normalized_paths = [path.replace("/", "\\") for path in filepaths]
        files_str = "\0".join(normalized_paths)
        data = files_str.encode("U16")[2:] + b"\0\0"

        p_dropfiles = DROPFILES()

        try:
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_HDROP, bytes(p_dropfiles) + data)
                return True
            finally:
                win32clipboard.CloseClipboard()
        except pywintypes.error as e:  # pylint: disable=no-member
            _logger.exception("Failed to copy files to clipboard: %s", e)
            return False

    @staticmethod
    def copy_text_to_clipboard(text: str) -> bool:
        """Copy text to clipboard.

        Args:
            text: Text to copy

        Returns:
            True if successful, False otherwise
        """
        if text is None:
            _logger.warning("No text provided to copy to clipboard")
            return False

        try:
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
                return True
            finally:
                win32clipboard.CloseClipboard()
        except pywintypes.error as e:  # pylint: disable=no-member
            _logger.exception("Failed to copy text to clipboard: %s", e)
            return False

    @staticmethod
    def get_text_from_clipboard() -> Optional[str]:
        """Get text from clipboard.

        Returns:
            Text from clipboard, or None if no text available
        """
        try:
            win32clipboard.OpenClipboard()
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                    text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                    return text
                return None
            finally:
                win32clipboard.CloseClipboard()
        except pywintypes.error as e:  # pylint: disable=no-member
            _logger.exception("Failed to get text from clipboard: %s", e)
            return None
