#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""血糖监测记录 — 自包含skill，独立部署，不依赖_shared/"""

import argparse
import json
import re
import sys
from datetime import date as date_type
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ── 固定配置 ──
API_URL = "https://maas-api.hivoice.cn/v1/chat/completions"
MODEL = "u1-insuremed"

# ── 同目录导入（preprocess.py 每个skill自带一份）──
from preprocess import (
    PreprocessError, SUPPORTED_FILE_TYPES,
    detect_input_type, load_input_artifact, first_matching_index, normalize_header,
)

FIELD_ALIASES = {
    "value": ["value", "血糖值", "值"],
    "unit": ["unit", "单位"],
    "measure_type": ["measure_type", "测量类型", "类型"],
    "measured_at": ["measured_at", "测量时间"],
    "note": ["note", "备注"],
}


# ═══════════════════════════════════════════════════════════════════
# LLM 调用（内联，无外部依赖）
# ═══════════════════════════════════════════════════════════════════

def _call_llm(system_prompt: str, user_prompt: str, appkey: str) -> str:
    payload = {
        "model": MODEL,
        "temperature": 0.0,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    try:
        req = Request(API_URL, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                      headers={"Content-Type": "application/json",
                               "Authorization": f"Bearer {appkey}"})
        resp = urlopen(req, timeout=120)
        body = json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"API HTTP {exc.code}: {detail}")
    except URLError as exc:
        raise RuntimeError(f"API unreachable: {exc.reason}")
    if "choices" not in body or not body["choices"]:
        raise RuntimeError("API response missing choices")
    return body["choices"][0].get("message", {}).get("content", "")


def _extract_json(text: str) -> Optional[Dict[str, Any]]:
    text = text.strip()
    try:
        val = json.loads(text)
        if isinstance(val, dict):
            return val
    except (json.JSONDecodeError, ValueError):
        pass
    code_block = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if code_block:
        try:
            val = json.loads(code_block.group(1).strip())
            if isinstance(val, dict):
                return val
        except (json.JSONDecodeError, ValueError):
            pass
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    val = json.loads(text[start:i + 1])
                    if isinstance(val, dict):
                        return val
                except (json.JSONDecodeError, ValueError):
                    pass
                break
    return None


# ═══════════════════════════════════════════════════════════════════
# 本地预处理
# ═══════════════════════════════════════════════════════════════════

