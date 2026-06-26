#!/usr/bin/env python3
"""Upper-layer input understanding for WotoHub upper-layer architecture.

This module only handles semantic understanding + context normalization.
It must not directly execute WotoHub API actions.
"""

from __future__ import annotations

import re
from typing import Any, Optional
from urllib.parse import urlparse

from context_schema import normalize_context, normalize_primary_task
from semantic_layer import SemanticLayer

_URL_RE = re.compile(r"https?://[^\s]+", re.IGNORECASE)


TASK_KEYWORDS = [
    ("monitor_replies", ["monitor replies", "reply assist", "inbox", "reply", "回复", "回信", "收件箱", "邮件回复"]),
    ("generate_email", ["generate email", "write email", "outreach", "邀约", "邮件", "开发信"]),
    ("campaign_create", ["campaign", "建campaign", "创建campaign", "建活动", "创建活动"]),
    ("search", ["search", "creator", "influencer", "找达人", "搜达人", "达人", "博主", "红人"]),
    ("product_analysis", ["product", "analyze", "分析", "产品", "链接"]),
]


PLATFORM_HINTS = {
    "tiktok": ["tiktok", "tik tok"],
    "amazon": ["amazon"],
    "shopify": ["shopify", "myshopify"],
    "youtube": ["youtube"],
    "instagram": ["instagram", "ig"],
}


MARKET_HINTS = {
    "us": ["美国", "us", "usa", "united states"],
    "uk": ["英国", "uk", "united kingdom"],
    "de": ["德国", "germany", "de"],
    "jp": ["日本", "japan", "jp"],
}


LANG_HINTS = {
    "en": ["英语", "英文", "english", "en"],
    "de": ["德语", "german", "deutsch"],
    "jp": ["日语", "japanese", "jp"],
}


OFFER_HINTS = {
    "sample": ["sample", "送样", "寄样"],
    "paid": ["paid", "付费", "合作费"],
    "affiliate": ["affiliate", "分佣", "佣金"],
}


GOAL_HINTS = {
    "conversion": ["转化", "成交", "下单", "带货"],
    "awareness": ["曝光", "种草", "认知"],
    "testing": ["测品", "测试", "试投", "试水"],
    "promotion": ["推广", "宣传", "引流"],
}


CREATOR_TYPE_HINTS = {
    "beauty": ["美妆", "护肤", "彩妆"],
    "fitness": ["健身", "运动"],
    "tech": ["科技", "数码"],
    "mom": ["宝妈", "母婴"],
    "lifestyle": ["生活方式", "生活", "lifestyle"],
    "food": ["美食", "吃播", "food"],
    "review": ["测评", "开箱", "review"],
}


FOLLOWER_PATTERNS = [
    re.compile(r"(\d+)[万wW]\s*(?:粉|粉丝)"),
    re.compile(r"(\d{1,4})\s*[kK]\s*(?:粉|粉丝|followers?)?", re.IGNORECASE),
    re.compile(r"(\d{4,7})\s*(?:粉|粉丝|followers?)", re.IGNORECASE),
]


TOP_N_PATTERNS = [
    re.compile(r"前\s*(\d{1,3})\s*(?:个|位|名)?"),
    re.compile(r"top\s*(\d{1,3})", re.IGNORECASE),
]


SORT_FOLLOWERS_DESC_HINTS = [
    "按粉丝数从高到低",
    "粉丝数从高到低",
    "粉丝最高",
    "优先粉丝高",
    "按粉丝排序",
]


EMAIL_REQUIRED_HINTS = [
    "有邮箱",
    "带邮箱",
    "有 email",
    "has email",
]


ALL_SEARCH_RESULTS_HINTS = [
    "全发",
    "都发",
    "全部发",
    "全选搜索结果",
    "所有搜索结果",
    "全部搜索结果",
    "这次搜索结果全发",
]


