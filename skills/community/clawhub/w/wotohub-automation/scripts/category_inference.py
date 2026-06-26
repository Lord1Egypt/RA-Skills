#!/usr/bin/env python3
from __future__ import annotations
from typing import Optional, Union

import json
import re
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATEGORY_JSON = ROOT / "references" / "category-source.json"
ALIASES_JSON = ROOT / "references" / "semantic-category-aliases.json"


def _tokenize(value: str) -> set[str]:
    normalized = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", " ", str(value or "").lower())
    return {tok for tok in normalized.split() if tok}


GENERIC_TOKENS = {
    "electric", "electrical", "smart", "portable", "wireless", "digital", "kit", "set",
    "gear", "equipment", "accessory", "accessories", "tool", "tools", "review", "reviews",
    "video", "creator", "influencer", "content", "product", "products", "brand", "comparison",
    "full", "test", "ride", "riding", "minute", "minutes", "performance", "battery", "top",
    "speed", "adult", "adults", "teen", "teens",
}

SEMANTIC_EQUIVALENTS = {
    "bike": {"bike", "bicycle", "cycling", "motorcycle", "ebike"},
    "bicycle": {"bike", "bicycle", "cycling", "ebike"},
    "cycling": {"bike", "bicycle", "cycling", "ebike"},
    "ebike": {"bike", "bicycle", "cycling", "ebike", "electric"},
    "motor": {"motor", "motorcycle", "engine"},
    "motorcycle": {"motor", "motorcycle", "bike"},
    "offroad": {"offroad", "outdoor", "sports"},
    "outdoor": {"offroad", "outdoor", "sports"},
    "sports": {"sports", "outdoor", "offroad"},
    "technology": {"technology", "tech", "electric"},
    "software": {"software", "saas", "app", "tool", "platform", "productivity", "automation"},
    "app": {"app", "software", "mobile", "tool", "productivity"},
    "ai": {"ai", "artificial", "intelligence", "automation", "software", "tool"},
}

ROOT_PRIORITY_HINTS = {
    "07": {"beauty", "cosmetics", "makeup", "skincare"},
    "08": {"care", "oral", "tooth", "toothbrush", "mouth", "hair", "grooming", "cleanser"},
    "09": {"electronics", "electronic", "tech", "device", "smartphone", "computer", "camera", "audio"},
    "10": {"tool", "tools", "hardware", "electrical", "welding", "instrument"},
    "11": {"home", "kitchen", "household", "appliance", "cleaning", "storage", "furniture"},
    "12": {"pet", "pets", "dog", "cat", "animal"},
    "13": {"baby", "maternal", "maternity", "infant", "diaper"},
    "14": {"toy", "toys", "educational", "doll", "blocks", "remote"},
    "15": {"outdoor", "sports", "cycling", "bike", "bicycle", "ebike", "running", "fitness", "fishing"},
    "16": {"automotive", "auto", "car", "motorcycle", "motor", "vehicle", "riding", "helmet"},
    "17": {"technology", "tech", "ai", "app", "software", "crypto", "nft"},
}


def _meaningful_tokens(value: str) -> set[str]:
    return {tok for tok in _tokenize(value) if tok and tok not in GENERIC_TOKENS and len(tok) >= 2}


def _semantic_overlap(query_tokens: set[str], candidate_tokens: set[str]) -> set[str]:
    overlap = set(query_tokens & candidate_tokens)
    for q in query_tokens:
        equivalents = SEMANTIC_EQUIVALENTS.get(q, {q})
        if equivalents & candidate_tokens:
            overlap.add(q)
    return overlap


def _level_weight(level: Optional[Union[str, int]]) -> float:
    level_s = str(level or "")
    if level_s == "3":
        return 1.25
    if level_s == "2":
        return 1.1
    if level_s == "1":
        return 1.0
    return 1.0


def _node_path_text(item: dict, by_code: dict[str, dict]) -> str:
    parts = []
    current = item
    seen = set()
    while isinstance(current, dict):
        code = str(current.get("dictCode") or "")
        if code in seen:
            break
        seen.add(code)
        parts.extend([str(current.get("dictValue") or ""), str(current.get("extAttrs") or "")])
        parent = str(current.get("col3") or current.get("col1") or "0")
        if not parent or parent == "0":
            break
        current = by_code.get(parent)
    return " ".join(parts)


def _expand_with_parents(code: str, by_code: dict[str, dict]) -> list[str]:
    out = []
    current = by_code.get(str(code))
    seen = set()
    while isinstance(current, dict):
        cur_code = str(current.get("dictCode") or "")
        if not cur_code or cur_code in seen:
            break
        seen.add(cur_code)
        out.append(cur_code)
        parent = str(current.get("col3") or current.get("col1") or "0")
        if not parent or parent == "0":
            break
        current = by_code.get(parent)
    return list(reversed(out))


