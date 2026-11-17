#!/usr/bin/env python3
"""Validate Workday Companion card JSON files with stdlib only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


MODULE_ROUTE = {
    "今日工作签": "sign-strip",
    "午饭判官": "lunch-receipt",
    "精神天气台": "mood-notice",
    "下班放行单": "afterwork-pass",
}
ROUTES = tuple(MODULE_ROUTE.values())

REQUIRED = ("module", "route", "time_label", "title", "reason", "action", "footer", "alt_text", "share_safe")
OPTIONAL = ("tags", "corner", "ratio")
PUBLIC_TEXT_FIELDS = ("module", "time_label", "title", "reason", "action", "footer", "corner", "alt_text")
PRIVATE_MARKERS = (
    "公司名",
    "公司名称",
    "具体住址",
    "真实地址",
    "精确定位",
    "同事姓名",
    "会议内容",
    "会议主题",
    "客户姓名",
    "手机号",
    "支付信息",
    "账号信息",
)
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


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}, column {exc.colno}") from exc


def require_text(data: dict[str, Any], key: str, errors: list[str]) -> None:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        errors.append(f"{key} must be non-empty text")
        return
    limit = TEXT_LIMITS[key]
    if len(value) > limit:
        errors.append(f"{key} exceeds {limit} chars")


def validate_tags(value: Any, errors: list[str]) -> None:
    if value is None:
        return
    if not isinstance(value, list):
        errors.append("tags must be a list")
        return
    if len(value) > 4:
        errors.append("tags allows at most 4 items")
    for index, item in enumerate(value, start=1):
        if not isinstance(item, str) or not item:
            errors.append(f"tags[{index}] must be non-empty text")
        elif len(item) > 8:
            errors.append(f"tags[{index}] exceeds 8 chars")


def iter_public_text(data: dict[str, Any]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for field in PUBLIC_TEXT_FIELDS:
        value = data.get(field)
        if isinstance(value, str):
            values.append((field, value))
    tags = data.get("tags", [])
    if isinstance(tags, list):
        for index, tag in enumerate(tags, start=1):
            if isinstance(tag, str):
                values.append((f"tags[{index}]", tag))
    return values


def validate_share_safe_text(data: dict[str, Any], errors: list[str]) -> None:
    if data.get("share_safe") is not True:
        errors.append("share_safe must be true for renderable card")
    for field, value in iter_public_text(data):
        for marker in PRIVATE_MARKERS:
            if marker in value:
                errors.append(f"{field} contains private marker: {marker}")


def validate_card(data: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["card must be a JSON object"]

    allowed = set(REQUIRED) | set(OPTIONAL)
    extra = sorted(set(data) - allowed)
    if extra:
        errors.append(f"unknown fields: {', '.join(extra)}")

    for key in REQUIRED:
        if key not in data:
            errors.append(f"missing required field: {key}")

    for key in ("time_label", "title", "reason", "action", "footer", "alt_text"):
        if key in data:
            require_text(data, key, errors)
    if "corner" in data:
        require_text(data, "corner", errors)

    module = data.get("module")
    route = data.get("route")
    if module not in MODULE_ROUTE:
        errors.append(f"module must be one of: {', '.join(MODULE_ROUTE)}")
    if route not in ROUTES:
        errors.append(f"route must be one of: {', '.join(ROUTES)}")
    if module in MODULE_ROUTE and route in ROUTES:
        expected = MODULE_ROUTE[module]
        if route != expected:
            errors.append(f"route {route} does not match module {module}; expected {expected}")

    validate_tags(data.get("tags"), errors)

    ratio = data.get("ratio")
    if ratio is not None and ratio not in RATIOS:
        errors.append("ratio must be 9:16 or 3:4")

    validate_share_safe_text(data, errors)

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Workday Companion card JSON files.")
    parser.add_argument("paths", nargs="+", help="Card JSON file paths.")
    args = parser.parse_args()

    has_error = False
    for raw_path in args.paths:
        path = Path(raw_path)
        try:
            data = load_json(path)
            errors = validate_card(data)
        except OSError as exc:
            errors = [str(exc)]
        except ValueError as exc:
            errors = [str(exc)]

        if errors:
            has_error = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK {path}")

    if has_error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
