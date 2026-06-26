#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""随访复诊提醒 — 自包含skill"""

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
    "disease_type": ["disease_type", "疾病类型", "疾病"],
    "last_visit_date": ["last_visit_date", "上次就诊", "上次就诊日期"],
    "followup_date": ["followup_date", "复诊日期"],
    "followup_interval_days": ["followup_interval_days", "间隔天数", "复诊间隔"],
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
    except HTTPError as exc:
        raise RuntimeError(f"API HTTP {exc.code}")
    except URLError as exc:
        raise RuntimeError(f"API unreachable: {exc.reason}")


def parse_date_safe(val: str) -> Optional[date]:
    if not val: return None
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d"]:
        try: return datetime.strptime(val.strip(), fmt).date()
        except ValueError: continue
    return None


SYSTEM_PROMPT = """你是一位贴心的患者管理助手，帮助慢性病患者按时复诊随访。

你的任务：
1. 根据患者的上次就诊日期和复诊周期，判断是否已逾期
2. 如已逾期，评估风险等级并说明定期复诊的重要性
3. 如即将到期，给出复诊准备提醒
4. 给出复诊前需准备的材料清单（病历、检查报告、用药清单、血压/血糖记录等）
5. 根据不同疾病类型给出针对性的复诊建议

输出Markdown格式，温馨关怀的语气。末尾加免责提示。"""


def build(data: Dict[str, Any], today: date, appkey: str) -> Dict[str, Any]:
    disease_type = data.get("disease_type", "")
    last_visit_date_str = data.get("last_visit_date", "")
    followup_date_str = data.get("followup_date", "")
    followup_interval = data.get("followup_interval_days", 0)
    note = data.get("note", "")

    last_visit = parse_date_safe(last_visit_date_str)

    if followup_date_str:
        followup_date = parse_date_safe(followup_date_str)
    elif last_visit and followup_interval:
        followup_date = last_visit + timedelta(days=int(followup_interval))
    else:
        raise ValueError("需要提供followup_date或(last_visit_date+followup_interval_days)")

    if followup_date is None:
        raise ValueError("无法计算复诊日期")

    days_overdue = (today - followup_date).days
    is_overdue = days_overdue > 0
    reminder_status = "overdue" if is_overdue else "scheduled"

    user_prompt = f"""请为以下患者生成复诊提醒：

疾病类型：{disease_type}
上次就诊：{last_visit_date_str}
复诊日期：{followup_date.isoformat()}
当前日期：{today.isoformat()}
是否逾期：{'是，已逾期' + str(days_overdue) + '天' if is_overdue else '否，还有' + str(-days_overdue) + '天'}
备注：{note}

请分析风险并给出复诊建议和准备清单。"""

    text = _call_llm(SYSTEM_PROMPT, user_prompt, appkey)

    return {
        "skill": "随访复诊提醒",
        "status": "ok",
        "data": {
            "disease_type": disease_type,
            "last_visit_date": last_visit_date_str,
            "followup_date": followup_date.isoformat(),
            "today": today.isoformat(),
            "is_overdue": is_overdue,
            "days_overdue": days_overdue,
            "reminder_status": reminder_status,
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
        for alias in aliases:
            header_map[normalize_header(alias)] = canonical
            header_map[normalize_header(canonical)] = canonical
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
                idx = first_matching_index(
                    {normalize_header(cell): i for i, cell in enumerate(header_row) if cell.strip()},
                    (alias, canonical))
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
    if output:
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def main():
    parser = argparse.ArgumentParser(description="随访复诊提醒")
    parser.add_argument("--input", required=True)
    parser.add_argument("--today", default=date.today().isoformat(), help="当前日期YYYY-MM-DD")
    parser.add_argument("--output", default="")
    parser.add_argument("--input-type", default="auto", choices=["auto", *sorted(SUPPORTED_FILE_TYPES)])
    parser.add_argument("--sheet", default="")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--save-prepared", action="store_true")
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
            pp = Path(args.output).with_suffix(".prepared.json") if args.output else input_path.with_suffix(".prepared.json")
            pp.parent.mkdir(parents=True, exist_ok=True)
            pp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        today_date = parse_date_safe(args.today)
        if today_date is None: raise ValueError(f"Invalid date: {args.today}")
        result = build(data, today_date, args.appkey)
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
