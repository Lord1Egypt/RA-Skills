#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Win32 control operation driver module.

Operates on native Win32 controls through pywinauto's Win32 backend,
including text reading/writing, clicking, key input, button/combobox/listbox operations, etc.
Also provides snapshot functionality for HWND control trees.
"""

import logging
from typing import Optional

import win32gui

from pywinauto.controls.hwndwrapper import HwndWrapper
from pywinauto.controls.win32_controls import (
    ButtonWrapper,
    ComboBoxWrapper,
    EditWrapper,
    ListBoxWrapper,
)

from constants import WIN32_CONTROL_TYPE_MAP
from models import Bounds, ElementFormatter
from win32_utils import Win32API

_logger = logging.getLogger(__name__)


class Win32Driver:
    """Driver class for Win32 control operations."""

    @staticmethod
    def infer_control_type(class_name: Optional[str]) -> Optional[str]:
        """Infer control type from window class name.

        Matching strategy (by priority):
        1. Exact match (case-insensitive)
        2. Prefix match (case-insensitive, pattern must be at least 3 characters)
           Requires delimiter (dot/underscore) after prefix to avoid false positives
           like "ButtonCustom" matching "Button"
        """
        if not class_name:
            return None
        class_lower = class_name.lower()
        prefix_match: Optional[str] = None
        for pattern, control_type in WIN32_CONTROL_TYPE_MAP.items():
            pattern_lower = pattern.lower()
            if pattern_lower == class_lower:
                return control_type
            if prefix_match is None and len(pattern) >= 3 and class_lower.startswith(pattern_lower):
                remaining = class_lower[len(pattern):]
                if remaining and remaining[0] in (".", "_"):
                    prefix_match = control_type
        return prefix_match

    @staticmethod
    def set_text(hwnd: int, text: str) -> None:
        """Set the text content of an edit control."""
        EditWrapper(hwnd).set_edit_text(text)

    @staticmethod
    def get_text(hwnd: int) -> str:
        """Get the text content of an edit control."""
        return EditWrapper(hwnd).text_block()

    @staticmethod
    def set_focus(hwnd: int) -> None:
        """Set focus to the specified control."""
        Win32API.set_focus(hwnd)

    @staticmethod
    def click(hwnd: int, button: str = "left") -> None:
        """Click the control.

        Note:
            This uses HwndWrapper.click() which sends WM_*BUTTONDOWN/UP messages.
            It works even when the control is hidden beneath other windows,
            but does not produce visual mouse movement. For a more realistic
            click with mouse_event(), use click_input() via pywinauto directly.
        """
        HwndWrapper(hwnd).click(button=button)

    @staticmethod
    def double_click(hwnd: int, button: str = "left") -> None:
        """Double-click the control."""
        HwndWrapper(hwnd).double_click(button=button)

    @staticmethod
    def right_click(hwnd: int) -> None:
        """Right-click the control."""
        HwndWrapper(hwnd).right_click()

    @staticmethod
    def type_keys(hwnd: int, keys: str) -> None:
        """Send key sequence to the control (pywinauto format)."""
        HwndWrapper(hwnd).type_keys(keys)

    @staticmethod
    def send_chars(hwnd: int, chars: str) -> None:
        """Send characters to an inactive window."""
        HwndWrapper(hwnd).send_chars(chars)

    @staticmethod
    def send_keystrokes(hwnd: int, keystrokes: str) -> None:
        """Send keystrokes to an inactive window (pywinauto format)."""
        HwndWrapper(hwnd).send_keystrokes(keystrokes)

    @staticmethod
    def check(hwnd: int) -> None:
        """Check a checkbox.

        Note:
            This uses BM_SETCHECK which sets the visual state but does NOT post
            BN_CLICKED or WM_COMMAND to the parent window. Application-side event
            handlers (e.g., OnBnClicked) will not fire. If the application reacts
            to checkbox changes, use check_by_click() instead to simulate user interaction.
        """
        ButtonWrapper(hwnd).check()

    @staticmethod
    def uncheck(hwnd: int) -> None:
        """Uncheck a checkbox.

        Note:
            This uses BM_SETCHECK which sets the visual state but does NOT post
            BN_CLICKED or WM_COMMAND to the parent window. Application-side event
            handlers (e.g., OnBnClicked) will not fire. If the application reacts
            to checkbox changes, use check_by_click() instead to simulate user interaction.
        """
        ButtonWrapper(hwnd).uncheck()

    @staticmethod
    def check_by_click(hwnd: int) -> None:
        """Check a checkbox by simulating a click.

        This method clicks the checkbox to check it, which triggers BN_CLICKED
        and WM_COMMAND notifications to the parent window. Use this when the
        application needs to react to the checkbox change event.

        If the checkbox is already checked, this method does nothing.

        Note:
            For three-state checkboxes in the indeterminate state, a single click
            cycles to unchecked (not checked). To reliably check a three-state
            checkbox, you may need to call this method multiple times or check
            the state first.
        """
        ButtonWrapper(hwnd).check_by_click()

    @staticmethod
    def uncheck_by_click(hwnd: int) -> None:
        """Uncheck a checkbox by simulating a click.

        This method clicks the checkbox to uncheck it, which triggers BN_CLICKED
        and WM_COMMAND notifications to the parent window. Use this when the
        application needs to react to the checkbox change event.

        If the checkbox is already unchecked, this method does nothing.

        Note:
            For three-state checkboxes in the indeterminate state, a single click
            cycles to checked (not unchecked). To reliably uncheck a three-state
            checkbox, you may need to call this method multiple times or check
            the state first.
        """
        ButtonWrapper(hwnd).uncheck_by_click()

    @staticmethod
    def is_checked(hwnd: int) -> Optional[bool]:
        """Get the checked state of a checkbox.

        Returns:
            True if checked, False if unchecked or not a checkbox,
            None if indeterminate (three-state checkbox).

        Note:
            This returns Optional[bool] for Win32 checkboxes, while UIA's get_toggle_state
            returns int (0=off, 1=on, 2=indeterminate). Both patterns match their underlying
            API conventions.
        """
        return ButtonWrapper(hwnd).is_checked()

    @staticmethod
    def combo_select(hwnd: int, item: int | str) -> None:
        """Select an item in a combobox (by index or text)."""
        ComboBoxWrapper(hwnd).select(item)

    @staticmethod
    def combo_items(hwnd: int) -> list[str]:
        """Get all item texts in a combobox."""
        return ComboBoxWrapper(hwnd).item_texts()

    @staticmethod
    def combo_selected_index(hwnd: int) -> int:
        """Get the selected item index in a combobox."""
        return ComboBoxWrapper(hwnd).selected_index()

    @staticmethod
    def combo_selected_text(hwnd: int) -> Optional[str]:
        """Get the selected item text in a combobox.

        Returns None if no item is selected (selected_index returns CB_ERR = -1).

        Note:
            Uses ComboBoxWrapper.selected_text() which calls item_texts()
            internally. This strips left-to-right mark characters (\\u200e)
            that appear in RTL locale controls, consistent with combo_items().
        """
        cb = ComboBoxWrapper(hwnd)
        idx = cb.selected_index()
        if idx < 0:
            return None
        return cb.selected_text()

    @staticmethod
    def listbox_select(
        hwnd: int,
        item: int | str | list[int] | list[str] | tuple[int, ...] | tuple[str, ...]
    ) -> None:
        """Select an item in a listbox (by index or text).

        For multi-selection listboxes, pass a list or tuple of indices or texts.
        Note: Single-selection listboxes will raise an error if given multiple items.
        """
        ListBoxWrapper(hwnd).select(item)

    @staticmethod
    def listbox_items(hwnd: int) -> list[str]:
        """Get all item texts in a listbox."""
        return ListBoxWrapper(hwnd).item_texts()

    @staticmethod
    def listbox_selected_indices(hwnd: int) -> tuple[int, ...]:
        """Get the indices of all selected items in a listbox."""
        return ListBoxWrapper(hwnd).selected_indices()

    @staticmethod
    def snapshot_hwnd_tree(window_id: int, max_depth: Optional[int] = None) -> str:
        """Generate an HWND control tree snapshot for the window.

        Traverses the target window and all its descendant controls,
        formatting each control's handle, text, class name, visibility,
        enabled state, and bounds information.

        Uses iterative DFS with an explicit stack to avoid RecursionError
        on deeply nested control trees.

        Args:
            window_id: Target window handle
            max_depth: Maximum tree depth to traverse (default: unlimited).
                       The root window is at depth 0. Set to 1 for only direct children.

        Note:
            Uses win32gui.EnumChildWindows to enumerate only direct children
            of each node (filtered by GetParent), avoiding the O(n²) wrapper
            creation that would result from HwndWrapper.children() which calls
            EnumChildWindows recursively for ALL descendants at every level.

        Returns coordinates relative to the window (not screen absolute).
        """
        lines: list[str] = []
        visited: set[int] = set()

        window_bounds_result = Win32API.get_window_bounds(window_id)
        window_bounds = window_bounds_result.value if window_bounds_result.is_ok else None
        win_x = window_bounds.x if window_bounds else 0
        win_y = window_bounds.y if window_bounds else 0

        def _get_direct_child_hwnds(parent_hwnd: int) -> list[int]:
            result: list[int] = []
            try:

                def _enum_cb(child_hwnd, _):
                    if win32gui.GetParent(child_hwnd) == parent_hwnd:
                        result.append(child_hwnd)

                win32gui.EnumChildWindows(parent_hwnd, _enum_cb, None)
            except Exception:  # pylint: disable=broad-exception-caught
                _logger.exception("Failed to enumerate child windows for %d", parent_hwnd)
            return result

        stack: list[tuple[int, int]] = [(window_id, 0)]
        while stack:
            hwnd, level = stack.pop()
            if hwnd in visited:
                continue
            visited.add(hwnd)
            text = Win32API.get_window_text(hwnd)
            cls = Win32API.get_class_name(hwnd)
            visible = win32gui.IsWindowVisible(hwnd) != 0
            enabled = win32gui.IsWindowEnabled(hwnd) != 0
            control_id = win32gui.GetDlgCtrlID(hwnd)
            control_type = Win32Driver.infer_control_type(cls)

            bounds_result = Win32API.get_window_bounds(hwnd)
            rect_tuple: Optional[tuple[int, int, int, int]] = None
            if bounds_result.is_ok:
                relative_bounds = Bounds.from_bounds_relative(bounds_result.value, win_x, win_y)
                rect_tuple = (relative_bounds.x, relative_bounds.y, relative_bounds.width, relative_bounds.height)

            lines.append(ElementFormatter.format_hwnd(hwnd, text, cls, visible, enabled, control_id, level, control_type, rect_tuple))

            if max_depth is None or level < max_depth:
                for child_hwnd in reversed(_get_direct_child_hwnds(hwnd)):
                    stack.append((child_hwnd, level + 1))

        return "\n".join(lines)
