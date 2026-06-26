#!/usr/bin/env python3
import json
import re
import sys
from typing import Any, Dict, List
from urllib.parse import urlparse


def read_stdin_json() -> Dict[str, Any]:
    raw = sys.stdin.read().strip()
    if not raw:
        raise ValueError("No JSON input provided on stdin")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON input: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError("Top-level JSON input must be an object")
    return data


def write_json(data: Dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(data, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")


def write_error(message: str) -> None:
    write_json({"error": message})


def make_candidate_id(index: int) -> str:
    return f"c{index + 1}"


def clean_text(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return re.sub(r"\s+", " ", value).strip()


def merge_notes(*values: Any) -> str | None:
    parts = []
    seen = set()
    for value in values:
        text = clean_text(value)
        if text and text not in seen:
            parts.append(text)
            seen.add(text)
    return " | ".join(parts) if parts else None


def infer_source_from_url(url: str | None) -> str | None:
    if not url:
        return None
    host = urlparse(url).netloc.lower()
    if "jd.com" in host:
        return "jd"
    if "tmall.com" in host:
        return "tmall"
    if "taobao.com" in host:
        return "taobao"
    if "pinduoduo.com" in host or "yangkeduo.com" in host or "pdd" in host:
        return "pdd"
    return "other" if host else None


def infer_decision_mode(items: List[Dict[str, Any]], text: str | None = None) -> str:
    normalized = clean_text(text).lower()
    if normalized:
        if any(token in normalized for token in ["值不值", "能买吗", "值得买吗", "worth it"]):
            return "single_judgement"
        if any(token in normalized for token in ["对比", "哪个好", "选哪个", "compare"]):
            return "compare"
        if any(token in normalized for token in ["想买", "求推荐", "买什么", "recommend"]):
            return "need_driven"
    if len(items) >= 2:
        return "compare"
    if len(items) == 1:
        return "single_judgement"
    return "need_driven"


def extract_title(item: Dict[str, Any], index: int) -> tuple[str, bool]:
    explicit = clean_text(item.get("title"))
    if explicit:
        return explicit, False

    raw_text = clean_text(item.get("raw_text"))
    if raw_text:
        return raw_text[:80], False

    url = clean_text(item.get("url"))
    if url:
        host = urlparse(url).netloc or url
        return host[:80], True

    return f"Candidate {index + 1}", True


def extract_price_value(item: Dict[str, Any]) -> tuple[float | None, str]:
    for key in ["price_hint", "final_price", "price", "amount"]:
        value = item.get(key)
        if isinstance(value, (int, float)):
            return float(value), "estimated" if key == "price_hint" else "discounted"
        if isinstance(value, str):
            text = clean_text(value).replace("¥", "")
            try:
                return float(text), "estimated" if key == "price_hint" else "discounted"
            except ValueError:
                pass

    text = merge_notes(item.get("raw_text"), item.get("title")) or ""
    match = re.search(r"(?:¥|￥)?\s*(\d{2,6}(?:\.\d{1,2})?)", text)
    if match:
        return float(match.group(1)), "estimated"

    return None, "unknown"


def get_final_price(item: Dict[str, Any]) -> Dict[str, Any] | None:
    value, label = extract_price_value(item)
    if value is None:
        return None
    return {"final_price": value, "currency": clean_text(item.get("currency")) or "CNY", "price_label": label}


def _comparison_tokens(text: str) -> set[str]:
    normalized = clean_text(text).lower()
    if not normalized:
        return set()
    pattern = r"[a-z0-9]+(?:g|gb|tb|寸|mm|ml|w|k)?|标准版|pro|plus|max|ultra|套装|礼盒|单机|裸机|赠品|升级款|升级版|同系列|类似款|相近款"
    return set(re.findall(pattern, normalized))


def classify_comparison(base_text: str, other_text: str) -> Dict[str, Any]:
    base_clean = clean_text(base_text)
    other_clean = clean_text(other_text)
    base_tokens = _comparison_tokens(base_clean)
    other_tokens = _comparison_tokens(other_clean)
    reason_tags: list[str] = []

    spec_pairs = [("128g", "256g"), ("256g", "512g"), ("标准版", "pro"), ("plus", "max")]
    for left, right in spec_pairs:
        if left in base_tokens and right in other_tokens or right in base_tokens and left in other_tokens:
            reason_tags.append("spec_conflict")

    bundle_tokens = {"套装", "礼盒", "赠品", "单机", "裸机"}
    if base_tokens.intersection(bundle_tokens) != other_tokens.intersection(bundle_tokens):
        if base_tokens.intersection(bundle_tokens) or other_tokens.intersection(bundle_tokens):
            reason_tags.append("bundle_conflict")

    uncertainty_tokens = {"升级款", "升级版", "同系列", "类似款", "相近款"}
    if any(token in base_clean or token in other_clean for token in uncertainty_tokens):
        relation = "similar_item"
        reason_tags.append("weak_match")
    elif reason_tags:
        relation = "not_directly_comparable"
    else:
        overlap = len(base_tokens.intersection(other_tokens))
        relation = "same_item" if overlap >= 2 else "similar_item"
        if relation == "similar_item":
            reason_tags.append("weak_match")

    if reason_tags and "spec_conflict" in reason_tags or "bundle_conflict" in reason_tags:
        relation = "not_directly_comparable"

    return {
        "relation": relation,
        "reason_tags": sorted(set(reason_tags)),
    }
