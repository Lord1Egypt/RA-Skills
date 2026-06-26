#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

from shared_utils import load_json, write_json

PROMO_WORDS = {
    "sponsored",
    "sponsor",
    "register now",
    "sign up",
    "webinar",
    "limited time",
    "promo",
    "promotion",
    "buy now",
    "book now",
}
CTA_WORDS = {
    "subscribe",
    "join now",
    "start free",
    "request demo",
    "get started",
    "book a demo",
}
DOMAIN_WORDS = {
    "vc",
    "venture",
    "startup",
    "founder",
    "funding",
    "capital",
    "ai",
    "china",
    "market",
    "strategy",
    "robotics",
    "business",
}
PRODUCT_WORDS = {"launch", "announces", "release", "tool", "product", "platform", "feature"}
CONTEXT_WORDS = {"use case", "customer", "revenue", "business", "pain point", "problem", "workflow"}
BALANCED_MARKERS = {"however", "on the other hand", "pros and cons", "tradeoff", "trade-off", "but"}


def _text_fields(article: Dict[str, Any]) -> Tuple[str, str, str]:
    title = str(article.get("title") or "")
    summary = str(article.get("summary") or "")
    text = str(article.get("text") or "")
    return title, summary, text


def _contains_any(haystack: str, needles: set[str]) -> bool:
    h = haystack.lower()
    return any(n in h for n in needles)


def _list_like_bonus(text: str) -> bool:
    low = text.lower()
    if re.search(r"\b(top\s*\d+|\d+\s+(examples|ways|cases))\b", low):
        return True
    numbered = len(re.findall(r"(^|\n)\s*(\d+\.|[-*])\s+", text))
    return numbered >= 5


def _quality_bad(text: str) -> bool:
    if not text:
        return True
    bad_char_ratio = text.count("�") / max(1, len(text))
    weird_ratio = len(re.findall(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", text)) / max(1, len(text))
    return bad_char_ratio > 0.01 or weird_ratio > 0.01


def _score_article(article: Dict[str, Any], seen_titles: set[str]) -> Dict[str, Any]:
    title, summary, text = _text_fields(article)
    merged = f"{title}\n{summary}\n{text}"
    low = merged.lower()

    plus_tags: List[str] = []
    minus_tags: List[str] = []
    rule_score = 0

    if len(text) > 2000:
        plus_tags.append("length_gt_2000")
        rule_score += 1
    if len(text) > 5000:
        plus_tags.append("length_gt_5000")
        rule_score += 1
    if _list_like_bonus(text):
        plus_tags.append("multi_case_roundup")
        rule_score += 1
    if _contains_any(low, BALANCED_MARKERS):
        plus_tags.append("balanced_structure")
        rule_score += 1

    promo_like = _contains_any(low, PROMO_WORDS)
    heavy_cta = _contains_any(low, CTA_WORDS)
    teaser = len(summary.strip()) < 80 and len(text.strip()) < 400
    corrupted = _quality_bad(text)
    product_without_context = _contains_any(low, PRODUCT_WORDS) and not _contains_any(low, CONTEXT_WORDS)

    if promo_like:
        minus_tags.append("promo_like")
        rule_score -= 1
    if heavy_cta:
        minus_tags.append("heavy_cta")
        rule_score -= 3
    if teaser:
        minus_tags.append("teaser_only")
        rule_score -= 1
    if corrupted:
        minus_tags.append("corrupted_extraction")
        rule_score -= 2
    if product_without_context:
        minus_tags.append("product_without_context")
        rule_score -= 1

    normalized_title = re.sub(r"\W+", " ", title.lower()).strip()
    duplicate_title = bool(normalized_title and normalized_title in seen_titles)
    if normalized_title:
        seen_titles.add(normalized_title)

    reject = False
    reject_reason = ""
    if duplicate_title:
        reject = True
        reject_reason = "duplicate_title"
    elif corrupted:
        reject = True
        reject_reason = "corrupted_extraction"
    elif teaser and not _contains_any(low, {"breaking", "urgent", "acquires", "raises"}):
        reject = True
        reject_reason = "teaser_only"
    elif promo_like and heavy_cta:
        reject = True
        reject_reason = "promo_cta"

    return {
        **article,
        "rule_score": rule_score,
        "rule_plus_tags": plus_tags,
        "rule_minus_tags": minus_tags,
        "rule_reject": reject,
        "rule_reject_reason": reject_reason,
        "rule_floor_relaxed": False,
    }


def _apply_floor_fallback(scored_items: List[Dict[str, Any]], floor_count: int, allow_promo_cta: bool = False) -> None:
    passed = [a for a in scored_items if not a.get("rule_reject")]
    if len(passed) >= floor_count:
        return

    rejected = [a for a in scored_items if a.get("rule_reject")]

    # Conservative default: only relax teaser-only rejections.
    # promo_cta remains rejected unless explicitly allowed.
    relax_reasons = {"teaser_only"}
    if allow_promo_cta:
        relax_reasons.add("promo_cta")

    relaxable = [a for a in rejected if a.get("rule_reject_reason") in relax_reasons]
    relaxable.sort(key=lambda a: int(a.get("rule_score", 0)), reverse=True)

    needed = max(0, floor_count - len(passed))
    for item in relaxable[:needed]:
        item["rule_reject"] = False
        item["rule_floor_relaxed"] = True
        item["rule_reject_reason"] = ""


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase Rule Filter + Scoring for RSS-Brew Scoring V2")
    ap.add_argument("--input", required=True, help="new-articles.json")
    ap.add_argument("--output", required=True, help="rule-filtered-articles.json")
    ap.add_argument("--floor-count", type=int, default=12, help="Minimum pass count before relaxing selected hard-filters")
    ap.add_argument(
        "--allow-floor-relax-promo-cta",
        action="store_true",
        help="Allow floor fallback to relax promo_cta rejects (disabled by default for safety)",
    )
    args = ap.parse_args()

    payload = load_json(Path(args.input), {})
    articles = payload.get("articles", []) or []

    seen_titles: set[str] = set()
    scored_items = [_score_article(dict(article), seen_titles) for article in articles]
    _apply_floor_fallback(
        scored_items,
        max(0, int(args.floor_count)),
        allow_promo_cta=bool(args.allow_floor_relax_promo_cta),
    )

    passed = [a for a in scored_items if not a.get("rule_reject")]
    rejected = [a for a in scored_items if a.get("rule_reject")]

    out_payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "article_count": len(passed),
        "input_article_count": len(scored_items),
        "rejected_count": len(rejected),
        "floor_count": int(args.floor_count),
        "floor_relaxed_count": sum(1 for a in scored_items if a.get("rule_floor_relaxed")),
        "articles": passed,
        # Keep visibility for debugging/calibration; downstream readers can ignore.
        "rejected_articles": [
            {
                "title": a.get("title", ""),
                "url": a.get("url", ""),
                "rule_reject_reason": a.get("rule_reject_reason", ""),
                "rule_score": int(a.get("rule_score", 0)),
                "rule_minus_tags": a.get("rule_minus_tags", []),
            }
            for a in rejected
        ],
    }

    write_json(Path(args.output), out_payload)
    print(
        json.dumps(
            {
                "phase": "rule_filter",
                "input": len(scored_items),
                "passed": len(passed),
                "rejected": len(rejected),
                "floor_relaxed": out_payload["floor_relaxed_count"],
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
