"""
writer.py - 数据导出模块
将 DataFrame + 元数据转写为各类统计/数据格式

支持的格式：SPSS (.sav/.zsav), Stata (.dta), R (.rda/.rds), Excel (.xlsx/.xls),
SAS XPT (.xpt), CSV (.csv), TSV (.tsv), Parquet (.parquet), HDF5 (.h5/.hdf5),
JSON (.json), Feather (.feather)
"""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from typing import Any

import pandas as pd
import pyarrow as pa

from .reader_core import _bilingual


# ============================================================
# 辅助函数
# ============================================================

def _get_variable_labels(metadata: dict) -> dict[str, str]:
    if not metadata:
        return {}
    return metadata.get("variable_labels", {})


def _get_value_labels(metadata: dict) -> dict[str, dict]:
    if not metadata:
        return {}
    return metadata.get("value_labels", {})


def _get_missing_ranges(metadata: dict) -> dict:
    """提取 missing_ranges 元数据，转换为 write_sav 格式。
    
    返回格式：{"varname": [{"lo": x, "hi": y}]}
    """
    if not metadata:
        return {}
    ranges = metadata.get("missing_ranges", {})
    if not isinstance(ranges, dict):
        return {}
    return {k: v for k, v in ranges.items() if isinstance(v, list) and v}


def _get_missing_user_values(metadata: dict) -> dict:
    """提取 missing_user_values 元数据。
    
    对于 Stata：应是 {"varname": ["a", "b", "c"]}（小写字母列表）
    对于 SPSS：应是 {"varname": [-99, -98]}
    """
    if not metadata:
        return {}
    vals = metadata.get("missing_user_values", {})
    if not isinstance(vals, dict):
        return {}
    return {k: v for k, v in vals.items() if isinstance(v, (list, tuple))}


def _build_full_meta(metadata: dict) -> dict:
    """从 metadata dict 中提取全部 17 个核心字段，用于嵌入到非统计格式中"""
    if not metadata:
        return {}
    
    fields = [
        "variable_labels", "value_labels", "special_missing",
        "variable_display_width", "variable_storage_width",
        "variable_measure", "variable_alignment",
        "missing_ranges", "missing_user_values",
        "date_origin", "file_encoding", "file_label",
        "creation_time", "notes", "original_variable_types",
        "column_names_to_labels", "mr_sets",
    ]
    full_meta = {}
    for field in fields:
        val = metadata.get(field)
        if val:  # 只保存非空字段
            full_meta[field] = val
    return full_meta


# 核心字段名常量（供 reader 端解析）
STAT_FULL_META_KEY = "stat-full-meta"  # 单一 key 存储全部 17 个字段的 JSON
STAT_META_VERSION = "1.0"


def _pyreadstat_value_labels(val_labels: dict, columns: list) -> dict | None:
    """将值标签转换为 pyreadstat 接受的格式 {varname: {value: label}}"""
    result = {}
    for varname, labels_dict in val_labels.items():
        if varname in columns:
            lab_dict = {}
            for val, lab in labels_dict.items():
                if isinstance(val, str) and not val.startswith("_"):
                    try:
                        val = int(val)
                    except ValueError:
                        try:
                            val = float(val)
                        except ValueError:
                            continue
                if isinstance(val, (int, float)):
                    lab_dict[val] = str(lab)
            if lab_dict:
                result[varname] = lab_dict
    return result if result else None


