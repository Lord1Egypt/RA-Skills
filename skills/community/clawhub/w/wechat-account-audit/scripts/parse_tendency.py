#!/usr/bin/env python3
"""
Parse WeChat Official Account tendency Excel file.

Usage:
    python3 parse_tendency.py <excel_path> [--output result.json]

Auto-detects column names from the header row and maps them to standardized keys.
Supports both .xls and .xlsx formats.
"""

import json
import sys
import argparse
from pathlib import Path


def detect_format(filepath: str) -> str:
    ext = Path(filepath).suffix.lower()
    if ext == ".xls":
        return "xls"
    elif ext == ".xlsx":
        return "xlsx"
    else:
        raise ValueError(f"Unsupported format: {ext}. Expected .xls or .xlsx")


def read_excel(filepath: str) -> list[dict]:
    fmt = detect_format(filepath)

    # Try openpyxl first (xlsx), fall back to xlrd (xls)
    rows = []
    headers = []

    if fmt == "xlsx":
        try:
            import openpyxl
        except ImportError:
            raise ImportError("openpyxl is required for .xlsx files. Install with: pip install openpyxl")

        wb = openpyxl.load_workbook(filepath, data_only=True)
        ws = wb.active

        for i, row in enumerate(ws.iter_rows(values_only=True)):
            row_vals = [str(cell) if cell is not None else "" for cell in row]
            if i == 0:
                headers = row_vals
            else:
                rows.append(dict(zip(headers, row_vals)))
        wb.close()

    else:  # xls
        try:
            import xlrd
        except ImportError:
            raise ImportError("xlrd is required for .xls files. Install with: pip install xlrd")

        wb = xlrd.open_workbook(filepath)
        ws = wb.sheet_by_index(0)

        for i in range(ws.nrows):
            row_vals = [str(ws.cell_value(i, j)).strip() for j in range(ws.ncols)]
            if i == 0:
                headers = row_vals
            else:
                rows.append(dict(zip(headers, row_vals)))

    return rows


# Column name mappings: known WeChat tendency Excel column names → standardized keys
COLUMN_MAP = {
    # Title
    "文章标题": "title",
    "标题": "title",

    # Publish date
    "发布时间": "publish_date",
    "发表时间": "publish_date",
    "时间": "publish_date",

    # Read count
    "阅读人数": "reads",
    "阅读量": "reads",
    "阅读": "reads",
    "阅读次数": "reads",

    # Share count
    "分享人数": "shares",
    "分享量": "shares",
    "分享": "shares",
    "分享次数": "shares",

    # Like count
    "点赞人数": "likes",
    "点赞": "likes",

    # Comment count
    "留言人数": "comments",
    "评论": "comments",

    # Favorite count
    "收藏人数": "favorites",
    "收藏": "favorites",
    "收藏量": "favorites",

    # Read-after-share (在看)
    "在看人数": "read_after_share",
    "在看": "read_after_share",

    # Channel / source
    "阅读渠道": "channel",
    "渠道": "channel",
    "来源": "channel",
    "阅读来源": "channel",

    # Main source
    "主要来源": "main_source",

    # URL
    "链接": "url",
    "文章链接": "url",

    # Reach count
    "送达人数": "delivery_count",

    # Read rate
    "阅读率": "read_rate",

    # Data date range
    "数据时间": "data_period",
    "统计时间": "data_period",
}


def normalize_row(row: dict) -> dict:
    """Map raw column names to standardized keys, drop unmapped columns."""
    normalized = {}
    for raw_key, value in row.items():
        key = raw_key.strip()
        if key in COLUMN_MAP:
            std_key = COLUMN_MAP[key]
            # Convert numeric strings
            if std_key in ("reads", "shares", "likes", "comments", "favorites",
                           "read_after_share", "delivery_count"):
                try:
                    normalized[std_key] = int(float(value))
                except (ValueError, TypeError):
                    normalized[std_key] = 0
            elif std_key == "read_rate":
                try:
                    normalized[std_key] = float(value.replace("%", ""))
                except (ValueError, TypeError):
                    normalized[std_key] = 0.0
            else:
                normalized[std_key] = value

    return normalized


def parse_channel_breakdown(channel_str: str) -> dict:
    """
    Parse WeChat's channel breakdown string.

    Example input: "公众号消息500次,朋友圈300次,聊天会话200次"
    Returns: {"公众号消息": 500, "朋友圈": 300, "聊天会话": 200}
    """
    if not channel_str or channel_str.isspace():
        return {}

    breakdown = {}
    parts = channel_str.replace("\n", ",").replace("，", ",").split(",")

    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Pattern: "渠道名123次" or "渠道名 123次" or "渠道名:123"
        import re
        match = re.match(r"(.+?)(\d+)次?", part)
        if match:
            name = match.group(1).strip().rstrip(":：")
            count = int(match.group(2))
            breakdown[name] = count

    return breakdown


def parse_tendency(filepath: str) -> list[dict]:
    """Main entry point: parse tendency Excel and return article list."""
    raw_rows = read_excel(filepath)

    articles = []
    for row in raw_rows:
        normalized = normalize_row(row)
        if not normalized.get("title"):
            continue  # Skip empty rows

        # Parse channel breakdown if present
        channel_str = ""
        # Check raw row for channel column
        for key, val in row.items():
            if key.strip() == "阅读渠道" or key.strip() == "渠道":
                channel_str = val
                break

        if channel_str:
            normalized["channel_breakdown"] = parse_channel_breakdown(channel_str)

        articles.append(normalized)

    return articles


def main():
    parser = argparse.ArgumentParser(
        description="Parse WeChat Official Account tendency Excel file"
    )
    parser.add_argument("excel_path", help="Path to the tendency Excel file (.xls or .xlsx)")
    parser.add_argument("--output", "-o", help="Output JSON file path (default: stdout)")
    parser.add_argument("--summary", "-s", action="store_true",
                        help="Print summary statistics")

    args = parser.parse_args()

    try:
        articles = parse_tendency(args.excel_path)
    except Exception as e:
        print(f"Error parsing Excel: {e}", file=sys.stderr)
        sys.exit(1)

    output = {
        "total_articles": len(articles),
        "articles": articles,
    }

    if args.summary:
        total_reads = sum(a.get("reads", 0) for a in articles)
        total_shares = sum(a.get("shares", 0) for a in articles)
        total_favorites = sum(a.get("favorites", 0) for a in articles)

        output["summary"] = {
            "total_reads": total_reads,
            "avg_reads": round(total_reads / len(articles), 1) if articles else 0,
            "total_shares": total_shares,
            "total_favorites": total_favorites,
        }

    json_str = json.dumps(output, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"Output written to {args.output}")
    else:
        print(json_str)


if __name__ == "__main__":
    main()
