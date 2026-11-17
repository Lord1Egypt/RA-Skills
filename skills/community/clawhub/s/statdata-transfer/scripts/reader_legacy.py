"""
reader_legacy.py - 老牌 / 专有统计软件数据格式读入
====================================================

本模块覆盖 statdata-transfer 在 Stat/Transfer 9 与 statsoft-cli 对照中暴露的
高/中优先格式缺口。按实现可靠度分两类：

【真实现 — 纯 Python / 系统驱动可读】
  .dbf      dBASE III+/IV / Visual FoxPro   (dbfread 读 + dbf 写, 纯 Python, 支持中文 codepage)
  .mdb/.accdb MS Access                      (pyodbc + 系统自带 Microsoft Access Driver)
  .wdx      Mathematica "Wolfram Data Exchange" XML  (lxml 解析, best-effort)
  .opju/.oggu Origin 项目 (zip+XML)          (zipfile 解包 + XML 解析, best-effort)

【占位降级 — 无现成解析库 / 沙盒无样本，给出清晰导出指引】
  .cpt      SAS CPORT          (SAS PROC CPORT 专有二进制, 需 SAS 导出 XPORT/.sas7bdat)
  .sta      Statistica         (专有二进制, 需导出 .sav/.csv)
  .in7      OxMetrics          (专有二进制, 需导出 .csv/.dta)
  .sys/.syd SYSTAT             (专有二进制, 需导出 .csv/.sav)
  .db/.px   Paradox            (Borland 老库, 需导出 .dbf/.csv)
  .lpw      LIMDEP/NLOGIT      (专有工作文件, 需导出 .csv)
  .ncss     NCSS               (专有数据包, 需导出 .csv)

所有 reader 返回 reader_core.StatFileResult 契约：
  { "dataframe", "metadata", "warnings", "column_report" }
"""

from __future__ import annotations

import os
import zipfile
import io
from typing import Any, Optional
from datetime import datetime

import pandas as pd
import numpy as np

from .reader_core import (
    ColumnInfo,
    StatFileResult,
    _bilingual,
    _calc_missing_pct,
    _get_source_type,
    _build_metadata,
)


# ============================================================
# 公共辅助
# ============================================================

def _legacy_column_report(df: pd.DataFrame, variable_labels: Optional[dict] = None) -> dict[str, ColumnInfo]:
    """构造统一的 column_report（复用 reader_gretl 的字段结构）。"""
    variable_labels = variable_labels or {}
    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        col_info: ColumnInfo = {
            "source_type": _get_source_type(df[col]),
            "pandas_dtype": str(df[col].dtype),
            "original_label": variable_labels.get(col),
            "has_value_labels": False,
            "n_missing": int(df[col].isnull().sum()),
            "missing_are_special": False,
            "precision_warning": False,
            "format_string": None,
            "display_width": None,
            "storage_width": None,
            "measure_level": None,
            "alignment": None,
            "original_type": None,
            "formula": None,
            "column_property": None,
        }
        if pd.api.types.is_numeric_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                col_info["precision_warning"] = True
        column_report[col] = col_info
    return column_report


def _make_unsupported(software: str, suggestion_zh: str, suggestion_en: str):
    """生成「占位降级」reader：识别扩展名但给出清晰导出指引，不虚假声称可解析。"""

    def _handler(filepath: str, timestamp: str) -> StatFileResult:
        ext = os.path.splitext(filepath)[1].lower()
        raise RuntimeError(
            _bilingual(
                f"Direct reading of {software} proprietary format {ext} is not yet supported.\n"
                f"Please export the data from {software} to a common format ({suggestion_en}) first, "
                f"then convert with this skill.",
                f"暂不支持直接读取 {software} 专有格式 {ext}。\n"
                f"请先用 {software} 将该数据导出为通用格式（{suggestion_zh}），"
                f"再用本技能转换。",
            )
        )

    return _handler


