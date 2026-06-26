#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT
# pylint: disable=too-many-lines,too-many-return-statements

"""winguictl - Windows desktop automation command-line tool.

Provides a unified CLI entry point for window management, structure snapshotting,
element finding, interaction operations, control manipulation, and screenshot capture.
"""

import argparse
import io
import logging
import sys
from typing import TYPE_CHECKING, Optional

from models import ActionResult, Bounds, ElementFormatter, Err
from output_utils import (
    emit,
    emit_action,
    emit_action_result,
    generate_nonce,
    build_error_context,
    unwrap_result,
    wrap_with_boundary,
)

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

if TYPE_CHECKING:
    from find_driver import FindDriver
    from ocr_driver import OCRDriver
    from output_utils import (
        build_center_payload,
        build_control_info,
        build_point_context,
        build_uia_control_info,
        format_window_tree,
        resolve_window_context,
        validate_relative_coords,
    )
    from uia_driver import UIADriver
    from win32_driver import Win32Driver
    from win32_utils import Win32API
    from windows_driver import WindowsDriver

_logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""
    parser = argparse.ArgumentParser(prog="winguictl", description="Windows automation CLI.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    _build_window_parser(subparsers)
    _build_snapshot_parser(subparsers)
    _build_find_parser(subparsers)
    _build_action_parser(subparsers)
    _build_control_parser(subparsers)
    _build_uia_control_parser(subparsers)
    _build_screenshot_parser(subparsers)
    _build_wait_parser(subparsers)
    _build_clipboard_parser(subparsers)

    return parser


def _build_window_parser(subparsers: argparse._SubParsersAction) -> None:
    """Build the window subcommand parser."""
    p = subparsers.add_parser("window", help="Inspect and control desktop windows.")
    p.add_argument("--window-id", type=int, help="Window handle (required for all subcommands except 'list')")
    sp = p.add_subparsers(dest="window_command", required=True)
    sp.add_parser("list", help="List visible windows.")
    sp.add_parser("focus", help="Focus a window (bring to foreground).")
    sp.add_parser("minimize", help="Minimize a window.")
    sp.add_parser("maximize", help="Maximize a window.")
    sp.add_parser("restore", help="Restore a window.")
    sp.add_parser("close", help="Close a window.")
    move = sp.add_parser("move", help="Move a window to a new position.")
    move.add_argument("--x", type=int, required=True)
    move.add_argument("--y", type=int, required=True)
    resize = sp.add_parser("resize", help="Resize a window.")
    resize.add_argument("--width", type=int, required=True)
    resize.add_argument("--height", type=int, required=True)


def _build_snapshot_parser(subparsers: argparse._SubParsersAction) -> None:
    """Build the snapshot subcommand parser."""
    p = subparsers.add_parser("snapshot", help="Capture window structure snapshots.")
    p.add_argument("--window-id", type=int, required=True)
    sp = p.add_subparsers(dest="snapshot_command", required=True)
    sp.add_parser("hwnd", help="Snapshot HWND tree of a window.")
    uia = sp.add_parser("uia", help="Snapshot UIA tree of a window.")
    uia.add_argument("--skip-actions", action="store_true", help="Skip collecting supported actions (faster)")
    uia.add_argument("--skip-state", action="store_true", help="Skip collecting element state (faster)")
    p.add_argument("--max-depth", type=int, default=None, help="Maximum tree depth to traverse (default: unlimited)")
    sp.add_parser("ocr", help="Snapshot OCR text regions of a window.")


def _build_find_parser(subparsers: argparse._SubParsersAction) -> None:
    """Build the find subcommand parser."""
    p = subparsers.add_parser("find", help="Resolve text or control targets inside a window.")
    p.add_argument("--window-id", type=int, required=True)
    sp = p.add_subparsers(dest="find_command", required=True)

    find_text = sp.add_parser("text", help="Find visible text inside a window.")
    find_text.add_argument("text", help="Text to search for")
    find_text.add_argument("--exact", action="store_true")

    find_uia = sp.add_parser("uia", help="Find UIA controls inside a window.")
    find_uia.add_argument("--text")
    find_uia.add_argument("--control-type")
    find_uia.add_argument("--class", dest="class_name", help="Filter by window class name")
    find_uia.add_argument("--automation-id", help="Filter by automation ID")
    find_uia.add_argument("--action", help="Filter by supported uia-control action (e.g. set-text, invoke)")
    find_uia.add_argument("--exact", action="store_true")
    find_uia.add_argument("--skip-actions", action="store_true", help="Skip collecting supported actions (faster)")
    find_uia.add_argument("--skip-state", action="store_true", help="Skip collecting element state (faster)")

    find_ocr = sp.add_parser("ocr", help="Find OCR text inside a window.")
    find_ocr.add_argument("text", help="Text to search for")
    find_ocr.add_argument("--exact", action="store_true")
    find_ocr.add_argument("--confidence-threshold", type=float, default=0.0)

    find_image = sp.add_parser("image", help="Find an image template inside a window.")
    find_image.add_argument("--image-path", required=True)
    find_image.add_argument("--threshold", type=float, default=0.9, help="Match confidence threshold (0-1)")
    find_image.add_argument("--overlap-threshold", type=float, default=0.5,
                            help="IoU threshold for non-maximum suppression (0-1). Higher values allow more overlapping matches.")


def _build_action_parser(subparsers: argparse._SubParsersAction) -> None:
    """Build the action subcommand parser."""
    p = subparsers.add_parser("action", help="Preview or run actions against a window.")
    p.add_argument("--window-id", type=int, help="Window handle (required for relative coordinates)")
    sp = p.add_subparsers(dest="action_command", required=True)

    click = sp.add_parser("click", help="Click at coordinates or element center.")
    coord_group = click.add_mutually_exclusive_group(required=True)
    coord_group.add_argument("--relative-x", type=int, help="X coordinate relative to window (requires --relative-y and --window-id)")
    coord_group.add_argument("--absolute-x", type=int, help="Absolute screen X coordinate (requires --absolute-y)")
    coord_group.add_argument("--element-id", help="UIA element ID (automation_id or runtime_id), clicks element center")
    click.add_argument("--relative-y", type=int, help="Y coordinate relative to window (requires --relative-x and --window-id)")
    click.add_argument("--absolute-y", type=int, help="Absolute screen Y coordinate (requires --absolute-x)")
    click.add_argument("--dry-run", action="store_true")

    click_image = sp.add_parser("click-image", help="Click the first matching image template.")
    click_image.add_argument("--image-path", required=True)
    click_image.add_argument("--threshold", type=float, default=0.9)
    click_image.add_argument("--dry-run", action="store_true")

    drag = sp.add_parser("drag", help="Drag from one point to another.")
    drag_coord_group = drag.add_mutually_exclusive_group(required=True)
    drag_coord_group.add_argument("--relative-x1", type=int, help="Start X coordinate relative to window")
    drag_coord_group.add_argument("--absolute-x1", type=int, help="Absolute start screen X coordinate")
    drag.add_argument("--relative-y1", type=int, help="Start Y coordinate relative to window")
    drag.add_argument("--absolute-y1", type=int, help="Absolute start screen Y coordinate")
    drag.add_argument("--relative-x2", type=int, help="End X coordinate relative to window")
    drag.add_argument("--absolute-x2", type=int, help="Absolute end screen X coordinate")
    drag.add_argument("--relative-y2", type=int, help="End Y coordinate relative to window")
    drag.add_argument("--absolute-y2", type=int, help="Absolute end screen Y coordinate")
    drag.add_argument("--duration-ms", type=int, default=500)
    drag.add_argument("--dry-run", action="store_true")

    type_cmd = sp.add_parser("type", help="Type text.")
    type_cmd.add_argument("--text", required=True)
    type_cmd.add_argument("--dry-run", action="store_true")

    press_key = sp.add_parser("press-key", help="Press a single key.")
    press_key.add_argument("--key", required=True)
    press_key.add_argument("--dry-run", action="store_true")

    hotkey = sp.add_parser("hotkey", help="Press a key chord in order.")
    hotkey.add_argument("--keys", nargs="+", required=True)
    hotkey.add_argument("--dry-run", action="store_true")

    clear_text = sp.add_parser("clear-text", help="Clear the currently focused text field.")
    clear_text.add_argument("--dry-run", action="store_true")

    scroll = sp.add_parser("scroll", help="Send mouse wheel scroll events.")
    scroll.add_argument("--direction", required=True, choices=["up", "down", "left", "right"], help="Scroll direction.")
    scroll.add_argument("--amount", type=int, default=1, help="Number of notches to scroll (default: 1).")
    coord_group = scroll.add_mutually_exclusive_group(required=False)
    coord_group.add_argument("--relative-x", type=int, help="X coordinate relative to window (requires --relative-y and --window-id)")
    coord_group.add_argument("--absolute-x", type=int, help="Absolute screen X coordinate (requires --absolute-y)")
    coord_group.add_argument("--element-id", help="UIA element ID (automation_id or runtime_id), scrolls at element center")
    scroll.add_argument("--relative-y", type=int, help="Y coordinate relative to window (requires --relative-x and --window-id)")
    scroll.add_argument("--absolute-y", type=int, help="Absolute screen Y coordinate (requires --absolute-x)")
    scroll.add_argument("--dry-run", action="store_true")


def _build_control_parser(subparsers: argparse._SubParsersAction) -> None:
    """Build the control subcommand parser (Win32 control operations)."""
    p = subparsers.add_parser("control", help="Directly control a specific control by hwnd.")
    p.add_argument("--hwnd", type=int, required=True, help="Control handle (hwnd).")
    p.add_argument("--dry-run", action="store_true", help="Preview mode, does not execute actual operation.")
    sp = p.add_subparsers(dest="control_command", required=True)

    set_text = sp.add_parser("set-text", help="Set text content of an edit control.")
    set_text.add_argument("text", nargs="?", default=None, help="Text to set.")
    set_text.add_argument("--text", dest="text_opt", default=None, help="Text to set (for compatibility, prefer positional argument).")
    sp.add_parser("set-focus", help="Set focus to the control.")
    sp.add_parser("get-text", help="Get text content of an edit control.")
    sp.add_parser("click", help="Click a button control.")
    sp.add_parser("double-click", help="Double click the control.")
    sp.add_parser("right-click", help="Right click the control.")
    sp.add_parser("check", help="Check a checkbox control.")
    sp.add_parser("uncheck", help="Uncheck a checkbox control.")
    sp.add_parser("check-by-click", help="Check a checkbox by click (triggers event handlers).")
    sp.add_parser("uncheck-by-click", help="Uncheck a checkbox by click (triggers event handlers).")
    sp.add_parser("is-checked", help="Get check state of a checkbox/button control.")

    type_keys = sp.add_parser("type-keys", help="Type keys to the control.")
    type_keys.add_argument(
        "keys",
        help=(
            "Keys to type (pywinauto format). "
            "Special keys: {ENTER}, {TAB}, {ESC}, {SPACE}, {BACK}, {DELETE}, {UP}, {DOWN}, {LEFT}, {RIGHT}, "
            "{HOME}, {END}, {PGUP}, {PGDN}, {F1}-{F12}. "
            "Modifiers: {CTRL}, {SHIFT}, {ALT}, {LCTRL}, {RCTRL}, etc. "
            "Combine: {CTRL}c{CTRL} for Ctrl+C, {CTRL}{SHIFT}s{SHIFT}{CTRL} for Ctrl+Shift+S. "
            "Repeat: {ENTER 3} for 3 Enter presses."
        ),
    )

    send_chars = sp.add_parser("send-chars", help="Send characters to inactive window.")
    send_chars.add_argument("chars", help="Characters to send.")

    send_keystrokes = sp.add_parser("send-keystrokes", help="Send keystrokes to inactive window.")
    send_keystrokes.add_argument(
        "keystrokes",
        help=(
            "Keystrokes to send (pywinauto format). "
            "Special keys: {ENTER}, {TAB}, {ESC}, {SPACE}, {BACK}, {DELETE}, {UP}, {DOWN}, {LEFT}, {RIGHT}, "
            "{HOME}, {END}, {PGUP}, {PGDN}, {F1}-{F12}. "
            "Modifiers: {CTRL}, {SHIFT}, {ALT}, {LCTRL}, {RCTRL}, etc. "
            "Combine: {CTRL}c{CTRL} for Ctrl+C, {CTRL}{SHIFT}s{SHIFT}{CTRL} for Ctrl+Shift+S. "
            "Repeat: {ENTER 3} for 3 Enter presses."
        ),
    )

    combo_select = sp.add_parser("combo-select", help="Select an item in a combobox by index or text.")
    combo_select.add_argument("item", help="Item index (0-based) or text to select.")
    combo_select.add_argument("--index", action="store_true", help="Treat item as a 0-based index instead of text.")
    sp.add_parser("combo-items", help="Get all items in a combobox.")
    sp.add_parser("combo-selected-index", help="Get selected index in a combobox.")
    sp.add_parser("combo-selected-text", help="Get selected text in a combobox.")

    listbox_select = sp.add_parser("listbox-select", help="Select an item in a listbox by index or text.")
    listbox_select.add_argument("item", help="Item index (0-based) or text to select.")
    sp.add_parser("listbox-items", help="Get all items in a listbox.")
    sp.add_parser("listbox-selected-indices", help="Get selected indices in a listbox.")


def _build_uia_control_parser(subparsers: argparse._SubParsersAction) -> None:
    """Build the uia-control subcommand parser (UIA element operations)."""
    p = subparsers.add_parser("uia-control", help="Control UIA elements by automation_id or runtime_id.")
    p.add_argument("--window-id", type=int, required=True, help="Parent window ID.")
    p.add_argument("--element-id", required=True, help="UIA element automation_id or runtime_id.")
    p.add_argument("--dry-run", action="store_true", help="Preview mode, does not execute actual operation.")
    sp = p.add_subparsers(dest="uia_control_command", required=True)

    sp.add_parser("click", help="Click the element.")
    sp.add_parser("double-click", help="Double click the element.")
    sp.add_parser("right-click", help="Right click the element.")
    sp.add_parser("invoke", help="Invoke the element (for buttons, menu items).")
    toggle = sp.add_parser("toggle", help="Toggle the element (for checkboxes).")
    toggle.add_argument("--target-state", choices=["on", "off"], default=None, help="Target toggle state (idempotent: only toggles if current state differs)")
    sp.add_parser("get-toggle-state", help="Get toggle state (0=off, 1=on, 2=indeterminate).")
    sp.add_parser("get-text", help="Get element text.")

    set_text = sp.add_parser("set-text", help="Set text in edit control.")
    set_text.add_argument("text", nargs="?", default=None, help="Text to set.")
    set_text.add_argument("--text", dest="text_opt", default=None, help="Text to set (for compatibility, prefer positional argument).")
    set_text.add_argument("--verify-change", action="store_true", help="Only set text if it differs from current value (idempotent)")
    sp.add_parser("set-focus", help="Set focus to the element.")

    type_keys = sp.add_parser("type-keys", help="Type keys to the element.")
    type_keys.add_argument(
        "keys",
        help=(
            "Keys to type (pywinauto format). "
            "Special keys: {ENTER}, {TAB}, {ESC}, {SPACE}, {BACK}, {DELETE}, {UP}, {DOWN}, {LEFT}, {RIGHT}, "
            "{HOME}, {END}, {PGUP}, {PGDN}, {F1}-{F12}. "
            "Modifiers: {CTRL}, {SHIFT}, {ALT}, {LCTRL}, {RCTRL}, etc. "
            "Combine: {CTRL}c{CTRL} for Ctrl+C, {CTRL}{SHIFT}s{SHIFT}{CTRL} for Ctrl+Shift+S. "
            "Repeat: {ENTER 3} for 3 Enter presses."
        ),
    )

    scroll = sp.add_parser("scroll", help="Scroll the element.")
    scroll.add_argument("direction", choices=["up", "down", "left", "right"], help="Scroll direction.")
    scroll.add_argument("--amount", default="page", choices=["line", "page"], help="Scroll amount.")
    scroll.add_argument("--count", type=int, default=1, help="Scroll count.")

    sp.add_parser("get-value", help="Get element value.")

    set_value = sp.add_parser("set-value", help="Set element value.")
    set_value.add_argument("value", help="Value to set.")

    sp.add_parser("select", help="Select the element (for list items, tree items).")
    sp.add_parser("is-selected", help="Check if element is selected.")
    sp.add_parser("expand", help="Expand the element (for combo boxes, trees, menu items).")
    sp.add_parser("collapse", help="Collapse the element (for combo boxes, trees, menu items).")
    sp.add_parser("is-expanded", help="Check if element is expanded.")

    combo_select = sp.add_parser("combo-select", help="Select item in combo box.")
    combo_select.add_argument("item", help="Item index or text.")
    combo_select.add_argument("--index", action="store_true", help="Treat item as a 0-based index instead of text.")
    sp.add_parser("combo-items", help="Get combo box items.")
    sp.add_parser("combo-selected-text", help="Get selected text in combo box.")
    sp.add_parser("combo-selected-index", help="Get selected index in combo box.")
    sp.add_parser("list-items", help="Get list items.")

    list_select = sp.add_parser("list-select", help="Select item in list.")
    list_select.add_argument("item", help="Item index or text.")
    sp.add_parser("list-selected-items", help="Get selected items in list.")

    tab_select = sp.add_parser("tab-select", help="Select tab by index or text.")
    tab_select.add_argument("item", help="Tab index or text.")
    sp.add_parser("tab-selected", help="Get selected tab index.")
    sp.add_parser("tab-count", help="Get tab count.")
    sp.add_parser("slider-value", help="Get slider value.")

    slider_set = sp.add_parser("slider-set", help="Set slider value.")
    slider_set.add_argument("value", type=float, help="Value to set.")
    sp.add_parser("slider-min", help="Get slider minimum value.")
    sp.add_parser("slider-max", help="Get slider maximum value.")

    sp.add_parser("window-close", help="Close the window (WindowPattern).")
    sp.add_parser("window-minimize", help="Minimize the window (WindowPattern).")
    sp.add_parser("window-maximize", help="Maximize the window (WindowPattern).")
    sp.add_parser("window-restore", help="Restore the window to normal size (WindowPattern).")
    sp.add_parser("window-state", help="Get window visual state (WindowPattern).")

    transform_move = sp.add_parser("transform-move", help="Move element to screen coordinates (TransformPattern).")
    transform_move.add_argument("--absolute-x", type=int, required=True, help="Target absolute screen X coordinate.")
    transform_move.add_argument("--absolute-y", type=int, required=True, help="Target absolute screen Y coordinate.")
    transform_resize = sp.add_parser("transform-resize", help="Resize element (TransformPattern).")
    transform_resize.add_argument("width", type=int, help="New width in pixels.")
    transform_resize.add_argument("height", type=int, help="New height in pixels.")
    transform_rotate = sp.add_parser("transform-rotate", help="Rotate element (TransformPattern).")
    transform_rotate.add_argument("degrees", type=float, help="Rotation angle in degrees.")


def _build_screenshot_parser(subparsers: argparse._SubParsersAction) -> None:
    """Build the screenshot subcommand parser."""
    p = subparsers.add_parser("screenshot", help="Take a screenshot of a window.")
    p.add_argument("--window-id", type=int, required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--x", type=int, help="Left offset relative to window (optional)")
    p.add_argument("--y", type=int, help="Top offset relative to window (optional)")
    p.add_argument("--width", type=int, help="Rectangle width (optional)")
    p.add_argument("--height", type=int, help="Rectangle height (optional)")
    p.add_argument("--dry-run", action="store_true")


def _build_wait_parser(subparsers: argparse._SubParsersAction) -> None:
    """Build the wait subcommand parser."""
    p = subparsers.add_parser("wait", help="Wait for conditions (window, text, element, image).")
    p.add_argument("--window-id", type=int, help="Window handle (required for text, uia, ocr, image subcommands).")
    sp = p.add_subparsers(dest="wait_command", required=True)

    sleep_cmd = sp.add_parser("sleep", help="Wait for a specified duration.")
    sleep_cmd.add_argument("duration_ms", type=int, help="Duration to wait in milliseconds.")

    window_cmd = sp.add_parser("window", help="Wait for a window to appear or disappear.")
    window_cmd.add_argument("title", help="Window title (supports partial match).")
    window_cmd.add_argument("--exact", action="store_true", help="Match title exactly.")
    window_cmd.add_argument("--class", dest="class_name", help="Filter by window class name.")
    window_cmd.add_argument("--timeout", type=float, default=30.0, help="Timeout in seconds (default: 30).")
    window_cmd.add_argument("--interval", type=int, default=500, help="Poll interval in milliseconds (default: 500).")
    window_cmd.add_argument("--disappear", action="store_true", help="Wait for window to disappear instead of appear.")

    text_cmd = sp.add_parser("text", help="Wait for text to appear or disappear in a window.")
    text_cmd.add_argument("text", help="Text to wait for.")
    text_cmd.add_argument("--exact", action="store_true", help="Match text exactly.")
    text_cmd.add_argument("--timeout", type=float, default=30.0, help="Timeout in seconds (default: 30).")
    text_cmd.add_argument("--interval", type=int, default=500, help="Poll interval in milliseconds (default: 500).")
    text_cmd.add_argument("--disappear", action="store_true", help="Wait for text to disappear instead of appear.")

    uia_cmd = sp.add_parser("uia", help="Wait for UIA element to appear or disappear in a window.")
    uia_cmd.add_argument("--text", help="Filter by element text/name.")
    uia_cmd.add_argument("--control-type", help="Filter by control type.")
    uia_cmd.add_argument("--class", dest="class_name", help="Filter by window class name.")
    uia_cmd.add_argument("--automation-id", help="Filter by automation ID.")
    uia_cmd.add_argument("--exact", action="store_true", help="Match text exactly.")
    uia_cmd.add_argument("--timeout", type=float, default=30.0, help="Timeout in seconds (default: 30).")
    uia_cmd.add_argument("--interval", type=int, default=500, help="Poll interval in milliseconds (default: 500).")
    uia_cmd.add_argument("--disappear", action="store_true", help="Wait for element to disappear instead of appear.")

    ocr_cmd = sp.add_parser("ocr", help="Wait for OCR text to appear or disappear in a window.")
    ocr_cmd.add_argument("text", help="Text to wait for.")
    ocr_cmd.add_argument("--exact", action="store_true", help="Match text exactly.")
    ocr_cmd.add_argument("--confidence-threshold", type=float, default=0.0, help="OCR confidence threshold.")
    ocr_cmd.add_argument("--timeout", type=float, default=30.0, help="Timeout in seconds (default: 30).")
    ocr_cmd.add_argument("--interval", type=int, default=500, help="Poll interval in milliseconds (default: 500).")
    ocr_cmd.add_argument("--disappear", action="store_true", help="Wait for text to disappear instead of appear.")

    image_cmd = sp.add_parser("image", help="Wait for image to appear or disappear in a window.")
    image_cmd.add_argument("--image-path", required=True, help="Template image file path.")
    image_cmd.add_argument("--threshold", type=float, default=0.9, help="Match confidence threshold (0-1).")
    image_cmd.add_argument("--timeout", type=float, default=30.0, help="Timeout in seconds (default: 30).")
    image_cmd.add_argument("--interval", type=int, default=500, help="Poll interval in milliseconds (default: 500).")
    image_cmd.add_argument("--disappear", action="store_true", help="Wait for image to disappear instead of appear.")


def _build_clipboard_parser(subparsers: argparse._SubParsersAction) -> None:
    """Build the clipboard subcommand parser."""
    p = subparsers.add_parser("clipboard", help="Clipboard operations.")
    sp = p.add_subparsers(dest="clipboard_command", required=True)

    copy_files = sp.add_parser("copy-files", help="Copy files to clipboard.")
    copy_files.add_argument("files", nargs="+", help="File paths to copy to clipboard.")

    copy_text = sp.add_parser("copy-text", help="Copy text to clipboard.")
    copy_text.add_argument("text", help="Text to copy to clipboard.")

    sp.add_parser("get-text", help="Get text from clipboard.")


def _handle_window(args: argparse.Namespace) -> int:
    """Handle window subcommands."""
    from output_utils import format_window_tree
    from win32_utils import Win32API
    from windows_driver import WindowsDriver

    if args.window_command == "list":
        try:
            windows = WindowsDriver.list_windows()
            content = format_window_tree(windows)
            nonce = generate_nonce()
            print(wrap_with_boundary(content, nonce))
            return 0
        except Exception as e:  # pylint: disable=broad-exception-caught
            emit_action(False, "list", {"error": str(e)})
            return 1

    if args.window_id is None:
        emit_action(False, args.window_command, {"error": "--window-id is required for this subcommand"})
        return 1

    try:
        unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
        window_title = Win32API.get_window_text(args.window_id)
        window_info = {"window_id": str(args.window_id), "window_title": window_title}

        action_map = {
            "focus": lambda: WindowsDriver.focus_window(args.window_id),
            "minimize": lambda: WindowsDriver.minimize_window(args.window_id),
            "maximize": lambda: WindowsDriver.maximize_window(args.window_id),
            "restore": lambda: WindowsDriver.restore_window(args.window_id),
            "close": lambda: WindowsDriver.close_window(args.window_id),
            "move": lambda: WindowsDriver.move_window(args.window_id, args.x, args.y),
            "resize": lambda: WindowsDriver.resize_window(args.window_id, args.width, args.height),
        }
        handler = action_map.get(args.window_command)
        if handler is None:
            emit_action(False, args.window_command, {"window_id": str(args.window_id), "error": f"unknown window subcommand: {args.window_command}"})
            return 1
        success = handler()
        emit_action(success, args.window_command, window_info)
        return 0 if success else 1
    except Exception as e:  # pylint: disable=broad-exception-caught
        emit_action(False, args.window_command, {"window_id": str(args.window_id) if args.window_id else None, "error": str(e)})
        return 1


def _handle_snapshot(args: argparse.Namespace) -> int:
    """Handle snapshot subcommands."""
    from ocr_driver import OCRDriver
    from uia_driver import UIADriver
    from win32_driver import Win32Driver
    from win32_utils import Win32API

    try:
        unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")

        nonce = generate_nonce()
        max_depth = getattr(args, "max_depth", None)
        match args.snapshot_command:
            case "hwnd":
                content = Win32Driver.snapshot_hwnd_tree(args.window_id, max_depth=max_depth)
                print(wrap_with_boundary(content, nonce))
            case "uia":
                skip_actions = getattr(args, "skip_actions", False)
                skip_state = getattr(args, "skip_state", False)
                content = UIADriver.snapshot_uia_tree(args.window_id, skip_actions=skip_actions, skip_state=skip_state, max_depth=max_depth)
                print(wrap_with_boundary(content, nonce))
            case "ocr":
                content = OCRDriver.snapshot_ocr(args.window_id)
                print(wrap_with_boundary(content, nonce))
            case _:
                emit_action(False, f"snapshot_{args.snapshot_command}", {"window_id": str(args.window_id), "error": f"unknown snapshot subcommand: {args.snapshot_command}"})
                return 1
        return 0
    except Exception as e:  # pylint: disable=broad-exception-caught
        emit_action(False, f"snapshot_{args.snapshot_command}", {"window_id": str(args.window_id), "error": str(e)})
        return 1


def _handle_find(args: argparse.Namespace) -> int:
    """Handle find subcommands."""
    from find_driver import FindDriver
    from ocr_driver import OCRDriver
    from output_utils import validate_threshold
    from win32_utils import Win32API

    try:
        unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")

        nonce = generate_nonce()
        match args.find_command:
            case "text":
                content = FindDriver.find_text(args.window_id, args.text, exact=args.exact)
                print(wrap_with_boundary(content, nonce))
            case "uia":
                skip_actions = getattr(args, "skip_actions", False)
                skip_state = getattr(args, "skip_state", False)
                content = FindDriver.find_uia(
                    args.window_id,
                    text=args.text,
                    control_type=args.control_type,
                    class_name=args.class_name,
                    automation_id=args.automation_id,
                    action=args.action,
                    exact=args.exact,
                    skip_actions=skip_actions,
                    skip_state=skip_state,
                )
                print(wrap_with_boundary(content, nonce))
            case "ocr":
                result = OCRDriver.find_ocr_text(args.window_id, args.text, exact=args.exact, confidence_threshold=args.confidence_threshold)
                content = "\n".join(ElementFormatter.format_element(m) for m in result)
                print(wrap_with_boundary(content, nonce))
            case "image":
                validate_threshold(args.threshold, "--threshold")
                if args.overlap_threshold is not None:
                    validate_threshold(args.overlap_threshold, "--overlap-threshold")
                result = FindDriver.find_image(
                    window_id=args.window_id,
                    image_path=args.image_path,
                    threshold=args.threshold,
                    overlap_threshold=args.overlap_threshold
                )
                content = "\n".join(ElementFormatter.format_element(m) for m in result) if result else ""
                print(wrap_with_boundary(content, nonce))
            case _:
                emit_action(False, f"find_{args.find_command}", {"window_id": str(args.window_id), "error": f"unknown find subcommand: {args.find_command}"})
                return 1
        return 0
    except Exception as e:  # pylint: disable=broad-exception-caught
        error_data: dict = {"window_id": str(args.window_id), "error": str(e)}
        error_data.update(build_error_context(args.window_id))
        emit_action(False, f"find_{args.find_command}", error_data)
        return 1


def _handle_action(args: argparse.Namespace) -> int:  # pylint: disable=too-many-statements
    """Handle action subcommands."""
    import win32api

    from find_driver import FindDriver
    from output_utils import (
        build_center_payload,
        build_point_context,
        resolve_window_context,
        validate_coordinate_pair,
        validate_relative_coords,
        validate_threshold,
    )
    from uia_driver import UIADriver
    from win32_utils import Win32API
    from windows_driver import WindowsDriver

    try:
        match args.action_command:
            case "click":
                is_absolute_mode = args.absolute_x is not None
                is_relative_mode = args.relative_x is not None
                is_element_mode = args.element_id is not None

                if is_absolute_mode:
                    validate_coordinate_pair(args.absolute_x, args.absolute_y, "--absolute-x", "--absolute-y")
                    absolute_x = args.absolute_x
                    absolute_y = args.absolute_y
                    hwnd_result = Win32API.get_hwnd_from_point(absolute_x, absolute_y)
                    window_id = hwnd_result.value if hwnd_result.is_ok else None
                    window_title = Win32API.get_window_text(window_id) if window_id else None
                    bounds_result = Win32API.get_window_bounds(window_id) if window_id else Err("no window")
                    window_bounds = bounds_result.value if bounds_result.is_ok else None
                    relative_x = absolute_x - window_bounds.x if window_bounds else None
                    relative_y = absolute_y - window_bounds.y if window_bounds else None
                    point_ctx = build_point_context(absolute_x, absolute_y)
                    data = {
                        "absolute": {"x": absolute_x, "y": absolute_y},
                        "window_id": str(window_id) if window_id else None,
                        "window_title": window_title,
                        **point_ctx,
                    }
                    if relative_x is not None and relative_y is not None:
                        data["relative"] = {"x": relative_x, "y": relative_y}
                elif is_relative_mode:
                    validate_coordinate_pair(args.relative_x, args.relative_y, "--relative-x", "--relative-y")
                    if args.window_id is None:
                        raise ValueError("--window-id is required for relative coordinates")
                    unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                    window_title, bounds = resolve_window_context(args.window_id)
                    validate_relative_coords(args.relative_x, args.relative_y, bounds)
                    relative_x = args.relative_x
                    relative_y = args.relative_y
                    absolute_x = bounds.x + args.relative_x
                    absolute_y = bounds.y + args.relative_y
                    point_ctx = build_point_context(absolute_x, absolute_y)
                    data = {
                        "window_id": str(args.window_id),
                        "window_title": window_title,
                        "relative": {"x": relative_x, "y": relative_y},
                        **point_ctx,
                    }
                elif is_element_mode:
                    if args.window_id is None:
                        raise ValueError("--window-id is required for --element-id")
                    unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                    window_title, bounds = resolve_window_context(args.window_id)
                    # Accessing protected member _get_uia_wrapper is intentional for UIA element resolution
                    wrapper = UIADriver._get_uia_wrapper(args.window_id, args.element_id)  # pylint: disable=protected-access
                    element_info = wrapper.element_info
                    rect = getattr(element_info, "rectangle", None)
                    if rect is None or rect.right <= rect.left or rect.bottom <= rect.top:
                        raise ValueError(f"Element has no valid bounding rectangle: {args.element_id}")
                    absolute_x = (rect.left + rect.right) // 2
                    absolute_y = (rect.top + rect.bottom) // 2
                    relative_x = absolute_x - bounds.x
                    relative_y = absolute_y - bounds.y
                    point_ctx = build_point_context(absolute_x, absolute_y)
                    data = {
                        "window_id": str(args.window_id),
                        "window_title": window_title,
                        "element_id": args.element_id,
                        "relative": {"x": relative_x, "y": relative_y},
                        "absolute": {"x": absolute_x, "y": absolute_y},
                        **point_ctx,
                    }
                else:
                    raise ValueError("either --absolute-x/--absolute-y, --relative-x/--relative-y with --window-id, or --element-id with --window-id is required")
                if not args.dry_run:
                    if args.window_id:
                        WindowsDriver.focus_window(args.window_id)
                    Win32API.send_click(absolute_x, absolute_y)
                emit_action_result("click", args.dry_run, data)
            case "click-image":
                if args.window_id is None:
                    raise ValueError("--window-id is required for click-image")
                unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                validate_threshold(args.threshold, "--threshold")
                matches = FindDriver.find_image(window_id=args.window_id, image_path=args.image_path, threshold=args.threshold)
                if not matches:
                    raise ValueError(f"image target not found: {args.image_path}")
                target = matches[0]
                payload = build_center_payload(target)
                window_title = Win32API.get_window_text(int(target.window_id))
                bounds_result = Win32API.get_window_bounds(int(target.window_id))
                window_bounds = bounds_result.value if bounds_result.is_ok else None
                if window_bounds:
                    absolute_x = window_bounds.x + payload["relative"]["x"]
                    absolute_y = window_bounds.y + payload["relative"]["y"]
                else:
                    absolute_x = payload["relative"]["x"]
                    absolute_y = payload["relative"]["y"]
                point_ctx = build_point_context(absolute_x, absolute_y)
                payload["window_title"] = window_title
                payload.update(point_ctx)
                if not args.dry_run:
                    WindowsDriver.focus_window(int(target.window_id))
                    Win32API.send_click(absolute_x, absolute_y)
                emit_action_result("click_image", args.dry_run, payload)
            case "drag":
                is_absolute_mode = args.absolute_x1 is not None
                is_relative_mode = args.relative_x1 is not None

                if is_absolute_mode:
                    validate_coordinate_pair(args.absolute_x1, args.absolute_y1, "--absolute-x1", "--absolute-y1")
                    validate_coordinate_pair(args.absolute_x2, args.absolute_y2, "--absolute-x2", "--absolute-y2")
                    if args.window_id is not None:
                        unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                    absolute_x1 = args.absolute_x1
                    absolute_y1 = args.absolute_y1
                    absolute_x2 = args.absolute_x2
                    absolute_y2 = args.absolute_y2
                    hwnd_result = Win32API.get_hwnd_from_point(absolute_x1, absolute_y1)
                    window_id = args.window_id if args.window_id is not None else (hwnd_result.value if hwnd_result.is_ok else None)
                    window_title = Win32API.get_window_text(window_id) if window_id else None
                    bounds_result = Win32API.get_window_bounds(window_id) if window_id else Err("no window")
                    window_bounds = bounds_result.value if bounds_result.is_ok else None
                    from_ctx = build_point_context(absolute_x1, absolute_y1)
                    to_ctx = build_point_context(absolute_x2, absolute_y2)
                    data = {
                        "from": {"absolute": {"x": absolute_x1, "y": absolute_y1}, **from_ctx},
                        "to": {"absolute": {"x": absolute_x2, "y": absolute_y2}, **to_ctx},
                        "duration_ms": args.duration_ms,
                        "window_id": str(window_id) if window_id else None,
                        "window_title": window_title,
                    }
                elif is_relative_mode:
                    validate_coordinate_pair(args.relative_x1, args.relative_y1, "--relative-x1", "--relative-y1")
                    validate_coordinate_pair(args.relative_x2, args.relative_y2, "--relative-x2", "--relative-y2")
                    if args.window_id is None:
                        raise ValueError("--window-id is required for relative coordinates")
                    unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                    window_title, bounds = resolve_window_context(args.window_id)
                    validate_relative_coords(args.relative_x1, args.relative_y1, bounds)
                    validate_relative_coords(args.relative_x2, args.relative_y2, bounds)
                    absolute_x1 = bounds.x + args.relative_x1
                    absolute_y1 = bounds.y + args.relative_y1
                    absolute_x2 = bounds.x + args.relative_x2
                    absolute_y2 = bounds.y + args.relative_y2
                    from_ctx = build_point_context(absolute_x1, absolute_y1)
                    to_ctx = build_point_context(absolute_x2, absolute_y2)
                    data = {
                        "window_id": str(args.window_id), "window_title": window_title,
                        "from": {"relative": {"x": args.relative_x1, "y": args.relative_y1}, **from_ctx},
                        "to": {"relative": {"x": args.relative_x2, "y": args.relative_y2}, **to_ctx},
                        "duration_ms": args.duration_ms,
                    }
                else:
                    raise ValueError("either --absolute-x1/y1/x2/y2 or --relative-x1/y1/x2/y2 with --window-id is required")
                if not args.dry_run:
                    if window_id:
                        WindowsDriver.focus_window(window_id)
                    Win32API.send_drag(absolute_x1, absolute_y1, absolute_x2, absolute_y2, duration_ms=args.duration_ms)
                emit_action_result("drag", args.dry_run, data)
            case "type":
                if args.window_id is None:
                    raise ValueError("--window-id is required for type")
                unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                window_title = Win32API.get_window_text(args.window_id)
                data = {"window_id": str(args.window_id), "window_title": window_title, "text": args.text, "length": len(args.text)}
                if not args.dry_run:
                    WindowsDriver.focus_window(args.window_id)
                    Win32API.move_mouse_to_window_center(args.window_id)
                    Win32API.send_type_text(args.text)
                emit_action_result("type_text", args.dry_run, data)
            case "press-key":
                if args.window_id is None:
                    raise ValueError("--window-id is required for press-key")
                unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                window_title = Win32API.get_window_text(args.window_id)
                data = {"window_id": str(args.window_id), "window_title": window_title, "key": args.key}
                if not args.dry_run:
                    WindowsDriver.focus_window(args.window_id)
                    Win32API.move_mouse_to_window_center(args.window_id)
                    Win32API.send_press_key(args.key)
                emit_action_result("press_key", args.dry_run, data)
            case "hotkey":
                if args.window_id is None:
                    raise ValueError("--window-id is required for hotkey")
                unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                window_title = Win32API.get_window_text(args.window_id)
                data = {"window_id": str(args.window_id), "window_title": window_title, "keys": args.keys}
                if not args.dry_run:
                    WindowsDriver.focus_window(args.window_id)
                    Win32API.move_mouse_to_window_center(args.window_id)
                    Win32API.send_hotkey(args.keys)
                emit_action_result("hotkey", args.dry_run, data)
            case "clear-text":
                if args.window_id is None:
                    raise ValueError("--window-id is required for clear-text")
                unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                window_title = Win32API.get_window_text(args.window_id)
                data = {"window_id": str(args.window_id), "window_title": window_title}
                if not args.dry_run:
                    WindowsDriver.focus_window(args.window_id)
                    Win32API.move_mouse_to_window_center(args.window_id)
                    Win32API.send_hotkey(["{CTRL}", "{A}"])
                    Win32API.send_press_key("{DELETE}")
                emit_action_result("clear_text", args.dry_run, data)
            case "scroll":
                is_absolute_mode = args.absolute_x is not None
                is_relative_mode = args.relative_x is not None
                is_element_mode = args.element_id is not None
                is_default_mode = not (is_absolute_mode or is_relative_mode or is_element_mode)

                if is_absolute_mode:
                    validate_coordinate_pair(args.absolute_x, args.absolute_y, "--absolute-x", "--absolute-y")
                    absolute_x = args.absolute_x
                    absolute_y = args.absolute_y
                    hwnd_result = Win32API.get_hwnd_from_point(absolute_x, absolute_y)
                    window_id = hwnd_result.value if hwnd_result.is_ok else None
                    window_title = Win32API.get_window_text(window_id) if window_id else None
                    bounds_result = Win32API.get_window_bounds(window_id) if window_id else Err("no window")
                    window_bounds = bounds_result.value if bounds_result.is_ok else None
                    relative_x = absolute_x - window_bounds.x if window_bounds else None
                    relative_y = absolute_y - window_bounds.y if window_bounds else None
                    point_ctx = build_point_context(absolute_x, absolute_y)
                    data = {
                        "direction": args.direction,
                        "amount": args.amount,
                        "absolute": {"x": absolute_x, "y": absolute_y},
                        "window_id": str(window_id) if window_id else None,
                        "window_title": window_title,
                        **point_ctx,
                    }
                    if relative_x is not None and relative_y is not None:
                        data["relative"] = {"x": relative_x, "y": relative_y}
                elif is_relative_mode:
                    validate_coordinate_pair(args.relative_x, args.relative_y, "--relative-x", "--relative-y")
                    if args.window_id is None:
                        raise ValueError("--window-id is required for relative coordinates")
                    unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                    window_title, bounds = resolve_window_context(args.window_id)
                    validate_relative_coords(args.relative_x, args.relative_y, bounds)
                    relative_x = args.relative_x
                    relative_y = args.relative_y
                    absolute_x = bounds.x + args.relative_x
                    absolute_y = bounds.y + args.relative_y
                    point_ctx = build_point_context(absolute_x, absolute_y)
                    data = {
                        "direction": args.direction,
                        "amount": args.amount,
                        "window_id": str(args.window_id),
                        "window_title": window_title,
                        "relative": {"x": relative_x, "y": relative_y},
                        **point_ctx,
                    }
                elif is_element_mode:
                    if args.window_id is None:
                        raise ValueError("--window-id is required for --element-id")
                    unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                    window_title, bounds = resolve_window_context(args.window_id)
                    wrapper = UIADriver._get_uia_wrapper(args.window_id, args.element_id)  # pylint: disable=protected-access
                    element_info = wrapper.element_info
                    rect = getattr(element_info, "rectangle", None)
                    if rect is None or rect.right <= rect.left or rect.bottom <= rect.top:
                        raise ValueError(f"Element has no valid bounding rectangle: {args.element_id}")
                    absolute_x = (rect.left + rect.right) // 2
                    absolute_y = (rect.top + rect.bottom) // 2
                    relative_x = absolute_x - bounds.x
                    relative_y = absolute_y - bounds.y
                    point_ctx = build_point_context(absolute_x, absolute_y)
                    data = {
                        "direction": args.direction,
                        "amount": args.amount,
                        "window_id": str(args.window_id),
                        "window_title": window_title,
                        "element_id": args.element_id,
                        "relative": {"x": relative_x, "y": relative_y},
                        "absolute": {"x": absolute_x, "y": absolute_y},
                        **point_ctx,
                    }
                elif is_default_mode:
                    if args.window_id is None:
                        raise ValueError("--window-id is required when no coordinates are specified")
                    unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                    window_title, bounds = resolve_window_context(args.window_id)
                    absolute_x = bounds.x + bounds.width // 2
                    absolute_y = bounds.y + bounds.height // 2
                    relative_x = bounds.width // 2
                    relative_y = bounds.height // 2
                    data = {
                        "direction": args.direction,
                        "amount": args.amount,
                        "window_id": str(args.window_id),
                        "window_title": window_title,
                        "relative": {"x": relative_x, "y": relative_y},
                        "absolute": {"x": absolute_x, "y": absolute_y},
                    }
                else:
                    raise ValueError("invalid scroll parameters")
                if not args.dry_run:
                    if args.window_id:
                        WindowsDriver.focus_window(args.window_id)
                    win32api.SetCursorPos((absolute_x, absolute_y))
                    Win32API.send_scroll(args.direction, args.amount)
                emit_action_result("scroll", args.dry_run, data)
            case _:
                emit_action(False, args.action_command, {"window_id": str(args.window_id) if args.window_id else None, "error": f"unknown action subcommand: {args.action_command}"})
                return 1
        return 0
    except Exception as e:  # pylint: disable=broad-exception-caught
        error_data: dict = {"window_id": str(args.window_id) if args.window_id else None, "error": str(e)}
        error_data.update(build_error_context(args.window_id))
        emit_action(False, args.action_command, error_data)
        return 1


def _handle_control(args: argparse.Namespace) -> int:
    """Handle control subcommands (Win32 control operations)."""
    from output_utils import build_control_info
    from win32_driver import Win32Driver
    from win32_utils import Win32API

    hwnd = args.hwnd

    try:
        bounds_result = Win32API.get_window_bounds(hwnd)
        if bounds_result.is_err:
            raise ValueError(f"control not found: hwnd {hwnd}")

        control_info = build_control_info(hwnd)

        if args.dry_run:
            emit_action(True, args.control_command, {**control_info, "dry_run": True})
            return 0

        match args.control_command:
            case "set-text":
                text = args.text if args.text is not None else args.text_opt
                Win32Driver.set_text(hwnd, text)
                emit_action(True, "set_text", {**control_info, "text": text})
            case "set-focus":
                Win32Driver.set_focus(hwnd)
                emit_action(True, "set_focus", control_info)
            case "get-text":
                text = Win32Driver.get_text(hwnd)
                emit_action(True, "get_text", {**control_info, "text": text})
            case "click":
                Win32Driver.click(hwnd)
                emit_action(True, "click", control_info)
            case "double-click":
                Win32Driver.double_click(hwnd)
                emit_action(True, "double_click", control_info)
            case "right-click":
                Win32Driver.right_click(hwnd)
                emit_action(True, "right_click", control_info)
            case "check":
                Win32Driver.check(hwnd)
                emit_action(True, "check", control_info)
            case "uncheck":
                Win32Driver.uncheck(hwnd)
                emit_action(True, "uncheck", control_info)
            case "check-by-click":
                Win32Driver.check_by_click(hwnd)
                emit_action(True, "check_by_click", control_info)
            case "uncheck-by-click":
                Win32Driver.uncheck_by_click(hwnd)
                emit_action(True, "uncheck_by_click", control_info)
            case "is-checked":
                checked = Win32Driver.is_checked(hwnd)
                emit_action(True, "is_checked", {**control_info, "checked": checked})
            case "type-keys":
                Win32Driver.type_keys(hwnd, args.keys)
                emit_action(True, "type_keys", {**control_info, "keys": args.keys})
            case "send-chars":
                Win32Driver.send_chars(hwnd, args.chars)
                emit_action(True, "send_chars", {**control_info, "chars": args.chars})
            case "send-keystrokes":
                Win32Driver.send_keystrokes(hwnd, args.keystrokes)
                emit_action(True, "send_keystrokes", {**control_info, "keystrokes": args.keystrokes})
            case "combo-select":
                item = int(args.item) if args.index else args.item
                Win32Driver.combo_select(hwnd, item)
                emit_action(True, "combo_select", {**control_info, "item": item})
            case "combo-items":
                items = Win32Driver.combo_items(hwnd)
                emit_action(True, "combo_items", {**control_info, "items": items})
            case "combo-selected-index":
                index = Win32Driver.combo_selected_index(hwnd)
                emit_action(True, "combo_selected_index", {**control_info, "index": index})
            case "combo-selected-text":
                text = Win32Driver.combo_selected_text(hwnd)
                emit_action(True, "combo_selected_text", {**control_info, "text": text})
            case "listbox-select":
                Win32Driver.listbox_select(hwnd, args.item)
                emit_action(True, "listbox_select", {**control_info, "item": args.item})
            case "listbox-items":
                items = Win32Driver.listbox_items(hwnd)
                emit_action(True, "listbox_items", {**control_info, "items": items})
            case "listbox-selected-indices":
                indices = Win32Driver.listbox_selected_indices(hwnd)
                emit_action(True, "listbox_selected_indices", {**control_info, "indices": indices})
            case _:
                emit_action(False, args.control_command, {"hwnd": str(hwnd), "error": f"unknown control subcommand: {args.control_command}"})
                return 1
    except Exception as e:  # pylint: disable=broad-exception-caught
        emit_action(False, args.control_command, {"hwnd": str(hwnd), "error": str(e)})
        return 1
    return 0


def _handle_uia_control(args: argparse.Namespace) -> int:
    """Handle uia-control subcommands (UIA element operations)."""
    from output_utils import build_uia_control_info
    from uia_driver import UIADriver
    from win32_utils import Win32API

    wid = args.window_id
    eid = args.element_id

    if not eid or not eid.strip():
        emit_action(False, "uia_control", {"window_id": str(wid), "error": "element_id must not be empty"})
        return 1

    def _emit(cmd: str, data: dict) -> None:
        emit_action(True, cmd, {**uia_info, **data})

    def _no_args(cmd: str, func) -> None:
        func(wid, eid)
        _emit(cmd, {})

    def _with_text(cmd: str, func) -> None:
        text = args.text if args.text is not None else args.text_opt
        _emit(cmd, {"text": text})
        func(wid, eid, text)

    def _with_keys(cmd: str, func) -> None:
        _emit(cmd, {"keys": args.keys})
        func(wid, eid, args.keys)

    def _with_item(cmd: str, func) -> None:
        item = int(args.item) if getattr(args, "index", False) else args.item
        _emit(cmd, {"item": item})
        func(wid, eid, item)

    def _handle_toggle_with_target_state() -> None:
        target_state = getattr(args, "target_state", None)
        if target_state is None:
            UIADriver.toggle(wid, eid)
            _emit("toggle", {})
            return
        current_state = UIADriver.get_toggle_state(wid, eid)
        desired = 1 if target_state == "on" else 0
        if current_state != desired:
            UIADriver.toggle(wid, eid)
            _emit("toggle", {"target_state": target_state, "previous_state": current_state, "toggled": True})
        else:
            _emit("toggle", {"target_state": target_state, "current_state": current_state, "toggled": False})

    def _handle_set_text_with_verify() -> None:
        text = args.text if args.text is not None else args.text_opt
        verify_change = getattr(args, "verify_change", False)
        if verify_change:
            current_text = UIADriver.get_text(wid, eid)
            if current_text == text:
                _emit("set_text", {"text": text, "changed": False, "reason": "text already matches"})
                return
            _emit("set_text", {"text": text, "changed": True, "previous_text": current_text})
        else:
            _emit("set_text", {"text": text})
        UIADriver.set_text(wid, eid, text)

    _uia_commands: dict[str, tuple[callable, str]] = {
        "click": (lambda: _no_args("click", UIADriver.click), "click"),
        "double-click": (lambda: _no_args("double_click", UIADriver.double_click), "double_click"),
        "right-click": (lambda: _no_args("right_click", UIADriver.right_click), "right_click"),
        "invoke": (lambda: _no_args("invoke", UIADriver.invoke), "invoke"),
        "toggle": (_handle_toggle_with_target_state, "toggle"),
        "get-toggle-state": (lambda: _emit("get_toggle_state", {"state": UIADriver.get_toggle_state(wid, eid)}), "get_toggle_state"),
        "get-text": (lambda: _emit("get_text", {"text": UIADriver.get_text(wid, eid)}), "get_text"),
        "set-text": (_handle_set_text_with_verify, "set_text"),
        "set-focus": (lambda: _no_args("set_focus", UIADriver.set_focus), "set_focus"),
        "type-keys": (lambda: _with_keys("type_keys", UIADriver.type_keys), "type_keys"),
        "select": (lambda: _no_args("select", UIADriver.select), "select"),
        "is-selected": (lambda: _emit("is_selected", {"selected": UIADriver.is_selected(wid, eid)}), "is_selected"),
        "expand": (lambda: _no_args("expand", UIADriver.expand), "expand"),
        "collapse": (lambda: _no_args("collapse", UIADriver.collapse), "collapse"),
        "is-expanded": (lambda: _emit("is_expanded", {"expanded": UIADriver.is_expanded(wid, eid)}), "is_expanded"),
        "combo-items": (lambda: _emit("combo_items", {"items": UIADriver.combo_items(wid, eid)}), "combo_items"),
        "combo-selected-text": (lambda: _emit("combo_selected_text", {"text": UIADriver.combo_selected_text(wid, eid)}), "combo_selected_text"),
        "combo-selected-index": (lambda: _emit("combo_selected_index", {"index": UIADriver.combo_selected_index(wid, eid)}), "combo_selected_index"),
        "list-items": (lambda: _emit("list_items", {"items": UIADriver.list_items(wid, eid)}), "list_items"),
        "list-selected-items": (lambda: _emit("list_selected_items", {"items": UIADriver.list_selected_items(wid, eid)}), "list_selected_items"),
        "tab-selected": (lambda: _emit("tab_selected", {"index": UIADriver.tab_selected(wid, eid)}), "tab_selected"),
        "tab-count": (lambda: _emit("tab_count", {"count": UIADriver.tab_count(wid, eid)}), "tab_count"),
        "slider-value": (lambda: _emit("slider_value", {"value": UIADriver.slider_value(wid, eid)}), "slider_value"),
        "slider-min": (lambda: _emit("slider_min", {"value": UIADriver.slider_min(wid, eid)}), "slider_min"),
        "slider-max": (lambda: _emit("slider_max", {"value": UIADriver.slider_max(wid, eid)}), "slider_max"),
        "window-close": (lambda: _no_args("window_close", UIADriver.window_close), "window_close"),
        "window-minimize": (lambda: _no_args("window_minimize", UIADriver.window_minimize), "window_minimize"),
        "window-maximize": (lambda: _no_args("window_maximize", UIADriver.window_maximize), "window_maximize"),
        "window-restore": (lambda: _no_args("window_restore", UIADriver.window_restore), "window_restore"),
        "window-state": (lambda: _emit("window_state", {"state": UIADriver.window_state(wid, eid)}), "window_state"),
    }

    _uia_commands_with_args: dict[str, callable] = {
        "scroll": lambda: (
            UIADriver.scroll(wid, eid, args.direction, args.amount, args.count),
            _emit("scroll", {"direction": args.direction, "amount": args.amount, "count": args.count})
        )[1],
        "get-value": lambda: _emit("get_value", {"value": UIADriver.get_value(wid, eid)}),
        "set-value": lambda: (
            UIADriver.set_value(wid, eid, args.value),
            _emit("set_value", {"value": args.value})
        )[1],
        "combo-select": lambda: _with_item("combo_select", UIADriver.combo_select),
        "list-select": lambda: (
            UIADriver.list_select(wid, eid, args.item),
            _emit("list_select", {"item": args.item})
        )[1],
        "tab-select": lambda: (
            UIADriver.tab_select(wid, eid, args.item),
            _emit("tab_select", {"item": args.item})
        )[1],
        "slider-set": lambda: (
            UIADriver.slider_set_value(wid, eid, args.value),
            _emit("slider_set_value", {"value": args.value})
        )[1],
        "transform-move": lambda: (
            UIADriver.transform_move(wid, eid, args.absolute_x, args.absolute_y),
            _emit("transform_move", {"absolute_x": args.absolute_x, "absolute_y": args.absolute_y})
        )[1],
        "transform-resize": lambda: (
            UIADriver.transform_resize(wid, eid, args.width, args.height),
            _emit("transform_resize", {"width": args.width, "height": args.height})
        )[1],
        "transform-rotate": lambda: (
            UIADriver.transform_rotate(wid, eid, args.degrees),
            _emit("transform_rotate", {"degrees": args.degrees})
        )[1],
    }

    try:
        unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
        uia_info = build_uia_control_info(wid, eid)

        if args.dry_run:
            emit_action(True, args.uia_control_command, {**uia_info, "dry_run": True})
            return 0

        cmd = args.uia_control_command
        if cmd in _uia_commands:
            _uia_commands[cmd][0]()
        elif cmd in _uia_commands_with_args:
            _uia_commands_with_args[cmd]()
        else:
            emit_action(False, cmd, {"window_id": str(wid), "element_id": eid, "error": f"unknown uia-control subcommand: {cmd}"})
            return 1
    except Exception as e:  # pylint: disable=broad-exception-caught
        error_data: dict = {"window_id": str(wid), "element_id": eid, "error": str(e)}
        error_data.update(build_error_context(wid))
        emit_action(False, args.uia_control_command, error_data)
        return 1
    return 0


def _handle_screenshot(args: argparse.Namespace) -> int:
    """Handle screenshot subcommands."""
    from windows_driver import WindowsDriver
    from win32_utils import Win32API

    rect = None
    rect_bounds = None
    rect_args = [args.x, args.y, args.width, args.height]
    provided_count = sum(1 for v in rect_args if v is not None)
    if provided_count == 4:
        rect = (args.x, args.y, args.width, args.height)
        rect_bounds = Bounds(x=args.x, y=args.y, width=args.width, height=args.height)
    elif provided_count > 0:
        emit_action(False, "screenshot", {"error": "crop requires all four parameters: --x, --y, --width, --height"})
        return 1

    try:
        if args.dry_run:
            emit(ActionResult(ok=True, code="DRY_RUN", message="screenshot preview generated", data={"window_id": args.window_id, "output": args.output, "rect": rect_bounds}).to_dict())
        else:
            unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
            output_path = WindowsDriver.screenshot_window(args.window_id, args.output, rect)
            emit(ActionResult(ok=True, code="OK", message="screenshot executed", data={"window_id": args.window_id, "output": output_path, "rect": rect_bounds}).to_dict())
        return 0
    except Exception as e:  # pylint: disable=broad-exception-caught
        emit_action(False, "screenshot", {"window_id": str(args.window_id), "output": args.output, "rect": rect_bounds, "error": str(e)})
        return 1


def _handle_wait(args: argparse.Namespace) -> int:
    """Handle wait subcommands."""
    import time

    from wait_utils import PollResult, WaitUtils
    from win32_utils import Win32API

    def _format_window_info(info: dict) -> str:
        """Format window info dict to ElementFormatter style output."""
        formatter = ElementFormatter(
            text=info.get("title", ""),
            class_name=info.get("class_name"),
            extra={
                "window_id": info.get("window_id"),
                "process": info.get("process"),
                "pid": info.get("pid"),
            },
        )
        return formatter.format()

    def _handle_poll_result(
        result: PollResult,
        command_name: str,
        disappear: bool,
        timeout_sec: float,
        extra_info: dict,
        format_fn=None,
    ) -> int:
        """Handle poll result and emit appropriate action."""
        if result.found:
            if disappear:
                emit_action(True, f"{command_name}_disappear", {**extra_info, "elapsed_ms": result.elapsed_ms})
                return 0
            if format_fn and result.data is not None:
                nonce = generate_nonce()
                if isinstance(result.data, list):
                    content = "\n".join(format_fn(m) for m in result.data)
                else:
                    content = format_fn(result.data)
                print(wrap_with_boundary(content, nonce))
            return 0
        emit_action(False, f"{command_name}_timeout", {**extra_info, "timeout_sec": timeout_sec, "disappear": disappear, "error": f"timeout waiting for {command_name} to {'disappear' if disappear else 'appear'}"})
        return 1

    try:
        match args.wait_command:
            case "sleep":
                duration_sec = args.duration_ms / 1000.0
                time.sleep(duration_sec)
                emit_action(True, "sleep", {"duration_ms": args.duration_ms})
                return 0

            case "window":
                result = WaitUtils.poll_condition(
                    check_fn=lambda: WaitUtils.check_window_exists(args.title, args.exact, args.class_name),
                    timeout_sec=args.timeout,
                    interval_sec=args.interval / 1000.0,
                    disappear=args.disappear,
                )
                return _handle_poll_result(
                    result,
                    "window",
                    args.disappear,
                    args.timeout,
                    {"title": args.title},
                    _format_window_info if not args.disappear else None,
                )

            case "text":
                if not args.window_id:
                    emit_action(False, "text", {"error": "--window-id is required for text subcommand"})
                    return 1
                unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                result = WaitUtils.poll_condition(
                    check_fn=lambda: WaitUtils.check_text_exists(args.window_id, args.text, args.exact),
                    timeout_sec=args.timeout,
                    interval_sec=args.interval / 1000.0,
                    disappear=args.disappear,
                )
                return _handle_poll_result(
                    result,
                    "text",
                    args.disappear,
                    args.timeout,
                    {"window_id": str(args.window_id), "text": args.text},
                    str if not args.disappear else None,
                )

            case "uia":
                if not args.window_id:
                    emit_action(False, "uia", {"error": "--window-id is required for uia subcommand"})
                    return 1
                unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                uia_filter_info = {
                    "text": args.text,
                    "control_type": args.control_type,
                    "class_name": args.class_name,
                    "automation_id": args.automation_id,
                    "exact": args.exact,
                }
                result = WaitUtils.poll_condition(
                    check_fn=lambda: WaitUtils.check_uia_exists(args.window_id, args.text, args.control_type, args.class_name, args.automation_id, args.exact),
                    timeout_sec=args.timeout,
                    interval_sec=args.interval / 1000.0,
                    disappear=args.disappear,
                )
                return _handle_poll_result(
                    result,
                    "uia",
                    args.disappear,
                    args.timeout,
                    {"window_id": str(args.window_id), **uia_filter_info},
                    str if not args.disappear else None,
                )

            case "ocr":
                if not args.window_id:
                    emit_action(False, "ocr", {"error": "--window-id is required for ocr subcommand"})
                    return 1
                unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                result = WaitUtils.poll_list_condition(
                    check_fn=lambda: WaitUtils.check_ocr_exists(args.window_id, args.text, args.exact, args.confidence_threshold),
                    timeout_sec=args.timeout,
                    interval_sec=args.interval / 1000.0,
                    disappear=args.disappear,
                )
                return _handle_poll_result(
                    result,
                    "ocr",
                    args.disappear,
                    args.timeout,
                    {"window_id": str(args.window_id), "text": args.text},
                    ElementFormatter.format_element if not args.disappear else None,
                )

            case "image":
                if not args.window_id:
                    emit_action(False, "image", {"error": "--window-id is required for image subcommand"})
                    return 1
                unwrap_result(Win32API.validate_window_id(args.window_id), "invalid window")
                result = WaitUtils.poll_list_condition(
                    check_fn=lambda: WaitUtils.check_image_exists(args.window_id, args.image_path, args.threshold),
                    timeout_sec=args.timeout,
                    interval_sec=args.interval / 1000.0,
                    disappear=args.disappear,
                )
                return _handle_poll_result(
                    result,
                    "image",
                    args.disappear,
                    args.timeout,
                    {"window_id": str(args.window_id), "image_path": args.image_path},
                    ElementFormatter.format_element if not args.disappear else None,
                )

            case _:
                emit_action(False, args.wait_command, {"error": f"unknown wait subcommand: {args.wait_command}"})
                return 1
    except Exception as e:  # pylint: disable=broad-exception-caught
        emit_action(False, args.wait_command, {"error": str(e)})
        return 1


def _handle_clipboard(args: argparse.Namespace) -> int:
    """Handle clipboard subcommands."""
    from clipboard_driver import ClipboardDriver

    try:
        match args.clipboard_command:
            case "copy-files":
                success = ClipboardDriver.copy_files_to_clipboard(args.files)
                if success:
                    emit_action(True, "copy_files", {"files": args.files, "count": len(args.files)})
                    return 0
                emit_action(False, "copy_files", {"files": args.files, "error": "failed to copy files to clipboard"})
                return 1

            case "copy-text":
                success = ClipboardDriver.copy_text_to_clipboard(args.text)
                if success:
                    emit_action(True, "copy_text", {"text": args.text, "length": len(args.text)})
                    return 0
                emit_action(False, "copy_text", {"text": args.text, "error": "failed to copy text to clipboard"})
                return 1

            case "get-text":
                text = ClipboardDriver.get_text_from_clipboard()
                if text is not None:
                    nonce = generate_nonce()
                    print(wrap_with_boundary(text, nonce))
                    return 0
                emit_action(False, "get_text", {"error": "no text in clipboard"})
                return 1

            case _:
                emit_action(False, args.clipboard_command, {"error": f"unknown clipboard subcommand: {args.clipboard_command}"})
                return 1
    except Exception as e:  # pylint: disable=broad-exception-caught
        emit_action(False, args.clipboard_command, {"error": str(e)})
        return 1


def main(argv: Optional[list[str]] = None) -> int:
    """CLI main entry function."""
    if argv is None:
        argv = sys.argv[1:]
    argv = _preprocess_window_id(argv)
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
    except SystemExit:
        return 1

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    handler_map = {
        "window": _handle_window,
        "snapshot": _handle_snapshot,
        "find": _handle_find,
        "action": _handle_action,
        "control": _handle_control,
        "uia-control": _handle_uia_control,
        "screenshot": _handle_screenshot,
        "wait": _handle_wait,
        "clipboard": _handle_clipboard,
    }
    handler = handler_map.get(args.command)
    if handler is None:
        _logger.error("unknown command: %s", args.command)
        emit(ActionResult(ok=False, code="ERROR", message=f"unknown command: {args.command}").to_dict())
        return 1

    try:
        result = handler(args)
        return result
    except ValueError as e:
        _logger.warning("validation error: %s", e)
        emit(ActionResult(ok=False, code="VALIDATION_ERROR", message=str(e)).to_dict())
        return 1
    except Exception as e:  # pylint: disable=broad-exception-caught
        _logger.exception("unexpected error: %s", e)
        emit(ActionResult(ok=False, code="ERROR", message=str(e)).to_dict())
        return 1


def _preprocess_window_id(argv: list[str]) -> list[str]:
    """Preprocess argv to move --window-id to the correct position.

    This allows --window-id to be specified anywhere in the command line.
    For example:
        winguictl --window-id 123 window focus
        winguictl window --window-id 123 focus
        winguictl window focus --window-id 123
        winguictl --window-id 123 wait uia --automation-id chat_input_field
    All become equivalent.
    """
    commands_with_window_id = {"window", "snapshot", "find", "action", "uia-control", "screenshot", "wait"}

    window_id_value = None
    window_id_indices_to_remove = []

    for i, arg in enumerate(argv):
        if arg == "--window-id" and i + 1 < len(argv):
            window_id_value = argv[i + 1]
            window_id_indices_to_remove = [i, i + 1]
            break
        if arg.startswith("--window-id="):
            window_id_value = arg.split("=", 1)[1]
            window_id_indices_to_remove = [i]
            break

    if window_id_value is None:
        return argv

    command_index = None
    for i, arg in enumerate(argv):
        if arg in commands_with_window_id:
            command_index = i
            break

    if command_index is None:
        return argv

    new_argv = []
    for i, arg in enumerate(argv):
        if i not in window_id_indices_to_remove:
            new_argv.append(arg)

    insert_index = 1
    new_argv.insert(insert_index, "--window-id")
    new_argv.insert(insert_index + 1, window_id_value)

    return new_argv


if __name__ == "__main__":
    raise SystemExit(main())
