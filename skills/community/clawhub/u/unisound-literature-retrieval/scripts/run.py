#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""医学文献检索 — 临床问题 + 可选摘要片段，PICO 与延展检索建议（内部医疗大模型）。"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import urllib.error
import urllib.request

API_URL = "https://maas-api.hivoice.cn/v1/chat/completions"
MODEL = "u1-insuremed"


def _http_post(url: str, payload: Dict[str, Any], headers: Dict[str, str], *, timeout: int = 120) -> Any:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url=url,
        data=data,
        method="POST",
        headers={"Content-Type": "application/json", **headers},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e


def call_llm(system: str, user: str, appkey: str) -> str:
    payload = {"model": MODEL, "temperature": 0.0, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]}
    body = _http_post(API_URL, payload, {"Authorization": f"Bearer {appkey}"})
    try:
        return body["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Unexpected LLM response: {body}") from e


SYSTEM = """你是医学文献与循证方法学助手，帮助临床医生整理检索思路与证据叙事。

任务：
1. 将用户的临床问题改写为清晰的 PICO 要素（若信息不足，标注「待补充」）。
2. 若提供了文献片段，逐条提炼与问题的相关性及主要证据强度（叙述性，非正式 GRADE）。
3. 给出可操作的检索延展建议（同义词、MeSH 风格主题词思路、研究设计过滤思路等；勿伪造 PMID）。
4. Markdown 输出。末尾说明：未提供全文时结论仅为辅助草稿，不能替代系统评价与原文阅读。"""


def _normalize_passages(raw: Any) -> List[Dict[str, Any]]:
    if not isinstance(raw, list):
        return []
    out: List[Dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        title = (item.get("title") or "").strip()
        excerpt = (item.get("excerpt") or item.get("abstract") or "").strip()
        if not title and not excerpt:
            continue
        row: Dict[str, Any] = {}
        if title:
            row["title"] = title
        if item.get("year") not in (None, ""):
            row["year"] = item.get("year")
        if excerpt:
            row["excerpt"] = excerpt[:8000]
        out.append(row)
    return out


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    q = (data.get("clinical_question") or "").strip()
    if not q:
        raise ValueError("clinical_question 不能为空")
    constraints = (data.get("constraints") or "").strip()
    passages = _normalize_passages(data.get("passages"))

    user = f"""临床 / 科研问题：
{q}

{f"约束与偏好：{constraints}" if constraints else ""}

{"用户提供的文献片段：" if passages else "（当前未提供文献片段，请仅输出 PICO 重构与检索延展建议。）"}
```json
{json.dumps(passages, ensure_ascii=False, indent=2) if passages else "[]"}
```
"""

    text = call_llm(SYSTEM, user, appkey)
    return {
        "skill": "医学文献检索",
        "status": "ok",
        "data": {
            "clinical_question": q,
            "passage_count": len(passages),
            "has_passages": bool(passages),
        },
        "text": text,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="医学文献检索（临床科研）")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument(
        "--appkey",
        required=True,
        help="内部医疗大模型鉴权 key。",
    )
    args = parser.parse_args()
    inp = Path(args.input)
    if not inp.is_file():
        print(f"ERROR: 输入文件不存在: {inp}", file=sys.stderr)
        return 1
    try:
        data = json.loads(inp.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("输入须为 JSON 对象")
        out = build(data, args.appkey)
        text = json.dumps(out, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            p = Path(args.output)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