def _label_limit_warnings(metadata: dict, var_label_limit: int,
                          value_label_name_limit: int = 0,
                          by_bytes: bool = True) -> list:
    """检查变量标签 / 值标签是否超过目标格式上限。

    返回告警列表（双语）。若未超上限则返回空列表。
    目的：目标格式（SPSS 255 字节、Stata 变量标签 80 字符等）会在写入时
    **静默截断**标签，导致无声数据丢失；此处显式告警，让用户知情。

    Parameters
    ----------
    var_label_limit : 上限值
    by_bytes : True 按 UTF-8 字节计（SPSS）；False 按字符计（Stata）
    """
    if not metadata:
        return []
    warnings = []
    var_labels = _get_variable_labels(metadata)
    for col, lab in var_labels.items():
        if not lab:
            continue
        s = str(lab)
        n = len(s.encode("utf-8", "ignore")) if by_bytes else len(s)
        unit = "字节" if by_bytes else "字符"
        if n > var_label_limit:
            warnings.append(_bilingual(
                f"变量 '{col}' 的变量标签为 {n} {unit}，超过 {var_label_limit} {unit}上限，"
                f"写入时将被静默截断 | Variable label for '{col}' is {n} {unit}, exceeds "
                f"{var_label_limit}-{unit} limit and will be silently truncated on write",
                f"变量 '{col}' 的变量标签为 {n} {unit}，超过 {var_label_limit} {unit}上限，写入时将被静默截断",
            ))
    val_labels = _get_value_labels(metadata)
    for col, mapping in val_labels.items():
        if value_label_name_limit and len(str(col)) > value_label_name_limit:
            warnings.append(_bilingual(
                f"值标签名 '{col}' 长度为 {len(str(col))}，超过 Stata {value_label_name_limit} 字符上限，"
                f"将被静默截断 | Value-label name '{col}' exceeds Stata {value_label_name_limit}-char limit",
                f"值标签名 '{col}' 长度为 {len(str(col))}，超过 Stata {value_label_name_limit} 字符上限，将被静默截断",
            ))
    return warnings


def _try_stata_version(version: int) -> int:
    """检查 pyreadstat 是否支持指定的 Stata 版本"""
    try:
        import pyreadstat
        # pyreadstat 1.3.5 支持版本 13, 14, 15
        supported = [13, 14, 15]
        if version in supported:
            return version
        return 15
    except Exception:
        return 15


# ============================================================
# SPSS .sav 写入
# ============================================================

def _check_non_stat_target_loss(metadata):
    """Check metadata loss when writing to non-statistical formats | 检查写出到非统计格式时的元数据丢失"""
    warnings = []
    if metadata.get("special_missing"):
        warnings.append(f"目标格式不保存 special_missing | Target format does not save special_missing ({len(metadata['special_missing'])} vars lost)")
    if metadata.get("variable_display_width"):
        non_empty = {k:v for k,v in metadata["variable_display_width"].items() if v}
        if non_empty:
            warnings.append(f"目标格式不保存 variable_display_width | Target format does not save variable_display_width ({len(non_empty)} vars lost)")
    if metadata.get("variable_storage_width"):
        non_empty = {k:v for k,v in metadata["variable_storage_width"].items() if v}
        if non_empty:
            warnings.append(f"目标格式不保存 variable_storage_width | Target format does not save variable_storage_width ({len(non_empty)} vars lost)")
    if metadata.get("variable_measure"):
        non_empty = {k:v for k,v in metadata["variable_measure"].items() if v}
        if non_empty:
            warnings.append(f"目标格式不保存 variable_measure | Target format does not save variable_measure ({len(non_empty)} vars lost)")
    if metadata.get("variable_alignment"):
        non_empty = {k:v for k,v in metadata["variable_alignment"].items() if v}
        if non_empty:
            warnings.append(f"目标格式不保存 variable_alignment | Target format does not save variable_alignment ({len(non_empty)} vars lost)")
    if metadata.get("missing_ranges"):
        warnings.append(f"目标格式不保存 missing_ranges | Target format does not save missing_ranges ({len(metadata['missing_ranges'])} vars lost)")
    if metadata.get("missing_user_values"):
        warnings.append(f"目标格式不保存 missing_user_values | Target format does not save missing_user_values ({len(metadata['missing_user_values'])} vars lost)")
    if metadata.get("mr_sets"):
        warnings.append(f"目标格式不保存 mr_sets | Target format does not save mr_sets ({len(metadata['mr_sets'])} sets lost)")
    if metadata.get("date_origin"):
        warnings.append(f"目标格式不保存 date_origin | Target format does not save date_origin (date baseline lost)")
    if metadata.get("file_encoding"):
        warnings.append(f"目标格式不保存 file_encoding | Target format does not save file_encoding")
    if metadata.get("file_label"):
        warnings.append(f"目标格式不保存 file_label | Target format does not save file_label")
    if metadata.get("notes"):
        non_empty = [n for n in metadata["notes"] if n]
        if non_empty:
            warnings.append(f"目标格式不保存 notes | Target format does not save notes ({len(non_empty)} notes lost)")
    if metadata.get("original_variable_types"):
        non_empty = {k:v for k,v in metadata["original_variable_types"].items() if v}
        if non_empty:
            warnings.append(f"目标格式不保存 original_variable_types | Target format does not save original_variable_types ({len(non_empty)} vars lost)")
    return warnings


