#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ICD_DRG_DIR = SCRIPT_DIR.parents[1]
SKILLS_ROOT = SCRIPT_DIR.parents[3]
PREPROCESS_DIR = SKILLS_ROOT / "_shared" / "doc-preprocess" / "scripts"
if str(PREPROCESS_DIR) not in sys.path:
    sys.path.insert(0, str(PREPROCESS_DIR))
if str(ICD_DRG_DIR) not in sys.path:
    sys.path.insert(0, str(ICD_DRG_DIR))
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from preprocess import PreprocessError, SUPPORTED_FILE_TYPES, detect_input_type, load_input_artifact
from surgery_review import DEFAULT_LLM_BASE, DEFAULT_LLM_MODEL, review_surgery_payload


def extract_text(path: Path, input_type: str, encoding: str, sheet: str) -> str:
    artifact = load_input_artifact(path, input_type, encoding, sheet, pdf_as_single_text=True)
    kind = artifact["kind"]
    if kind == "text":
        return str(artifact.get("text") or "")
    if kind == "json":
        data = artifact["data"]
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            for key in ("record", "text", "content"):
                value = data.get(key)
                if isinstance(value, str) and value.strip():
                    return value
        return json.dumps(data, ensure_ascii=False)
    if kind == "tables":
        rows_text: list[str] = []
        for table in artifact.get("tables", []):
            for row in table.get("rows", []):
                rows_text.append("\t".join(str(cell) for cell in row))
        return "\n".join(rows_text)
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def load_record_payload(path: Path, input_type: str, encoding: str, sheet: str) -> dict[str, Any]:
    resolved_type = detect_input_type(path, input_type)
    artifact = load_input_artifact(path, resolved_type, encoding, sheet, pdf_as_single_text=True)
    if artifact.get("kind") == "json" and isinstance(artifact.get("data"), dict):
        data = artifact["data"]
        if isinstance(data.get("record"), dict):
            return data
        if any(key in data for key in ("docs", "diagnosis", "surgery", "hospitalId", "serialNum")):
            return {"record": data}
    text = extract_text(path, resolved_type, encoding, sheet)
    if not text.strip():
        raise PreprocessError("预处理后病历文本为空")
    return {
        "record": {
            "hospitalId": "",
            "serialNum": path.stem,
            "docs": [{"docName": "完整病历", "fileName": path.name, "docClassName": "完整病历", "content": text}],
            "diagnosis": {},
            "surgery": {},
        }
    }


def record_to_prepared_text(payload: dict[str, Any]) -> str:
    docs = (payload.get("record") or {}).get("docs") or []
    chunks: list[str] = []
    for index, doc in enumerate(docs, start=1):
        if not isinstance(doc, dict):
            continue
        title = str(doc.get("docName") or doc.get("fileName") or doc.get("docClassName") or f"文书{index}")
        content = str(doc.get("content") or "").strip()
        if content:
            chunks.append(f"【{title}】\n{content}")
    return "\n\n".join(chunks)


def save_prepared(payload: dict[str, Any], output_json: str, input_path: Path) -> None:
    save_dir = Path(output_json).parent if output_json else ICD_DRG_DIR / "runs" / "surgery-review"
    save_dir.mkdir(parents=True, exist_ok=True)
    prepared_path = save_dir / f"{input_path.stem}.prepared.txt"
    prepared_path.write_text(record_to_prepared_text(payload), encoding="utf-8")
    print(f"Prepared text saved to: {prepared_path}", file=sys.stderr)


def parse_candidate_items(values: list[str], *, default_role: str = "other") -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for value in values:
        parts = [part.strip() for part in str(value or "").strip().split("|")]
        if not parts or not parts[0]:
            continue
        if len(parts) >= 3:
            role, code, name = parts[0], parts[1], "|".join(parts[2:]).strip()
        elif len(parts) == 2:
            role, code, name = default_role, parts[0], parts[1]
        else:
            role, code, name = default_role, "", parts[0]
        items.append({"role": role or default_role, "code": code, "name": name})
    return items


