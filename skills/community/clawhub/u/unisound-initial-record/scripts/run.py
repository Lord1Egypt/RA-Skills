#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
门诊初诊病历生成：根据医患对话生成结构化的初诊病历信息。
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

from preprocess import (
    PreprocessError,
    SUPPORTED_FILE_TYPES,
    detect_input_type,
    load_input_artifact,
)


DEFAULT_LLM_BASE = "https://maas-api.hivoice.cn/v1"
DEFAULT_LLM_MODEL = "u1-insuremed"


def _read_json(path: Path) -> dict[str, Any]:
    """读取 JSON 文件并验证结构。"""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("输入 JSON 必须是对象")
    return payload


def extract_text(path: Path, input_type: str, encoding: str, sheet: str) -> str:
    """从任意格式文件中提取纯文本。"""
    artifact = load_input_artifact(
        path, input_type, encoding, sheet, pdf_as_single_text=True
    )
    kind = artifact["kind"]
    if kind == "text":
        return str(artifact.get("text") or "")
    if kind == "json":
        data = artifact["data"]
        if isinstance(data, str):
            return data
        if isinstance(data, dict):
            for key in ("dialogue", "dialogue_records", "text", "content", "records"):
                value = data.get(key)
                if isinstance(value, str) and value.strip():
                    return value
            if "dialogue_records" in data and isinstance(
                data["dialogue_records"], list
            ):
                return json.dumps(data, ensure_ascii=False)
        return json.dumps(data, ensure_ascii=False)
    if kind == "tables":
        rows_text: list[str] = []
        for table in artifact.get("tables", []):
            for row in table.get("rows", []):
                rows_text.append("\t".join(str(cell) for cell in row))
        return "\n".join(rows_text)
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def build_payload_from_input(
    path: Path,
    *,
    input_type: str,
    encoding: str,
    sheet: str,
) -> dict[str, Any]:
    """根据输入构建 API 请求体。"""
    resolved_type = detect_input_type(path, input_type)

    # 尝试直接读取 JSON
    if resolved_type == "json":
        try:
            payload = _read_json(path)
            # 检查是否已包含 dialogue_records 或其他支持字段
            if (
                payload.get("dialogue_records")
                or payload.get("dialogue")
                or payload.get("text")
            ):
                return payload
        except Exception:
            pass

    # 从文件提取文本
    text = extract_text(path, resolved_type, encoding, sheet)
    if not text.strip():
        raise PreprocessError("预处理后对话文本为空")

    # 尝试解析 JSON 文本
    try:
        data = json.loads(text)
        if isinstance(data, dict) and (
            data.get("dialogue_records") or data.get("dialogue")
        ):
            return data
    except json.JSONDecodeError:
        pass

    # 默认为纯文本对话，尝试解析为对话格式
    # 支持简单的对话格式：患者：xxx\n医生：xxx
    dialogue_records = parse_simple_dialogue(text)
    if dialogue_records:
        return {"dialogue_records": dialogue_records}

    # 回退为单个文本字段
    return {"text": text}


def parse_simple_dialogue(text: str) -> list[dict[str, str]]:
    """解析简单的对话文本格式：患者/医生：内容。"""
    lines = text.strip().split("\n")
    records = []
    speaker_map = {"患者": "患者", "医生": "医生"}

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 支持中文冒号和英文冒号
        for speaker, label in speaker_map.items():
            if line.startswith(f"{speaker}:") or line.startswith(f"{speaker}："):
                content = line.split(":", 1)[-1].split("：", 1)[-1].strip()
                if content:
                    records.append({"speaker": label, "text": content})
                break

    return records if records else None


def _http_post(
    url: str, payload: dict[str, Any], headers: dict[str, str], *, timeout: int = 0
) -> Any:
    """发送 HTTP POST 请求。"""
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            **{key: value for key, value in headers.items() if value},
        },
    )
    try:
        opener = (
            urllib.request.urlopen(req)
            if not timeout
            else urllib.request.urlopen(req, timeout=timeout)
        )
        with opener as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return json.loads(body)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc}") from exc


def call_llm(prompt: str, *, base: str, model: str, appkey: str, timeout: int) -> str:
    """调用内部医疗大模型。"""
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


def build_prompt(payload: dict[str, Any]) -> str:
    """构建 LLM 提示词。"""
    dialogue_records = payload.get("dialogue_records")
    if dialogue_records and isinstance(dialogue_records, list):
        # 将对话记录格式化为对话文本
        dialogue_text = []
        for record in dialogue_records:
            speaker = record.get("speaker", "")
            text = record.get("text", "")
            dialogue_text.append(f"{speaker}：{text}")
        dialogue = "\n".join(dialogue_text)
    else:
        # 从其他字段获取
        dialogue = (
            payload.get("dialogue")
            or payload.get("text")
            or payload.get("content")
            or ""
        )

    if not dialogue:
        raise ValueError("输入缺少 dialogue_records 或 text 字段")

    prompt = f"""根据下面的历史摘要信息和历史医患对话及摘要，生成最新轮次对话的医学信息摘要：
{dialogue}"""
    return prompt.strip()


def run(
    payload: dict[str, Any], *, base: str, model: str, appkey: str, timeout: int
) -> str:
    """执行病历生成。"""
    prompt = build_prompt(payload)
    return call_llm(prompt, base=base, model=model, appkey=appkey, timeout=timeout)


def save_prepared(payload: dict[str, Any], output_path: str, input_path: Path) -> None:
    """保存预处理后的数据，便于调试。"""
    save_dir = (
        Path(output_path).parent
        if output_path
        else SCRIPT_DIR.parents[1] / "runs" / "initial-record"
    )
    save_dir.mkdir(parents=True, exist_ok=True)
    prepared_path = save_dir / f"{input_path.stem}.prepared.json"
    prepared_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(f"Prepared data saved to: {prepared_path}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="门诊初诊病历生成统一入口：支持 pdf/doc/docx/xls/xlsx/csv/txt/json 输入。"
    )
    parser.add_argument("--input", required=True, help="输入对话文件路径。")
    parser.add_argument(
        "--input-type",
        default="auto",
        choices=["auto", *sorted(SUPPORTED_FILE_TYPES)],
        help="输入类型；默认 auto。",
    )
    parser.add_argument("--sheet", default="", help="读取 Excel 时指定 sheet（可选）。")
    parser.add_argument("--encoding", default="utf-8", help="txt/csv 编码（默认：utf-8）。")
    parser.add_argument(
        "--base",
        default=DEFAULT_LLM_BASE,
        help=f"内部大模型 base URL（默认：{DEFAULT_LLM_BASE}）。",
    )
    parser.add_argument(
        "--model", default=DEFAULT_LLM_MODEL, help=f"模型名称（默认：{DEFAULT_LLM_MODEL}）。"
    )
    parser.add_argument(
        "--timeout", type=int, default=0, help="HTTP 超时秒数；0 表示一直等待（默认：0）。"
    )
    parser.add_argument(
        "--appkey",
        required=True,
        help="必须传入。内部医疗大模型鉴权 key，使用 Bearer 方式认证。",
    )
    parser.add_argument("--output-json", default="", help="输出 JSON 文件路径（可选）。")
    parser.add_argument("--output", default="", help="输出病历文本文件路径（可选）。")
    parser.add_argument("--save-prepared", action="store_true", help="保存预处理后的数据，便于调试。")
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
