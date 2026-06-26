#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str):
        return [line.strip() for line in re.split(r"[\n,，;；]", value) if line.strip()]
    return []


def parse_candidate_json(value: str) -> Any:
    raw = str(value or "").strip()
    if not raw:
        return None
    path = Path(raw)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(raw)


def parse_string_list(values: list[str], json_value: str = "") -> list[str]:
    items: list[str] = []
    if json_value:
        parsed = parse_candidate_json(json_value)
        if isinstance(parsed, dict):
            for key in ("candidate_diagnoses", "candidate_surgeries", "候选诊断", "候选手术", "items", "candidates"):
                if isinstance(parsed.get(key), list):
                    parsed = parsed[key]
                    break
        if not isinstance(parsed, list):
            raise ValueError("候选项 JSON 必须是字符串数组或包含字符串数组的对象")
        items.extend(str(item).strip() for item in parsed if str(item).strip())
    for value in values:
        for line in str(value or "").replace("，", "\n").replace(",", "\n").splitlines():
            line = line.strip()
            if line:
                items.append(line)
    return items


def _format_candidates(items: list[str]) -> str:
    return "\n".join(items)


def build_prompt(payload: dict[str, Any]) -> str:
    raw_prompt = str(payload.get("prompt") or "").strip()
    if raw_prompt:
        return raw_prompt

    admission = str(payload.get("admission") or payload.get("入院情况") or "").strip()
    treatment = str(payload.get("treatment") or payload.get("诊疗过程") or "").strip()
    pathology = str(payload.get("pathology") or payload.get("病理") or "").strip()
    candidate_diagnoses = _string_list(payload.get("candidate_diagnoses") or payload.get("候选诊断"))
    candidate_surgeries = _string_list(payload.get("candidate_surgeries") or payload.get("候选手术"))

    if not admission and not treatment and not pathology:
        raise ValueError("输入缺少 admission/treatment/pathology 或 prompt")
    if not candidate_diagnoses:
        raise ValueError("输入缺少 candidate_diagnoses")
    if not candidate_surgeries:
        raise ValueError("输入缺少 candidate_surgeries")

    return f"""根据如下患者信息，以及对应的【候选诊断】和【候选手术】，请你分别从【候选诊断】和【候选手术】中挑选本次入院的【主要诊断】和【主要手术】
【入院情况】: {admission}
【诊疗过程】: {treatment}
【病理】: {pathology}
【候选诊断】:
{_format_candidates(candidate_diagnoses)}
【候选手术】:
{_format_candidates(candidate_surgeries)}

要求：
1. 主要诊断必须从【候选诊断】中选择，主要手术必须从【候选手术】中选择。
2. 不允许输出候选项之外的诊断或手术。
3. 只返回 JSON，不要输出 Markdown、解释、序号或额外提示语。
4. JSON 格式必须为：
{{"main_diagnosis": "候选诊断之一", "main_surgery": "候选手术之一"}}
"""


def build_payload_from_input(
    path: Path,
    *,
    input_type: str,
    encoding: str,
    sheet: str,
    candidate_diagnoses: list[str],
    candidate_surgeries: list[str],
) -> dict[str, Any]:
    resolved_type = detect_input_type(path, input_type)
    if resolved_type == "json":
        try:
            payload = _read_json(path)
            if payload.get("prompt") or (
                any(payload.get(key) for key in ("admission", "入院情况", "treatment", "诊疗过程", "pathology", "病理"))
                and (payload.get("candidate_diagnoses") or payload.get("候选诊断") or candidate_diagnoses)
                and (payload.get("candidate_surgeries") or payload.get("候选手术") or candidate_surgeries)
            ):
                if candidate_diagnoses:
                    payload["candidate_diagnoses"] = candidate_diagnoses
                if candidate_surgeries:
                    payload["candidate_surgeries"] = candidate_surgeries
                return payload
        except Exception:
            pass

    record_text = extract_text(path, resolved_type, encoding, sheet)
    if not record_text.strip():
        raise PreprocessError("预处理后病历文本为空")
    if not candidate_diagnoses:
        raise ValueError("使用普通病历文件输入时必须传 --candidate-diagnosis 或 --candidate-diagnoses-json")
    if not candidate_surgeries:
        raise ValueError("使用普通病历文件输入时必须传 --candidate-surgery 或 --candidate-surgeries-json")
    return {
        "admission": record_text,
        "treatment": "",
        "pathology": "",
        "candidate_diagnoses": candidate_diagnoses,
        "candidate_surgeries": candidate_surgeries,
    }


def payload_to_prepared_text(payload: dict[str, Any]) -> str:
    raw_prompt = str(payload.get("prompt") or "").strip()
    if raw_prompt:
        return raw_prompt
    chunks = []
    for key in ("admission", "入院情况", "treatment", "诊疗过程", "pathology", "病理"):
        value = str(payload.get(key) or "").strip()
        if value:
            chunks.append(f"【{key}】\n{value}")
    return "\n\n".join(chunks)