def _root_code(code: str) -> str:
    return str(code or "")[:2]


def _root_priority_score(query_tokens: set[str], code: str) -> float:
    root = _root_code(code)
    hints = ROOT_PRIORITY_HINTS.get(root, set())
    if not hints:
        return 0.0
    overlap = _semantic_overlap(query_tokens, hints)
    return float(len(overlap))


@lru_cache(maxsize=1)
def load_categories():
    data = json.loads(CATEGORY_JSON.read_text()) if CATEGORY_JSON.exists() else []
    by_code = {str(x.get("dictCode")): x for x in data if isinstance(x, dict) and x.get("dictCode")}
    children: dict[str, list[dict]] = {}
    category_index: dict[str, list[str]] = {}
    for item in data:
        if not isinstance(item, dict):
            continue
        code = str(item.get("dictCode") or "")
        parent = str(item.get("col3") or "0")
        children.setdefault(parent, []).append(item)
        for field in ("dictValue", "extAttrs"):
            value = str(item.get(field) or "").strip()
            if value:
                category_index.setdefault(value.lower(), []).append(code)
    return data, by_code, children, category_index


@lru_cache(maxsize=1)
def load_semantic_category_aliases() -> dict[str, list[str]]:
    if not ALIASES_JSON.exists():
        return {}
    raw = json.loads(ALIASES_JSON.read_text())
    return raw if isinstance(raw, dict) else {}


def build_category_ids(query: str, data: list[dict], by_code: dict, category_index: dict) -> tuple[list[str], list[dict]]:
    query_tokens = _meaningful_tokens(query)
    if not query_tokens:
        query_tokens = _tokenize(query)

    scored: list[tuple[float, dict]] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        combined = _node_path_text(item, by_code)
        tokens = _meaningful_tokens(combined)
        if not tokens:
            tokens = _tokenize(combined)
        overlap = _semantic_overlap(query_tokens, tokens)
        if not overlap:
            continue
        precision = len(overlap) / max(len(tokens), 1)
        recall = len(overlap) / max(len(query_tokens), 1)
        root_bonus = _root_priority_score(query_tokens, str(item.get("dictCode") or ""))
        score = (len(overlap) * 3.0 + precision * 2.5 + recall * 1.5 + root_bonus * 2.0) * _level_weight(item.get("col2"))
        if len(overlap) == 1 and precision < 0.34 and recall < 0.34:
            continue
        scored.append((score, item))

    scored.sort(key=lambda x: (x[0], _level_weight(x[1].get("col2"))), reverse=True)
    matched = [item for score, item in scored[:8] if score > 0]

    stable_matches = []
    for score, item in scored:
        combined = _node_path_text(item, by_code)
        tokens = _meaningful_tokens(combined) or _tokenize(combined)
        overlap = _semantic_overlap(query_tokens, tokens)
        precision = len(overlap) / max(len(tokens), 1)
        recall = len(overlap) / max(len(query_tokens), 1)
        level = str(item.get("col2") or "")
        if level == "3" and len(overlap) >= 2 and precision >= 0.34:
            stable_matches.append(item)
        elif level == "2" and len(overlap) >= 1 and precision >= 0.25:
            stable_matches.append(item)
        elif level == "1" and len(overlap) >= 1 and precision >= 0.2 and recall >= 0.2:
            stable_matches.append(item)

    matched = stable_matches[:6] if stable_matches else matched[:6]

    selected_leaf_codes = []
    seen = set()
    for item in matched:
        code = str(item.get("dictCode") or "")
        if code and code not in seen:
            seen.add(code)
            selected_leaf_codes.append(code)
        if len(selected_leaf_codes) >= 3:
            break

    # If we only have weak / adjacent matches, prefer stable upper-level classes
    # instead of forcing noisy leaf nodes.
    if matched:
        root_buckets: dict[str, list[tuple[float, str, list[str]]]] = {}
        for item in matched:
            code = str(item.get("dictCode") or "")
            chain = _expand_with_parents(code, by_code)
            if not chain:
                continue
            combined = _node_path_text(item, by_code)
            tokens = _meaningful_tokens(combined) or _tokenize(combined)
            overlap = _semantic_overlap(query_tokens, tokens)
            precision = len(overlap) / max(len(tokens), 1)
            recall = len(overlap) / max(len(query_tokens), 1)
            root = _root_code(code)
            bucket_score = len(overlap) * 3.0 + precision * 2.5 + recall * 1.5 + _root_priority_score(query_tokens, code) * 2.0
            preferred = chain[1] if len(chain) >= 2 else chain[0]
            root_buckets.setdefault(root, []).append((bucket_score, preferred, chain))

        stable_top_codes = []
        for root, items in sorted(root_buckets.items(), key=lambda kv: max(x[0] for x in kv[1]), reverse=True):
            items.sort(key=lambda x: x[0], reverse=True)
            best_score, preferred, chain = items[0]
            if best_score <= 0:
                continue
            if preferred not in stable_top_codes:
                stable_top_codes.append(preferred)
            # also keep root if different and there is room
            root_code = chain[0]
            if root_code not in stable_top_codes and len(stable_top_codes) < 3:
                stable_top_codes.append(root_code)
            if len(stable_top_codes) >= 3:
                break

        if stable_top_codes:
            selected_leaf_codes = stable_top_codes[:3]

    expanded_codes = []
    expanded_seen = set()
    for code in selected_leaf_codes:
        for ancestor_code in _expand_with_parents(code, by_code):
            if ancestor_code not in expanded_seen:
                expanded_seen.add(ancestor_code)
                expanded_codes.append(ancestor_code)

    return expanded_codes[:9], matched[:6]


