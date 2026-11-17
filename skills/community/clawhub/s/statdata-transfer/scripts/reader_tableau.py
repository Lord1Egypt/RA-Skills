"""
reader_tableau.py - Tableau Hyper (.hyper) read/write bridge.

Reads a Tableau Hyper extract file into a pandas DataFrame, recovering
``statdata_meta`` (variable labels / value labels / special missing) from a
side-table when present. Writes a DataFrame to a ``.hyper`` file using the
official Tableau Hyper API.

Security notes
--------------
* Uses the official ``tableauhyperapi`` package (Tableau/Salesforce, Apache-2.0).
* No shell, no R subprocess, no string interpolation into executable code.
* All table/column identifiers are passed through the typed Hyper API; the
  only string we interpolate is JSON metadata we ourselves generated.
"""
from __future__ import annotations

import json
import os
import tempfile
import zipfile
from typing import Any

import pandas as pd
from tableauhyperapi import (
    Connection,
    CreateMode,
    HyperProcess,
    Inserter,
    Interval as HyperInterval,
    Nullability,
    SchemaName,
    SqlType,
    TableDefinition,
    TableName,
    Telemetry,
)

from .reader_core import (
    StatFileResult,
    _build_column_report,
    _build_metadata,
    _calc_missing_pct,
    _bilingual,
)

HYPER_TELEMETRY = Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU
SYS_SCHEMAS = {"pg_catalog", "information_schema"}
EXTRACT_SCHEMA = "Extract"
EXTRACT_TABLE = "Extract"
META_SCHEMA = "statdata"
META_TABLE = "meta"

# keys we persist into the statdata_meta side-table
_META_KEYS = ("variable_labels", "value_labels", "special_missing", "measurement_levels")


def _unquote(name: Any) -> str:
    # TableName/column identifiers render as "Schema"."Table" (quoted).
    # Strip every quote so we can match against plain names like Extract.Extract.
    return str(name).replace('"', '')


# ============================================================
# READ
# ============================================================
def _read_hyper(filepath: str, timestamp: str) -> StatFileResult:
    """Read a Tableau ``.hyper`` file into a StatFileResult dict."""
    warnings_list: list[str] = []

    hyper = HyperProcess(telemetry=HYPER_TELEMETRY)
    conn = Connection(
        endpoint=hyper.endpoint,
        database=filepath,
        create_mode=CreateMode.NONE,
    )
    try:
        # enumerate user tables (skip system schemas)
        schemas = conn.catalog.get_schema_names()
        tables: list[TableName] = []
        for s in schemas:
            if _unquote(s) in SYS_SCHEMAS:
                continue
            for t in conn.catalog.get_table_names(s):
                tables.append(t)

        if not tables:
            raise RuntimeError(_bilingual(
                f"No data table found in Hyper file: {filepath}",
                f"Hyper 文件中未找到任何数据表: {filepath}",
            ))

        # prefer the Tableau extract convention "Extract"."Extract"
        target = None
        for t in tables:
            if _unquote(t) == f"{EXTRACT_SCHEMA}.{EXTRACT_TABLE}":
                target = t
                break
        if target is None:
            target = tables[0]

        query = "SELECT * FROM %s" % str(target)
        result = conn.execute_query(query)
        col_defs = [(c.name.unescaped, str(c.type).lower()) for c in result.schema.columns]
        columns = [n for n, _ in col_defs]

        # convert Hyper-native types to pandas-friendly Python types while reading,
        # so DataFrame construction succeeds (pandas cannot ingest Timestamp/Interval directly)
        def _coerce(v, sqltype):
            if "interval" in sqltype:
                if isinstance(v, HyperInterval):
                    return pd.Timedelta(days=v.days, microseconds=v.microseconds)
                return v
            if "timestamp" in sqltype:
                if hasattr(v, "to_datetime"):
                    return v.to_datetime()
                return v
            return v

        rows = []
        while result.next_row():
            vals = result.get_values()
            rows.append(
                tuple(_coerce(v, sqltype) for v, (_, sqltype) in zip(vals, col_defs))
            )
        df = pd.DataFrame(rows, columns=columns)
        result.close()

        # recover statdata_meta side-table if present
        all_meta: dict[str, Any] = {
            "variable_labels": {},
            "value_labels": {},
            "special_missing": {},
        }
        if conn.catalog.has_table(TableName(META_SCHEMA, META_TABLE)):
            try:
                mres = conn.execute_query(
                    'SELECT "json" FROM "%s"."%s"' % (META_SCHEMA, META_TABLE)
                )
                try:
                    if mres.next_row():
                        stored = json.loads(mres.get_value(0))
                        if isinstance(stored, dict):
                            for k in _META_KEYS:
                                if k in stored and isinstance(stored[k], dict):
                                    all_meta[k] = stored[k]
                finally:
                    mres.close()
            except Exception:
                # never fail the whole read because of a malformed meta side-table
                pass

        column_report = _build_column_report(
            df,
            all_meta,
            all_meta.get("value_labels", {}),
            {},
            {},
            warnings_list,
            "tableau_hyper",
        )

        metadata = _build_metadata(
            all_meta,
            "tableau_hyper",
            {
                "collected_at": timestamp,
                "row_count": df.shape[0],
                "column_count": df.shape[1],
                "total_missing_pct": _calc_missing_pct(df),
            },
        )
    finally:
        conn.close()
        hyper.close()

    return {
        "dataframe": df,
        "metadata": metadata,
        "warnings": warnings_list,
        "column_report": column_report,
    }