def save_prepared(payload: dict[str, Any], output_json: str, input_path: Path) -> None:
    save_dir = Path(output_json).parent if output_json else SCRIPT_DIR.parents[1] / "runs" / "primary-diagnosis-surgery-selection"
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


def parse_json_object(text: str) -> dict[str, Any]:
    cleaned = re.sub(r"<think[^>]*>.*?</think>", "", text or "", flags=re.S | re.I).strip()
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    start = cleaned.find("{")
    if start < 0:
        raise ValueError("模型输出中未找到 JSON 对象")
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(cleaned[start:], start=start):
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                parsed = json.loads(cleaned[start : index + 1])
                if not isinstance(parsed, dict):
                    raise ValueError("模型 JSON 输出必须是对象")
                return parsed
    raise ValueError("模型输出中的 JSON 对象不完整")


def normalize_output(payload: dict[str, Any], source_payload: dict[str, Any]) -> dict[str, str]:
    main_diagnosis = str(
        payload.get("main_diagnosis")
        or payload.get("主要诊断")
        or payload.get("primary_diagnosis")
        or ""
    ).strip()
    main_surgery = str(
        payload.get("main_surgery")
        or payload.get("主要手术")
        or payload.get("primary_surgery")
        or ""
    ).strip()

    diagnoses = _string_list(source_payload.get("candidate_diagnoses") or source_payload.get("候选诊断"))
    surgeries = _string_list(source_payload.get("candidate_surgeries") or source_payload.get("候选手术"))
    if diagnoses and main_diagnosis not in diagnoses:
        raise ValueError(f"模型输出的 main_diagnosis 不在候选诊断中: {main_diagnosis}")
    if surgeries and main_surgery not in surgeries:
        raise ValueError(f"模型输出的 main_surgery 不在候选手术中: {main_surgery}")
    if not main_diagnosis:
        raise ValueError("模型输出缺少 main_diagnosis")
    if not main_surgery:
        raise ValueError("模型输出缺少 main_surgery")
    return {"main_diagnosis": main_diagnosis, "main_surgery": main_surgery}


def run(payload: dict[str, Any], *, base: str, model: str, appkey: str, timeout: int) -> dict[str, str]:
    prompt = build_prompt(payload)
    raw = call_llm(prompt, base=base, model=model, appkey=appkey, timeout=timeout)
    parsed = parse_json_object(raw)
    return normalize_output(parsed, payload)


def main() -> int:
    parser = argparse.ArgumentParser(description="主诊断和主手术选择统一入口：支持 pdf/doc/docx/xls/xlsx/csv/txt/json 输入。")
    parser.add_argument("--input", required=True, help="输入病历文件路径。")
    parser.add_argument("--input-type", default="auto", choices=["auto", *sorted(SUPPORTED_FILE_TYPES)], help="输入类型；默认 auto。")
    parser.add_argument("--sheet", default="", help="读取 Excel 时指定 sheet（可选）。")
    parser.add_argument("--encoding", default="utf-8", help="txt/csv 编码（默认：utf-8）。")
    parser.add_argument("--candidate-diagnosis", action="append", default=[], help="候选诊断；可重复。")
    parser.add_argument("--candidate-diagnoses-json", default="", help="候选诊断字符串数组 JSON 或文件路径。")
    parser.add_argument("--candidate-surgery", action="append", default=[], help="候选手术；可重复。")
    parser.add_argument("--candidate-surgeries-json", default="", help="候选手术字符串数组 JSON 或文件路径。")
    parser.add_argument("--base", default=DEFAULT_LLM_BASE, help=f"内部大模型 base URL（默认：{DEFAULT_LLM_BASE}）。")
    parser.add_argument("--model", default=DEFAULT_LLM_MODEL, help=f"模型名称（默认：{DEFAULT_LLM_MODEL}）。")
    parser.add_argument("--timeout", type=int, default=0, help="HTTP 超时秒数；0 表示一直等待（默认：0）。")
    parser.add_argument("--appkey", required=True, help="内部医疗大模型鉴权 key，由平台分配；调用时必填，使用 Bearer 鉴权。")
    parser.add_argument("--output-json", default="", help="输出 JSON 文件路径（可选；优先于 --output）。")
    parser.add_argument("--output", default="", help="输出 JSON 文件路径（可选；兼容旧调用方式，等同于 --output-json）。")
    parser.add_argument("--save-prepared", action="store_true", help="保存预处理后的病历文本，便于调试。")
    args = parser.parse_args()

    try:
        candidate_diagnoses = parse_string_list(args.candidate_diagnosis, args.candidate_diagnoses_json)
        candidate_surgeries = parse_string_list(args.candidate_surgery, args.candidate_surgeries_json)
        input_path = Path(args.input)
        payload = build_payload_from_input(
            input_path,
            input_type=args.input_type,
            encoding=args.encoding,
            sheet=args.sheet,
            candidate_diagnoses=candidate_diagnoses,
            candidate_surgeries=candidate_surgeries,
        )
        if args.save_prepared:
            save_prepared(payload, args.output_json or args.output, input_path)
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
