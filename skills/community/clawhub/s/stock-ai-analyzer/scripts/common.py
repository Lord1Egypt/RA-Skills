#!/usr/bin/env python3
"""Common utilities for data formatting, normalization, and type conversion."""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

import pandas as pd


def normalize_ts_code(code: str) -> str:
    """Normalize common A-share code formats to Tushare ts_code."""
    if not code or not str(code).strip():
        raise ValueError("Stock code cannot be empty.")

    raw = str(code).strip()
    upper = raw.upper()

    if "." in upper:
        prefix, suffix = upper.split(".", 1)
        suffix = suffix.replace("SS", "SH")
        if suffix in {"SH", "SZ", "BJ"}:
            return f"{prefix}.{suffix}"

    if upper.startswith(("SH", "SZ", "BJ")) and len(upper) >= 8:
        return f"{upper[2:]}.{upper[:2]}"

    if raw.isdigit() and len(raw) == 6:
        if raw.startswith(("0", "3")):
            return f"{raw}.SZ"
        if raw.startswith(("6", "9")):
            return f"{raw}.SH"
        if raw.startswith(("4", "8")):
            return f"{raw}.BJ"

    return upper


def normalize_yyyymmdd(value: Optional[str]) -> Optional[str]:
    """Normalize YYYY-MM-DD or YYYYMMDD to YYYYMMDD."""
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    if re.fullmatch(r"\d{8}", raw):
        return raw
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        return raw.replace("-", "")
    raise ValueError(f"Date must be YYYYMMDD or YYYY-MM-DD: {value}")


def dataframe_to_records(df: Optional[pd.DataFrame]) -> List[Dict[str, Any]]:
    """Convert a DataFrame to JSON-serializable records."""
    if df is None or df.empty:
        return []

    cleaned = df.copy()
    for column in cleaned.columns:
        if pd.api.types.is_datetime64_any_dtype(cleaned[column]):
            cleaned[column] = cleaned[column].dt.strftime("%Y-%m-%d")
    cleaned = cleaned.where(pd.notnull(cleaned), None)
    return cleaned.to_dict(orient="records")


def compact_records(records: List[Dict[str, Any]], fields: List[str], limit: int) -> List[Dict[str, Any]]:
    """Keep a bounded list of records and selected fields for model context."""
    compacted: List[Dict[str, Any]] = []
    for record in records[: max(0, limit)]:
        compacted.append({field: record.get(field) for field in fields if field in record})
    return compacted


def sanitize_filename(value: str) -> str:
    """Sanitize a value for use as a filename on Windows."""
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1F]+', "_", str(value or "").strip())
    cleaned = cleaned.strip(" .")
    return cleaned or "report"


def classify_board(code6: str) -> str:
    """Classify an A-share board from the six-digit code."""
    if code6.startswith(("688", "689")):
        return "科创板"
    if code6.startswith(("300", "301")):
        return "创业板"
    if code6.startswith(("4", "8")):
        return "北交所"
    if code6.startswith(("0", "3", "6")):
        return "主板"
    return "其他"


def _to_float(value: Any) -> Optional[float]:
    try:
        f = float(value)
        if pd.isna(f):
            return None
        return f
    except (TypeError, ValueError):
        return None


def _num(value: Any) -> Optional[float]:
    """Safely coerce a value to float, returning None on failure or NaN."""
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None
    return round(f, 4) if f == f else None


def _clean_nan(obj: Any) -> Any:
    """Recursively replace NaN/inf/numpy types with native Python types for valid JSON."""
    # Handle numpy types first
    if hasattr(obj, "item"):  # numpy scalar
        obj = obj.item()
    if isinstance(obj, float):
        if pd.isna(obj) or obj != obj:  # NaN check
            return None
        if obj == float("inf") or obj == float("-inf"):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _clean_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_nan(v) for v in obj]
    return obj
