#!/usr/bin/env python3
from __future__ import annotations
from typing import Optional, Union

import json
from datetime import datetime, timedelta
from pathlib import Path

from common import state_file


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _state_path() -> Path:
    return state_file("conversation_state.json")


def load_state() -> dict:
    path = _state_path()
    if not path.exists():
        return {"emails": {}, "chats": {}}
    try:
        data = json.loads(path.read_text())
        if not isinstance(data, dict):
            return {"emails": {}, "chats": {}}
        data.setdefault("emails", {})
        data.setdefault("chats", {})
        return data
    except Exception:
        return {"emails": {}, "chats": {}}


def save_state(state: dict) -> None:
    path = _state_path()
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def get_email_state(email_id: Union[str, int]) -> Optional[dict]:
    state = load_state()
    return (state.get("emails") or {}).get(str(email_id))


def get_chat_state(chat_id: Optional[Union[str, int]]) -> Optional[dict]:
    if chat_id in (None, ""):
        return None
    state = load_state()
    return (state.get("chats") or {}).get(str(chat_id))


def upsert_email_state(email_id: Union[str, int], patch: dict) -> dict:
    state = load_state()
    emails = state.setdefault("emails", {})
    current = emails.get(str(email_id), {})
    current.update(patch)
    current["lastProcessedAt"] = _now_iso()
    emails[str(email_id)] = current
    save_state(state)
    return current


def upsert_chat_state(chat_id: Optional[Union[str, int]], patch: dict) -> Optional[dict]:
    if chat_id in (None, ""):
        return None
    state = load_state()
    chats = state.setdefault("chats", {})
    current = chats.get(str(chat_id), {})
    current.update(patch)
    current["lastProcessedAt"] = _now_iso()
    chats[str(chat_id)] = current
    save_state(state)
    return current


def mark_scanned(email_id, chat_id=None, blogger_id=None, metadata: Optional[dict]= None) -> dict:
    current = get_email_state(email_id) or {}
    payload = {
        "emailId": email_id,
        "chatId": chat_id,
        "bloggerId": blogger_id,
        "lastAction": "scanned",
        "processed": False,
        "campaignCycleState": current.get("campaignCycleState") or "scanned",
        "scanCount": int(current.get("scanCount") or 0) + 1,
        "autoReplyCount": int(current.get("autoReplyCount") or 0),
    }
    if metadata:
        payload["meta"] = metadata
    updated = upsert_email_state(email_id, payload)
    upsert_chat_state(chat_id, {
        "chatId": chat_id,
        "bloggerId": blogger_id,
        "lastAction": "scanned",
        "campaignCycleState": (get_chat_state(chat_id) or {}).get("campaignCycleState") or "scanned",
        "autoReplyCount": int(((get_chat_state(chat_id) or {}).get("autoReplyCount") or 0)),
        "lastEmailId": email_id,
    })
    return updated


def mark_classified(email_id, classification: str, priority: str, requires_human: bool, metadata: Optional[dict]= None) -> dict:
    current = get_email_state(email_id) or {}
    payload = {
        "classification": classification,
        "priority": priority,
        "requiresHuman": requires_human,
        "lastAction": "classified",
        "campaignCycleState": "human_review_required" if requires_human else "classified",
    }
    if metadata:
        payload["classificationMeta"] = metadata
    updated = upsert_email_state(email_id, payload)
    upsert_chat_state(current.get("chatId"), {
        "chatId": current.get("chatId"),
        "bloggerId": current.get("bloggerId"),
        "classification": classification,
        "priority": priority,
        "requiresHuman": requires_human,
        "lastAction": "classified",
        "campaignCycleState": "human_review_required" if requires_human else "classified",
        "lastEmailId": email_id,
    })
    return updated


