#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Optional


def coerce_model_reply_analysis(payload: Any) -> Optional[dict[str, Any]]:
    if payload in (None, "", [], {}):
        return None
    if isinstance(payload, dict):
        if isinstance(payload.get("items"), list):
            items = [x for x in payload.get("items", []) if isinstance(x, dict)]
            return {"items": items}
        return payload
    if isinstance(payload, list):
        items = [x for x in payload if isinstance(x, dict)]
        return {"items": items}
    return None


def validate_model_reply_analysis(payload: Optional[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {
            "ok": False,
            "errors": ["reply_model_analysis must be a JSON object"],
            "warnings": [],
            "itemCount": 0,
            "validItemCount": 0,
        }

    items = payload.get("items")
    if isinstance(items, list):
        target_items = [x for x in items if isinstance(x, dict)]
    else:
        target_items = [payload]

    if not target_items:
        return {
            "ok": False,
            "errors": ["reply_model_analysis.items must be a non-empty array"],
            "warnings": [],
            "itemCount": 0,
            "validItemCount": 0,
        }

    errors: list[str] = []
    warnings: list[str] = []
    valid_count = 0
    for idx, item in enumerate(target_items):
        item_errors = []
        if not (item.get("replyId") or item.get("chatId")):
            item_errors.append("missing replyId/chatId")
        if not str(item.get("conversationStage") or item.get("stage") or "").strip():
            item_errors.append("missing conversationStage")
        if not str(item.get("replyBody") or item.get("body") or "").strip():
            item_errors.append("missing replyBody")
        if not str(item.get("subject") or "").strip():
            warnings.append(f"items[{idx}] missing subject")
        if item_errors:
            errors.extend([f"items[{idx}] {msg}" for msg in item_errors])
        else:
            valid_count += 1

    return {
        "ok": valid_count > 0 and not errors,
        "errors": errors,
        "warnings": warnings,
        "itemCount": len(target_items),
        "validItemCount": valid_count,
    }
