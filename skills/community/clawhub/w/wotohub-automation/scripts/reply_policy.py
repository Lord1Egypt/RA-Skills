#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from reply_safety import should_allow_auto_reply

DEFAULT_POLICY = {
    "defaultMode": "reply_assist",
    "maxAutoRepliesPerChat": 1,
    "autoReplyWhitelist": [
        "asks_for_product_details",
        "asks_for_sample_process",
        "asks_for_next_steps",
        "simple_interest_acknowledgement",
    ],
    "forceHumanReview": [
        "negotiation",
        "pricing_discussion",
        "commission_discussion",
        "timeline_commitment",
        "shipping_commitment",
        "rejection",
        "unknown",
    ],
}


def load_policy(path: Optional[str]= None) -> dict[str, Any]:
    if not path:
        return DEFAULT_POLICY
    p = Path(path)
    if not p.exists():
        return DEFAULT_POLICY
    try:
        data = json.loads(p.read_text())
        if isinstance(data, dict):
            merged = dict(DEFAULT_POLICY)
            merged.update(data)
            return merged
    except Exception:
        pass
    return DEFAULT_POLICY


def decide_reply_action(
    classification_result: dict,
    mode: str = "reply_assist",
    policy_config: Optional[dict]= None,
    conversation_state: Optional[dict]= None,
) -> dict[str, Any]:
    policy = policy_config or DEFAULT_POLICY
    classification = str(classification_result.get("classification") or "unknown")
    requires_human = bool(classification_result.get("requiresHuman", False))

    if classification in set(policy.get("forceHumanReview", [])):
        return {
            "action": "notify_only",
            "reason": f"{classification} is configured for human review",
            "requiresHuman": True,
            "autoReplyAllowed": False,
        }

    if mode == "reply_assist":
        return {
            "action": "preview_reply",
            "reason": "Reply Assist mode uses preview-first behavior",
            "requiresHuman": requires_human,
            "autoReplyAllowed": False,
        }

    if mode == "auto_reply":
        guard = should_allow_auto_reply(
            mode=mode,
            classification_result=classification_result,
            state_item=conversation_state,
            mail=classification_result.get('_mail') if isinstance(classification_result, dict) else None,
            max_auto_replies_per_chat=int(policy.get('maxAutoRepliesPerChat', 1)),
        )
        if guard.get("allowed") and classification in set(policy.get("autoReplyWhitelist", [])) and not requires_human:
            return {
                "action": "auto_reply",
                "reason": f"{classification} is in auto-reply whitelist",
                "requiresHuman": False,
                "autoReplyAllowed": True,
                "guardrail": guard,
            }
        return {
            "action": "notify_only",
            "reason": f"auto-reply blocked: {guard.get('reason')}",
            "requiresHuman": True if requires_human or not guard.get('allowed') else False,
            "autoReplyAllowed": False,
            "guardrail": guard,
        }

    if classification in {"low_value"}:
        return {
            "action": "archive",
            "reason": "low-value message can be archived",
            "requiresHuman": False,
            "autoReplyAllowed": False,
        }

    return {
        "action": "notify_only",
        "reason": "default safe fallback",
        "requiresHuman": True if requires_human else False,
        "autoReplyAllowed": False,
    }
