#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
手术记录生成：将手术相关病历转换为规范手术记录文本。
LLM 调用使用公司内部医疗大模型。
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_ROOT = SCRIPT_DIR.parents[3]
PREPROCESS_DIR = SKILLS_ROOT / "_shared" / "doc-preprocess" / "scripts"
if str(PREPROCESS_DIR) not in sys.path:
    sys.path.insert(0, str(PREPROCESS_DIR))

from preprocess import PreprocessError, SUPPORTED_FILE_TYPES, detect_input_type, load_input_artifact


DEFAULT_LLM_BASE = "https://maas-api.hivoice.cn/v1"
DEFAULT_LLM_MODEL = "u1-insuremed"

OPERATION_RECORD_INSTRUCTIONS = """请你作为临床外科病历书写专家，严格依据提供的患者手术相关病历素材，生成一份规范、完整、专业的手术记录。手术记录需符合临床手术记录书写标准，内容真实忠于原文，无编造、无遗漏、无多余无关信息，医疗术语规范，逻辑严谨，语句通顺，结构完整。
核心生成要求及结构规范（务必严格遵守）：
1.  手术记录需包含以下核心模块（无遗漏）：手术日期、手术时间、手术地点、手术医生、助手、麻醉方式、手术名称、手术指征、术前诊断、术中诊断、手术经过、术中出现的情况及处理、术后情况、手术者签名。
2.  各模块生成规则：
（1）手术日期、时间、地点、手术医生、助手、麻醉方式：直接从提供的病历素材中抽取，原文提取，不修改、不新增。
（2）手术名称：以病历素材中明确的手术名称为准，完整书写，不得简写、漏写（含术式细节）。
（3）手术指征：结合术前诊断、患者症状及检查结果，从病历素材中提取相关信息，整理成规范的手术指征（说明为何需进行本次手术）。
（4）术前诊断、术中诊断：直接从病历素材中抽取，若术中诊断与术前诊断有差异，需完整保留两者，明确标注，不得遗漏。
（5）手术经过：这是核心模块，需严格按照手术操作顺序，从病历素材中抽取手术步骤、操作细节（消毒、铺巾、切口、术中操作、止血、缝合等），按时间顺序/操作顺序整理，语言简洁、专业，准确呈现手术全过程，无关键步骤遗漏，不添加素材中未提及的操作。
（6）术中出现的情况及处理：若素材中有相关记录，如实提取、整理；若未提及，需注明"术中未出现特殊异常情况，各项操作顺利"。
（7）术后情况：提取素材中术后患者的生命体征、切口情况、麻醉苏醒情况等，整理成规范表述，明确患者术后状态。
（8）手术者签名：提取素材中明确的手术者姓名，如实填写。
3.  额外要求：全程忠于提供的病历素材，不凭空捏造任何手术细节、病情信息；医疗术语使用规范，避免口语化；结构清晰，每个模块分段明确，便于阅读；若某模块素材中无相关信息，需注明"未提及"，不得随意编造。"""


def _read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("input JSON 必须是对象")
    return payload


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
            for key in ("record", "text", "content", "records"):
                value = data.get(key)
                if isinstance(value, str) and value.strip():
                    return value
            if "records" in data and isinstance(data["records"], list):
                return json.dumps(data, ensure_ascii=False)
        return json.dumps(data, ensure_ascii=False)
    if kind == "tables":
        rows_text: list[str] = []
        for table in artifact.get("tables", []):
            for row in table.get("rows", []):
                rows_text.append("\t".join(str(cell) for cell in row))
        return "\n".join(rows_text)
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def _format_records_body(records: list[Any]) -> str:
    parts: list[str] = []
    current_section = ""
    for record in records:
        section = str(record.get("section") or "").strip()
        content = str(record.get("content") or record.get("text") or "").strip()
        if section and section != current_section:
            current_section = section
            parts.append(f"#### {section}\n")
        if content:
            parts.append(f"{content}\n")
        parts.append("\n")
    return "".join(parts)


def _wrap_operation_prompt(record_body: str) -> str:
    return (
        f"{OPERATION_RECORD_INSTRUCTIONS}\n\n"
        f"患者手术相关病历\n{record_body}\n\n"
        "### 输出"
    )


def build_prompt(payload: dict[str, Any]) -> str:
    raw_prompt = str(payload.get("prompt") or "").strip()
    if raw_prompt:
        return raw_prompt

    records = payload.get("records")
    if records:
        return _wrap_operation_prompt(_format_records_body(records))

    record_text = str(payload.get("record") or payload.get("text") or payload.get("content") or "").strip()
    if not record_text.strip():
        raise ValueError("输入缺少 records 或 prompt")

    return _wrap_operation_prompt(record_text)