def map_semantic_labels_to_category_ids(semantic: Optional[dict], data: list[dict], by_code: dict, category_index: dict) -> tuple[list[str], list[dict]]:
    resolution = map_semantic_labels_with_scores(semantic, data, by_code, category_index)
    return resolution.get("selectedBlogCateIds", []), resolution.get("matchedCategories", [])


def map_semantic_labels_with_scores(semantic: Optional[dict], data: list[dict], by_code: dict, category_index: dict) -> dict:
    if not semantic:
        return {
            "candidateCategoryLabels": [],
            "matchedCategories": [],
            "selectedBlogCateIds": [],
            "confidenceLevel": "low",
            "mustApplyBlogCateIds": False,
            "strategy": "keyword_only",
            "mappingWarnings": ["semantic input missing"],
        }

    semantic_brief = (semantic.get("semanticBrief") or {}) if isinstance(semantic, dict) else {}
    product = semantic_brief.get("product") or {}
    keyword_clusters = semantic_brief.get("keyword_clusters") or {}
    marketing = semantic_brief.get("marketing") or {}
    alias_map = load_semantic_category_aliases()

    labels = []
    labels.extend((product.get("category_forms") or {}).get("value") or [])
    labels.extend((product.get("functions") or {}).get("value") or [])
    labels.extend((keyword_clusters.get("core") or {}).get("value") or [])
    labels.extend((keyword_clusters.get("benefit") or {}).get("value") or [])
    labels.extend((keyword_clusters.get("creator") or {}).get("value") or [])
    labels.extend((marketing.get("creator_types") or {}).get("value") or [])

    expanded_labels: list[str] = []
    for label in labels:
        clean = str(label or "").strip()
        if not clean:
            continue
        expanded_labels.append(clean)
        expanded_labels.extend(alias_map.get(clean.lower(), []))

    query = " ".join(dict.fromkeys(expanded_labels))
    selected, matched = build_category_ids(query, data, by_code, category_index)
    confidence = "high" if len(selected) >= 2 else ("medium" if len(selected) == 1 else "low")
    if confidence == "high":
        strategy = "category_plus_keyword"
    elif confidence == "medium":
        strategy = "broad_category_plus_keyword"
    else:
        root_candidates = []
        seen_roots = set()
        for item in matched:
            code = str(item.get("dictCode") or "")
            root = code[:2]
            if len(root) == 2 and root not in seen_roots:
                seen_roots.add(root)
                root_candidates.append(root)
        if root_candidates:
            selected = root_candidates[:2]
            confidence = "medium"
            strategy = "broad_category_plus_keyword"
        else:
            strategy = "keyword_only"
            selected = []

    formatted = []
    for item in matched:
        formatted.append({
            "label": item.get("dictValue") or item.get("extAttrs"),
            "blogCateId": item.get("dictCode"),
            "displayName": item.get("dictValue"),
            "displayNameEn": item.get("extAttrs"),
            "level": item.get("col2"),
            "score": 1,
            "source": "semantic_alias_match",
        })

    return {
        "candidateCategoryLabels": list(dict.fromkeys(expanded_labels))[:6],
        "matchedCategories": formatted[:10],
        "selectedBlogCateIds": selected[:4],
        "confidenceLevel": confidence,
        "mustApplyBlogCateIds": bool(selected),
        "strategy": strategy,
        "mappingWarnings": [] if selected else ["no stable category mapping found from semantic labels"],
    }
