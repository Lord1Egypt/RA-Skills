"""
reader_epinfo.py - EpiInfo 项目文件读入（.prj / Project.xml）
EpiInfo 是 CDC 开发的流行病学调查软件，项目文件为 XML 格式

支持结构：
  Project → Form → Page → Field（字段定义）
  数据文件：CSV 或 Access（通过字段名关联）
"""

from __future__ import annotations
import os
import csv
from typing import Any, Optional
from datetime import datetime

import pandas as pd
import xml.etree.ElementTree as ET

from .reader_core import (ColumnInfo, BaseMeta, StatFileResult, _bilingual,
                           _calc_missing_pct, _get_source_type, _build_column_report, _build_metadata)

# ═══════════════════════════════════════════════════════════════════════════════
# EpiInfo 字段类型 → pandas dtype 映射
# ═══════════════════════════════════════════════════════════════════════════════

EPIINFO_DTYPE_MAP = {
    "number": "float64",
    "text": "object",
    "date": "datetime64[ns]",
    "time": "object",
    "datetime": "datetime64[ns]",
    "boolean": "bool",
    "yesno": "category",
    "phonenumber": "object",
    "guid": "object",
    "object": "object",
}

EPIINFO_TYPE_LABELS = {
    "number": "数值",
    "text": "文本",
    "date": "日期",
    "time": "时间",
    "datetime": "日期时间",
    "boolean": "布尔",
    "yesno": "是/否",
    "phonenumber": "电话",
    "guid": "GUID",
    "object": "对象",
}


def _find_data_file(prj_path: str, field_names: list[str]) -> tuple[str, str] | tuple[None, None]:
    """Find data file associated with the project (CSV or Access).
    
    Returns (file_path, file_type) or (None, None).
    """
    base_dir = os.path.dirname(prj_path)
    
    # Priority 1: Look for CSV with same name as project
    base_name = os.path.splitext(os.path.basename(prj_path))[0]
    for ext in [".csv", ".txt", ".tsv"]:
        candidate = os.path.join(base_dir, base_name + ext)
        if os.path.exists(candidate):
            return candidate, "csv"
    
    # Priority 2: Look for any CSV in the same directory
    for f in os.listdir(base_dir):
        if f.endswith(".csv") and f != os.path.basename(prj_path):
            candidate = os.path.join(base_dir, f)
            # Check if it has matching headers
            try:
                with open(candidate, 'r', encoding='utf-8', errors='replace') as csvfile:
                    reader = csv.reader(csvfile)
                    header = next(reader, [])
                    if header and any(fn in header for fn in field_names if fn):
                        return candidate, "csv"
            except Exception:
                pass
    
    # Priority 3: Access database
    for ext in [".mdb", ".accdb"]:
        candidate = os.path.join(base_dir, base_name + ext)
        if os.path.exists(candidate):
            return candidate, "access"
    
    return None, None


def _parse_epinfo_xml(prj_path: str) -> dict:
    """Parse EpiInfo XML project file and extract form/field definitions."""
    tree = ET.parse(prj_path)
    root = tree.getroot()
    
    project_info = {
        "project_name": None,
        "project_description": None,
        "forms": [],
    }
    
    # Handle EpiInfo 7 namespace
    ns = {}
    if root.tag.startswith("{"):
        uri = root.tag.split("}")[0].strip("{")
        ns = {"e": uri}
    
    # Project attributes
    project_info["project_name"] = root.get("name") or root.get("Name")
    desc_elem = root.find(".//description", ns) or root.find(".//Description", ns)
    if desc_elem is not None and desc_elem.text:
        project_info["project_description"] = desc_elem.text
    
    # Parse forms
    forms = root.findall(".//form", ns) or root.findall(".//Form", ns)
    if not forms:
        forms = root.findall(".//view", ns) or root.findall(".//View", ns)
    
    for form in forms:
        form_info = {
            "name": form.get("name") or form.get("Name", "UnknownForm"),
            "pages": [],
        }
        
        pages = form.findall(".//page", ns) or form.findall(".//Page", ns)
        if not pages:
            pages = [form]  # Single-page form
        
        for page in pages:
            page_info = {
                "name": page.get("name") or page.get("Name", "Page1"),
                "fields": [],
            }
            
            fields = page.findall(".//field", ns) or page.findall(".//Field", ns)
            if not fields:
                fields = page.findall(".//control", ns) or page.findall(".//Control", ns)
            
            for field in fields:
                field_type_raw = (field.get("type") or field.get("Type") or "text").lower().replace(" ", "")
                # Normalize type names
                if field_type_raw in ("number", "integer", "double", "float", "decimal"):
                    field_type = "number"
                elif field_type_raw in ("text", "string", "memo", "varchar"):
                    field_type = "text"
                elif field_type_raw in ("date",):
                    field_type = "date"
                elif field_type_raw in ("time",):
                    field_type = "time"
                elif field_type_raw in ("datetime", "date/time"):
                    field_type = "datetime"
                elif field_type_raw in ("boolean", "bool"):
                    field_type = "boolean"
                elif field_type_raw in ("yesno", "yes/no"):
                    field_type = "yesno"
                elif field_type_raw in ("phone", "phonenumber"):
                    field_type = "phonenumber"
                elif field_type_raw in ("guid", "uniqueid"):
                    field_type = "guid"
                else:
                    field_type = "text"  # Default
                
                field_info = {
                    "name": field.get("name") or field.get("Name") or field.get("id") or field.get("ID"),
                    "label": field.get("label") or field.get("Label") or field.get("text") or field.get("Text"),
                    "type": field_type,
                    "original_type": field_type_raw,
                    "required": (field.get("required") or field.get("Required", "false")).lower() == "true",
                    "read_only": (field.get("readonly") or field.get("ReadOnly", "false")).lower() == "true",
                }
                
                # Parse code/value labels (optional)
                codes = field.findall(".//code", ns) or field.findall(".//Code", ns)
                if not codes:
                    codes = field.findall(".//option", ns) or field.findall(".//Option", ns)
                val_labels = {}
                for code in codes:
                    val = code.get("value") or code.get("Value") or code.get("code") or code.get("Code")
                    lbl = code.get("label") or code.get("Label") or code.get("text") or code.get("Text")
                    if val is not None and lbl:
                        try:
                            val_labels[int(val)] = lbl
                        except (ValueError, TypeError):
                            val_labels[val] = lbl
                if val_labels:
                    field_info["value_labels"] = val_labels
                
                if field_info["name"]:
                    page_info["fields"].append(field_info)
            
            form_info["pages"].append(page_info)
        
        project_info["forms"].append(form_info)
    
    return project_info


