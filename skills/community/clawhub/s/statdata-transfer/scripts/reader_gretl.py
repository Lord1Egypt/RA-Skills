"""
reader_gretl.py - Gretl .gdt (Gretl Data) 文件读入
Gretl 计量经济学软件原生数据格式

支持：
  .gdt 纯 XML 格式（默认）
  .gdt gzip 压缩格式（自动检测）
  .gdtb 纯二进制格式（暂不支持，需提示导出）
"""

from __future__ import annotations
import os
import gzip
from typing import Any, Optional
from datetime import datetime

import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET

from .reader_core import (ColumnInfo, GretlMeta, StatFileResult, _bilingual,
                           _calc_missing_pct, _get_source_type, _build_column_report, _build_metadata)


def _parse_gdt_xml(tree: ET.ElementTree) -> dict:
    """Parse GDT XML tree and extract metadata + data."""
    root = tree.getroot()
    
    # Root-level metadata
    info = {
        "name": root.get("name") or root.get("Name", ""),
        "frequency": root.get("frequency") or root.get("Frequency"),
        "type": root.get("type") or root.get("Type", "cross-section"),
        "n_obs": int(root.get("n") or root.get("N", 0)),
        "startobs": root.get("startobs") or root.get("Startobs"),
        "endobs": root.get("endobs") or root.get("Endobs"),
        "description": "",
        "source": "",
        "variables": [],
        "value_labels": {},
        "data": [],
    }
    
    # Description
    desc = root.find(".//description") or root.find(".//Description")
    if desc is not None and desc.text:
        info["description"] = desc.text
    
    if root.get("source"):
        info["source"] = root.get("source")
    
    # Variables section
    variables = root.find("variables") or root.find("Variables")
    if variables is not None:
        count = int(variables.get("count") or variables.get("Count", 0))
        vars_list = variables.findall("variable") or variables.findall("Variable")
        for var in vars_list:
            var_info = {
                "name": var.get("name") or var.get("Name", ""),
                "label": var.get("label") or var.get("Label", ""),
                "displayname": var.get("displayname") or var.get("Displayname", ""),
                "discrete": var.get("discrete", "0") == "1",
                "coded": var.get("coded", "0") == "1",
                "transform": var.get("transform"),
                "lag": var.get("lag"),
                "compact_method": var.get("compact-method"),
                "role": var.get("role"),
                "missing_value": var.get("missing-value"),
            }
            info["variables"].append(var_info)
    
    # String tables (value labels)
    string_tables = root.find("string-tables") or root.find("StringTables")
    if string_tables is not None:
        for vt in string_tables.findall("valstrings") or string_tables.findall("ValStrings"):
            owner = vt.get("owner") or vt.get("Owner")
            if owner:
                labels = {}
                for pair in vt.findall("pair") or vt.findall("Pair"):
                    val = pair.get("value") or pair.get("Value")
                    lbl = pair.get("label") or pair.get("Label")
                    if val and lbl:
                        try:
                            labels[int(val)] = lbl
                        except ValueError:
                            labels[val] = lbl
                if labels:
                    info["value_labels"][owner] = labels
    
    # Observations
    observations = root.find("observations") or root.find("Observations")
    if observations is not None:
        for obs in observations.findall("obs") or observations.findall("Obs"):
            # Each obs element contains space-separated values
            values = obs.text.split() if obs.text else []
            info["data"].append([float(v) if v != "nan" and v != "NA" else np.nan for v in values])
    
    return info


