#!/usr/bin/env python3
"""
Reply handling and classification for campaign engine.

Consolidates reply-related logic:
- Intent classification
- Reply classification via model
- Safe reply body building
- Reply model analysis generation
"""

from __future__ import annotations

from typing import Any, Optional


class ReplyHandler:
    """Unified reply handling interface.

    Policy:
    - Prefer host-model-produced reply analysis when available.
    - Local classification in this file is rule-based fallback only.
    """

    @staticmethod
    def classify_intent(reply: dict[str, Any]) -> str:
        """Classify reply intent from content."""
        text = " ".join([
            str(reply.get("subject") or ""),
            str(reply.get("content") or reply.get("cleanContent") or ""),
        ]).lower()

        if any(x in text for x in ["not interested", "no thanks", "pass", "decline", "不了", "拒绝"]):
            return "rejected"
        if any(x in text for x in ["interested", "sounds good", "let's do it", "可以", "同意", "合作", "confirm"]):
            return "confirmed"
        if any(x in text for x in ["price", "budget", "details", "sample", "shipping", "more info", "next step"]):
            return "discussing"
        return "discussing"

    @staticmethod
    def classify_reply(reply: dict[str, Any]) -> dict[str, Any]:
        """Classify reply with detailed analysis.

        This is rule-based fallback only. It should not be treated as the
        primary conversation understanding layer when reply_model_analysis is available.
        """
        text_for_analysis = " ".join([
            str(reply.get("subject") or ""),
            str(reply.get("content") or reply.get("cleanContent") or ""),
        ]).lower()

        classification = "unknown"
        requires_human = False
        stage = "unknown"
        intent = "unknown"
        tone = "neutral"
        risk_flags = []

        if any(k in text_for_analysis for k in ["price", "pricing", "budget", "cost", "rate", "commission", "价格", "费用"]):
            classification = "pricing_discussion"
            requires_human = True
            stage = "pricing_negotiation"
            intent = "asking_pricing"
            tone = "business"
            risk_flags = ["price_sensitive"]
        elif any(k in text_for_analysis for k in ["sample", "process", "怎么", "how to get"]):
            classification = "asks_for_sample_process"
            requires_human = False
            stage = "sample_shipping"
            intent = "asking_sample"
        elif any(k in text_for_analysis for k in ["detail", "info", "information", "spec", "参数"]):
            classification = "asks_for_product_details"
            requires_human = False
            stage = "product_question"
            intent = "asking_product_details"
        elif any(k in text_for_analysis for k in ["interested", "sounds good", "let's do", "可以", "合作"]):
            classification = "simple_interest_acknowledgement"
            requires_human = False
            stage = "collaboration_confirm"
            intent = "confirming_collab"
        elif any(k in text_for_analysis for k in ["not interested", "no thanks", "pass", "decline", "拒绝", "不了"]):
            classification = "soft_rejection"
            requires_human = True
            stage = "soft_rejection"
            intent = "rejecting"
            tone = "closure-polite"
        elif any(k in text_for_analysis for k in ["shipping", "ship to", "address", "tracking", "快递"]):
            classification = "logistics_commitment"
            requires_human = True
            stage = "logistics_planning"
            intent = "asking_logistics"
            tone = "business"
            risk_flags = ["shipping_commitment"]
        elif any(k in text_for_analysis for k in ["contract", "agreement", "terms", "exclusive", "合同", "协议"]):
            classification = "contract_discussion"
            requires_human = True
            stage = "contract_review"
            intent = "discussing_contract"
            tone = "business"
            risk_flags = ["contract_sensitive"]
        elif any(k in text_for_analysis for k in ["next step", "what's next", "timeline", "when", "deadline", "下一步"]):
            classification = "asks_for_next_steps"
            requires_human = False
            stage = "process_clarification"
            intent = "asking_process"

        return {
            "classification": classification,
            "requiresHuman": requires_human,
            "stage": stage,
            "intent": intent,
            "tone": tone,
            "riskFlags": risk_flags,
            "analysisSource": "reply_handler_rule_based_fallback",
        }

    @staticmethod
    def generate_analysis(items: list[dict[str, Any]], context: dict[str, Any]) -> dict[str, Any]:
        """Generate reply model analysis from items."""
        if not isinstance(items, list):
            items = []

        analyzed_items = []
        for item in items:
            if not isinstance(item, dict):
                continue

            reply_id = item.get("replyId") or item.get("chatId")
            if not reply_id:
                continue

            classification = ReplyHandler.classify_reply(item)
            analyzed_items.append({
                "replyId": reply_id,
                "chatId": item.get("chatId"),
                "conversationStage": item.get("conversationStage") or classification.get("stage"),
                "replyBody": item.get("replyBody") or item.get("content") or "",
                "subject": item.get("subject") or "",
                "classification": classification.get("classification"),
                "requiresHuman": classification.get("requiresHuman"),
                "intent": classification.get("intent"),
                "tone": classification.get("tone"),
                "riskFlags": classification.get("riskFlags", []),
            })

        return {
            "items": analyzed_items,
            "context": context,
            "analysisMode": "rule-based-fallback",
            "analysisProvenance": {
                "source": "reply_handler_rule_based_fallback",
                "confidence": "low",
            },
        }

    @staticmethod
    def build_safe_body(
        template: str,
        product_name: Optional[str]= None,
        brand_name: Optional[str]= None,
        sender_name: Optional[str]= None,
        offer_type: Optional[str]= None,
    ) -> str:
        """Build safe reply body from template."""
        body = template or ""

        if product_name:
            body = body.replace("{product_name}", product_name)
        if brand_name:
            body = body.replace("{brand_name}", brand_name)
        if sender_name:
            body = body.replace("{sender_name}", sender_name)
        if offer_type:
            body = body.replace("{offer_type}", offer_type)

        return body.strip()
