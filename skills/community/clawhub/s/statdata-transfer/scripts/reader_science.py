"""
reader_science.py - 科学计算格式（MATLAB/HDF5/Parquet/Feather/ORC/FST）
自动从 stat_reader.py 拆分生成
"""

from __future__ import annotations
import os
import json
import shutil
import subprocess
import tempfile
from datetime import datetime
from typing import Any

import h5py
import numpy as np
import pandas as pd

from .reader_core import (ColumnInfo, MatlabMeta, Hdf5Meta, ParquetMeta, FeatherMeta, OrcMeta, StatFileResult, _bilingual, _calc_missing_pct, _get_source_type, _parse_value_labels, _build_column_report)


# ============================================================
# 科学计算格式（MATLAB/HDF5/Parquet/Feather/ORC/FST）
# ============================================================

def _extract_full_meta(custom_meta: dict) -> dict:
    """从 custom_meta dict 中提取完整元数据，支持新旧两种格式。
    
    优先解析 stat-full-meta（新格式，17 字段），否则回退到
    stat-var-labels / stat-val-labels 旧格式。
    返回要 merge 到最终 metadata 的 dict。
    """
    full_meta_from_embed = {}
    var_labels: dict = {}
    val_labels: dict = {}
    if "stat-full-meta" in custom_meta:
        try:
            from .reader_core import restore_full_meta
            full_meta_from_embed = restore_full_meta(json.loads(custom_meta["stat-full-meta"]))
        except Exception:
            pass
    elif "stat-var-labels" in custom_meta:
        try:
            var_labels = json.loads(custom_meta["stat-var-labels"])
        except Exception:
            pass
        if "stat-val-labels" in custom_meta:
            try:
                val_raw = json.loads(custom_meta["stat-val-labels"])
                val_labels = _parse_value_labels(val_raw)
            except Exception:
                pass
    if var_labels:
        full_meta_from_embed["variable_labels"] = var_labels
    if val_labels:
        full_meta_from_embed["value_labels"] = val_labels
    return full_meta_from_embed


# 常见「变量标签」属性名（HDF5 数据集/组上用于存储列说明的属性键）
_LABEL_ATTR_KEYS = (
    "variable_label", "label", "var_label", "LABEL",
    "description", "DESCRIPTION", "column_label", "columnLabel",
    "units", "UNITS",
)


def _build_df_from_datasets(datasets: dict, include_non_numeric: bool = True) -> tuple:
    """从 {name: ndarray} 合并为单一 DataFrame。

    - 1D 数组 → 一列
    - 2D 数组 → 按列拆为多列（name_0, name_1, ...）
    - >2D 数组 → 展平后 2D 保留（按列命名）
    - 各行对齐到最大首维，首维为 1 的 1D 数组广播为全量
    - 非数值 / 复杂类型默认跳过；include_non_numeric=True 时尝试 object 序列化
    返回 (DataFrame, skipped_keys)。
    """
    skipped: list = []
    max_len = 0
    numeric = {}
    for k, a in datasets.items():
        if not hasattr(a, "shape"):
            skipped.append(k); continue
        arr = np.asarray(a)
        if arr.dtype.kind not in "iufc" and arr.dtype.kind not in ("O", "S", "b"):
            skipped.append(k); continue
        numeric[k] = arr
        ndim = arr.ndim
        if ndim >= 1 and arr.shape[0] > max_len:
            max_len = arr.shape[0]

    if not numeric:
        return pd.DataFrame(), skipped

    out: dict = {}
    for k, a in numeric.items():
        if a.ndim == 0:
            a = np.repeat(float(a), max_len)
        if a.ndim == 1:
            if len(a) == 1 and max_len > 1:
                a = np.repeat(a, max_len)
            out[k] = a.astype(object) if a.dtype.kind == "O" else a
        elif a.ndim == 2:
            for j in range(a.shape[1]):
                out[f"{k}_{j}"] = a[:, j].astype(object) if a.dtype.kind == "O" else a[:, j]
        else:
            arr2 = a.reshape(a.shape[0], -1)
            for j in range(arr2.shape[1]):
                out[f"{k}_{j}"] = arr2[:, j]
    return pd.DataFrame(out), skipped


