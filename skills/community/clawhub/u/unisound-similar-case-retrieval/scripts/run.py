#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""相似病例检索 — 锚点病例对候选池的语义排序与可解释解读（内部医疗大模型）。"""

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
    body = _http_post(
        API_URL,
        payload,
        {"Authorization": f"Bearer {appkey}"},
    )
    try:
        return body["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as e:
        raise RuntimeError(f"Unexpected LLM response: {body}") from e


SYSTEM = """你是临床研究辅助助手，擅长病例基推理（Case-based Reasoning）风格的「相似病例」分析。

任务：
1. 将锚点病例与每条候选病例从诊断线索、时间轴、合并症、关键结局等维度对比。
2. 给出按相似度主观排序的列表（从最接近到较远），每条附简短「为何相似/差异」。
3. 指出可进一步做队列研究或亚组分析的方向。
4. 全文使用 Markdown。末尾附简短免责：结果由 AI 辅助生成，仅供科研参考，不构成诊疗建议。"""


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    anchor = (data.get("anchor_case") or "").strip()
    if not anchor:
        raise ValueError("anchor_case 不能为空")
    raw = data.get("candidate_cases")
    if not isinstance(raw, list) or not raw:
        raise ValueError("candidate_cases 必须为非空数组")
    candidates: List[Dict[str, Any]] = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict):
            continue
        cid = str(item.get("id", f"c{i}")).strip()
        summary = (item.get("summary") or "").strip()
        if summary:
            candidates.append({"id": cid, "summary": summary})
    if not candidates:
        raise ValueError("candidate_cases 中需至少一条含 summary 的病例")

    top_k = data.get("top_k", 5)
    try:
        top_k = max(1, min(20, int(top_k)))
    except (TypeError, ValueError):
        top_k = 5
    hint = (data.get("task_hint") or "").strip()

    user = f"""锚点病例：
{anchor}

候选病例（共 {len(candidates)} 条）：
```json
{json.dumps(candidates, ensure_ascii=False, indent=2)}
```

请重点展开讨论最接近的前 {top_k} 条与其余病例的差异。
{f"科研关注点：{hint}" if hint else ""}
"""

    text = call_llm(SYSTEM, user, appkey)
    return {
        "skill": "相似病例检索",
        "status": "ok",
        "data": {
            "anchor_case": anchor,
            "candidate_count": len(candidates),
            "top_k": top_k,
            "candidate_ids": [c["id"] for c in candidates],
        },
        "text": text,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="相似病例检索（临床科研）")
    parser.add_argument("--input", required=True, help="输入 JSON 路径")
    parser.add_argument("--output", default="", help="输出 JSON 路径（可选）")
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