def _read_epinfo(prj_path: str, timestamp: str, encoding: str | None = None,
                 data_file: str | None = None) -> StatFileResult:
    """Read EpiInfo project file (.prj / .xml)."""
    warnings_list = []
    
    # Parse XML for form/field definitions
    project_info = _parse_epinfo_xml(prj_path)
    
    # Collect all fields across pages/forms
    all_fields = []
    field_names = []
    for form in project_info["forms"]:
        for page in form["pages"]:
            all_fields.extend(page["fields"])
            for field in page["fields"]:
                if field["name"]:
                    field_names.append(field["name"])
    
    if not all_fields:
        warnings_list.append(_bilingual("EpiInfo project file contains no field definitions, please check file format", "EpiInfo 项目文件不包含任何字段定义，请检查文件格式"))
    
    # Find data file
    actual_data_file = data_file
    data_file_type = "csv"
    if actual_data_file is None:
        actual_data_file, data_file_type = _find_data_file(prj_path, field_names)
    
    if actual_data_file is None:
        warnings_list.append(_bilingual(
            "No associated data file found for EpiInfo. Please specify data_file parameter, or ensure a CSV file with the same name as the project exists in the project directory.",
            "未找到 EpiInfo 关联的数据文件。请指定 data_file 参数，或确保项目目录下有与项目同名的 .csv 文件。"
        ))
    
    # Read data
    df = pd.DataFrame()
    if actual_data_file:
        try:
            if data_file_type == "csv":
                read_kwargs = {"encoding": encoding} if encoding else {}
                df = pd.read_csv(actual_data_file, **read_kwargs)
            else:
                # Access - use R bridge or pyodbc
                warnings_list.append(_bilingual("Access database import is not supported, please use CSV export format", "Access 数据库读入暂不支持，请使用 CSV 导出格式"))
        except Exception as e:
            warnings_list.append(_bilingual(f"Failed to read data file: {e}", f"读入数据文件失败: {e}"))
    
    # Build metadata
    variable_labels = {}
    original_variable_types = {}
    value_labels = {}
    
    for field in all_fields:
        name = field.get("name", "")
        if not name:
            continue
        if field.get("label"):
            variable_labels[name] = field["label"]
        original_variable_types[name] = field.get("original_type", field.get("type", "text"))
        if field.get("value_labels"):
            value_labels[name] = field["value_labels"]
    
    # Format all field info as notes
    notes = []
    if project_info["project_description"]:
        notes.append(f"项目描述: {project_info['project_description'][:200]}")
    
    form_summaries = []
    for form in project_info["forms"]:
        page_count = len(form["pages"])
        field_count = sum(len(p["fields"]) for p in form["pages"])
        form_summaries.append(f"{form['name']}({page_count} 页, {field_count} 字段)")
    if form_summaries:
        notes.append(f"表单结构: {'; '.join(form_summaries)}")
    
    # Column-level report
    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        matching_field = None
        for field in all_fields:
            if field["name"] == col:
                matching_field = field
                break
        
        col_info: ColumnInfo = {
            "source_type": _get_source_type(df[col]),
            "pandas_dtype": str(df[col].dtype),
            "original_label": variable_labels.get(col) if matching_field else None,
            "has_value_labels": col in value_labels if matching_field else False,
            "n_missing": int(df[col].isnull().sum()),
            "missing_are_special": False,
            "precision_warning": False,
            "format_string": matching_field.get("original_type") if matching_field else None,
            "display_width": None,
            "storage_width": None,
            "measure_level": None,
            "alignment": None,
            "original_type": original_variable_types.get(col) if matching_field else None,
            "formula": None,
            "column_property": None,
        }
        
        if pd.api.types.is_numeric_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                col_info["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")
        
        column_report[col] = col_info
    
    epinfo_metadata = {
        "project_name": project_info["project_name"],
        "project_description": project_info["project_description"],
        "forms": [{"name": f["name"], "pages": len(f["pages"])} for f in project_info["forms"]],
        "data_file": actual_data_file,
        "data_file_type": data_file_type,
    }
    
    return {
        "dataframe": df,
        "metadata": _build_metadata({
            "variable_labels": variable_labels,
            "value_labels": value_labels,
            "original_variable_types": original_variable_types,
            "notes": notes,
            "special_missing": {},
        }, "epinfo", extra={
            "collected_at": timestamp,
            "row_count": df.shape[0],
            "column_count": df.shape[1],
            "total_missing_pct": _calc_missing_pct(df),
        }, format_meta={"epinfo_metadata": epinfo_metadata}),
        "warnings": warnings_list,
        "column_report": column_report,
    }