def _collect_attr_labels(f) -> dict:
    """扫描 HDF5 文件顶层 dataset/group 的属性，按名称映射出变量标签。

    仅当数据集/组的 base 名与 DataFrame 列名一致时才匹配（见 _read_hdf5 调用处）。
    """
    found: dict = {}

    def _scan(name, obj):
        if isinstance(obj, (h5py.Dataset, h5py.Group)):
            base = name.rsplit("/", 1)[-1]
            for ak in _LABEL_ATTR_KEYS:
                if ak in obj.attrs:
                    v = obj.attrs[ak]
                    if isinstance(v, bytes):
                        v = v.decode("utf-8", errors="replace")
                    found[base] = str(v)
                    break

    f.visititems(_scan)
    return found


def _is_matlab_v73(filepath: str) -> bool:
    """检测 MATLAB 7.3 (HDF5) 格式 —— scipy.loadmat 不支持，需要 h5py 回退。"""
    try:
        with open(filepath, "rb") as fh:
            head = fh.read(128)
        return b"MATLAB 7.3" in head
    except Exception:
        return False


def _read_matlab_v73(filepath: str, timestamp: str, warnings_list: list) -> StatFileResult:
    """MATLAB 7.3 (HDF5) 回退读取：提取顶层数值数据集为 DataFrame。

    仅做 best-effort：struct/cell/对象等复杂类型暂跳过（保留在 matlab_metadata 中）。
    """
    import h5py
    import numpy as np

    arrays: dict = {}
    skipped: list = []
    mat_variables: dict = {}
    with h5py.File(filepath, "r") as f:
        for key in f.keys():
            obj = f[key]
            if isinstance(obj, h5py.Dataset):
                arr = np.asarray(obj[()])
                if arr.dtype.kind in "iufc":  # 数值 / 复数
                    arrays[key] = arr
                    mat_variables[key] = {"type": "ndarray", "shape": list(arr.shape), "dtype": str(arr.dtype)}
                else:
                    skipped.append(key)
                    mat_variables[key] = {"type": "ndarray", "shape": list(arr.shape),
                                          "dtype": str(arr.dtype), "note": "non-numeric skipped"}
            elif isinstance(obj, h5py.Group):
                skipped.append(key)
                mat_variables[key] = {"type": "struct/cell", "note": "skipped (complex type)"}

    if not arrays:
        raise ValueError(_bilingual(
            "No numeric datasets convertible to DataFrame found in MATLAB 7.3 (HDF5) file",
            "MATLAB 7.3 (HDF5) 文件中未找到可转换为 DataFrame 的数值数据集"))

    # 以最大首维为准对齐，1D 数组广播；2D 按列拆分成多列；>2D 压平为 2D
    max_len = 0
    for a in arrays.values():
        if a.ndim >= 1:
            max_len = max(max_len, a.shape[0])
    out: dict = {}
    for k, a in arrays.items():
        if a.ndim == 1:
            out[k] = a
        elif a.ndim == 2:
            for j in range(a.shape[1]):
                out[f"{k}_{j}"] = a[:, j]
        else:
            out[k] = a.reshape(a.shape[0], -1)
    for k in list(out.keys()):
        if len(out[k]) == 1 and max_len > 1:
            out[k] = np.repeat(out[k], max_len)

    df = pd.DataFrame(out)
    used_var = next(iter(arrays.keys()), None)
    matlab_metadata: dict = {
        "file_variables": mat_variables,
        "mat_file_version": "7.3 (HDF5)",
        "selected_variable": used_var,
        "total_variables_in_file": len(mat_variables),
        "skipped_variables": skipped,
        "mat_file_header": "MATLAB 7.3 MAT-file (read via h5py fallback)",
    }
    if skipped:
        warnings_list.append(_bilingual(
            f"{len(skipped)} non-numeric/complex variables skipped in MATLAB 7.3 file, only numeric datasets kept",
            f"MATLAB 7.3 文件中 {len(skipped)} 个非数值/复杂变量已跳过（如 struct/cell），仅保留数值数据集"))
    return _finalize_matlab(df, used_var, matlab_metadata, warnings_list, timestamp)


def _finalize_matlab(df, used_var, matlab_metadata, warnings_list, timestamp) -> StatFileResult:
    column_report: dict = {}
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
        "metadata": MatlabMeta(
            file_format="matlab", collected_at=timestamp,
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
            matlab_metadata=matlab_metadata,
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }


