"""
reader_core.py - 核心数据结构与公共接口
 TypedDict 定义、工具函数、read_stat_file 入口
 所有格式 handler 通过延迟导入加载，避免循环依赖
"""
from __future__ import annotations

import os
import json
from datetime import datetime
from typing import Any, TypedDict

import pandas as pd
import pyreadstat


# ═══════════════════════════════════════════════════════════════════════════════
# TypedDict 定义（所有格式共享的数据架构）
# ═══════════════════════════════════════════════════════════════════════════════

class ColumnInfo(TypedDict):
    """列级详情报告"""
    source_type: str
    pandas_dtype: str
    original_label: str | None
    has_value_labels: bool
    n_missing: int
    missing_are_special: bool
    precision_warning: bool
    format_string: str | None
    display_width: int | None
    storage_width: int | None
    measure_level: str | None
    alignment: str | None
    original_type: str | None
    formula: str | None
    column_property: dict | None


class MRSet(TypedDict):
    """多响应集（MR Sets）"""
    type: str
    is_dichotomy: bool
    counted_value: int | None
    label: str
    variable_list: list[str]


class MissingRange(TypedDict):
    """自定义缺失值范围"""
    lo: float
    hi: float


class BaseMeta(TypedDict):
    """基础元数据（所有格式共享）"""
    file_format: str
    collected_at: str
    row_count: int
    column_count: int
    total_missing_pct: float
    variable_labels: dict[str, str]
    value_labels: dict[str, dict]
    special_missing: dict
    date_origin: str | None
    file_encoding: str | None
    file_label: str | None
    creation_time: str | None
    modification_time: str | None
    notes: list[str]
    original_variable_types: dict[str, str]
    readstat_variable_types: dict[str, str]
    variable_value_labels: dict[str, dict]
    variable_to_label: dict[str, str]
    missing_user_values: dict
    missing_ranges: dict
    variable_display_width: dict[str, int]
    variable_storage_width: dict[str, int]
    variable_measure: dict[str, str]
    variable_alignment: dict[str, str]
    column_names_to_labels: dict[str, str]
    mr_sets: dict
    table_name: str | None


class RMeta(BaseMeta):
    """R 格式扩展元数据"""
    r_metadata: dict[str, Any]


class StataMeta(BaseMeta):
    """Stata 格式扩展元数据"""
    pass


class SasMeta(BaseMeta):
    """SAS 数据格式扩展元数据"""
    pass


class SpssMeta(BaseMeta):
    """SPSS 格式扩展元数据"""
    pass


class ExcelMeta(BaseMeta):
    """Excel 格式扩展元数据"""
    excel_metadata: dict[str, Any]


class MatlabMeta(BaseMeta):
    """MATLAB 格式扩展元数据"""
    matlab_metadata: dict[str, Any]


class Hdf5Meta(BaseMeta):
    """HDF5 格式扩展元数据"""
    hdf5_metadata: dict[str, Any]


class ParquetMeta(BaseMeta):
    """Parquet 格式扩展元数据"""
    parquet_metadata: dict[str, Any]


class FeatherMeta(BaseMeta):
    """Feather 格式扩展元数据"""
    feather_metadata: dict[str, Any]


class JsonMeta(BaseMeta):
    """JSON 格式扩展元数据"""
    json_metadata: dict[str, Any]


class XmlMeta(BaseMeta):
    """XML 格式扩展元数据"""
    xml_metadata: dict[str, Any]


class OdsMeta(BaseMeta):
    """ODS 格式扩展元数据"""
    ods_metadata: dict[str, Any]


class HtmlMeta(BaseMeta):
    """HTML 格式扩展元数据"""
    html_metadata: dict[str, Any]


class OrcMeta(BaseMeta):
    """ORC 格式扩展元数据"""
    orc_metadata: dict[str, Any]


class FstMeta(BaseMeta):
    """FST 格式扩展元数据"""
    fst_metadata: dict[str, Any]


class OdmMeta(BaseMeta):
    """CDISC ODM 格式扩展元数据"""
    odm_metadata: dict[str, Any]


class SasCatalogMeta(BaseMeta):
    """SAS 目录文件 (.sas7bcat) 扩展元数据"""
    sas_catalog_metadata: dict[str, Any]


class JmpMeta(BaseMeta):
    """JMP 数据文件 (.jmp) 扩展元数据"""
    jmp_metadata: dict[str, Any]


class MinitabMeta(BaseMeta):
    """Minitab 工作簿文件扩展元数据"""
    minitab_metadata: dict[str, Any]


class PrismMeta(BaseMeta):
    """GraphPad Prism 项目文件扩展元数据"""
    prism_metadata: dict[str, Any]


class JamoviMeta(BaseMeta):
    """jamovi 项目文件扩展元数据"""
    jamovi_metadata: dict[str, Any]


class EpidataMeta(BaseMeta):
    """EpiData 数据文件扩展元数据"""
    epidata_metadata: dict[str, Any]


class EviewsMeta(BaseMeta):
    """EViews 数据文件扩展元数据"""
    eviews_metadata: dict[str, Any]


