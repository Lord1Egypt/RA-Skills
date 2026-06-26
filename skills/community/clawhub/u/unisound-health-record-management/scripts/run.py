#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""健康档案管理 — 自包含skill，整理结构化健康档案"""

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
    "profile": ["profile", "基本信息"],
    "medical_history": ["medical_history", "既往史", "病史"],
    "allergy_history": ["allergy_history", "过敏史"],
    "surgery_history": ["surgery_history", "手术史"],
    "family_history": ["family_history", "家族史"],
    "medication_history": ["medication_history", "用药史"],
    "updated_at": ["updated_at", "更新时间"],
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
    return [value]


SYSTEM_PROMPT = """你是一位健康档案管理助手，帮助患者整理和理解自己的健康档案。

你的任务：
1. 整理基本信息、既往史、过敏史、手术史、家族史、用药史
2. 高亮标注过敏史（⚠️关键安全信息）和重要病史
3. 检查档案完整性，指出缺失的关键信息
4. 用Markdown格式清晰展示各模块

输出Markdown格式。末尾加免责提示：本档案由患者自行维护，就医时请以医疗机构记录为准。"""


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    profile = data.get("profile", {})
    medical_history = as_list(data.get("medical_history", []))
    allergy_history = as_list(data.get("allergy_history", []))
    surgery_history = as_list(data.get("surgery_history", []))
    family_history = as_list(data.get("family_history", []))
    medication_history = as_list(data.get("medication_history", []))
    updated_at = data.get("updated_at", "")

    # 本地检查完整性
    missing = []
    if not profile or not profile.get("name"): missing.append("基本信息不完整")
    if not allergy_history: missing.append("过敏史未填写（重要）")
    if not medical_history: missing.append("既往史未填写")
    if not medication_history: missing.append("用药史未填写")

    user_prompt = f"""请整理以下健康档案：

基本信息：{json.dumps(profile, ensure_ascii=False)}
既往史：{json.dumps(medical_history, ensure_ascii=False)}
过敏史：{json.dumps(allergy_history, ensure_ascii=False)}
手术史：{json.dumps(surgery_history, ensure_ascii=False)}
家族史：{json.dumps(family_history, ensure_ascii=False)}
用药史：{json.dumps(medication_history, ensure_ascii=False)}
更新时间：{updated_at}
缺失项：{json.dumps(missing, ensure_ascii=False)}

请高亮标注过敏史，检查完整性，生成清晰的健康档案摘要。"""

    text = _call_llm(SYSTEM_PROMPT, user_prompt, appkey)

    return {
        "skill": "健康档案管理",
        "status": "ok",
        "data": {
            "profile": profile,
            "medical_history": medical_history,
            "allergy_history": allergy_history,
            "surgery_history": surgery_history,
            "family_history": family_history,
            "medication_history": medication_history,
            "updated_at": updated_at,
            "completeness": {"missing_fields": missing},
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
        header_row = all_rows[0]
        col_map = {}
        for canonical, aliases in field_aliases.items():
            for alias in aliases:
                idx = first_matching_index({normalize_header(cell): i for i, cell in enumerate(header_row) if cell.strip()}, (alias, canonical))
                if idx is not None: col_map[canonical] = idx; break
        if len(all_rows) < 2: return {}
        data_row = all_rows[1]
        result = {}
        for key, idx in col_map.items():
            if idx < len(data_row) and data_row[idx].strip():
                val = data_row[idx].strip()
                try: result[key] = json.loads(val)
                except (json.JSONDecodeError, ValueError): result[key] = val
        return result
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def write_json(data, output):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output: Path(output).parent.mkdir(parents=True, exist_ok=True); Path(output).write_text(text + "\n", encoding="utf-8")
    else: print(text)


def main():
    parser = argparse.ArgumentParser(description="健康档案管理 — 整理结构化健康档案")
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
