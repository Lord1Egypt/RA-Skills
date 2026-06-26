#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一入口：支持 pdf/doc/docx/xls/xlsx/csv/txt/json，预处理后执行本质控点。"""

import argparse
import sys
from pathlib import Path

RULE_KEY = "missing-tumor-name"

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_ROOT = SCRIPT_DIR.parents[3]
_preprocess_dir = SKILLS_ROOT / "_shared" / "doc-preprocess" / "scripts"
for p in (_preprocess_dir, SCRIPT_DIR):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)

from preprocess import (  # noqa: E402
    PreprocessError,
    SUPPORTED_FILE_TYPES,
    detect_input_type,
    load_input_artifact,
)
from emr_qc_impl import DEFAULT_LLM_BASE, DEFAULT_LLM_MODEL, run_qc  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "病历内涵质控（未记录肿瘤名称）：支持 pdf/doc/docx/xls/xlsx/csv/txt/json，"
            "预处理为文本后调用医疗大模型。"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--input", required=True, help="输入文件路径。")
    parser.add_argument(
        "--input-type",
        default="auto",
        choices=["auto", *sorted(SUPPORTED_FILE_TYPES)],
        help="输入类型；默认 auto（自动识别）。",
    )
    parser.add_argument("--sheet", default="", help="读取 Excel 时指定 sheet（可选）。")
    parser.add_argument("--encoding", default="utf-8", help="txt/csv 编码（默认：utf-8）。")
    parser.add_argument(
        "--appkey", required=True,
        help="调用内部医疗大模型的鉴权 key，由平台分配。",
    )
    parser.add_argument(
        "--base", default=DEFAULT_LLM_BASE,
        help=f"大模型 base URL（默认：{DEFAULT_LLM_BASE}）。",
    )
    parser.add_argument(
        "--model", default=DEFAULT_LLM_MODEL,
        help=f"模型名称（默认：{DEFAULT_LLM_MODEL}）。",
    )
    parser.add_argument("--timeout", type=int, default=0, help="HTTP 超时秒数；0 表示一直等待（默认：0）。")
    parser.add_argument("--output", default="", help="输出文件路径（默认自动生成）。")
    parser.add_argument("--save-prepared", action="store_true", help="保存预处理后的文本，便于调试。")
    return parser.parse_args()


def extract_text(path: Path, input_type: str, encoding: str, sheet: str) -> str:
    import json as _json
    artifact = load_input_artifact(path, input_type, encoding, sheet, pdf_as_single_text=True)
    kind = artifact["kind"]
    if kind == "text":
        return artifact["text"]
    if kind == "json":
        data = artifact["data"]
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            for key in ("record", "text", "content"):
                v = data.get(key)
                if isinstance(v, str) and v.strip():
                    return v
        return _json.dumps(data, ensure_ascii=False)
    if kind == "tables":
        rows_text = []
        for table in artifact.get("tables", []):
            for row in table.get("rows", []):
                rows_text.append("\t".join(str(c) for c in row))
        return "\n".join(rows_text)
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"✗ Error: Input file not found: {input_path}", file=sys.stderr)
        return 1

    try:
        input_type = detect_input_type(input_path, args.input_type)
        record_text = extract_text(input_path, input_type, args.encoding, args.sheet)
    except PreprocessError as e:
        print(f"✗ Preprocess Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Preprocess Unexpected Error: {e}", file=sys.stderr)
        return 1

    if args.save_prepared:
        save_dir = Path(args.output).parent if args.output else Path("..") / "runs" / "med-emr-qc"
        save_dir.mkdir(parents=True, exist_ok=True)
        prep_path = save_dir / f"{RULE_KEY}.prepared.txt"
        prep_path.write_text(record_text, encoding="utf-8")
        print(f"✓ 预处理文本已保存至：{prep_path}")

    try:
        run_qc(
            record=record_text,
            appkey=args.appkey,
            base=args.base,
            model=args.model,
            timeout=args.timeout,
            output_path=args.output or None,
        )
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