def _write_sav(df, filepath, metadata=None, *, compress_zsav=False):
    """写入 SPSS .sav / .zsav 格式
    
    pyreadstat 1.3.5 write_sav 支持 missing_ranges 参数。
    SPSS 用户自定义缺失值通过 missing_ranges 写出。
    """
    import pyreadstat
    
    var_labels = _get_variable_labels(metadata)
    val_labels = _get_value_labels(metadata)
    
    column_labels = [var_labels.get(col, col) for col in df.columns]
    variable_value_labels = _pyreadstat_value_labels(val_labels, list(df.columns))
    file_label = metadata.get("file_label", "") if metadata else ""
    
    # 提取缺失值范围（SPSS 使用 missing_ranges 参数）
    missing_ranges = _get_missing_ranges(metadata)
    
    kwargs_write = dict(
        column_labels=column_labels,
        variable_value_labels=variable_value_labels,
        file_label=file_label if file_label else None,
    )
    
    if missing_ranges:
        kwargs_write["missing_ranges"] = missing_ranges
    
    # pyreadstat 1.3.5 不支持 write_zsav / read_zsav，降级为 .sav
    if compress_zsav:
        try:
            if hasattr(pyreadstat, 'write_zsav'):
                write_fn = pyreadstat.write_zsav
            else:
                compress_zsav = False
                write_fn = pyreadstat.write_sav
        except Exception:
            compress_zsav = False
            write_fn = pyreadstat.write_sav
    else:
        write_fn = pyreadstat.write_sav
    
    write_fn(
        df, filepath,
        **kwargs_write,
    )

    # SPSS 变量标签上限 255 字节，超限会被 pyreadstat 静默截断；显式告警避免无声数据丢失
    warnings = _label_limit_warnings(metadata, var_label_limit=255, by_bytes=True)
    return warnings


# ============================================================
# Stata .dta 写入
# ============================================================

def _write_stata(df, filepath, metadata=None, *, version=15):
    """写入 Stata .dta 格式
    
    支持的元数据参数：
    - missing_user_values: {"varname": ["a", "b"]}（小写字母）
    - missing_ranges: {"varname": [{"lo": x, "hi": y}]}
    """
    import pyreadstat
    
    # 调整版本
    version = _try_stata_version(version)
    
    var_labels = _get_variable_labels(metadata)
    val_labels = _get_value_labels(metadata)
    
    column_labels = [var_labels.get(col, col) for col in df.columns]
    variable_value_labels = _pyreadstat_value_labels(val_labels, list(df.columns))
    file_label = metadata.get("file_label", "") if metadata else ""
    if file_label and len(file_label) > 80:
        file_label = file_label[:80]
    
    # 恢复 Stata 特殊缺失值定义
    missing_user_values = _get_missing_user_values(metadata)
    
    # 从 DataFrame 自动检测字符 'a'-'z' 标签
    if not missing_user_values:
        missing_user_values = {}
    
    for col in df.columns:
        if df[col].dtype == object:
            char_tags = set()
            for val in df[col].dropna():
                if isinstance(val, str) and len(val) == 1 and 'a' <= val <= 'z':
                    char_tags.add(val)
            if char_tags:
                existing = set(missing_user_values.get(col, []))
                missing_user_values[col] = sorted(existing | char_tags)
    
    kwargs_write = dict(
        version=version,
        column_labels=column_labels,
        variable_value_labels=variable_value_labels,
        file_label=file_label if file_label else None,
    )
    
    if missing_user_values:
        kwargs_write["missing_user_values"] = missing_user_values
    
    pyreadstat.write_dta(
        df, filepath,
        **kwargs_write,
    )

    # Stata 变量标签上限 80 字符、值标签名上限 32 字符，超限会被静默截断；显式告警
    warnings = _label_limit_warnings(metadata, var_label_limit=80,
                                     value_label_name_limit=32, by_bytes=False)
    return warnings