HOST_SUFFIX_PLATFORM = {
    "tiktok.com": "tiktok",
    "amazon.com": "amazon",
    "amazon.co.uk": "amazon",
    "amazon.de": "amazon",
    "amazon.co.jp": "amazon",
    "myshopify.com": "shopify",
    "shopify.com": "shopify",
}


DEFAULT_PRIMARY_TASK = "product_analysis"


MISSING_FIELD_MESSAGES = {
    "product_anchor": "请补充产品链接或明确产品名称。",
    "offerType": "请补充合作方式，例如送样 / 付费 / 分佣。",
    "input": "请补充原始输入内容或产品链接。",
    "platforms": "请补充投放平台，例如 TikTok / Instagram / YouTube。",
    "productName": "请补充产品名称，方便生成邀约邮件。",
    "campaignId_or_input": "请补充 campaignId 或相关回复上下文。",
}


def _extract_urls(raw_text: str) -> list[str]:
    return [m.group(0).strip() for m in _URL_RE.finditer(raw_text or "")]


def _infer_platforms(raw_text: str, urls: list[str]) -> list[str]:
    text = (raw_text or "").lower()
    platforms: list[str] = []
    for platform, hints in PLATFORM_HINTS.items():
        if any(hint in text for hint in hints):
            platforms.append(platform)
    for url in urls:
        try:
            host = urlparse(url).netloc.lower()
        except Exception:
            host = ""
        for suffix, platform in HOST_SUFFIX_PLATFORM.items():
            if host == suffix or host.endswith("." + suffix):
                platforms.append(platform)
    deduped = []
    seen = set()
    for item in platforms:
        if item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def _infer_markets(raw_text: str) -> list[str]:
    text = (raw_text or "").lower()
    out = []
    for market, hints in MARKET_HINTS.items():
        if any(hint in text for hint in hints):
            out.append(market)
    return out


def _infer_languages(raw_text: str) -> list[str]:
    text = (raw_text or "").lower()
    out = []
    for lang, hints in LANG_HINTS.items():
        if any(hint in text for hint in hints):
            out.append(lang)
    return out


def _infer_offer_type(raw_text: str) -> Optional[str]:
    text = (raw_text or "").lower()
    for offer_type, hints in OFFER_HINTS.items():
        if any(hint in text for hint in hints):
            return offer_type
    return None


def _infer_goal(raw_text: str) -> Optional[str]:
    text = (raw_text or "").lower()
    for goal, hints in GOAL_HINTS.items():
        if any(hint in text for hint in hints):
            return goal
    return None


def _infer_creator_types(raw_text: str) -> list[str]:
    text = (raw_text or "").lower()
    out = []
    for creator_type, hints in CREATOR_TYPE_HINTS.items():
        if any(hint in text for hint in hints):
            out.append(creator_type)
    return out


def _normalize_creator_types(existing: Optional[list[Any]], raw_text: str) -> list[str]:
    normalized: list[str] = []
    seen = set()

    for item in existing or []:
        item_text = str(item or "").strip().lower()
        if not item_text:
            continue
        mapped = None
        for creator_type, hints in CREATOR_TYPE_HINTS.items():
            if item_text == creator_type or any(hint in item_text for hint in hints):
                mapped = creator_type
                break
        mapped = mapped or item_text
        if mapped not in seen:
            seen.add(mapped)
            normalized.append(mapped)

    for inferred in _infer_creator_types(raw_text):
        if inferred not in seen:
            seen.add(inferred)
            normalized.append(inferred)

    return normalized


