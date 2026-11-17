#!/usr/bin/env python3
"""Convert judgment JSON into renderable card JSON."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


MODULE_META = {
    "work_charm": ("今日工作签", "sign-strip", "09:30", "保命"),
    "lunch_oracle": ("午饭判官", "lunch-receipt", "12:00", "重判"),
    "mood_weather": ("精神天气台", "mood-notice", "15:00", "只给动作"),
    "afterwork_pass": ("下班放行单", "afterwork-pass", "18:30", "放行"),
}
REQUIRED = ["module", "title", "verdict", "reason", "action", "backup", "follow_up", "share_safe"]
TEXT_LIMITS = {
    "time_label": 10,
    "title": 18,
    "reason": 40,
    "action": 40,
    "corner": 10,
    "footer": 16,
    "alt_text": 120,
}
RATIOS = {"9:16", "3:4"}


def load_json(path: str) -> dict[str, Any]:
    raw = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("input must be a JSON object")
    if isinstance(payload.get("judgment"), dict):
        payload = payload["judgment"]
    return payload


def clipped(text: Any, limit: int) -> str:
    value = "" if text is None else str(text).strip()
    return value[:limit]


def split_entry(text: Any) -> list[str]:
    if not isinstance(text, str) or not text.strip():
        return []
    parts = [part.strip() for part in text.replace("｜", "/").split("/")]
    return [part[:8] for part in parts if part][:3]


def validate_judgment(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing field: {key}")
    if data.get("module") not in MODULE_META:
        errors.append("module unsupported")
    for key in ["title", "verdict", "reason", "action"]:
        if not isinstance(data.get(key), str) or not data.get(key, "").strip():
            errors.append(f"{key} must be non-empty text")
    if data.get("share_safe") is not True:
        errors.append("share_safe must be true for renderable card")
    return errors


def convert_judgment(data: dict[str, Any], ratio: str = "9:16") -> dict[str, Any]:
    errors = validate_judgment(data)
    if errors:
        raise ValueError("; ".join(errors))
    if ratio not in RATIOS:
        raise ValueError("ratio must be 9:16 or 3:4")
    module_label, route, default_time, default_corner = MODULE_META[str(data["module"])]
    tags = split_entry(data.get("backup")) + split_entry(data.get("follow_up"))
    if not tags:
        tags = [module_label[:4]]
    card = {
        "module": module_label,
        "route": route,
        "time_label": clipped(data.get("time_label", default_time), TEXT_LIMITS["time_label"]),
        "title": clipped(data["title"], TEXT_LIMITS["title"]),
        "reason": clipped(data["reason"], TEXT_LIMITS["reason"]),
        "action": clipped(data["action"], TEXT_LIMITS["action"]),
        "tags": tags[:4],
        "corner": clipped(split_entry(data.get("follow_up"))[0] if split_entry(data.get("follow_up")) else default_corner, TEXT_LIMITS["corner"]),
        "footer": "今天先这么过。",
        "alt_text": clipped(f"{module_label}。{data['title']}。依据：{data['reason']}。现在做：{data['action']}。", TEXT_LIMITS["alt_text"]),
        "ratio": ratio,
        "share_safe": True,
    }
    return card


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert judgment JSON into Workday Companion card JSON.")
    parser.add_argument("input", help="Path to judgment JSON, or - for stdin.")
    parser.add_argument("--out", help="Output path. Defaults to stdout.")
    parser.add_argument("--ratio", choices=sorted(RATIOS), default="9:16", help="Output card ratio.")
    args = parser.parse_args()
    try:
        card = convert_judgment(load_json(args.input), ratio=args.ratio)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc)) from exc
    text = json.dumps(card, ensure_ascii=False, indent=2) + "\n"
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