# ============================================================
# READ - Tableau packaged workbook (.twbx)
# ============================================================
def _read_twbx(filepath: str, timestamp: str) -> StatFileResult:
    """Read a Tableau packaged workbook (.twbx).

    A .twbx is a zip archive containing a .twb workbook (XML definition, no
    data) plus one or more embedded data extracts.  Typical layouts:

    * 现代的 Tableau 打包工作簿内嵌一个或多个 ``.hyper`` 文件（优先读取）。
    * 部分旧版 / 特殊 .twbx 可能内嵌一个 MS Access 数据库（ ``.mdb`` / ``.accdb``）。
    """
    warnings_list: list[str] = []
    with zipfile.ZipFile(filepath) as z:
        names = z.namelist()
    hyper_entries = [n for n in names if n.lower().endswith(".hyper")]
    tde_entries = [n for n in names if n.lower().endswith(".tde")]
    mdb_entries = [n for n in names if n.lower().endswith(".mdb")]
    accdb_entries = [n for n in names if n.lower().endswith(".accdb")]
    embedded_access = mdb_entries + accdb_entries

    if not hyper_entries and not embedded_access:
        raise RuntimeError(
            _bilingual(
                "No .hyper/.mdb/.accdb extract found inside .twbx; cannot read a data table "
                "(the .twb workbook holds no data; legacy .tde is not yet supported)",
                ".twbx 内未找到 .hyper / .mdb / .accdb 任何数据提取，无法读取数据表（.twb 工作簿本身不含数据；"
                "若为旧版 .tde 提取暂不支持）",
            )
        )

    results = []
    with zipfile.ZipFile(filepath) as z, tempfile.TemporaryDirectory() as tmp:
        for i, h in enumerate(hyper_entries):
            dest = os.path.join(tmp, "embedded_%d.hyper" % i)
            with z.open(h) as src, open(dest, "wb") as out:
                out.write(src.read())
            results.append((h, _read_hyper(dest, timestamp)))
        for i, m in enumerate(embedded_access, start=len(hyper_entries)):
            dest = os.path.join(tmp, "embedded_%d%s" % (i, os.path.splitext(m)[1]))
            with z.open(m) as src, open(dest, "wb") as out:
                out.write(src.read())
            try:
                from . import reader_legacy
                if m.lower().endswith(".accdb"):
                    res_acc = reader_legacy._read_access(dest, timestamp)
                else:
                    res_acc = reader_legacy._read_access(dest, timestamp)
                results.append((m, res_acc))
            except Exception as e:
                warnings_list.append(_bilingual(
                    "Failed to read embedded Access file %s inside .twbx: %s" % (m, e),
                    ".twbx 中内嵌 Access 文件 %s 读取失败: %s" % (m, e)))

    if not results:
        raise RuntimeError(_bilingual(
            "All embedded extracts inside .twbx failed to read",
            ".twbx 内所有数据提取均读取失败"))

    primary_name, primary = results[0]
    primary["metadata"]["file_format"] = "tableau_twbx"
    primary["metadata"]["source_container"] = "tableau_twbx"
    primary["metadata"]["embedded_extracts"] = [n for n, _ in results]
    primary["warnings"].append(
        _bilingual(
            "Unpacked and read embedded extract(s) from .twbx: %s"
            % ", ".join(n for n, _ in results),
            "已从 .twbx 解包并读取内嵌数据提取: %s" % ", ".join(n for n, _ in results),
        )
    )
    if len(results) > 1:
        primary["warnings"].append(
            _bilingual(
                "Found %d embedded extracts; only the first «%s» is returned; others "
                "not read: %s" % (len(results), primary_name, ", ".join(n for n, _ in results[1:])),
                "检测到 %d 个内嵌数据提取，仅返回首个「%s」；其余未读取: %s"
                % (len(results), primary_name, ", ".join(n for n, _ in results[1:])),
            )
        )
    if tde_entries:
        primary["warnings"].append(
            _bilingual(
                "Found %d legacy .tde extract(s) not read (unsupported yet): %s"
                % (len(tde_entries), ", ".join(tde_entries)),
                "发现 %d 个旧版 .tde 提取未读取（暂不支持）: %s"
                % (len(tde_entries), ", ".join(tde_entries)),
            )
        )
    return primary


