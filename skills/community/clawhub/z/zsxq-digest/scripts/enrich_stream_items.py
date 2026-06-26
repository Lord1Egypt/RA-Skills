#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

DEFAULT_WEIGHT_OVERRIDES = {
    "睡前消息的编辑们": {
        "comments_multiplier": 3.0,
        "likes_multiplier": 1.5,
    }
}


def load_json(path: Path, default: Any = None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def load_items(path: Path) -> Tuple[List[dict], dict]:
    data = load_json(path, [])
    meta = {}
    if isinstance(data, dict):
        meta = {k: v for k, v in data.items() if k != "items"}
        data = data.get("items", [])
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list or an object with an 'items' array")
    return [item for item in data if isinstance(item, dict)], meta


def write_output(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def coerce_int(value: Any) -> int:
    if value in (None, "", False):
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    text = str(value).strip().replace(",", "")
    digits = ""
    for ch in text:
        if ch.isdigit() or (ch == "-" and not digits):
            digits += ch
        elif digits:
            break
    try:
        return int(digits) if digits else 0
    except Exception:
        return 0


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return "\n".join(line.rstrip() for line in text.splitlines()).strip()


def truncate_text(text: str, max_chars: int) -> Tuple[str, bool]:
    text = clean_text(text)
    if max_chars <= 0 or len(text) <= max_chars:
        return text, False
    candidate = text[:max_chars].rstrip()
    split_at = max(candidate.rfind("\n\n"), candidate.rfind("。"), candidate.rfind("！"), candidate.rfind("？"))
    if split_at >= max_chars // 2:
        candidate = candidate[: split_at + 1].rstrip()
    return candidate, True


def merge_overrides(user_overrides: dict) -> dict:
    merged = json.loads(json.dumps(DEFAULT_WEIGHT_OVERRIDES, ensure_ascii=False))
    for circle, cfg in (user_overrides or {}).items():
        if not isinstance(cfg, dict):
            continue
        target = merged.setdefault(circle, {})
        target.update(cfg)
    return merged


def load_overrides(path: str) -> dict:
    if not path:
        return DEFAULT_WEIGHT_OVERRIDES
    data = load_json(Path(path), {})
    if not isinstance(data, dict):
        raise ValueError("weight overrides file must be a JSON object")
    return merge_overrides(data)


def engagement(item: dict) -> Tuple[int, int]:
    hint = item.get("engagement_hint") if isinstance(item.get("engagement_hint"), dict) else {}
    likes = coerce_int(item.get("likes", hint.get("likes")))
    comments = coerce_int(item.get("comments", hint.get("comments")))
    return likes, comments


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value in (None, "", 0, "0", "false", "False", "no", "No"):
        return False
    return bool(value)


def detect_has_links(item: dict, text: str) -> bool:
    if boolish(item.get("has_links")):
        return True
    if item.get("url"):
        return True
    return "http://" in text or "https://" in text


def detect_has_images(item: dict) -> bool:
    if boolish(item.get("has_images")):
        return True
    images = item.get("images")
    if isinstance(images, list) and images:
        return True
    return coerce_int(item.get("image_count")) > 0


def ladder_points(value: float, steps: List[Tuple[float, int]]) -> int:
    for threshold, points in steps:
        if value > threshold:
            return points
    return 0


def weak_content_penalty(item: dict, excerpt: str) -> int:
    title = clean_text(item.get("title_or_hook") or item.get("title") or "")
    if len(excerpt) < 40 and len(title) < 18:
        return -8
    if item.get("guessed_type") == "chat" and len(excerpt) < 80:
        return -6
    if item.get("has_links") and len(excerpt) < 40:
        return -8
    return 0


def enrich_item(item: dict, max_chars: int, overrides: dict) -> dict:
    enriched = dict(item)
    circle_name = clean_text(item.get("circle_name") or "未分类星球") or "未分类星球"
    raw_excerpt = clean_text(item.get("detail_excerpt") or item.get("raw_text") or item.get("content_preview") or "")
    if not raw_excerpt:
        raw_excerpt = clean_text(item.get("title_or_hook") or item.get("title") or "")
    detail_excerpt, render_truncated = truncate_text(raw_excerpt, max_chars)

    explicit_truncated = boolish(item.get("is_truncated")) or boolish(item.get("detail_truncated"))
    is_truncated = explicit_truncated or render_truncated
    detail_chars = len(detail_excerpt)

    likes, comments = engagement(item)
    circle_override = overrides.get(circle_name, {}) if isinstance(overrides, dict) else {}
    likes_multiplier = float(circle_override.get("likes_multiplier", 1.0) or 1.0)
    comments_multiplier = float(circle_override.get("comments_multiplier", 1.0) or 1.0)
    weighted_likes = likes * likes_multiplier
    weighted_comments = comments * comments_multiplier

    source_mode = clean_text(item.get("source_mode") or item.get("capture_mode") or "unknown") or "unknown"
    source_confidence = clean_text(item.get("source_confidence") or "") or ("high" if detail_chars >= 400 and not is_truncated else "medium" if detail_chars >= 120 else "low")
    guessed_type = clean_text(item.get("guessed_type") or item.get("content_type") or "other") or "other"

    score = 0
    if boolish(item.get("is_elite")):
        score += 30
    if boolish(item.get("is_pinned")):
        score += 20

    if detail_chars >= 500:
        score += 12
    elif detail_chars >= 280:
        score += 8
    elif detail_chars >= 120:
        score += 4

    score += ladder_points(weighted_likes, [(50, 10), (20, 7), (5, 4)])
    score += ladder_points(weighted_comments, [(30, 14), (10, 10), (3, 6)])

    has_links = detect_has_links(item, detail_excerpt)
    has_images = detect_has_images(item)
    if has_links:
        score += 5
    if has_images:
        score += 5

    if source_mode == "token" and source_confidence == "high":
        score += 8
    elif source_mode == "browser" and source_confidence == "medium":
        score += 2
    elif source_mode == "browser" and source_confidence == "low":
        score -= 4

    if guessed_type in ("qa", "analysis", "resource"):
        score += 2

    score += weak_content_penalty({**item, "has_links": has_links, "guessed_type": guessed_type}, detail_excerpt)

    content_preview = clean_text(item.get("content_preview") or detail_excerpt)
    if len(content_preview) > 280:
        content_preview = content_preview[:280].rstrip()

    enriched.update(
        {
            "circle_name": circle_name,
            "title_or_hook": clean_text(item.get("title_or_hook") or item.get("title") or "（无标题）") or "（无标题）",
            "content_preview": content_preview,
            "detail_excerpt": detail_excerpt,
            "detail_excerpt_raw": raw_excerpt,
            "detail_truncated": is_truncated,
            "detail_chars": detail_chars,
            "is_truncated": is_truncated,
            "engagement_hint": {"likes": likes, "comments": comments},
            "guessed_type": guessed_type,
            "source_mode": source_mode,
            "source_confidence": source_confidence,
            "has_links": has_links,
            "has_images": has_images,
            "stream_score": int(score),
            "weight_override": circle_override,
        }
    )
    return enriched


def choose_full_indices(items: List[dict], full_per_circle: int, min_full_score: int) -> set:
    if not items:
        return set()
    full_indices = {0}
    top_score = items[0].get("stream_score", 0)
    for idx, item in enumerate(items[1:full_per_circle], start=1):
        score = item.get("stream_score", 0)
        threshold = max(min_full_score, 1) if idx == 1 else max(min_full_score + 2, 3)
        if score >= threshold and score >= top_score - 12:
            full_indices.add(idx)
    return full_indices


def sort_key(item: dict):
    return (
        -coerce_int(item.get("stream_score")),
        str(item.get("published_at") or ""),
        str(item.get("title_or_hook") or ""),
    )


def main():
    parser = argparse.ArgumentParser(description="Enrich normalized ZSXQ items for stream digest rendering")
    parser.add_argument("input", help="Path to normalized/new items JSON")
    parser.add_argument("--output", help="Optional path to save enriched JSON")
    parser.add_argument("--full-per-circle", type=int, default=3)
    parser.add_argument("--full-max-chars", type=int, default=800)
    parser.add_argument("--min-full-score", type=int, default=0)
    parser.add_argument("--weight-overrides-file")
    args = parser.parse_args()

    items, meta = load_items(Path(args.input))
    overrides = load_overrides(args.weight_overrides_file)

    enriched_items = [enrich_item(item, args.full_max_chars, overrides) for item in items]
    grouped: Dict[str, List[dict]] = defaultdict(list)
    for item in enriched_items:
        grouped[item.get("circle_name") or "未分类星球"].append(item)

    final_items: List[dict] = []
    circles_summary = []
    full_blocks_count = 0
    compact_items_count = 0

    for circle_name in sorted(grouped):
        group_items = sorted(grouped[circle_name], key=sort_key)
        full_indices = choose_full_indices(group_items, max(1, args.full_per_circle), args.min_full_score)
        circle_full = 0
        for idx, item in enumerate(group_items):
            enriched = dict(item)
            if idx in full_indices:
                enriched["summary_mode"] = "full"
                circle_full += 1
                full_blocks_count += 1
            else:
                enriched["summary_mode"] = "compact"
                compact_items_count += 1
            final_items.append(enriched)
        circles_summary.append(
            {
                "circle_name": circle_name,
                "item_count": len(group_items),
                "full_count": circle_full,
                "compact_count": len(group_items) - circle_full,
                "top_score": group_items[0].get("stream_score", 0) if group_items else 0,
            }
        )

    result = {
        "status": "ok",
        "kind": "stream_enriched",
        "count": len(final_items),
        "items": final_items,
        "source_meta": meta,
        "stats": {
            "circles_count": len(grouped),
            "full_blocks_count": full_blocks_count,
            "compact_items_count": compact_items_count,
            "score_scope": "per-circle-only",
            "pipeline_message": f"Pipeline completed: {len(grouped)} circles, {full_blocks_count} full blocks, {compact_items_count} compact items",
            "circles": circles_summary,
        },
    }

    if args.output:
        write_output(Path(args.output), result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
