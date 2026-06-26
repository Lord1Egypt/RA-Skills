#!/usr/bin/env python3
"""
Campaign brief normalization and validation.

Handles:
- Legacy/public brief format conversion
- Field normalization
- Missing field detection
"""

from __future__ import annotations

import copy
from typing import Any, Optional


FORBIDDEN_SCHEDULED_EXECUTION_FIELDS = {
    "search.blogCateIds",
    "search.advancedKeywordList",
    "search.searchType",
    "search.regionList",
    "search.keywords",
    "blogCateIds",
    "advancedKeywordList",
    "searchType",
    "regionList",
    "searchPayload",
}


def detect_forbidden_scheduled_execution_fields(raw_brief: dict[str, Any]) -> list[str]:
    brief = raw_brief or {}
    search = brief.get("search") or {}
    hits: list[str] = []

    field_map = {
        "search.blogCateIds": search.get("blogCateIds"),
        "search.advancedKeywordList": search.get("advancedKeywordList"),
        "search.searchType": search.get("searchType"),
        "search.regionList": search.get("regionList"),
        "search.keywords": search.get("keywords"),
        "blogCateIds": brief.get("blogCateIds"),
        "advancedKeywordList": brief.get("advancedKeywordList"),
        "searchType": brief.get("searchType"),
        "regionList": brief.get("regionList"),
        "searchPayload": brief.get("searchPayload"),
    }
    for key, value in field_map.items():
        if value not in (None, "", [], {}):
            hits.append(key)
    return sorted(set(hits))


def validate_scheduled_execution_brief(brief: dict[str, Any]) -> dict[str, Any]:
    forbidden = detect_forbidden_scheduled_execution_fields(brief)
    errors = []
    if forbidden:
        errors.append(
            "scheduled cycle brief must not carry near-final search payload fields; keep semantic inputs/model_analysis only and compile search params at execution time"
        )
    return {
        "ok": not errors,
        "errors": errors,
        "forbiddenFields": forbidden,
    }




def _to_advanced_keywords(values: list[Any], *, limit: int = 8) -> list[dict[str, Any]]:
    """Convert values to advanced keyword list format."""
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for value in values or []:
        text = str(value or "").strip()
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append({"value": text, "exclude": False})
        if len(out) >= limit:
            break
    return out


def _normalize_selection_rule(rule: Any) -> Optional[dict[str, Any]]:
    if not isinstance(rule, dict):
        return None
    rule_type = str(rule.get("type") or "").strip().lower()
    if not rule_type:
        return None
    normalized: dict[str, Any] = {"type": rule_type}
    if rule_type == "top_n":
        top_n = rule.get("top_n") if rule.get("top_n") is not None else rule.get("topN")
        try:
            top_n_int = int(top_n)
        except Exception:
            top_n_int = 0
        if top_n_int > 0:
            normalized["top_n"] = top_n_int
    for key, value in rule.items():
        if key in {"type", "topN", "top_n"}:
            continue
        normalized[key] = value
    return normalized