def _infer_primary_task(raw_text: str, explicit_task: Optional[str]= None) -> str:
    if explicit_task:
        return normalize_primary_task(explicit_task) or explicit_task

    text = (raw_text or "").lower()
    urls = _extract_urls(raw_text)

    if any(token in text for token in ["回复", "回信", "reply", "inbox", "收件箱"]):
        return "monitor_replies"
    if any(token in text for token in ["开发信", "邀约邮件", "outreach", "generate email", "write email"]):
        return "generate_email"
    if any(token in text for token in ["建campaign", "创建campaign", "campaign", "建活动", "创建活动"]):
        return "campaign_create"
    if any(token in text for token in ["找达人", "搜达人", "search", "creator", "influencer", "达人", "博主", "红人"]):
        return "search"
    if urls and any(token in text for token in ["分析", "analyze", "product", "产品", "链接"]):
        return "product_analysis"

    for task, hints in TASK_KEYWORDS:
        if any(hint in text for hint in hints):
            return task

    if urls:
        return "product_analysis"
    return DEFAULT_PRIMARY_TASK


def _infer_follower_range(raw_text: str) -> dict[str, int | None]:
    text = raw_text or ""
    for pattern in FOLLOWER_PATTERNS:
        m = pattern.search(text)
        if not m:
            continue
        raw_num = int(m.group(1))
        matched = m.group(0).lower()
        if "万" in matched or "w" in matched:
            raw_num *= 10000
        elif "k" in matched:
            raw_num *= 1000
        return {"min": raw_num, "max": None}
    return {"min": None, "max": None}


def _infer_selection_semantics(raw_text: str) -> dict[str, Any]:
    text = (raw_text or "").lower()

    all_selected = any(hint in text for hint in ALL_SEARCH_RESULTS_HINTS)
    sort_by_followers_desc = any(hint in text for hint in SORT_FOLLOWERS_DESC_HINTS)
    require_email = any(hint in text for hint in EMAIL_REQUIRED_HINTS)
    follower_range = _infer_follower_range(raw_text)

    top_n = None
    for pattern in TOP_N_PATTERNS:
        m = pattern.search(text)
        if not m:
            continue
        try:
            top_n = int(m.group(1))
        except Exception:
            top_n = None
        if top_n and top_n > 0:
            break

    has_send_semantics = any(token in text for token in ["发", "发送", "send", "邮件", "邀约", "开发信"])
    selection_rule = None
    if top_n and has_send_semantics:
        selection_rule = {"type": "top_n", "topN": top_n}
    elif all_selected:
        selection_rule = {"type": "all_search_results"}

    filters: dict[str, Any] = {}
    if follower_range.get("min"):
        filters["minFollowers"] = follower_range.get("min")
    if follower_range.get("max"):
        filters["maxFollowers"] = follower_range.get("max")
    if require_email:
        filters["hasEmail"] = True

    if selection_rule:
        if filters:
            selection_rule["filters"] = filters
        if sort_by_followers_desc:
            selection_rule["sort"] = [{"field": "followers", "order": "desc"}]

    return {
        "allSearchResultsSelected": bool(all_selected),
        "selectionRule": selection_rule,
    }


def _clean_product_name(raw_name: Optional[str], raw_input: str, primary_task: str) -> Optional[str]:
    name = (raw_name or "").strip()
    if not name:
        return None

    # 如果已经是短词组，直接保留
    if len(name) <= 24 and not any(token in name for token in ["请帮", "帮我", "达人", "开发信", "campaign", "美国市场"]):
        return name

    candidate = name or raw_input or ""
    candidate = re.sub(r"https?://\S+", " ", candidate, flags=re.IGNORECASE)

    wrappers = [
        r"^请?帮我",
        r"^麻烦帮我",
        r"^帮我",
        r"^请",
        r"写一封",
        r"写封",
        r"生成一封",
        r"创建一个",
        r"创建一场",
        r"做一个",
        r"推广",
    ]
    suffixes = [
        r"的?(开发信|邀约邮件|邮件)",
        r"，?送样合作.*$",
        r"，?付费合作.*$",
        r"，?分佣合作.*$",
        r"，?面向.*$",
        r"，?给.*达人.*$",
        r"，?美国市场.*$",
        r"，?TikTok.*$",
        r"，?Instagram.*$",
        r"，?YouTube.*$",
    ]

    for pattern in wrappers:
        candidate = re.sub(pattern, "", candidate, flags=re.IGNORECASE)
    for pattern in suffixes:
        candidate = re.sub(pattern, "", candidate, flags=re.IGNORECASE)

    candidate = re.sub(r"^(一封|一个|一场)", "", candidate)
    candidate = re.sub(r"^(关于|针对)", "", candidate)
    candidate = re.sub(r"\s+", " ", candidate).strip(" ，,。:：")

    if primary_task == "generate_email":
        m = re.search(r"(.{1,24}?)(?:的?(?:开发信|邀约邮件|邮件)|$)", candidate)
        if m:
            candidate = m.group(1).strip(" ，,。:：")

    if not candidate:
        return name
    return candidate if len(candidate) <= len(name) else name


