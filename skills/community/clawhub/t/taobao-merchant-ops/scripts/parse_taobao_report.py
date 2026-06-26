"""
淘宝生意参谋报表解析器
按 mapping.final.json 规则解析Excel输出结构化JSON
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from app_config import load_runtime_config
from app_errors import ParseError
from parser_utils import compute_expression, load_workbook_data, safe_number

# Force UTF-8
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load_mapping(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Parse Taobao Excel report into JSON")
    parser.add_argument("--config", default="", help="Path to settings.json")
    parser.add_argument("--mapping-path", default="", help="Path to mapping.final.json")
    parser.add_argument("--excel-dir", default="", help="Directory containing xlsx downloads")
    parser.add_argument("--output-dir", default="", help="Directory for parsed output")
    parser.add_argument("--excel-path", default="", help="Specific Excel file to parse")
    parser.add_argument("--output-name", default="taobao_parsed.json", help="Output JSON filename")
    return parser.parse_args()


def pick_latest_excel(excel_dir: Path) -> Path:
    files = [p for p in excel_dir.iterdir() if p.suffix.lower() == ".xlsx"]
    if not files:
        raise ParseError(f"No Excel files found in: {excel_dir}")
    return max(files, key=lambda p: p.stat().st_mtime)


def parse_excel(excel_path: str | Path, mapping: dict) -> tuple[dict, dict]:
    full_header_map, data_row = load_workbook_data(excel_path)

    def get_val(col_name: str):
        idx = full_header_map.get(col_name)
        if idx is None or idx >= len(data_row):
            return None
        return safe_number(data_row[idx])

    raw_data = {col: get_val(col) for col in full_header_map}
    result: dict[str, object] = {}

    for out_key, in_key in mapping.get("direct_mapping", {}).items():
        result[out_key] = raw_data.get(in_key)

    for out_key, in_key in mapping.get("renamed_mapping", {}).items():
        result[out_key] = raw_data.get(in_key)

    for out_key, config in mapping.get("computed_mapping", {}).items():
        deps = config.get("depends_on", [])
        eval_data = {k: raw_data.get(k) for k in deps}
        result[out_key] = compute_expression(config.get("expression", ""), eval_data)

    for key, value in result.items():
        result[key] = safe_number(value) if value is not None else None
    return result, raw_data


def main() -> int:
    args = parse_args()
    runtime = load_runtime_config(args.config or None)
    mapping_path = Path(args.mapping_path or runtime["mapping_path"])
    excel_dir = Path(args.excel_dir or runtime["downloads_dir"])
    output_dir = Path(args.output_dir or runtime["output_dir"])
    excel_path = Path(args.excel_path) if args.excel_path else pick_latest_excel(excel_dir)

    if not mapping_path.exists():
        raise ParseError(f"Mapping file not found: {mapping_path}")
    if not excel_path.exists():
        raise ParseError(f"Excel file not found: {excel_path}")

    started_at = time.time()
    mapping = load_mapping(mapping_path)
    print(f"Parsing: {excel_path.name}")
    parsed, raw = parse_excel(excel_path, mapping)

    output = {
        "schema_version": 1,
        "report_date": datetime.now().strftime("%Y-%m-%d"),
        "source_file": excel_path.name,
        "source_file_mtime": int(excel_path.stat().st_mtime),
        "mapping_path": str(mapping_path),
        "mapping_version": mapping.get("version", "unknown"),
        "parse_duration_ms": int((time.time() - started_at) * 1000),
        "data": parsed,
        "raw_field_count": len(raw),
        "unmapped_count": len(mapping.get("unmapped_fields", [])),
        "unmapped_fields": mapping.get("unmapped_fields", []),
        "notes": mapping.get("notes", []),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / args.output_name
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== 解析结果 ({len(parsed)} fields) ===")
    for key, value in parsed.items():
        print(f"  {key}: {value}")
    print(f"\nOutput saved to: {out_path}")
    print("\n注意: 数据为空（NULL）通常表示 Excel 下载失败或模板变化。")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ParseError as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)