def _read_gdt(filepath: str, timestamp: str) -> StatFileResult:
    """Read Gretl .gdt file (XML or gzip-compressed XML)."""
    warnings_list = []
    
    # Detect if gzipped
    with open(filepath, "rb") as f:
        magic = f.read(2)
    
    try:
        if magic == b"\x1f\x8b":
            with gzip.open(filepath, "rb") as f:
                tree = ET.parse(f)
        else:
            tree = ET.parse(filepath)
        
        info = _parse_gdt_xml(tree)
    except ET.ParseError as e:
        raise RuntimeError(
            f"Gretl GDT 文件解析失败: {e}\n"
            f"如果这是 .gdtb 二进制格式，请先用 Gretl 导出为 XML 格式:\n"
            f"  File → Save Data → 选择 'GDT (XML)' 格式"
        )
    
    # Build DataFrame
    col_names = [v["name"] for v in info["variables"]]
    n_vars = len(col_names)
    
    if info["data"]:
        arr = np.array(info["data"], dtype=float)
        if arr.shape[0] == 0:
            df = pd.DataFrame(columns=col_names)
        elif arr.shape[1] != n_vars:
            warnings_list.append(_bilingual(
                f"Data column count ({arr.shape[1]}) does not match variable definition count ({n_vars}), some data may be lost",
                f"数据列数 ({arr.shape[1]}) 与变量定义数 ({n_vars}) 不匹配，部分数据可能丢失"
            ))
            n_vars = min(arr.shape[1], n_vars)
            col_names = col_names[:n_vars]
            arr = arr[:, :n_vars]
            df = pd.DataFrame(arr, columns=col_names)
        else:
            df = pd.DataFrame(arr, columns=col_names)
    else:
        df = pd.DataFrame(columns=col_names)
    
    # Apply discrete/coded → category
    for var_info in info["variables"]:
        name = var_info["name"]
        if name in df.columns:
            if var_info["discrete"] or var_info["coded"]:
                if name in info["value_labels"]:
                    labels = info["value_labels"][name]
                    # Map numeric codes to labels
                    df[name] = df[name].map(labels).fillna("").astype("category")
                else:
                    df[name] = df[name].astype("category")
    
    # Build metadata
    variable_labels = {}
    original_variable_types = {}
    
    for var_info in info["variables"]:
        name = var_info["name"]
        if var_info["label"]:
            variable_labels[name] = var_info["label"]
        
        # Map type
        if var_info["discrete"] or var_info["coded"]:
            original_variable_types[name] = "discrete"
        else:
            original_variable_types[name] = "continuous"
    
    # Notes
    notes = []
    if info["name"]:
        notes.append(f"数据集名: {info['name']}")
    if info["description"]:
        notes.append(f"描述: {info['description'][:200]}")
    if info["frequency"]:
        notes.append(f"频率: {info['frequency']}")
    if info["startobs"] or info["endobs"]:
        notes.append(f"范围: {info['startobs']} - {info['endobs']}")
    if info["source"]:
        notes.append(f"来源: {info['source'][:200]}")
    
    # Column report
    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        var_info = None
        for vi in info["variables"]:
            if vi["name"] == col:
                var_info = vi
                break
        
        has_vl = col in info["value_labels"]
        
        col_info: ColumnInfo = {
            "source_type": _get_source_type(df[col]),
            "pandas_dtype": str(df[col].dtype),
            "original_label": variable_labels.get(col) if var_info else None,
            "has_value_labels": has_vl,
            "n_missing": int(df[col].isnull().sum()),
            "missing_are_special": var_info["missing_value"] is not None if var_info else False,
            "precision_warning": False,
            "format_string": original_variable_types.get(col) if var_info else None,
            "display_width": None,
            "storage_width": None,
            "measure_level": "nominal" if (var_info and var_info["discrete"]) else ("ordinal" if var_info and var_info["coded"] else None),
            "alignment": None,
            "original_type": original_variable_types.get(col) if var_info else None,
            "formula": var_info.get("transform"),
            "column_property": {"missing_value": var_info["missing_value"]} if var_info else None,
        }
        
        if pd.api.types.is_numeric_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                col_info["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")
        
        column_report[col] = col_info
    
    gretl_metadata = {
        "name": info["name"],
        "frequency": info["frequency"],
        "type": info["type"],
        "startobs": info["startobs"],
        "endobs": info["endobs"],
        "n_obs": info["n_obs"],
        "source": info["source"],
    }
    
    return {
        "dataframe": df,
        "metadata": _build_metadata({
            "variable_labels": variable_labels,
            "value_labels": info["value_labels"],
            "original_variable_types": original_variable_types,
            "notes": notes,
            "special_missing": {},
        }, "gretl", extra={
            "collected_at": timestamp,
            "row_count": df.shape[0],
            "column_count": df.shape[1],
            "total_missing_pct": _calc_missing_pct(df),
        }, format_meta={"gretl_metadata": gretl_metadata}),
        "warnings": warnings_list,
        "column_report": column_report,
    }
