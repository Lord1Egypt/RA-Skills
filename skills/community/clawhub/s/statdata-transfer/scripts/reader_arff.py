"""
reader_arff.py - Weka ARFF (Attribute-Relation File Format) 读入
Weka 机器学习平台原生数据格式

支持：
  @relation / @attribute NUMERIC|INTEGER|REAL|STRING|DATE|NOMINAL|RELATIONAL
  @data 实例行（含稀疏格式 {index value} 和缺失值 ?）
  行内注释 %
"""

from __future__ import annotations
import os
import re
from typing import Any

import pandas as pd
import numpy as np

from .reader_core import (ColumnInfo, ArffMeta, StatFileResult, _bilingual,
                           _calc_missing_pct, _get_source_type, _build_column_report, _build_metadata)


# ARFF 数据类型 → pandas 类型映射
ARFF_DTYPE_MAP = {
    "numeric": "float64",
    "integer": "int64",
    "real": "float64",
    "string": "object",
    "date": "datetime64[ns]",
}


def _parse_arff_attribute(line: str):
    """Parse @attribute line, return (name, type_str, type_info)."""
    line = line.strip()
    if not line.lower().startswith("@attribute"):
        return None
    
    m = re.match(r'@attribute\s+(\S+)\s+(.*)', line, re.I)
    if not m:
        return None
    
    name = m.group(1).strip("'\"")
    # Keep original case for nominal values — only use lowercase for type detection
    type_raw = m.group(2).strip()
    type_str = type_raw.lower()
    
    if type_str.startswith("{") and type_str.endswith("}"):
        # Nominal: {val1,val2,...} — preserve original case for values
        vals = [v.strip().strip("'\"") for v in type_raw[1:-1].split(",")]
        return name, "nominal", {"values": vals}
    elif type_str.startswith("date"):
        # Date [format]
        fmt_match = re.search(r'date\s+"?([^"]+)"?', line, re.I)
        fmt = fmt_match.group(1) if fmt_match else None
        return name, "date", {"format": fmt}
    elif type_str.startswith("relational"):
        return name, "relational", {}
    else:
        return name, type_str, {}


