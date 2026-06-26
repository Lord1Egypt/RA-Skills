#!/usr/bin/env python3
"""
Internal WotoHub campaign orchestrator.

Architecture split:
- semantic_layer.py          → model understanding / semantic contract
- search_strategy.py         → lightweight search strategy generation
- build_search_payload.py     → deterministic payload compilation
- claw_search.py              → API execution + fallback search variants
- this file                   → orchestration only

Public users should run the root entrypoint: ../run_campaign.py
"""
from __future__ import annotations

import argparse
import copy
import json
import logging
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Optional

import claw_search
import generate_outreach_emails
import product_resolve
from brief_resolver import resolve_campaign_brief

# Configure logging
import os
logger = logging.getLogger("wotohub")
_log_level = os.environ.get("WOTOHUB_LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, _log_level, logging.INFO))
if not logger.handlers:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(handler)

try:
    import search_cache
except ImportError:
    search_cache = None  # type: ignore

try:
    import semantic_matcher
except ImportError:
    semantic_matcher = None  # type: ignore

from build_search_payload import (
    load_categories,
    load_region_keywords,
    load_lang_keywords,
    DEFAULT_SEARCH_PAGE_SIZE,
    MAX_SEARCH_PAGE_SIZE,
    build_payload_from_context,
    focus_advanced_keywords,
)
from context_schema import normalize_context
from common import get_token
from error_taxonomy import api_error_to_structured, build_error
from semantic_layer import SemanticLayer


def _is_url(value: str) -> bool:
    return value.strip().startswith(("http://", "https://"))


URL_NOISE_TOKENS = {
    "products", "shop", "source", "detail", "fit", "x27", "amp", "nbsp",
    "quot", "th", "dp", "product_detail", "www", "http", "https",
}


def normalize_search_keywords(keywords: list[Any]) -> dict[str, Any]:
    before = copy.deepcopy(keywords or [])
    cleaned: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in keywords or []:
        if isinstance(item, dict):
            value = str(item.get("value", "")).strip()
            exclude = bool(item.get("exclude", False))
        else:
            value = str(item).strip()
            exclude = False
        if not value:
            continue
        low = value.lower().strip()
        if low in URL_NOISE_TOKENS or (len(low) < 3 and re.fullmatch(r"[a-z]+", low)):
            continue
        normalized = re.sub(r"\s+", " ", low)
        if normalized and normalized not in seen:
            seen.add(normalized)
            cleaned.append({"value": value, "exclude": exclude})

    focused = focus_advanced_keywords(cleaned, limit=5)
    focused_values = {re.sub(r"\s+", " ", str(item.get("value", "")).strip().lower()) for item in focused}
    removed = []
    for item in cleaned:
        normalized = re.sub(r"\s+", " ", str(item.get("value", "")).strip().lower())
        if normalized and normalized not in focused_values:
            removed.append(item.get("value"))
    return {"before": before, "after": focused, "removed": removed}


def _make_analysis_summary(product_info: dict) -> dict:
    return {
        "productName": product_info.get("productName", ""),
        "detectedForms": product_info.get("forms", []) or product_info.get("categoryForms", []),
        "detectedFunctions": product_info.get("functions", []),
        "targetAudiences": product_info.get("targetAudiences", []),
        "platformHints": [product_info.get("platform", "tiktok")],
        "regionHints": product_info.get("regions", ["us"]) or ["us"],
        "languageHints": product_info.get("languages", ["en"]) or ["en"],
        "keywordHints": product_info.get("keywordHints", []),
        "priceHint": product_info.get("price"),
    }


def _build_standard_search_payload_from_semantics(
    *,
    user_input: str,
    model_analysis: Optional[dict[str, Any]],
    product_summary: Optional[dict[str, Any]],
    platform: str,
    min_fans: int,
    max_fans: int,
    has_email: bool,
    page_size: int,
    target_market: Optional[str]= None,
) -> dict[str, Any]:
    model_analysis = model_analysis or {}
    product_summary = product_summary or {}
    constraints = model_analysis.get("constraints") or {}
    marketing = model_analysis.get("marketing") or {}
    product = model_analysis.get("product") or {}

    target_markets: list[str] = []
    if target_market:
        text = str(target_market).strip().lower()
        if text:
            target_markets.append(text)
    for item in (constraints.get("regions") or []):
        text = str(item or "").strip().lower()
        if text and text not in target_markets:
            target_markets.append(text)

    languages: list[str] = []
    for item in (constraints.get("languages") or []):
        text = str(item or "").strip().lower()
        if text and text not in languages:
            languages.append(text)

    features: list[str] = []
    for item in [
        *(product_summary.get("sellingPoints") or []),
        *(product.get("coreBenefits") or []),
        *(product.get("features") or []),
    ]:
        text = str(item or "").strip()
        if text and text not in features:
            features.append(text)

    creator_types: list[str] = []
    for item in (marketing.get("creatorTypes") or []):
        text = str(item or "").strip()
        if text and text not in creator_types:
            creator_types.append(text)

    ctx = normalize_context({
        "intent": {"primaryTask": "search"},
        "productSignals": {
            "rawInput": user_input,
            "urls": [user_input] if _is_url(user_input) else [],
            "productName": product.get("productName") or product_summary.get("productName"),
            "brand": product.get("brand") or product_summary.get("brand"),
            "category": product.get("productSubtype") or product.get("productType") or product_summary.get("productTypeHint"),
            "features": features,
            "useCases": product.get("functions") or product_summary.get("detectedFunctions") or [],
        },
        "marketingContext": {
            "targetMarkets": target_markets,
            "platforms": [platform] if platform else (marketing.get("platformPreference") or []),
            "creatorTypes": creator_types,
            "followerRange": {
                "min": min_fans or constraints.get("minFansNum"),
                "max": max_fans or constraints.get("maxFansNum"),
            },
            "languages": languages,
        },
        "resolvedArtifacts": {
            "modelAnalysis": model_analysis,
            "productSummary": product_summary,
        },
        "meta": {
            "usedHostModel": bool(model_analysis),
            "usedFallback": not bool(model_analysis),
            "analysisPath": "run_campaign_standard_compiler",
        },
    })

    payload = build_payload_from_context(ctx)
    payload.setdefault("pageNum", 1)
    payload.setdefault("pageSize", min(max(int(page_size or DEFAULT_SEARCH_RESULT_LIMIT), 1), MAX_SEARCH_PAGE_SIZE))
    if has_email:
        payload["hasEmail"] = True
    if min_fans:
        payload["minFansNum"] = min_fans
    if max_fans:
        payload["maxFansNum"] = max_fans
    return claw_search.normalize_search_payload(payload)


def fallback_analysis_from_input(
    user_input: str,
    token: Optional[str],
    platform: str,
    min_fans: int,
    max_fans: int,
    has_email: bool,
    exclude_contacted: bool,
    page_size: int,
    semantic_mode: str,
    retry_fallbacks: bool,
    debug: bool,
    target_market: Optional[str]= None,
) -> dict[str, Any]:
    resolved: dict[str, Any]
    if _is_url(user_input):
        resolved = product_resolve.resolve_product(user_input, mode="url", timeout=20, debug=debug)
        if ((resolved or {}).get("fallback") or {}).get("active"):
            analysis = resolved.get("analysis", {})
            return {
                "success": False,
                "needsUserInput": True,
                "fallback": resolved.get("fallback"),
                "resolved": resolved,
                "analysis": analysis,
                "productSummary": resolved.get("productSummary", {}),
                "payload": None,
            }
    else:
        resolved = product_resolve.resolve_product(user_input, mode="text")

    analysis = (resolved or {}).get("analysis", {})
    if ((resolved or {}).get("fallback") or {}).get("active"):
        return {
            "success": False,
            "needsUserInput": True,
            "fallback": resolved.get("fallback"),
            "resolved": resolved,
            "analysis": analysis,
            "productSummary": resolved.get("productSummary", {}),
            "payload": None,
        }
    product_summary = resolved.get("productSummary", {})
    payload = _build_standard_search_payload_from_semantics(
        user_input=user_input,
        model_analysis=analysis,
        product_summary=product_summary,
        platform=platform,
        min_fans=min_fans,
        max_fans=max_fans,
        has_email=has_email,
        page_size=page_size,
        target_market=target_market,
    )
    return {
        "resolved": resolved,
        "analysis": analysis,
        "productSummary": product_summary,
        "payload": payload,
        "payloadResult": {"payload": payload, "matchedCategories": []},
        "semanticBoost": {},
        "urlCleaning": resolved.get("urlCleaning"),
        "urlModelInput": resolved.get("urlModelInput"),
    }


def merge_model_and_fallback_payload(model_payload: dict, fallback_payload: dict) -> dict:
    merged = copy.deepcopy(model_payload)
    for key, value in (fallback_payload or {}).items():
        if merged.get(key) in (None, '', [], {}):
            merged[key] = copy.deepcopy(value)
    return claw_search.normalize_search_payload(merged)


def _parallel_search(payloads: list[dict[str, Any]], token: Optional[str], max_workers: int = 3) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(claw_search.execute_search, claw_search.claw_search_path() if token else claw_search.open_search_path(), token, p): p for p in payloads}
        for fut in as_completed(futures):
            try:
                r = fut.result()
                if r.get("result", {}).get("code") in {0, "0", 200, "200"}:
                    results.append(r)
            except Exception:
                pass
    return results


