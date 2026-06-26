#!/usr/bin/env python3
"""Unified reply processing pipeline.

Policy:
- Host model analysis should be preferred by the caller.
- This module provides rule-based fallback classification only.
"""

from __future__ import annotations

from typing import Any, Optional


class ReplyPipeline:
    """Single pipeline for reply analysis."""

    @staticmethod
    def _normalize_model_item(item: dict[str, Any]) -> dict[str, Any]:
        return {
            "classification": item.get("classification") or "unknown",
            "intent": item.get("intent") or "unknown",
            "requiresHuman": bool(item.get("requiresHuman")),
            "riskFlags": item.get("riskFlags") or [],
            "conversationStage": item.get("conversationStage") or item.get("stage"),
            "tone": item.get("tone") or "neutral",
            "replyBody": item.get("replyBody") or item.get("body"),
            "analysisSource": item.get("analysisSource") or "reply_model_analysis",
        }

    @staticmethod
    def _match_model_item(reply: dict[str, Any], reply_model_analysis: Optional[dict[str, Any]]= None) -> Optional[dict[str, Any]]:
        if not isinstance(reply_model_analysis, dict):
            return None
        items = reply_model_analysis.get("items") if isinstance(reply_model_analysis.get("items"), list) else [reply_model_analysis]
        reply_ids = {
            str(reply.get("id") or "").strip(),
            str(reply.get("emailId") or "").strip(),
            str(reply.get("replyId") or "").strip(),
        }
        chat_id = str(reply.get("chatId") or "").strip()
        blogger_id = str(reply.get("bloggerId") or "").strip()
        for item in items:
            if not isinstance(item, dict):
                continue
            item_reply_id = str(item.get("replyId") or item.get("id") or "").strip()
            item_chat_id = str(item.get("chatId") or "").strip()
            item_blogger_id = str(item.get("bloggerId") or "").strip()
            if item_reply_id and item_reply_id in reply_ids:
                return item
            if chat_id and item_chat_id and item_chat_id == chat_id:
                return item
            if blogger_id and item_blogger_id and item_blogger_id == blogger_id:
                return item
        return None

    @staticmethod
    def analyze(
        reply: dict,
        brief: Optional[dict]= None,
        reply_model_analysis: Optional[dict]= None,
        allow_fallback: bool = False,
    ) -> dict:
        """Analyze reply with model-analysis-first logic.

        If a matching item exists in reply_model_analysis, use it directly.
        Rule-based heuristics are available only when allow_fallback=True.
        """
        del brief

        model_item = ReplyPipeline._match_model_item(reply, reply_model_analysis)
        if model_item:
            return ReplyPipeline._normalize_model_item(model_item)

        if not allow_fallback:
            return {
                "classification": "needs_reply_model_analysis",
                "intent": "unknown",
                "requiresHuman": True,
                "riskFlags": ["missing_reply_model_analysis"],
                "analysisSource": "blocked_missing_reply_model_analysis",
            }

        text = " ".join([
            str(reply.get("subject", "")),
            str(reply.get("cleanContent", reply.get("content", ""))),
        ]).lower()

        # Simple heuristic rules (no model call for now)
        if any(k in text for k in ["price", "budget", "cost", "rate", "commission"]):
            return {
                "classification": "pricing_discussion",
                "intent": "asking_pricing",
                "requiresHuman": True,
                "riskFlags": ["price_sensitive"],
                "analysisSource": "rule_based_fallback",
            }
        elif any(k in text for k in ["interested", "sounds good", "let's do", "可以", "合作"]):
            return {
                "classification": "simple_interest",
                "intent": "confirming",
                "requiresHuman": False,
                "riskFlags": [],
                "analysisSource": "rule_based_fallback",
            }
        elif any(k in text for k in ["not interested", "decline", "pass", "拒绝"]):
            return {
                "classification": "rejection",
                "intent": "rejecting",
                "requiresHuman": True,
                "riskFlags": [],
                "analysisSource": "rule_based_fallback",
            }
        elif any(k in text for k in ["sample", "process", "how to", "怎么"]):
            return {
                "classification": "asks_for_sample",
                "intent": "asking_sample",
                "requiresHuman": False,
                "riskFlags": [],
                "analysisSource": "rule_based_fallback",
            }
        elif any(k in text for k in ["detail", "info", "spec", "参数"]):
            return {
                "classification": "asks_for_details",
                "intent": "asking_details",
                "requiresHuman": False,
                "riskFlags": [],
                "analysisSource": "rule_based_fallback",
            }

        return {
            "classification": "unknown",
            "intent": "unknown",
            "requiresHuman": False,
            "riskFlags": [],
            "analysisSource": "rule_based_fallback",
        }
