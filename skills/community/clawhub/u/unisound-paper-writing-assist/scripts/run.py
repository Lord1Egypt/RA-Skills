#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""论文写作辅助 — IMRaD 章节级草稿与报告规范提醒（内部医疗大模型）。"""

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


SYSTEM = """你是医学学术写作编辑，协助作者将要点组织为符合 IMRaD 习惯的学术中文或英文段落草稿。

规则：
1. 只根据用户给出的要点组织语言；不得编造数据、样本量、p 值或参考文献。
2. 若要点不足，用 Markdown 列出「待作者补充」清单，而非虚构内容。
3. 输出主体为章节草稿；其后附简短「写作自检」提示（可提及 CONSORT/STROBE 等仅为提醒，非认证）。
4. 末尾声明：草稿由 AI 辅助生成，须由作者审阅修改并对学术内容负责。"""


def _as_notes(raw: Any) -> List[str]:
    if raw is None:
        return []
    if isinstance(raw, str) and raw.strip():
        return [raw.strip()]
    if isinstance(raw, list):
        return [str(x).strip() for x in raw if str(x).strip()]
    raise ValueError("notes 须为字符串或非空字符串数组")


def build(data: Dict[str, Any], appkey: str) -> Dict[str, Any]:
    section = (data.get("section") or "").strip()
    if not section:
        raise ValueError("section 不能为空")
    lang = (data.get("language") or "zh").strip().lower()
    if lang not in ("zh", "en"):
        lang = "zh"
    notes = _as_notes(data.get("notes"))
    if not notes:
        raise ValueError("notes 不能为空")
    journal = (data.get("journal_style_hint") or "").strip()

    user = f"""目标章节：{section}
写作语言：{"中文" if lang == "zh" else "English"}

要点列表：
{chr(10).join(f"- {n}" for n in notes)}

{f"期刊 / 风格提示：{journal}" if journal else ""}

请输出该章节的连贯草稿（可适当分子标题），并附写作自检 bullet。"""

    text = call_llm(SYSTEM, user, appkey)
    return {
        "skill": "论文写作辅助",
        "status": "ok",
        "data": {
            "section": section,
            "language": lang,
            "note_count": len(notes),
        },
        "text": text,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="论文写作辅助（临床科研）")
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