def _best_search_result(results: list[dict[str, Any]]) -> dict[str, Any]:
    if not results:
        return {"result": {"code": -1, "message": "All searches failed", "data": None}}
    scored = []
    for r in results:
        data = r.get("result", {}).get("data") or {}
        blogger_list = None
        for key in ("bloggerList", "records", "list", "rows", "dataList"):
            if isinstance(data.get(key), list):
                blogger_list = data[key]
                break
        if not blogger_list:
            continue
        count = len(blogger_list)
        avg_match_score = sum(b.get("matchScore", 0) for b in blogger_list) / count if count > 0 else 0
        scored.append((avg_match_score, count, r))
    if not scored:
        return {"result": {"code": -1, "message": "All searches returned empty results", "data": None}}
    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return scored[0][2]


def _build_email_preview(emails: list[dict[str, Any]]) -> dict[str, Any]:
    if not emails:
        text = "未生成可发送的邮件预览"
        return {"count": 0, "summary": text, "markdownText": text, "plainText": text, "displayText": text}
    preview_items = emails[:3]
    summary = f"已生成 {len(emails)} 封邮件，先展示前 {len(preview_items)} 封预览"
    blocks = []
    for idx, mail in enumerate(preview_items, 1):
        blocks.append(
            f"### {idx}. {mail.get('nickname') or '未知达人'}\n"
            f"- 主题：{mail.get('subject') or '-'}\n"
            f"- 原始链接：{mail.get('link') or '-'}\n"
            f"- WotoHub分析：{mail.get('wotohubLink') or '-'}\n\n"
            f"**正文预览：**\n\n{mail.get('body') or '-'}"
        )
    markdown_text = summary + "\n\n" + "\n\n---\n\n".join(blocks)
    return {"count": len(emails), "summary": summary, "markdownText": markdown_text, "plainText": markdown_text, "displayText": markdown_text}


def _minimal_campaign_brief_check(product_summary: dict[str, Any], sender_name: Optional[str]= None, offer_type: Optional[str]= None) -> dict[str, Any]:
    missing: list[str] = []
    if not (product_summary.get("productName") or "").strip():
        missing.append("productName")
    if not sender_name or not sender_name.strip():
        missing.append("senderName")
    if not offer_type or not str(offer_type).strip():
        missing.append("offerType")
    return {
        "ok": len(missing) == 0,
        "missing": missing,
        "nextStep": "补齐最小 campaign brief：产品名、邮件署名、合作方式（sample / paid / affiliate）。",
    }


def _build_brief_fill_template(campaign_brief: Optional[dict[str, Any]], missing_required: Optional[list[str]]) -> str:
    brief = campaign_brief or {}
    missing = [str(x).strip() for x in (missing_required or []) if str(x).strip()]
    ordered_fields = ["productName", "senderName", "offerType"]
    field_values = {
        "productName": str(brief.get("productName") or "").strip(),
        "senderName": str(brief.get("senderName") or brief.get("signoff") or "").strip(),
        "offerType": str(brief.get("offerType") or "").strip(),
    }
    lines = ["请直接补齐下面这几个字段（没有的留空也行，我会继续接着补）："]
    for field in ordered_fields:
        prefix = "*" if field in missing else "-"
        value = field_values.get(field, "")
        lines.append(f"{prefix} {field}: {value}")
    lines.append("可直接回复示例：senderName: Alice / offerType: sample")
    return "\n".join(lines)


