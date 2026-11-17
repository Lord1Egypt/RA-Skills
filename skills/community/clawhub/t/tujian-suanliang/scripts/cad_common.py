#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""算量内核共用的标量清洗助手。

各内核过去各自抄一份 `_number`/`_text`/`_round`，改一处要改十几处。
这里只收语义完全一致的那一份：数值清洗失败返回默认值、文字清洗不剥空格、
剥空格的标签清洗单独叫 `to_label`，避免两种行为混成一个函数。
几何类助手（bbox、距离、面域）各内核算法口径不同，不在此合并。
"""
from __future__ import annotations

from typing import Any

__all__ = ["to_number", "to_text", "to_label", "round_number"]


def to_number(value: Any, default: float = 0.0) -> float:
    """转 float；空值或脏数据返回 default，不抛异常。"""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def to_text(value: Any) -> str:
    """转字符串，None 当空串；不剥首尾空格（原文照抄是算量对账的前提）。"""
    return "" if value is None else str(value)


def to_label(value: Any) -> str:
    """转字符串并剥首尾空格，用于表格行标签和图名。"""
    return str(value if value is not None else "").strip()


def round_number(value: Any, digits: int = 4) -> float:
    """按 digits 四舍五入；脏数据当 0 处理，保持台账列不为空。"""
    return round(to_number(value), digits)