# ============================================================
# R .rda / .rds 写入（通过 R subprocess）
# ============================================================



# ============================================================
# 安全辅助：以「写临时 .R 脚本 + 命令行参数」方式运行 R
# 与 reader_r.py / reader_v14.py 的 _run_r_script 保持一致模式（消除命令注入）。
# ============================================================
def _run_r_script(rscript_path, script_body, *args, timeout=120):
    """将**完全静态**的 R 脚本写入临时文件，用 `Rscript script.R <args...>` 运行。

    安全要点：脚本体不得内插任何不可信输入（文件路径、标签、元数据等），
    所有动态值通过命令行参数 (R 内 commandArgs(trailingOnly=TRUE)) 传入，
    从而消除把用户输入拼进可执行 R 代码造成的命令注入风险。
    """
    fd, script_path = tempfile.mkstemp(suffix=".R", prefix="statdata_r_")
    os.close(fd)
    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_body)
        cmd = [rscript_path, script_path] + [str(a) for a in args]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace",
        )
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass
    return result


# 静态 R 脚本：经 argv 接收 csv 路径 / 输出路径 / save_func / 标签JSON / 元数据JSON，
# 用 jsonlite 解析后把标签作为数据（非代码）赋给各列，绝不内插用户输入。
_R_WRITE_SCRIPT = r"""
args <- commandArgs(trailingOnly=TRUE)
csv_path <- args[1]
out_path <- args[2]
save_func <- args[3]
labels_json <- args[4]
full_meta_json <- args[5]
library(jsonlite)
df <- read.csv(csv_path, stringsAsFactors=FALSE, fileEncoding='UTF-8')
lab <- fromJSON(labels_json, simplifyVector=FALSE)
if (!is.null(lab$var_labels)) {
  for (col in names(lab$var_labels)) {
    if (col %in% names(df)) {
      v <- lab$var_labels[[col]]
      if (!is.null(v) && length(v) > 0) { attr(df[[col]], "label") <- as.character(v) }
    }
  }
}
if (!is.null(lab$val_labels)) {
  for (col in names(lab$val_labels)) {
    if (col %in% names(df)) {
      lv <- lab$val_labels[[col]]
      if (!is.null(lv) && length(lv) > 0) {
        attr(df[[col]], "labels") <- unlist(lv, use.names=TRUE)
        class(df[[col]]) <- c("labelled", "integer")
      }
    }
  }
}
if (nchar(full_meta_json) > 0) { attr(df, "statdata_meta") <- full_meta_json }
if (save_func == "saveRDS") { saveRDS(df, out_path) } else { save(df, file=out_path) }
"""
def _write_r_via_subprocess(df, filepath, metadata=None, object_name="df", save_func="save", allow_r_exec: bool = False):
    """通过 R subprocess 写入 R 格式文件，并将全部 17 个元数据字段保存为 R 数据属性"""
    from .reader_r import _check_r_available
    
    r_exe = _check_r_available()
    if not r_exe:
        raise RuntimeError(_bilingual("R is not installed, cannot write R format file. Please configure R environment first.", "R 未安装，无法写入 R 格式文件。请先配置 R 环境。"))
    if not allow_r_exec:
        raise RuntimeError(
            "Writing R format files requires invoking the local R interpreter (saveRDS/save), "
            "which is disabled by default for security (R can execute embedded code). "
            "If you trust the environment, retry with allow_r_exec=True.\n"
            "写入 R 格式文件需调用本地 R 解释器（saveRDS/save），出于安全默认禁用"
            "（R 可能执行嵌入代码）。若信任环境，请使用 allow_r_exec=True 重试。"
        )
    
    filepath_fwd = filepath.replace("\\", "/")
    tmp_csv = tempfile.NamedTemporaryFile(suffix='.csv', delete=False, mode='w', encoding='utf-8')
    tmp_csv.close()

    try:
        df.to_csv(tmp_csv.name, index=False, encoding='utf-8')
        csv_fwd = tmp_csv.name.replace("\\", "/")

        var_labels = _get_variable_labels(metadata)
        val_labels = _get_value_labels(metadata)
        full_meta = _build_full_meta(metadata)

        # 将所有用户派生字符串打包为 JSON，经 argv 传入 R（避免把用户输入内插进 R 代码造成注入）
        labels_payload = json.dumps(
            {"var_labels": var_labels, "val_labels": val_labels},
            ensure_ascii=False,
        )
        full_meta_json = json.dumps(full_meta, ensure_ascii=False) if full_meta else ""

        result = _run_r_script(
            r_exe, _R_WRITE_SCRIPT,
            csv_fwd, filepath_fwd, save_func, labels_payload, full_meta_json,
        )
        if result.returncode != 0:
            err = result.stderr.strip()
            raise RuntimeError(_bilingual(f"R write failed: {err}", f"R 写入失败: {err}"))
    
    except Exception as e:
        if isinstance(e, RuntimeError):
            raise
        raise RuntimeError(_bilingual(f"R write failed: {e}", f"R 写入失败: {e}"))
    
    finally:
        if os.path.exists(tmp_csv.name):
            os.unlink(tmp_csv.name)