def _read_matlab(filepath: str, timestamp: str) -> StatFileResult:
    """读入 MATLAB .mat 文件，使用 scipy.io.loadmat（v7.3 自动回退 h5py）。"""
    import scipy.io
    import numpy as np

    warnings_list = [_bilingual("MATLAB format does not contain statistical metadata like variable/value labels, only raw data values", "MATLAB 格式不含变量标签、值标签等统计元数据，仅保留原始数据值")]

    # MATLAB 7.3 (HDF5) 不被 scipy 支持 → 直接走 h5py 回退
    if _is_matlab_v73(filepath):
        warnings_list.append(_bilingual("Detected MATLAB 7.3 (HDF5) file, using h5py fallback", "检测到 MATLAB 7.3 (HDF5) 文件，使用 h5py 回退读取"))
        return _read_matlab_v73(filepath, timestamp, warnings_list)

    try:
        mat_data = scipy.io.loadmat(filepath, struct_as_record=False, squeeze_me=True)
    except (NotImplementedError, OSError) as e:
        msg = str(e)
        if "7.3" in msg or "HDF5" in msg:
            warnings_list.append(_bilingual(f"scipy cannot read this MAT file ({msg}), falling back to h5py", f"scipy 无法读取该 MAT 文件（{msg}），回退到 h5py"))
            return _read_matlab_v73(filepath, timestamp, warnings_list)
        raise
    matlab_metadata: dict[str, Any] = {
        "file_variables": {},
        "mat_file_version": None,
        "mat_file_global_variables": [],
    }

    # Extract metadata from the raw mat dict (excluding __header__, __version__, __globals__)
    data_vars = {}
    for key, value in mat_data.items():
        if key.startswith("__") and key.endswith("__"):
            if key == "__header__":
                if isinstance(value, np.ndarray):
                    matlab_metadata["mat_file_header"] = value.tobytes().decode("utf-8", errors="replace")[:200]
            elif key == "__version__":
                if isinstance(value, np.ndarray):
                    matlab_metadata["mat_file_version"] = value.tobytes().decode("utf-8", errors="replace")
            elif key == "__globals__":
                if isinstance(value, np.ndarray):
                    matlab_metadata["mat_file_global_variables"] = [str(v) for v in value]
            continue
        var_info = {
            "type": type(value).__name__,
            "shape": getattr(value, "shape", None),
        }
        if isinstance(value, np.ndarray):
            var_info["dtype"] = str(value.dtype)
        matlab_metadata["file_variables"][key] = var_info
        data_vars[key] = value

    # Try to construct a DataFrame from numeric/struct arrays
    df = pd.DataFrame()
    struct_vars = {k: v for k, v in data_vars.items()
                   if hasattr(v, 'dtype') and v.dtype.names is not None}

    if struct_vars:
        # Struct array: convert to DataFrame
        first_key = list(struct_vars.keys())[0]
        struct_arr = struct_vars[first_key]
        try:
            df = pd.DataFrame(struct_arr)
            used_var = first_key
        except Exception:
            pass
    else:
        # Try numeric arrays
        numeric_vars = {k: v for k, v in data_vars.items()
                        if isinstance(v, np.ndarray) and v.ndim <= 2 and v.dtype.kind in "iufcb"}
        if numeric_vars:
            try:
                arrays = {}
                for k, arr in numeric_vars.items():
                    if arr.ndim == 1:
                        arrays[k] = arr
                    elif arr.ndim == 2:
                        for col_idx in range(arr.shape[1]):
                            arrays[f"{k}_{col_idx}"] = arr[:, col_idx]
                if arrays:
                    max_len = max(len(a) for a in arrays.values())
                    # Broadcast 1D arrays
                    for k, arr in arrays.items():
                        if len(arr) == 1 and max_len > 1:
                            arrays[k] = np.repeat(arr, max_len)
                    df = pd.DataFrame(arrays)
                    used_var = list(numeric_vars.keys())[0]
            except Exception as e:
                warnings_list.append(_bilingual(f"MAT file numeric array conversion to DataFrame failed: {str(e)[:200]}", f"MAT 文件数值数组转换为 DataFrame 失败: {str(e)[:200]}"))

    if df.empty:
        # Fallback: grab first numeric array as single-column
        for key, value in data_vars.items():
            if isinstance(value, np.ndarray) and value.ndim <= 2:
                try:
                    flat = value.flatten()
                    df = pd.DataFrame({key: flat})
                    used_var = key
                    warnings_list.append(_bilingual(f"MAT file has complex structure, flattened variable '{key}' as single-column DataFrame", f"MAT 文件结构复杂，仅将变量 '{key}' 展平为单列 DataFrame"))
                    break
                except Exception:
                    continue

    if df.empty:
        raise ValueError(_bilingual("MAT file cannot be converted to DataFrame (may contain only non-numeric data/complex structures)", "MAT 文件无法转换为 DataFrame（可能只包含非数值数据/复杂结构）"))

    matlab_metadata["selected_variable"] = used_var
    matlab_metadata["total_variables_in_file"] = len(data_vars)

    if len(struct_vars) > 1 or len(data_vars) - len(struct_vars) > 1:
        warnings_list.append(_bilingual(f"MAT file contains {len(data_vars)} variables, selected '{used_var}' for DataFrame, remaining variable info saved in matlab_metadata.file_variables", f"MAT 文件包含 {len(data_vars)} 个变量，已选择 '{used_var}' 构造 DataFrame，其余变量信息保留在 matlab_metadata.file_variables"))

    return _finalize_matlab(df, used_var, matlab_metadata, warnings_list, timestamp)







