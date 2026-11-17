"""
reader_v14.py - v1.4 新增格式（JMP/Minitab/Prism/jamovi/EpiData/EViews）
自动从 stat_reader.py 拆分生成
"""

from __future__ import annotations
import os
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime
from typing import Any

import pandas as pd
import pyreadstat

from .reader_core import (ColumnInfo, JmpMeta, MinitabMeta, PrismMeta, JamoviMeta, EpidataMeta, EviewsMeta, StatFileResult, _bilingual, _build_column_report, _calc_missing_pct, _get_source_type)
from .reader_r import _check_r_available

# ============================================================
# v1.4 新增格式（JMP/Minitab/Prism/jamovi/EpiData/EViews）
# ============================================================

def _read_sas_catalog(filepath: str, timestamp: str) -> StatFileResult:
    """读入 SAS 目录文件 (.sas7bcat)，返回格式定义（值标签）。"""
    result = pyreadstat.read_sas7bcat(filepath)
    # result 是 dict: {format_name: {value: label}}
    warnings_list = []
    warnings_list.append(_bilingual("SAS Catalog (.sas7bcat) only provides format catalog, reads value_labels only", "SAS Catalog (.sas7bcat) 仅提供格式目录，仅读入 value_labels"))
    rows = []
    for fmt_name, val_dict in result.items():
        for val, lbl in val_dict.items():
            rows.append({"format_name": fmt_name, "value": val, "label": lbl})
    if rows:
        df = pd.DataFrame(rows)
    else:
        df = pd.DataFrame(columns=["format_name", "value", "label"])
        warnings_list.append(_bilingual("SAS catalog file is empty, no format definitions found", "SAS 目录文件为空，未找到任何格式定义"))

    column_report: dict[str, ColumnInfo] = {}
    for col in df.columns:
        column_report[col] = ColumnInfo(
            source_type=_get_source_type(df[col]),
            pandas_dtype=str(df[col].dtype),
            original_label=col,
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
            formula=None,
            column_property=None,
        )

    return {
        "dataframe": df,
        "metadata": SasCatalogMeta(
            file_format="sas_catalog",
            collected_at=timestamp,
            row_count=df.shape[0],
            column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={},
            value_labels=result,
            special_missing={},
            date_origin=None,
            file_encoding=None,
            file_label=None,
            creation_time=None,
            modification_time=None,
            notes=[],
            original_variable_types={},
            readstat_variable_types={},
            variable_value_labels=result,
            variable_to_label={},
            missing_user_values={},
            missing_ranges={},
            variable_display_width={},
            variable_storage_width={},
            variable_measure={},
            variable_alignment={},
            column_names_to_labels={},
            mr_sets={},
            table_name=None,
            sas_catalog_metadata={
                "format_count": len(result),
                "formats": list(result.keys()),
            },
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }



def _read_jmp(filepath: str, timestamp: str) -> StatFileResult:
    """读入 JMP 数据文件 (.jmp），返回第一个数据表。"""
    try:
        import jmpio
    except ImportError:
        raise ImportError(
            "读取 JMP 文件需要 jmpio-python 包。\n"
            "Reading JMP files requires the jmpio-python package.\n"
            "安装方法：pip install jmpio-python\n"
            "Install: pip install jmpio-python\n"
            "或使用 @skill:statsoft-cli 配置 JMP 软件后通过 JSL 脚本读入。"
        )

    warnings_list = []
    jmp = jmpio.read_jmp(filepath)

    # jmpio 返回的对象结构
    if hasattr(jmp, 'tables'):
        tables = jmp.tables
    elif hasattr(jmp, 'data_tables'):
        tables = jmp.data_tables
    else:
        tables = [jmp]

    if not tables:
        raise ValueError(_bilingual("JMP file does not contain any data tables", "JMP 文件不包含任何数据表"))

    # 默认返回第一个表
    table = tables[0]
    if hasattr(table, 'to_df'):
        df = table.to_df()
    elif hasattr(table, 'df'):
        df = table.df
    else:
        df = pd.DataFrame(table)

    warnings_list.append(_bilingual(f"JMP file has {len(tables)} data tables, only the first one returned", f"JMP 文件共 {len(tables)} 个数据表，当前仅返回第一个"))

    all_meta = {
        "variable_labels": getattr(table, 'variable_labels', {}),
        "value_labels": getattr(table, 'value_labels', {}),
    }
    value_labels = all_meta.get("value_labels", {})
    column_report = _build_column_report(
        df, all_meta, value_labels, {}, {}, warnings_list, "jmp"
    )

    return {
        "dataframe": df,
        "metadata": JmpMeta(
            file_format="jmp",
            collected_at=timestamp,
            row_count=df.shape[0],
            column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels=all_meta.get("variable_labels", {}),
            value_labels=value_labels,
            special_missing={},
            date_origin=None,
            file_encoding=None,
            file_label=None,
            creation_time=None,
            modification_time=None,
            notes=[],
            original_variable_types={},
            readstat_variable_types={},
            variable_value_labels=value_labels,
            variable_to_label={},
            missing_user_values={},
            missing_ranges={},
            variable_display_width={},
            variable_storage_width={},
            variable_measure={},
            variable_alignment={},
            column_names_to_labels={},
            mr_sets={},
            table_name=None,
            jmp_metadata={
                "table_count": len(tables),
                "table_names": [getattr(t, 'name', f'table_{i}') for i, t in enumerate(tables)],
            },
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }


# v1.4 新增格式 handler（续）



def _read_minitab(filepath, timestamp, *, format_type, allow_r_exec: bool = False):
    """读入 Minitab 工作簿文件 (.mtw/.mpj)。
    优先尝试 mtbpy；失败时通过 R foreign::read.mtb() 中继；
    都不可用则提示使用 @skill:statsoft-cli 配置 Minitab。
    """
    import tempfile, subprocess, pandas as pd, os

    warnings_list = []
    warnings_list.append(_bilingual("Minitab format does not contain statistical metadata like variable/value labels, only raw data values", "Minitab 格式不含变量标签、值标签等统计元数据，仅保留原始数据值"))

    # 1. 尝试 mtbpy（需要 Minitab 安装）
    try:
        import mtbpy
        # mtbpy 用法参考：mtbpy.read_mtw(filepath)
        df = mtbpy.read_mtw(filepath) if format_type == "minitab_mtw" else mtbpy.read_mpj(filepath)
        warnings_list.append(_bilingual("Read Minitab file via mtbpy", "通过 mtbpy 读入 Minitab 文件"))
        meta_extra = {"read_via": "mtbpy"}
    except ImportError:
        # 2. 尝试 R foreign::read.mtb() 中继（需显式开启，默认隔离）
        if not allow_r_exec:
            raise RuntimeError(
                "Minitab software not installed and the R-interpreter bridge is disabled by default for security "
                "(invoking R on untrusted files can execute embedded code). "
                "If the file is TRUSTED, install R+foreign and retry with allow_r_exec=True.\n"
                "Minitab 软件未安装，且出于安全默认禁用 R 解释器中继（对不可信文件调用 R 可能执行嵌入代码）。"
                "若文件可信，请安装 R+foreign 后用 allow_r_exec=True 重试。"
            )
        rscript = _check_r_available()
        if rscript:
            warnings_list.append(_bilingual("Minitab software not installed, reading via R foreign package bridge", "Minitab 软件未安装，通过 R foreign 包中继读入"))
            return _read_minitab_via_r(filepath, timestamp, format_type, rscript, allow_r_exec=allow_r_exec)
        # 3. 都不可用：提示用户
        raise RuntimeError(
            "读入 Minitab 文件需要 Minitab 软件。\\n"
            "Reading Minitab files requires Minitab software.\\n"
            "请使用 @skill:statsoft-cli 配置 Minitab，或安装 R 及 foreign 包：\\n"
            "Use @skill:statsoft-cli to configure Minitab, or install R and foreign package:\\n"
            "  install.packages(\"foreign\")\\n"
            "Minitab 下载：https://www.minitab.com/"
        )

    column_report = _build_column_report(
        df, {"variable_labels": {}}, {}, {}, {}, warnings_list, "minitab"
    )

    return {
        "dataframe": df,
        "metadata": MinitabMeta(
            file_format="minitab",
            collected_at=timestamp,
            row_count=df.shape[0],
            column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={},
            value_labels={},
            special_missing={},
            date_origin=None,
            file_encoding=None,
            file_label=None,
            creation_time=None,
            modification_time=None,
            notes=[],
            original_variable_types={},
            readstat_variable_types={},
            variable_value_labels={},
            variable_to_label={},
            missing_user_values={},
            missing_ranges={},
            variable_display_width={},
            variable_storage_width={},
            variable_measure={},
            variable_alignment={},
            column_names_to_labels={},
            mr_sets={},
            table_name=None,
            minitab_metadata={"read_via": "mtbpy"},
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }





# ============================================================
# 安全辅助：以「写临时 .R 脚本 + 命令行参数」方式运行 R
# 与 reader_r.py 的 _run_r_script 保持一致模式（消除命令注入）。
# ============================================================
def _run_r_script(rscript_path, script_body, *args, timeout=120):
    """将**完全静态**的 R 脚本写入临时文件，用 `Rscript script.R <args...>` 运行。

    安全要点：脚本体不得内插任何不可信输入（文件路径等），
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


# 静态 R 脚本：经 foreign::read.mtb() 读 Minitab 并写 CSV。
# filepath / out_csv 均经 argv 传入，脚本不含任何用户输入。
_R_MINITAB_SCRIPT = r"""
args <- commandArgs(trailingOnly=TRUE)
filepath <- args[1]
out_csv <- args[2]
library(foreign)
data <- read.mtb(filepath)
write.csv(data, file=out_csv, row.names=FALSE, fileEncoding='UTF-8')
"""

# 静态 R 脚本：经 foreign::read.epiinfo() 读 EpiData 并写 CSV。
_R_EPIDATA_SCRIPT = r"""
args <- commandArgs(trailingOnly=TRUE)
filepath <- args[1]
out_csv <- args[2]
library(foreign)
data <- read.epiinfo(filepath)
write.csv(data, file=out_csv, row.names=FALSE, fileEncoding='UTF-8')
"""
def _read_minitab_via_r(filepath, timestamp, format_type, rscript_path, allow_r_exec: bool = False):
    """通过 R foreign::read.mtb() 中继读入 Minitab 文件。"""
    import pandas as pd

    fd, tmp_csv = tempfile.mkstemp(suffix=".csv", prefix="statdata_mtb_")
    os.close(fd)
    try:
        _run_r_script(rscript_path, _R_MINITAB_SCRIPT, filepath, tmp_csv)
        df = pd.read_csv(tmp_csv, encoding="utf-8")
    finally:
        try:
            os.unlink(tmp_csv)
        except Exception:
            pass

    column_report = _build_column_report(
        df, {"variable_labels": {}}, {}, {}, {}, [], "minitab"
    )

    return {
        "dataframe": df,
        "metadata": MinitabMeta(
            file_format="minitab",
            collected_at=timestamp,
            row_count=df.shape[0],
            column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={},
            value_labels={},
            special_missing={},
            date_origin=None,
            file_encoding=None,
            file_label=None,
            creation_time=None,
            modification_time=None,
            notes=[],
            original_variable_types={},
            readstat_variable_types={},
            variable_value_labels={},
            variable_to_label={},
            missing_user_values={},
            missing_ranges={},
            variable_display_width={},
            variable_storage_width={},
            variable_measure={},
            variable_alignment={},
            column_names_to_labels={},
            mr_sets={},
            table_name=None,
            minitab_metadata={"read_via": "R foreign::read.mtb()"},
        ),
        "warnings": [_bilingual("Read Minitab file via R foreign package bridge", "通过 R foreign 包中继读入 Minitab 文件")],
        "column_report": column_report,
    }



def _read_prism(filepath, timestamp, *, format_type):
    """读入 GraphPad Prism 项目文件 (.pzfx/.pz)。
    需要 pzfx 包（PyPI），或 @skill:statsoft-cli 配置 PRISM CLI。
    """
    try:
        import pzfx
    except ImportError:
        raise RuntimeError(
            "读入 PRISM 文件需要 pzfx 包。\\n"
            "Reading PRISM files requires the pzfx package.\\n"
            "安装：pip install pzfx\\n"
            "Install: pip install pzfx\\n"
            "或直接使用 GraphPad PRISM 软件导出 CSV，然后使用 @skill:statsoft-cli 配置 Prism CLI。"
        )

    warnings_list = []
    warnings_list.append(_bilingual("Prism format does not contain most statistical metadata like variable labels, value labels, measure levels, etc.", "Prism 格式不含变量标签、值标签、测量级别等大部分统计元数据"))
    pz = pzfx.load_prism(filepath)

    # pzfx 返回的数据结构：pz.tables 是数据表列表
    tables = getattr(pz, "tables", [])
    if not tables:
        raise ValueError(_bilingual("PRISM file does not contain any data tables", "PRISM 文件不包含任何数据表"))

    # 默认返回第一个数据表
    table = tables[0]
    df = table.to_dataframe() if hasattr(table, "to_dataframe") else pd.DataFrame(table)
    if len(tables) > 1:
        warnings_list.append(_bilingual(f"PRISM file has {len(tables)} data/result tables, only the first one returned", f"PRISM 文件共 {len(tables)} 个数据表/结果表，当前仅返回第一个"))

    column_report = _build_column_report(
        df, {"variable_labels": {}}, {}, {}, {}, warnings_list, "prism"
    )

    return {
        "dataframe": df,
        "metadata": PrismMeta(
            file_format="prism",
            collected_at=timestamp,
            row_count=df.shape[0],
            column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={},
            value_labels={},
            special_missing={},
            date_origin=None,
            file_encoding=None,
            file_label=None,
            creation_time=None,
            modification_time=None,
            notes=warnings_list,
            original_variable_types={},
            readstat_variable_types={},
            variable_value_labels={},
            variable_to_label={},
            missing_user_values={},
            missing_ranges={},
            variable_display_width={},
            variable_storage_width={},
            variable_measure={},
            variable_alignment={},
            column_names_to_labels={},
            mr_sets={},
            table_name=None,
            prism_metadata={
                "table_count": len(tables),
                "tables": [getattr(t, "name", f"table_{i}") for i, t in enumerate(tables)],
            },
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }



def _read_jamovi(filepath, timestamp):
    """读入 jamovi 项目文件 (.omv)。
    jamovi 文件是 ZIP 压缩包，内含 CSV 数据和 JSON 分析设置。
    """
    import zipfile, pandas as pd, json, io

    warnings_list = []
    warnings_list.append(_bilingual("jamovi format does not contain most statistical metadata like variable/value labels, etc.", "jamovi 格式不含变量标签、值标签等大部分统计元数据"))

    with zipfile.ZipFile(filepath, "r") as zf:
        # 查找 CSV 数据文件
        csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
        if not csv_files:
            raise ValueError(_bilingual("No CSV data file found in jamovi file", "jamovi 文件中未找到 CSV 数据文件"))

        # 读入第一个 CSV 文件
        with zf.open(csv_files[0]) as f:
            df = pd.read_csv(io.BytesIO(f.read()), encoding="utf-8")

        # 安全：jamovi 的 .json 为分析设置/笔记等嵌入内容，与数据转换无关，
        # 且可能包含敏感信息，故不读取、不向外传播（避免意外收集/泄露嵌入内容）。
        analysis = {}

    warnings_list.append(_bilingual(f"jamovi file contains {len(csv_files)} CSV files, currently only reading {csv_files[0]}", f"jamovi 文件包含 {len(csv_files)} 个 CSV 文件，当前仅读入 {csv_files[0]}"))

    column_report = _build_column_report(
        df, {"variable_labels": {}}, {}, {}, {}, warnings_list, "jamovi"
    )

    return {
        "dataframe": df,
        "metadata": JamoviMeta(
            file_format="jamovi",
            collected_at=timestamp,
            row_count=df.shape[0],
            column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={},
            value_labels={},
            special_missing={},
            date_origin=None,
            file_encoding="utf-8",
            file_label=None,
            creation_time=None,
            modification_time=None,
            notes=warnings_list,
            original_variable_types={},
            readstat_variable_types={},
            variable_value_labels={},
            variable_to_label={},
            missing_user_values={},
            missing_ranges={},
            variable_display_width={},
            variable_storage_width={},
            variable_measure={},
            variable_alignment={},
            column_names_to_labels={},
            mr_sets={},
            table_name=None,
            jamovi_metadata={
                "csv_files": csv_files,
                "analysis_files": list(analysis.keys()),
                "analysis": analysis,
            },
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }



def _read_epidata(filepath, timestamp, *, allow_r_exec: bool = False):
    """读入 EpiData/Epi Info 数据文件 (.rec)。
    通过 R foreign 包中继（pyreadstat 不支持 .rec 格式）。
    """
    import tempfile, subprocess, pandas as pd, os

    warnings_list = []
    warnings_list.append(_bilingual("EpiData format does not contain statistical metadata like variable/value labels, only raw data values", "EpiData 格式不含变量标签、值标签等统计元数据，仅保留原始数据值"))

    if not allow_r_exec:
        raise RuntimeError(
            "Reading EpiData .rec requires invoking the local R interpreter (foreign::read.epiinfo), "
            "which is disabled by default for security (R can execute embedded code from untrusted files). "
            "If the file is TRUSTED, retry with allow_r_exec=True.\n"
            "读入 EpiData .rec 需调用本地 R 解释器（foreign::read.epiinfo），出于安全默认禁用"
            "（R 可能执行不可信文件中的嵌入代码）。若文件可信，请使用 allow_r_exec=True 重试。"
        )
    rscript = _check_r_available()
    if rscript:
        return _read_epidata_via_r(filepath, timestamp, rscript, allow_r_exec=allow_r_exec)

    raise RuntimeError(
        "读入 EpiData .rec 文件需要 R 及 foreign 包。\\n"
        "Reading EpiData .rec files requires R and the foreign package.\\n"
        "请安装 R：https://cran.r-project.org/，然后运行：\\n"
        "  install.packages(\"foreign\")"
    )



def _read_epidata_via_r(filepath, timestamp, rscript_path, allow_r_exec: bool = False):
    """通过 R foreign::read.epiinfo() 中继读入 EpiData .rec 文件。"""
    import pandas as pd

    fd, tmp_csv = tempfile.mkstemp(suffix=".csv", prefix="statdata_epi_")
    os.close(fd)
    try:
        _run_r_script(rscript_path, _R_EPIDATA_SCRIPT, filepath, tmp_csv)
        df = pd.read_csv(tmp_csv, encoding="utf-8")
    finally:
        try:
            os.unlink(tmp_csv)
        except Exception:
            pass

    column_report = _build_column_report(
        df, {"variable_labels": {}}, {}, {}, {}, warnings_list, "epidata"
    )

    return {
        "dataframe": df,
        "metadata": EpidataMeta(
            file_format="epidata",
            collected_at=timestamp,
            row_count=df.shape[0],
            column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={},
            value_labels={},
            special_missing={},
            date_origin=None,
            file_encoding=None,
            file_label=None,
            creation_time=None,
            modification_time=None,
            notes=[],
            original_variable_types={},
            readstat_variable_types={},
            variable_value_labels={},
            variable_to_label={},
            missing_user_values={},
            missing_ranges={},
            variable_display_width={},
            variable_storage_width={},
            variable_measure={},
            variable_alignment={},
            column_names_to_labels={},
            mr_sets={},
            table_name=None,
            epidata_metadata={"read_via": "R foreign::read.epiinfo()"},
        ),
        "warnings": [_bilingual("Read EpiData .rec file via R foreign package bridge", "通过 R foreign 包中继读入 EpiData .rec 文件")],
        "column_report": column_report,
    }



def _read_eviews(filepath, timestamp, *, format_type):
    """读入 EViews 工作文件 (.wf1/.wf2)。
    .wf2 是 JSON 格式，可直接解析；.wf1 是封闭二进制格式，需要 EViews 软件。
    """
    import pandas as pd, json

    warnings_list = []
    warnings_list.append(_bilingual("EViews format does not contain most statistical metadata like variable labels, value labels, etc.", "EViews 格式不含变量标签、值标签等大部分统计元数据"))

    if format_type == "eviews_wf2":
        with open(filepath, "r", encoding="utf-8") as f:
            eviews_data = json.load(f)

        # 尝试提取数据（不同 EViews 版本的 JSON 结构不同）
        df = pd.DataFrame()
        if "pages" in eviews_data:
            for page in eviews_data["pages"]:
                if "series" in page:
                    for sname, sdata in page["series"].items():
                        df[sname] = sdata.get("data", [])
        elif "workfile" in eviews_data:
            warnings_list.append(_bilingual("EViews .wf2 format: detected workfile structure, attempting to extract data", "EViews .wf2 格式：检测到 workfile 结构，尝试提取数据"))
        else:
            warnings_list.append(_bilingual("EViews .wf2 format: unrecognized JSON structure, saving raw JSON only", "EViews .wf2 格式：未识别的 JSON 结构，仅保存原始 JSON"))

        if df.empty:
            warnings_list.append(_bilingual("Unable to extract DataFrame from EViews .wf2, please export data to CSV or Excel", "无法从 EViews .wf2 提取 DataFrame，请将数据导出为 CSV 或 Excel"))
            df = pd.DataFrame({"raw_json": [json.dumps(eviews_data, ensure_ascii=False)[:1000]]})
    else:
        # .wf1 是封闭二进制格式，需要 EViews 软件
        raise RuntimeError(
            "读入 EViews .wf1 文件需要 EViews 软件。\\n"
            "Reading EViews .wf1 files requires EViews software.\\n"
            "请使用 @skill:statsoft-cli 配置 EViews，或将文件导出为 .wf2（JSON 格式）。"
        )

    column_report = _build_column_report(
        df, {"variable_labels": {}}, {}, {}, {}, warnings_list, "eviews"
    )

    return {
        "dataframe": df,
        "metadata": EviewsMeta(
            file_format="eviews",
            collected_at=timestamp,
            row_count=df.shape[0],
            column_count=df.shape[1],
            total_missing_pct=_calc_missing_pct(df),
            variable_labels={},
            value_labels={},
            special_missing={},
            date_origin=None,
            file_encoding="utf-8",
            file_label=None,
            creation_time=None,
            modification_time=None,
            notes=warnings_list,
            original_variable_types={},
            readstat_variable_types={},
            variable_value_labels={},
            variable_to_label={},
            missing_user_values={},
            missing_ranges={},
            variable_display_width={},
            variable_storage_width={},
            variable_measure={},
            variable_alignment={},
            column_names_to_labels={},
            mr_sets={},
            table_name=None,
            eviews_metadata={
                "format_type": format_type,
                "raw_json_keys": list(eviews_data.keys()) if format_type == "eviews_wf2" else [],
            },
        ),
        "warnings": warnings_list,
        "column_report": column_report,
    }
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: C:\\Tools\\anaconda3\\python.exe -c \"from scripts.reader_core import read_stat_file; result = read_stat_file('data.sav')\"")
        sys.exit(1)

    filepath = sys.argv[1]
    enc = sys.argv[2] if len(sys.argv) > 2 else None
    result = read_stat_file(filepath, encoding=enc)
    report = generate_read_report(result)
    print(report)

    summary = {
        "metadata": result["metadata"],
        "warnings": result["warnings"],
        "column_report": result["column_report"],
    }
    summary_json = json.dumps(summary, ensure_ascii=False, default=str)
    print("\n\n===JSON_SUMMARY_START===")
    print(summary_json)
    print("===JSON_SUMMARY_END===")


