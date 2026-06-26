"""winguictl - Windows desktop automation CLI tool.

This package provides modules for window management, UIA/Win32 control operations,
OCR, image matching, and screenshot capture.
"""

__version__ = "1.0.0"

from .models import (
    ActionResult,
    Bounds,
    ElementFormatter,
    ElementInfo,
    Ok,
    Err,
    Result,
    Rect,
    WindowInfo,
)
from .constants import VK_CODE_MAP, WIN32_CONTROL_TYPE_MAP

__all__ = [
    "ActionResult",
    "Bounds",
    "ElementFormatter",
    "ElementInfo",
    "Ok",
    "Err",
    "Result",
    "Rect",
    "WindowInfo",
    "VK_CODE_MAP",
    "WIN32_CONTROL_TYPE_MAP",
]