DEFAULT_OUTREACH_EMAIL_LIMIT = 200
DEFAULT_SEARCH_RESULT_LIMIT = DEFAULT_SEARCH_PAGE_SIZE


def _select_email_targets(search_output: dict[str, Any], selected_blogger_ids: Optional[list[str]]= None, selected_ranks: Optional[list[int]]= None, selection_rule: Optional[dict[str, Any]]= None, all_search_results_selected: bool = False, exclude_blogger_ids: Optional[list[str]]= None, max_items: int = DEFAULT_OUTREACH_EMAIL_LIMIT) -> list[dict[str, Any]]:
    def _blogger_id(item: dict[str, Any]) -> str:
        return str(item.get("bEsId") or item.get("besId") or item.get("bloggerId") or item.get("id") or "")

    def _to_int(value: Any, default: int = 0) -> int:
        try:
            if value in (None, ""):
                return default
            return int(float(value))
        except Exception:
            return default

    def _has_email(item: dict[str, Any]) -> bool:
        raw = item.get("hasEmail")
        if isinstance(raw, bool):
            return raw
        if raw in (1, "1", "true", "True", "yes", "YES"):
            return True
        if raw in (0, "0", "false", "False", "no", "NO"):
            return False
        return bool(item.get("email") or item.get("emailAddress"))

    search_data = search_output.get("result", {}) if isinstance(search_output, dict) else {}
    blogger_list: list[dict[str, Any]] = []
    data = search_data.get("data") if isinstance(search_data, dict) else None
    if isinstance(data, dict):
        for key in ("bloggerList", "records", "list", "rows", "dataList"):
            if isinstance(data.get(key), list):
                blogger_list = data[key]
                break
    elif isinstance(data, list):
        blogger_list = data

    exclude_set = {str(x) for x in (exclude_blogger_ids or []) if str(x).strip()}
    if exclude_set:
        blogger_list = [b for b in blogger_list if _blogger_id(b) not in exclude_set]

    if selected_blogger_ids:
        selected_set = {str(x) for x in selected_blogger_ids if str(x).strip()}
        out = []
        for item in blogger_list:
            if _blogger_id(item) in selected_set:
                out.append(item)
        return out[:max_items]

    if selected_ranks:
        out = []
        for rank in selected_ranks:
            idx = int(rank) - 1
            if 0 <= idx < len(blogger_list):
                out.append(blogger_list[idx])
        return out[:max_items]

    rule = selection_rule or {}
    rule_type = str(rule.get("type") or "").strip().lower()
    if not (rule_type == "top_n" or rule_type == "all_search_results" or all_search_results_selected):
        return blogger_list[:max_items]

    filtered = list(blogger_list)
    filters = rule.get("filters") or {}
    min_followers = _to_int(filters.get("minFollowers"), default=0)
    max_followers = _to_int(filters.get("maxFollowers"), default=0)
    require_email = filters.get("hasEmail")

    if min_followers > 0:
        filtered = [item for item in filtered if _to_int(item.get("fansNum"), default=0) >= min_followers]
    if max_followers > 0:
        filtered = [item for item in filtered if _to_int(item.get("fansNum"), default=0) <= max_followers]
    if require_email is True:
        filtered = [item for item in filtered if _has_email(item)]

    sort_rules = rule.get("sort") or []
    for sort_rule in reversed(sort_rules if isinstance(sort_rules, list) else []):
        field = str((sort_rule or {}).get("field") or "").strip().lower()
        order = str((sort_rule or {}).get("order") or "asc").strip().lower()
        reverse = order == "desc"
        if field == "followers":
            filtered.sort(key=lambda item: _to_int(item.get("fansNum"), default=0), reverse=reverse)

    if rule_type == "all_search_results" or all_search_results_selected:
        return filtered[:max_items]
    if rule_type == "top_n":
        try:
            top_n = int(rule.get("top_n") or rule.get("topN") or 0)
        except Exception:
            top_n = 0
        if top_n > 0:
            return filtered[: min(top_n, max_items)]

    return filtered[:max_items]


def _extract_send_target_creator_ids(items: Optional[list[dict[str, Any]]]) -> list[str]:
    ids: list[str] = []
    for item in (items or []):
        creator_id = item.get("bloggerId") or item.get("besId") or item.get("bEsId") or item.get("id")
        if creator_id in (None, ""):
            continue
        creator_id = str(creator_id)
        if creator_id not in ids:
            ids.append(creator_id)
    return ids