def _read_hdf5(filepath: str, timestamp: str) -> StatFileResult:
    """读入 HDF5 文件（.h5/.hdf5），尝试使用 pd.read_hdf，并提取 stat-full-meta / stat-data-meta 属性"""
    import h5py
    
    warnings_list = []
    attr_labels: dict = {}
    hdf5_metadata: dict[str, Any] = {
        "datasets": [],
        "file_attributes": {},
        "groups": [],
        "total_datasets": 0,
        "total_groups": 0,
    }
    
    full_meta_from_embed = {}
    
    def _extract_from_attrs(attrs) -> dict:
        """从 h5py attrs 对象中提取元数据，优先 stat-full-meta"""
        if "stat-full-meta" in attrs:
            try:
                from .reader_core import restore_full_meta
                return restore_full_meta(json.loads(attrs["stat-full-meta"]))
            except Exception:
                pass
        # Fallback to old stat-data-meta
        if "stat-data-meta" in attrs:
            try:
                meta_payload = json.loads(attrs["stat-data-meta"])
                result = {}
                if "variable_labels" in meta_payload:
                    result["variable_labels"] = meta_payload["variable_labels"]
                if "value_labels" in meta_payload:
                    result["value_labels"] = _parse_value_labels(meta_payload["value_labels"])
                return result
            except Exception:
                pass
        return {}
    
    # 先尝试使用 pd.read_hdf
    try:
        df = pd.read_hdf(filepath)
        
        # 获取 h5py 元数据和标签
        with h5py.File(filepath, "r") as f:
            ds_count = 0
            for key in f.keys():
                obj = f[key]
                if isinstance(obj, h5py.Dataset):
                    ds_info = {
                        "path": key,
                        "shape": obj.shape,
                        "dtype": str(obj.dtype),
                    }
                    hdf5_metadata["datasets"].append(ds_info)
                    ds_count += 1
                elif isinstance(obj, h5py.Group):
                    hdf5_metadata["groups"].append(key)
            hdf5_metadata["total_datasets"] = ds_count
            hdf5_metadata["total_groups"] = len(hdf5_metadata["groups"])
            for attr_key, attr_val in f.attrs.items():
                if isinstance(attr_val, bytes):
                    hdf5_metadata["file_attributes"][attr_key] = attr_val.decode("utf-8", errors="replace")[:500]
                else:
                    hdf5_metadata["file_attributes"][attr_key] = str(attr_val)[:500]
            
            # 尝试从根属性读取嵌入的元数据
            full_meta_from_embed = _extract_from_attrs(f.attrs)
            # 如果没有，尝试从 dataset 属性读取
            if not full_meta_from_embed:
                for k in f.keys():
                    obj = f[k]
                    if isinstance(obj, h5py.Dataset):
                        ds_meta = _extract_from_attrs(obj.attrs)
                        if ds_meta:
                            full_meta_from_embed = ds_meta
                            break
            # 扫描顶层 dataset/group 的标签类属性，按列名还原变量标签
            attr_labels = _collect_attr_labels(f)
        
        var_labels = full_meta_from_embed.get("variable_labels", {})
        val_labels = full_meta_from_embed.get("value_labels", {})
        # 用 HDF5 属性标签补充（仅当 embed 未提供该列标签）
        for col in df.columns:
            if col not in var_labels and col in attr_labels:
                var_labels[col] = attr_labels[col]
        if any(col in attr_labels for col in df.columns):
            warnings_list.append(_bilingual(
                "Restored some variable labels from HDF5 dataset/group attributes",
                "已从 HDF5 数据集/组属性中还原部分变量标签"))

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
                format_string=None, display_width=None, storage_width=None,
                measure_level=None, alignment=None, original_type=None,
            )
        
        result = {
            "dataframe": df,
            "metadata": Hdf5Meta(
                file_format="hdf5", collected_at=timestamp,
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
                hdf5_metadata=hdf5_metadata,
            ),
            "warnings": warnings_list,
            "column_report": column_report,
        }
        # Merge all restored fields (包括 variable_labels, value_labels 等全部 17 个字段)
        result["metadata"].update({k: v for k, v in full_meta_from_embed.items() if v})
        return result
    except Exception as e:
        # 降级到 h5py 遍历模式
        warnings_list.append(_bilingual(f"pd.read_hdf failed, falling back to h5py mode: {e}", f"pd.read_hdf 失败，回退到 h5py 模式: {e}"))
    
        def _collect_datasets(name: str, obj):
            if isinstance(obj, h5py.Dataset):
                ds_info = {"path": name, "shape": obj.shape, "dtype": str(obj.dtype)}
                hdf5_metadata["datasets"].append(ds_info)
            elif isinstance(obj, h5py.Group):
                hdf5_metadata["groups"].append(name)
        
        with h5py.File(filepath, "r") as f:
            for attr_key, attr_val in f.attrs.items():
                if isinstance(attr_val, bytes):
                    hdf5_metadata["file_attributes"][attr_key] = attr_val.decode("utf-8", errors="replace")[:500]
                else:
                    hdf5_metadata["file_attributes"][attr_key] = str(attr_val)[:500]
            
            f.visititems(_collect_datasets)
        
        hdf5_metadata["total_datasets"] = len(hdf5_metadata["datasets"])
        hdf5_metadata["total_groups"] = len(hdf5_metadata["groups"])

        if not hdf5_metadata["datasets"]:
            raise ValueError(_bilingual("HDF5 file contains no Dataset", "HDF5 文件不包含任何 Dataset"))

        # 收集所有可转换的数据集，合并为单一 DataFrame（不再只取最大的那一个）
        ds_map: dict = {}
        for ds_info in hdf5_metadata["datasets"]:
            shape = ds_info.get("shape", [])
            if len(shape) > 2:
                continue
            ds_map[ds_info["path"]] = None

        if ds_map:
            with h5py.File(filepath, "r") as f:
                for path in list(ds_map.keys()):
                    try:
                        ds_map[path] = f[path][()]
                    except Exception:
                        pass

        df, ds_skipped = _build_df_from_datasets(ds_map, include_non_numeric=True)

        if df.empty:
            raise ValueError(_bilingual("HDF5 file has no Dataset convertible to DataFrame", "HDF5 文件中没有可转换为 DataFrame 的 Dataset"))

        hdf5_metadata["selected_dataset"] = "multi-merge (%d datasets)" % len([k for k, v in ds_map.items() if v is not None])

        with h5py.File(filepath, "r") as f:
            # 尝试读取嵌入的标签（先从根属性，再从 dataset 属性）
            full_meta_from_embed = _extract_from_attrs(f.attrs)
            # 扫描顶层 dataset/group 的标签类属性，按列名还原变量标签
            attr_labels = _collect_attr_labels(f)
        
        var_labels = full_meta_from_embed.get("variable_labels", {})
        val_labels = full_meta_from_embed.get("value_labels", {})
        # 用 HDF5 属性标签补充（仅当 embed 未提供该列标签）
        for col in df.columns:
            if col not in var_labels and col in attr_labels:
                var_labels[col] = attr_labels[col]
        if any(col in attr_labels for col in df.columns):
            warnings_list.append(_bilingual(
                "Restored some variable labels from HDF5 dataset/group attributes",
                "已从 HDF5 数据集/组属性中还原部分变量标签"))

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
                format_string=None, display_width=None, storage_width=None,
                measure_level=None, alignment=None, original_type=None,
            )
        
        result = {
            "dataframe": df,
            "metadata": Hdf5Meta(
                file_format="hdf5", collected_at=timestamp,
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
                hdf5_metadata=hdf5_metadata,
            ),
            "warnings": warnings_list,
            "column_report": column_report,
        }
        # Merge all restored fields (包括 variable_labels, value_labels 等全部 17 个字段)
        result["metadata"].update({k: v for k, v in full_meta_from_embed.items() if v})
        return result



