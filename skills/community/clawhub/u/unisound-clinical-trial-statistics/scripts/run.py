#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""临床试验数据统计 — 自包含skill，计算描述性统计并解读结果"""

import argparse, json, math, re, sys
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
    "trial_id": ["trial_id", "试验编号", "试验ID"],
    "population": ["population", "分析集"],
    "group_field": ["group_field", "分组字段"],
    "endpoint_fields": ["endpoint_fields", "endpoint_field", "终点字段", "终点字段列表"],
    "records": ["records", "data", "记录", "数据"],
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


def parse_number(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)) and not isinstance(value, bool): return float(value)
    text = str(value or "").strip().replace("%", "")
    if not text: return None
    try: return float(text)
    except ValueError: return None


def describe(values: List[float]) -> Dict[str, Any]:
    n = len(values)
    mean = sum(values) / n if n else None
    sd = None
    if n > 1 and mean is not None:
        sd = math.sqrt(sum((v - mean) ** 2 for v in values) / (n - 1))
    return {"n": n, "mean": round(mean, 4) if mean is not None else None,
            "sd": round(sd, 4) if sd is not None else None,
            "min": round(min(values), 4) if values else None,
            "max": round(max(values), 4) if values else None}


def infer_endpoint_fields(records: List[Dict[str, Any]], group_field: str) -> List[str]:
    if not records: return []
    endpoints = []
    ignored = {group_field, "subject_id", "id", "trial_id", "population"}
    for key in records[0].keys():
        if key in ignored: continue
        if any(parse_number(row.get(key)) is not None for row in records):
            endpoints.append(key)
    return endpoints


SYSTEM_PROMPT = """你是一位临床试验统计分析师，帮助解读临床试验数据的统计结果。

你的任务：
1. 解读各终点指标的描述性统计结果（均值、标准差、范围）
2. 分析组间差异的临床意义（不仅仅是统计显著性）
3. 指出统计结果的局限性（样本量、偏倚、混杂因素）
4. 用Markdown表格展示关键统计结果

输出Markdown格式。末尾加免责提示：本分析为AI辅助描述性统计，不替代专业统计师的正式分析。"""


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    records = data.get("records") or data.get("data")
    if not isinstance(records, list) or not records: raise ValueError("records must contain at least one row")
    records = [r for r in records if isinstance(r, dict)]
    if not records: raise ValueError("records must contain object rows")

    group_field = str(data.get("group_field") or "group")
    endpoint_fields = [str(item) for item in as_list(data.get("endpoint_fields") or data.get("endpoint_field"))]
    if not endpoint_fields: endpoint_fields = infer_endpoint_fields(records, group_field)
    if not endpoint_fields: raise ValueError("endpoint_fields is required")

    # 本地计算描述性统计
    group_order = []
    for row in records:
        g = str(row.get(group_field, "未分组"))
        if g not in group_order: group_order.append(g)

    statistics = []
    for endpoint in endpoint_fields:
        groups = []
        means = {}
        for group in group_order:
            values = []
            for row in records:
                if str(row.get(group_field, "未分组")) != group: continue
                parsed = parse_number(row.get(endpoint))
                if parsed is not None: values.append(parsed)
            summary = describe(values)
            means[group] = summary["mean"]
            groups.append({"group": group, **summary})

        differences = []
        base_group = group_order[0] if group_order else ""
        base_mean = means.get(base_group)
        if base_mean is not None:
            for group in group_order[1:]:
                mean = means.get(group)
                if mean is not None:
                    differences.append({"comparison": f"{group} - {base_group}", "mean_difference": round(mean - base_mean, 4)})
        statistics.append({"endpoint": endpoint, "groups": groups, "mean_differences": differences})

    # 调用API解读统计结果
    user_prompt = f"""请解读以下临床试验统计结果：

试验ID：{data.get('trial_id', '')}
分析集：{data.get('population', '')}
分组字段：{group_field}
组别：{json.dumps(group_order, ensure_ascii=False)}
总样本量：{len(records)}

统计结果：
```json
{json.dumps(statistics, ensure_ascii=False, indent=2)}
```

请解读各终点指标的统计结果，分析组间差异的临床意义，说明局限性。"""

    text = _call_llm(SYSTEM_PROMPT, user_prompt, appkey)

    return {
        "skill": "临床试验数据统计",
        "status": "ok",
        "data": {
            "trial_id": data.get("trial_id", ""),
            "population": data.get("population", ""),
            "statistics": statistics,
        },
        "text": text.strip(),
    }


# ── 多格式解析 ──

def load_json(path: str) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list): return {"records": data}
    if not isinstance(data, dict): raise ValueError("input must be a JSON object or record list")
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


def table_rows_to_records(all_rows):
    if len(all_rows) < 2: return []
    header = [cell.strip() for cell in all_rows[0]]
    records = []
    for row in all_rows[1:]:
        item = {}
        for idx, key in enumerate(header):
            if not key or idx >= len(row) or not row[idx].strip(): continue
            value = row[idx].strip()
            number = parse_number(value)
            item[key] = number if number is not None else value
        if item: records.append(item)
    return records


def normalize_artifact(artifact, field_aliases=None):
    if field_aliases is None: field_aliases = FIELD_ALIASES
    kind = artifact.get("kind")
    if kind == "json":
        data = artifact["data"]
        if isinstance(data, list): return {"records": data}
        if isinstance(data, dict): return data
        raise PreprocessError("JSON input must be an object or record list.")
    if kind == "text":
        text = artifact.get("text", "")
        try:
            data = json.loads(text)
            if isinstance(data, list): return {"records": data}
            if isinstance(data, dict): return data
        except (json.JSONDecodeError, ValueError): pass
        return parse_text_kv(text, FIELD_ALIASES)
    if kind == "tables":
        all_rows = []
        for table in artifact.get("tables", []): all_rows.extend(table.get("rows", []))
        if not all_rows: raise PreprocessError("No data rows found.")
        records = table_rows_to_records(all_rows)
        meta = {"records": records}
        if len(all_rows) >= 2:
            for canonical, aliases in FIELD_ALIASES.items():
                if canonical == "records": continue
                idx = first_matching_index({normalize_header(cell): i for i, cell in enumerate(all_rows[0]) if cell.strip()}, tuple(aliases) + (canonical,))
                if idx is not None and idx < len(all_rows[1]) and all_rows[1][idx].strip():
                    meta.setdefault(canonical, all_rows[1][idx].strip())
        return meta
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def write_json(data, output):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output: Path(output).parent.mkdir(parents=True, exist_ok=True); Path(output).write_text(text + "\n", encoding="utf-8")
    else: print(text)


def main():
    parser = argparse.ArgumentParser(description="临床试验数据统计 — 描述性统计与解读")
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
        else: data = normalize_artifact(load_input_artifact(input_path, input_type, args.encoding, args.sheet))
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
