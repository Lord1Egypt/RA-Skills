#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from shared_utils import chat_completion, load_json, parse_dt, slugify, sort_by_score_then_published, write_json

CATEGORIES = [
    "ai-frontier-tech",
    "vc-investment",
    "startup-strategy",
    "business-insights",
    "china-tech-market",
    "product-design",
    "learning-career",
    "productivity-tools",
    "strategy-analysis",
    "other",
]

SYSTEM = """You are Phase-B analyzer for RSS-Brew.
Return STRICT JSON only with keys:
- category (one allowed kebab-case category)
- english_summary (2-4 sentences)
- chinese_summary (2-4 sentences)
- deep_analysis (object, optional when score<4)
If deep_analysis exists include:
- paragraph_summaries (array of 2-5 bullets)
- underwater_insights (string)
- golden_quotes (array of 1-2 strings)
Do not output markdown.
"""


def pick_deep_set(scored: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], bool]:
    ranked = sort_by_score_then_published(scored)
    high_signal = [a for a in ranked if int(a.get("score", 0)) >= 4]

    # Explicit UX guardrail:
    # keep enough items in "Other New Articles" so the digest never feels empty.
    min_other = 2 if len(ranked) <= 5 else 5
    base_cap = 3 if len(ranked) <= 5 else 5
    cap_by_other = max(1, len(ranked) - min_other)
    cap = min(base_cap, cap_by_other)

    if high_signal:
        return high_signal[:cap], False

    return ranked[: min(3, cap_by_other)], True


def analyze_one(article: Dict[str, Any], model_alias: str, mock: bool = False) -> Dict[str, Any]:
    score = int(article.get("score", 0))
    summary = (article.get("summary") or "").strip()
    text = (article.get("text") or "")[:1800]
    body = summary or text

    prompt = (
        f"Allowed categories: {', '.join(CATEGORIES)}\n"
        f"Article title: {article.get('title','')}\n"
        f"Source: {article.get('source','')}\n"
        f"Published: {article.get('published','')}\n"
        f"URL: {article.get('url','')}\n"
        f"Phase-A score: {score}\n"
        f"Content:\n{body}\n"
        "If score < 4, do not include deep_analysis."
    )
    if mock:
        data = {
            "category": "other",
            "english_summary": f"{article.get('title','')} — mock English summary.",
            "chinese_summary": f"{article.get('title','')}——模拟中文摘要。",
        }
        if score >= 4:
            data["deep_analysis"] = {
                "paragraph_summaries": ["Mock point 1", "Mock point 2"],
                "underwater_insights": "Mock contrarian insight.",
                "golden_quotes": ["Mock quote"],
            }
    else:
        content = chat_completion(model_alias, SYSTEM, prompt)
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            start, end = content.find("{"), content.rfind("}")
            if start >= 0 and end > start:
                data = json.loads(content[start : end + 1])
            else:
                raise

    category = str(data.get("category", "other")).strip().lower()
    if category not in CATEGORIES:
        category = "other"
    article["category"] = category
    article["english_summary"] = str(data.get("english_summary", "")).strip()
    article["chinese_summary"] = str(data.get("chinese_summary", "")).strip()
    if score >= 4 and isinstance(data.get("deep_analysis"), dict):
        article["deep_analysis"] = data["deep_analysis"]
    return article


def write_single_article_md(item: Dict[str, Any], data_root: Path) -> None:
    if int(item.get("score", 0)) < 4:
        return
    category = item.get("category", "other")
    folder = data_root / category
    folder.mkdir(parents=True, exist_ok=True)
    date_s = parse_dt(item.get("published", "")).strftime("%Y-%m-%d")
    filename = f"{slugify(item.get('title','untitled'))}_{date_s}.md"
    p = folder / filename

    deep = item.get("deep_analysis") or {}
    bullets = deep.get("paragraph_summaries") or []
    quotes = deep.get("golden_quotes") or []
    stars = "⭐" * int(item.get("score", 0)) + "☆" * (5 - int(item.get("score", 0)))

    lines = [
        "---",
        f"title: \"{item.get('title','')}\"",
        f"date: \"{item.get('published','')}\"",
        f"source: \"{item.get('source','')}\"",
        f"url: \"{item.get('url','')}\"",
        f"category: \"{item.get('category','other')}\"",
        f"score: {int(item.get('score',0))}",
        "---",
        "",
        f"# {item.get('title','')}",
        "",
        f"## 📊 Evaluation Score: {int(item.get('score',0))}/5 ({stars})",
        "",
        "## 🇬🇧 English Summary",
        item.get("english_summary", ""),
        "",
        "## 🇨🇳 中文摘要 (Chinese Summary)",
        item.get("chinese_summary", ""),
    ]

    if int(item.get("score", 0)) >= 4:
        lines += [
            "",
            "## 🔍 Deep Analysis (Only if Score ≥ 4)",
            "### Key Points / Paragraph Summaries",
        ]
        for b in bullets[:5]:
            lines.append(f"- {b}")
        lines += [
            "",
            "### 💡 Underwater Insights (Hidden/Contrarian views)",
            str(deep.get("underwater_insights", "")),
            "",
            "### 💬 Golden Quotes",
        ]
        for q in quotes[:2]:
            lines.append(f"> \"{q}\"")

    p.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase B analysis (GLM) + deep-set")
    ap.add_argument("--input", required=True, help="scored-articles.json or preselected deep-set.json")
    ap.add_argument("--output", required=True, help="deep-set.json")
    ap.add_argument("--data-root", required=True, help="rss data root")
    ap.add_argument("--model", default="GLM", help="Model alias, default GLM")
    ap.add_argument("--mock", action="store_true", help="Mock mode without model API")
    ap.add_argument("--preselected", action="store_true", help="Treat --input as preselected deep-set list (V2)")
    args = ap.parse_args()

    scored_payload = load_json(Path(args.input), {})
    scored = scored_payload.get("articles", []) or []
    if args.preselected:
        deep_set = scored
        fallback_used = False
    else:
        deep_set, fallback_used = pick_deep_set(scored)

    print(f"[phase_b] model={args.model} deep_set={len(deep_set)} fallback_top3={fallback_used}")
    out_items: List[Dict[str, Any]] = []
    for i, article in enumerate(deep_set, start=1):
        try:
            analyzed = analyze_one(dict(article), args.model, mock=args.mock)
            out_items.append(analyzed)
            write_single_article_md(analyzed, Path(args.data_root))
            print(f"[phase_b] analyzed {i}/{len(deep_set)}")
        except Exception as e:
            print(f"[phase_b] ERROR analyze index={i-1}: {e}", file=sys.stderr)
            sys.exit(21)

    out_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "fallback_top3": fallback_used,
        "article_count": len(out_items),
        "articles": out_items,
    }
    write_json(Path(args.output), out_payload)
    print(f"[phase_b] wrote {args.output}")


if __name__ == "__main__":
    main()
