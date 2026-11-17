"""
reader_sas.py - SAS 格式读入（.sas7bdat/.xpt/.sas7bcat）
自动从 stat_reader.py 拆分生成
"""

from __future__ import annotations
import os
from typing import Any, Optional

import pandas as pd
import pyreadstat

from .reader_core import (ColumnInfo, BaseMeta, StatFileResult, _calc_missing_pct, _get_source_type, _build_column_report, _build_metadata, _extract_pyreadstat_meta, _normalize_value_labels, _normalize_missing_ranges, _normalize_missing_user_values, _normalize_mr_sets)

# ============================================================
# SAS 格式读入（.sas7bdat/.xpt/.sas7bcat）
# ============================================================

def _find_sas_catalog(filepath: str) -> str | None:
    """Find .sas7bcat catalog file in same directory."""
    base_dir = os.path.dirname(filepath)
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    catalog_name = base_name + ".sas7bcat"
    catalog_path = os.path.join(base_dir, catalog_name)
    if os.path.exists(catalog_path):
        return catalog_path
    return None



def _read_sas(filepath, timestamp, *, format_type, user_missing=True, encoding) -> StatFileResult:
    """Read SAS file (.sas7bdat / .xpt / .sd2)."""
    warnings_list = []

    # Auto-detect encoding if user didn't specify one
    if encoding is None:
        from .reader_core import _auto_detect_encoding
        encoding = _auto_detect_encoding(filepath)

    if format_type == "sas_xpt":
        read_kwargs = {"dates_as_pandas_datetime": True}
        if encoding is not None:
            read_kwargs["encoding"] = encoding
        df, meta = pyreadstat.read_xport(filepath, **read_kwargs)
        actual_format = "xpt"
    elif format_type == "sas_sd2":
        raise ValueError(
            "SD2 格式 (SAS Dataset Descriptor) 不被 pyreadstat 支持。\n"
            "请使用 SAS 或 Stat/Transfer 将其转换为 .sas7bdat 后读入，\n"
            "或用 SAS 命令 `proc cport` 转换为 .xpt 格式。"
        )
    else:
        read_kwargs = {"dates_as_pandas_datetime": True, "user_missing": user_missing}
        if encoding is not None:
            read_kwargs["encoding"] = encoding
        df, meta = pyreadstat.read_sas7bdat(filepath, **read_kwargs)
        actual_format = "sas7bdat"

        # sas7bdat: auto-load format catalog
        catalog_path = _find_sas_catalog(filepath)
        if catalog_path:
            try:
                _, catalog_meta = pyreadstat.read_sas7bcat(catalog_path, encoding=encoding)
                df, meta = pyreadstat.set_catalog_to_sas(
                    df, meta, catalog_meta, formats_as_category=False
                )
                warnings_list.append(f"已应用 SAS 格式目录: {os.path.basename(catalog_path)}")
            except Exception as e:
                warnings_list.append(f"读取 SAS 格式目录 {os.path.basename(catalog_path)} 失败: {e}")

    all_meta = _extract_pyreadstat_meta(meta)
    all_meta.pop("file_format", None)

    value_labels = _normalize_value_labels(
        all_meta.get("variable_value_labels", {}),
        all_meta.get("variable_to_label", {}),
        all_meta.get("value_labels", {})
    )
    all_meta["value_labels"] = value_labels
    
    # SAS: pyreadstat 没有 special_missing 属性，需从缺失范围 + 用户缺失值拼接重建
    missing_ranges = _normalize_missing_ranges(all_meta.get("missing_ranges", {}))
    missing_user_values = _normalize_missing_user_values(all_meta.get("missing_user_values", {}))
    special_missing = {}
    for varname, ranges in missing_ranges.items():
        special_missing[varname] = ranges
    for varname, vals in missing_user_values.items():
        if varname not in special_missing:
            special_missing[varname] = vals
    mr_sets = _normalize_mr_sets(all_meta.get("mr_sets", {}))

    if special_missing:
        if user_missing:
            warnings_list.append(
                f"SAS: 保留 {len(special_missing)} 个变量的特殊缺失值信息 | "
                f"SAS: Preserved {len(special_missing)} variables' special missing info"
            )
        else:
            warnings_list.append(
                f"SAS: {len(special_missing)} 个变量的特殊缺失值已转为 NaN（设置 user_missing=True 可保留） | "
                f"SAS: {len(special_missing)} variables' special missing converted to NaN (set user_missing=True to preserve)"
            )
    if mr_sets:
        warnings_list.append(f"SAS 读入：保留 {len(mr_sets)} 个多重响应集（MRSETS）")

    if missing_ranges or missing_user_values:
        if user_missing:
            warnings_list.append(f"SAS 读入：user_missing=True 已保留用户自定义缺失值原始数值")
        else:
            warnings_list.append(f"SAS 读入：user_missing=False 缺失值已变为 NaN（设置 user_missing=True 可保留）")

    column_report = _build_column_report(df, all_meta, value_labels, missing_ranges, missing_user_values, warnings_list, "sas")

    table_label = all_meta.get("table_label")
    if table_label:
        warnings_list.append(f"文件包含表标签 '{table_label}'，已读入到 file_label 字段")

    original_types = all_meta.get("original_variable_types", {})
    sas_formats = {k: v for k, v in original_types.items() if v is not None}
    if sas_formats:
        all_meta["sas_variable_formats"] = sas_formats
        warnings_list.append(f"文件包含 {len(sas_formats)} 个 SAS 格式（如 MONYY, F8.2），已记录在 sas_variable_formats 字段")
    
    # Preserve variable_format from pyreadstat
    variable_format = all_meta.get("variable_format", {})
    if variable_format:
        warnings_list.append(f"SAS 读入：保留 {len(variable_format)} 个变量格式字符串")

    return {
        "dataframe": df,
        "metadata": _build_metadata(all_meta, "sas", {
            "collected_at": timestamp,
            "row_count": df.shape[0],
            "column_count": df.shape[1],
            "total_missing_pct": _calc_missing_pct(df),
        }),
        "warnings": warnings_list,
        "column_report": column_report,
    }


