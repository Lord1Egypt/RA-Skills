#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-FileCopyrightText: Fushan Wen <qydwhotmail@gmail.com>
# SPDX-License-Identifier: MIT

"""Element finding driver module.

Provides multiple element finding strategies:
- find_text: Find text through UIA or Win32 enumeration
- find_uia: Find controls through UIA tree
- find_image: Find images through OpenCV template matching
"""

import itertools
import logging
from collections import Counter
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

import win32gui

from constants import check_opencv_available, cv2, np
from models import Bounds, ElementFormatter, ElementInfo
from uia_driver import _get_uia_desktop
from win32_utils import Win32API

if TYPE_CHECKING:
    from pywinauto.uia_element_info import UIAElementInfo

_logger = logging.getLogger(__name__)


def _format_runtime_id(runtime_id_raw: Any) -> Optional[str]:
    """Format runtime_id tuple/list into a dash-separated string.

    Note: UIAElementInfo.runtime_id returns 0 on COMError, not None.
    This function handles both None and 0 as invalid values.
    """
    if not runtime_id_raw:
        return None
    return "-".join(str(x) for x in runtime_id_raw)


def _check_duplicate_automation_ids(automation_ids: list[str]) -> Optional[str]:
    """Check for duplicate automation_id values and return warning message if found.

    Args:
        automation_ids: List of automation_id values to check

    Returns:
        Warning message string if duplicates found, None otherwise
    """
    if not automation_ids:
        return None
    counter = Counter(automation_ids)
    duplicates = [aid for aid, count in counter.items() if count > 1]
    if not duplicates:
        return None
    dup_list = ", ".join(f'"{aid}"' for aid in duplicates)
    return (
        f"WARNING: Duplicate automation_id detected: {dup_list}. "
        "Prefer runtime_id for element identification."
    )


def _is_valid_rect(rect) -> bool:
    """Check if rectangle has valid non-zero dimensions.

    Note: UIAElementInfo.rectangle never returns None - it returns a zeroed RECT()
    on COMError. This function checks for both None and zero dimensions.
    """
    if rect is None:
        return False
    try:
        return rect.right > rect.left and rect.bottom > rect.top
    except (AttributeError, TypeError) as e:
        _logger.debug("Invalid rect format: %s", e)
        return False