def _read_parquet(filepath: str, timestamp: str) -> StatFileResult:
    """读入 Parquet 文件，使用 pyarrow.parquet.read_table。目录则按分区数据集读取。"""
    # 分区 Parquet 目录（含 part-*.parquet / Hive 分区子目录）
    if os.path.isdir(filepath):
        return _read_parquet_partitioned(filepath, timestamp)

    import pyarrow.parquet as pq

    warnings_list = []
    parquet_metadata: dict[str, Any] = {}

    pf = pq.ParquetFile(filepath)
    meta = pf.metadata
    parquet_metadata["num_row_groups"] = meta.num_row_groups
    parquet_metadata["num_columns"] = meta.num_columns
    parquet_metadata["num_rows"] = meta.num_rows
    parquet_metadata["serialized_size"] = meta.serialized_size
    parquet_metadata["created_by"] = meta.created_by

    # Schema info
    schema = pf.schema_arrow
    parquet_metadata["schema"] = str(schema)

    # Row groups info
    rg_info_list = []
    for i in range(meta.num_row_groups):
        rg = meta.row_group(i)
        rg_info = {
            "num_rows": rg.num_rows,
            "num_columns": rg.num_columns,
            "total_byte_size": rg.total_byte_size,
        }
        # total_compressed_size 可能在某些 pyarrow 版本中不存在
        if hasattr(rg, 'total_compressed_size'):
            rg_info["total_compressed_size"] = rg.total_compressed_size
        rg_info_list.append(rg_info)
    parquet_metadata["row_groups"] = rg_info_list

    # Column info
    col_info_list = []
    for col_name in schema.names:
        col_field = schema.field(col_name)
        col_info = {
            "name": col_name,
            "type": str(col_field.type),
            "nullable": col_field.nullable,
        }
        col_info_list.append(col_info)
    parquet_metadata["columns_info"] = col_info_list

    # Read the table
    table = pq.read_table(filepath)
    df = table.to_pandas()

    # Custom metadata if any (支持新 stat-full-meta / 旧 stat-var/val-labels)
    full_meta_from_embed = {}
    if hasattr(meta, 'metadata') and meta.metadata:
        custom_meta = {}
        for k, v in meta.metadata.items():
            try:
                key_str = k.decode("utf-8") if isinstance(k, bytes) else str(k)
                val_str = v.decode("utf-8") if isinstance(v, bytes) else str(v)
            except Exception:
                continue
            custom_meta[key_str] = val_str
        if custom_meta:
            parquet_metadata["custom_metadata"] = custom_meta
            full_meta_from_embed = _extract_full_meta(custom_meta)

    if df.empty:
        warnings_list.append(_bilingual("Parquet file parsed result is empty", "Parquet 文件解析结果为空"))

    return _finalize_parquet(df, parquet_metadata, full_meta_from_embed, warnings_list, timestamp)


