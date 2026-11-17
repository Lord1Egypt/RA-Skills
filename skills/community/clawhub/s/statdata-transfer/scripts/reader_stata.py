"""
reader_stata.py - Stata 格式读入（.dta）
自动从 stat_reader.py 拆分生成
"""

from __future__ import annotations
import os
from typing import Any, Optional

import pandas as pd
import pyreadstat

from .reader_core import (ColumnInfo, StataMeta, StatFileResult, _bilingual, _calc_missing_pct, _get_source_type, _build_column_report, _build_metadata, _extract_pyreadstat_meta, _is_stata_special_missing, _normalize_value_labels, _normalize_missing_ranges, _normalize_missing_user_values, _normalize_mr_sets)

# ============================================================
# Stata 格式读入（.dta）
# ============================================================

def _read_stata(filepath, timestamp, *, user_missings, encoding) -> StatFileResult:
    warnings_list = []
    read_kwargs = {"user_missing": user_missings, "dates_as_pandas_datetime": True}
    # Auto-detect encoding if user didn't specify one
    if encoding is None:
        from .reader_core import _auto_detect_encoding
        encoding = _auto_detect_encoding(filepath)
    if encoding is not None:
        read_kwargs["encoding"] = encoding
    df, meta = pyreadstat.read_dta(filepath, **read_kwargs)
    all_meta = _extract_pyreadstat_meta(meta)

    value_labels = _normalize_value_labels(
        all_meta.get("variable_value_labels", {}),
        all_meta.get("variable_to_label", {}),
        all_meta.get("value_labels", {})
    )
    all_meta["value_labels"] = value_labels

    # Stata special missing detection — scan both missing_ranges and missing_user_values
    stata_specials = {}
    if all_meta.get("missing_ranges"):
        for varname, ranges in all_meta["missing_ranges"].items():
            for r in ranges:
                lo = r.get("lo") if isinstance(r, dict) else getattr(r, "lo", None)
                if lo is not None and _is_stata_special_missing(float(lo)):
                    stata_specials.setdefault(varname, []).append(lo)
                    break
    
    # Also detect from missing_user_values (v1.6+ may have 'a'-'z' labels there)
    if all_meta.get("missing_user_values"):
        for varname, vals in all_meta["missing_user_values"].items():
            if isinstance(vals, list):
                for v in vals:
                    if isinstance(v, str) and len(v) == 1 and 'a' <= v <= 'z':
                        if varname not in stata_specials:
                            stata_specials[varname] = []
                        if v not in stata_specials[varname]:
                            stata_specials[varname].append(v)
    
    # When user_missing=True, scan DataFrame for 'a'-'z' character tags
    if user_missings:
        for varname in list(stata_specials.keys()):
            if varname in df.columns:
                col = df[varname]
                char_tags = set()
                for val in col.dropna():
                    if isinstance(val, str) and len(val) == 1 and 'a' <= val <= 'z':
                        char_tags.add(val)
                if char_tags:
                    stata_specials[varname] = sorted(char_tags)
                    warnings_list.append(
                        f"列 '{varname}' Stata 特殊缺失 .a-.z → 保留为字符标签 {sorted(char_tags)} | "
                        f"Column '{varname}' Stata special missing .a-.z → preserved as char tags"
                    )
                elif varname in stata_specials:
                    warnings_list.append(
                        f"列 '{varname}' Stata 特殊缺失 .a-.z → 保留范围信息 | "
                        f"Column '{varname}' Stata special missing .a-.z → range info preserved"
                    )
    else:
        if stata_specials:
            warnings_list.append(
                f"列 {list(stata_specials.keys())} Stata 特殊缺失 .a-.z → 已转为 NaN | "
                f"Columns {list(stata_specials.keys())} Stata special missing .a-.z → converted to NaN"
            )
    
    all_meta["special_missing"] = stata_specials

    column_report = _build_column_report(df, all_meta, value_labels, all_meta.get("missing_ranges", {}), all_meta.get("missing_user_values", {}), warnings_list, "stata")

    return {
        "dataframe": df,
        "metadata": _build_metadata(all_meta, "stata", {"collected_at": timestamp, "row_count": df.shape[0], "column_count": df.shape[1], "total_missing_pct": _calc_missing_pct(df)}),
        "warnings": warnings_list,
        "column_report": column_report,
    }