def mark_preview_generated(email_id, metadata: Optional[dict]= None) -> dict:
    current = get_email_state(email_id) or {}
    payload = {"lastAction": "preview_generated", "previewGenerated": True, "campaignCycleState": "preview_generated"}
    if metadata:
        payload["previewMeta"] = metadata
    updated = upsert_email_state(email_id, payload)
    upsert_chat_state(current.get("chatId"), {
        "chatId": current.get("chatId"),
        "bloggerId": current.get("bloggerId"),
        "lastAction": "preview_generated",
        "campaignCycleState": "preview_generated",
        "lastEmailId": email_id,
    })
    return updated


def mark_notified(email_id, metadata: Optional[dict]= None) -> dict:
    current = get_email_state(email_id) or {}
    payload = {"lastAction": "notified", "notified": True, "campaignCycleState": "human_review_required"}
    if metadata:
        payload["notifyMeta"] = metadata
    updated = upsert_email_state(email_id, payload)
    upsert_chat_state(current.get("chatId"), {
        "chatId": current.get("chatId"),
        "bloggerId": current.get("bloggerId"),
        "lastAction": "notified",
        "campaignCycleState": "human_review_required",
        "lastEmailId": email_id,
    })
    return updated


def mark_replied(email_id, reply_id=None, auto: bool = False, metadata: Optional[dict]= None, chat_id=None) -> dict:
    current = get_email_state(email_id) or {}
    resolved_chat_id = chat_id or current.get("chatId")
    current_chat = get_chat_state(resolved_chat_id) or {}
    payload = {
        "lastAction": "auto_replied" if auto else "replied",
        "processed": True,
        "replySent": True,
        "replyId": reply_id,
        "autoReplied": auto,
        "autoReplyCount": int(current.get("autoReplyCount") or 0) + (1 if auto else 0),
        "campaignCycleState": "auto_replied" if auto else "replied",
    }
    if metadata:
        payload["replyMeta"] = metadata
    updated = upsert_email_state(email_id, payload)
    upsert_chat_state(resolved_chat_id, {
        "chatId": resolved_chat_id,
        "bloggerId": current.get("bloggerId"),
        "lastAction": "auto_replied" if auto else "replied",
        "replySent": True,
        "replyId": reply_id,
        "autoReplied": auto,
        "autoReplyCount": int(current_chat.get("autoReplyCount") or 0) + (1 if auto else 0),
        "campaignCycleState": "auto_replied" if auto else "replied",
        "lastEmailId": email_id,
    })
    return updated


def mark_archived(email_id, metadata: Optional[dict]= None) -> dict:
    current = get_email_state(email_id) or {}
    payload = {"lastAction": "archived", "processed": True, "archived": True, "campaignCycleState": "archived"}
    if metadata:
        payload["archiveMeta"] = metadata
    updated = upsert_email_state(email_id, payload)
    upsert_chat_state(current.get("chatId"), {
        "chatId": current.get("chatId"),
        "bloggerId": current.get("bloggerId"),
        "lastAction": "archived",
        "processed": True,
        "archived": True,
        "campaignCycleState": "archived",
        "lastEmailId": email_id,
    })
    return updated


def get_skip_reason(email_id, chat_id=None, cooldown_minutes: int = 30) -> Optional[str]:
    item = get_email_state(email_id)
    if not item:
        return None
    if item.get("processed"):
        return "already_processed"
    if item.get("campaignCycleState") in {"human_review_required", "preview_generated", "auto_replied", "replied", "archived"}:
        return f"campaign_state_{item.get('campaignCycleState')}"
    if item.get("lastAction") in {"notified", "preview_generated", "auto_replied", "replied", "archived"}:
        return f"already_{item.get('lastAction')}"
    ts = item.get("lastProcessedAt")
    if ts:
        try:
            last_dt = datetime.fromisoformat(ts)
            if datetime.now().astimezone() - last_dt < timedelta(minutes=cooldown_minutes):
                return "cooldown_active"
        except Exception:
            pass
    return None


def should_skip_email(email_id, chat_id=None, cooldown_minutes: int = 30) -> bool:
    return get_skip_reason(email_id, chat_id=chat_id, cooldown_minutes=cooldown_minutes) is not None