class GretlMeta(BaseMeta):
    """Gretl 数据文件扩展元数据"""
    gretl_metadata: dict[str, Any]


class ArffMeta(BaseMeta):
    """Weka ARFF 数据文件扩展元数据"""
    arff_metadata: dict[str, Any]


class EpinfoMeta(BaseMeta):
    """EpiInfo 项目文件扩展元数据"""
    epinfo_metadata: dict[str, Any]


StatFileResult = dict[str, Any]


__all__ = [
    # TypedDict
    "ColumnInfo", "MRSet", "MissingRange", "BaseMeta",
    "StataMeta", "SasMeta", "SpssMeta", "RMeta", "ExcelMeta",
    "MatlabMeta", "Hdf5Meta", "ParquetMeta", "FeatherMeta",
    "JsonMeta", "XmlMeta", "OdsMeta", "HtmlMeta", "OrcMeta",
    "FstMeta", "OdmMeta",
    "SasCatalogMeta", "JmpMeta", "MinitabMeta", "PrismMeta",
    "JamoviMeta", "EpidataMeta", "EviewsMeta", "GretlMeta", "ArffMeta", "EpinfoMeta",
    # 公共函数
    "read_stat_file", "read_all_sheets", "read_all_r_objects",
    "apply_value_labels", "apply_variable_labels", "generate_read_report",
]


# ═══════════════════════════════════════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════════════════════════════════════

DATE_ORIGINS = {
    "stata": "1960-01-01",
    "sas": "1960-01-01",
    "spss": "1960-01-01",
    "excel": "1899-12-30",
}


# ═══════════════════════════════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════════════════════════════

def _calc_missing_pct(df: pd.DataFrame) -> float:
    """计算总缺失值百分比"""
    if df.empty:
        return 0.0
    total = df.shape[0] * df.shape[1]
    if total == 0:
        return 0.0
    missing = df.isnull().sum().sum()
    return round(missing / total * 100, 2)


def _bilingual(en: str, zh: str) -> str:
    """Create bilingual string (en | zh). English first, Chinese second."""
    return f"{en} | {zh}"


def _parse_value_labels(val_raw: dict) -> dict:
    """Helper: 将 JSON 序列化后的值标签（字符串键）还原为数值键"""
    val_labels = {}
    for var, labs in val_raw.items():
        if not isinstance(labs, dict):
            continue
        val_labels[var] = {}
        for v, l in labs.items():
            try:
                val_labels[var][int(v)] = l
            except (ValueError, TypeError):
                try:
                    val_labels[var][float(v)] = l
                except (ValueError, TypeError):
                    val_labels[var][v] = l
    return val_labels


# 与 writer.py 保持一致的嵌入 key
STAT_FULL_META_KEY = "stat-full-meta"


def restore_full_meta(meta_json: dict) -> dict:
    """从嵌入的 stat-full-meta JSON 中还原全部 17 个元数据字段
    
    返回包含所有字段的 dict，空字段用默认值填充。
    会自动还原 value_labels 中的数值键（JSON 会将数字键序列化为字符串）
    """
    if not meta_json:
        return {}
    
    restored = dict(meta_json)  # copy
    
    # 还原 value_labels 数值键
    val_raw = restored.get("value_labels", {})
    if val_raw:
        restored["value_labels"] = _parse_value_labels(val_raw)
    
    return restored


def _get_source_type(series: pd.Series) -> str:
    """获取列的数据来源类型"""
    if pd.api.types.is_integer_dtype(series):
        return "int"
    if pd.api.types.is_float_dtype(series):
        return "float"
    if pd.api.types.is_bool_dtype(series):
        return "bool"
    if pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    if isinstance(series.dtype, pd.CategoricalDtype):
        return "category"
    return "str"


def _is_stata_special_missing(val: float) -> bool:
    """检查是否为 Stata 特殊缺失值 (.a-.z)"""
    if pd.isna(val):
        return False
    return 100 <= val <= 127


