#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
出院记录生成：将住院病历转换为标准出院记录文本。
LLM 调用使用公司内部医疗大模型。
"""

from __future__ import annotations

import argparse
import json
import re
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


def build_prompt(payload: dict[str, Any]) -> str:
    raw_prompt = str(payload.get("prompt") or "").strip()
    if raw_prompt:
        return raw_prompt

    records = payload.get("records")
    if records:
        records_text = []
        current_section = ""
        for idx, record in enumerate(records):
            section = str(record.get("section") or "").strip()
            title = str(record.get("title") or "").strip()
            content = str(record.get("content") or record.get("text") or "").strip()
            
            if section and section != current_section:
                current_section = section
                records_text.append(f"#### {section}\n")
            
            if title:
                records_text.append(f"{title}:\n")
            if content:
                records_text.append(f"{content}\n")
            records_text.append("\n")
        
        return f"""你作为专业医疗病历整理专家，严格依据给定住院病历原文，按照固定规则生成标准出院记录，各字段数据源及生成规则如下：
1. 主诉：从入院记录中抽取「主诉」原文。
2. 入院情况：二选一生成
方案 1：①解析入院记录原始信息；②抽取既往史、家族史、系统查体**阳性内容**；③按规则整合生成入院情况；
方案 2：无方案 1 条件时，直接抽取首次病程记录中「病例特点」。
3. 入院诊断：从入院记录抽取「入院诊断/初步诊断」。
4. 诊疗经过：从首次病程、日常病程、手术操作记录、特殊检查记录中，抽取病情变化、检查检验、治疗处置、手术事件，按**时间线**整理概括生成。
5. 出院诊断：整合入院记录中「入院诊断/初步诊断、修正诊断、补充诊断」全部内容。
6. 出院情况：解析末次病程记录，剔除出院用药、检查、康复、生活指导、随诊建议，剩余内容整理为出院情况。
7. 出院医嘱：从末次病程记录提取出院用药、复查检查、康复训练、生活饮食、复诊随诊相关建议。

要求：**完全忠于原文、不编造、不臆造、不新增病情**，医疗术语规范，语句通顺，分段清晰，严格按七个字段输出。

### 患者原始病历文本
{''.join(records_text)}

### 输出
""".strip()

    # 从 JSON 的 record 或 text 字段获取
    record_text = str(payload.get("record") or payload.get("text") or payload.get("content") or "").strip()
    if not record_text.strip():
        raise ValueError("输入缺少 records 或 prompt")

    return f"""你作为专业医疗病历整理专家，严格依据给定住院病历原文，按照固定规则生成标准出院记录，各字段数据源及生成规则如下：
1. 主诉：从入院记录中抽取「主诉」原文。
2. 入院情况：二选一生成
方案 1：①解析入院记录原始信息；②抽取既往史、家族史、系统查体**阳性内容**；③按规则整合生成入院情况；
方案 2：无方案 1 条件时，直接抽取首次病程记录中「病例特点」。
3. 入院诊断：从入院记录抽取「入院诊断/初步诊断」。
4. 诊疗经过：从首次病程、日常病程、手术操作记录、特殊检查记录中，抽取病情变化、检查检验、治疗处置、手术事件，按**时间线**整理概括生成。
5. 出院诊断：整合入院记录中「入院诊断/初步诊断、修正诊断、补充诊断」全部内容。
6. 出院情况：解析末次病程记录，剔除出院用药、检查、康复、生活指导、随诊建议，剩余内容整理为出院情况。
7. 出院医嘱：从末次病程记录提取出院用药、复查检查、康复训练、生活饮食、复诊随诊相关建议。

要求：**完全忠于原文、不编造、不臆造、不新增病情**，医疗术语规范，语句通顺，分段清晰，严格按七个字段输出。

### 患者原始病历文本
{record_text}

### 输出
""".strip()


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
        records_text = []
        current_section = ""
        for idx, record in enumerate(records):
            section = str(record.get("section") or "").strip()
            title = str(record.get("title") or "").strip()
            content = str(record.get("content") or record.get("text") or "").strip()
            
            if section and section != current_section:
                current_section = section
                records_text.append(f"#### {section}\n")
            
            if title:
                records_text.append(f"{title}:\n")
            if content:
                records_text.append(f"{content}\n")
            records_text.append("\n")
        
        return ''.join(records_text)

    record_text = str(payload.get("record") or payload.get("text") or payload.get("content") or "").strip()
    return record_text


def save_prepared(payload: dict[str, Any], output_path: str, input_path: Path) -> None:
    save_dir = Path(output_path).parent if output_path else SCRIPT_DIR.parents[1] / "runs" / "discharge-record"
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
    parser = argparse.ArgumentParser(description="出院记录生成统一入口：支持 pdf/doc/docx/xls/xlsx/csv/txt/json 输入。")
    parser.add_argument("--input", required=True, help="输入病历文件路径。")
    parser.add_argument("--input-type", default="auto", choices=["auto", *sorted(SUPPORTED_FILE_TYPES)], help="输入类型；默认 auto。")
    parser.add_argument("--sheet", default="", help="读取 Excel 时指定 sheet（可选）。")
    parser.add_argument("--encoding", default="utf-8", help="txt/csv 编码（默认：utf-8）。")
    parser.add_argument("--base", default=DEFAULT_LLM_BASE, help=f"内部大模型 base URL（默认：{DEFAULT_LLM_BASE}）。")
    parser.add_argument("--model", default=DEFAULT_LLM_MODEL, help=f"模型名称（默认：{DEFAULT_LLM_MODEL}）。")
    parser.add_argument("--timeout", type=int, default=0, help="HTTP 超时秒数；0 表示一直等待（默认：0）。")
    parser.add_argument("--appkey", required=True, help="必须传入。内部医疗大模型鉴权 key，使用 Bearer 方式认证。")
    parser.add_argument("--output-json", default="", help="输出 JSON 文件路径（可选）。")
    parser.add_argument("--output", default="", help="输出出院记录文本文件路径（可选）。")
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