def _read_arff(filepath: str, timestamp: str, encoding: str = "utf-8") -> StatFileResult:
    """Read Weka ARFF file."""
    warnings_list = []
    relation_name = "unknown"
    attributes = []  # [(name, type, info), ...]
    data_lines = []
    in_data = False
    
    with open(filepath, "r", encoding=encoding, errors="replace") as f:
        for line in f:
            stripped = line.strip()
            
            # Skip comments
            if stripped.startswith("%"):
                continue
            
            # Relation
            if stripped.lower().startswith("@relation"):
                rel_part = stripped[len("@relation"):].strip()
                relation_name = rel_part.strip("'\"")
                continue
            
            # Attribute
            if stripped.lower().startswith("@attribute"):
                attr = _parse_arff_attribute(stripped)
                if attr:
                    attributes.append(attr)
                continue
            
            # Data start
            if stripped.lower().startswith("@data"):
                in_data = True
                continue
            
            # Data content
            if in_data and stripped:
                # Sparse format: {1 X, 3 Y, ...}
                if stripped.startswith("{"):
                    sparse = {}
                    for entry in stripped[1:-1].split(","):
                        parts = entry.strip().split(None, 1)
                        if len(parts) == 2:
                            idx = int(parts[0])
                            val = parts[1].strip("'\"")
                            sparse[idx] = val
                    data_lines.append(sparse)
                else:
                    values = []
                    in_quote = False
                    current = ""
                    for ch in stripped:
                        if ch == "'" and not in_quote:
                            in_quote = True
                        elif ch == "'" and in_quote:
                            in_quote = False
                        elif ch == "," and not in_quote:
                            values.append(current.strip())
                            current = ""
                        else:
                            current += ch
                    values.append(current.strip())
                    data_lines.append(values)
    
    if not data_lines:
        warnings_list.append(_bilingual("ARFF file does not contain @data section, only metadata can be read", "ARFF 文件不包含 @data 数据区，仅能读取元数据"))
    
    # Build DataFrame
    n_cols = len(attributes)
    if n_cols == 0:
        warnings_list.append(_bilingual("ARFF file has no @attribute definitions", "ARFF 文件无 @attribute 定义"))
    
    # Initialize data matrix
    data = np.full((len(data_lines), n_cols), None, dtype=object) if data_lines else np.empty((0, n_cols), dtype=object)
    
    for i, row in enumerate(data_lines):
        if isinstance(row, dict):
            # Sparse
            for j, val in row.items():
                if j < n_cols:
                    data[i, j] = val if val != "?" else None
        else:
            for j, val in enumerate(row):
                if j < n_cols and val != "?":
                    data[i, j] = val
    
    # Column names and types
    col_names = [attr[0] for attr in attributes] if attributes else [f"V{i}" for i in range(n_cols)]
    
    # Build DataFrame with proper dtypes
    df_dict = {}
    for j, (name, type_str, type_info) in enumerate(attributes):
        col_data = data[:, j] if len(data_lines) > 0 else []
        
        if type_str in ("numeric", "integer", "real"):
            df_dict[name] = pd.to_numeric(col_data, errors="coerce")
        elif type_str == "date":
            fmt = type_info.get("format")
            if fmt:
                df_dict[name] = pd.to_datetime(col_data, format=fmt, errors="coerce")
            else:
                df_dict[name] = pd.to_datetime(col_data, errors="coerce")
        elif type_str == "nominal":
            cats = type_info.get("values", [])
            if cats:
                df_dict[name] = pd.Categorical(col_data, categories=cats)
            else:
                df_dict[name] = pd.Series(col_data, dtype="category")
        else:
            df_dict[name] = col_data
    
    if df_dict:
        df = pd.DataFrame(df_dict)
    else:
        df = pd.DataFrame()
    
    # Build metadata
    variable_labels = {}
    original_variable_types = {}
    value_labels = {}
    
    for name, type_str, type_info in attributes:
        original_variable_types[name] = type_str
        if type_str == "nominal" and type_info.get("values"):
            value_labels[name] = {i: v for i, v in enumerate(type_info["values"])}
            variable_labels[name] = f"名义变量: {', '.join(type_info['values'][:5])}"
    
    notes = [
        f"关系名: {relation_name}",
        f"实例数: {len(data_lines)}, 属性数: {n_cols}",
    ]
    
    # Column report
    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        attr_info = None
        for name, type_str, type_info in attributes:
            if name == col:
                attr_info = (type_str, type_info)
                break
        
        type_str = attr_info[0] if attr_info else "unknown"
        has_vl = col in value_labels
        
        col_info: ColumnInfo = {
            "source_type": _get_source_type(df[col]),
            "pandas_dtype": str(df[col].dtype),
            "original_label": variable_labels.get(col),
            "has_value_labels": has_vl,
            "n_missing": int(df[col].isnull().sum()),
            "missing_are_special": False,
            "precision_warning": False,
            "format_string": type_str,
            "display_width": None,
            "storage_width": None,
            "measure_level": None,
            "alignment": None,
            "original_type": original_variable_types.get(col, "unknown"),
            "formula": None,
            "column_property": None,
        }
        
        if pd.api.types.is_numeric_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                col_info["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")
        
        column_report[col] = col_info
    
    arff_metadata = {
        "relation_name": relation_name,
        "attributes": [{"name": a[0], "type": a[1]} for a in attributes],
    }
    
    return {
        "dataframe": df,
        "metadata": _build_metadata({
            "variable_labels": variable_labels,
            "value_labels": value_labels,
            "original_variable_types": original_variable_types,
            "notes": notes,
            "special_missing": {},
        }, "arff", extra={
            "collected_at": timestamp,
            "row_count": df.shape[0],
            "column_count": df.shape[1],
            "total_missing_pct": _calc_missing_pct(df),
        }, format_meta={"arff_metadata": arff_metadata}),
        "warnings": warnings_list,
        "column_report": column_report,
    }
