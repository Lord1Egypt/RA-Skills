#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Optional


LOW_RISK_CLASSIFICATIONS = {
    "asks_for_product_details",
    "asks_for_sample_process",
    "asks_for_next_steps",
    "simple_interest_acknowledgement",
}


def classify_reply_risk(mail: dict[str, Any], classification: Optional[dict[str, Any]]= None) -> dict[str, Any]:
    classification = classification or {}
    label = str(classification.get("classification") or "unknown")
    text = " ".join([
        str(mail.get("subject") or ""),
        str(mail.get("cleanContent") or mail.get("content") or mail.get("body") or ""),
    ]).lower()

    reasons: list[str] = []
    risk_level = "low"
    if any(x in text for x in ("price", "budget", "commission", "rate", "cost", "报价", "佣金")) or label in {"pricing_discussion", "negotiation"}:
        reasons.append("pricing_or_negotiation")
        risk_level = "high"
    if any(x in text for x in ("contract", "agreement", "terms", "exclusive", "合同", "协议")):
        reasons.append("contract_sensitive")
        risk_level = "high"
    if any(x in text for x in ("shipping", "address", "tracking", "deadline", "timeline", "发货", "地址", "时间")):
        reasons.append("logistics_or_timeline")
        risk_level = "medium" if risk_level != "high" else risk_level
    if label not in LOW_RISK_CLASSIFICATIONS and label != "unknown":
        reasons.append("classification_not_whitelisted")
        risk_level = "medium" if risk_level == "low" else risk_level
    if label == "unknown":
        reasons.append("classification_unknown")
        risk_level = "high"

    auto_send_allowed = risk_level == "low" and label in LOW_RISK_CLASSIFICATIONS
    return {
        "riskLevel": risk_level,
        "reasons": reasons,
        "autoSendAllowed": auto_send_allowed,
        "reviewRequired": not auto_send_allowed,
    }


def extract_reply_risk_flags(mail: dict[str, Any], classification: Optional[dict[str, Any]]= None) -> list[str]:
    return classify_reply_risk(mail, classification).get("reasons", [])


def should_allow_auto_reply(
    *,
    mode: str,
    classification_result: dict[str, Any],
    state_item: Optional[dict[str, Any]]= None,
    mail: Optional[dict[str, Any]]= None,
    max_auto_replies_per_chat: int = 1,
) -> dict[str, Any]:
    if mode != "auto_reply":
        return {"allowed": False, "reason": "mode_is_not_auto_reply"}
    state_item = state_item or {}
    if int(state_item.get("autoReplyCount") or 0) >= max_auto_replies_per_chat:
        return {"allowed": False, "reason": "auto_reply_limit_reached"}
    if state_item.get("campaignCycleState") in {"auto_replied", "replied", "human_review_required"}:
        return {"allowed": False, "reason": f"campaign_state_{state_item.get('campaignCycleState')}"}
    risk = classify_reply_risk(mail or {}, classification_result)
    if not risk.get("autoSendAllowed"):
        return {
            "allowed": False,
            "reason": "reply_risk_blocked",
            "riskLevel": risk.get("riskLevel"),
            "riskFlags": risk.get("reasons", []),
        }
    return {"allowed": True, "reason": "safe_auto_reply_guardrails_passed", "riskLevel": risk.get("riskLevel")}
