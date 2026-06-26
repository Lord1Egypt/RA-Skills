#!/usr/bin/env python3
from __future__ import annotations

import re
from typing import Dict, Any

INTENT_PATTERNS = [
    ("official", ["official image", "official", "logo", "emblem", "mascot", "brand mark"]),
    ("meme", ["meme first", "meme", "reaction image", "funny image", "emoji"]),
    ("avatar", ["avatar", "profile picture", "icon"]),
    ("wallpaper", ["hd wallpaper", "wallpaper", "4k", "hd", "high resolution"]),
]
ORIENTATION_PATTERNS = {
    "horizontal": ["landscape", "horizontal"],
    "vertical": ["portrait", "vertical"],
}


def parse_count(text: str) -> int | None:
    m = re.search(r"\b([1-5])\s*(?:images?|pics?)\b", text, re.I)
    if m:
        return max(1, min(5, int(m.group(1))))
    return None


def parse_query_params(text: str) -> Dict[str, Any]:
    raw = text.strip()
    parsed: Dict[str, Any] = {
        "raw": raw,
        "core_query": raw,
        "count": None,
        "intent_override": None,
        "orientation": None,
        "high_res": False,
        "removed_tokens": [],
    }

    count = parse_count(raw)
    if count:
        parsed["count"] = count
        new = re.sub(rf"\b{count}\s*(?:images?|pics?)\b", " ", parsed["core_query"], count=1, flags=re.I)
        if new != parsed["core_query"]:
            parsed["removed_tokens"].append(f"{count} images")
            parsed["core_query"] = new

    for intent, kws in INTENT_PATTERNS:
        for kw in kws:
            if kw.lower() in parsed["core_query"].lower():
                parsed["intent_override"] = intent
                parsed["core_query"] = re.sub(re.escape(kw), " ", parsed["core_query"], flags=re.I)
                parsed["removed_tokens"].append(kw)
                break
        if parsed["intent_override"]:
            break

    for orient, kws in ORIENTATION_PATTERNS.items():
        for kw in kws:
            if kw.lower() in parsed["core_query"].lower():
                parsed["orientation"] = orient
                parsed["core_query"] = re.sub(re.escape(kw), " ", parsed["core_query"], flags=re.I)
                parsed["removed_tokens"].append(kw)
                break
        if parsed["orientation"]:
            break

    for kw in ["hd", "4k", "high resolution", "ultra hd"]:
        if kw.lower() in parsed["core_query"].lower():
            parsed["high_res"] = True
            parsed["core_query"] = re.sub(re.escape(kw), " ", parsed["core_query"], flags=re.I)
            parsed["removed_tokens"].append(kw)

    parsed["core_query"] = re.sub(r"\s+", " ", parsed["core_query"]).strip()
    if not parsed["core_query"]:
        parsed["core_query"] = raw
    return parsed


if __name__ == "__main__":
    import json, sys
    q = " ".join(sys.argv[1:]).strip()
    print(json.dumps(parse_query_params(q), ensure_ascii=False, indent=2))
