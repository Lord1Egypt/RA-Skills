#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""异常指标预警 — 自包含skill，表格形式分析异常"""

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
    "indicator_type": ["indicator_type", "指标类型"],
    "value": ["value", "值", "当前值"],
    "unit": ["unit", "单位"],
    "measured_at": ["measured_at", "测量时间"],
    "threshold_profile": ["threshold_profile", "阈值配置"],
    "suggested_action": ["suggested_action", "建议动作"],
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


INDICATOR_NAMES = {
    "blood_glucose": "血糖", "blood_pressure_systolic": "收缩压", "blood_pressure_diastolic": "舒张压",
    "heart_rate": "心率", "hba1c": "糖化血红蛋白", "total_cholesterol": "总胆固醇",
    "triglyceride": "甘油三酯", "ldl": "低密度脂蛋白", "hdl": "高密度脂蛋白",
    "uric_acid": "尿酸", "creatinine": "肌酐", "alt": "谷丙转氨酶", "ast": "谷草转氨酶",
}

SYSTEM_PROMPT = """你是一位临床检验分析助手，擅长解读异常检验指标。

你的任务：
1. 根据用户提供的异常指标数据，分析每个指标的异常程度
2. 用Markdown表格清晰展示：指标名称、当前值、正常参考范围、异常程度、可能原因、建议
3. 异常程度用 ⚠️偏高/偏低 或 🔴严重偏高/严重偏低 标注
4. 综合评估后给出就医建议优先级

输出Markdown格式表格和简要分析，末尾加免责提示。"""


def _check_abnormal(value: float, threshold: Dict) -> Dict:
    high = threshold.get("high")
    low = threshold.get("low")
    reasons = []
    if high is not None and float(value) > high:
        severity = "critical" if float(value) > high * 1.5 else "warning"
        reasons.append({"field": "value", "value": value, "rule": "high", "threshold": high, "alert_level": severity})
    if low is not None and float(value) < low:
        severity = "critical" if float(value) < low * 0.5 else "warning"
        reasons.append({"field": "value", "value": value, "rule": "low", "threshold": low, "alert_level": severity})
    if reasons:
        return {"is_abnormal": True, "alert_level": max(r["alert_level"] for r in reasons), "reason": reasons}
    return {"is_abnormal": False, "alert_level": "normal", "reason": []}


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    indicator_type = data.get("indicator_type", "")
    value = data.get("value", 0)
    unit = data.get("unit", "")
    measured_at = data.get("measured_at", "")
    threshold_profile = data.get("threshold_profile", {})

    check_result = _check_abnormal(float(value), threshold_profile)
    indicator_name = INDICATOR_NAMES.get(indicator_type, indicator_type)

    user_prompt = f"""请分析以下指标：

指标类型：{indicator_name}（{indicator_type}）
当前值：{value} {unit}
测量时间：{measured_at}
阈值配置：{json.dumps(threshold_profile, ensure_ascii=False)}
异常判定：{json.dumps(check_result, ensure_ascii=False)}

请用Markdown表格形式分析，包含：指标名、当前值、正常范围、异常程度、可能原因（至少2-3个）、建议。"""

    text = _call_llm(SYSTEM_PROMPT, user_prompt, appkey)

    return {
        "skill": "异常指标预警",
        "status": "ok",
        "data": {
            "indicator_type": indicator_type, "value": value, "unit": unit,
            "measured_at": measured_at,
            "is_abnormal": check_result["is_abnormal"],
            "alert_level": check_result["alert_level"],
            "reason": check_result["reason"],
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
    parser = argparse.ArgumentParser(description="异常指标预警 — 表格形式分析异常指标")
    parser.add_argument("--input", required=True)
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
