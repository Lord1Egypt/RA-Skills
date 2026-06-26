#!/usr/bin/env python3
"""
sheet-agent core script

Capabilities:
- Spreadsheet reading and comprehension
- Anomaly detection
- Natural-language business queries
- Safe change previews
- Daily and weekly summary generation

Core principle:
Never write blindly. Show a preview first and execute changes only after the
user explicitly confirms them.
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


def _check_deps() -> None:
    missing = []
    try:
        import pandas as pd  # noqa: F401
    except ImportError:
        missing.append("pandas")
    try:
        import openpyxl  # noqa: F401
    except ImportError:
        missing.append("openpyxl")
    if missing:
        print(
            f"[sheet-agent] Missing dependencies: {', '.join(missing)}. "
            "Install them with: pip install pandas openpyxl"
        )
        sys.exit(1)


_check_deps()

import openpyxl  # noqa: E402,F401
import pandas as pd  # noqa: E402


BACKUP_DIR = Path(__file__).parent.parent / "backup"
SKILL_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = SKILL_DIR / "templates"


ORDER_TERMS = ["order", "\u8ba2\u5355", "\u9500\u552e\u989d", "\u4ea4\u6613"]
INVENTORY_TERMS = ["inventory", "\u5e93\u5b58", "\u5546\u54c1", "product"]
LEAD_TERMS = [
    "lead",
    "customer",
    "follow up",
    "phone",
    "\u7ebf\u7d22",
    "\u5ba2\u6237",
    "\u8ddf\u8fdb",
]
DAILY_LOG_TERMS = ["daily", "log", "\u65e5\u62a5", "\u65e5\u5fd7", "\u53f0\u8d26"]
DATE_TERMS = [
    "date",
    "time",
    "datetime",
    "\u65e5\u671f",
    "\u65f6\u95f4",
    "\u8ddf\u8fdb\u65e5\u671f",
    "\u5f55\u5165\u65e5\u671f",
    "\u521b\u5efa\u65f6\u95f4",
]
AMOUNT_TERMS = [
    "amount",
    "total",
    "price",
    "quantity",
    "\u91d1\u989d",
    "\u9500\u552e\u989d",
    "\u603b\u4ef7",
    "\u6570\u91cf",
]
STATUS_TERMS = ["status", "level", "type", "tier", "\u72b6\u6001", "\u7b49\u7ea7", "\u7c7b\u578b", "\u5ba2\u6237\u7b49\u7ea7"]
COUNT_TERMS = ["count", "how many", "total records", "\u7edf\u8ba1", "\u5408\u8ba1", "\u603b\u548c", "\u6709\u591a\u5c11", "\u603b\u5171"]
REPORT_TERMS = ["weekly report", "daily report", "summary", "report", "\u5468\u62a5", "\u65e5\u62a5", "\u6458\u8981", "\u603b\u7ed3", "\u6c47\u603b"]
ANOMALY_TERMS = ["issue", "problem", "anomaly", "abnormal", "\u5f02\u5e38", "\u95ee\u9898"]
FOLLOW_UP_TERMS = ["followed up", "follow up", "pending", "contact", "reply", "\u8ddf\u8fdb", "\u672a\u5904\u7406", "\u5f85\u8054\u7cfb", "\u672a\u56de\u590d"]
CHANGE_VERBS = ["change", "set", "update", "modify", "\u6539\u6210", "\u53d8\u4e3a", "\u4fee\u6539"]
CONFIRM_WORDS = ["confirm", "\u786e\u8ba4"]
CANCEL_WORDS = ["cancel", "\u53d6\u6d88"]
ID_TERMS = ["id", "no.", "no", "\u7f16\u53f7", "\u8ba2\u5355\u53f7", "\u5e8f\u53f7"]


def contains_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term.lower() in lowered for term in terms)


def expand_path(path_str: str) -> Path:
    """Expand user home and relative segments to an absolute path."""
    return Path(os.path.expanduser(path_str)).resolve()


def ensure_backup_dir() -> None:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def backup_file(file_path: Path) -> Path:
    """Back up a file to the skill-local backup directory."""
    ensure_backup_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.stem}_{ts}{file_path.suffix}"
    backup_path = BACKUP_DIR / backup_name
    shutil.copy2(file_path, backup_path)
    return backup_path


def read_table(file_path: Path) -> pd.DataFrame:
    """Read a CSV or Excel file and return it as a DataFrame."""
    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        for encoding in ("utf-8", "gbk", "latin1"):
            try:
                return pd.read_csv(file_path, encoding=encoding)
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Failed to decode CSV file: {file_path}")
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(file_path, engine="openpyxl")
    raise ValueError(
        f"Unsupported file format: {suffix}. Only CSV and Excel "
        "(.xlsx/.xls) are supported."
    )


def get_table_info(df: pd.DataFrame) -> dict:
    """Analyze spreadsheet structure and return metadata."""
    info = {
        "rows": len(df),
        "cols": len(df.columns),
        "col_names": list(df.columns),
        "col_types": {},
        "has_empty": df.isnull().any().any(),
        "empty_counts": df.isnull().sum().to_dict(),
        "table_type": infer_table_type(df),
    }
    for col in df.columns:
        info["col_types"][col] = str(df[col].dtype)
    return info


def infer_table_type(df: pd.DataFrame) -> str:
    """Infer a business-oriented spreadsheet type from column names."""
    col_text = " ".join(str(col).lower() for col in df.columns)
    if contains_any(col_text, ORDER_TERMS):
        return "Orders"
    if contains_any(col_text, INVENTORY_TERMS):
        return "Inventory"
    if contains_any(col_text, LEAD_TERMS):
        return "Sales leads"
    if contains_any(col_text, DAILY_LOG_TERMS):
        return "Daily log"
    return "General spreadsheet"


def detect_anomalies(df: pd.DataFrame) -> list[dict]:
    """Detect missing values, negatives, duplicate IDs, and date outliers."""
    anomalies: list[dict] = []

    for col in df.columns:
        null_rows = df[df[col].isnull()]
        if not null_rows.empty:
            for idx in null_rows.index[:5]:
                row_num = idx + 2
                anomalies.append(
                    {
                        "type": "Missing value",
                        "row": row_num,
                        "col": col,
                        "detail": f"Row {row_num} [{col}] is empty",
                    }
                )

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            negative_rows = df[df[col] < 0]
            if not negative_rows.empty:
                for idx in negative_rows.index[:5]:
                    row_num = idx + 2
                    value = df.loc[idx, col]
                    anomalies.append(
                        {
                            "type": "Negative value",
                            "row": row_num,
                            "col": col,
                            "value": float(value),
                            "detail": f"Row {row_num} [{col}] = {value} (negative)",
                        }
                    )

    id_col = find_first_matching_column(df, ID_TERMS)
    if id_col:
        dup_ids = df[df[id_col].duplicated(keep=False)]
        dup_ids = dup_ids[dup_ids[id_col].notnull()]
        if not dup_ids.empty:
            for idx in dup_ids.index[:5]:
                row_num = idx + 2
                value = df.loc[idx, id_col]
                anomalies.append(
                    {
                        "type": "Duplicate ID",
                        "row": row_num,
                        "col": id_col,
                        "value": str(value),
                        "detail": f"Row {row_num} [{id_col}] = {value} is duplicated",
                    }
                )

    for col in df.columns:
        if column_matches(col, DATE_TERMS):
            try:
                parsed = pd.to_datetime(df[col], errors="coerce")
                future_rows = df[parsed > pd.Timestamp(datetime.now() + timedelta(days=1))]
                if not future_rows.empty:
                    for idx in future_rows.index[:3]:
                        row_num = idx + 2
                        value = df.loc[idx, col]
                        anomalies.append(
                            {
                                "type": "Date anomaly",
                                "row": row_num,
                                "col": col,
                                "value": str(value),
                                "detail": f"Row {row_num} [{col}] = {value} is in the future",
                            }
                        )
            except Exception:
                pass

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) and df[col].max() > 0:
            q99 = df[col].quantile(0.99)
            if q99 > 0 and df[col].max() > q99 * 10:
                outliers = df[df[col] > q99 * 10]
                for idx in outliers.index[:3]:
                    row_num = idx + 2
                    value = df.loc[idx, col]
                    anomalies.append(
                        {
                            "type": "Outlier",
                            "row": row_num,
                            "col": col,
                            "value": float(value),
                            "detail": (
                                f"Row {row_num} [{col}] = {value} is far outside the "
                                "normal range"
                            ),
                        }
                    )

    return anomalies


def column_matches(column_name: str, terms: list[str]) -> bool:
    text = str(column_name).lower()
    return any(term.lower() in text for term in terms)


def find_first_matching_column(df: pd.DataFrame, terms: list[str]) -> Optional[str]:
    for col in df.columns:
        if column_matches(str(col), terms):
            return str(col)
    return None


def _extract_number(pattern: re.Pattern[str], query: str) -> Optional[int]:
    match = pattern.search(query)
    if not match:
        return None
    for group in match.groups():
        if group:
            return int(group)
    return None


def parse_natural_query(df: pd.DataFrame, query: str) -> dict:
    """Parse a natural-language instruction into an action plan."""
    q = query.strip()
    q_lower = q.lower()

    overdue_days = _extract_number(
        re.compile(
            r"(?:more than|over)\s*(\d+)\s*days?|"
            r"\u8d85\u8fc7?(\d+)[\u5929\u65e5]"
        ),
        q_lower,
    )
    if overdue_days is not None and contains_any(q_lower, FOLLOW_UP_TERMS):
        date_col = find_date_column(df)
        if date_col:
            return {
                "action": "query",
                "description": f"Records without follow-up for more than {overdue_days} days",
                "date_col": date_col,
                "days": overdue_days,
            }

    threshold = _extract_number(
        re.compile(
            r"(?:greater than|more than|above)\s*(\d+)|"
            r"\u91d1\u989d[\u662f\u4e3a\u5927\u4e8e\u7ea6]+(\d+)|"
            r"\u5927\u4e8e?(\d+)"
        ),
        q_lower,
    )
    if threshold is not None and contains_any(q_lower, AMOUNT_TERMS):
        amount_col = find_amount_column(df)
        if amount_col:
            return {
                "action": "query",
                "description": f"{amount_col} greater than {threshold}",
                "amount_col": amount_col,
                "threshold": threshold,
            }

    status_match = re.search(
        r"(?:status|level|type|tier)\s*(?:is|=)\s*([^\s,.!?]+)|"
        r"[\u662f\u4e3a]([^\uff0c,\u3002\uff01]+)",
        q,
        re.IGNORECASE,
    )
    if status_match and contains_any(q_lower, STATUS_TERMS):
        keyword = next(group for group in status_match.groups() if group).strip()
        for col in df.columns:
            if column_matches(str(col), STATUS_TERMS):
                return {
                    "action": "query",
                    "description": f"{col} contains {keyword}",
                    "filter_col": str(col),
                    "filter_value": keyword,
                }

    if contains_any(q_lower, COUNT_TERMS):
        amount_col = find_amount_column(df)
        if amount_col:
            return {
                "action": "aggregate",
                "amount_col": amount_col,
                "description": "Numeric summary",
            }
        return {"action": "count", "description": "Record count"}

    if contains_any(q_lower, REPORT_TERMS):
        report_type = "weekly" if ("week" in q_lower or "\u5468" in q_lower) else "daily"
        return {
            "action": "report",
            "report_type": report_type,
            "description": f"{report_type.title()} operations summary",
        }

    if contains_any(q_lower, ANOMALY_TERMS):
        return {"action": "anomalies", "description": "Anomaly scan"}

    row_match = re.search(
        r"(?:row|line)\s*(\d+).*?(?:to|=)\s*([^\n,.!?]+)|"
        r"\u7b2c(\d+)[\u884c\u4e2a].*?[\u6539\u6210\u53d8\u4e3a=]([^\uff0c,\u3002]+)",
        q,
        re.IGNORECASE,
    )
    if row_match and contains_any(q_lower, CHANGE_VERBS):
        row_group = row_match.group(1) or row_match.group(3)
        value_group = row_match.group(2) or row_match.group(4)
        row_num = int(row_group)
        new_value = value_group.strip()
        col = find_target_column(q, df)
        return {
            "action": "preview_change",
            "row": row_num,
            "col": col,
            "new_value": new_value,
        }

    return {"action": "info", "description": "Spreadsheet overview"}


def find_date_column(df: pd.DataFrame) -> Optional[str]:
    return find_first_matching_column(df, DATE_TERMS)


def find_amount_column(df: pd.DataFrame) -> Optional[str]:
    for col in df.columns:
        if column_matches(str(col), AMOUNT_TERMS) and pd.api.types.is_numeric_dtype(df[col]):
            return str(col)
    return None


def find_target_column(query: str, df: pd.DataFrame) -> str:
    """Find the most likely target column for a change instruction."""
    query_lower = query.lower()
    for col in df.columns:
        col_text = str(col)
        if col_text.lower() in query_lower:
            return col_text
    for col in df.columns:
        if df[col].dtype == "object":
            return str(col)
    return str(df.columns[0])


def execute_query(df: pd.DataFrame, query_plan: dict) -> pd.DataFrame:
    """Execute a structured query plan against a DataFrame."""
    action = query_plan.get("action")

    if action == "query":
        if "date_col" in query_plan and "days" in query_plan:
            date_col = query_plan["date_col"]
            try:
                parsed = pd.to_datetime(df[date_col], errors="coerce")
                cutoff = datetime.now() - timedelta(days=query_plan["days"])
                return df[parsed < pd.Timestamp(cutoff)].copy()
            except Exception:
                return df.head(0)
        if "amount_col" in query_plan:
            col = query_plan["amount_col"]
            return df[df[col] > query_plan["threshold"]].copy()
        if "filter_col" in query_plan:
            col = query_plan["filter_col"]
            value = query_plan["filter_value"]
            return df[df[col].astype(str).str.contains(value, na=False)].copy()

    return df.copy()


def build_change_preview(df: pd.DataFrame, row: int, col: str, new_value: str) -> dict:
    """Build a change preview without writing anything to disk."""
    df_index = row - 2
    if df_index < 0 or df_index >= len(df):
        return {"error": f"Row {row} is out of range. The sheet has {len(df)} data rows."}

    old_value = df.iloc[df_index][col]
    return {
        "file_modified": False,
        "preview": {
            "row": row,
            "col": col,
            "old_value": str(old_value),
            "new_value": new_value,
        },
    }


def apply_change(df: pd.DataFrame, row: int, col: str, new_value: str) -> pd.DataFrame:
    """Apply a change to a DataFrame copy and return the modified copy."""
    df_index = row - 2
    updated = df.copy()
    old_dtype = updated[col].dtype
    try:
        if old_dtype in ["int64", "int32"]:
            updated.at[df_index, col] = int(new_value)
        elif old_dtype in ["float64", "float32"]:
            updated.at[df_index, col] = float(new_value)
        else:
            updated.at[df_index, col] = new_value
    except (ValueError, TypeError):
        updated.at[df_index, col] = new_value
    return updated


def save_table(df: pd.DataFrame, file_path: Path) -> Path:
    """Save a DataFrame back to disk after creating a backup."""
    backup_file(file_path)
    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        df.to_csv(file_path, index=False, encoding="utf-8")
    else:
        df.to_excel(file_path, index=False, engine="openpyxl")
    return file_path


def generate_report(df: pd.DataFrame, report_type: str = "weekly") -> str:
    """Generate a lightweight daily or weekly operations summary."""
    lines: list[str] = []
    today = datetime.now()

    if report_type == "weekly":
        lines.append(f"📈 Operations Summary — {today.strftime('%B %Y')}")
    else:
        lines.append(f"📅 Daily Summary — {today.strftime('%Y-%m-%d')}")
    lines.append("")

    lines.append("[Overview]")
    lines.append(f"- Total records: {len(df)}")

    amount_col = find_amount_column(df)
    if amount_col:
        total = df[amount_col].sum()
        avg = df[amount_col].mean()
        lines.append(f"- {amount_col} total: {total:,.2f}")
        lines.append(f"- {amount_col} average: {avg:,.2f}")

    lines.append("")

    str_cols = [col for col in df.columns if df[col].dtype == "object"]
    if str_cols:
        top_col = str_cols[0]
        if df[top_col].nunique() <= 20:
            lines.append("[Top distribution]")
            for value, count in df[top_col].value_counts().head(5).items():
                lines.append(f"- {value}: {count} records")
            lines.append("")

    null_total = int(df.isnull().sum().sum())
    if null_total > 0:
        lines.append("[Data quality]")
        lines.append(f"- Missing values: {null_total}")
        lines.append("")

    anomalies = detect_anomalies(df)
    if anomalies:
        summary: dict[str, int] = {}
        for anomaly in anomalies:
            summary[anomaly["type"]] = summary.get(anomaly["type"], 0) + 1
        lines.append("[Anomalies]")
        for anomaly_type, count in summary.items():
            lines.append(f"- {anomaly_type}: {count}")
        lines.append("")

    return "\n".join(lines).rstrip()


def format_query_result(df: pd.DataFrame, description: str = "") -> str:
    """Format query results as compact markdown-friendly text."""
    if df.empty:
        return "📭 No matching records found."

    lines = [f"📊 Query results: {len(df)} record(s)"]
    if description:
        lines.append(f"({description})")
    lines.append("")
    lines.append(df_to_markdown(df.head(20)))
    if len(df) > 20:
        lines.append(f"\n... {len(df) - 20} more record(s) not shown")
    return "\n".join(lines)


def format_anomalies(anomalies: list[dict]) -> str:
    """Format anomaly results for terminal or chat output."""
    if not anomalies:
        return "✅ No obvious anomalies found."

    lines = [f"⚠️ Found {len(anomalies)} anomaly/anomalies:", ""]
    for index, anomaly in enumerate(anomalies[:10], 1):
        lines.append(f"{index}. {anomaly['detail']}")
    if len(anomalies) > 10:
        lines.append(f"\n... {len(anomalies) - 10} more anomaly/anomalies not shown")
    return "\n".join(lines)


def format_table_info(info: dict) -> str:
    """Format spreadsheet metadata as readable text."""
    lines = [
        f"📋 Columns: {info['col_names']}",
        f"📐 Size: {info['rows']} rows × {info['cols']} columns",
        f"🏷️ Inferred type: {info['table_type']}",
    ]
    if info["has_empty"]:
        lines.append(f"⚠️ Missing values present: {sum(info['empty_counts'].values())}")
    return "\n".join(lines)


def df_to_markdown(df: pd.DataFrame) -> str:
    """Render a DataFrame as a markdown table."""
    cols = df.columns.tolist()
    lines = [
        "| " + " | ".join(str(col) for col in cols) + " |",
        "| " + " | ".join(["---"] * len(cols)) + " |",
    ]
    for _, row in df.iterrows():
        values = []
        for value in row:
            rendered = str(value) if pd.notna(value) else "(empty)"
            values.append(rendered[:30])
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def main(args: list = None) -> None:
    """
    Entry point.

    Supported invocation styles:
    1. CLI: python sheet_agent.py <file_path> <query>
    2. JSON params: python sheet_agent.py '{"file":"~/x.csv","query":"..."}'
    """
    if args is None:
        args = sys.argv[1:]

    if len(args) >= 1 and os.path.exists(os.path.expanduser(args[0])):
        file_path = expand_path(args[0])
        query = args[1] if len(args) > 1 else ""
        action = "query"
    else:
        try:
            params = json.loads(" ".join(args))
            file_path = expand_path(params["file"])
            query = params.get("query", "")
            action = params.get("action", "query")
        except Exception:
            print("Usage: python sheet_agent.py <file_path> <query>")
            print('   or: python sheet_agent.py \'{"file":"~/x.csv","query":"..."}\'')
            sys.exit(1)

    try:
        df = read_table(file_path)
    except Exception as exc:
        print(f"[sheet-agent] Failed to read file: {exc}")
        sys.exit(1)

    if not query and action == "query":
        info = get_table_info(df)
        print(format_table_info(info))
        print("")
        print(format_anomalies(detect_anomalies(df)))
        return

    plan = parse_natural_query(df, query)
    action = plan.get("action", "info")

    if action == "info":
        print(format_table_info(get_table_info(df)))
    elif action == "query":
        print(format_query_result(execute_query(df, plan), plan.get("description", "")))
    elif action == "aggregate":
        amount_col = plan.get("amount_col")
        if amount_col:
            print("📊 Numeric summary:")
            print(f"- Total: {df[amount_col].sum():,.2f}")
            print(f"- Average: {df[amount_col].mean():,.2f}")
            print(f"- Max: {df[amount_col].max():,.2f}")
            print(f"- Min: {df[amount_col].min():,.2f}")
    elif action == "count":
        print(f"📊 Total records: {len(df)}")
    elif action == "report":
        print(generate_report(df, plan.get("report_type", "weekly")))
    elif action == "anomalies":
        print(format_anomalies(detect_anomalies(df)))
    elif action == "preview_change":
        preview = build_change_preview(df, plan["row"], plan["col"], plan["new_value"])
        if "error" in preview:
            print(f"❌ {preview['error']}")
        else:
            details = preview["preview"]
            print("📝 Proposed change preview:")
            print(f"Row: {details['row']}")
            print(f"Field: {details['col']}")
            print(f"Old value: {details['old_value']}")
            print(f"New value: {details['new_value']}")
            print("")
            print('⚠️ Confirm execution? Reply "confirm" or "cancel".')

    anomalies = detect_anomalies(df)
    if anomalies and action not in ["preview_change", "anomalies"]:
        print("")
        print(format_anomalies(anomalies))


if __name__ == "__main__":
    main()
