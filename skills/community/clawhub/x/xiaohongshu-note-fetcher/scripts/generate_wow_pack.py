#!/usr/bin/env python3
"""Generate an online mindmap URL from article list."""

from __future__ import annotations

import argparse
import base64
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


def load_rows(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("Input must be a JSON list from xhs_article_list.json")
    out = []
    for x in data:
        if isinstance(x, dict):
            out.append(x)
    return out


def pick_keywords(text: str) -> List[str]:
    tags = re.findall(r"#([^\s#]{2,20})", text or "")
    return [t.strip() for t in tags if t.strip()]


def build_mindmap_data(rows: List[Dict[str, Any]], keyword: str) -> Dict[str, Any]:
    top_tags: Counter[str] = Counter()
    for r in rows:
        top_tags.update(pick_keywords((r.get("title") or "") + " " + (r.get("desc") or "")))
    tag_children = [f"{k} ({v})" for k, v in top_tags.most_common(6)] or ["无明显标签聚类"]

    top_notes = rows[:5]
    top_note_children = [f"{(r.get('title') or 'Untitled')[:18]} | ❤️{r.get('liked_count', 0)}" for r in top_notes]

    strategy_children = [
        "爆款结构复盘（标题+开头钩子）",
        "系列化发布（同标签连续5天）",
        "封面/标题 AB 测试",
        "评论区关键词二次扩展",
    ]
    risk_children = [
        "避免内容搬运与侵权",
        "数据仅作选题参考",
        "商业合作需标注与合规",
    ]

    return {
        "central": f"小红书高赞选题池（{keyword or '关键词'}）",
        "branches": [
            {"label": "🏆 高赞Top", "children": top_note_children},
            {"label": "🏷️ 话题聚类", "children": tag_children},
            {"label": "🚀 下周动作", "children": strategy_children},
            {"label": "⚠️ 风险注意", "children": risk_children},
        ],
    }


def _sanitize_text(text: str) -> str:
    s = (text or "").replace("\n", " ").replace('"', "'").strip()
    return s[:120]


def build_mermaid_mindmap_text(mindmap_data: Dict[str, Any]) -> str:
    central = _sanitize_text(str(mindmap_data.get("central") or "选题导图"))
    lines = ["mindmap", f'  root["{central}"]']
    branch_index = 0
    for branch in mindmap_data.get("branches", []):
        if not isinstance(branch, dict):
            continue
        branch_index += 1
        label = _sanitize_text(str(branch.get("label") or "分支"))
        branch_id = f"b{branch_index}"
        lines.append(f'    {branch_id}["{label}"]')
        child_index = 0
        for child in branch.get("children", []):
            child_index += 1
            child_text = _sanitize_text(str(child))
            child_id = f"{branch_id}_{child_index}"
            lines.append(f'      {child_id}["{child_text}"]')
    return "\n".join(lines)


def build_mindmap_url(mindmap_data: Dict[str, Any]) -> str:
    mermaid_text = build_mermaid_mindmap_text(mindmap_data)
    payload = base64.urlsafe_b64encode(mermaid_text.encode("utf-8")).decode("ascii").rstrip("=")
    # Mermaid Ink accepts base64-encoded mermaid text in path.
    return f"https://mermaid.ink/svg/{payload}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an online mindmap URL from article list.")
    parser.add_argument("--input", required=True, help="Input article list JSON (xhs_article_list.json).")
    parser.add_argument("--keyword", default="", help="Keyword label override.")
    parser.add_argument(
        "--url-output",
        default="",
        help="Optional output txt path for the generated mindmap URL.",
    )
    args = parser.parse_args()

    rows = load_rows(Path(args.input))
    if not rows:
        raise SystemExit("Input rows empty.")
    keyword = args.keyword or "高赞内容"

    rows_sorted = sorted(rows, key=lambda x: int(x.get("liked_count", 0)), reverse=True)

    mindmap_data = build_mindmap_data(rows_sorted, keyword)
    mindmap_url = build_mindmap_url(mindmap_data)

    if args.url_output.strip():
        out_path = Path(args.url_output).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(mindmap_url + "\n", encoding="utf-8")
        print(f"Saved URL: {out_path}")

    print(f"Mindmap URL: {mindmap_url}")
    print("\nOutput guide:")
    print("- 直接把上面的 Mindmap URL 发给用户即可，无需再发导图文件。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