def _auto_detect_encoding(filepath: str, *, metadata_only: bool = True) -> str | None:
    """自动检测 SPSS/Stata/SAS 文件的变量标签编码。

    优先使用 pyreadstat 从文件头部读出的声明编码（file_encoding），
    这是最可靠的方式（UTF-8 / GBK / Windows-1252 / ISO-8859-1 等）。
    仅当声明编码缺失或未知时，才回退到启发式检测链：
    UTF-8 → GB18030 → GBK → Latin-1，并校验中文标签解码后无乱码（无 U+FFFD）。
    """
    def _read_meta(enc=None):
        if filepath.endswith(".por"):
            return pyreadstat.read_por(filepath, encoding=enc, metadataonly=metadata_only) if enc else pyreadstat.read_por(filepath, metadataonly=metadata_only)
        if filepath.endswith((".sav", ".zsav")):
            return pyreadstat.read_sav(filepath, encoding=enc, metadataonly=metadata_only) if enc else pyreadstat.read_sav(filepath, metadataonly=metadata_only)
        if filepath.endswith(".dta"):
            return pyreadstat.read_dta(filepath, encoding=enc, metadataonly=metadata_only) if enc else pyreadstat.read_dta(filepath, metadataonly=metadata_only)
        if filepath.endswith(".sas7bdat"):
            return pyreadstat.read_sas7bdat(filepath, encoding=enc, metadataonly=metadata_only) if enc else pyreadstat.read_sas7bdat(filepath, metadataonly=metadata_only)
        if filepath.endswith(".xpt"):
            return pyreadstat.read_xport(filepath, encoding=enc, metadataonly=metadata_only) if enc else pyreadstat.read_xport(filepath, metadataonly=metadata_only)
        return None

    # 1) 优先使用文件声明的编码（最可靠）
    try:
        res = _read_meta()
        if res is not None:
            _, m0 = res
            declared = getattr(m0, "file_encoding", None)
            if declared and str(declared).strip().lower() not in ("none", "unknown", ""):
                return str(declared)
    except Exception:
        pass

    # 2) 启发式回退：UTF-8 优先（现代文件默认），再 CJK，最后 Latin-1
    for enc in ("utf-8", "gb18030", "gbk", "latin1"):
        try:
            res = _read_meta(enc)
            if res is None:
                continue
            _, m = res
            labels = getattr(m, "column_names_to_labels", {}) or {}
            for v in labels.values():
                if isinstance(v, str) and any(ord(c) > 127 for c in v):
                    if "�" in v or "\ufffd" in v:
                        raise UnicodeDecodeError(enc, b"", 0, 0, "replacement char in label")
                    v.encode(enc)  # 中文标签应可正常编码
            return enc
        except Exception:
            continue
    return None


def _extract_pyreadstat_meta(meta: Any) -> dict[str, Any]:
    """从 pyreadstat 元数据对象提取为纯 dict — 100% 覆盖 pyreadstat 属性"""
    if meta is None:
        return {}
    # pyreadstat 的 variable_labels 属性不存在，使用 column_names_to_labels
    column_names_to_labels = getattr(meta, "column_names_to_labels", {}) or {}
    return {
        # 文件基本信息
        "row_count": getattr(meta, "row_count", None),
        "column_count": getattr(meta, "column_count", None),
        "column_names": getattr(meta, "column_names", []),
        "column_names_to_labels": column_names_to_labels,
        "number_columns": getattr(meta, "number_columns", None),
        "number_rows": getattr(meta, "number_rows", None),
        "table_name": getattr(meta, "table_name", None),
        # 文件标签 / 编码 / 时间戳
        "file_label": getattr(meta, "file_label", None),
        "file_encoding": getattr(meta, "file_encoding", None),
        "creation_time": str(getattr(meta, "creation_time", "")) if getattr(meta, "creation_time", None) else None,
        "modification_time": str(getattr(meta, "modification_time", "")) if getattr(meta, "modification_time", None) else None,
        "notes": getattr(meta, "notes", []),
        # 变量级标签 — variable_labels 与 column_names_to_labels 共用
        "variable_labels": column_names_to_labels,
        "value_labels": getattr(meta, "value_labels", {}),
        "variable_value_labels": getattr(meta, "variable_value_labels", {}) or {},
        "variable_to_label": getattr(meta, "variable_to_label", {}) or {},
        # 变量属性
        "variable_display_width": getattr(meta, "variable_display_width", {}) or {},
        "variable_storage_width": getattr(meta, "variable_storage_width", {}) or {},
        "variable_measure": getattr(meta, "variable_measure", {}) or {},
        "variable_alignment": getattr(meta, "variable_alignment", {}) or {},
        "original_variable_types": getattr(meta, "original_variable_types", {}) or {},
        "readstat_variable_types": getattr(meta, "readstat_variable_types", {}) or {},
        # 缺失值
        "missing_ranges": getattr(meta, "missing_ranges", {}) or {},
        "missing_user_values": getattr(meta, "missing_user_values", {}) or {},
        # 以上全部确保在 dict 中
        "special_missing": getattr(meta, "special_missing", {}),  # SAS/Stata 特殊缺失值
        "mr_sets": getattr(meta, "mr_sets", {}),  # 多重响应集
        # 以下两个关键字段：variable_format 和 column_properties
        "variable_format": getattr(meta, "variable_format", {}) or {},  # Stata / SPSS / SAS 格式字符串
        "column_properties": getattr(meta, "column_properties", {}) or {},  # SPSS 列级属性
    }


def _normalize_value_labels(variable_value_labels: dict, variable_to_label: dict, value_labels: dict = None) -> dict:
    """
    标准化值标签映射
    
    Parameters
    ----------
    variable_value_labels : dict
        变量级别的值标签映射 {varname: {value: label}}
    variable_to_label : dict
        变量到标签名的映射 {varname: label_name}
    value_labels : dict, optional
        全局值标签定义 {label_name: {value: label}}（pyreadstat 新增字段）
    """
    if variable_value_labels:
        return variable_value_labels
    if variable_to_label:
        result = {}
        # 如果有全局值标签，尝试解析
        if value_labels:
            for var, lbl_name in variable_to_label.items():
                if lbl_name in value_labels:
                    result[var] = value_labels[lbl_name]
                else:
                    result[var] = {"_label_name": lbl_name}
        else:
            for var, lbl_name in variable_to_label.items():
                result[var] = {"_label_name": lbl_name}
        return result
    return {}