def _write_rda(df, filepath, metadata=None, *, object_name="df", allow_r_exec: bool = False):
    """写入 R .rda 格式"""
    _write_r_via_subprocess(df, filepath, metadata, object_name, "save", allow_r_exec=allow_r_exec)


def _write_rds(df, filepath, metadata=None, *, allow_r_exec: bool = False):
    """写入 R .rds 格式"""
    _write_r_via_subprocess(df, filepath, metadata, "df", "saveRDS", allow_r_exec=allow_r_exec)


# ============================================================
# Excel .xlsx 写入
# ============================================================

def _write_excel(df, filepath, metadata=None, *, engine="openpyxl"):
    """写入 Excel 并附加标签工作表，返回元数据丢失警告"""
    warnings = []
    
    # Excel 需要检查是否有丢失的元数据
    if metadata:
        lost_fields = _check_excel_metadata_loss(metadata)
        warnings.extend(lost_fields)
    
    with pd.ExcelWriter(filepath, engine=engine) as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
        
        if metadata:
            var_labels = _get_variable_labels(metadata)
            val_labels = _get_value_labels(metadata)
            
            meta_rows = []
            for col in df.columns:
                meta_rows.append({"Column": col, "Label": var_labels.get(col, "")})
            if meta_rows:
                pd.DataFrame(meta_rows).to_excel(writer, index=False, sheet_name="_col_labels")
            
            vl_rows = []
            for var, labels_dict in val_labels.items():
                for val, lab in labels_dict.items():
                    vl_rows.append({"Variable": var, "Value": val, "Label": lab})
            if vl_rows:
                pd.DataFrame(vl_rows).to_excel(writer, index=False, sheet_name="_val_labels")
    
    return warnings


def _check_excel_metadata_loss(metadata):
    """检查哪些 Excel 格式无法保存"""
    warnings = []
    if metadata.get("special_missing"):
        warnings.append(f"Excel 不保存 special_missing（{len(metadata['special_missing'])} 个变量丢失） | Excel does not save special_missing ({len(metadata['special_missing'])} vars lost)")
    if metadata.get("variable_display_width"):
        non_empty = {k:v for k,v in metadata["variable_display_width"].items() if v}
        if non_empty:
            warnings.append(f"Excel 不保存 variable_display_width（{len(non_empty)} 个变量丢失） | Excel does not save variable_display_width ({len(non_empty)} vars lost)")
    if metadata.get("variable_measure"):
        non_empty = {k:v for k,v in metadata["variable_measure"].items() if v}
        if non_empty:
            warnings.append(f"Excel 不保存 variable_measure（{len(non_empty)} 个变量丢失） | Excel does not save variable_measure ({len(non_empty)} vars lost)")
    if metadata.get("variable_alignment"):
        non_empty = {k:v for k,v in metadata["variable_alignment"].items() if v}
        if non_empty:
            warnings.append(f"Excel 不保存 variable_alignment（{len(non_empty)} 个变量丢失） | Excel does not save variable_alignment ({len(non_empty)} vars lost)")
    return warnings


