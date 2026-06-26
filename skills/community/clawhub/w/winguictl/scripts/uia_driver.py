#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""UIA element operation driver module.

Operates on UI Automation elements through pywinauto's UIA backend,
including clicking, invoking, toggling, text reading/writing, scrolling, selecting, expanding/collapsing,
and combobox/list/tab/slider operations.
Also provides snapshot functionality for UIA element trees.
"""

import itertools
import logging
import re
import threading
from collections import deque
from typing import TYPE_CHECKING, Any, Optional

import win32con
import win32gui

from pywinauto import Desktop
from pywinauto.uia_element_info import UIAElementInfo
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.timings import TimeoutError as PywinautoTimeoutError

from constants import (
    DEFAULT_COMBOBOX_DROPDOWN_TIMEOUT_MS,
)
from models import ElementFormatter

if TYPE_CHECKING:
    from pywinauto.controls.uiawrapper import UiaWrapper

_logger = logging.getLogger(__name__)

_uia_desktop: Optional[Desktop] = None
_uia_desktop_lock = threading.Lock()


def _get_uia_desktop() -> Desktop:
    """Get or create a cached UIA Desktop instance.

    Thread-safe: uses a lock to prevent race conditions when
    multiple threads access the desktop for the first time.
    """
    global _uia_desktop
    if _uia_desktop is None:
        with _uia_desktop_lock:
            if _uia_desktop is None:
                _uia_desktop = Desktop(backend="uia")
    return _uia_desktop


_PATTERN_TO_ACTIONS: dict[str, list[str]] = {
    "InvokePattern": ["invoke"],
    "ValuePattern": ["get-value", "set-value", "set-text", "get-text"],
    "TextPattern": ["get-text"],
    "TogglePattern": ["toggle", "get-toggle-state"],
    "ExpandCollapsePattern": ["expand", "collapse", "is-expanded"],
    "ScrollPattern": ["scroll"],
    "SelectionPattern": ["list-selected-items"],
    "SelectionItemPattern": ["select", "is-selected", "combo-select", "list-select", "tab-select"],
    "RangeValuePattern": ["slider-value", "slider-set", "slider-min", "slider-max"],
    "WindowPattern": ["window-close", "window-state", "window-minimize", "window-maximize", "window-restore"],
    "TransformPattern": ["transform-move", "transform-resize", "transform-rotate"],
}

_PATTERN_CAN_CHECK: dict[str, dict[str, tuple[str, bool]]] = {
    "ValuePattern": {
        "set-value": ("CurrentIsReadOnly", True),
        "set-text": ("CurrentIsReadOnly", True),
    },
    "WindowPattern": {
        "window-minimize": ("CurrentCanMinimize", False),
        "window-maximize": ("CurrentCanMaximize", False),
    },
    "TransformPattern": {
        "transform-move": ("CurrentCanMove", False),
        "transform-resize": ("CurrentCanResize", False),
        "transform-rotate": ("CurrentCanRotate", False),
    },
}


def get_supported_actions(element_info: UIAElementInfo) -> list[str]:
    """Get the list of uia-control actions supported by an element.

    Uses IUIAutomation.PollForPotentialSupportedPatterns to discover
    all patterns an element supports, then maps them to winguictl
    uia-control subcommand names. For WindowPattern and TransformPattern,
    checks Can* properties to filter actions that are actually available.

    Args:
        element_info: UIA element info object

    Returns:
        List of supported uia-control action names (e.g. ['invoke', 'get-value', 'set-value'])
    """
    try:
        from pywinauto.uia_defines import IUIA, NoPatternInterfaceError, get_elem_interface
        element = element_info._element  # pylint: disable=protected-access
        _, names = IUIA().iuia.PollForPotentialSupportedPatterns(element)
        actions: list[str] = []
        seen: set[str] = set()
        for name in names:
            mapped = _PATTERN_TO_ACTIONS.get(name, [])
            can_check = _PATTERN_CAN_CHECK.get(name)
            if can_check:
                try:
                    pattern_name = name.replace("Pattern", "")
                    iface = get_elem_interface(element, pattern_name)
                except (NoPatternInterfaceError, Exception):  # pylint: disable=broad-exception-caught
                    _logger.exception("Failed to get pattern interface %s", name)
                    continue
                for action in mapped:
                    if action in can_check:
                        attr, negate = can_check[action]
                        val = getattr(iface, attr, False)
                        if negate:
                            val = not val
                        if val:
                            if action not in seen:
                                seen.add(action)
                                actions.append(action)
                    else:
                        if action not in seen:
                            seen.add(action)
                            actions.append(action)
            else:
                for action in mapped:
                    if action not in seen:
                        seen.add(action)
                        actions.append(action)
        return actions
    except Exception:  # pylint: disable=broad-exception-caught
        _logger.exception("Failed to get supported patterns")
        return []


_PATTERN_STATE: dict[str, list[tuple[str, str]]] = {
    "TogglePattern": [("toggle_state", "CurrentToggleState")],
    "ExpandCollapsePattern": [("is_expanded", "CurrentExpandCollapseState")],
    "SelectionItemPattern": [("is_selected", "CurrentIsSelected")],
    "RangeValuePattern": [("slider_value", "CurrentValue")],
    "WindowPattern": [("window_state", "CurrentWindowVisualState")],
}


def get_element_state(element_info: UIAElementInfo) -> dict[str, Any]:
    """Get state information for a UIA element based on its supported patterns.

    Args:
        element_info: UIA element info object

    Returns:
        Dictionary of state key-value pairs (e.g. {"toggle_state": 1, "is_selected": True})
    """
    try:
        from pywinauto.uia_defines import IUIA, NoPatternInterfaceError, get_elem_interface
        element = element_info._element  # pylint: disable=protected-access
        _, names = IUIA().iuia.PollForPotentialSupportedPatterns(element)
        state: dict[str, Any] = {}
        for name in names:
            state_attrs = _PATTERN_STATE.get(name)
            if not state_attrs:
                continue
            try:
                pattern_name = name.replace("Pattern", "")
                iface = get_elem_interface(element, pattern_name)
            except (NoPatternInterfaceError, Exception):  # pylint: disable=broad-exception-caught
                _logger.exception("Failed to get pattern interface for state %s", name)
                continue
            for key, attr in state_attrs:
                try:
                    state[key] = getattr(iface, attr)
                except Exception:  # pylint: disable=broad-exception-caught
                    _logger.exception("Failed to get state attribute %s", attr)
        return state
    except Exception:  # pylint: disable=broad-exception-caught
        _logger.exception("Failed to get element state")
        return {}


class UIAOperationError(RuntimeError):
    """Base exception for UIA operation failures."""


class UIAElementNotFoundError(UIAOperationError):
    """Raised when a UIA element cannot be found."""


class UIATimeoutError(UIAOperationError):
    """Raised when a UIA operation times out."""


class UIAAttributeError(UIAOperationError):
    """Raised when a required UIA attribute is not available."""


class UIADriver:
    """Driver class for UIA element operations."""

    @staticmethod
    def _get_uia_wrapper(window_id: int, element_id: str) -> "UiaWrapper":
        """Find and return the UIA element wrapper based on element_id.

        Search strategy:
        1. Strip "uia-" prefix if present (added by _get_uia_element_id)
        2. Detect query format: runtime_id (hyphen-separated integers) vs automation_id
        3. Search by runtime_id if format matches, otherwise by automation_id
        4. Fall back to pywinauto's conditional search by automation_id
        5. Raise UIAElementNotFoundError if not found

        Args:
            window_id: Parent window handle
            element_id: Element identifier (automation_id, runtime_id, or uia-prefixed id)

        Returns:
            Matched pywinauto UIA wrapper (UiaWrapper)

        Raises:
            UIAElementNotFoundError: No matching element found

        Note:
            The visited set tracks runtime_ids to skip duplicate elements, but cannot
            prevent infinite loops if iter_descendants() itself cycles due to a buggy
            UIA provider. For tree snapshotting, use snapshot_uia_tree() which uses
            its own stack-based DFS with cycle detection.
        """
        desktop = _get_uia_desktop()
        wrapper = desktop.window(handle=window_id)

        query = element_id.strip()

        if query.startswith("uia-"):
            query = query[4:]

        if query.startswith("hwnd-"):
            hwnd_str = query[5:]
            try:
                target_hwnd = int(hwnd_str)
            except ValueError as exc:
                raise UIAElementNotFoundError(f"Invalid hwnd format: {query}") from exc
            try:
                return desktop.window(handle=target_hwnd).wrapper_object()
            except (ElementNotFoundError, PywinautoTimeoutError) as e:
                _logger.debug("hwnd lookup for %s failed: %s", target_hwnd, e)
            raise UIAElementNotFoundError(f"UIA element not found by hwnd: {target_hwnd}")

        is_runtime_id_query = bool(re.match(r"^-?\d+(?:--?\d+)+$", query))

        visited: set[tuple[int, ...] | int] = set()
        try:
            root_wrapper = wrapper.wrapper_object()
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("Failed to get root wrapper")
            root_wrapper = None
        candidates = itertools.chain([root_wrapper] if root_wrapper else [], wrapper.iter_descendants())
        for candidate in candidates:
            info = candidate.element_info
            rid = getattr(info, "runtime_id", None)
            if rid:
                rid_tuple = tuple(rid)
            else:
                rid_tuple = id(info)
            if rid_tuple in visited:
                continue
            visited.add(rid_tuple)
            if rid:
                rid_str = "-".join(str(x) for x in rid)
                if is_runtime_id_query and rid_str == query:
                    return candidate
            if not is_runtime_id_query:
                aid = getattr(info, "auto_id", None) or getattr(info, "automation_id", None)
                if aid and aid.strip() == query:
                    return candidate

        if not is_runtime_id_query:
            try:
                try:
                    return wrapper.child_window(auto_id=element_id, found_index=0).wrapper_object()
                except TypeError:
                    return wrapper.child_window(automation_id=element_id, found_index=0).wrapper_object()
            except (ElementNotFoundError, PywinautoTimeoutError):
                _logger.exception("child_window search for auto_id=%s failed", element_id)
            except Exception as e:  # pylint: disable=broad-exception-caught
                _logger.debug("unexpected error in child_window search: %s", e)

        raise UIAElementNotFoundError(f"UIA element not found: {element_id}")

    @staticmethod
    def click(window_id: int, element_id: str) -> None:
        """Click the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).click()

    @staticmethod
    def invoke(window_id: int, element_id: str) -> None:
        """Invoke the UIA element's Invoke pattern (for buttons, menu items, etc.)."""
        UIADriver._get_uia_wrapper(window_id, element_id).invoke()

    @staticmethod
    def toggle(window_id: int, element_id: str) -> None:
        """Toggle the UIA element's Toggle pattern (for checkboxes)."""
        UIADriver._get_uia_wrapper(window_id, element_id).toggle()

    @staticmethod
    def get_toggle_state(window_id: int, element_id: str) -> int:
        """Get the toggle state of the UIA element.

        Returns:
            0=off, 1=on, 2=indeterminate.

        Note:
            This returns int for UIA TogglePattern, while Win32's is_checked returns
            Optional[bool] (True/False/None). Both patterns match their underlying API conventions:
            - UIA ToggleState enum: ToggleState_Off=0, ToggleState_On=1, ToggleState_Indeterminate=2
            - Win32 checkbox: True=checked, False=unchecked, None=indeterminate
        """
        return UIADriver._get_uia_wrapper(window_id, element_id).get_toggle_state()

    @staticmethod
    def get_text(window_id: int, element_id: str) -> str:
        """Get the text content of the UIA element."""
        return UIADriver._get_uia_wrapper(window_id, element_id).window_text()

    @staticmethod
    def set_text(window_id: int, element_id: str, text: str) -> None:
        """Set the text content of a UIA edit control.

        Args:
            window_id: Parent window handle
            element_id: Element identifier
            text: Text content to set

        Raises:
            UIAOperationError: If text cannot be set via either method

        Note:
            For Edit controls, uses set_text() which replaces the entire content.
            For other controls with ValuePattern, uses SetValue() directly.
        """
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        from pywinauto.controls.uia_controls import EditWrapper as UIAEditWrapper
        if isinstance(wrapper, UIAEditWrapper):
            try:
                wrapper.set_text(text)
                return
            except Exception:  # pylint: disable=broad-exception-caught
                _logger.exception("set_text failed on EditWrapper")
        try:
            wrapper.iface_value.SetValue(text)
        except Exception as inner_e:  # pylint: disable=broad-exception-caught
            raise UIAOperationError(f"Failed to set text: {inner_e}") from inner_e

    @staticmethod
    def set_focus(window_id: int, element_id: str) -> None:
        """Set focus to the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).set_focus()

    @staticmethod
    def double_click(window_id: int, element_id: str, button: str = "left") -> None:
        """Double-click the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).double_click_input(button=button)

    @staticmethod
    def right_click(window_id: int, element_id: str) -> None:
        """Right-click the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).right_click_input()

    @staticmethod
    def type_keys(window_id: int, element_id: str, keys: str) -> None:
        """Send key sequence to the UIA element (pywinauto format)."""
        UIADriver._get_uia_wrapper(window_id, element_id).type_keys(keys)

    @staticmethod
    def scroll(window_id: int, element_id: str, direction: str, amount: str = "page", count: int = 1) -> None:
        """Scroll the UIA element.

        Args:
            direction: Scroll direction ("up"/"down"/"left"/"right")
            amount: Scroll amount ("line"/"page")
            count: Number of scrolls
        """
        UIADriver._get_uia_wrapper(window_id, element_id).scroll(direction, amount, count)

    @staticmethod
    def get_value(window_id: int, element_id: str) -> str:
        """Get the current value of the UIA element (via Value pattern)."""
        return UIADriver._get_uia_wrapper(window_id, element_id).iface_value.CurrentValue

    @staticmethod
    def set_value(window_id: int, element_id: str, value: str) -> None:
        """Set the value of the UIA element (via Value pattern)."""
        UIADriver._get_uia_wrapper(window_id, element_id).iface_value.SetValue(value)

    @staticmethod
    def select(window_id: int, element_id: str) -> None:
        """Select the UIA element (for list items, tree items, etc.)."""
        UIADriver._get_uia_wrapper(window_id, element_id).select()

    @staticmethod
    def is_selected(window_id: int, element_id: str) -> bool:
        """Check whether the UIA element is selected.

        Args:
            window_id: Parent window handle
            element_id: Element identifier

        Returns:
            True if selected, False otherwise (including on error)
        """
        try:
            return UIADriver._get_uia_wrapper(window_id, element_id).is_selected()
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("is_selected failed")
            return False

    @staticmethod
    def expand(window_id: int, element_id: str) -> None:
        """Expand the UIA element (for combo boxes, tree nodes, etc.)."""
        UIADriver._get_uia_wrapper(window_id, element_id).expand()

    @staticmethod
    def collapse(window_id: int, element_id: str) -> None:
        """Collapse the UIA element."""
        UIADriver._get_uia_wrapper(window_id, element_id).collapse()

    @staticmethod
    def is_expanded(window_id: int, element_id: str) -> bool:
        """Check whether the UIA element is in expanded state.

        Args:
            window_id: Parent window handle
            element_id: Element identifier

        Returns:
            True if expanded, False otherwise (including on error)
        """
        try:
            return UIADriver._get_uia_wrapper(window_id, element_id).is_expanded()
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("is_expanded failed")
            return False

    @staticmethod
    def combo_select(window_id: int, element_id: str, item: int | str) -> None:
        """Select an item in a UIA combobox."""
        UIADriver._get_uia_wrapper(window_id, element_id).select(item)

    @staticmethod
    def combo_items(
        window_id: int,
        element_id: str,
        dropdown_timeout_ms: int = DEFAULT_COMBOBOX_DROPDOWN_TIMEOUT_MS  # pylint: disable=unused-argument
    ) -> list[str]:
        """Get all item texts in a UIA combobox.

        Uses pywinauto's texts() method which already handles:
        - WinForms (Open button workaround)
        - Qt5 (List child)
        - Win32 fallback via win32_controls.ComboBoxWrapper when handle is available

        Args:
            window_id: Parent window handle
            element_id: Element identifier
            dropdown_timeout_ms: Unused, kept for API compatibility

        Returns:
            List of item text strings
        """
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)

        from pywinauto.controls.uia_controls import ComboBoxWrapper as UIAComboBoxWrapper
        if isinstance(wrapper, UIAComboBoxWrapper):
            try:
                texts = wrapper.texts()
                if texts:
                    return texts
            except Exception:  # pylint: disable=broad-exception-caught
                _logger.exception("texts() failed for UIA combobox")

        return []

    @staticmethod
    def combo_selected_text(window_id: int, element_id: str) -> Optional[str]:
        """Get the selected item text in a UIA combobox.

        Args:
            window_id: Parent window handle
            element_id: Element identifier

        Returns:
            Selected item text or None if no selection

        Note:
            For ComboBoxWrapper, selected_text() already handles get_selection()
            and falls back to iface_value.CurrentValue internally. The get_selection()
            fallback is only useful for generic UIAWrapper instances that have
            SelectionPattern but are not ComboBoxWrapper subclasses.
            get_selection() returns UIAElementInfo objects, so .name accesses
            the element's Name property directly.
        """
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        try:
            return wrapper.selected_text()
        except (AttributeError, TypeError) as e:
            _logger.debug("selected_text() not available: %s", e)
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("selected_text() failed")

        try:
            selection = wrapper.get_selection()
            if selection:
                return selection[0].name
        except (AttributeError, TypeError) as e:
            _logger.debug("get_selection() not available: %s", e)
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("get_selection() failed")

        return None

    @staticmethod
    def combo_selected_index(window_id: int, element_id: str) -> int:  # pylint: disable=too-many-return-statements
        """Get the selected item index in a UIA combobox.

        Strategy:
        1. Try Win32 API directly (most reliable for native ComboBox)
        2. Try wrapper.selected_index() directly
        3. Get selected text and search in items

        Args:
            window_id: Parent window handle
            element_id: Element identifier

        Returns:
            Selected item index (0-based), or -1 if not found
        """
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)

        combo_hwnd = None
        try:
            combo_hwnd = getattr(wrapper.element_info, "handle", None)
        except (AttributeError, TypeError) as e:
            _logger.debug("handle attribute not available: %s", e)

        if combo_hwnd:
            try:
                idx = win32gui.SendMessage(combo_hwnd, win32con.CB_GETCURSEL, 0, 0)
                if idx >= 0:
                    return idx
            except Exception:  # pylint: disable=broad-exception-caught
                _logger.exception("Win32 API CB_GETCURSEL failed for combobox")

        try:
            return wrapper.selected_index()
        except (AttributeError, TypeError) as e:
            _logger.debug("selected_index() not available: %s", e)
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("selected_index() failed")

        selected_text = UIADriver.combo_selected_text(window_id, element_id)
        if selected_text is None:
            return -1

        items = UIADriver.combo_items(window_id, element_id)
        try:
            return items.index(selected_text)
        except ValueError as e:
            _logger.debug("selected_text not found in items: %s", e)

        for i, item in enumerate(items):
            if item.lower() == selected_text.lower():
                return i

        return -1

    @staticmethod
    def list_items(window_id: int, element_id: str) -> list[str]:
        """Get all item texts in a UIA list."""
        items = UIADriver._get_uia_wrapper(window_id, element_id).children(content_only=True)
        return [item.window_text() for item in items]

    @staticmethod
    def list_select(window_id: int, element_id: str, item: int | str) -> None:
        """Select an item in a UIA list."""
        UIADriver._get_uia_wrapper(window_id, element_id).get_item(item).select()

    @staticmethod
    def list_selected_items(window_id: int, element_id: str) -> list[str]:
        """Get all selected item texts in a UIA list."""
        selection = UIADriver._get_uia_wrapper(window_id, element_id).get_selection()
        if selection:
            return [elem.name for elem in selection]
        return []

    @staticmethod
    def tab_select(window_id: int, element_id: str, item: int | str) -> None:
        """Select a UIA tab."""
        UIADriver._get_uia_wrapper(window_id, element_id).select(item)

    @staticmethod
    def tab_selected(window_id: int, element_id: str) -> int:
        """Get the selected tab index in a UIA tab control."""
        return UIADriver._get_uia_wrapper(window_id, element_id).get_selected_tab()

    @staticmethod
    def tab_count(window_id: int, element_id: str) -> int:
        """Get the number of tabs in a UIA tab control."""
        return UIADriver._get_uia_wrapper(window_id, element_id).tab_count()

    @staticmethod
    def slider_value(window_id: int, element_id: str) -> float:
        """Get the current value of a UIA slider."""
        return UIADriver._get_uia_wrapper(window_id, element_id).value()

    @staticmethod
    def slider_set_value(window_id: int, element_id: str, value: float) -> None:
        """Set the value of a UIA slider."""
        UIADriver._get_uia_wrapper(window_id, element_id).set_value(value)

    @staticmethod
    def slider_min(window_id: int, element_id: str) -> float:
        """Get the minimum value of a UIA slider."""
        return UIADriver._get_uia_wrapper(window_id, element_id).min_value()

    @staticmethod
    def slider_max(window_id: int, element_id: str) -> float:
        """Get the maximum value of a UIA slider."""
        return UIADriver._get_uia_wrapper(window_id, element_id).max_value()

    @staticmethod
    def window_close(window_id: int, element_id: str) -> None:
        """Close the window (via WindowPattern)."""
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        try:
            wrapper.iface_window.Close()
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("iface_window.Close failed, falling back to ESC")
            wrapper.type_keys("{ESC}")

    @staticmethod
    def window_minimize(window_id: int, element_id: str) -> None:
        """Minimize the window (via WindowPattern)."""
        from pywinauto.uia_defines import window_visual_state_minimized
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        iface = wrapper.iface_window
        if iface.CurrentCanMinimize:
            iface.SetWindowVisualState(window_visual_state_minimized)
        else:
            raise UIAOperationError("Window cannot be minimized")

    @staticmethod
    def window_maximize(window_id: int, element_id: str) -> None:
        """Maximize the window (via WindowPattern)."""
        from pywinauto.uia_defines import window_visual_state_maximized
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        iface = wrapper.iface_window
        if iface.CurrentCanMaximize:
            iface.SetWindowVisualState(window_visual_state_maximized)
        else:
            raise UIAOperationError("Window cannot be maximized")

    @staticmethod
    def window_restore(window_id: int, element_id: str) -> None:
        """Restore the window to normal size (via WindowPattern)."""
        from pywinauto.uia_defines import window_visual_state_normal
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        wrapper.iface_window.SetWindowVisualState(window_visual_state_normal)

    @staticmethod
    def window_state(window_id: int, element_id: str) -> str:
        """Get the window visual state (via WindowPattern).

        Returns:
            "normal", "maximized", or "minimized"
        """
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        state = wrapper.iface_window.CurrentWindowVisualState
        state_map = {0: "normal", 1: "maximized", 2: "minimized"}
        return state_map.get(state, f"unknown({state})")

    @staticmethod
    def transform_move(window_id: int, element_id: str, x: int, y: int) -> None:
        """Move the element to the specified screen coordinates (via TransformPattern)."""
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        iface = wrapper.iface_transform
        if not iface.CurrentCanMove:
            raise UIAOperationError("Element cannot be moved")
        iface.Move(x, y)

    @staticmethod
    def transform_resize(window_id: int, element_id: str, width: int, height: int) -> None:
        """Resize the element (via TransformPattern)."""
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        iface = wrapper.iface_transform
        if not iface.CurrentCanResize:
            raise UIAOperationError("Element cannot be resized")
        iface.Resize(width, height)

    @staticmethod
    def transform_rotate(window_id: int, element_id: str, degrees: float) -> None:
        """Rotate the element (via TransformPattern)."""
        wrapper = UIADriver._get_uia_wrapper(window_id, element_id)
        iface = wrapper.iface_transform
        if not iface.CurrentCanRotate:
            raise UIAOperationError("Element cannot be rotated")
        iface.Rotate(degrees)

    @staticmethod
    def snapshot_uia_tree(window_id: int, skip_actions: bool = False, skip_state: bool = False, max_depth: Optional[int] = None) -> str:
        """Generate a UIA element tree snapshot for the window.

        Iteratively traverses all UIA child elements of the target window using a stack,
        formatting each element's name, control type, class name, automation ID, etc.
        Uses a visited set to prevent infinite loops from buggy UIA providers.

        Args:
            window_id: Target window handle
            skip_actions: If True, skip collecting supported actions (faster for Qt apps)
            skip_state: If True, skip collecting element state (faster for Qt apps)
            max_depth: Maximum tree depth to traverse (default: unlimited).
                       The root window is at depth 0. Set to 1 for only direct children.

        Note:
            Uses iter_children() which yields children one at a time via TreeWalker.
            Children are prepended to the stack using deque.appendleft() (O(1)) to
            maintain correct DFS visitation order without materializing the entire
            children list.

            When duplicate automation_id values are detected, a warning is prepended
            to the output. runtime_id is preferred for element identification as it
            is guaranteed unique within a desktop session.

        Returns coordinates relative to the window (not screen absolute).
        """
        from find_driver import _check_duplicate_automation_ids
        from win32_utils import Win32API

        desktop = _get_uia_desktop()
        wrapper = desktop.window(handle=window_id)
        lines: list[str] = []

        window_bounds_result = Win32API.get_window_bounds(window_id)
        window_bounds = window_bounds_result.value if window_bounds_result.is_ok else None
        win_x = window_bounds.x if window_bounds else 0
        win_y = window_bounds.y if window_bounds else 0

        visited: set[tuple[int, ...] | int] = set()
        automation_ids: list[str] = []
        stack: deque[tuple[object, int]] = deque([(wrapper, 0)])
        while stack:
            element, level = stack.pop()
            info = element.element_info

            rid = getattr(info, "runtime_id", None)
            elem_key = tuple(rid) if rid else id(info)
            if elem_key in visited:
                continue
            visited.add(elem_key)

            automation_id = (getattr(info, "auto_id", None) or getattr(info, "automation_id", "") or "").strip()
            if automation_id:
                automation_ids.append(automation_id)

            actions = [] if skip_actions else get_supported_actions(info)
            elem_state = {} if skip_state else get_element_state(info)
            lines.append(ElementFormatter.format_uia(info, level, win_x, win_y, supported_actions=actions, state=elem_state))
            if max_depth is None or level < max_depth:
                try:
                    for child in element.iter_children():
                        stack.appendleft((child, level + 1))
                except Exception:  # pylint: disable=broad-exception-caught
                    _logger.exception("iter_children() failed for element")

        result_lines: list[str] = []
        warning = _check_duplicate_automation_ids(automation_ids)
        if warning:
            result_lines.append(warning)

        result_lines.extend(lines)
        return "\n".join(result_lines)

    @staticmethod
    def get_element_at_point(absolute_x: int, absolute_y: int) -> Optional[dict]:
        """Get UIA element information at the specified screen coordinates.

        Args:
            absolute_x: Absolute X coordinate on screen
            absolute_y: Absolute Y coordinate on screen

        Returns:
            Dictionary with element information or None if no element found

        Note:
            UIAElementInfo.from_point() always returns an instance (possibly wrapping
            a null COM pointer). Accessing properties on a null element raises COMError,
            which is caught and returns None.
        """
        try:
            element_info = UIAElementInfo.from_point(absolute_x, absolute_y)

            name = (getattr(element_info, "name", "") or "").strip()
            control_type = (getattr(element_info, "control_type", "") or "").strip() or None
            class_name = (getattr(element_info, "class_name", "") or "").strip() or None
            automation_id = (getattr(element_info, "auto_id", None) or getattr(element_info, "automation_id", "") or "").strip() or None
            runtime_id = getattr(element_info, "runtime_id", None)

            result = {
                "name": name,
                "control_type": control_type,
                "class_name": class_name,
                "automation_id": automation_id,
            }

            if runtime_id:
                result["runtime_id"] = "-".join(str(x) for x in runtime_id)

            return result
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("Failed to get UIA element at point (%d, %d)", absolute_x, absolute_y)
            return None