def _serialize_missing(obj: Any) -> Any:
    """序列化缺失值对象为 JSON 安全格式"""
    if isinstance(obj, (list, tuple)):
        return [_serialize_missing(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _serialize_missing(v) for k, v in obj.items()}
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    return str(obj)


def _normalize_missing_ranges(missing_ranges: dict) -> dict:
    """标准化缺失值范围"""
    result = {}
    for var, ranges in missing_ranges.items():
        if isinstance(ranges, list):
            result[var] = [_serialize_missing(r) for r in ranges]
        else:
            result[var] = _serialize_missing(ranges)
    return result


def _normalize_missing_user_values(missing_user_values: dict) -> dict:
    """标准化用户自定义缺失值"""
    result = {}
    for var, vals in missing_user_values.items():
        if isinstance(vals, list):
            result[var] = [float(v) if isinstance(v, (int, float)) else v for v in vals]
        else:
            result[var] = float(vals) if isinstance(vals, (int, float)) else vals
    return result


def _normalize_mr_sets(mr_sets: dict) -> dict:
    """标准化多响应集"""
    return {k: _serialize_missing(v) for k, v in mr_sets.items()}


def _read_gretl_gdtb_hint(filepath: str):
    """Raise helpful error for binary .gdtb files."""
    raise ValueError(
        "Gretl .gdtb 二进制格式暂不支持读入 | Gretl .gdtb binary format is not yet supported for reading.\n"
        "请用 Gretl 打开数据后导出为 XML 格式 | Please open with Gretl and export to XML format:\n"
        "  File → Save Data → 选择 'GDT (XML)' | File → Save Data → select 'GDT (XML)'\n"
        "或使用 Gretl 脚本 | Or use Gretl script:\n"
        "  open data.gdtb\n"
        "  store data.gdt"
    )


def _build_metadata(all_meta: dict, format_name: str, extra: dict | None = None,
                    format_meta: dict | None = None) -> dict:
    """构建元数据 dict
    
    Parameters
    ----------
    all_meta : dict
        基础元数据字段
    format_name : str
        格式标识符
    extra : dict, optional
        额外字段（如 collected_at、row_count、column_count、total_missing_pct）
    format_meta : dict, optional
        格式特定的扩展元数据（如 gretl_metadata、arff_metadata、epinfo_metadata）
    """
    meta = {}
    meta["file_format"] = format_name
    meta["collected_at"] = datetime.now().isoformat(timespec="seconds")
    meta["row_count"] = all_meta.get("row_count", 0)
    meta["column_count"] = all_meta.get("column_count", 0)
    meta["total_missing_pct"] = _calc_missing_pct(
        pd.DataFrame()  # 空 DataFrame，占位
    )
    meta["variable_labels"] = all_meta.get("variable_labels", {})
    meta["value_labels"] = all_meta.get("value_labels", {})
    meta["special_missing"] = all_meta.get("special_missing", {})
    meta["measurement_levels"] = all_meta.get("measurement_levels", {})
    meta["date_origin"] = DATE_ORIGINS.get(format_name)
    meta["file_encoding"] = all_meta.get("file_encoding")
    meta["file_label"] = all_meta.get("file_label")
    meta["creation_time"] = all_meta.get("creation_time")
    meta["modification_time"] = all_meta.get("modification_time")
    meta["notes"] = all_meta.get("notes", [])
    meta["original_variable_types"] = all_meta.get("original_variable_types", {})
    meta["readstat_variable_types"] = all_meta.get("readstat_variable_types", {})
    meta["variable_value_labels"] = all_meta.get("variable_value_labels", {})
    meta["variable_to_label"] = all_meta.get("variable_to_label", {})
    meta["missing_user_values"] = all_meta.get("missing_user_values", {})
    meta["missing_ranges"] = all_meta.get("missing_ranges", {})
    meta["variable_display_width"] = all_meta.get("variable_display_width", {})
    meta["variable_storage_width"] = all_meta.get("variable_storage_width", {})
    meta["variable_measure"] = all_meta.get("variable_measure", {})
    meta["variable_alignment"] = all_meta.get("variable_alignment", {})
    meta["column_names_to_labels"] = all_meta.get("column_names_to_labels", {})
    meta["mr_sets"] = all_meta.get("mr_sets", {})
    meta["table_name"] = all_meta.get("table_name")
    meta["variable_format"] = all_meta.get("variable_format", {})
    meta["column_properties"] = all_meta.get("column_properties", {})

    meta["missing_ranges"] = _normalize_missing_ranges(meta.get("missing_ranges", {}))
    meta["missing_user_values"] = _normalize_missing_user_values(meta.get("missing_user_values", {}))
    meta["mr_sets"] = _normalize_mr_sets(meta.get("mr_sets", {}))

    if extra:
        meta.update(extra)
    
    # Inject format-specific metadata (e.g., gretl_metadata, arff_metadata)
    if format_meta:
        meta.update(format_meta)

    return meta


def _build_column_report(
    df: pd.DataFrame,
    all_meta: dict,
    value_labels: dict,
    missing_ranges: dict,
    missing_user_values: dict,
    warnings_list: list,
    format_type: str,
) -> dict[str, ColumnInfo]:
    """构建列级详情报告"""
    column_report: dict[str, ColumnInfo] = {}
    variable_labels = all_meta.get("variable_labels", {})

    for col in df.columns:
        col_info: ColumnInfo = {
            "source_type": _get_source_type(df[col]),
            "pandas_dtype": str(df[col].dtype),
            "original_label": variable_labels.get(col),
            "has_value_labels": col in value_labels,
            "n_missing": int(df[col].isnull().sum()),
            "missing_are_special": col in missing_ranges or col in missing_user_values,
            "precision_warning": False,
            "format_string": all_meta.get("variable_format", {}).get(col),
            "display_width": all_meta.get("variable_display_width", {}).get(col),
            "storage_width": all_meta.get("variable_storage_width", {}).get(col),
            "measure_level": all_meta.get("variable_measure", {}).get(col),
            "alignment": all_meta.get("variable_alignment", {}).get(col),
            "original_type": all_meta.get("original_variable_types", {}).get(col),
            "column_property": all_meta.get("column_properties", {}).get(col),
        }

        if pd.api.types.is_integer_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                col_info["precision_warning"] = True
                warnings_list.append(f"列 '{col}' >1e15 | Column '{col}' contains values >1e15, float64 precision may be insufficient")

        column_report[col] = col_info

    return column_report


def apply_value_labels(df: pd.DataFrame, value_labels: dict, *, inplace: bool = False,
                       drop_original: bool = False, suffix: str = "_label") -> pd.DataFrame:
    """将值标签应用到 DataFrame（类似 Stata/SPSS 的 value labels）"""
    target = df if inplace else df.copy()
    for var, mapping in value_labels.items():
        if var in target.columns:
            lbl_col = f"{var}{suffix}"
            target[lbl_col] = target[var].map(mapping).fillna("").astype(str)
            if drop_original:
                target.drop(columns=[var], inplace=True)
                target.rename(columns={lbl_col: var}, inplace=True)
    return target


def apply_variable_labels(df: pd.DataFrame, variable_labels: dict) -> pd.DataFrame:
    """将变量标签应用到 DataFrame 的列名（类似 Stata/SPSS 的 variable labels）"""
    target = df.copy()
    rename_map = {var: lbl for var, lbl in variable_labels.items() if var in target.columns}
    if rename_map:
        target.rename(columns=rename_map, inplace=True)
    return target


def generate_read_report(result: StatFileResult) -> str:
    """Generate human-readable read report (zh-cn/en)."""
    meta = result["metadata"]
    warnings_list = result["warnings"]
    column_report = result["column_report"]

    lines = []
    lines.append(f"=== 数据读入报告 | Data Read Report ({meta.get('file_format', 'unknown')}) ===")
    lines.append(f"来源文件 | Source format: {meta.get('file_format', 'unknown')}")
    lines.append(f"读入时间 | Read time: {meta.get('collected_at', 'unknown')}")
    lines.append(f"数据维度 | Dimensions: {meta.get('row_count', '?')} 行 | rows × {meta.get('column_count', '?')} 列 | columns")

    if meta.get("file_encoding"):
        lines.append(f"文件编码 | Encoding: {meta['file_encoding']}")
    if meta.get("file_label"):
        lines.append(f"文件标签 | Label: {meta['file_label']}")

    missing_pct = meta.get("total_missing_pct", 0)
    lines.append(f"总缺失值 | Total missing: {missing_pct}%")

    if meta.get("variable_labels"):
        lines.append(f"变量标签数 | Variable labels: {len(meta['variable_labels'])}")
    if meta.get("value_labels"):
        lines.append(f"值标签集数 | Value label sets: {len(meta['value_labels'])}")
    if meta.get("notes"):
        for note in meta["notes"][:3]:
            lines.append(f"  注 | Note: {note[:100]}")

    if warnings_list:
        lines.append(f"\n⚠️ 警告 | Warnings ({len(warnings_list)}):")
        for w in warnings_list[:10]:
            lines.append(f"  - {w[:150]}")

    if column_report:
        lines.append(f"\n=== 列级报告 | Column Report ===")
        for col, info in list(column_report.items())[:20]:
            missing_info = f", n_missing={info['n_missing']}" if info['n_missing'] > 0 else ''
            lines.append(
                f"  {col}: {info.get('source_type', '?')} -> {info.get('pandas_dtype', '?')}{missing_info}"
                f" | {'!!' if info.get('missing_are_special') else '-'}"
                f" | {'!!' if info.get('precision_warning') else '-'}"
            )

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# 公共接口（延迟导入 handler 子模块，避免循环依赖）
# ═══════════════════════════════════════════════════════════════════════════════


def read_stat_file(
    filepath: str,
    *,
    user_missings: bool = True,
    encoding: str | None = None,
    sheet_name: str | None = None,
    object_name: str | None = None,
    table_name: str | None = None,
    allow_r_exec: bool = False,
) -> StatFileResult:
    """读入统计软件格式文件，最大限度保留元数据。

    对于多 Sheet Excel：可通过 sheet_name 指定工作表，不指定则默认选最大的
    对于多对象 RDA：可通过 object_name 指定对象，不指定则默认选最大的 DataFrame
    对于多表 Access：可通过 table_name 指定表名，不指定则默认选首个
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"文件不存在: {filepath}")

    timestamp = datetime.now().isoformat(timespec="seconds")

    # 分区 Parquet 目录（含 part-*.parquet）：直接走专用读入，无需扩展名
    if os.path.isdir(filepath):
        from . import reader_science
        import glob

        # 校验确为 Parquet 分区目录，避免任意目录（如误传路径、命名 .sav 的目录）
        # 被静默当作 Parquet 读取而产生令人困惑的底层错误。
        has_parquet = (
            glob.glob(os.path.join(filepath, "**", "*.parquet"), recursive=True)
            or glob.glob(os.path.join(filepath, "**", "*.pq"), recursive=True)
        )
        if not has_parquet:
            raise ValueError(_bilingual(
                f"Directory is not a Parquet partition: {filepath}\n"
                f"No .parquet files found inside. Please pass a real data file or a Parquet partition directory.",
                f"目录不是 Parquet 分区目录: {filepath}\n"
                f"内部未发现 .parquet 文件。请传入真实的数据文件或 Parquet 分区目录。",
            ))
        return reader_science._read_parquet_partitioned(filepath, timestamp)

    # 延迟导入所有 handler（避免循环依赖）
    from . import (
        reader_spss, reader_sas, reader_stata, reader_r,
        reader_excel, reader_science, reader_modern, reader_odm,
        reader_v14, reader_epinfo, reader_arff, reader_gretl, reader_tableau, reader_legacy,
    )

    ext = os.path.splitext(filepath)[1].lower()
    format_map = {
        ".dta": "stata",
        ".sas7bdat": "sas", ".xpt": "sas_xpt", ".sd2": "sas_sd2",
        ".sav": "spss_sav", ".zsav": "spss_zsav", ".por": "spss_por",
        ".rda": "r_rda", ".rdata": "r_rda", ".rds": "r_rds",
        ".xlsx": "excel_xlsx", ".xls": "excel_xls", ".xlsm": "excel_xlsm",
        ".mat": "matlab_mat",
        ".h5": "hdf5_h5", ".hdf5": "hdf5_h5",
        ".parquet": "parquet_parquet",
        ".feather": "feather_feather", ".arrow": "feather_arrow",
        ".orc": "orc_orc", ".fst": "fst_fst",
        ".json": "json_json", ".xml": "xml_xml", ".ods": "ods_ods",
        ".html": "html_html",
        ".csv": "csv_csv",
        ".tsv": "csv_tsv",                              # 制表符分隔 (与 writer 对称)
        ".odm": "odm_odm",
        ".sas7bcat": "sas_catalog",
        ".jmp": "jmp_jmp",
        ".mtw": "minitab_mtw", ".mpj": "minitab_mpj",
        ".pzfx": "prism_pzfx", ".pz": "prism_pz",
        ".omv": "jamovi_omv",
        ".rec": "epidata_rec",
        ".wf1": "eviews_wf1", ".wf2": "eviews_wf2",
        # v1.7 新增
        ".prj": "epinfo_prj",      # EpiInfo project file
        ".arff": "arff_arff",       # Weka ARFF
        ".gdt": "gretl_gdt",        # Gretl data
        ".gdtb": "gretl_gdtb",      # Gretl binary data (hint only)
        ".hyper": "tableau_hyper",  # Tableau Hyper extract
        ".twbx": "tableau_twbx",    # Tableau packaged workbook (zip; embeds .hyper)
        ".twb": "tableau_twb",      # Tableau workbook XML (no embedded data)
        # v1.10 新增（Stat/Transfer 9 对照缺口）
        ".dbf": "dbf_dbf",                    # dBASE / FoxPro
        ".mdb": "access_mdb",                 # MS Access (pyodbc + 系统驱动)
        ".accdb": "access_accdb",
        ".wdx": "wdx_wdx",                    # Mathematica Wolfram Data Exchange
        ".opju": "origin_opju",               # Origin project (zip+XML)
        ".oggu": "origin_oggu",
        ".cpt": "sas_cport",                  # SAS CPORT (占位: 需 SAS 导出)
        ".sta": "statistica_sta",             # Statistica (占位: 需导出)
        ".in7": "oxmetrics_in7",              # OxMetrics (占位: 需导出)
        ".sys": "systat_sys",                 # SYSTAT (占位: 需导出)
        ".syd": "systat_syd",
        ".db": "paradox_db",                  # Paradox (占位: 需导出)
        ".px": "paradox_px",
        ".lpw": "limdep_lpw",                 # LIMDEP/NLOGIT (占位: 需导出)
        ".ncss": "ncss_ncss",                 # NCSS (占位: 需导出)
        ".ssp": "sas_ssp",                    # SAS 6 数据集 (Windows), 占位: 需 SAS 导出 .sas7bdat/.xpt
    }

    file_format = format_map.get(ext)
    if file_format is None:
        raise ValueError(f"不支持的文件扩展名: {ext}")

    handlers = {
        "stata": lambda: reader_stata._read_stata(filepath, timestamp,
                                                   user_missings=user_missings, encoding=encoding),
        "sas": lambda: reader_sas._read_sas(filepath, timestamp,
                                            format_type="sas", user_missing=user_missings, encoding=encoding),
        "sas_xpt": lambda: reader_sas._read_sas(filepath, timestamp,
                                                format_type="sas_xpt", user_missing=user_missings, encoding=encoding),
        "sas_sd2": lambda: reader_sas._read_sas(filepath, timestamp,
                                                format_type="sas_sd2", user_missing=user_missings, encoding=encoding),
        "sas_catalog": lambda: reader_v14._read_sas_catalog(filepath, timestamp),
        "spss_sav": lambda: reader_spss._read_spss(filepath, timestamp,
                                                   format_type="spss_sav", user_missings=user_missings, encoding=encoding),
        "spss_zsav": lambda: reader_spss._read_spss(filepath, timestamp,
                                                    format_type="spss_zsav", user_missings=user_missings, encoding=encoding),
        "spss_por": lambda: reader_spss._read_spss(filepath, timestamp,
                                                   format_type="spss_por", user_missings=user_missings, encoding=encoding),
        "r_rda": lambda: reader_r._read_r(filepath, timestamp,
                                          format_type="r_rda", object_name=object_name, allow_r_exec=allow_r_exec),
        "r_rds": lambda: reader_r._read_r(filepath, timestamp,
                                          format_type="r_rds", object_name=object_name, allow_r_exec=allow_r_exec),
        "excel_xlsx": lambda: reader_excel._read_excel(filepath, timestamp,
                                                       format_type="excel_xlsx", encoding=encoding, sheet_name=sheet_name),
        "excel_xls": lambda: reader_excel._read_excel(filepath, timestamp,
                                                      format_type="excel_xls", encoding=encoding, sheet_name=sheet_name),
        "excel_xlsm": lambda: reader_excel._read_excel(filepath, timestamp,
                                                       format_type="excel_xlsm", encoding=encoding, sheet_name=sheet_name),
        "matlab_mat": lambda: reader_science._read_matlab(filepath, timestamp),
        "hdf5_h5": lambda: reader_science._read_hdf5(filepath, timestamp),
        "parquet_parquet": lambda: reader_science._read_parquet(filepath, timestamp),
        "feather_feather": lambda: reader_science._read_feather(filepath, timestamp),
        "feather_arrow": lambda: reader_science._read_feather(filepath, timestamp),
        "orc_orc": lambda: reader_science._read_orc(filepath, timestamp),
        "fst_fst": lambda: reader_science._read_fst(filepath, timestamp),
        "json_json": lambda: reader_modern._read_json(filepath, timestamp),
        "xml_xml": lambda: reader_modern._read_xml(filepath, timestamp),
        "ods_ods": lambda: reader_modern._read_ods(filepath, timestamp),
        "html_html": lambda: reader_modern._read_html(filepath, timestamp),
        "csv_csv": lambda: reader_modern._read_csv(filepath, timestamp, encoding=encoding),
        "csv_tsv": lambda: reader_modern._read_csv(filepath, timestamp, encoding=encoding, sep="\t"),
        "odm_odm": lambda: reader_odm._read_odm(filepath, timestamp),
        "jmp_jmp": lambda: reader_v14._read_jmp(filepath, timestamp),
        "minitab_mtw": lambda: reader_v14._read_minitab(filepath, timestamp,
                                                         format_type="minitab_mtw", allow_r_exec=allow_r_exec),
        "minitab_mpj": lambda: reader_v14._read_minitab(filepath, timestamp,
                                                         format_type="minitab_mpj", allow_r_exec=allow_r_exec),
        "prism_pzfx": lambda: reader_v14._read_prism(filepath, timestamp,
                                                     format_type="prism_pzfx"),
        "prism_pz": lambda: reader_v14._read_prism(filepath, timestamp,
                                                   format_type="prism_pz"),
        "jamovi_omv": lambda: reader_v14._read_jamovi(filepath, timestamp),
        "epidata_rec": lambda: reader_v14._read_epidata(filepath, timestamp, allow_r_exec=allow_r_exec),
        "eviews_wf1": lambda: reader_v14._read_eviews(filepath, timestamp,
                                                       format_type="eviews_wf1"),
        "eviews_wf2": lambda: reader_v14._read_eviews(filepath, timestamp,
                                                       format_type="eviews_wf2"),
        # v1.7 新增
        "epinfo_prj": lambda: reader_epinfo._read_epinfo(filepath, timestamp, encoding),
        "arff_arff": lambda: reader_arff._read_arff(filepath, timestamp),
        "gretl_gdt": lambda: reader_gretl._read_gdt(filepath, timestamp),
        "gretl_gdtb": lambda: _read_gretl_gdtb_hint(filepath),  # .gdtb needs Gretl export
        "tableau_hyper": lambda: reader_tableau._read_hyper(filepath, timestamp),
        "tableau_twbx": lambda: reader_tableau._read_twbx(filepath, timestamp),
        "tableau_twb": lambda: reader_tableau._read_twb(filepath, timestamp),
        # v1.10 新增
        "dbf_dbf": lambda: reader_legacy._read_dbf(filepath, timestamp),
        "access_mdb": lambda: reader_legacy._read_access(filepath, timestamp, table_name=table_name),
        "access_accdb": lambda: reader_legacy._read_access(filepath, timestamp, table_name=table_name),
        "wdx_wdx": lambda: reader_legacy._read_wdx(filepath, timestamp),
        "origin_opju": lambda: reader_legacy._read_origin(filepath, timestamp),
        "origin_oggu": lambda: reader_legacy._read_origin(filepath, timestamp),
        "sas_cport": lambda: reader_legacy._read_cport(filepath, timestamp),
        "sas_ssp": lambda: reader_legacy._read_sas_ssp(filepath, timestamp),
        "statistica_sta": lambda: reader_legacy._read_statistica(filepath, timestamp),
        "oxmetrics_in7": lambda: reader_legacy._read_oxmetrics(filepath, timestamp),
        "systat_sys": lambda: reader_legacy._read_systat(filepath, timestamp),
        "systat_syd": lambda: reader_legacy._read_systat(filepath, timestamp),
        "paradox_db": lambda: reader_legacy._read_paradox(filepath, timestamp),
        "paradox_px": lambda: reader_legacy._read_paradox(filepath, timestamp),
        "limdep_lpw": lambda: reader_legacy._read_limdep(filepath, timestamp),
        "ncss_ncss": lambda: reader_legacy._read_ncss(filepath, timestamp),
    }

    return handlers[file_format]()


def read_all_sheets(filepath: str, encoding: str | None = None) -> dict[str, StatFileResult]:
    """读入 Excel 文件的所有工作表，返回 {sheet_name: StatFileResult}。"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"文件不存在: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()
    if ext not in (".xlsx", ".xls"):
        raise ValueError(f"仅支持 Excel 文件 (.xlsx/.xls)， got: {ext}")

    from . import reader_excel

    timestamp = datetime.now().isoformat(timespec="seconds")
    results = {}

    if ext == ".xls":
        xl = pd.ExcelFile(filepath, engine="xlrd")
    else:
        xl = pd.ExcelFile(filepath, engine="openpyxl")

    sheet_names = xl.sheet_names
    if len(sheet_names) == 0:
        raise ValueError("Excel 文件不包含任何工作表")

    for name in sheet_names:
        # 跳过本技能写出的辅助工作表（_col_labels / _val_labels）
        if name.startswith("_"):
            continue
        result = reader_excel._read_excel(filepath, timestamp,
                                          format_type=f"excel_{ext[1:]}",
                                          encoding=encoding,
                                          sheet_name=name)
        results[name] = result

    return results


def read_all_r_objects(filepath: str) -> dict[str, StatFileResult]:
    """读入 RDA 文件的所有对象，返回 {object_name: StatFileResult}。"""
    from . import reader_r

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"文件不存在: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()
    if ext != ".rda":
        raise ValueError(f"仅支持 .rda 文件， got: {ext}")

    return reader_r.read_all_r_objects_inner(filepath)


# ============================================================
# 写入/转写接口
# ============================================================

def write_stat_file(dataframe, filepath, metadata=None, *, allow_r_exec: bool = False, **kwargs):
    """
    Write DataFrame to specified format file.

    Auto-selects writer based on file extension, preserves variable labels, value labels etc.

    Parameters
    ----------
    dataframe : pd.DataFrame
    filepath : str
        Output file path (extension determines format)
    metadata : dict, optional
        Metadata (variable_labels, value_labels etc.)
    allow_r_exec : bool, default False
        Gate for R-interpreter-backed writes (.rda/.rds). Disabled by default;
        pass True only on a TRUSTED file/environment.
    **kwargs
        Additional arguments passed to the underlying writer

    Supported formats: .sav, .zsav, .dta, .rda, .rds, .xlsx, .xpt, .csv, .tsv,
    .parquet, .hdf5, .feather, .json
    """
    from .writer import write_stat_file as _writer
    return _writer(dataframe, filepath, metadata, allow_r_exec=allow_r_exec, **kwargs)


def convert_stat_file(src_path, dst_path, *, metadata=None, **kwargs):
    """
    One-step: read source file and convert to target format.
    
    Parameters
    ----------
    src_path : str
    dst_path : str
    metadata : dict, optional
    **kwargs
        Additional arguments passed to write_stat_file
    
    Returns
    -------
    dict
        {"src_format", "dst_format", "rows", "columns", "warnings"}
    """
    from .writer import convert_stat_file as _converter
    return _converter(src_path, dst_path, metadata=metadata, **kwargs)