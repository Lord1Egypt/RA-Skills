"""
reader_modern.py - 现代数据格式（JSON/XML/ODS/HTML）
"""

from __future__ import annotations
import json
import os
from typing import Any

import pandas as pd

from .reader_core import (ColumnInfo, JsonMeta, XmlMeta, OdsMeta, HtmlMeta, StatFileResult, _bilingual, _calc_missing_pct, _get_source_type, _parse_value_labels, _build_column_report)

# ============================================================
# 现代数据格式（JSON/XML/ODS/HTML）
# ============================================================

def _read_json(filepath: str, timestamp: str) -> StatFileResult:
    """读入 JSON 文件，支持 meta+data 包裹结构以保留标签"""
    warnings_list = []
    warnings_list.append(_bilingual("JSON format only supports variable_labels and value_labels in {meta:{...}, data:[...]} wrapper structure, no other statistical metadata", "JSON 格式仅在使用 {\"meta\":{}, \"data\":[]} 包裹结构时可保留 variable_labels 和 value_labels，不含其他统计元数据"))
    json_metadata: dict[str, Any] = {}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    
    var_labels = {}
    val_labels = {}
    data_part = None
    
    # Check for wrapper structure
    if isinstance(raw, dict) and "data" in raw:
        data_part = raw["data"]
        if "meta" in raw:
            meta = raw["meta"]
            if isinstance(meta, dict):
                var_labels = meta.get("variable_labels", {})
                val_raw = meta.get("value_labels", {})
                val_labels = _parse_value_labels(val_raw)
    else:
        data_part = raw
    
    df = pd.json_normalize(data_part) if isinstance(data_part, list) else pd.DataFrame(data_part)
    
    json_metadata["num_rows"] = len(df)
    json_metadata["num_columns"] = len(df.columns)
    json_metadata["column_names"] = list(df.columns)
    json_metadata["has_meta"] = bool(var_labels or val_labels)
    
    if df.empty:
        warnings_list.append(_bilingual("JSON file parsed result is empty", "JSON 文件解析结果为空"))

    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        column_report[col] = ColumnInfo(
            source_type=_get_source_type(df[col]),
            pandas_dtype=str(df[col].dtype),
            original_label=var_labels.get(col),
            has_value_labels=bool(val_labels.get(col)),
            n_missing=int(df[col].isnull().sum()),
            missing_are_special=False,
            precision_warning=False,
            format_string=None,
            display_width=None,
            storage_width=None,
            measure_level=None,
            alignment=None,
            original_type=None,
        )
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                column_report[col]["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")

    return {
        "dataframe": df,
        "metadata": JsonMeta(
            file_format="json", collected_at=timestamp,
            row_count=df.shape[0], column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels=var_labels, value_labels=val_labels, special_missing={},
            date_origin=None, file_encoding=None, file_label=None,
            creation_time=None, modification_time=None, notes=[],
            original_variable_types={}, readstat_variable_types={},
            variable_value_labels={}, variable_to_label={},
            missing_user_values={}, missing_ranges={},
            variable_display_width={}, variable_storage_width={},
            variable_measure={}, variable_alignment={},
            column_names_to_labels={}, mr_sets={}, table_name=None,
            json_metadata=json_metadata,
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }


def _read_xml(filepath: str, timestamp: str) -> StatFileResult:
    """读入 XML 文件，使用 pd.read_xml。"""
    warnings_list = []
    warnings_list.append(_bilingual("XML format does not contain statistical metadata like variable/value labels, only raw data values", "XML 格式不含变量标签、值标签等统计元数据，仅保留原始数据值"))
    xml_metadata: dict[str, Any] = {}

    df = pd.read_xml(filepath)

    xml_metadata["num_rows"] = len(df)
    xml_metadata["num_columns"] = len(df.columns)
    xml_metadata["column_names"] = list(df.columns)

    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        column_report[col] = ColumnInfo(
            source_type=_get_source_type(df[col]),
            pandas_dtype=str(df[col].dtype),
            original_label=None,
            has_value_labels=False,
            n_missing=int(df[col].isnull().sum()),
            missing_are_special=False,
            precision_warning=False,
            format_string=None,
            display_width=None,
            storage_width=None,
            measure_level=None,
            alignment=None,
            original_type=None,
        )
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                column_report[col]["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")

    return {
        "dataframe": df,
        "metadata": XmlMeta(
            file_format="xml", collected_at=timestamp,
            row_count=df.shape[0], column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={}, value_labels={}, special_missing={},
            date_origin=None, file_encoding=None, file_label=None,
            creation_time=None, modification_time=None, notes=[],
            original_variable_types={}, readstat_variable_types={},
            variable_value_labels={}, variable_to_label={},
            missing_user_values={}, missing_ranges={},
            variable_display_width={}, variable_storage_width={},
            variable_measure={}, variable_alignment={},
            column_names_to_labels={}, mr_sets={}, table_name=None,
            xml_metadata=xml_metadata,
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }


def _read_ods(filepath: str, timestamp: str) -> StatFileResult:
    """读入 ODS 文件，使用 pd.read_excel(engine='odf')。"""
    warnings_list = []
    warnings_list.append(_bilingual("ODS format does not contain statistical metadata like variable/value labels, only raw data values", "ODS 格式不含变量标签、值标签等统计元数据，仅保留原始数据值"))

    xl = pd.ExcelFile(filepath, engine="odf")
    sheet_names = xl.sheet_names
    if len(sheet_names) == 0:
        raise ValueError(_bilingual("ODS file does not contain any worksheet", "ODS 文件不包含任何工作表"))

    # Select the largest sheet
    selected_sheet = None
    if len(sheet_names) == 1:
        selected_sheet = sheet_names[0]
    else:
        sheet_sizes = {}
        for name in sheet_names:
            try:
                temp_df = pd.read_excel(filepath, sheet_name=name, engine="odf")
                sheet_sizes[name] = len(temp_df)
            except Exception:
                sheet_sizes[name] = 0
        selected_sheet = max(sheet_sizes, key=sheet_sizes.get)

    df = pd.read_excel(filepath, sheet_name=selected_sheet, engine="odf")

    ods_metadata: dict[str, Any] = {
        "sheet_names": sheet_names,
        "selected_sheet": selected_sheet,
        "total_sheets": len(sheet_names),
    }

    if len(sheet_names) > 1:
        warnings_list.append(
            _bilingual(f"ODS file contains {len(sheet_names)} sheets, selected '{selected_sheet}'", f"ODS 文件包含 {len(sheet_names)} 个工作表，已选择 '{selected_sheet}'")
        )

    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        column_report[col] = ColumnInfo(
            source_type=_get_source_type(df[col]),
            pandas_dtype=str(df[col].dtype),
            original_label=None,
            has_value_labels=False,
            n_missing=int(df[col].isnull().sum()),
            missing_are_special=False,
            precision_warning=False,
            format_string=None,
            display_width=None,
            storage_width=None,
            measure_level=None,
            alignment=None,
            original_type=None,
        )
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                column_report[col]["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")

    return {
        "dataframe": df,
        "metadata": OdsMeta(
            file_format="ods", collected_at=timestamp,
            row_count=df.shape[0], column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={}, value_labels={}, special_missing={},
            date_origin=None, file_encoding=None, file_label=None,
            creation_time=None, modification_time=None, notes=[],
            original_variable_types={}, readstat_variable_types={},
            variable_value_labels={}, variable_to_label={},
            missing_user_values={}, missing_ranges={},
            variable_display_width={}, variable_storage_width={},
            variable_measure={}, variable_alignment={},
            column_names_to_labels={}, mr_sets={}, table_name=None,
            ods_metadata=ods_metadata,
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }


def _read_html(filepath: str, timestamp: str) -> StatFileResult:
    """读入 HTML 文件，使用 pd.read_html（可能返回多个表），返回第一个表。"""
    warnings_list = []
    warnings_list.append(_bilingual("HTML format does not contain statistical metadata like variable/value labels, only raw data values", "HTML 格式不含变量标签、值标签等统计元数据，仅保留原始数据值"))

    # Read all tables from HTML
    tables = pd.read_html(filepath)
    if not tables:
        raise ValueError(_bilingual("HTML file contains no <table> elements", "HTML 文件未找到任何 <table> 元素"))

    html_metadata: dict[str, Any] = {
        "total_tables": len(tables),
        "table_sizes": [],
    }
    for i, tbl in enumerate(tables):
        html_metadata["table_sizes"].append({
            "index": i,
            "rows": len(tbl),
            "columns": len(tbl.columns),
        })

    # Select the largest table
    best_idx = 0
    best_size = 0
    for i, tbl in enumerate(tables):
        tbl_size = len(tbl) * len(tbl.columns)
        if tbl_size > best_size:
            best_size = tbl_size
            best_idx = i

    df = tables[best_idx]
    html_metadata["selected_table_index"] = best_idx
    html_metadata["selected_table_rows"] = len(df)
    html_metadata["selected_table_columns"] = len(df.columns)

    if len(tables) > 1:
        warnings_list.append(
            f"HTML 文件包含 {len(tables)} 个 <table> 元素，已选择第 {best_idx + 1} 个（{len(df)} 行 × {len(df.columns)} 列，共 {best_size} 个单元格） | HTML file contains {len(tables)} <table> elements, selected #{best_idx + 1} ({len(df)} rows × {len(df.columns)} cols, {best_size} cells total)"
        )

    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        column_report[col] = ColumnInfo(
            source_type=_get_source_type(df[col]),
            pandas_dtype=str(df[col].dtype),
            original_label=None,
            has_value_labels=False,
            n_missing=int(df[col].isnull().sum()),
            missing_are_special=False,
            precision_warning=False,
            format_string=None,
            display_width=None,
            storage_width=None,
            measure_level=None,
            alignment=None,
            original_type=None,
        )
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                column_report[col]["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")

    return {
        "dataframe": df,
        "metadata": HtmlMeta(
            file_format="html", collected_at=timestamp,
            row_count=df.shape[0], column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={}, value_labels={}, special_missing={},
            date_origin=None, file_encoding=None, file_label=None,
            creation_time=None, modification_time=None, notes=[],
            original_variable_types={}, readstat_variable_types={},
            variable_value_labels={}, variable_to_label={},
            missing_user_values={}, missing_ranges={},
            variable_display_width={}, variable_storage_width={},
            variable_measure={}, variable_alignment={},
            column_names_to_labels={}, mr_sets={}, table_name=None,
            html_metadata=html_metadata,
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }


def _detect_delimiter(filepath: str, encoding: str) -> tuple:
    """从文件前几行探测分隔符，返回 (sep, auto_detected: bool)。
    
    常见分隔符：逗号、分号、制表符、竖线。若探测结果与默认逗号不同，
    标记 auto_detected=True 以便上层告警（欧洲 CSV 常用分号）。
    """
    import csv as _csv
    try:
        with open(filepath, "r", encoding=encoding, errors="replace", newline="") as f:
            sample_lines = []
            for _ in range(5):
                line = f.readline()
                if not line:
                    break
                sample_lines.append(line.rstrip("\n").rstrip("\r"))
    except Exception:
        return ",", False
    candidates = [",", ";", "\t", "|"]
    counts = {d: 0 for d in candidates}
    for line in sample_lines:
        if not line.strip():
            continue
        for d in candidates:
            counts[d] += line.count(d)
    best = max(candidates, key=lambda d: counts[d])
    if counts[best] == 0:
        return ",", False
    # 仅当最佳分隔符与默认逗号不同、且确有出现时，视为自动探测
    detected = best != ","
    return best, detected


def _read_csv(filepath: str, timestamp: str, encoding: str = None, sep: str = None) -> StatFileResult:
    """读入 CSV 文件，使用 pd.read_csv。

    支持：
    - 编码自动探测（UTF-16 经 BOM 判定；否则回退 utf-8-sig / utf-8 / gbk / latin-1）
    - 分隔符自动探测（逗号 / 分号 / 制表符 / 竖线）；也可经 sep 显式指定
    """
    warnings_list = []
    csv_metadata: dict[str, Any] = {}
    
    # 尝试检测编码
    if encoding is None:
        # 先用 BOM 判定 UTF-16（UTF-16 文件必带 BOM，避免与 GBK 误判冲突）
        enc_detected = "utf-8"
        try:
            with open(filepath, "rb") as _f:
                _head = _f.read(2)
            if _head == b"\xff\xfe":
                enc_detected = "utf-16-le"
            elif _head == b"\xfe\xff":
                enc_detected = "utf-16-be"
            else:
                # 无 BOM：按常见编码回退（utf-8 优先，GBK 在 utf-16 之前以免误判）
                for enc in ["utf-8-sig", "utf-8", "gbk", "gb2312", "latin-1"]:
                    try:
                        df = pd.read_csv(filepath, encoding=enc, nrows=5)
                        enc_detected = enc
                        break
                    except (UnicodeDecodeError, UnicodeError):
                        continue
        except (OSError, IOError):
            enc_detected = "utf-8"
        encoding = enc_detected

    # 分隔符自动探测（仅在未显式指定时）
    auto_detected = False
    if sep is None:
        sep, auto_detected = _detect_delimiter(filepath, encoding)
    
    # Read full file with detected/specified encoding
    df = pd.read_csv(filepath, encoding=encoding, sep=sep)
    csv_metadata["encoding"] = encoding
    csv_metadata["separator_guess"] = sep
    if auto_detected:
        warnings_list.append(_bilingual(
            f"CSV 分隔符非逗号，已自动探测为 '{sep}' | CSV delimiter auto-detected as '{sep}' (non-comma)",
            f"CSV 分隔符非逗号，已自动探测为 '{sep}'",
        ))
    
    if df.empty:
        warnings_list.append(_bilingual("CSV file parsed result is empty", "CSV 文件解析结果为空"))

    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        column_report[col] = ColumnInfo(
            source_type=_get_source_type(df[col]),
            pandas_dtype=str(df[col].dtype),
            original_label=None,
            has_value_labels=False,
            n_missing=int(df[col].isnull().sum()),
            missing_are_special=False,
            precision_warning=False,
            format_string=None,
            display_width=None,
            storage_width=None,
            measure_level=None,
            alignment=None,
            original_type=None,
        )
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                column_report[col]["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")

    return {
        "dataframe": df,
        "metadata": {
            "file_format": "csv",
            "collected_at": timestamp,
            "row_count": df.shape[0],
            "column_count": df.shape[1],
            "total_missing_pct": _calc_missing_pct(df),
            "variable_labels": {},
            "value_labels": {},
            "special_missing": {},
            "csv_metadata": csv_metadata,
        },
        "warnings": warnings_list,
        "column_report": column_report,
    }
