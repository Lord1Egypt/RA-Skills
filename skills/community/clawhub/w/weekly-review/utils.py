"""通用工具函数（无产品绑定、无数据库发现）."""

from __future__ import annotations


def safe_div(a: float, b: float, default: float = 0.0) -> float:
    """安全除法."""
    return a / b if b else default


def fmt_hours(hours: float) -> str:
    """格式化为小时，保留一位小数. ``hours`` 为小时数."""
    return f"{hours:.1f}h"


def truncate(s: str, max_len: int = 30) -> str:
    """截断字符串."""
    return s if len(s) <= max_len else s[:max_len] + "…"