def _write_xls(df, filepath, metadata=None):
    """写入旧版 Excel .xls（最多 65536 行）"""
    _write_excel(df, filepath, metadata, engine="xlwt")


# ============================================================
# SAS XPT 写入
# ============================================================

def _write_xpt(df, filepath, metadata=None):
    """写入 SAS XPORT (.xpt) 格式
    
    注意：XPT 格式不支持 special_missing 和 mr_sets，写出时会丢失。
    这些元数据会被保存到 17 字段的嵌入 JSON 中供读入追溯。
    """
    import pyreadstat
    
    var_labels = _get_variable_labels(metadata)
    column_labels = [(var_labels.get(col) or col)[:40] for col in df.columns]
    val_labels = _get_value_labels(metadata)
    variable_value_labels = _pyreadstat_value_labels(val_labels, list(df.columns))
    file_label = (metadata.get("file_label", "") or "")[:40] if metadata else ""
    xpt_kwargs = {"column_labels": column_labels}
    if variable_value_labels:
        xpt_kwargs["variable_value_labels"] = variable_value_labels
    if file_label:
        xpt_kwargs["file_label"] = file_label
    pyreadstat.write_xport(df, filepath, **xpt_kwargs)
    return []


# ============================================================
# CSV / TSV 写入
# ============================================================

def _write_csv(df, filepath, metadata=None, *, encoding="utf-8-sig"):
    """写入 CSV 格式，附加全部 17 个元数据字段到 _metadata.json"""
    df.to_csv(filepath, index=False, encoding=encoding)
    
    if metadata:
        base, _ = os.path.splitext(filepath)
        meta_file = base + "_metadata.json"
        full_meta = _build_full_meta(metadata)
        if full_meta:
            full_meta["source_format"] = metadata.get("file_format", "unknown")
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(full_meta, f, ensure_ascii=False, indent=2)


def _write_tsv(df, filepath, metadata=None, *, encoding="utf-8-sig"):
    """写入 TSV 格式，附加全部 17 个元数据字段到 _metadata.json"""
    df.to_csv(filepath, index=False, sep='\t', encoding=encoding)
    
    if metadata:
        base, _ = os.path.splitext(filepath)
        meta_file = base + "_metadata.json"
        full_meta = _build_full_meta(metadata)
        if full_meta:
            full_meta["source_format"] = metadata.get("file_format", "unknown")
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(full_meta, f, ensure_ascii=False, indent=2)


# ============================================================
# Parquet 写入
# ============================================================

def _write_parquet(df, filepath, metadata=None):
    """
    写入 Parquet 格式，将全部 17 个元数据字段嵌入 schema.metadata
    可通过 read_stat_file() 无损还原
    """
    import pyarrow as pa
    import pyarrow.parquet as pq

    try:
        table = pa.Table.from_pandas(df)
    except pa.ArrowInvalid:
        # 混合类型 object 列（如数值 + 空串 '' + NaN 混存）会让 pyarrow 推断为
        # double 后遭遇空串而失败（ArrowInvalid: Could not convert '' ... to double）。
        # 回退：将全部 object 列转为 nullable string 类型后重试，避免数据丢失，
        # 同时把该列作为文本保存（空串与缺失值可同时保留）。
        df = df.copy()
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype("string")
        table = pa.Table.from_pandas(df)

    if metadata:
        full_meta = _build_full_meta(metadata)
        if full_meta:
            embed = {b"stat-full-meta": json.dumps(full_meta, ensure_ascii=False).encode("utf-8")}
            # 保留原有的 pandas schema metadata
            existing = dict(table.schema.metadata) if table.schema.metadata else {}
            existing.update(embed)
            new_schema = table.schema.with_metadata(existing)
            table = table.cast(new_schema)
    
    pq.write_table(table, filepath)