def require(data: Dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "":
        raise ValueError(f"missing required field: {key}")
    return value


def _local_normalize(records: List[Dict]) -> List[Dict]:
    result = []
    for r in records:
        result.append({
            "value": r.get("value", ""),
            "unit": r.get("unit", "mmol/L"),
            "measure_type": r.get("measure_type", ""),
            "measured_at": r.get("measured_at", ""),
            "note": r.get("note", ""),
        })
    return result


# ═══════════════════════════════════════════════════════════════════
# 核心逻辑
# ═══════════════════════════════════════════════════════════════════

SYSTEM_PROMPT = """你是一位专业的慢病管理助手，擅长血糖数据分析。

你的任务：
1. 根据用户提供的血糖记录数据，进行结构化记录
2. 判断每条血糖值是否在正常范围（空腹3.9-6.1 mmol/L，餐后<7.8 mmol/L，随机<11.1 mmol/L）
3. 如果是多条记录，分析血糖趋势（上升/下降/波动/稳定）
4. 标注异常值并给出风险提示
5. 给出简洁实用的生活方式建议

输出要求：
- 输出自然语言Markdown文本，面向患者，通俗易懂
- 包含：血糖记录概览、趋势分析（多记录时）、异常提示、建议
- 禁止输出任何医嘱或诊断结论
- 末尾加上免责提示：本内容仅供参考，不替代医生诊疗
"""


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    # 1. 本地预处理：标准化记录列表
    raw = data if isinstance(data, list) else [data]
    records = _local_normalize(raw)

    # 2. 校验必填字段
    for i, rec in enumerate(records):
        require(rec, "value")

    # 3. 构建 user prompt
    user_prompt = f"请分析以下血糖监测数据：\n```json\n{json.dumps(records, ensure_ascii=False, indent=2)}\n```"

    # 4. 调用 API
    text = _call_llm(SYSTEM_PROMPT, user_prompt, appkey)

    return {
        "skill": "血糖监测记录",
        "status": "ok",
        "data": {
            "record_type": "blood_glucose",
            "record_count": len(records),
            "records": records,
        },
        "text": text.strip(),
    }


# ═══════════════════════════════════════════════════════════════════
# 多格式输入解析
# ═══════════════════════════════════════════════════════════════════

def load_json(path: str) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object or array")
    return data


def parse_text_kv(text: str, field_aliases: Dict[str, List[str]]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    pattern = re.compile(r"^\s*([A-Za-z一-鿿_][A-Za-z0-9一-鿿_\s]*)\s*[:：]\s*(.+?)\s*$")
    header_map = {}
    for canonical, aliases in field_aliases.items():
        for alias in aliases:
            header_map[normalize_header(alias)] = canonical
            header_map[normalize_header(canonical)] = canonical
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
        raw_key = match.group(1).strip()
        value_str = match.group(2).strip()
        key = header_map.get(normalize_header(raw_key))
        if key is None:
            continue
        try:
            value: Any = json.loads(value_str)
        except (json.JSONDecodeError, ValueError):
            value = value_str
        result[key] = value
    return result


def normalize_artifact(artifact: Dict[str, Any], field_aliases: Dict[str, List[str]]) -> Dict[str, Any]:
    kind = artifact.get("kind")
    if kind == "json":
        data = artifact["data"]
        if isinstance(data, (dict, list)):
            return data
        raise PreprocessError("JSON input must be an object or array.")
    if kind == "text":
        text = artifact.get("text", "")
        try:
            data = json.loads(text)
            if isinstance(data, (dict, list)):
                return data
        except (json.JSONDecodeError, ValueError):
            pass
        return parse_text_kv(text, field_aliases)
    if kind == "tables":
        all_rows: List[List[str]] = []
        for table in artifact.get("tables", []):
            all_rows.extend(table.get("rows", []))
        if not all_rows:
            raise PreprocessError("No data rows found in table input.")
        header_row = all_rows[0]
        col_map = {}
        for canonical, aliases in field_aliases.items():
            for alias in aliases:
                idx = first_matching_index(
                    {normalize_header(cell): i for i, cell in enumerate(header_row) if cell.strip()},
                    (alias, canonical),
                )
                if idx is not None:
                    col_map[canonical] = idx
                    break
        records = []
        for data_row in all_rows[1:]:
            rec = {}
            for key, idx in col_map.items():
                if idx < len(data_row) and data_row[idx].strip():
                    val = data_row[idx].strip()
                    try:
                        rec[key] = json.loads(val)
                    except (json.JSONDecodeError, ValueError):
                        rec[key] = val
            if rec:
                records.append(rec)
        if not records:
            return {}
        return records if len(records) > 1 else records[0]
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def write_json(data: Dict[str, Any], output: str) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


# ═══════════════════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════════════════

def main() -> int:
    parser = argparse.ArgumentParser(description="血糖监测记录 — 结构化血糖数据并调用AI分析")
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--output", default="", help="输出JSON路径，不传则输出到stdout")
    parser.add_argument("--input-type", default="auto",
                        choices=["auto", *sorted(SUPPORTED_FILE_TYPES)],
                        help="输入类型，默认auto自动检测")
    parser.add_argument("--sheet", default="", help="xlsx指定sheet名")
    parser.add_argument("--encoding", default="utf-8", help="txt/csv编码，默认utf-8")
    parser.add_argument("--save-prepared", action="store_true", help="保存预处理后的JSON便于调试")
    parser.add_argument("--appkey", required=True, help="内部医疗大模型鉴权key（必填）")
    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
            return 1

        input_type = detect_input_type(input_path, args.input_type)
        if input_type == "json":
            data = load_json(args.input)
        else:
            artifact = load_input_artifact(input_path, input_type, args.encoding, args.sheet)
            data = normalize_artifact(artifact, FIELD_ALIASES)

        if args.save_prepared:
            prepared_path = Path(args.output).with_suffix(".prepared.json") if args.output else input_path.with_suffix(".prepared.json")
            prepared_path.parent.mkdir(parents=True, exist_ok=True)
            prepared_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

        result = build(data, args.appkey)
        write_json(result, args.output)
        return 0
    except PreprocessError as exc:
        # 回退到 _shared/doc-preprocess 尝试处理
        try:
            _shared_dir = Path(__file__).resolve().parent.parents[3] / "_shared" / "doc-preprocess" / "scripts"
            if not _shared_dir.exists():
                print(f"ERROR: 无法读取输入文件，本地预处理失败且 _shared/doc-preprocess 不可用。原因：{exc}", file=sys.stderr)
                return 1
            import importlib.util as _iu
            _spec = _iu.spec_from_file_location("_shared_preprocess", _shared_dir / "preprocess.py")
            _sp = _iu.module_from_spec(_spec)
            _spec.loader.exec_module(_sp)
            input_type = _sp.detect_input_type(input_path, args.input_type)
            if input_type == "json":
                data = load_json(args.input)
            else:
                artifact = _sp.load_input_artifact(input_path, input_type, args.encoding, args.sheet)
                data = normalize_artifact(artifact, FIELD_ALIASES)
            if args.save_prepared:
                prepared_path = Path(args.output).with_suffix(".prepared.json") if args.output else input_path.with_suffix(".prepared.json")
                prepared_path.parent.mkdir(parents=True, exist_ok=True)
                prepared_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            result = build(data, args.appkey)
            write_json(result, args.output)
            return 0
        except Exception as shared_exc:
            print(f"ERROR: 无法读取输入文件。本地预处理失败：{exc}；_shared/doc-preprocess 回退也失败：{shared_exc}", file=sys.stderr)
            return 1
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
