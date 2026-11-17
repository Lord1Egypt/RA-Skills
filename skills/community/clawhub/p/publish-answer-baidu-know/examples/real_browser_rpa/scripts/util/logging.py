"""示例结构化日志工具。"""

from __future__ import annotations

import logging
import re
from typing import Any

from util.constants import LOG_LOGGER_NAME


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name or LOG_LOGGER_NAME)


def mask_text(value: str, *, keep_start: int = 2, keep_end: int = 2) -> str:
    s = (value or "").strip()
    if len(s) >= 11 and s.isdigit():
        return s[:3] + "****" + s[-4:]
    if len(s) > keep_start + keep_end:
        return s[:keep_start] + "****" + s[-keep_end:]
    return "****"


def safe_log_value(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    if re.fullmatch(r"\d{7,}", text):
        return mask_text(text)
    if "@" in text and len(text) > 6:
        local, _, domain = text.partition("@")
        return f"{mask_text(local, keep_start=1, keep_end=1)}@{domain}"
    return text
