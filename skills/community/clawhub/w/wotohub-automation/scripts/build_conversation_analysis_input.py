#!/usr/bin/env python3
from __future__ import annotations
from typing import Optional

import argparse
import json
from pathlib import Path

import inbox
from common import get_token


def _pick_first(*values, default=""):
    for value in values:
        if value not in (None, "", []):
            return value
    return default


def _extract_records(resp: dict) -> list[dict]:
    data = resp.get("data") if isinstance(resp, dict) else None
    if isinstance(data, dict):
        for key in ("records", "list", "rows", "dataList"):
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    return []


def _extract_dialogue_items(resp: dict) -> list[dict]:
    data = resp.get("data") if isinstance(resp, dict) else None
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in ("records", "list", "rows", "dataList"):
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
    return []


def _normalize_thread_item(item: dict) -> dict:
    return {
        "id": item.get("id"),
        "type": item.get("type"),
        "subject": item.get("subject"),
        "cleanContent": _pick_first(item.get("cleanContent"), item.get("content")),
        "createTime": item.get("createTime"),
        "addresser": item.get("addresser"),
        "addressee": item.get("addressee"),
        "cc": item.get("cc"),
        "userName": item.get("userName"),
        "bloggerName": item.get("bloggerName"),
        "bloggerUserName": item.get("bloggerUserName"),
    }


def build_input_from_inbox(
    token: str,
    page_size: int = 20,
    only_unread: bool = True,
    only_unreplied: bool = True,
    limit: int = 10,
    include_dialogue: bool = False,
    candidate_items: Optional[list[dict]]= None,
) -> dict:
    if candidate_items is None:
        inbox_resp = inbox.list_inbox(
            token,
            current_page=1,
            page_size=page_size,
            is_read=1 if only_unread else 0,
            is_reply=0 if only_unreplied else 0,
            time_range=3,
        )
        records = _extract_records(inbox_resp)
    else:
        records = [x for x in candidate_items if isinstance(x, dict)]

    items = []
    for mail in records[:limit]:
        mail_id = mail.get("id")
        chat_id = mail.get("chatId")
        if not mail_id or not chat_id:
            continue

        detail_resp = inbox.get_email_detail(token, int(mail_id))
        detail = detail_resp.get("data") if isinstance(detail_resp, dict) and isinstance(detail_resp.get("data"), dict) else mail

        dialogue_items = []
        if include_dialogue:
            dialogue_resp = inbox.get_dialogue(token, str(chat_id))
            dialogue_items = _extract_dialogue_items(dialogue_resp)

        items.append({
            "replyId": _pick_first(detail.get("id"), mail.get("id")),
            "chatId": _pick_first(detail.get("chatId"), mail.get("chatId")),
            "bloggerId": _pick_first(detail.get("bloggerId"), mail.get("bloggerId")),
            "bloggerName": _pick_first(detail.get("bloggerName"), mail.get("bloggerName"), mail.get("bloggerUserName")),
            "subject": _pick_first(detail.get("subject"), mail.get("subject")),
            "latestMail": {
                "id": _pick_first(detail.get("id"), mail.get("id")),
                "subject": _pick_first(detail.get("subject"), mail.get("subject")),
                "cleanContent": _pick_first(detail.get("cleanContent"), detail.get("content"), mail.get("cleanContent"), mail.get("content")),
                "createTime": _pick_first(detail.get("createTime"), mail.get("createTime")),
                "type": _pick_first(detail.get("type"), mail.get("type"), 1),
                "bloggerName": _pick_first(detail.get("bloggerName"), mail.get("bloggerName"), mail.get("bloggerUserName")),
                "bloggerUserName": _pick_first(detail.get("bloggerUserName"), mail.get("bloggerUserName")),
            },
            "thread": [_normalize_thread_item(x) for x in dialogue_items],
            "threadDeferred": not include_dialogue,
            "meta": {
                "isRead": _pick_first(detail.get("isRead"), mail.get("isRead")),
                "isReply": _pick_first(detail.get("isReply"), mail.get("isReply")),
                "addresser": _pick_first(detail.get("addresser"), mail.get("addresser")),
                "addressee": _pick_first(detail.get("addressee"), mail.get("addressee")),
                "bloggerUserName": _pick_first(detail.get("bloggerUserName"), mail.get("bloggerUserName")),
            },
        })

    return {
        "instruction": "Use prompts/conversation-analysis.md and references/conversation-analysis-schema.md to generate conversation_analysis JSON.",
        "items": items,
        "count": len(items),
    }


def main():
    ap = argparse.ArgumentParser(description="Build normalized input JSON for conversation-analysis prompt from inbox/detail/dialogue")
    ap.add_argument("--token")
    ap.add_argument("--page-size", type=int, default=20)
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--include-read", action="store_true")
    ap.add_argument("--include-replied", action="store_true")
    ap.add_argument("--include-dialogue", action="store_true")
    ap.add_argument("--candidate-file")
    ap.add_argument("--output")
    args = ap.parse_args()

    token = get_token(args.token, feature="conversation_analysis")
    candidate_items = None
    if args.candidate_file:
        raw = json.loads(Path(args.candidate_file).read_text())
        candidate_items = raw.get("items") if isinstance(raw, dict) else None
    result = build_input_from_inbox(
        token=token,
        page_size=args.page_size,
        only_unread=not args.include_read,
        only_unreplied=not args.include_replied,
        limit=args.limit,
        include_dialogue=args.include_dialogue,
        candidate_items=candidate_items,
    )
    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
