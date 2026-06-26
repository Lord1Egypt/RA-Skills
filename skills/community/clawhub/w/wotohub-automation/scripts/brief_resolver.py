#!/usr/bin/env python3
from __future__ import annotations

from typing import Any, Optional


def build_canonical_campaign_brief(
    product_summary: Optional[dict[str, Any]]= None,
    sender_name: Optional[str]= None,
    offer_type: Optional[str]= None,
    language: Optional[str]= None,
    brand_name: Optional[str]= None,
    deliverable: Optional[str]= None,
    compensation: Optional[str]= None,
    target_market: Optional[str]= None,
    cta_goal: Optional[str]= None,
) -> dict[str, Any]:
    product_summary = product_summary or {}
    return {
        "product": {
            "productName": (product_summary.get("productName") or "").strip(),
            "brandName": (brand_name or "").strip(),
            "sellingPoints": product_summary.get("sellingPoints") or [],
            "productType": (product_summary.get("productTypeHint") or "").strip(),
            "targetMarket": (target_market or "").strip(),
            "language": (language or "en").strip() or "en",
        },
        "search": {
            "platform": (product_summary.get("platformHints") or ["tiktok"])[0] if (product_summary.get("platformHints") or ["tiktok"]) else "tiktok",
            "regions": product_summary.get("regionHints") or [],
            "languages": product_summary.get("languageHints") or [],
            "keywordHints": product_summary.get("keywordHints") or [],
            "categoryHints": product_summary.get("detectedForms") or [],
        },
        "outreach": {
            "senderName": (sender_name or "").strip(),
            "offerType": (offer_type or "sample").strip() or "sample",
            "deliverable": (deliverable or "").strip(),
            "compensation": (compensation or "").strip(),
            "ctaGoal": (cta_goal or "").strip(),
        },
        "meta": {
            "source": "merged",
            "confidence": "medium",
        },
    }


def resolve_campaign_brief(
    product_summary: Optional[dict[str, Any]]= None,
    sender_name: Optional[str]= None,
    offer_type: Optional[str]= None,
    language: Optional[str]= None,
    brand_name: Optional[str]= None,
    deliverable: Optional[str]= None,
    compensation: Optional[str]= None,
    target_market: Optional[str]= None,
    cta_goal: Optional[str]= None,
) -> dict[str, Any]:
    product_summary = product_summary or {}
    brief = {
        "productName": (product_summary.get("productName") or "").strip(),
        "brandName": (brand_name or "").strip(),
        "senderName": (sender_name or "").strip(),
        "offerType": (offer_type or "sample").strip() or "sample",
        "language": (language or "en").strip() or "en",
        "deliverable": (deliverable or "").strip(),
        "compensation": (compensation or "").strip(),
        "targetMarket": (target_market or "").strip(),
        "ctaGoal": (cta_goal or "").strip(),
        "sellingPoints": product_summary.get("sellingPoints") or [],
    }
    canonical = build_canonical_campaign_brief(
        product_summary=product_summary,
        sender_name=sender_name,
        offer_type=offer_type,
        language=language,
        brand_name=brand_name,
        deliverable=deliverable,
        compensation=compensation,
        target_market=target_market,
        cta_goal=cta_goal,
    )

    missing_required: list[str] = []
    for key in ("productName", "senderName", "offerType"):
        if not brief.get(key):
            missing_required.append(key)

    missing_optional: list[str] = []
    for key in ("brandName", "deliverable", "targetMarket", "ctaGoal"):
        if not brief.get(key):
            missing_optional.append(key)

    suggested_questions: list[str] = []
    if "productName" in missing_required:
        suggested_questions.append("这次要推广的产品名称是什么？")
    if "senderName" in missing_required:
        suggested_questions.append("邮件结尾希望署名什么名字？")
    if "offerType" in missing_required:
        suggested_questions.append("这次合作方式是 sample、paid 还是 affiliate？")
    if "brandName" in missing_optional:
        suggested_questions.append("邮件里需要带上品牌名吗？如果需要，品牌名是什么？")
    if "deliverable" in missing_optional:
        suggested_questions.append("对方需要产出什么内容形式？比如测评视频、开箱、短帖。")

    return {
        "campaignBrief": brief,
        "canonicalCampaignBrief": canonical,
        "missingRequired": missing_required,
        "missingOptional": missing_optional,
        "needsUserInput": len(missing_required) > 0,
        "suggestedQuestions": suggested_questions[:3],
    }