def _generate_emails(search_output: dict[str, Any], product_summary: dict[str, Any], sender_name: Optional[str]= None, offer_type: str = "sample", selected_blogger_ids: Optional[list[str]]= None, selected_ranks: Optional[list[int]]= None, selection_rule: Optional[dict[str, Any]]= None, all_search_results_selected: bool = False, exclude_blogger_ids: Optional[list[str]]= None, email_language: str = "en", model_drafts: Optional[dict]= None, allow_fallback_drafts: bool = False, max_items: int = DEFAULT_OUTREACH_EMAIL_LIMIT) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    product_for_email: dict[str, Any] = {
        "productName": product_summary.get("productName", "unknown product"),
        "sellingPoints": product_summary.get("sellingPoints", []),
    }
    blogger_list = _select_email_targets(
        search_output,
        selected_blogger_ids=selected_blogger_ids,
        selected_ranks=selected_ranks,
        selection_rule=selection_rule,
        all_search_results_selected=all_search_results_selected,
        exclude_blogger_ids=exclude_blogger_ids,
        max_items=max_items,
    )

    emails: list[dict[str, Any]] = []
    for item in blogger_list:
        try:
            blogger_id = item.get("bEsId") or item.get("besId") or item.get("bloggerId") or item.get("id") or ""
            matched_draft = generate_outreach_emails._match_model_draft(model_drafts, item) if model_drafts else None
            if matched_draft and matched_draft.get("subject") and (matched_draft.get("htmlBody") or matched_draft.get("body") or matched_draft.get("plainTextBody")):
                draft_blogger_id = str(matched_draft.get("bloggerId") or matched_draft.get("besId") or matched_draft.get("bEsId") or "")
                item_nickname = str(item.get("nickname") or "").strip()
                if not draft_blogger_id:
                    continue
                if blogger_id and draft_blogger_id != str(blogger_id):
                    continue
                raw_html = matched_draft.get("htmlBody")
                raw_fallback_text = matched_draft.get("body") or matched_draft.get("plainTextBody") or ""
                if raw_html and generate_outreach_emails.validate_email_html(raw_html):
                    html_body = generate_outreach_emails.normalize_html_body(raw_html)
                else:
                    html_body = generate_outreach_emails.normalize_html_body(
                        generate_outreach_emails.plain_text_to_html(raw_html or raw_fallback_text)
                    )
                plain_text_body = matched_draft.get("plainTextBody") or generate_outreach_emails.html_to_plain_text(html_body)
                subject = str(matched_draft.get("subject") or "").strip()
                emails.append({
                    "bloggerId": blogger_id,
                    "nickname": item_nickname,
                    "bloggerName": item.get("bloggerName") or item_nickname,
                    "channelName": item.get("channelName") or item_nickname,
                    "emailAvailable": bool(item.get("hasEmail")),
                    "subject": subject,
                    "body": plain_text_body,
                    "htmlBody": html_body,
                    "plainTextBody": plain_text_body,
                    "wordCount": len(str(plain_text_body).split()),
                    "fansNum": item.get("fansNum"),
                    "followers": item.get("fansNum"),
                    "link": item.get("link"),
                    "wotohubLink": f"https://www.wotohub.com/kocNewDetail?id={blogger_id}" if blogger_id else None,
                    "tagList": item.get("tagList") or [],
                    "platform": item.get("platform"),
                    "country": item.get("country"),
                    "language": matched_draft.get("language") or item.get("language") or item.get("blogLang") or email_language,
                    "category": item.get("category"),
                    "contentStyle": item.get("contentStyle") or item.get("category"),
                    "recentTopics": item.get("recentTopics") or item.get("tagList") or [],
                    "style": matched_draft.get("style") or "model-first",
                    "draftSource": generate_outreach_emails._draft_source_label(matched_draft) or "host-model",
                })
                continue

            if not allow_fallback_drafts:
                continue
            email = generate_outreach_emails.generate_email(item, product_for_email, cooperation=offer_type, lang=email_language, sender_name=sender_name)
            emails.append({
                "bloggerId": blogger_id,
                "nickname": item.get("nickname"),
                "bloggerName": item.get("bloggerName") or item.get("nickname"),
                "channelName": item.get("channelName") or item.get("nickname"),
                "emailAvailable": bool(item.get("hasEmail")),
                "subject": email["subject"],
                "body": email["plainTextBody"],
                "htmlBody": email["htmlBody"],
                "plainTextBody": email["plainTextBody"],
                "wordCount": email["wordCount"],
                "fansNum": item.get("fansNum"),
                "followers": item.get("fansNum"),
                "link": item.get("link"),
                "wotohubLink": f"https://www.wotohub.com/kocNewDetail?id={blogger_id}" if blogger_id else None,
                "tagList": item.get("tagList") or [],
                "platform": item.get("platform"),
                "country": item.get("country"),
                "language": item.get("language") or item.get("blogLang") or email_language,
                "category": item.get("category"),
                "contentStyle": item.get("contentStyle") or item.get("category"),
                "recentTopics": item.get("recentTopics") or item.get("tagList") or [],
                "style": "fallback-light",
                "draftSource": "fallback-script",
            })
        except Exception as e:
            logger.warning("Skip email generation for blogger %s (%s): %s", item.get("nickname") or "-", blogger_id or "-", e)
    recommendations = claw_search.enrich_recommendations(search_output)
    return emails, recommendations


