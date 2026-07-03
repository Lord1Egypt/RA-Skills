import os
import pandas as pd
import numpy as np

USL_KEYWORDS = ["usl", "ucl", "spec_upper", "upper_spec", "upper", "specupper", "spec上限", "规格上限", "上限"]
LSL_KEYWORDS = ["lsl", "lcl", "spec_lower", "lower_spec", "lower", "speclower", "spec下限", "规格下限", "下限"]
TIME_KEYWORDS = ["time", "小时", "循环", "cycle", "hour", "duration", "period"]
CENSOR_KEYWORDS = ["censor", "f/s", "删失", "状态", "status", "event", "failure", "生存状态", "cens"]
BATCH_KEYWORDS = ["batch", "批", "lot", "组", "subgroup", "子组"]
LABEL_VALUES = {"ok", "ng", "合格", "不合格", "pass", "fail", "good", "bad", "通过", "不通过", "accept", "reject"}


def _read_file(file_path: str) -> pd.DataFrame:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".csv":
            return pd.read_csv(file_path)
        elif ext in (".xlsx", ".xls"):
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    except Exception as e:
        raise ValueError(f"Failed to read {file_path}: {e}")


def _identify_column(df: pd.DataFrame, col: str) -> str:
    name_lower = col.lower().strip()
    series = df[col]

    for kw in USL_KEYWORDS:
        if kw in name_lower:
            return "spec_upper"
    for kw in LSL_KEYWORDS:
        if kw in name_lower:
            return "spec_lower"
    for kw in TIME_KEYWORDS:
        if kw in name_lower:
            if series.dropna().apply(lambda x: isinstance(x, (int, float)) or (isinstance(x, str) and x.replace(".", "", 1).replace("-", "", 1).isdigit())).all():
                return "time"
    for kw in CENSOR_KEYWORDS:
        if kw in name_lower:
            unique_vals = set(series.dropna().unique())
            if unique_vals.issubset({0, 1, "0", "1", 0.0, 1.0, True, False}):
                return "censor"
    for kw in BATCH_KEYWORDS:
        if kw in name_lower:
            return "batch"

    if series.dtype in [np.float64, np.int64, float, int]:
        return "measurement"

    unique_vals = set(str(v).lower().strip() for v in series.dropna().unique())
    if unique_vals.issubset(LABEL_VALUES):
        return "pass_fail"

    try:
        pd.to_numeric(series.dropna())
        return "measurement"
    except (ValueError, TypeError):
        pass

    return "label"


def qc_parse_data(file_path: str, mode: str = "auto") -> dict:
    file_name = os.path.basename(file_path)
    df = _read_file(file_path)
    num_rows = len(df)

    columns_info = []
    spec_upper_value = None
    spec_lower_value = None

    for col in df.columns:
        col_type = _identify_column(df, col)
        col_entry = {"name": col, "type": col_type}

        if col_type == "measurement":
            series = pd.to_numeric(df[col], errors="coerce").dropna()
            col_entry["mean"] = float(round(series.mean(), 6))
            col_entry["std"] = float(round(series.std(ddof=1), 6))
            col_entry["min"] = float(round(series.min(), 6))
            col_entry["max"] = float(round(series.max(), 6))
            col_entry["rows"] = len(series)
        elif col_type == "spec_upper":
            series = pd.to_numeric(df[col], errors="coerce").dropna()
            spec_upper_value = float(series.iloc[0]) if len(series) > 0 else None
            col_entry["value"] = spec_upper_value
        elif col_type == "spec_lower":
            series = pd.to_numeric(df[col], errors="coerce").dropna()
            spec_lower_value = float(series.iloc[0]) if len(series) > 0 else None
            col_entry["value"] = spec_lower_value

        columns_info.append(col_entry)

    has_time = any(c["type"] == "time" for c in columns_info)
    has_censor = any(c["type"] == "censor" for c in columns_info)
    has_measurement = any(c["type"] == "measurement" for c in columns_info)
    has_batch = any(c["type"] == "batch" for c in columns_info)

    if has_time and has_censor:
        pipeline = "reliability"
    elif has_measurement:
        pipeline = "spc"
    else:
        pipeline = "unknown"

    suggestions = {"control_chart": None, "subgroup_size": None}

    if pipeline == "spc":
        measurement_cols = [c["name"] for c in columns_info if c["type"] == "measurement"]
        batch_cols = [c["name"] for c in columns_info if c["type"] == "batch"]
        has_pass_fail_col = any(c["type"] == "pass_fail" for c in columns_info)

        if has_pass_fail_col:
            suggestions["control_chart"] = "P-Chart"
            suggestions["subgroup_size"] = num_rows
        elif batch_cols and measurement_cols:
            batch_sizes = df.groupby(batch_cols[0]).size()
            avg_size = int(batch_sizes.mean())
            suggestions["subgroup_size"] = avg_size
            suggestions["control_chart"] = "Xbar-R" if avg_size <= 10 else "Xbar-S"
        elif measurement_cols and not batch_cols:
            suggestions["control_chart"] = "I-MR"
            suggestions["subgroup_size"] = 1

    if spec_upper_value is not None:
        suggestions["usl"] = spec_upper_value
    if spec_lower_value is not None:
        suggestions["lsl"] = spec_lower_value

    return {
        "file": file_name,
        "_file_path": file_path,
        "rows": num_rows,
        "columns": columns_info,
        "pipeline": pipeline,
        "suggestions": suggestions,
    }
