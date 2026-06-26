#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Optional

from brief_schema import normalize_campaign_brief


FORBIDDEN_SCHEDULED_SEARCH_FIELDS = {
    "regionList",
    "blogCateIds",
    "advancedKeywordList",
    "searchType",
}


def _detect_forbidden_scheduled_search_overrides(*sources: Any) -> list[str]:
    hits: list[str] = []
    for source in sources:
        if not isinstance(source, dict):
            continue
        for key in FORBIDDEN_SCHEDULED_SEARCH_FIELDS:
            value = source.get(key)
            if value not in (None, "", [], {}):
                hits.append(key)
    return sorted(set(hits))


SCHEDULE_HINTS = [
    ("every_30m", ["每30分钟", "每半小时", "every 30 minutes", "every 30 mins"]),
    ("every_1h", ["每小时", "every hour", "hourly"]),
    ("daily", ["每天", "daily", "每天一次"]),
]


def _infer_schedule(raw_input: str, config: Optional[dict[str, Any]]= None) -> dict[str, Any]:
    text = (raw_input or "").lower()
    cfg = config or {}
    if cfg.get("schedule"):
        return cfg["schedule"]
    for key, hints in SCHEDULE_HINTS:
        if any(hint in text for hint in hints):
            if key == "every_30m":
                return {"kind": "every", "everyMs": 1800000}
            if key == "every_1h":
                return {"kind": "every", "everyMs": 3600000}
            if key == "daily":
                return {"kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai"}
    return {"kind": "every", "everyMs": 1800000}


def build_campaign_plan(
    *,
    raw_input: str,
    semantic_context: dict[str, Any],
    legacy_input: dict[str, Any],
    config: Optional[dict[str, Any]]= None,
) -> dict[str, Any]:
    ctx = semantic_context or {}
    resolved = ctx.get("resolvedArtifacts") or {}
    marketing = ctx.get("marketingContext") or {}
    product = ctx.get("productSignals") or {}
    summary = resolved.get("productSummary") or {}
    model_analysis = resolved.get("modelAnalysis") or legacy_input.get("modelAnalysis") or {}
    search_payload = legacy_input.get("searchPayload") or {}

    selection_rule = resolved.get("selectionRule") or None
    all_search_results_selected = bool(resolved.get("allSearchResultsSelected"))
    if not selection_rule and all_search_results_selected:
        selection_rule = {"type": "all_search_results"}

    schedule = _infer_schedule(raw_input, config=config)

    forbidden_overrides = _detect_forbidden_scheduled_search_overrides(
        legacy_input,
        legacy_input.get("searchPayload") or {},
        model_analysis.get("searchPayloadHints") or {},
    )

    campaign_plan = {
        "intent": "scheduled_outreach",
        "rawInput": raw_input,
        "product": {
            "productName": product.get("productName") or summary.get("productName"),
            "brandName": product.get("brand") or summary.get("brand"),
            "sellingPoints": summary.get("sellingPoints") or (model_analysis.get("product") or {}).get("coreBenefits") or [],
            "sourceUrl": ((product.get("urls") or [None])[0]),
        },
        "searchStrategy": {
            "platform": legacy_input.get("platform") or (search_payload.get("platform")),
            "regions": marketing.get("targetMarkets") or [],
            "languages": marketing.get("languages") or legacy_input.get("blogLangs") or search_payload.get("blogLangs") or [],
            "keywordHints": [
                item.get("value") if isinstance(item, dict) else item
                for item in (search_payload.get("advancedKeywordList") or [])
            ],
            "categoryHints": search_payload.get("blogCateIds") or [],
            "followerRange": {
                "min": legacy_input.get("minFansNum") or search_payload.get("minFansNum"),
                "max": legacy_input.get("maxFansNum") or search_payload.get("maxFansNum"),
            },
            "hasEmail": legacy_input.get("hasEmail") if legacy_input.get("hasEmail") is not None else search_payload.get("hasEmail"),
        },
        "selectionRule": selection_rule,
        "outreachPolicy": {
            "senderName": (config or {}).get("senderName") or legacy_input.get("senderName") or (legacy_input.get("campaignContext") or {}).get("senderName"),
            "offerType": marketing.get("offerType") or (legacy_input.get("campaignContext") or {}).get("offerType"),
            "emailLanguage": (marketing.get("languages") or ["en"])[0] if (marketing.get("languages") or []) else "en",
            "sendPolicy": (config or {}).get("sendPolicy") or "scheduled_send",
            "reviewRequired": (config or {}).get("reviewRequired"),
        },
        "draftPolicy": {
            "mode": ((config or {}).get("draftPolicy") or {}).get("mode") or "host_model_per_cycle",
            "allowFallbackDrafts": bool(((config or {}).get("draftPolicy") or {}).get("allowFallbackDrafts", False)),
            "batchGeneration": True,
        },
        "schedule": schedule,
        "modelAnalysis": model_analysis,
        "productSummary": summary,
        "missingFields": [],
        "validation": {
            "forbiddenScheduledSearchOverrides": forbidden_overrides,
            "ok": len(forbidden_overrides) == 0,
        },
    }

    if not campaign_plan["product"].get("productName"):
        campaign_plan["missingFields"].append("productName")
    if not campaign_plan["searchStrategy"].get("platform"):
        campaign_plan["missingFields"].append("platforms")
    if not campaign_plan["outreachPolicy"].get("offerType"):
        campaign_plan["missingFields"].append("offerType")
    if forbidden_overrides:
        campaign_plan["missingFields"].append("scheduled_search_overrides_not_allowed")
    return campaign_plan


