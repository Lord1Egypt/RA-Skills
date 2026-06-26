#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Optional

from campaign_reply_analysis import coerce_model_reply_analysis, validate_model_reply_analysis
from generate_reply_preview import _build_preview_item
from reply_safety import classify_reply_risk
from send_reply_previews import build_commands, run_commands


class ReplyProcessor:
    @staticmethod
    def coerce_model_reply_analysis(payload: Any) -> Optional[dict[str, Any]]:
        return coerce_model_reply_analysis(payload)

    @staticmethod
    def validate_model_reply_analysis(payload: Optional[dict[str, Any]]) -> dict[str, Any]:
        return validate_model_reply_analysis(payload)

    @staticmethod
    def generate_preview(model_analysis: dict[str, Any], template: str = "") -> list[dict[str, Any]]:
        del template
        normalized = coerce_model_reply_analysis(model_analysis) or {}
        items = normalized.get("items") if isinstance(normalized.get("items"), list) else [normalized]
        previews = []
        for item in items:
            if not isinstance(item, dict):
                continue
            mail = {
                "id": item.get("replyId"),
                "chatId": item.get("chatId"),
                "bloggerId": item.get("bloggerId"),
                "bloggerName": item.get("bloggerName"),
                "subject": item.get("subject"),
                "cleanContent": item.get("latestIncoming") or item.get("replyBody") or "",
            }
            detail = dict(mail)
            previews.append(_build_preview_item(mail, detail, [], model_analysis=item))
        return previews

    @staticmethod
    def classify_risk(mail: dict[str, Any], classification: Optional[dict[str, Any]]= None) -> dict[str, Any]:
        return classify_reply_risk(mail, classification)

    @staticmethod
    def build_commands(previews: list[dict[str, Any]], dry_run: bool = False) -> list[dict[str, Any]]:
        return build_commands(previews, dry_run=dry_run)

    @staticmethod
    def run_commands(commands: list[dict[str, Any]], campaign_id: Optional[str] = None) -> list[dict[str, Any]]:
        return run_commands(commands, campaign_id=campaign_id)