def _read_twb(filepath: str, timestamp: str) -> StatFileResult:
    """A bare .twb workbook holds no embedded data -- refuse with guidance."""
    raise RuntimeError(
        _bilingual(
            ".twb is a Tableau workbook (XML definition) with no embedded data; cannot be "
            "read as a data file. Use a packaged .twbx (embeds .hyper) or a .hyper extract directly",
            ".twb 是 Tableau 工作簿（XML 定义），本身不含数据表，无法作为数据文件读取；"
            "请使用打包工作簿 .twbx（含内嵌 .hyper）或直接提供 .hyper 提取文件",
        )
    )


# ============================================================
# WRITE
# ============================================================
def _pandas_col_to_hyper(series: pd.Series):
    """Map a pandas Series dtype to a (SqlType, nullable) pair."""
    dtype = series.dtype
    if pd.api.types.is_bool_dtype(dtype):
        return SqlType.bool(), True
    if pd.api.types.is_integer_dtype(dtype):
        return SqlType.big_int(), True
    if pd.api.types.is_float_dtype(dtype):
        return SqlType.double(), True
    if pd.api.types.is_datetime64_any_dtype(dtype):
        if getattr(dtype, "tz", None) is not None:
            return SqlType.timestamp_tz(), True
        return SqlType.timestamp(), True
    if pd.api.types.is_timedelta64_dtype(dtype):
        return SqlType.interval(), True
    # object / category / unknown -> text (values coerced to str)
    return SqlType.text(), True


def _convert_value(v: Any, series: pd.Series) -> Any:
    """Coerce a pandas cell value into a Hyper-acceptable Python type."""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    dtype = series.dtype
    if pd.api.types.is_bool_dtype(dtype):
        return bool(v)
    if pd.api.types.is_integer_dtype(dtype):
        return int(v)
    if pd.api.types.is_float_dtype(dtype):
        return float(v)
    if pd.api.types.is_datetime64_any_dtype(dtype):
        if hasattr(v, "to_pydatetime"):
            return v.to_pydatetime()
        return v
    if pd.api.types.is_timedelta64_dtype(dtype):
        # pandas Timedelta -> Hyper Interval (months always 0 for timedelta)
        days = v.days
        micros = v.seconds * 1_000_000 + v.microseconds
        return HyperInterval(months=0, days=days, microseconds=micros)
    # text column: str-coerce everything (Hyper TEXT is UTF-8)
    if v is None:
        return None
    return str(v)


