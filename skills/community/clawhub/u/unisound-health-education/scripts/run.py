#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""健康知识科普 — 自包含skill，根据主题/关键词匹配文章并生成科普摘要"""

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
    "topic": ["topic", "主题"],
    "keywords": ["keywords", "关键词"],
}

ARTICLE_ALIASES = {
    "title": ["title", "标题"],
    "category": ["category", "分类", "类别"],
    "summary": ["summary", "摘要"],
    "keywords": ["keywords", "关键词"],
    "url": ["url", "链接"],
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


SYSTEM_PROMPT = """你是一位健康教育助手，帮助患者了解健康知识。

你的任务：
1. 根据用户提供的主题和关键词，从文章列表中匹配相关文章
2. 为匹配的文章生成简洁的科普摘要（每篇2-3句话要点）
3. 标注文章来源（如有URL）和可信度提示
4. 用Markdown格式组织输出，方便阅读

输出Markdown格式。末尾加免责提示：健康科普内容仅供了解，不替代医生诊疗建议。"""


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    topic = data.get("topic", "")
    keywords = as_list(data.get("keywords", []))
    articles = [item for item in as_list(data.get("articles")) if isinstance(item, dict)]

    # 本地关键词匹配
    terms = [str(topic).strip().lower()]
    terms.extend(str(k).strip().lower() for k in keywords)
    terms = [t for t in terms if t]

    matched = []
    for article in articles:
        text = " ".join(str(v).lower() for v in [
            article.get("title", ""),
            article.get("category", ""),
            article.get("summary", ""),
            " ".join(as_list(article.get("keywords", []))),
        ])
        if not terms or any(term in text for term in terms):
            matched.append({
                "title": article.get("title", ""),
                "category": article.get("category", ""),
                "summary": article.get("summary", ""),
                "url": article.get("url", ""),
            })

    user_prompt = f"""请为以下健康知识查询生成科普内容：

主题：{topic}
关键词：{json.dumps(keywords, ensure_ascii=False)}
总文章数：{len(articles)}，匹配数：{len(matched)}

匹配文章：
```json
{json.dumps(matched, ensure_ascii=False, indent=2)}
```

请为匹配的文章生成科普摘要，标注来源，给出健康提示。"""

    text = _call_llm(SYSTEM_PROMPT, user_prompt, appkey)

    return {
        "skill": "健康知识科普",
        "status": "ok",
        "data": {
            "topic": topic,
            "keywords": keywords,
            "matched_count": len(matched),
            "matched_articles": matched,
            "source_refs": [item.get("url", "") for item in matched if item.get("url")],
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
        meta = {}
        if len(all_rows) >= 2:
            header_row = all_rows[0]; data_row = all_rows[1]
            for canonical, aliases in field_aliases.items():
                for alias in aliases:
                    idx = first_matching_index({normalize_header(cell): i for i, cell in enumerate(header_row) if cell.strip()}, (alias, canonical))
                    if idx is not None and idx < len(data_row) and data_row[idx].strip():
                        val = data_row[idx].strip()
                        try: meta[canonical] = json.loads(val)
                        except (json.JSONDecodeError, ValueError): meta[canonical] = val
                        break
        articles = _parse_table_rows(all_rows, ARTICLE_ALIASES)
        if articles: meta["articles"] = articles
        return meta
    raise PreprocessError(f"Unsupported artifact kind: {kind}")


def write_json(data, output):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if output: Path(output).parent.mkdir(parents=True, exist_ok=True); Path(output).write_text(text + "\n", encoding="utf-8")
    else: print(text)


def main():
    parser = argparse.ArgumentParser(description="健康知识科普 — 根据主题匹配文章并生成科普摘要")
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