# ============================================================
# Feather 写入
# ============================================================

def _write_feather(df, filepath, metadata=None):
    """写入 Feather 格式，将全部 17 个元数据字段嵌入 schema.metadata"""
    import pyarrow.feather as ft
    
    table = pa.Table.from_pandas(df)
    
    if metadata:
        full_meta = _build_full_meta(metadata)
        if full_meta:
            embed = {b"stat-full-meta": json.dumps(full_meta, ensure_ascii=False).encode("utf-8")}
            existing = dict(table.schema.metadata) if table.schema.metadata else {}
            existing.update(embed)
            new_schema = table.schema.with_metadata(existing)
            table = table.cast(new_schema)
    
    ft.write_feather(table, filepath)


# ============================================================
# HDF5 写入
# ============================================================

def _write_hdf5(df, filepath, metadata=None, *, key="data"):
    """写入 HDF5 格式，将全部 17 个元数据字段打包为 JSON 字符串存在根属性中"""
    import h5py
    
    df.to_hdf(filepath, key=key, mode='w', format='table', index=False)
    
    if metadata:
        full_meta = _build_full_meta(metadata)
        if full_meta:
            with h5py.File(filepath, 'a') as f:
                f.attrs[STAT_FULL_META_KEY] = json.dumps(full_meta, ensure_ascii=False)


# ============================================================
# JSON 写入
# ============================================================

def _write_json(df, filepath, metadata=None, *, orient="records"):
    """写入 JSON 格式，使用 meta+data 包裹结构保留全部 17 个元数据字段"""
    output = {"data": json.loads(df.to_json(orient=orient, date_format="iso"))}
    
    if metadata:
        full_meta = _build_full_meta(metadata)
        if full_meta:
            output["meta"] = full_meta
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)


def _write_hyper_dispatch(df, filepath, metadata=None, **kwargs):
    """Write .hyper via reader_tableau (lazy import: tableauhyperapi only needed for .hyper)."""
    from . import reader_tableau
    return reader_tableau._write_hyper(df, filepath, metadata, **kwargs)


def _write_dbf_dispatch(df, filepath, metadata=None, **kwargs):
    """Write .dbf via reader_legacy (lazy import: dbf only needed for .dbf)."""
    from . import reader_legacy
    return reader_legacy._write_dbf(df, filepath, metadata, **kwargs)


# ============================================================
# 统一写入入口
# ============================================================

_SUPPORT_WRITERS = {
    ".sav": _write_sav,
    ".zsav": _write_sav,
    ".dta": _write_stata,
    ".rda": _write_rda,
    ".rds": _write_rds,
    ".xlsx": _write_excel,
    ".xls": _write_xls,
    ".xpt": _write_xpt,
    ".csv": _write_csv,
    ".tsv": _write_tsv,
    ".parquet": _write_parquet,
    ".feather": _write_feather,
    ".h5": _write_hdf5,
    ".hdf5": _write_hdf5,
    ".json": _write_json,
    ".hyper": _write_hyper_dispatch,
    ".dbf": _write_dbf_dispatch,
}