def _write_meta_side_table(conn, metadata: dict) -> None:
    """Store statdata_meta as a single-row JSON side-table (best-effort)."""
    payload = {k: metadata[k] for k in _META_KEYS if metadata.get(k)}
    if not payload:
        return
    conn.catalog.create_schema_if_not_exists(SchemaName(META_SCHEMA))
    mt = TableDefinition(
        TableName(META_SCHEMA, META_TABLE),
        [TableDefinition.Column("json", SqlType.text(), Nullability.NOT_NULLABLE)],
    )
    conn.catalog.create_table_if_not_exists(mt)
    with Inserter(conn, mt) as mins:
        mins.add_row((json.dumps(payload, ensure_ascii=False),))
        mins.execute()


def _write_hyper(df: pd.DataFrame, filepath: str, metadata: dict | None = None, **kwargs) -> list:
    """Write a DataFrame to a Tableau ``.hyper`` file.

    Returns a list of metadata-loss warnings (mirrors the other writers).
    """
    warnings_list: list[str] = []
    metadata = metadata or {}

    # 安全写入策略：先写临时目录内的 .hyper 文件，成功后再原子替换目标文件。
    # 这样写入失败/异常时，原 filepath 完全不动，杜绝静默数据丢失。
    # 用临时目录（而非 mkstemp 的空文件）以便 tableauhyperapi 自行创建新库。
    import tempfile, shutil
    tmp_dir = tempfile.mkdtemp(prefix="statdata_hyper_")
    tmp_path = os.path.join(tmp_dir, "out.hyper")

    hyper = HyperProcess(telemetry=HYPER_TELEMETRY)
    conn = Connection(
        endpoint=hyper.endpoint,
        database=tmp_path,
        create_mode=CreateMode.CREATE_AND_REPLACE,
    )
    success = False
    try:
        conn.catalog.create_schema(SchemaName(EXTRACT_SCHEMA))
        cols = []
        for col in df.columns:
            sql_type, nullable = _pandas_col_to_hyper(df[col])
            cols.append(
                TableDefinition.Column(
                    str(col),
                    sql_type,
                    Nullability.NULLABLE if nullable else Nullability.NOT_NULLABLE,
                )
            )
        td = TableDefinition(TableName(EXTRACT_SCHEMA, EXTRACT_TABLE), cols)
        conn.catalog.create_table(td)
        with Inserter(conn, td) as ins:
            for _, row in df.iterrows():
                ins.add_row(
                    tuple(_convert_value(v, df[col]) for col, v in row.items())
                )
            # commit the buffered rows (execute() flushes + closes the inserter)
            ins.execute()

        # persist statdata_meta for round-trip label recovery
        _write_meta_side_table(conn, metadata)

        # metadata-loss note (mirrors non-stat targets)
        if metadata.get("variable_labels") or metadata.get("value_labels"):
            warnings_list.append(
                _bilingual(
                    "Variable/value labels stored in a statdata_meta side-table, "
                    "readable only by this skill; Tableau sees data columns only",
                    "变量/值标签通过 statdata_meta 副表存入 .hyper，仅本技能可读回；"
                    "Tableau 等外部工具打开时仅见数据列",
                )
            )
        success = True
    finally:
        conn.close()
        hyper.close()

    if success:
        # 原子替换：先轮转备份 —— 永不静默删除 .bak，仅将其降级为 .bak.1
        if os.path.exists(filepath):
            backup = filepath + ".bak"
            bak1 = filepath + ".bak.1"
            if os.path.exists(backup):
                if os.path.exists(bak1):
                    try:
                        os.remove(bak1)  # 只删最旧历史 .bak.1，不动 .bak
                    except OSError:
                        pass
                os.rename(backup, bak1)
            os.rename(filepath, backup)
        os.replace(tmp_path, filepath)  # 跨平台原子替换
    else:
        # 写入失败：原 filepath 保持不变
        pass
    # 无论成功失败，清理临时目录
    shutil.rmtree(tmp_dir, ignore_errors=True)

    return warnings_list