# ============================================================
# dBASE / FoxPro  (.dbf)  —— 真实现（读 + 写）
# ============================================================

def _read_dbf(filepath: str, timestamp: str) -> StatFileResult:
    """读取 dBASE III+/IV / Visual FoxPro .dbf 文件。"""
    import dbfread

    warnings_list: list[str] = []
    try:
        table = dbfread.DBF(filepath, load=True, encoding="utf-8")
        records = list(table.records)
        df = pd.DataFrame(records, columns=table.field_names)
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(
            _bilingual(
                f"Failed to read dBASE (.dbf): {e}",
                f"dBASE (.dbf) 文件读取失败: {e}\n"
                f"请确认文件是有效的 dBASE/FoxPro 数据文件（非带备注的 .dbt 缺失或损坏）。",
            )
        )

    variable_labels: dict[str, str] = {}
    # dbfread 不携带变量标签（dBASE 无标签概念），column_report 仅基础信息
    column_report = _legacy_column_report(df, variable_labels)

    return {
        "dataframe": df,
        "metadata": _build_metadata(
            {
                "variable_labels": variable_labels,
                "value_labels": {},
                "special_missing": {},
                "notes": [f"dBASE/FoxPro 文件: {os.path.basename(filepath)}"],
            },
            "dbf",
            extra={
                "collected_at": timestamp,
                "row_count": df.shape[0],
                "column_count": df.shape[1],
                "total_missing_pct": _calc_missing_pct(df),
            },
            format_meta={"dbf_field_count": df.shape[1]},
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }


def _to_dbf_value(v: Any, dtype) -> Any:
    if pd.isna(v):
        return None
    if pd.api.types.is_bool_dtype(dtype):
        return bool(v)
    if pd.api.types.is_integer_dtype(dtype):
        return int(v)
    if pd.api.types.is_float_dtype(dtype):
        return float(v)
    return str(v)


def _write_dbf(df: pd.DataFrame, filepath: str, metadata: Optional[dict] = None, **kwargs: Any) -> list[str]:
    """将 DataFrame 写入 dBASE .dbf（纯 Python，支持中文 codepage='utf8'）。"""
    import dbf

    variable_labels = (metadata or {}).get("variable_labels", {}) or {}

    specs: list[str] = []
    for col in df.columns:
        dtype = df[col].dtype
        label = variable_labels.get(col, "")
        safe_name = str(col)[:10]  # dBASE 字段名最长 10 字符
        if pd.api.types.is_bool_dtype(dtype):
            specs.append(f"{safe_name} L")
        elif pd.api.types.is_integer_dtype(dtype):
            specs.append(f"{safe_name} N(19,0)")
        elif pd.api.types.is_float_dtype(dtype):
            specs.append(f"{safe_name} N(20,6)")
        else:
            specs.append(f"{safe_name} C(254)")
    spec_str = ";".join(specs)

    table = dbf.Table(filepath, spec_str, codepage="utf8")
    table.open(dbf.READ_WRITE)
    try:
        for _, row in df.iterrows():
            rec = tuple(_to_dbf_value(v, df[col].dtype) for col, v in row.items())
            table.append(rec)
    finally:
        table.close()

    warnings_list = []
    if variable_labels:
        warnings_list.append(
            _bilingual(
                "dBASE has no variable-label concept; label metadata was dropped (data columns only).",
                "dBASE 格式不含变量标签概念，标签信息已丢弃（仅数据列写出）。",
            )
        )
    # dBASE 字段名仅支持大写字母/数字/下划线，且最长 10 字符
    lower_cols = [str(c) for c in df.columns if str(c) != str(c).upper()[:10]]
    if lower_cols:
        warnings_list.append(
            _bilingual(
                f"dBASE field names are upper-cased and truncated to 10 chars; "
                f"affected columns: {', '.join(lower_cols)}.",
                f"dBASE 字段名仅支持大写且最长 10 字符，以下列名已转换: {', '.join(lower_cols)}。",
            )
        )
    return warnings_list


# ============================================================
# MS Access  (.mdb / .accdb)  —— 真实现（pyodbc + 系统驱动）
# ============================================================

def _read_access(filepath: str, timestamp: str, *, table_name: str | None = None) -> StatFileResult:
    """读取 MS Access .mdb/.accdb（pyodbc + Microsoft Access Driver）。

    多表数据库默认返回第一个用户表；可通过 ``table_name='订单'`` 指定。
    """
    import pyodbc

    conn_str = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;" % filepath
    try:
        conn = pyodbc.connect(conn_str)
    except pyodbc.Error as e:  # noqa: BLE001
        raise RuntimeError(
            _bilingual(
                f"Cannot open Access database: {e}\n"
                f"Confirm the file exists and the Microsoft Access Driver is installed.",
                f"无法打开 Access 数据库: {e}\n"
                f"请确认：①文件存在且未损坏；②系统已安装 Microsoft Access Driver "
                f"(Microsoft Access Database Engine)。",
            )
        )

    warnings_list: list[str] = []
    try:
        cur = conn.cursor()
        tables = [
            r.table_name
            for r in cur.tables(tableType="TABLE")
            if not r.table_name.startswith("MSys")
        ]
        if not tables:
            raise RuntimeError(
                _bilingual("No user tables found in Access database.", "Access 数据库未找到用户表。")
            )

        # 选择目标表：用户指定 > 默认首表
        specified = (table_name or "").strip()
        if specified:
            if specified not in tables:
                raise ValueError(_bilingual(
                    f"Table '{specified}' not in database table list ({', '.join(tables)})",
                    f"表 '{specified}' 不在数据库表清单 ({', '.join(tables)})"))
            target = specified
        else:
            target = tables[0]

        df = pd.read_sql(f"SELECT * FROM [{target}]", conn)

        if len(tables) > 1 and not specified:
            warnings_list.append(
                _bilingual(
                    f"Access DB has {len(tables)} tables; returned the first ('{target}'). "
                    f"Others: {', '.join(tables[1:])}.",
                    f"Access 数据库检测到 {len(tables)} 个表，已返回第一个表 '{target}'。"
                    f"其余表: {', '.join(tables[1:])}。如需指定表请用 table_name 参数。",
                )
            )

        variable_labels: dict[str, str] = {}
        column_report = _legacy_column_report(df, variable_labels)

        return {
            "dataframe": df,
            "metadata": _build_metadata(
                {
                    "variable_labels": variable_labels,
                    "value_labels": {},
                    "special_missing": {},
                    "notes": [
                        f"MS Access 表: {target}",
                        f"数据库表清单: {', '.join(tables)}",
                    ],
                },
                "access",
                extra={
                    "collected_at": timestamp,
                    "row_count": df.shape[0],
                    "column_count": df.shape[1],
                    "total_missing_pct": _calc_missing_pct(df),
                },
                format_meta={"access_tables": tables, "access_table": target},
            ),
            "warnings": warnings_list,
            "column_report": column_report,
        }
    finally:
        conn.close()


def _secure_lxml_parser():
    """构建一个针对 XXE (CVE-2026-41066) 加固的 lxml 解析器。

    不解析外部实体、禁止联网、限制树深，确保解析用户提供的 .wdx / .opju
    等 XML 时不会读取本地文件或访问网络，即便 lxml 版本偏低也安全。
    lxml 为可选/扩展依赖，故在此惰性导入。
    """
    import lxml.etree as ET
    return ET.XMLParser(resolve_entities=False, no_network=True, huge_tree=False)


# ============================================================
# Mathematica  .wdx  —— best-effort（lxml 解析 XML）
# ============================================================

def _read_wdx(filepath: str, timestamp: str) -> StatFileResult:
    """读取 Mathematica .wdx（Wolfram Data Exchange，XML 形式）。

    .wdx 有两种：旧版 XML（本函数处理）与新版 WXF 二进制（暂不支持）。
    解析策略：定位 <variable> 元素，将其值序列（<value> 或 <row>）拼为列。
    """
    import lxml.etree as ET

    try:
        tree = ET.parse(filepath, parser=_secure_lxml_parser())
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(
            _bilingual(
                f"Failed to parse .wdx: {e}",
                f".wdx 文件解析失败: {e}\n"
                f"若为 WXF 二进制格式，请用 Mathematica 'Export[\"file.wdx\", data, \"WXF\"]' "
                f"导出为 XML 形式，或用 'Export[\"file.csv\", data]' 导出 CSV。",
            )
        )

    root = tree.getroot()
    variables = root.findall(".//variable") or root.findall(".//{*}variable")
    if not variables:
        raise RuntimeError(
            _bilingual(
                "No <variable> element found in .wdx; cannot interpret as tabular data.",
                "未在 .wdx 中找到 <variable> 元素，无法识别为列数据。",
            )
        )

    warnings_list: list[str] = []
    warnings_list.append(
        _bilingual(
            ".wdx parsed on a best-effort basis; if columns are wrong, use CSV as intermediary.",
            ".wdx 为 best-effort 解析（基于常见 WDX XML 结构）；若列未正确还原请改用 CSV 中转。",
        )
    )

    columns: dict[str, list] = {}
    for var in variables:
        name = var.get("name") or var.get("varName") or f"col{len(columns)+1}"
        # 值序列：<value> 子元素 或 <row> 子元素
        vals = [c.text for c in (var.findall("value") or var.findall("{*}value")
                                 or var.findall("row") or var.findall("{*}row"))]
        # 退路：直接取文本（逗号分隔）
        if not vals and var.text:
            vals = [x.strip() for x in var.text.split(",") if x.strip() != ""]
        columns[name] = vals

    df = pd.DataFrame({k: pd.Series(v) for k, v in columns.items()})

    variable_labels: dict[str, str] = {}
    column_report = _legacy_column_report(df, variable_labels)

    return {
        "dataframe": df,
        "metadata": _build_metadata(
            {
                "variable_labels": variable_labels,
                "value_labels": {},
                "special_missing": {},
                "notes": [f"Mathematica .wdx (best-effort): {os.path.basename(filepath)}"],
            },
            "wdx",
            extra={
                "collected_at": timestamp,
                "row_count": df.shape[0],
                "column_count": df.shape[1],
                "total_missing_pct": _calc_missing_pct(df),
            },
            format_meta={"wdx_vars": list(columns.keys())},
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }


# ============================================================
# Origin  .opju / .oggu  —— best-effort（zip + XML）
# ============================================================

def _read_origin(filepath: str, timestamp: str) -> StatFileResult:
    """读取 Origin 项目 .opju（zip 包）/.oggu（旧版，尝试 zip）。

    Origin 项目为 OOXML 风格 zip，工作表数据在 worksheet XML 的 <Data> 元素中。
    best-effort：解包后查找含 <Data> 的 worksheet，将首个二维数据块转为 DataFrame。
    """
    if not zipfile.is_zipfile(filepath):
        raise RuntimeError(
            _bilingual(
                f"Not a valid Origin package (expected zip): {os.path.basename(filepath)}",
                f"文件不是有效的 Origin 包（期望 zip 结构）: {os.path.basename(filepath)}\n"
                f"若为旧版 .oggu 二进制，请用 Origin 导出为 .opju 或 CSV。",
            )
        )

    warnings_list: list[str] = []
    warnings_list.append(
        _bilingual(
            "Origin read is best-effort; for complex workbooks export CSV from Origin.",
            "Origin 读取为 best-effort（基于常见 worksheet XML 结构）；复杂工作簿建议用 Origin 导出 CSV。",
        )
    )

    import lxml.etree as ET

    found: list[pd.DataFrame] = []
    try:
        with zipfile.ZipFile(filepath) as zf:
            names = zf.namelist()
            for n in names:
                if not (n.lower().endswith(".xml") or n.lower().endswith(".xhtml")):
                    continue
                try:
                    tree = ET.parse(io.BytesIO(zf.read(n)), parser=_secure_lxml_parser())
                except Exception:  # noqa: BLE001
                    continue
                root = tree.getroot()
                # 查找所有 <Data> 二维块
                data_elems = root.findall(".//Data") or root.findall(".//{*}Data")
                for de in data_elems:
                    rows = []
                    for r in (de.findall("row") or de.findall("{*}row") or []):
                        cells = [c.text for c in (r.findall("c") or r.findall("{*}c")
                                                  or r.findall("d") or r.findall("{*}d"))]
                        if cells:
                            rows.append(cells)
                    if len(rows) >= 1:
                        # 首行作表头（若像字符串），否则自动列名
                        header = rows[0]
                        if all(isinstance(h, str) and h and not _looks_numeric(h) for h in header):
                            df = pd.DataFrame(rows[1:], columns=header)
                        else:
                            df = pd.DataFrame(rows)
                        found.append(df)
                        break  # 每个 worksheet 取第一个数据块
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(
            _bilingual(f"Origin package parse failed: {e}", f"Origin 包解析失败: {e}")
        )

    if not found:
        raise RuntimeError(
            _bilingual(
                "No parseable worksheet data block found in Origin package.",
                "未在 Origin 包中找到可解析的工作表数据块。",
            )
        )

    # 返回数据量最大的块
    df = max(found, key=lambda d: d.shape[0] * d.shape[1])
    if len(found) > 1:
        warnings_list.append(
            _bilingual(
                f"Origin package had {len(found)} data blocks; returned the largest.",
                f"Origin 包中找到 {len(found)} 个数据块，已返回最大的一个。",
            )
        )

    variable_labels: dict[str, str] = {}
    column_report = _legacy_column_report(df, variable_labels)

    return {
        "dataframe": df,
        "metadata": _build_metadata(
            {
                "variable_labels": variable_labels,
                "value_labels": {},
                "special_missing": {},
                "notes": [f"Origin project (best-effort): {os.path.basename(filepath)}"],
            },
            "origin",
            extra={
                "collected_at": timestamp,
                "row_count": df.shape[0],
                "column_count": df.shape[1],
                "total_missing_pct": _calc_missing_pct(df),
            },
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }


def _looks_numeric(s: Any) -> bool:
    try:
        float(str(s))
        return True
    except (ValueError, TypeError):
        return False


# ============================================================
# 占位降级 readers（专有二进制，无现成库）
# ============================================================

_read_cport = _make_unsupported(
    "SAS CPORT",
    ".xpt (SAS XPORT, 本技能已支持) 或 .sas7bdat",
    ".xpt (SAS XPORT, already supported) or .sas7bdat",
)
_read_statistica = _make_unsupported(
    "Statistica", ".sav 或 .csv", ".sav or .csv"
)
_read_oxmetrics = _make_unsupported(
    "OxMetrics", ".csv 或 .dta (Stata)", ".csv or .dta (Stata)"
)
_read_systat = _make_unsupported(
    "SYSTAT", ".csv 或 .sav (SPSS)", ".csv or .sav (SPSS)"
)
_read_paradox = _make_unsupported(
    "Paradox", ".dbf 或 .csv", ".dbf or .csv"
)
_read_limdep = _make_unsupported(
    "LIMDEP/NLOGIT", ".csv", ".csv"
)
_read_ncss = _make_unsupported(
    "NCSS", ".csv", ".csv"
)
_read_sas_ssp = _make_unsupported(
    "SAS 6 数据集 (.ssp)",
    ".sas7bdat (SAS 7+) 或 .xpt (SAS XPORT)",
    ".sas7bdat (SAS 7+) or .xpt (SAS XPORT)",
)
