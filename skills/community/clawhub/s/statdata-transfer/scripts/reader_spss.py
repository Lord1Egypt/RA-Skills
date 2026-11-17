"""
reader_spss.py - SPSS 格式读入（.sav/.zsav/.por）
自动从 stat_reader.py 拆分生成
"""

from __future__ import annotations
import os
from typing import Any, Optional

import pandas as pd
import pyreadstat

from .reader_core import (ColumnInfo, BaseMeta, MRSet, MissingRange, _calc_missing_pct, _get_source_type, _build_column_report, _build_metadata, _extract_pyreadstat_meta, _normalize_value_labels, _normalize_missing_ranges, _normalize_missing_user_values, _normalize_mr_sets)

# ============================================================
# SPSS 格式读入（.sav/.zsav/.por）
# ============================================================

def _read_spss(filepath, timestamp, *, format_type, user_missings, encoding) -> StatFileResult:
    """读入 SPSS 格式文件（.sav / .zsav / .por）"""
    warnings_list = []
    read_kwargs = {"user_missing": user_missings, "dates_as_pandas_datetime": True}
    # Auto-detect encoding if user didn't specify one
    if encoding is None:
        from .reader_core import _auto_detect_encoding
        encoding = _auto_detect_encoding(filepath)
    if encoding is not None:
        read_kwargs["encoding"] = encoding

    if format_type == "spss_zsav":
        try:
            df, meta = pyreadstat.read_zsav(filepath, **read_kwargs)
        except (AttributeError, Exception):
            # Fallback for pyreadstat < 1.2
            import gzip, shutil as _shutil, tempfile as _tf
            tmp_sav = _tf.NamedTemporaryFile(suffix='.sav', delete=False)
            tmp_sav.close()
            try:
                with gzip.open(filepath, 'rb') as f_in:
                    with open(tmp_sav.name, 'wb') as f_out:
                        _shutil.copyfileobj(f_in, f_out)
                df, meta = pyreadstat.read_sav(tmp_sav.name, **read_kwargs)
            finally:
                if os.path.exists(tmp_sav.name):
                    os.unlink(tmp_sav.name)
    elif format_type == "spss_por":
        df, meta = pyreadstat.read_por(filepath, **read_kwargs)
    else:
        df, meta = pyreadstat.read_sav(filepath, **read_kwargs)

    all_meta = _extract_pyreadstat_meta(meta)
    all_meta.pop("file_format", None)  # pyreadstat 返回 'sav/zsav'，不需要

    value_labels = _normalize_value_labels(
        all_meta.get("variable_value_labels", {}),
        all_meta.get("variable_to_label", {}),
        all_meta.get("value_labels", {})
    )
    all_meta["value_labels"] = value_labels

    # Special missing: combine missing_ranges and missing_user_values
    special_missing = {}
    missing_ranges = _normalize_missing_ranges(all_meta.get("missing_ranges", {}))
    missing_user_values = _normalize_missing_user_values(all_meta.get("missing_user_values", {}))
    
    for varname, ranges in missing_ranges.items():
        special_missing[varname] = ranges
    
    for varname, vals in missing_user_values.items():
        if varname not in special_missing:
            special_missing[varname] = vals
    
    if special_missing:
        if user_missings:
            warnings_list.append(
                f"列 {list(special_missing.keys())} SPSS 用户自定义缺失值已保留原始数值 | "
                f"Columns {list(special_missing.keys())} SPSS user-defined missing values preserved"
            )
        else:
            warnings_list.append(
                f"列 {list(special_missing.keys())} SPSS 用户自定义缺失值已转为 NaN | "
                f"Columns {list(special_missing.keys())} SPSS user-defined missing values converted to NaN"
            )
    
    all_meta["special_missing"] = special_missing

    # MR sets
    mr_sets_serialized = _normalize_mr_sets(all_meta.get("mr_sets", {}))
    if mr_sets_serialized:
        warnings_list.append(
            f"文件包含 {len(mr_sets_serialized)} 个多重响应集，读入后不保留结构 | "
            f"File contains {len(mr_sets_serialized)} MR sets, structure not preserved after reading"
        )

    column_report = _build_column_report(df, all_meta, value_labels, missing_ranges, missing_user_values, warnings_list, "spss")

    return {
        "dataframe": df,
        "metadata": _build_metadata(all_meta, "spss", {
            "collected_at": timestamp,
            "row_count": df.shape[0],
            "column_count": df.shape[1],
            "total_missing_pct": _calc_missing_pct(df),
        }),
        "warnings": warnings_list,
        "column_report": column_report,
    }