def run_campaign(
    user_input: str,
    token: Optional[str]= None,
    platform: str = "tiktok",
    min_fans: int = 10000,
    max_fans: int = 500000,
    has_email: bool = True,
    exclude_contacted: bool = True,
    page_size: int = 50,
    semantic_mode: str = "mock",
    retry_fallbacks: bool = True,
    parallel_strategies: bool = False,
    debug: bool = False,
    model_analysis: Optional[dict]= None,
    url_model_analysis: Optional[dict]= None,
    prefer_model_analysis: bool = True,
    sender_name: Optional[str]= None,
    include_email_preview: bool = False,
    offer_type: str = "sample",
    email_language: str = "en",
    selected_blogger_ids: Optional[list[str]]= None,
    selected_ranks: Optional[list[int]]= None,
    selection_rule: Optional[dict[str, Any]]= None,
    all_search_results_selected: bool = False,
    email_model_drafts: Optional[dict]= None,
    allow_fallback_drafts: bool = False,
    brand_name: Optional[str]= None,
    deliverable: Optional[str]= None,
    compensation: Optional[str]= None,
    target_market: Optional[str]= None,
    cta_goal: Optional[str]= None,
    exclude_blogger_ids: Optional[list[str]]= None,
) -> dict[str, Any]:
    step = ""
    try:
        url_cleaning = None
        keyword_normalization = None
        url_model_input = None
        url_model_analysis_used = False
        resolved: dict[str, Any] = {}
        analysis: dict[str, Any] = {}
        product_summary_dict: dict[str, Any] = {}
        # CLI compatibility path: prefer caller-supplied analysis. If none is
        # provided, opportunistically resolve local text/URL input into
        # model_analysis so this standalone script can still exercise the
        # understanding-first flow. This should not be interpreted as permission
        # for the main runtime to skip host understanding on core tasks.
        _cli_analysis = url_model_analysis if _is_url(user_input) and url_model_analysis is not None else model_analysis
        effective_model_analysis = _cli_analysis
        if _is_url(user_input) and _cli_analysis is not None:
            url_model_analysis_used = True
        if prefer_model_analysis and effective_model_analysis is None and user_input.strip():
            resolve_mode = "url" if _is_url(user_input) else "text"
            resolved = product_resolve.resolve_product(user_input, mode=resolve_mode, timeout=12, debug=debug)
            if not ((resolved.get("fallback") or {}).get("active")) and resolved.get("analysis"):
                effective_model_analysis = resolved.get("analysis")
                analysis = resolved.get("analysis") or {}
                product_summary_dict = resolved.get("productSummary") or {}
                url_cleaning = resolved.get("urlCleaning")
                url_model_input = resolved.get("urlModelInput")
        use_model = prefer_model_analysis and effective_model_analysis is not None
        missing_semantics_pause = {"pause": False}

        if use_model:
            step = "model_payload_compile"
            model_payload = _build_standard_search_payload_from_semantics(
                user_input=user_input,
                model_analysis=effective_model_analysis,
                product_summary=product_summary_dict,
                platform=platform,
                min_fans=min_fans,
                max_fans=max_fans,
                has_email=has_email,
                page_size=page_size,
                target_market=target_market,
            )
            validation = {"ok": True, "missing": [], "warnings": []}
            product_summary_dict = product_summary_dict or {
                "productName": (effective_model_analysis or {}).get("product", {}).get("productName") or "",
                "sellingPoints": (effective_model_analysis or {}).get("product", {}).get("coreBenefits") or [],
                "detectedForms": (effective_model_analysis or {}).get("product", {}).get("categoryForms") or [],
            }

            if not validation["ok"]:
                pause_result = {"pause": False, "reason": ""}
                if pause_result["pause"]:
                    return {
                        **build_error(
                            "MODEL_CLARIFICATION_REQUIRED",
                            pause_result["reason"],
                            details={
                                "clarificationsNeeded": (effective_model_analysis or {}).get("clarificationsNeeded", []),
                                "criticalFields": pause_result["criticalFields"],
                                "payloadPreview": model_payload,
                            },
                            retryable=False,
                            next_step="先补充关键搜索条件，再执行搜索。",
                        ),
                        "needsClarification": True,
                        "modelAnalysisUsed": True,
                        "modelAnalysisValidation": validation,
                        "payloadSource": "model",
                        "urlModelAnalysisUsed": url_model_analysis_used,
                    }

            missing_semantics_pause = {"pause": False, "reason": "", "missingSemantics": [], "detectedBusinessIntent": ""}
            if missing_semantics_pause["pause"]:
                existing = (effective_model_analysis or {}).get("clarificationsNeeded", [])
                enhanced = list(existing)
                return {
                    **build_error(
                        "PRODUCT_CONTEXT_MISSING",
                        missing_semantics_pause["reason"],
                        details={
                            "missingSemantics": missing_semantics_pause["missingSemantics"],
                            "detectedBusinessIntent": missing_semantics_pause["detectedBusinessIntent"],
                            "clarificationsNeeded": enhanced,
                            "payloadPreview": model_payload,
                        },
                        retryable=False,
                        next_step="补充产品名称、品类或链接，以及目标市场。",
                    ),
                    "needsClarification": True,
                    "modelAnalysisUsed": True,
                    "modelAnalysisValidation": validation,
                    "payloadSource": "model",
                    "urlModelAnalysisUsed": url_model_analysis_used,
                }

            if not validation["ok"]:
                step = "fallback_payload_compile"
                fb_result = fallback_analysis_from_input(user_input, token, platform, min_fans, max_fans, has_email, exclude_contacted, page_size, semantic_mode, retry_fallbacks, debug, target_market=target_market)
                if fb_result.get("success") is False and fb_result.get("error"):
                    return fb_result
                fb_payload = fb_result.get("payload", {})
                payload = merge_model_and_fallback_payload(model_payload, fb_payload)
                resolved = fb_result.get("resolved", {})
                analysis = fb_result.get("analysis", {})
                if not product_summary_dict.get("productName"):
                    product_summary_dict = fb_result.get("productSummary", product_summary_dict)
                semantic_boost = fb_result.get("semanticBoost", {})
                url_cleaning = fb_result.get("urlCleaning")
                url_model_input = fb_result.get("urlModelInput")
                payload_source = "model+fallback"
                payload_result_extra = fb_result.get("payloadResult", {})
            else:
                payload = model_payload
                if not resolved:
                    resolved = {"resolvedProduct": None}
                if not analysis:
                    analysis = {}
                semantic_boost = {}
                payload_source = "model"
                payload_result_extra = {}
                if _is_url(user_input) and not url_model_input:
                    resolved_url = product_resolve.resolve_product(user_input, mode="url", timeout=12, debug=debug)
                    if not (resolved_url.get("fallback") or {}).get("active"):
                        resolved = resolved or resolved_url
                        product_summary_dict = product_summary_dict or resolved_url.get("productSummary") or product_summary_dict
                        url_cleaning = resolved_url.get("urlCleaning")
                        url_model_input = resolved_url.get("urlModelInput")
        else:
            step = "fallback_payload_compile"
            fb_result = fallback_analysis_from_input(user_input, token, platform, min_fans, max_fans, has_email, exclude_contacted, page_size, semantic_mode, retry_fallbacks, debug, target_market=target_market)
            if fb_result.get("needsUserInput"):
                return {
                    **build_error(
                        "PRODUCT_INFO_REQUIRED",
                        (fb_result.get("fallback") or {}).get("userPrompt") or "需要补充商品信息后才能继续。",
                        details={
                            "fallback": fb_result.get("fallback"),
                            "resolved": fb_result.get("resolved"),
                            "productSummary": fb_result.get("productSummary"),
                            "replyTemplate": (fb_result.get("fallback") or {}).get("suggestedReplyTemplate"),
                        },
                        retryable=False,
                        next_step="请按提示补充产品名称、核心卖点、价格区间、目标市场、适合的达人类型中的任意 2-4 项。",
                    ),
                    "needsUserInput": True,
                    "fallback": fb_result.get("fallback"),
                    "payloadSource": "fallback",
                    "analysisPath": "fallback-user-guided",
                }
            if fb_result.get("success") is False and fb_result.get("error"):
                return fb_result
            payload = fb_result.get("payload", {})
            resolved = fb_result.get("resolved", {})
            analysis = fb_result.get("analysis", {})
            product_summary_dict = fb_result.get("productSummary", {})
            semantic_boost = fb_result.get("semanticBoost", {})
            url_cleaning = fb_result.get("urlCleaning")
            url_model_input = fb_result.get("urlModelInput")
            payload_source = "fallback"
            validation = {"ok": True, "missing": [], "warnings": []}
            payload_result_extra = fb_result.get("payloadResult", {})

        step = "search"
        keyword_normalization = normalize_search_keywords(payload.get("advancedKeywordList", []))
        payload["advancedKeywordList"] = keyword_normalization["after"]
        payload = claw_search.normalize_search_payload(payload)
        if token:
            payload["searchFilterList"] = ["THIS_UNTOUCH"] if exclude_contacted else []
        logger.info(f"Executing search with platform={payload.get('platform')}, keywords={len(payload.get('advancedKeywordList', []))}")
        cache_hit = False
        if search_cache is not None:
            try:
                cached = search_cache.cache_get(payload, token)
                if cached is not None:
                    search_output = cached
                    cache_hit = True
                else:
                    search_output = None
            except Exception:
                search_output = None
        else:
            search_output = None

        if not cache_hit:
            path = claw_search.claw_search_path() if token else claw_search.open_search_path()
            if parallel_strategies:
                strategies = payload_result_extra.get("semantic", {}).get("strategies", [])
                strategy_payloads = [s.get("payloadDraft", {}) for s in strategies][:3]
                all_payloads = [payload] + [{**payload, **sp} for sp in strategy_payloads if sp]
                parallel_results = _parallel_search(all_payloads[:4], token)
                search_output = _best_search_result(parallel_results)
            else:
                attempts = []
                first = claw_search.execute_search(path, token, payload)
                attempts.append({"label": "initial", "payload": payload, "result": first.get("result")})
                best = first
                if retry_fallbacks and not claw_search.is_search_success(first.get("result", {})):
                    fallback_variants = claw_search.build_error_driven_fallbacks(payload, first.get("result", {}))
                    if len(fallback_variants) > 1:
                        parallel_variants = fallback_variants[:3]
                        parallel_results = _parallel_search([v["payload"] for v in parallel_variants], token)
                        for variant in parallel_variants:
                            attempts.append({"label": variant["label"], "reason": variant["reason"], "payload": variant["payload"], "result": "parallel-dispatched"})
                        candidate_results = [first, *parallel_results]
                        best = _best_search_result(candidate_results)
                    else:
                        for variant in fallback_variants:
                            cur = claw_search.execute_search(path, token, variant["payload"])
                            attempts.append({"label": variant["label"], "reason": variant["reason"], "payload": variant["payload"], "result": cur.get("result")})
                            best = cur
                            if claw_search.is_search_success(cur.get("result", {})):
                                break
                search_output = dict(best)
                if debug:
                    search_output["attempts"] = attempts
            if search_cache is not None and search_output is not None:
                try:
                    search_cache.cache_set(payload, token, search_output)
                except Exception:
                    pass

        result_obj = search_output.get("result", {}) if isinstance(search_output, dict) else {}
        if not claw_search.is_search_success(result_obj):
            structured_error = api_error_to_structured(
                {"result": result_obj},
                context={"payload": payload},
            )
            return {
                **structured_error,
                "details": {
                    **(structured_error.get("details") or {}),
                    "apiResult": result_obj,
                },
                "modelAnalysisUsed": use_model,
                "modelAnalysisValidation": validation,
                "payloadSource": payload_source,
                "analysisPath": "model-first" if payload_source == "model" else ("model-first+fallback" if payload_source == "model+fallback" else "fallback-only"),
            }

        recommendations = claw_search.enrich_recommendations(search_output)
        if recommendations.get("count", 0) == 0:
            return {
                **build_error(
                    "SEARCH_NO_RESULTS",
                    "搜索执行成功，但未找到匹配红人。",
                    details={"payload": payload, "suggestions": recommendations.get("emptyState", {}).get("suggestions", [])},
                    retryable=True,
                    next_step="减少关键词数量、放宽类目/地区/邮箱要求后再试。",
                ),
                "modelAnalysisUsed": use_model,
                "modelAnalysisValidation": validation,
                "payloadSource": payload_source,
            }

        emails: list[dict[str, Any]] = []
        email_preview = {
            "count": 0,
            "summary": "已跳过邮件预览生成；如需继续，请在用户确认目标达人和署名后再生成。",
            "markdownText": "已跳过邮件预览生成；如需继续，请在用户确认目标达人和署名后再生成。",
            "plainText": "已跳过邮件预览生成；如需继续，请在用户确认目标达人和署名后再生成。",
            "displayText": "已跳过邮件预览生成；如需继续，请在用户确认目标达人和署名后再生成。",
        }
        if include_email_preview:
            step = "email_generation"
            if not selected_blogger_ids and not selected_ranks and not selection_rule and not all_search_results_selected:
                return {
                    **build_error(
                        "TARGET_SELECTION_REQUIRED",
                        "生成邮件前，必须先由用户指定目标达人。",
                        details={
                            "acceptedInputs": ["selected_blogger_ids", "selected_ranks", "selection_rule", "all_search_results_selected"],
                            "maxRecommended": 5,
                        },
                        retryable=False,
                        next_step="请让用户选择要生成邮件的达人，可传 bloggerId 列表、推荐序号列表，或显式指定全选当前搜索结果。",
                    ),
                    "needsTargetSelection": True,
                    "selectionGuide": "请先提供明确选择语义：可传 selected_ranks（如 [1,3,5]）、selected_blogger_ids（besId 列表）、selection_rule（如 {type: 'top_n', topN: 20}），或 all_search_results_selected=true 表示全选当前搜索结果。",
                    "payloadSource": payload_source,
                }
            brief_result = resolve_campaign_brief(
                product_summary=product_summary_dict,
                sender_name=sender_name,
                offer_type=offer_type,
                language=email_language,
                brand_name=brand_name,
                deliverable=deliverable,
                compensation=compensation,
                target_market=target_market,
                cta_goal=cta_goal,
            )
            if brief_result.get("needsUserInput"):
                return {
                    **build_error(
                        "CAMPAIGN_BRIEF_REQUIRED",
                        "生成达人邀约邮件前，必须先补齐关键 brief。",
                        details={
                            "missingRequired": brief_result.get("missingRequired", []),
                            "missingOptional": brief_result.get("missingOptional", []),
                            "suggestedQuestions": brief_result.get("suggestedQuestions", []),
                        },
                        retryable=False,
                        next_step="按 suggestedQuestions 追问缺失字段即可，不需要整张长表单。",
                    ),
                    "needsCampaignBrief": True,
                    "missingCampaignBriefFields": brief_result.get("missingRequired", []),
                    "campaignBrief": brief_result.get("campaignBrief"),
                    "briefFillTemplate": _build_brief_fill_template(
                        brief_result.get("campaignBrief"),
                        brief_result.get("missingRequired", []),
                    ),
                    "payloadSource": payload_source,
                    "analysisPath": "model-first" if payload_source == "model" else ("model-first+fallback" if payload_source == "model+fallback" else "fallback-only"),
                }
            if not email_model_drafts and not allow_fallback_drafts:
                return {
                    **build_error(
                        "HOST_DRAFTS_REQUIRED",
                        "正式邮件生成默认要求先提供宿主模型产出的 host drafts。",
                        details={
                            "acceptedInput": "email_model_drafts",
                            "allowFallbackDrafts": False,
                            "selectedBloggerCount": len(selected_blogger_ids or selected_ranks or []),
                            "selectionRule": selection_rule,
                            "allSearchResultsSelected": bool(all_search_results_selected),
                        },
                        retryable=False,
                        next_step="请先让宿主模型按目标达人生成 subject/htmlBody/plainTextBody，并通过 email_model_drafts 传入。",
                    ),
                    "needsHostDrafts": True,
                    "payloadSource": payload_source,
                    "analysisPath": "host-model-required",
                }
            emails, recommendations = _generate_emails(
                search_output,
                product_summary_dict,
                sender_name=sender_name,
                offer_type=offer_type,
                selected_blogger_ids=selected_blogger_ids,
                selected_ranks=selected_ranks,
                selection_rule=selection_rule,
                all_search_results_selected=all_search_results_selected,
                exclude_blogger_ids=exclude_blogger_ids,
                email_language=email_language,
                model_drafts=email_model_drafts,
                allow_fallback_drafts=allow_fallback_drafts,
            )
            email_preview = _build_email_preview(emails)
            logger.info(f"Generated {len(emails)} email previews for {len(recommendations.get('items', []))} influencers")
        else:
            logger.info("Email preview generation skipped (include_email_preview=False)")
            emails = []
            email_preview = {"count": 0, "summary": "邮件生成已跳过，等待用户确认目标达人后再生成"}


        analysis_path = "model-first" if payload_source == "model" else ("model-first+fallback" if payload_source == "model+fallback" else "fallback-only")
        analysis_input_type = "url" if _is_url(user_input) else "text"
        recommended_next_step = None
        if _is_url(user_input) and url_model_analysis is None and not url_model_analysis_used:
            recommended_next_step = "Generate url_model_analysis from urlModelInput before relying on fallback search. Pass --url-model-analysis-json with the model's schema output for best results."
        fallback_reason = None
        if payload_source == "model+fallback":
            if not validation["ok"]:
                fallback_reason = "missing_required_fields"
            elif missing_semantics_pause.get("pause"):
                fallback_reason = "missing_product_semantics"
        elif payload_source == "fallback":
            fallback_reason = "no_model_analysis_provided"

        result = {
            "success": True,
            "cacheHit": cache_hit,
            "modelAnalysisUsed": use_model,
            "urlModelAnalysisAvailable": url_model_analysis is not None,
            "urlModelAnalysisUsed": url_model_analysis_used,
            "modelAnalysisValidation": validation,
            "payloadSource": payload_source,
            "analysisPath": analysis_path,
            "analysisInputType": analysis_input_type,
            "fallbackReason": fallback_reason,
            "recommendedNextStep": recommended_next_step,
            "architecture": {
                "modelLayer": "semantic_layer.py",
                "semanticLayer": "search_strategy.py + build_search_payload.py",
                "payloadCompiler": "build_search_payload.py",
                "orchestrator": "scripts/run_campaign.py",
                "publicEntrypoint": "run_campaign.py",
            },
            "steps": {
                "product_resolve": {"step": "product_resolve", "success": True, "resolvedProduct": resolved.get("resolvedProduct") if isinstance(resolved, dict) else None},
                "build_payload": {"step": "build_payload", "success": True, "matchedCategories": payload_result_extra.get("matchedCategories", [])},
                "search": {"step": "search", "success": True, "bloggerCount": recommendations.get("count", 0)},
                "email_generation": {"step": "email_generation", "success": include_email_preview, "skipped": not include_email_preview, "emailCount": len(emails), "previewSummary": email_preview.get("summary")},
            },
            "core": {
                "productSummary": product_summary_dict,
                "payload": payload,
                "matchedCategories": payload_result_extra.get("matchedCategories", []),
                "recommendations": recommendations,
                "summary": recommendations.get("summary") if isinstance(recommendations, dict) else None,
                "markdownTable": recommendations.get("markdownTable") if isinstance(recommendations, dict) else None,
                "plainTextTable": recommendations.get("plainTextTable") if isinstance(recommendations, dict) else None,
                "displayText": recommendations.get("displayText") if isinstance(recommendations, dict) else None,
                "emails": emails,
                "emailPreview": email_preview,
                "emailPreviewText": email_preview.get("displayText"),
                "emailGenerationMode": ("model-first" if email_model_drafts else ("fallback-light" if allow_fallback_drafts else "host-drafts-required")) if include_email_preview else "deferred",
            },
            "artifacts": {
                "searchResult": search_output,
                "semanticBoost": semantic_boost or None,
                "urlCleaning": url_cleaning,
                "urlModelInput": url_model_input,
                "urlModelPromptPath": (url_model_input or {}).get("promptPath") if isinstance(url_model_input, dict) else None,
                "keywordNormalization": keyword_normalization,
            },
            "nextRecommendedAction": "先让用户确认目标达人名单；若要生成邀约邮件，请同时补齐 senderName 和 offerType；邮件建议先 prepare_only 预览，真正发信前再展示一次批量发送摘要并确认。",
        }
        result["productSummary"] = result["core"]["productSummary"]
        result["payload"] = result["core"]["payload"]
        result["matchedCategories"] = result["core"]["matchedCategories"]
        result["searchResult"] = result["artifacts"]["searchResult"]
        result["recommendations"] = result["core"]["recommendations"]
        result["summary"] = result["core"]["summary"]
        result["markdownTable"] = result["core"]["markdownTable"]
        result["plainTextTable"] = result["core"]["plainTextTable"]
        result["displayText"] = result["core"]["displayText"]
        result["nextStepGuidance"] = (result["core"].get("recommendations") or {}).get("nextStepGuidance") if isinstance(result["core"].get("recommendations"), dict) else None
        result["selectionHints"] = (result["core"].get("recommendations") or {}).get("selectionHints") if isinstance(result["core"].get("recommendations"), dict) else []
        result["emails"] = result["core"]["emails"]
        result["sendTargetCreatorIds"] = _extract_send_target_creator_ids(result["core"].get("emails") or [])
        result["emailPreview"] = result["core"]["emailPreview"]
        result["emailPreviewText"] = result["core"]["emailPreviewText"]
        result["emailGenerationMode"] = result["core"]["emailGenerationMode"]
        result["semanticBoost"] = result["artifacts"]["semanticBoost"]
        result["urlCleaning"] = result["artifacts"]["urlCleaning"]
        result["urlModelInput"] = result["artifacts"]["urlModelInput"]
        result["urlModelPromptPath"] = result["artifacts"]["urlModelPromptPath"]
        result["keywordNormalization"] = result["artifacts"]["keywordNormalization"]
        if debug:
            result["_debug"] = {"resolved": resolved, "payloadResult": payload_result_extra, "model_analysis": effective_model_analysis, "analysis": analysis}
        return result
    except Exception as e:
        import traceback
        return {
            **build_error(
                "SCRIPT_ERROR",
                str(e),
                details={"step": step, "traceback": traceback.format_exc()},
                retryable=False,
                next_step="检查模型输入、payload 编译结果或 API 返回结构。",
            ),
            "step": step,
        }


