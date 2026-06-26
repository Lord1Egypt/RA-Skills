#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""药物靶点筛选 — 自包含skill，对候选靶点进行优先级排序"""

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
    "disease": ["disease", "indication", "疾病", "适应症"],
    "targets": ["targets", "候选靶点", "靶点列表"],
}

TARGET_ALIASES = {
    "target": ["target", "gene", "symbol", "靶点", "基因"],
    "mechanism": ["mechanism", "作用机制", "机制"],
    "evidence": ["evidence", "evidence_strength", "证据", "证据强度"],
    "druggability": ["druggability", "可成药性"],
    "safety_risk": ["safety_risk", "safety", "安全风险", "安全性"],
    "references": ["references", "refs", "引用", "来源"],
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
        return parts if len(parts) > 1 else [value]
    return [value]


def score_value(value: Any, *, risk: bool = False) -> float:
    if isinstance(value, (int, float)): return float(value)
    text = str(value or "").strip().lower()
    mapping = {"high": 3.0, "strong": 3.0, "高": 3.0, "强": 3.0,
               "medium": 2.0, "moderate": 2.0, "中": 2.0,
               "low": 1.0, "weak": 1.0, "低": 1.0, "弱": 1.0}
    if text in mapping: return mapping[text]
    return 1.0 if risk else 0.0


def priority_level(score: float) -> str:
    if score >= 7: return "high"
    if score >= 4: return "medium"
    return "low"


SYSTEM_PROMPT = """你是一位药物研发靶点筛选专家，帮助团队评估候选药物靶点。

你的任务：
1. 根据疾病/适应症和候选靶点信息，对靶点进行优先级排序
2. 综合考虑证据强度、可成药性、安全性、机制新颖性
3. 为每个靶点给出推荐理由和风险提示
4. 用Markdown表格展示排序结果

输出Markdown格式。末尾加免责提示：靶点筛选结果为AI辅助分析，需经实验验证。"""


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    disease = data.get("disease", "") or data.get("indication", "")
    if not disease: raise ValueError("missing required field: disease")

    raw_targets = as_list(data.get("targets", []))
    alias_map = {}
    for canonical, aliases in TARGET_ALIASES.items():
        for alias in aliases: alias_map[normalize_header(alias)] = canonical; alias_map[normalize_header(canonical)] = canonical
    targets = []
    for item in raw_targets:
        if isinstance(item, str): targets.append({"target": item})
        elif isinstance(item, dict):
            norm = {}
            for k, v in item.items():
                c = alias_map.get(normalize_header(str(k)))
                if c: norm[c] = v
            targets.append(norm)
    targets = [t for t in targets if t.get("target")]
    if not targets: raise ValueError("targets must contain at least one target")

    # 本地计算优先级评分
    ranked = []
    for item in targets:
        evidence_score = score_value(item.get("evidence"))
        drug_score = score_value(item.get("druggability"))
        risk_score = score_value(item.get("safety_risk"), risk=True)
        score = round(evidence_score * 2 + drug_score * 1.5 - risk_score, 2)
        ranked.append({
            "target": item.get("target", ""),
            "mechanism": item.get("mechanism", ""),
            "evidence": item.get("evidence", ""),
            "druggability": item.get("druggability", ""),
            "safety_risk": item.get("safety_risk", ""),
            "priority_score": score,
            "priority_level": priority_level(score),
            "references": as_list(item.get("references", [])),
        })
    ranked.sort(key=lambda r: r["priority_score"], reverse=True)

    user_prompt = f"""请分析以下靶点筛选结果：

适应症：{disease}
候选靶点数：{len(ranked)}

排序结果：
```json
{json.dumps(ranked, ensure_ascii=False, indent=2)}
```

评分规则：priority_score = evidence×2 + druggability×1.5 - safety_risk（high=3, medium=2, low=1）
优先级：score≥7=high, 4≤score<7=medium, <4=low

请解读排序结果，为每个靶点给出推荐理由，分析风险，给出下一步建议。"""

    text = _call_llm(SYSTEM_PROMPT, user_prompt, appkey)

    return {
        "skill": "药物靶点筛选",
        "status": "ok",
        "data": {
            "disease": disease,
            "ranked_targets": ranked,
            "screening_basis": "按证据强度(×2)、可成药性(×1.5)和安全风险(-)加权排序。",
        },
        "text": text.strip(),
    }


# ── 多格式解析 ──

def load_json(path: str) -> Dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list): return {"targets": data}
    if not isinstance(data, dict): raise ValueError("input must be a JSON object or target list")
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


def _parse_table_rows(all_rows, aliases):
    if not all_rows: return []
    header_row = all_rows[0]
    col_map = {}
    for canonical, alias_list in aliases.items():
        for alias in alias_list:
            idx = first_matching_index({normalize_header(cell): i for i, cell in enumerate(header_row) if cell.strip()}, (alias, canonical))
            if idx is not None: col_map[canonical] = idx; break
    rows_out = []
    for data_row in all_rows[1:]:
        row_dict = {}
        for key, idx in col_map.items():
            if idx < len(data_row) and data_row[idx].strip():
                val = data_row[idx].strip()
                try: row_dict[key] = json.loads(val)
                except (json.JSONDecodeError, ValueError): row_dict[key] = val
        if row_dict: rows_out.append(row_dict)
    return rows_out


def normalize_artifact(artifact, field_aliases=None):
    if field_aliases is None: field_aliases = FIELD_ALIASES
    kind = artifact.get("kind")
    if kind == "json":
        data = artifact["data"]
        if isinstance(data, list): return {"targets": data}
        if isinstance(data, dict): return data
        raise PreprocessError("JSON input must be an object or target list.")
    if kind == "text":
        text = artifact.get("text", "")
        try:
            data = json.loads(text)
            if isinstance(data, list): return {"targets": data}
            if isinstance(data, dict): return data
        except (json.JSONDecodeError, ValueError): pass
        return parse_text_kv(text, FIELD_ALIASES)
    if kind == "tables":
        all_rows = []
        for table in artifact.get("tables", []): all_rows.extend(table.get("rows", []))
        if not all_rows: raise PreprocessError("No data rows found.")
        targets = _parse_table_rows(all_rows, TARGET_ALIASES)
        meta = {}
        if len(all_rows) >= 2:
            header_row = all_rows[0]; data_row = all_rows[1]
            for canonical, aliases in FIELD_ALIASES.items():
                if canonical == "targets": continue
                for alias in aliases:
                    idx = first_matching_index({normalize_header(cell): i for i, cell in enumerate(header_row) if cell.strip()}, (alias, canonical))
                    if idx is not None and idx < len(data_row) and data_row[idx].strip():
                        meta[canonical] = data_row[idx].strip(); break
        if targets: meta["targets"] = targets
        return meta
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def write_json(data, output):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output: Path(output).parent.mkdir(parents=True, exist_ok=True); Path(output).write_text(text + "\n", encoding="utf-8")
    else: print(text)


def main():
    parser = argparse.ArgumentParser(description="药物靶点筛选 — 对候选靶点进行优先级排序")
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
