#!/usr/bin/env python3
"""Canonical upper-layer semantic context schema for WotoHub upper-layer architecture.

Scope of this file:
- define the stable semantic context shape for the new upper-layer brain
- normalize partial context into a predictable structure
- stay fully above the execution layer; no API calls here
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Optional


DEFAULT_CONTEXT: dict[str, Any] = {
    "intent": {
        "primaryTask": None,
        "secondaryTasks": [],
    },
    "productSignals": {
        "rawInput": None,
        "urls": [],
        "productName": None,
        "brand": None,
        "category": None,
        "priceHint": None,
        "features": [],
        "useCases": [],
        "sourcePlatform": None,
        "sourceHost": None,
    },
    "marketingContext": {
        "targetMarkets": [],
        "platforms": [],
        "creatorTypes": [],
        "followerRange": {
            "min": None,
            "max": None,
        },
        "offerType": None,
        "budgetLevel": None,
        "goal": None,
        "languages": [],
    },
    "operationalHints": {
        "needsProductResolve": False,
        "needsSearch": False,
        "needsCampaignBuild": False,
        "needsOutreachDraft": False,
        "needsInboxAssist": False,
    },
    "missingFields": [],
    "resolvedArtifacts": {
        "productResolve": None,
        "modelAnalysis": None,
        "replyModelAnalysis": None,
        "productSummary": None,
        "localHeuristicAnalysis": None,
        "searchPayloadHints": None,
        "categoryResolution": None,
        "selectedCreators": None,
        "hostDrafts": None,
        "hostEmailDrafts": None,
        "selectionRule": None,
        "allSearchResultsSelected": False,
        "searchResults": None,
    },
    "meta": {
        "usedHostModel": False,
        "usedFallback": False,
        "needsHostAnalysis": False,
        "confidence": None,
        "analysisPath": "upper_layer_brain",
        "campaignId": None,
        "notes": [],
        "hostResolution": {},
    },
}


TASK_TO_OPERATIONAL_HINTS: dict[str, dict[str, bool]] = {
    "product_analysis": {
        "needsProductResolve": True,
    },
    "search": {
        "needsSearch": True,
    },
    "influencer_search": {
        "needsSearch": True,
    },
    "recommend": {
        "needsSearch": True,
    },
    "campaign_create": {
        "needsCampaignBuild": True,
    },
    "generate_email": {
        "needsOutreachDraft": True,
    },
    "outreach_generate": {
        "needsOutreachDraft": True,
    },
    "inbox_assist": {
        "needsInboxAssist": True,
    },
    "monitor_replies": {
        "needsInboxAssist": True,
    },
}


CANONICAL_TASK_MAP = {
    "product_analysis": "product_analysis",
    "search": "search",
    "influencer_search": "search",
    "recommend": "recommend",
    "campaign_create": "campaign_create",
    "generate_email": "generate_email",
    "outreach_generate": "generate_email",
    "inbox_assist": "monitor_replies",
    "monitor_replies": "monitor_replies",
}


SUPPORTED_PRIMARY_TASKS = {
    "product_analysis",
    "search",
    "recommend",
    "campaign_create",
    "generate_email",
    "monitor_replies",
}


def empty_context() -> dict[str, Any]:
    return deepcopy(DEFAULT_CONTEXT)


def normalize_primary_task(task: Optional[str]) -> Optional[str]:
    if not task:
        return None
    normalized = CANONICAL_TASK_MAP.get(str(task).strip().lower(), str(task).strip().lower())
    if normalized in SUPPORTED_PRIMARY_TASKS:
        return normalized
    return normalized


def apply_task_defaults(ctx: dict[str, Any]) -> dict[str, Any]:
    task = normalize_primary_task(((ctx.get("intent") or {}).get("primaryTask")))
    if task:
        ctx.setdefault("intent", {})["primaryTask"] = task
    hints = (ctx.setdefault("operationalHints", {}) or {})
    for key in DEFAULT_CONTEXT["operationalHints"].keys():
        hints.setdefault(key, False)
    for key, value in TASK_TO_OPERATIONAL_HINTS.get(task, {}).items():
        hints[key] = value
    return ctx


def _merge_dict(base: dict[str, Any], incoming: dict[str, Any]) -> dict[str, Any]:
    for key, value in incoming.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            base[key] = _merge_dict(base[key], value)
        elif value not in (None, "", [], {}):
            base[key] = value
    return base


def normalize_context(partial: Optional[dict[str, Any]]= None) -> dict[str, Any]:
    ctx = empty_context()
    if partial:
        ctx = _merge_dict(ctx, partial)
    ctx = apply_task_defaults(ctx)
    return ctx