def parse_candidate_json(value: str) -> Any:
    raw = str(value or "").strip()
    if not raw:
        return None
    path = Path(raw)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(raw)


def merge_candidate_args(json_value: str, repeated_values: list[str], *, default_role: str = "other") -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    parsed = parse_candidate_json(json_value) if json_value else None
    if isinstance(parsed, dict):
        for key in ("diagnoses", "surgeries", "items", "candidates"):
            if isinstance(parsed.get(key), list):
                parsed = parsed[key]
                break
    if isinstance(parsed, list):
        for item in parsed:
            if isinstance(item, dict):
                code = str(item.get("code") or "").strip()
                name = str(item.get("name") or item.get("label") or "").strip()
                role = str(item.get("role") or default_role).strip() or default_role
                if code or name:
                    items.append({"role": role, "code": code, "name": name})
            elif isinstance(item, str):
                items.extend(parse_candidate_items([item], default_role=default_role))
    elif parsed is not None:
        raise ValueError("候选列表 JSON 必须是数组或包含数组字段的对象")
    items.extend(parse_candidate_items(repeated_values, default_role=default_role))
    return items


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="手术/操作编码审核统一入口：支持 pdf/doc/docx/xls/xlsx/csv/txt/json 输入。")
    parser.add_argument("--input", required=True, help="输入病历文件路径。")
    parser.add_argument("--input-type", default="auto", choices=["auto", *sorted(SUPPORTED_FILE_TYPES)], help="输入类型；默认 auto。")
    parser.add_argument("--sheet", default="", help="读取 Excel 时指定 sheet（可选）。")
    parser.add_argument("--encoding", default="utf-8", help="txt/csv 编码（默认：utf-8）。")
    parser.add_argument("--surgery", action="append", default=[], help="待审核手术/操作，格式 role|code|name 或 code|name；可重复。")
    parser.add_argument("--surgeries-json", default="", help="待审核手术/操作 JSON 字符串或文件路径。")
    parser.add_argument("--base", default=DEFAULT_LLM_BASE, help=f"内部大模型 base URL（默认：{DEFAULT_LLM_BASE}）。")
    parser.add_argument("--model", default=DEFAULT_LLM_MODEL, help=f"模型名称（默认：{DEFAULT_LLM_MODEL}）。")
    parser.add_argument("--timeout", type=int, default=0, help="HTTP 超时秒数；0 表示一直等待（默认：0）。")
    parser.add_argument("--appkey", required=True, help="内部医疗大模型鉴权 key，由平台分配；调用时必填，使用 Bearer 鉴权。")
    parser.add_argument("--no-llm", action="store_true", help="禁用 LLM，仅使用本地回退逻辑。")
    parser.add_argument("--output-json", default="", help="输出 JSON 文件路径（可选；优先于 --output）。")
    parser.add_argument("--output", default="", help="输出 JSON 文件路径（可选；兼容旧调用方式，等同于 --output-json）。")
    parser.add_argument("--save-prepared", action="store_true", help="保存预处理后的病历文本，便于调试。")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        return 1
    try:
        payload = load_record_payload(input_path, args.input_type, args.encoding, args.sheet)
        if args.save_prepared:
            save_prepared(payload, args.output_json or args.output, input_path)
        surgeries = merge_candidate_args(args.surgeries_json, args.surgery, default_role="other")
        if surgeries:
            payload["surgeries"] = surgeries
        payload.update({"base": args.base, "model": args.model, "timeout": args.timeout, "appkey": args.appkey, "use_llm": not args.no_llm})
        response = review_surgery_payload(payload)
    except (PreprocessError, Exception) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(response, ensure_ascii=False, indent=2)
    output_path = args.output_json or args.output
    if output_path:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