def _extract_missing_fields(ctx: dict[str, Any]) -> list[str]:
    missing = []
    primary_task = ((ctx.get("intent") or {}).get("primaryTask"))
    product_signals = ctx.get("productSignals") or {}
    if primary_task in {"product_analysis", "search", "generate_email"}:
        if not product_signals.get("urls") and not product_signals.get("productName"):
            missing.append("product_anchor")
    if primary_task == "generate_email" and not ((ctx.get("marketingContext") or {}).get("offerType")):
        missing.append("offerType")
    return missing


def build_missing_field_prompt(missing_fields: list[str]) -> Optional[str]:
    prompts = [MISSING_FIELD_MESSAGES[field] for field in missing_fields if field in MISSING_FIELD_MESSAGES]
    if not prompts:
        return None
    return "；".join(dict.fromkeys(prompts))


def understand_input(raw_input: str, explicit_task: Optional[str]= None) -> dict[str, Any]:
    raw_input = (raw_input or "").strip()
    urls = _extract_urls(raw_input)
    primary_task = _infer_primary_task(raw_input, explicit_task=explicit_task)

    model_understanding = SemanticLayer.understand_user_input(raw_input, explicit_task=primary_task)
    ctx = normalize_context(model_understanding)
    ctx.setdefault("intent", {})["primaryTask"] = normalize_primary_task(primary_task) or primary_task

    product_signals = ctx.setdefault("productSignals", {})
    marketing = ctx.setdefault("marketingContext", {})
    meta = ctx.setdefault("meta", {})

    product_signals["rawInput"] = raw_input
    product_signals["urls"] = urls
    product_signals["productName"] = _clean_product_name(product_signals.get("productName"), raw_input, primary_task)
    marketing["platforms"] = marketing.get("platforms") or _infer_platforms(raw_input, urls)
    marketing["targetMarkets"] = marketing.get("targetMarkets") or _infer_markets(raw_input)
    marketing["languages"] = marketing.get("languages") or _infer_languages(raw_input)
    marketing["offerType"] = marketing.get("offerType") or _infer_offer_type(raw_input)
    marketing["goal"] = marketing.get("goal") or _infer_goal(raw_input)
    marketing["creatorTypes"] = _normalize_creator_types(marketing.get("creatorTypes"), raw_input)
    marketing["followerRange"] = marketing.get("followerRange") or _infer_follower_range(raw_input)

    selection_semantics = _infer_selection_semantics(raw_input)
    resolved = ctx.setdefault("resolvedArtifacts", {})
    if selection_semantics.get("selectionRule") and not resolved.get("selectionRule"):
        resolved["selectionRule"] = selection_semantics.get("selectionRule")
    if selection_semantics.get("allSearchResultsSelected"):
        resolved["allSearchResultsSelected"] = True

    if urls:
        ctx.setdefault("operationalHints", {})["needsProductResolve"] = True

    ctx["missingFields"] = _extract_missing_fields(ctx)
    missing_prompt = build_missing_field_prompt(ctx["missingFields"])
    meta.setdefault("notes", [])
    meta["notes"] = [*meta.get("notes", []), "upper-layer input understanding applied"]
    if missing_prompt:
        meta["missingFieldPrompt"] = missing_prompt
    return normalize_context(ctx)
