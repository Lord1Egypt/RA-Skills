#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""今日康复任务 — 自包含skill，将任务转为时间线提醒"""

import argparse, json, re, sys
from datetime import date, datetime, timedelta
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
    "plan_id": ["plan_id", "planId", "计划ID"],
    "tasks": ["tasks", "任务列表"],
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


SYSTEM_PROMPT = """你是一位暖心的康复教练，帮助术后患者完成每日康复任务。

你的任务：
1. 将康复任务列表转化为分时段的提醒清单（上午/下午/晚上）
2. 每条任务标注：具体动作名称、建议执行时间、频次、执行要点、状态（✅已完成/⏳待完成）
3. 统计完成进度并给出鼓励
4. 对未完成任务给出温和提醒
5. 用Markdown格式展示，包含emoji让内容更亲切

重要：你是在提醒用户做任务，不是简单地罗列任务。语气要积极鼓励。

输出Markdown格式。"""


def build(data: Dict[str, Any], target_date: date, appkey: str) -> Dict[str, Any]:
    plan_id = data.get("plan_id", "")
    all_tasks = as_list(data.get("tasks", []))

    # 筛选当日任务
    today_str = target_date.isoformat()
    today_tasks = [t for t in all_tasks if str(t.get("date", "")).startswith(today_str)]

    completed = [t for t in today_tasks if t.get("status") == "completed"]
    pending = [t for t in today_tasks if t.get("status") != "completed"]

    if not today_tasks:
        text = f"### 📋 {today_str} 康复任务\n\n今天没有安排的康复任务。请注意休息，按计划进行康复。"
    else:
        user_prompt = f"""请为以下今日康复任务生成提醒：

日期：{today_str}
计划ID：{plan_id}

已完成任务：{json.dumps(completed, ensure_ascii=False)}
待完成任务：{json.dumps(pending, ensure_ascii=False)}
完成进度：{len(completed)}/{len(today_tasks)}

请将任务转为分时段提醒格式（上午/下午/晚上），标注每条任务的状态，给出鼓励语。"""

        text = _call_llm(SYSTEM_PROMPT, user_prompt, appkey)

    return {
        "skill": "今日康复任务",
        "status": "ok",
        "data": {
            "plan_id": plan_id, "date": today_str,
            "today_tasks": today_tasks,
            "completion_summary": {"total": len(today_tasks), "completed": len(completed), "pending": len(pending)},
            "pending_tasks": pending,
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


def parse_date_safe(val: str) -> Optional[date]:
    if not val: return None
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]:
        try: return datetime.strptime(val.strip(), fmt).date()
        except ValueError: continue
    return None


def main():
    parser = argparse.ArgumentParser(description="今日康复任务 — 时间线提醒格式")
    parser.add_argument("--input", required=True)
    parser.add_argument("--date", default=date.today().isoformat(), help="目标日期YYYY-MM-DD")
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
        target = parse_date_safe(args.date)
        if target is None: raise ValueError(f"Invalid date: {args.date}")
        result = build(data, target, args.appkey)
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