def build_payload_from_input(
    path: Path,
    *,
    input_type: str,
    encoding: str,
    sheet: str,
) -> dict[str, Any]:
    resolved_type = detect_input_type(path, input_type)
    if resolved_type == "json":
        try:
            payload = _read_json(path)
            if payload.get("prompt") or "records" in payload or payload.get("record") or payload.get("text"):
                return payload
        except Exception:
            pass

    record_text = extract_text(path, resolved_type, encoding, sheet)
    if not record_text.strip():
        raise PreprocessError("预处理后病历文本为空")
    return {
        "record": record_text,
    }


def payload_to_prepared_text(payload: dict[str, Any]) -> str:
    raw_prompt = str(payload.get("prompt") or "").strip()
    if raw_prompt:
        return raw_prompt

    records = payload.get("records")
    if records:
        return _format_records_body(records)

    record_text = str(payload.get("record") or payload.get("text") or payload.get("content") or "").strip()
    return record_text


def save_prepared(payload: dict[str, Any], output_path: str, input_path: Path) -> None:
    save_dir = Path(output_path).parent if output_path else SCRIPT_DIR.parents[1] / "runs" / "operation-record"
    save_dir.mkdir(parents=True, exist_ok=True)
    prepared_path = save_dir / f"{input_path.stem}.prepared.txt"
    prepared_path.write_text(payload_to_prepared_text(payload), encoding="utf-8")
    print(f"Prepared text saved to: {prepared_path}", file=sys.stderr)


def _http_post(url: str, payload: dict[str, Any], headers: dict[str, str], *, timeout: int = 0) -> Any:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json", **{key: value for key, value in headers.items() if value}},
    )
    try:
        opener = urllib.request.urlopen(req) if not timeout else urllib.request.urlopen(req, timeout=timeout)
        with opener as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


def call_llm(prompt: str, *, base: str, model: str, appkey: str, timeout: int) -> str:
    url = f"{base.rstrip('/')}/chat/completions"
    headers = {"Authorization": f"Bearer {appkey}"} if appkey else {}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
    }
    response = _http_post(url, payload, headers, timeout=timeout)
    try:
        return str(response["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"Unexpected LLM response: {response}") from exc


def run(payload: dict[str, Any], *, base: str, model: str, appkey: str, timeout: int) -> str:
    prompt = build_prompt(payload)
    return call_llm(prompt, base=base, model=model, appkey=appkey, timeout=timeout)


def main() -> int:
    parser = argparse.ArgumentParser(description="手术记录生成统一入口：支持 pdf/doc/docx/xls/xlsx/csv/txt/json 输入。")
    parser.add_argument("--input", required=True, help="输入病历文件路径。")
    parser.add_argument("--input-type", default="auto", choices=["auto", *sorted(SUPPORTED_FILE_TYPES)], help="输入类型；默认 auto。")
    parser.add_argument("--sheet", default="", help="读取 Excel 时指定 sheet（可选）。")
    parser.add_argument("--encoding", default="utf-8", help="txt/csv 编码（默认：utf-8）。")
    parser.add_argument("--base", default=DEFAULT_LLM_BASE, help=f"内部大模型 base URL（默认：{DEFAULT_LLM_BASE}）。")
    parser.add_argument("--model", default=DEFAULT_LLM_MODEL, help=f"模型名称（默认：{DEFAULT_LLM_MODEL}）。")
    parser.add_argument("--timeout", type=int, default=0, help="HTTP 超时秒数；0 表示一直等待（默认：0）。")
    parser.add_argument("--appkey", required=True, help="必须传入。内部医疗大模型鉴权 key，使用 Bearer 方式认证。")
    parser.add_argument("--output-json", default="", help="输出 JSON 文件路径（可选）。")
    parser.add_argument("--output", default="", help="输出手术记录文本文件路径（可选）。")
    parser.add_argument("--save-prepared", action="store_true", help="保存预处理后的文本，便于调试。")
    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        payload = build_payload_from_input(
            input_path,
            input_type=args.input_type,
            encoding=args.encoding,
            sheet=args.sheet,
        )
        if args.save_prepared:
            save_prepared(payload, args.output, input_path)
        response = run(
            payload,
            base=args.base,
            model=args.model,
            appkey=args.appkey,
            timeout=args.timeout,
        )
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    output_path = args.output or args.output_json
    if output_path:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(response, encoding="utf-8")
    print(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
