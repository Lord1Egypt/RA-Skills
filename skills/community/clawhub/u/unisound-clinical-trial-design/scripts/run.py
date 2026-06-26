#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""临床试验设计辅助 — 自包含skill，审阅和优化临床试验方案"""

import argparse, json, re, sys
from pathlib import Path
from typing import Any, Dict, List
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_URL = "https://maas-api.hivoice.cn/v1/chat/completions"
MODEL = "u1-insuremed"

from preprocess import (
    PreprocessError, SUPPORTED_FILE_TYPES,
    detect_input_type, load_input_artifact, first_matching_index, normalize_header,
)

FIELD_ALIASES = {
    "indication": ["indication", "适应症", "疾病"],
    "intervention": ["intervention", "干预措施", "研究药物"],
    "phase": ["phase", "试验分期", "分期"],
    "objective": ["objective", "研究目的", "目的"],
    "population": ["population", "目标人群", "人群"],
    "control": ["control", "对照方式", "对照"],
    "randomization": ["randomization", "随机化", "随机化方式"],
    "blinding": ["blinding", "盲法"],
    "endpoints": ["endpoints", "终点", "终点列表"],
    "visits": ["visits", "访视", "访视安排"],
}


def _call_llm(system_prompt: str, user_prompt: str, appkey: str) -> str:
    payload = {"model": MODEL, "temperature": 0.0, "messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}]}
    try:
        req = Request(API_URL, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
                      headers={"Content-Type": "application/json", "Authorization": f"Bearer {appkey}"})
        resp = urlopen(req, timeout=120)
        return json.loads(resp.read().decode("utf-8"))["choices"][0]["message"]["content"]
    except HTTPError as exc: raise RuntimeError(f"API HTTP {exc.code}")
    except URLError as exc: raise RuntimeError(f"API unreachable: {exc.reason}")


def as_list(value: Any) -> List[Any]:
    if value is None or value == "": return []
    if isinstance(value, list): return value
    if isinstance(value, str):
        parts = [p.strip() for p in re.split(r"[,，;；\n]+", value) if p.strip()]
        return parts if parts else []
    return [value]


SYSTEM_PROMPT = """你是一位临床试验方案设计专家，帮助审阅和优化临床试验设计。

你的任务：
1. 审阅试验方案的设计要素：适应症、干预措施、分期、终点、人群、对照、随机化、盲法
2. 指出设计方案中的潜在偏倚和缺陷
3. 基于适应症和分期，给出优化的终点选择和人群标准建议
4. 评估方案的可行性（样本量、访视安排等）

输出Markdown格式。末尾加免责提示：本设计辅助建议仅供参考，最终方案需经统计学、医学和法规专家审阅。"""


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    indication = data.get("indication", "")
    intervention = data.get("intervention", "")
    phase = data.get("phase", "")
    objective = data.get("objective", "")
    population = data.get("population", "")
    control = data.get("control", "")
    randomization = data.get("randomization", "")
    blinding = data.get("blinding", "")
    endpoints = as_list(data.get("endpoints", []))
    visits = as_list(data.get("visits", []))

    if not indication: raise ValueError("missing required field: indication")
    if not intervention: raise ValueError("missing required field: intervention")
    if not phase: raise ValueError("missing required field: phase")
    if not endpoints: raise ValueError("missing required field: endpoints")

    user_prompt = f"""请审阅以下临床试验设计：

适应症：{indication}
干预措施：{intervention}
试验分期：{phase}
研究目的：{objective}
目标人群：{population}
对照方式：{control}
随机化方式：{randomization}
盲法：{blinding}
终点列表：{json.dumps(endpoints, ensure_ascii=False)}
访视安排：{json.dumps(visits, ensure_ascii=False)}

请审阅设计合理性，指出潜在偏倚，给出优化建议。"""

    text = _call_llm(SYSTEM_PROMPT, user_prompt, appkey)

    return {
        "skill": "临床试验设计辅助",
        "status": "ok",
        "data": {
            "indication": indication,
            "intervention": intervention,
            "phase": phase,
            "study_design": {
                "objective": objective,
                "control": control,
                "randomization": randomization,
                "blinding": blinding,
            },
            "population": population,
            "endpoints": endpoints,
            "visit_schedule": visits,
        },
        "text": text.strip(),
    }


# ── 多格式解析 ──

def load_json(path: str) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict): raise ValueError("input must be a JSON object")
    return data


def parse_text_kv(text: str, field_aliases: Dict[str, List[str]]) -> Dict[str, Any]:
    result = {}
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    pattern = re.compile(r"^\s*([A-Za-z一-鿿_][A-Za-z0-9一-鿿_\s]*)\s*[:：]\s*(.+?)\s*$")
    header_map = {}
    for canonical, aliases in field_aliases.items():
        for alias in aliases: header_map[normalize_header(alias)] = canonical; header_map[normalize_header(canonical)] = canonical
    for line in lines:
        match = pattern.match(line)
        if not match: continue
        key = header_map.get(normalize_header(match.group(1).strip()))
        if key is None: continue
        value_str = match.group(2).strip()
        try: result[key] = json.loads(value_str)
        except (json.JSONDecodeError, ValueError): result[key] = value_str
    return result


def normalize_artifact(artifact, field_aliases):
    kind = artifact.get("kind")
    if kind == "json":
        data = artifact["data"]
        if isinstance(data, dict): return data
        raise PreprocessError("JSON input must be an object.")
    if kind == "text":
        text = artifact.get("text", "")
        try:
            data = json.loads(text)
            if isinstance(data, dict): return data
        except (json.JSONDecodeError, ValueError): pass
        return parse_text_kv(text, field_aliases)
    if kind == "tables":
        all_rows = []
        for table in artifact.get("tables", []): all_rows.extend(table.get("rows", []))
        if not all_rows: raise PreprocessError("No data rows found.")
        header_row = all_rows[0]; data_row = all_rows[1] if len(all_rows) > 1 else []
        result = {}
        for canonical, aliases in field_aliases.items():
            idx = first_matching_index({normalize_header(cell): i for i, cell in enumerate(header_row) if cell.strip()}, tuple(aliases) + (canonical,))
            if idx is not None and idx < len(data_row) and data_row[idx].strip():
                val = data_row[idx].strip()
                try: result[canonical] = json.loads(val)
                except (json.JSONDecodeError, ValueError): result[canonical] = val
        return result
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def write_json(data, output):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output: Path(output).parent.mkdir(parents=True, exist_ok=True); Path(output).write_text(text + "\n", encoding="utf-8")
    else: print(text)


def main():
    parser = argparse.ArgumentParser(description="临床试验设计辅助 — 审阅和优化试验方案")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--input-type", default="auto", choices=["auto", *sorted(SUPPORTED_FILE_TYPES)])
    parser.add_argument("--sheet", default=""); parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--save-prepared", action="store_true")
    parser.add_argument("--appkey", required=True, help="内部医疗大模型鉴权key（必填）")
    args = parser.parse_args()

    try:
        input_path = Path(args.input)
        if not input_path.exists(): print(f"ERROR: Input file not found: {input_path}", file=sys.stderr); return 1
        input_type = detect_input_type(input_path, args.input_type)
        if input_type == "json": data = load_json(args.input)
        else: data = normalize_artifact(load_input_artifact(input_path, input_type, args.encoding, args.sheet), FIELD_ALIASES)
        if args.save_prepared:
            pp = Path(args.output).with_suffix(".prepared.json") if args.output else input_path.with_suffix(".prepared.json")
            pp.parent.mkdir(parents=True, exist_ok=True); pp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
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