class FindDriver:
    """Driver class for element finding operations."""

    @staticmethod
    def _get_uia_element_id(info: "UIAElementInfo") -> str:
        """Generate a unique identifier string from UIA element info.

        Always returns a UIA-compatible identifier that can be resolved by
        _get_uia_wrapper(). Priority order:
        1. runtime_id (if available and non-zero; UIAElementInfo returns 0 on COMError)
        2. automation_id (if available and non-empty)
        3. handle with uia- prefix (if available and non-zero)
        4. control_id with uia- prefix (if available)
        5. fallback to id(info)

        Note:
            runtime_id is preferred over automation_id because automation_id may have
            duplicates, especially in Qt applications where multiple controls can share
            the same automation_id. runtime_id is guaranteed to be unique within a
            desktop session.

            A plain hwnd string (e.g. "12345") is NOT used because _get_uia_wrapper
            interprets it as an automation_id search, which would fail. Instead,
            handles are prefixed with "uia-" to use runtime_id-style lookup.
        """
        runtime_id_raw = getattr(info, "runtime_id", None)
        if runtime_id_raw:
            return f"uia-{_format_runtime_id(runtime_id_raw)}"
        automation_id = (
            getattr(info, "auto_id", None)
            or getattr(info, "automation_id", "")
            or ""
        ).strip()
        if automation_id:
            return automation_id
        handle = getattr(info, "handle", None)
        if handle:
            return f"uia-hwnd-{handle}"
        control_id = getattr(info, "control_id", None)
        if control_id is not None:
            return f"uia-{control_id}"
        return f"uia-{id(info)}"

    @staticmethod
    def find_text(window_id: int, text: str, exact: bool = False) -> str:
        """Find specified text in the window.

        Prioritizes UIA tree search; falls back to Win32 enumeration if no results found.
        Adds a warning comment to output when UIA search fails and Win32 fallback is used.

        Args:
            window_id: Window handle
            text: Text to find
            exact: Whether to match exactly

        Returns:
            Formatted matching result string with window-relative coordinates.
            May include a warning comment if UIA search failed.
        """
        query = text.strip()
        if not query:
            raise ValueError("text query must not be empty")
        matches: list[ElementInfo] = []
        lowered_query = query.casefold()
        uia_failed = False

        try:
            desktop = _get_uia_desktop()
            wrapper = desktop.window(handle=window_id)

            window_bounds_result = Win32API.get_window_bounds(window_id)
            window_bounds = window_bounds_result.value if window_bounds_result.is_ok else None
            win_x = window_bounds.x if window_bounds else 0
            win_y = window_bounds.y if window_bounds else 0

            for child in wrapper.iter_descendants():
                try:
                    info = child.element_info
                    name = (getattr(info, "name", "") or "").strip()
                    if not name:
                        continue
                    lowered = name.casefold()
                    is_match = lowered == lowered_query if exact else lowered_query in lowered
                    if not is_match:
                        continue
                    rect = getattr(info, "rectangle", None)
                    if not _is_valid_rect(rect):
                        continue
                    element_id = FindDriver._get_uia_element_id(info)
                    runtime_id = _format_runtime_id(getattr(info, "runtime_id", None))
                    control_id = getattr(info, "control_id", None)
                    control_type = (getattr(info, "control_type", "") or "").strip() or "uia-text"

                    matches.append(
                        ElementInfo(
                            element_id=element_id,
                            window_id=str(window_id),
                            text=name,
                            bounds=Bounds.from_rect_relative(rect, win_x, win_y),
                            class_name=(getattr(info, "class_name", "") or "").strip() or None,
                            control_type=control_type,
                            control_id=control_id,
                            runtime_id=runtime_id,
                            source="uia",
                            confidence=1.0 if exact else 0.95,
                        )
                    )
                except Exception:  # pylint: disable=broad-exception-caught
                    _logger.exception("Error processing UIA descendant")
                    continue
        except Exception:  # pylint: disable=broad-exception-caught
            _logger.exception("UIA traversal failed for window %d", window_id)
            uia_failed = True

        if not matches:
            matches = FindDriver._find_text_win32(window_id, text, exact)

        result_lines: list[str] = []
        if uia_failed and matches:
            result_lines.append("WARNING: UIA search failed, results from Win32 fallback")
        result_lines.extend(ElementFormatter.format_element(m) for m in matches)
        return "\n".join(result_lines)

    @staticmethod
    def _find_text_win32(hwnd: int, text: str, exact: bool = False) -> list[ElementInfo]:
        """Find text through Win32 EnumChildWindows enumeration (UIA fallback).

        Returns coordinates relative to the window (not screen absolute).
        """
        query = text.strip()
        lowered_query = query.casefold()
        matches: list[ElementInfo] = []

        window_bounds_result = Win32API.get_window_bounds(hwnd)
        window_bounds = window_bounds_result.value if window_bounds_result.is_ok else None
        win_x = window_bounds.x if window_bounds else 0
        win_y = window_bounds.y if window_bounds else 0

        def add_match(candidate_hwnd: int) -> None:
            title = Win32API.get_window_text(candidate_hwnd)
            if not title:
                return
            lowered_title = title.casefold()
            is_match = lowered_title == lowered_query if exact else lowered_query in lowered_title
            if not is_match:
                return
            bounds_result = Win32API.get_window_bounds(candidate_hwnd)
            if bounds_result.is_err:
                return
            bounds = bounds_result.value

            matches.append(
                ElementInfo(
                    element_id=str(candidate_hwnd),
                    window_id=str(hwnd),
                    text=title,
                    bounds=Bounds.from_bounds_relative(bounds, win_x, win_y),
                    class_name=Win32API.get_class_name(candidate_hwnd),
                    control_type="win32-child",
                    source="win32-text",
                    confidence=1.0 if exact else 0.85,
                )
            )

        add_match(hwnd)

        def child_callback(child_hwnd: int, _lparam: int) -> bool:
            if not win32gui.IsWindowVisible(child_hwnd):
                return True
            add_match(child_hwnd)
            return True

        win32gui.EnumChildWindows(hwnd, child_callback, 0)
        return matches

    @staticmethod
    def find_uia(
        window_id: int,
        text: Optional[str] = None,
        control_type: Optional[str] = None,
        class_name: Optional[str] = None,
        automation_id: Optional[str] = None,
        action: Optional[str] = None,
        exact: bool = False,
        skip_actions: bool = False,
        skip_state: bool = False,
    ) -> str:
        """Find controls through the UIA tree.

        At least one filter must be provided.

        Note: The search includes the window wrapper itself as the first candidate.
        If the window's own name/control_type matches the filter, it will appear
        in results. This is intentional to support finding top-level window properties.

            When duplicate automation_id values are detected, a warning is prepended
            to the output. runtime_id is preferred for element identification as it
            is guaranteed unique within a desktop session.

        Args:
            window_id: Window handle
            text: Text filter condition (optional)
            control_type: Control type filter condition (optional)
            class_name: Window class name filter condition (optional)
            automation_id: Automation ID filter condition (optional)
            action: Supported action filter condition (optional, e.g. "set-text")
            exact: Whether to match exactly
            skip_actions: If True, skip collecting supported actions (faster for Qt apps)
            skip_state: If True, skip collecting element state (faster for Qt apps)

        Returns:
            Formatted matching result string with window-relative coordinates.
        """
        if text is None and control_type is None and class_name is None \
                and automation_id is None and action is None:
            raise ValueError("find_uia requires at least one filter")
        desktop = _get_uia_desktop()
        wrapper = desktop.window(handle=window_id)

        window_bounds_result = Win32API.get_window_bounds(window_id)
        window_bounds = window_bounds_result.value if window_bounds_result.is_ok else None
        win_x = window_bounds.x if window_bounds else 0
        win_y = window_bounds.y if window_bounds else 0

        def normalize(value: Optional[str]) -> str:
            return (value or "").strip()

        uia_control_type: Optional[str] = None
        if control_type is not None and exact:
            try:
                from pywinauto.uia_defines import IUIA
                ct_lower = control_type.strip().casefold()
                for k in IUIA().known_control_types:
                    if k.casefold() == ct_lower:
                        uia_control_type = k
                        break
            except Exception:  # pylint: disable=broad-exception-caught
                _logger.exception("Failed to resolve UIA control type")

        _control_type_aliases: dict[str, list[str]] = {
            "edit": ["document"],
        }
        lowered_ct_aliases: list[str] = []
        if control_type is not None:
            aliases = _control_type_aliases.get(control_type.strip().casefold(), [])
            lowered_ct_aliases = [a.casefold() for a in aliases]
            if uia_control_type and lowered_ct_aliases:
                uia_control_type = None

        lowered_text = normalize(text).casefold() if text is not None else None
        lowered_ct = normalize(control_type).casefold() if control_type is not None else None
        lowered_class = normalize(class_name).casefold() if class_name is not None else None
        lowered_aid = normalize(automation_id).casefold() if automation_id is not None else None

        iter_kwargs = {"control_type": uia_control_type} if uia_control_type else {}
        candidates = itertools.chain([wrapper], wrapper.iter_descendants(**iter_kwargs))

        priority_results: list[ElementInfo] = []
        other_results: list[ElementInfo] = []
        seen_runtime_ids: set[str] = set()
        automation_ids: list[str] = []

        for candidate in candidates:
            info = candidate.element_info
            candidate_name = normalize(getattr(info, "name", ""))
            candidate_control_type = normalize(getattr(info, "control_type", ""))

            if text is not None:
                name_cf = candidate_name.casefold()
                if exact:
                    if name_cf != lowered_text:
                        continue
                else:
                    if lowered_text not in name_cf:
                        continue

            if control_type is not None and uia_control_type is None:
                ct_cf = candidate_control_type.casefold()
                if exact:
                    if ct_cf != lowered_ct and ct_cf not in lowered_ct_aliases:
                        continue
                else:
                    if lowered_ct not in ct_cf and not any(a in ct_cf for a in lowered_ct_aliases):
                        continue

            rect = getattr(info, "rectangle", None)
            if not _is_valid_rect(rect):
                continue

            candidate_automation_id = normalize(
                getattr(info, "auto_id", None) or getattr(info, "automation_id", "")
            )
            candidate_class_name = normalize(getattr(info, "class_name", ""))

            if class_name is not None:
                class_cf = candidate_class_name.casefold()
                if exact:
                    if class_cf != lowered_class:
                        continue
                else:
                    if lowered_class not in class_cf:
                        continue

            if automation_id is not None:
                aid_cf = candidate_automation_id.casefold()
                if exact:
                    if aid_cf != lowered_aid:
                        continue
                else:
                    if lowered_aid not in aid_cf:
                        continue

            if candidate_automation_id:
                automation_ids.append(candidate_automation_id)
            element_id = FindDriver._get_uia_element_id(info)
            control_id = getattr(info, "control_id", None)
            runtime_id = _format_runtime_id(getattr(info, "runtime_id", None))

            if runtime_id in seen_runtime_ids:
                continue
            seen_runtime_ids.add(runtime_id)

            from uia_driver import get_element_state, get_supported_actions
            element_actions = [] if skip_actions else get_supported_actions(info)
            element_state = {} if skip_state else get_element_state(info)

            if action is not None and not skip_actions:
                if action.casefold() not in (a.casefold() for a in element_actions):
                    continue

            element_info = ElementInfo(
                element_id=element_id,
                window_id=str(window_id),
                text=candidate_name or candidate_control_type or candidate_automation_id,
                bounds=Bounds.from_rect_relative(rect, win_x, win_y),
                class_name=candidate_class_name or None,
                control_type=candidate_control_type or None,
                automation_id=candidate_automation_id or None,
                control_id=control_id,
                runtime_id=runtime_id,
                source="uia",
                confidence=1.0 if exact else 0.95,
                supported_actions=element_actions if element_actions else None,
                state=element_state if element_state else None,
            )

            if candidate_class_name == "UIProperty":
                other_results.append(element_info)
            else:
                priority_results.append(element_info)

        combined_results = priority_results + other_results
        warning = _check_duplicate_automation_ids(automation_ids)
        result_lines: list[str] = []
        if warning:
            result_lines.append(warning)

        result_lines.extend(ElementFormatter.format_element(r) for r in combined_results)
        return "\n".join(result_lines)

    @staticmethod
    def find_image(  # pylint: disable=too-many-locals
        window_id: int,
        image_path: str,
        threshold: float = 0.9,
        overlap_threshold: float = 0.5,
    ) -> list[ElementInfo]:
        """Find image template in window using OpenCV template matching.

        Args:
            window_id: Window handle
            image_path: Template image file path
            threshold: Match confidence threshold (0-1)
            overlap_threshold: IoU threshold for non-maximum suppression (0-1).
                               Higher values allow more overlapping matches.
                               Default 0.5 means matches with >50% overlap are suppressed.

        Returns:
            List of matching ElementInfo

        Raises:
            RuntimeError: If opencv-python is not installed or image cannot be loaded
            ValueError: If threshold parameters are out of valid range
        """
        check_opencv_available()

        if not 0.0 <= threshold <= 1.0:
            raise ValueError(f"threshold must be between 0 and 1, got {threshold}")
        if not 0.0 <= overlap_threshold <= 1.0:
            raise ValueError(f"overlap_threshold must be between 0 and 1, got {overlap_threshold}")

        _, _, width, height, data = Win32API.capture_window_bgra(window_id)
        if width <= 0 or height <= 0:
            raise RuntimeError(f"invalid window dimensions for image matching: {width}x{height}")
        img_array = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 4))
        img_bgr = img_array[:, :, :3]
        template = cv2.imread(image_path, cv2.IMREAD_COLOR)  # pylint: disable=no-member
        if template is None:
            raise RuntimeError(f"failed to load template image: {image_path}")
        result = cv2.matchTemplate(img_bgr, template, cv2.TM_CCOEFF_NORMED)  # pylint: disable=no-member
        locations = np.where(result >= threshold)
        template_h, template_w = template.shape[:2]
        raw_matches: list[tuple[int, int, float]] = []
        for pt in zip(*locations[::-1]):
            score = float(result[pt[1], pt[0]])
            raw_matches.append((int(pt[0]), int(pt[1]), score))
        raw_matches.sort(key=lambda m: m[2], reverse=True)

        kept: list[tuple[int, int, float]] = []
        for x, y, score in raw_matches:
            suppressed = False
            for kx, ky, _ in kept:
                overlap_x = max(0, min(x + template_w, kx + template_w) - max(x, kx))
                overlap_y = max(0, min(y + template_h, ky + template_h) - max(y, ky))
                overlap_area = overlap_x * overlap_y
                area = template_w * template_h
                if area > 0 and overlap_area / area > overlap_threshold:
                    suppressed = True
                    break
            if not suppressed:
                kept.append((x, y, score))

        matches: list[ElementInfo] = []
        for x, y, score in kept:
            matches.append(
                ElementInfo(
                    element_id=f"image-{x}-{y}",
                    window_id=str(window_id),
                    text=Path(image_path).name,
                    bounds=Bounds(x=x, y=y, width=template_w, height=template_h),
                    source="image",
                    confidence=score,
                )
            )
        return matches
