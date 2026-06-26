#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用药记录管理 — 自包含skill，整理和分类用药记录"""

import argparse, json, re, sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_URL = "https://maas-api.hivoice.cn/v1/chat/completions"
MODEL = "u1-insuremed"

from preprocess import (
    PreprocessError, SUPPORTED_FILE_TYPES,
    detect_input_type, load_input_artifact, first_matching_index, normalize_header,
)

FIELD_ALIASES = {
    "medicine_name": ["medicine_name", "药品名称", "药品"],
    "dose": ["dose", "剂量"],
    "frequency": ["frequency", "频次"],
    "start_date": ["start_date", "开始日期"],
    "end_date": ["end_date", "结束日期"],
    "status": ["status", "状态"],
    "note": ["note", "备注"],
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


SYSTEM_PROMPT = """你是一位用药管理助手，帮助患者整理和回顾用药记录。

你的任务：
1. 分类用药记录：正在服用(active) vs 已停用(stopped)
2. 整理用药摘要，按药品名称列出服用方案
3. 标注长期用药（服用超过30天）和短期用药
4. 检查是否有药品相互作用风险提示（常见组合）
5. 用Markdown格式展示，包含表格

输出Markdown格式。末尾加免责提示：本内容仅供参考，用药请遵医嘱。"""


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    source = data.get("medications")
    if source is None and data.get("medicine_name"):
        source = [data]

    medications = []
    for item in as_list(source):
        if not isinstance(item, dict): continue
        medications.append({
            "medicine_name": item.get("medicine_name", ""),
            "dose": item.get("dose", ""),
            "frequency": item.get("frequency", ""),
            "start_date": item.get("start_date", ""),
            "end_date": item.get("end_date", ""),
            "status": item.get("status", "active"),
            "note": item.get("note", ""),
        })

    # 本地分类
    active = [m for m in medications if m.get("status") == "active"]
    stopped = [m for m in medications if m.get("status") != "active"]

    user_prompt = f"""请整理以下用药记录：

总记录数：{len(medications)}
正在服用：{len(active)}种
已停用：{len(stopped)}种

正在服用的药品：
```json
{json.dumps(active, ensure_ascii=False, indent=2)}
```

已停用的药品：
```json
{json.dumps(stopped, ensure_ascii=False, indent=2)}
```

请生成用药管理摘要，分类展示，标注长期/短期用药，给出用药提醒。"""

    text = _call_llm(SYSTEM_PROMPT, user_prompt, appkey)

    return {
        "skill": "用药记录管理",
        "status": "ok",
        "data": {
            "medications": medications,
            "active_medications": active,
            "stopped_medications": stopped,
            "history_summary": {"total": len(medications), "active": len(active), "stopped": len(stopped)},
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
        medications = []
        for row in all_rows[1:]:
            item = {}
            for key, idx in col_map.items():
                if idx < len(row) and row[idx].strip():
                    val = row[idx].strip()
                    try: item[key] = json.loads(val)
                    except (json.JSONDecodeError, ValueError): item[key] = val
            if item: medications.append(item)
        return {"medications": medications}
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def write_json(data, output):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output: Path(output).parent.mkdir(parents=True, exist_ok=True); Path(output).write_text(text + "\n", encoding="utf-8")
    else: print(text)


def main():
    parser = argparse.ArgumentParser(description="用药记录管理 — 整理和分类用药记录")
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
