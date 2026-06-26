#!/usr/bin/env python3
"""Semantic-context to legacy-input compatibility layer.

This file must stay above the execution layer.
It only maps canonical context into existing legacy task inputs.
"""

from __future__ import annotations

from typing import Any

from build_search_payload import build_payload_from_context


def _compact_dict(data: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for key, value in (data or {}).items():
        if value in (None, "", [], {}):
            continue
        out[key] = value
    return out


def to_product_analysis_input(ctx: dict[str, Any]) -> dict[str, Any]:
    product = ctx.get("productSignals") or {}
    urls = product.get("urls") or []
    raw_input = product.get("rawInput")
    resolved = ctx.get("resolvedArtifacts") or {}
    return _compact_dict({
        "input": urls[0] if urls else raw_input,
        "mode": "url" if urls else "text",
        "modelAnalysis": resolved.get("modelAnalysis"),
        "productSummary": resolved.get("productSummary"),
    })


def _base_search_like_input(ctx: dict[str, Any], *, include_search_payload: bool = True) -> dict[str, Any]:
    product = ctx.get("productSignals") or {}
    marketing = ctx.get("marketingContext") or {}
    resolved = ctx.get("resolvedArtifacts") or {}
    follower_range = marketing.get("followerRange") or {}
    meta = ctx.get("meta") or {}
    model_analysis = resolved.get("modelAnalysis") or {}
    model_constraints = model_analysis.get("constraints") or {}
    model_marketing = model_analysis.get("marketing") or {}

    if (not include_search_payload) or meta.get("missingFieldPrompt"):
        search_payload = None
    else:
        search_payload = build_payload_from_context(ctx)

    base = {
        "input": (product.get("urls") or [None])[0] or product.get("rawInput"),
        "platform": (marketing.get("platforms") or model_marketing.get("platformPreference") or [None])[0],
        "country": (marketing.get("targetMarkets") or model_constraints.get("regions") or [None])[0],
        "blogLangs": marketing.get("languages") or model_constraints.get("languages") or None,
        "minFansNum": follower_range.get("min") or model_constraints.get("minFansNum"),
        "maxFansNum": follower_range.get("max") or model_constraints.get("maxFansNum"),
        "modelAnalysis": model_analysis,
        "productSummary": resolved.get("productSummary"),
        "searchPayload": search_payload,
        "categoryResolution": resolved.get("categoryResolution"),
    }
    return _compact_dict(base)


def to_search_input(ctx: dict[str, Any]) -> dict[str, Any]:
    return _base_search_like_input(ctx)


def to_recommend_input(ctx: dict[str, Any]) -> dict[str, Any]:
    product = ctx.get("productSignals") or {}
    marketing = ctx.get("marketingContext") or {}
    resolved = ctx.get("resolvedArtifacts") or {}
    base = _base_search_like_input(ctx, include_search_payload=False)
    brief = _compact_dict({
        "productName": product.get("productName") or ((resolved.get("productSummary") or {}).get("productName")),
        "brand": product.get("brand") or ((resolved.get("productSummary") or {}).get("brand")),
        "goal": marketing.get("goal"),
        "targetMarkets": marketing.get("targetMarkets") or None,
        "platforms": marketing.get("platforms") or None,
        "creatorTypes": marketing.get("creatorTypes") or None,
        "languages": marketing.get("languages") or None,
    })
    enriched = {
        **base,
        "recommendationMode": "creator_match",
        "searchResults": resolved.get("searchResults") or [],
        "brief": brief,
        "creatorTypes": marketing.get("creatorTypes") or None,
        "goal": marketing.get("goal"),
        "productName": product.get("productName"),
        "brand": product.get("brand"),
    }
    return _compact_dict(enriched)


def to_campaign_create_input(ctx: dict[str, Any]) -> dict[str, Any]:
    product = ctx.get("productSignals") or {}
    marketing = ctx.get("marketingContext") or {}
    base = _base_search_like_input(ctx)
    enriched = {
        **base,
        "input": (product.get("urls") or [None])[0] or product.get("rawInput"),
        "campaignId": (ctx.get("meta") or {}).get("campaignId"),
        "semanticContext": ctx,
        "legacyInput": _compact_dict(base),
        "campaignContext": _compact_dict({
            "productName": product.get("productName"),
            "brand": product.get("brand"),
            "goal": marketing.get("goal"),
            "offerType": marketing.get("offerType"),
            "targetMarkets": marketing.get("targetMarkets") or None,
            "platforms": marketing.get("platforms") or None,
            "creatorTypes": marketing.get("creatorTypes") or None,
        }),
    }
    return _compact_dict(enriched)


def to_generate_email_input(ctx: dict[str, Any]) -> dict[str, Any]:
    product = ctx.get("productSignals") or {}
    marketing = ctx.get("marketingContext") or {}
    resolved = ctx.get("resolvedArtifacts") or {}
    selected_creators = resolved.get("selectedCreators") or []
    host_drafts = resolved.get("hostDrafts") or resolved.get("hostEmailDrafts") or []
    selection_rule = resolved.get("selectionRule") or None
    all_search_results_selected = bool(resolved.get("allSearchResultsSelected"))
    if not selection_rule and all_search_results_selected:
        selection_rule = {"type": "all_search_results"}
    if all_search_results_selected and not selected_creators:
        selected_creators = resolved.get("searchResults") or []
    language = (marketing.get("languages") or [None])[0]
    brief = {
        "productName": product.get("productName") or ((resolved.get("productSummary") or {}).get("productName")),
        "brand": product.get("brand") or ((resolved.get("productSummary") or {}).get("brand")),
        "offerType": marketing.get("offerType"),
        "goal": marketing.get("goal"),
        "targetMarkets": marketing.get("targetMarkets") or None,
        "platforms": marketing.get("platforms") or None,
        "creatorTypes": marketing.get("creatorTypes") or None,
        "languages": marketing.get("languages") or None,
    }
    return _compact_dict({
        "brief": _compact_dict(brief),
        "productSummary": resolved.get("productSummary"),
        "modelAnalysis": resolved.get("modelAnalysis"),
        "productName": brief.get("productName"),
        "offerType": marketing.get("offerType"),
        "selectedCreators": selected_creators,
        "allSearchResultsSelected": all_search_results_selected,
        "selectionRule": selection_rule,
        "hostDrafts": host_drafts,
        "emailLanguage": language,
        "sendTargetCreatorIds": [
            item.get("bloggerId") or item.get("besId") or item.get("id")
            for item in selected_creators
            if isinstance(item, dict) and (item.get("bloggerId") or item.get("besId") or item.get("id"))
        ],
    })


def to_monitor_replies_input(ctx: dict[str, Any]) -> dict[str, Any]:
    meta = ctx.get("meta") or {}
    product = ctx.get("productSignals") or {}
    resolved = ctx.get("resolvedArtifacts") or {}
    return _compact_dict({
        "campaignId": meta.get("campaignId"),
        "input": product.get("rawInput"),
        "replyModelAnalysis": resolved.get("replyModelAnalysis"),
        "contactedBloggerIds": meta.get("contactedBloggerIds"),
        "pageSize": meta.get("pageSize"),
    })


def get_required_fields(primary_task: str, ctx: dict[str, Any]) -> list[str]:
    product = ctx.get("productSignals") or {}
    marketing = ctx.get("marketingContext") or {}
    meta = ctx.get("meta") or {}
    resolved = ctx.get("resolvedArtifacts") or {}
    has_model_analysis = isinstance(resolved.get("modelAnalysis"), dict) and bool(resolved.get("modelAnalysis"))
    has_host_drafts = bool(resolved.get("hostDrafts") or resolved.get("hostEmailDrafts"))
    has_reply_analysis = isinstance(resolved.get("replyModelAnalysis"), dict) and bool(resolved.get("replyModelAnalysis"))

    missing = []
    if primary_task == "product_analysis":
        if not ((product.get("urls") or [None])[0] or product.get("rawInput")):
            missing.append("input")
    elif primary_task in {"search", "campaign_create"}:
        if not ((product.get("urls") or [None])[0] or product.get("rawInput")):
            missing.append("input")
        if not has_model_analysis:
            missing.append("hostAnalysis")
        if not (marketing.get("platforms") or []):
            missing.append("platforms")
    elif primary_task == "recommend":
        if not has_model_analysis:
            missing.append("hostAnalysis")
        has_search_results = bool(resolved.get("searchResults"))
        if not has_search_results:
            if not ((product.get("urls") or [None])[0] or product.get("rawInput")):
                missing.append("input")
            if not (marketing.get("platforms") or []):
                missing.append("platforms")
    elif primary_task == "generate_email":
        selection_rule = resolved.get("selectionRule") or None
        all_search_results_selected = bool(resolved.get("allSearchResultsSelected"))
        if not has_model_analysis:
            missing.append("hostAnalysis")
        if not (product.get("productName") or (resolved.get("productSummary") or {}).get("productName")):
            missing.append("productName")
        if not (marketing.get("offerType")):
            missing.append("offerType")
        if not has_host_drafts:
            missing.append("hostDrafts")
        if not (
            resolved.get("selectedCreators")
            or has_host_drafts
            or selection_rule
            or all_search_results_selected
        ):
            missing.append("selectedCreators")
    elif primary_task == "monitor_replies":
        if not (meta.get("campaignId") or product.get("rawInput")):
            missing.append("campaignId_or_input")
        if not has_reply_analysis:
            missing.append("replyModelAnalysis")
    return missing


def to_legacy_task_input(primary_task: str, ctx: dict[str, Any]) -> dict[str, Any]:
    if primary_task == "product_analysis":
        return to_product_analysis_input(ctx)
    if primary_task == "search":
        return to_search_input(ctx)
    if primary_task == "recommend":
        return to_recommend_input(ctx)
    if primary_task == "campaign_create":
        return to_campaign_create_input(ctx)
    if primary_task == "generate_email":
        return to_generate_email_input(ctx)
    if primary_task == "monitor_replies":
        return to_monitor_replies_input(ctx)
    return {
        "input": ((ctx.get("productSignals") or {}).get("rawInput")),
    }