def build_brief_from_campaign_plan(campaign_id: str, campaign_plan: dict[str, Any]) -> dict[str, Any]:
    product = campaign_plan.get("product") or {}
    search = campaign_plan.get("searchStrategy") or {}
    outreach = campaign_plan.get("outreachPolicy") or {}
    draft_policy = campaign_plan.get("draftPolicy") or {}
    brief = {
        "campaignId": campaign_id,
        "input": product.get("sourceUrl") or product.get("productName") or campaign_plan.get("rawInput"),
        "product": {
            "productName": product.get("productName"),
            "brandName": product.get("brandName"),
            "sellingPoints": product.get("sellingPoints") or [],
            "url": product.get("sourceUrl"),
        },
        "search": {
            "platform": search.get("platform") or "tiktok",
            "region": search.get("regions") or [],
            "language": search.get("languages") or [],
            "minFansNum": (search.get("followerRange") or {}).get("min"),
            "maxFansNum": (search.get("followerRange") or {}).get("max"),
            "hasEmail": search.get("hasEmail"),
        },
        "outreach": {
            "senderName": outreach.get("senderName"),
            "cooperationType": outreach.get("offerType"),
            "emailLanguage": outreach.get("emailLanguage") or "en",
            "sendPolicy": outreach.get("sendPolicy") or "scheduled_send",
            "reviewRequired": outreach.get("reviewRequired"),
        },
        "inboxMonitoring": {
            "autoReplyPolicy": "low_risk_auto_reply_with_high_risk_summary",
        },
        "selectionRule": campaign_plan.get("selectionRule"),
        "draftPolicy": {
            "mode": draft_policy.get("mode") or "host_model_per_cycle",
            "allowFallbackDrafts": bool(draft_policy.get("allowFallbackDrafts", False)),
            "batchGeneration": bool(draft_policy.get("batchGeneration", True)),
        },
        "requireReplyModelAnalysis": True,
        "scheduler": campaign_plan.get("schedule") or {"kind": "every", "everyMs": 1800000},
        "model_analysis": campaign_plan.get("modelAnalysis"),
        "productSummary": campaign_plan.get("productSummary"),
    }
    return normalize_campaign_brief(brief)
