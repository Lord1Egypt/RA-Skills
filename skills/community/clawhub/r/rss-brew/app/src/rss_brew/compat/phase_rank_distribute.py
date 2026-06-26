#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from shared_utils import load_json, parse_dt, write_json


def _to_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default


def _normalized_topic(article: Dict[str, Any]) -> Optional[str]:
    """Placeholder hook for future topic normalization.

    Scheme 3 defers hard topic caps until a stable normalized topic key exists.
    For now, we only honor an explicit normalized topic field when present.
    """
    for key in ("normalized_topic", "topic_key", "topic"):
        val = article.get(key)
        if isinstance(val, str):
            topic = val.strip().lower()
            if topic:
                return topic
    return None


def _is_low_conf(article: Dict[str, Any], threshold: float) -> bool:
    return _to_float(article.get("confidence"), 0.5) < threshold


def _ranked(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    enriched: List[Dict[str, Any]] = []
    for a in items:
        b = dict(a)
        b["rule_score"] = int(_to_float(b.get("rule_score"), 0.0))
        b["model_score"] = _to_float(b.get("model_score"), 0.0)
        b["final_score"] = float(b["rule_score"]) + float(b["model_score"])
        enriched.append(b)

    enriched.sort(
        key=lambda x: (
            x.get("final_score", 0.0),
            int(_to_float(x.get("score"), 0.0)),
            int(_to_float(x.get("rule_score"), 0.0)),
            parse_dt(str(x.get("published") or "")),
            str(x.get("url") or ""),
            str(x.get("title") or ""),
        ),
        reverse=True,
    )

    for i, item in enumerate(enriched, start=1):
        item["rank"] = i
    return enriched


def _select_deep(
    ranked: List[Dict[str, Any]],
    target: int,
    min_other: int,
    source_cap: int,
    topic_cap: int,
    enforce_topic_cap: bool,
    top3_low_conf_block: bool,
    low_conf_threshold: float,
) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    if not ranked or target <= 0:
        return [], {"blocked_low_conf_top3": 0, "blocked_source_cap": 0, "blocked_topic_cap": 0}

    allowed_deep = min(target, max(1, len(ranked) - max(0, min_other)))
    selected: List[Dict[str, Any]] = []
    source_used: Dict[str, int] = {}
    topic_used: Dict[str, int] = {}
    blocked = {"blocked_low_conf_top3": 0, "blocked_source_cap": 0, "blocked_topic_cap": 0}

    # First pass: enforce top-3 low-confidence block plus caps.
    for item in ranked:
        if len(selected) >= allowed_deep:
            break

        source = str(item.get("source") or "").strip().lower() or "unknown"
        topic = _normalized_topic(item)

        if source_used.get(source, 0) >= max(1, source_cap):
            blocked["blocked_source_cap"] += 1
            continue
        if enforce_topic_cap and topic is not None and topic_used.get(topic, 0) >= max(1, topic_cap):
            blocked["blocked_topic_cap"] += 1
            continue

        if top3_low_conf_block and len(selected) < 3 and _is_low_conf(item, low_conf_threshold):
            blocked["blocked_low_conf_top3"] += 1
            continue

        selected.append(item)
        source_used[source] = source_used.get(source, 0) + 1
        if topic is not None:
            topic_used[topic] = topic_used.get(topic, 0) + 1

    # Second pass: fill remaining slots while respecting caps.
    # Keep top-3 low-confidence blocking semantics consistent until first 3 deep slots are filled.
    if len(selected) < allowed_deep:
        selected_urls = {str(x.get("url") or "") for x in selected}
        for item in ranked:
            if len(selected) >= allowed_deep:
                break
            url = str(item.get("url") or "")
            if url in selected_urls:
                continue

            source = str(item.get("source") or "").strip().lower() or "unknown"
            topic = _normalized_topic(item)
            if source_used.get(source, 0) >= max(1, source_cap):
                continue
            if enforce_topic_cap and topic is not None and topic_used.get(topic, 0) >= max(1, topic_cap):
                continue
            if top3_low_conf_block and len(selected) < 3 and _is_low_conf(item, low_conf_threshold):
                blocked["blocked_low_conf_top3"] += 1
                continue

            selected.append(item)
            selected_urls.add(url)
            source_used[source] = source_used.get(source, 0) + 1
            if topic is not None:
                topic_used[topic] = topic_used.get(topic, 0) + 1

    return selected, blocked


def _select_other(
    ranked: List[Dict[str, Any]],
    deep: List[Dict[str, Any]],
    target: int,
    source_cap: int,
) -> List[Dict[str, Any]]:
    deep_urls = {str(x.get("url") or "") for x in deep}
    source_used: Dict[str, int] = {}
    out: List[Dict[str, Any]] = []

    for item in ranked:
        if len(out) >= max(0, target):
            break
        if str(item.get("url") or "") in deep_urls:
            continue

        source = str(item.get("source") or "").strip().lower() or "unknown"
        if source_used.get(source, 0) >= max(1, source_cap):
            continue
        out.append(item)
        source_used[source] = source_used.get(source, 0) + 1

    return out


def _payload_from(items: List[Dict[str, Any]], model: str, generated_at: str) -> Dict[str, Any]:
    return {
        "generated_at": generated_at,
        "model": model,
        "article_count": len(items),
        "articles": items,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Phase D rank+distribute for RSS-Brew Scoring V2")
    ap.add_argument("--input", required=True, help="model-scored-articles.json")
    ap.add_argument("--ranked-output", required=True, help="ranked-articles.json")
    ap.add_argument("--distribution-output", required=True, help="distribution.json")
    ap.add_argument("--deep-output", required=True, help="deep-set.json")
    ap.add_argument("--other-output", required=True, help="other-set.json")
    ap.add_argument("--compat-scored-output", default="", help="Optional scored-articles.json compatibility output")
    ap.add_argument("--deep-target", type=int, default=5)
    ap.add_argument("--other-target", type=int, default=12)
    ap.add_argument("--min-other", type=int, default=5)
    ap.add_argument("--source-cap", type=int, default=3)
    ap.add_argument("--deep-topic-cap", type=int, default=2)
    ap.add_argument(
        "--enforce-deep-topic-cap",
        action="store_true",
        help=(
            "Enforce deep topic cap using normalized topic keys only. "
            "Default is disabled until topic normalization is production-ready."
        ),
    )
    ap.add_argument("--low-confidence-threshold", type=float, default=0.4)
    ap.add_argument("--disable-top3-low-confidence-block", action="store_true")
    args = ap.parse_args()

    payload = load_json(Path(args.input), {})
    model = str(payload.get("model") or "CHEAP")
    generated_at = datetime.now(timezone.utc).isoformat()
    items = payload.get("articles", []) or []

    ranked = _ranked([dict(x) for x in items])
    deep, blocked = _select_deep(
        ranked,
        target=max(0, int(args.deep_target)),
        min_other=max(0, int(args.min_other)),
        source_cap=max(1, int(args.source_cap)),
        topic_cap=max(1, int(args.deep_topic_cap)),
        enforce_topic_cap=bool(args.enforce_deep_topic_cap),
        top3_low_conf_block=not bool(args.disable_top3_low_confidence_block),
        low_conf_threshold=float(args.low_confidence_threshold),
    )
    other = _select_other(ranked, deep, target=max(0, int(args.other_target)), source_cap=max(1, int(args.source_cap)))

    ranked_payload = _payload_from(ranked, model=model, generated_at=generated_at)
    deep_payload = _payload_from(deep, model=model, generated_at=generated_at)
    other_payload = _payload_from(other, model=model, generated_at=generated_at)

    distribution_payload = {
        "generated_at": generated_at,
        "input_article_count": len(items),
        "ranked_count": len(ranked),
        "deep_set_count": len(deep),
        "other_set_count": len(other),
        "deep_target": int(args.deep_target),
        "other_target": int(args.other_target),
        "min_other": int(args.min_other),
        "source_cap": int(args.source_cap),
        "deep_topic_cap": int(args.deep_topic_cap),
        "deep_topic_cap_enforced": bool(args.enforce_deep_topic_cap),
        "top3_low_confidence_block": not bool(args.disable_top3_low_confidence_block),
        "low_confidence_threshold": float(args.low_confidence_threshold),
        "guardrail_stats": blocked,
    }

    write_json(Path(args.ranked_output), ranked_payload)
    write_json(Path(args.distribution_output), distribution_payload)
    write_json(Path(args.deep_output), deep_payload)
    write_json(Path(args.other_output), other_payload)

    compat_out = (args.compat_scored_output or "").strip()
    if compat_out:
        # Compatibility contract: preserve scored-articles shape while adding final/rank fields.
        write_json(Path(compat_out), ranked_payload)

    print(
        {
            "phase": "rank_distribute",
            "input": len(items),
            "ranked": len(ranked),
            "deep": len(deep),
            "other": len(other),
        }
    )


if __name__ == "__main__":
    main()