def main():
    ap = argparse.ArgumentParser(description="WotoHub Campaign 单进程编排入口")
    ap.add_argument("--input", required=True, help="产品 URL 或文字描述")
    ap.add_argument("--token", help="WotoHub api-key（也可通过 WOTOHUB_API_KEY 环境变量）")
    ap.add_argument("--platform", default="tiktok")
    ap.add_argument("--min-fans", type=int, default=10000)
    ap.add_argument("--max-fans", type=int, default=500000)
    ap.add_argument("--has-email", action="store_true", default=True)
    ap.add_argument("--no-email", dest="has_email", action="store_false")
    ap.add_argument("--page-size", type=int, default=DEFAULT_SEARCH_RESULT_LIMIT)
    ap.add_argument("--exclude-contacted", action="store_true", default=True, help="默认过滤已联系达人")
    ap.add_argument("--include-contacted", dest="exclude_contacted", action="store_false", help="不过滤已联系达人，此时 searchFilterList 置空")
    ap.add_argument("--semantic-mode", choices=["disabled", "mock", "external"], default="mock")
    ap.add_argument("--no-retry", dest="retry_fallbacks", action="store_false")
    ap.add_argument("--parallel", dest="parallel_strategies", action="store_true")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--output", help="结果输出到文件")
    ap.add_argument("--prefer-model-analysis", action="store_true", default=True, dest="prefer_model_analysis")
    ap.add_argument("--no-prefer-model-analysis", action="store_false", dest="prefer_model_analysis")
    ap.add_argument("--model-analysis-json", help="JSON string of model_analysis dict")
    ap.add_argument("--url-model-analysis-json", help="JSON string of url_model_analysis dict for URL inputs")
    ap.add_argument("--sender-name", help="邮件署名；生成邀约邮件前必须先向用户确认")
    ap.add_argument("--offer-type", choices=["sample", "paid", "affiliate"], default="sample", help="合作方式；用于邮件生成阶段的最小 campaign brief")
    ap.add_argument("--email-language", default="en", help="邮件语言；默认 en，用户指定时使用指定语言")
    ap.add_argument("--selected-blogger-ids", help="逗号分隔的目标 bloggerId/besId 列表；只对这些达人生成邮件")
    ap.add_argument("--selected-ranks", help="逗号分隔的推荐序号列表；只对这些序号对应的达人生成邮件")
    ap.add_argument("--all-search-results-selected", action="store_true", help="显式全选当前搜索结果，用于批量生成/发送邮件")
    ap.add_argument("--email-model-drafts-json", help="宿主模型生成的邮件 drafts JSON string")
    ap.add_argument("--allow-fallback-drafts", action="store_true", help="允许在没有 host drafts 时退回脚本 fallback 草稿；默认关闭")
    ap.add_argument("--brand-name")
    ap.add_argument("--deliverable")
    ap.add_argument("--compensation")
    ap.add_argument("--target-market")
    ap.add_argument("--cta-goal")
    ap.add_argument("--include-email-preview", action="store_true", help="默认只返回搜索/推荐结果；显式开启后才生成邮件预览")
    args = ap.parse_args()

    token = args.token or get_token(None, required=False)
    model_analysis = json.loads(args.model_analysis_json) if args.model_analysis_json else None
    url_model_analysis = json.loads(args.url_model_analysis_json) if args.url_model_analysis_json else None
    email_model_drafts = json.loads(args.email_model_drafts_json) if args.email_model_drafts_json else None
    selected_blogger_ids = [x.strip() for x in (args.selected_blogger_ids or '').split(',') if x.strip()]
    selected_ranks = [int(x.strip()) for x in (args.selected_ranks or '').split(',') if x.strip()]

    result = run_campaign(
        user_input=args.input,
        token=token,
        platform=args.platform,
        min_fans=args.min_fans,
        max_fans=args.max_fans,
        has_email=args.has_email,
        exclude_contacted=args.exclude_contacted,
        page_size=args.page_size,
        semantic_mode=args.semantic_mode,
        retry_fallbacks=args.retry_fallbacks,
        parallel_strategies=args.parallel_strategies,
        debug=args.debug,
        model_analysis=model_analysis,
        url_model_analysis=url_model_analysis,
        prefer_model_analysis=args.prefer_model_analysis,
        sender_name=args.sender_name,
        include_email_preview=args.include_email_preview,
        offer_type=args.offer_type,
        email_language=args.email_language,
        selected_blogger_ids=selected_blogger_ids,
        selected_ranks=selected_ranks,
        all_search_results_selected=args.all_search_results_selected,
        email_model_drafts=email_model_drafts,
        allow_fallback_drafts=args.allow_fallback_drafts,
        brand_name=args.brand_name,
        deliverable=args.deliverable,
        compensation=args.compensation,
        target_market=args.target_market,
        cta_goal=args.cta_goal,
    )

    if args.output:
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