def _finalize_parquet(df, parquet_metadata, full_meta_from_embed, warnings_list, timestamp) -> StatFileResult:
    column_report: dict = {}
    var_labels = full_meta_from_embed.get("variable_labels", {})
    val_labels = full_meta_from_embed.get("value_labels", {})
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

    result = {
        "dataframe": df,
        "metadata": ParquetMeta(
            file_format="parquet", collected_at=timestamp,
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
            parquet_metadata=parquet_metadata,
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }
    # Merge all restored fields (包括 variable_labels, value_labels 等全部 17 个字段)
    result["metadata"].update({k: v for k, v in full_meta_from_embed.items() if v})
    return result


def _read_parquet_partitioned(filepath: str, timestamp: str) -> StatFileResult:
    """读入分区 Parquet 目录（Hive 风格 year=2020/part-*.parquet 或多 part 文件），合并为单一 DataFrame。"""
    import pyarrow.dataset as ds
    import pyarrow.parquet as pq

    warnings_list = [_bilingual(
        "Parquet partitioned directory: merged all part files via pyarrow.dataset",
        "Parquet 分区目录：已用 pyarrow.dataset 合并读取全部 part 文件")]

    try:
        dataset = ds.dataset(filepath, format="parquet", partitioning="hive")
    except Exception:
        dataset = ds.dataset(filepath, format="parquet")

    table = dataset.to_table()
    df = table.to_pandas()

    parquet_metadata: dict = {
        "partitioned": True,
        "num_files": len(dataset.files),
        "files": dataset.files,
        "num_rows": table.num_rows,
        "num_columns": table.num_columns,
        "partition_keys": dataset.partitioning.schema.names if dataset.partitioning is not None else [],
    }
    parquet_metadata["schema"] = str(table.schema)

    # 自定义元数据（优先取首个文件，或从合并后 schema.metadata）
    full_meta_from_embed = {}
    custom_meta = {}
    if hasattr(table.schema, "metadata") and table.schema.metadata:
        for k, v in table.schema.metadata.items():
            try:
                key_str = k.decode("utf-8") if isinstance(k, bytes) else str(k)
                val_str = v.decode("utf-8") if isinstance(v, bytes) else str(v)
            except Exception:
                continue
            custom_meta[key_str] = val_str
        if custom_meta:
            parquet_metadata["custom_metadata"] = custom_meta
            full_meta_from_embed = _extract_full_meta(custom_meta)
    else:
        # 退而从首个 part 文件读取 schema 级自定义元数据
        try:
            pf = pq.ParquetFile(dataset.files[0])
            meta = pf.metadata
            if hasattr(meta, "metadata") and meta.metadata:
                cm = {}
                for k, v in meta.metadata.items():
                    try:
                        cm[k.decode("utf-8") if isinstance(k, bytes) else str(k)] = v.decode("utf-8") if isinstance(v, bytes) else str(v)
                    except Exception:
                        continue
                if cm:
                    parquet_metadata["custom_metadata"] = cm
                    full_meta_from_embed = _extract_full_meta(cm)
        except Exception:
            pass

    if df.empty:
        warnings_list.append(_bilingual("Parquet partitioned directory parsed result is empty", "Parquet 分区目录解析结果为空"))

    return _finalize_parquet(df, parquet_metadata, full_meta_from_embed, warnings_list, timestamp)



def _read_feather(filepath: str, timestamp: str) -> StatFileResult:
    """读入 Feather 文件（.feather/.arrow），使用 pyarrow.feather.read_table。
    支持从 schema.metadata 中提取变量标签和值标签。"""
    import pyarrow.feather as ft
    
    warnings_list = []
    feather_metadata: dict[str, Any] = {}
    
    # Read the table
    table = ft.read_table(filepath)
    df = table.to_pandas()
    
    # Metadata from the table
    schema = table.schema
    feather_metadata["schema"] = str(schema)
    feather_metadata["num_rows"] = table.num_rows
    feather_metadata["num_columns"] = table.num_columns
    
    # Column info
    col_info_list = []
    for col_name in schema.names:
        col_field = schema.field(col_name)
        col_info = {
            "name": col_name,
            "type": str(col_field.type),
            "nullable": col_field.nullable,
        }
        col_info_list.append(col_info)
    feather_metadata["columns_info"] = col_info_list
    
    # Custom metadata from table metadata (pyarrow API compatibility)
    full_meta_from_embed = {}
    custom_meta = {}
    if hasattr(table.schema, 'metadata') and table.schema.metadata:
        for k, v in table.schema.metadata.items():
            try:
                key_str = k.decode("utf-8") if isinstance(k, bytes) else str(k)
                val_str = v.decode("utf-8") if isinstance(v, bytes) else str(v)
                custom_meta[key_str] = val_str
            except Exception:
                pass
        full_meta_from_embed = _extract_full_meta(custom_meta)

    if custom_meta:
        feather_metadata["custom_metadata"] = custom_meta

    column_report: dict[str, ColumnInfo] = {}
    var_labels = full_meta_from_embed.get("variable_labels", {})
    val_labels = full_meta_from_embed.get("value_labels", {})
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

    result = {
        "dataframe": df,
        "metadata": FeatherMeta(
            file_format="feather", collected_at=timestamp,
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
            feather_metadata=feather_metadata,
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }
    # Merge all restored fields (包括 variable_labels, value_labels 等全部 17 个字段)
    result["metadata"].update({k: v for k, v in full_meta_from_embed.items() if v})
    return result



def _read_orc(filepath: str, timestamp: str) -> StatFileResult:
    """读入 ORC 文件，使用 pyarrow.orc.read_table。"""
    import pyarrow.orc as orc_reader

    warnings_list = []
    orc_metadata: dict[str, Any] = {}

    # Read the table
    table = orc_reader.read_table(filepath)
    df = table.to_pandas()

    schema = table.schema
    orc_metadata["schema"] = str(schema)
    orc_metadata["num_rows"] = table.num_rows
    orc_metadata["num_columns"] = table.num_columns

    # Column info
    col_info_list = []
    for col_name in schema.names:
        col_field = schema.field(col_name)
        col_info = {
            "name": col_name,
            "type": str(col_field.type),
            "nullable": col_field.nullable,
        }
        col_info_list.append(col_info)
    orc_metadata["columns_info"] = col_info_list

    # Custom metadata (支持新 stat-full-meta / 旧 stat-var/val-labels)
    full_meta_from_embed = {}
    if hasattr(table, "metadata") and table.metadata:
        custom_meta = {}
        for k, v in table.metadata.items():
            try:
                custom_meta[k.decode("utf-8")] = v.decode("utf-8")
            except Exception:
                try:
                    custom_meta[str(k)] = str(v)
                except Exception:
                    pass
        if custom_meta:
            orc_metadata["custom_metadata"] = custom_meta
            full_meta_from_embed = _extract_full_meta(custom_meta)

    column_report: dict[str, ColumnInfo] = {}
    var_labels = full_meta_from_embed.get("variable_labels", {})
    val_labels = full_meta_from_embed.get("value_labels", {})
    for col in df.columns:
        column_report[col] = ColumnInfo(
            source_type=_get_source_type(df[col]),
            pandas_dtype=str(df[col].dtype),
            original_label=var_labels.get(col),
            has_value_labels=bool(val_labels.get(col)),
            n_missing=int(df[col].isnull().sum()),
            missing_are_special=False,
            precision_warning=False,
            format_string=None, display_width=None, storage_width=None,
            measure_level=None, alignment=None, original_type=None,
        )
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                column_report[col]["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")

    result = {
        "dataframe": df,
        "metadata": OrcMeta(
            file_format="orc", collected_at=timestamp,
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
            orc_metadata=orc_metadata,
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }
    # Merge all restored fields (包括 variable_labels, value_labels 等全部 17 个字段)
    result["metadata"].update({k: v for k, v in full_meta_from_embed.items() if v})
    return result



def _read_fst(filepath: str, timestamp: str) -> StatFileResult:
    """FST (R fst package) 是专有压缩列式格式，pyarrow.feather 无法解析。

    若确有 .fst 转换需求，请用 R 桥接：install.packages("fst"); fst::read_fst("in.fst", "out.csv")，
    然后读取 .csv；或直接联系作者加装 fst Python 解析库。
    """
    ext = os.path.splitext(filepath)[1].lower()
    raise RuntimeError(
        _bilingual(
            f"Direct reading of R {ext} (fst package) is not yet supported.\n"
            f"R's fst format is a proprietary compressed columnar format incompatible with Arrow IPC / Feather.\n"
            f"Workaround: in R, run `install.packages('fst'); fst::read_fst('{filepath}', 'out.csv')` then read the CSV.",
            f"暂不支持直接读取 R {ext} (fst 包格式)。\n"
            f"R 的 fst 格式是有损专有压缩列式格式，与 Arrow IPC / Feathers 不兼容。\n"
            f"折中方案：在 R 中运行 `install.packages('fst'); fst::read_fst('{filepath}', 'out.csv')`，然后读取 CSV。",
        )
    )

    # Column info
    col_info_list = []
    for col_name in schema.names:
        col_field = schema.field(col_name)
        col_info = {
            "name": col_name,
            "type": str(col_field.type),
            "nullable": col_field.nullable,
        }
        col_info_list.append(col_info)
    fst_metadata["columns_info"] = col_info_list

    # Custom metadata (支持新 stat-full-meta / 旧 stat-var/val-labels)
    full_meta_from_embed = {}
    if hasattr(table, "metadata") and table.metadata:
        custom_meta = {}
        for k, v in table.metadata.items():
            try:
                custom_meta[k.decode("utf-8")] = v.decode("utf-8")
            except Exception:
                try:
                    custom_meta[str(k)] = str(v)
                except Exception:
                    pass
        if custom_meta:
            fst_metadata["custom_metadata"] = custom_meta
            full_meta_from_embed = _extract_full_meta(custom_meta)

    column_report: dict[str, ColumnInfo] = {}
    var_labels = full_meta_from_embed.get("variable_labels", {})
    val_labels = full_meta_from_embed.get("value_labels", {})
    for col in df.columns:
        column_report[col] = ColumnInfo(
            source_type=_get_source_type(df[col]),
            pandas_dtype=str(df[col].dtype),
            original_label=var_labels.get(col),
            has_value_labels=bool(val_labels.get(col)),
            n_missing=int(df[col].isnull().sum()),
            missing_are_special=False,
            precision_warning=False,
            format_string=None, display_width=None, storage_width=None,
            measure_level=None, alignment=None, original_type=None,
        )
        if pd.api.types.is_numeric_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            max_val = df[col].abs().max()
            if pd.notna(max_val) and max_val > 1e15:
                column_report[col]["precision_warning"] = True
                warnings_list.append(f"列 '{col}' 包含 >1e15 的数值，float64 精度可能不足 | Column '{col}' contains values >1e15, float64 precision may be insufficient")

    result = {
        "dataframe": df,
        "metadata": FstMeta(
            file_format="fst", collected_at=timestamp,
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
            fst_metadata=fst_metadata,
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }
    # Merge all restored fields (包括 variable_labels, value_labels 等全部 17 个字段)
    result["metadata"].update({k: v for k, v in full_meta_from_embed.items() if v})
    return result