def write_stat_file(dataframe, filepath, metadata=None, **kwargs):
    """
    将 DataFrame 写入指定格式的文件
    
    Parameters
    ----------
    dataframe : pd.DataFrame
    filepath : str（目标路径，扩展名决定格式，如 .dta / .sav / .xlsx / .csv / .rda 等）
    metadata : dict, optional（含 variable_labels / value_labels 的元数据字典）
    **kwargs
        传递给底层写入函数的额外参数
        
    Raises
    ------
    ValueError
        目标格式不支持
    RuntimeError
        写入失败
    
    Warns
    -----
    warnings : list
        元数据丢失警告列表，可通过 result['warnings'] 获取
    """
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext not in _SUPPORT_WRITERS:
        supported = ", ".join(sorted(_SUPPORT_WRITERS.keys()))
        raise ValueError(_bilingual(f"Unsupported write format: {ext}\\nSupported formats: {supported}", f"不支持的写入格式: {ext}\\n支持的格式: {supported}"))
    
    writer_func = _SUPPORT_WRITERS[ext]
    
    out_dir = os.path.dirname(filepath)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    
    # 传递 compress_zsav 参数给 zsav
    if ext == ".zsav":
        kwargs["compress_zsav"] = True

    # 捕获 R 执行闸门：仅 R 格式（.rda/.rds）writer 接受此参数，
    # 其余格式不接受，必须从 kwargs 中 pop 避免透传报错
    allow_r_exec = kwargs.pop("allow_r_exec", False)
    if ext in {".rda", ".rds"}:
        kwargs["allow_r_exec"] = allow_r_exec
    
    # 对于非统计软件格式，检查元数据丢失
    warnings = []
    if metadata and ext in {".parquet", ".feather", ".orc", ".fst", ".hdf5", ".json", ".xlsx", ".xls", ".csv", ".tsv"}:
        warnings = _check_non_stat_target_loss(metadata)
    
    writer_warnings = writer_func(dataframe, filepath, metadata or {}, **kwargs)
    if writer_warnings:
        warnings.extend(writer_warnings)

    return warnings


def supported_write_formats():
    """返回支持的写入格式扩展名列表"""
    return sorted(_SUPPORT_WRITERS.keys())


def can_preserve_labels(ext):
    """判断指定格式是否能在原生层面保留值和变量标签"""
    return ext.lower() in {".sav", ".zsav", ".dta", ".rda", ".rds", ".xpt"}


def conversion_has_metadata_loss(src_ext, dst_ext):
    """判断从源格式转为目标格式是否有元数据丢失风险 | Check metadata loss risk in conversion."""
    src_labels = src_ext.lower() in {".sav", ".zsav", ".dta", ".rda", ".rds", ".por", ".sas7bdat", ".xpt"}
    dst_labels = dst_ext.lower() in {".sav", ".zsav", ".dta", ".rda", ".rds", ".xpt"}
    
    if src_labels and not dst_labels:
        return (
            f"源格式 {src_ext} 含有变量/值标签 → {dst_ext} 无法保存 | "
            f"Source {src_ext} has variable/value labels → {dst_ext} cannot save them. "
            f"额外生成 _metadata.json | Extra _metadata.json will be generated."
        )
    return None


# ============================================================
# 格式转换入口
# ============================================================

def convert_stat_file(src_path, dst_path, *, metadata=None, **kwargs):
    """
    读入源文件 + 转写目标格式
    
    Parameters
    ----------
    src_path : str（源文件路径）
    dst_path : str（目标文件路径）
    metadata : dict, optional（提供则跳过源文件读入元数据）
    **kwargs
        传递给 write_stat_file 的参数
    
    Returns
    -------
    dict
        {"src_format", "dst_format", "rows", "columns", "warnings"}
    """
    from .reader_core import read_stat_file
    
    result = {
        "src_format": "unknown",
        "dst_format": "unknown",
        "rows": 0,
        "columns": 0,
        "warnings": [],
    }
    
    if metadata is None:
        src_result = read_stat_file(src_path)
        metadata = src_result["metadata"]
        dataframe = src_result["dataframe"]
        result["src_format"] = metadata.get("file_format", "unknown")
        result["warnings"].extend(src_result.get("warnings", []))
    else:
        src_result = read_stat_file(src_path)
        dataframe = src_result["dataframe"]
        result["src_format"] = src_result["metadata"].get("file_format", "unknown")
    
    src_ext = "." + src_path.rsplit(".", 1)[-1].lower() if "." in src_path else ""
    dst_ext = "." + dst_path.rsplit(".", 1)[-1].lower() if "." in dst_path else ""
    
    loss_warning = conversion_has_metadata_loss(src_ext, dst_ext)
    if loss_warning:
        result["warnings"].append(loss_warning)
    
    write_warnings = write_stat_file(dataframe, dst_path, metadata, **kwargs)
    result["warnings"].extend(write_warnings)
    
    result["dst_format"] = dst_ext
    result["rows"] = len(dataframe)
    result["columns"] = len(dataframe.columns)
    
    return result


supported_output_formats = supported_write_formats