def normalize_campaign_brief(raw_brief: dict[str, Any]) -> dict[str, Any]:
    """Normalize legacy/public campaign briefs into flat engine contract.

    Accepts both internal flat format and public package style:
    {product:{...}, search:{...}, outreach:{...}, inboxMonitoring:{...}}
    """
    brief = copy.deepcopy(raw_brief or {})
    product = brief.get("product") or {}
    search = brief.get("search") or {}
    outreach = brief.get("outreach") or {}
    inbox = brief.get("inboxMonitoring") or {}

    def first_non_empty(*values: Any) -> Any:
        for value in values:
            if value in (None, "", [], {}):
                continue
            if isinstance(value, str) and not value.strip():
                continue
            return value
        return None

    normalized = dict(brief)
    product_name = first_non_empty(
        brief.get("product_name"),
        brief.get("productName"),
        product.get("name"),
        product.get("productName"),
    )
    product_url = first_non_empty(
        brief.get("product_url"),
        brief.get("url"),
        product.get("url"),
        product.get("productUrl"),
    )
    selling_points = first_non_empty(
        brief.get("selling_points"),
        brief.get("sellingPoints"),
        product.get("sellingPoints"),
    ) or []
    keyword_terms = first_non_empty(brief.get("keywords"), search.get("keywords")) or []
    if isinstance(keyword_terms, str):
        keyword_terms = [keyword_terms]

    platform = str(first_non_empty(brief.get("platform"), search.get("platform"), "tiktok")).strip() or "tiktok"

    region = first_non_empty(brief.get("region"), search.get("region"))
    if isinstance(region, list):
        region_codes = [str(x).strip().lower() for x in region if str(x).strip()]
    elif region:
        region_codes = [str(region).strip().lower()]
    else:
        region_codes = []

    language = first_non_empty(brief.get("language"), search.get("lang"), search.get("language"))
    if isinstance(language, list):
        language_codes = [str(x).strip().lower() for x in language if str(x).strip()]
    elif language:
        language_codes = [str(language).strip().lower()]
    else:
        language_codes = []

    if not normalized.get("input"):
        normalized["input"] = product_url or product_name or " ".join(
            [str(x).strip() for x in selling_points[:3] if str(x).strip()]
        )
    if product_name and not normalized.get("product_name"):
        normalized["product_name"] = product_name

    normalized["platform"] = platform
    min_fans_value = first_non_empty(brief.get("min_fans"), search.get("minFans"), search.get("minFansNum"))
    max_fans_value = first_non_empty(brief.get("max_fans"), search.get("maxFans"), search.get("maxFansNum"))
    normalized["min_fans"] = int(min_fans_value) if min_fans_value not in (None, "") else None
    normalized["max_fans"] = int(max_fans_value) if max_fans_value not in (None, "") else None
    normalized["has_email"] = bool(first_non_empty(brief.get("has_email"), search.get("hasEmail"), True))
    normalized["sender_name"] = first_non_empty(brief.get("sender_name"), outreach.get("senderName"))
    normalized["offer_type"] = str(first_non_empty(brief.get("offer_type"), outreach.get("cooperationType"), "sample")).strip() or "sample"
    normalized["language"] = language_codes[0] if language_codes else "en"
    normalized["target_market"] = first_non_empty(brief.get("target_market"), product.get("targetMarket"), search.get("region"))
    normalized["cta_goal"] = first_non_empty(brief.get("cta_goal"), outreach.get("ctaGoal"))
    normalized["brand_name"] = first_non_empty(brief.get("brand_name"), product.get("brand"), product.get("brandName"))
    normalized["deliverable"] = first_non_empty(brief.get("deliverable"), outreach.get("deliverable"))
    normalized["compensation"] = first_non_empty(brief.get("compensation"), outreach.get("compensation"))
    normalized["selected_blogger_ids"] = first_non_empty(brief.get("selected_blogger_ids"), brief.get("selectedBloggerIds"))
    normalized["selected_ranks"] = first_non_empty(brief.get("selected_ranks"), brief.get("selectedRanks"))
    normalized["selection_rule"] = _normalize_selection_rule(
        first_non_empty(brief.get("selection_rule"), brief.get("selectionRule"))
    )
    normalized["all_search_results_selected"] = bool(
        first_non_empty(brief.get("all_search_results_selected"), brief.get("allSearchResultsSelected"), False)
    )
    if not normalized["selection_rule"] and normalized["all_search_results_selected"]:
        normalized["selection_rule"] = {"type": "all_search_results"}
    normalized["semantic_mode"] = first_non_empty(brief.get("semantic_mode"), "mock")
    normalized["debug"] = bool(first_non_empty(brief.get("debug"), False))
    normalized["host_analysis"] = first_non_empty(
        brief.get("host_analysis"),
        brief.get("hostAnalysis"),
        brief.get("understanding"),
        brief.get("model_analysis"),
        brief.get("modelAnalysis"),
    )
    normalized["host_drafts"] = first_non_empty(
        brief.get("host_drafts"),
        brief.get("hostDrafts"),
        brief.get("hostEmailDrafts"),
        brief.get("emailModelDrafts"),
        outreach.get("hostDrafts"),
        outreach.get("hostEmailDrafts"),
        outreach.get("emailModelDrafts"),
    )
    normalized["email_model_drafts"] = first_non_empty(
        normalized.get("host_drafts"),
        brief.get("email_model_drafts"),
        brief.get("emailModelDrafts"),
    )
    normalized["reply_model_analysis"] = first_non_empty(
        brief.get("reply_model_analysis"),
        brief.get("replyModelAnalysis"),
        brief.get("conversationAnalysis"),
    )
    normalized["require_reply_model_analysis"] = bool(
        first_non_empty(brief.get("require_reply_model_analysis"), brief.get("requireReplyModelAnalysis"), False)
    )
    normalized["auto_reply_policy"] = first_non_empty(brief.get("auto_reply_policy"), inbox.get("autoReplyPolicy"))
    normalized["draft_policy"] = first_non_empty(brief.get("draft_policy"), brief.get("draftPolicy")) or {}
    normalized["scheduler"] = first_non_empty(brief.get("scheduler"), {}) or {}

    if not normalized.get("model_analysis"):
        normalized["model_analysis"] = normalized.get("host_analysis") or {
            "product": {
                "productName": product_name or "",
                "productType": product.get("category") or product.get("productType"),
                "productSubtype": product.get("productSubtype"),
                "categoryForms": product.get("categoryForms") or [],
                "coreBenefits": selling_points[:8],
                "functions": product.get("functions") or [],
                "targetAreas": product.get("targetAreas") or [],
                "targetAudiences": product.get("targetAudiences") or [],
                "price": product.get("price"),
                "priceTier": product.get("priceTier") or "unknown",
                "brand": normalized.get("brand_name"),
                "sourceUrl": product_url,
                "pageTitle": product_name or "",
                "features": product.get("features") or [],
            },
            "marketing": {
                "platformPreference": [platform],
                "creatorTypes": product.get("creatorTypes") or [],
                "creatorIntent": product.get("creatorIntent") or [],
                "contentAngles": product.get("contentAngles") or search.get("contentAngles") or [],
            },
            "constraints": {
                "regions": region_codes or [],
                "languages": language_codes or ["en"],
                "minFansNum": normalized["min_fans"],
                "maxFansNum": normalized["max_fans"],
                "hasEmail": normalized["has_email"],
            },
            "clarificationsNeeded": [],
        }

    if not normalized.get("host_analysis") and normalized.get("model_analysis"):
        normalized["host_analysis"] = normalized.get("model_analysis")

    return normalized


def validate_brief(brief: dict[str, Any]) -> dict[str, Any]:
    """Validate campaign brief."""
    errors = []
    warnings = []

    if not brief.get("input"):
        errors.append("input is required")
    if not brief.get("product_name"):
        warnings.append("product_name is recommended")

    scheduled_validation = validate_scheduled_execution_brief(brief)
    if scheduled_validation.get("forbiddenFields"):
        warnings.append(
            "scheduled execution brief contains legacy search overrides; these fields should be removed before scheduled_cycle execution"
        )

    return {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "scheduledExecutionValidation": scheduled_validation,
    }


def get_missing_fields(brief: dict[str, Any]) -> list[str]:
    """Get list of missing required fields."""
    missing = []
    required = ["input", "platform"]
    for field in required:
        if not brief.get(field):
            missing.append(field)
    return missing
