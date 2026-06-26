#!/usr/bin/env python3
from typing import Optional
import argparse
import copy
import json
import sys
from pathlib import Path

from common import get_token, request_json, print_json
from config import claw_search_path, open_search_path, RECOMMENDATION_MAX_ITEMS
from recommendation_presenter import build_recommendation_display
from query_constraints import build_region_list

# Known WotoHub blogger-list response keys (checked in order of commonality)
WOTO_BLOGGER_KEYS = ('bloggerList', 'records', 'list', 'rows', 'dataList')
CONTENT_TEXT_KEYS = (
    'video_title', 'videoTitle', 'title', 'desc', 'description', 'content',
    'latestVideoTitle', 'latestVideoDesc', 'productTitle', 'productName',
    'prodTitle', 'prodName', 'mainProductName'
)
LIST_CONTENT_KEYS = ('tagList', 'productList', 'videoList', 'recentVideos', 'recentProducts')


def build_payload_from_args(args):
    payload = {
        "platform": args.platform,
        "pageNum": args.page_num,
        "pageSize": args.page_size,
    }
    if args.min_fans is not None:
        payload["minFansNum"] = args.min_fans
    if args.max_fans is not None:
        payload["maxFansNum"] = args.max_fans
    if args.min_interactive_rate is not None:
        payload["minInteractiveRate"] = args.min_interactive_rate
    payload["hasEmail"] = True
    payload.setdefault("searchFilterList", ["THIS_UNTOUCH"])
    if args.sort:
        payload["searchSort"] = args.sort
    if args.sort_order:
        payload["sortOrder"] = args.sort_order
    if args.lang:
        payload["blogLangs"] = args.lang
    if args.cate:
        payload["blogCateIds"] = args.cate
    if args.region:
        payload["regionList"] = build_region_list(args.region)
    if args.keyword:
        payload["searchType"] = "KEYWORD"
        payload["advancedKeywordList"] = [{"value": keyword, "exclude": False} for keyword in args.keyword]
    return payload


def normalize_search_payload(payload: dict) -> dict:
    """Normalize search payloads with minimal API-safe defaults.

    Keep this layer intentionally lightweight: execution scripts should enforce
    required request defaults, while higher-level semantic analysis remains in
    the model/builder layer.

    WotoHub search should default to `searchType=KEYWORD` unless the caller
    explicitly sets another value.
    """
    if not isinstance(payload, dict):
        raise ValueError('payload input must contain a JSON object')

    normalized = copy.deepcopy(payload)

    if not normalized.get('searchType'):
        normalized['searchType'] = 'KEYWORD'

    return normalized



def load_payload_arg(payload_file: Optional[str]):
    if payload_file:
        raw = Path(payload_file).read_text()
        parsed = json.loads(raw)
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
        if not raw:
            return None
        parsed = json.loads(raw)
    else:
        return None

    if isinstance(parsed, dict) and 'payload' in parsed and isinstance(parsed['payload'], dict):
        return normalize_search_payload(parsed['payload'])
    if not isinstance(parsed, dict):
        raise ValueError('payload input must contain a JSON object')
    return normalize_search_payload(parsed)


def is_search_success(result: dict) -> bool:
    if not isinstance(result, dict):
        return False
    if result.get('success') is True:
        return True
    code = result.get('code')
    return code in {0, '0', 200, '200'}


def trim_advanced_keywords(payload: dict, limit: int) -> dict:
    trimmed = copy.deepcopy(payload)
    if trimmed.get('advancedKeywordList'):
        trimmed['advancedKeywordList'] = trimmed['advancedKeywordList'][:limit]
        trimmed['searchType'] = 'KEYWORD'
    return trimmed


def unique_top_categories(blog_cate_ids: list[str], depth: int) -> list[str]:
    if not blog_cate_ids:
        return []
    out = []
    seen = set()
    for code in blog_cate_ids:
        shortened = code[:depth] if len(code) >= depth else code
        if shortened and shortened not in seen:
            seen.add(shortened)
            out.append(shortened)
    return out


def build_semantic_fallbacks(payload: dict) -> list[dict]:
    variants = []

    if payload.get('advancedKeywordList'):
        variants.append({
            'label': 'core_keywords_4',
            'payload': trim_advanced_keywords(payload, 4),
            'reason': '保留前4个核心关键词，减少关键词噪音',
        })
        variants.append({
            'label': 'core_keywords_2',
            'payload': trim_advanced_keywords(payload, 2),
            'reason': '仅保留最核心的2个商品关键词',
        })

    if payload.get('blogCateIds'):
        level2 = copy.deepcopy(payload)
        level2['blogCateIds'] = unique_top_categories(level2['blogCateIds'], 4)
        variants.append({
            'label': 'category_to_level2',
            'payload': level2,
            'reason': '类目从更深层收敛到二级',
        })

        level1 = copy.deepcopy(payload)
        level1['blogCateIds'] = unique_top_categories(level1['blogCateIds'], 2)
        variants.append({
            'label': 'category_to_level1',
            'payload': level1,
            'reason': '类目继续收敛到一级大类',
        })

    keyword_and_level2 = copy.deepcopy(payload)
    if keyword_and_level2.get('advancedKeywordList'):
        keyword_and_level2['advancedKeywordList'] = keyword_and_level2['advancedKeywordList'][:3]
        keyword_and_level2['searchType'] = 'KEYWORD'
    if keyword_and_level2.get('blogCateIds'):
        keyword_and_level2['blogCateIds'] = unique_top_categories(keyword_and_level2['blogCateIds'], 4)
    variants.append({
        'label': 'balanced_light',
        'payload': keyword_and_level2,
        'reason': '同时缩减关键词和类目，保留平衡搜索意图',
    })

    category_only = copy.deepcopy(payload)
    category_only.pop('advancedKeywordList', None)
    category_only.pop('searchType', None)
    if category_only.get('blogCateIds'):
        variants.append({
            'label': 'category_only',
            'payload': category_only,
            'reason': '仅保留分类过滤，验证类目路径可用性',
        })

    lightweight = copy.deepcopy(payload)
    if lightweight.get('advancedKeywordList'):
        lightweight['advancedKeywordList'] = lightweight['advancedKeywordList'][:2]
        lightweight['searchType'] = 'KEYWORD'
    if lightweight.get('blogCateIds'):
        lightweight['blogCateIds'] = unique_top_categories(lightweight['blogCateIds'], 2)
    variants.append({
        'label': 'lightweight_core_fields',
        'payload': lightweight,
        'reason': '保留平台/地区/语言/粉丝量 + 极简关键词/类目',
    })

    unique = []
    seen = set()
    for item in variants:
        key = json.dumps(item['payload'], sort_keys=True, ensure_ascii=False)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


# ── 错误驱动的精准回退 ────────────────────────────────────────────────────────

def _error_tag(result: dict) -> tuple[str, str]:
    """
    从 API 返回的 result 中提取错误类型标签和消息。
    返回 (error_tag, error_message)。
    """
    code = str(result.get("code", ""))
    message = str(result.get("message", "")).lower()
    # 按优先级匹配已知错误
    if "category" in message and "not found" in message:
        return "CATEGORY_NOT_FOUND", message
    if "keyword" in message and ("narrow" in message or "no result" in message):
        return "KEYWORD_TOO_NARROW", message
    if "region" in message and ("not support" in message or "not found" in message):
        return "REGION_NOT_SUPPORTED", message
    if code in {"429", "429000"}:
        return "RATE_LIMIT", message
    # 按 code 值判断
    if code == "404":
        return "NOT_FOUND", message
    return "UNKNOWN", message


def _is_rate_limit(result: dict) -> bool:
    code = str(result.get("code", ""))
    message = str(result.get("message", "")).lower()
    return code == "429" or "rate limit" in message or "too many" in message


def _count_results(result: dict) -> int:
    """从 result 中提取 blogger 列表长度。"""
    data = result.get("data")
    if not isinstance(data, dict):
        return 0
    for key in WOTO_BLOGGER_KEYS:
        if isinstance(data.get(key), list):
            return len(data[key])
    return 0


def build_error_driven_fallbacks(
    payload: dict,
    failed_result: dict,
) -> list[dict]:
    """
    根据 API 返回的错误类型动态生成精准回退策略。

    策略映射
    --------
    - CATEGORY_NOT_FOUND  → 先缩到更上层类目，不直接清空 blogCateIds
    - KEYWORD_TOO_NARROW  → 减少关键词，保留类目
    - REGION_NOT_SUPPORTED → 去掉 regionList，扩大地区
    - RATE_LIMIT          → 空列表（由 execute_search 重试逻辑处理）
    - 结果数=0（但 code=0） → 同时缩减关键词和类目
    """
    tag, _ = _error_tag(failed_result)
    variants: list[dict] = []
    count = _count_results(failed_result)

    if tag == "CATEGORY_NOT_FOUND":
        variant = copy.deepcopy(payload)
        if variant.get("blogCateIds"):
            variant["blogCateIds"] = unique_top_categories(variant["blogCateIds"], 4) or variant.get("blogCateIds")
        variants.append({
            "label": "relax_category_to_level2",
            "payload": variant,
            "reason": "类目不可用，先放宽到二级类目而不是直接退成纯关键词",
        })
        variant2 = copy.deepcopy(payload)
        if variant2.get("blogCateIds"):
            variant2["blogCateIds"] = unique_top_categories(variant2["blogCateIds"], 2) or variant2.get("blogCateIds")
        if variant2.get("advancedKeywordList"):
            variant2["advancedKeywordList"] = variant2["advancedKeywordList"][:3]
            variant2["searchType"] = "KEYWORD"
        variants.append({
            "label": "relax_category_to_level1",
            "payload": variant2,
            "reason": "继续放宽到一级类目，同时保留少量关键词 refinement",
        })

    elif tag == "KEYWORD_TOO_NARROW" or (tag == "UNKNOWN" and count == 0):
        # 减少关键词，保留类目
        variant = copy.deepcopy(payload)
        if variant.get("advancedKeywordList"):
            variant["advancedKeywordList"] = variant["advancedKeywordList"][:3]
            variant["searchType"] = "KEYWORD"
        if variant.get("blogCateIds"):
            # 扩大类目到一级
            variant["blogCateIds"] = unique_top_categories(variant["blogCateIds"], 2)
        variants.append({
            "label": "reduce_keywords_keep_category",
            "payload": variant,
            "reason": "关键词范围过窄，缩减关键词并扩大类目",
        })
        # 进一步：完全去掉关键词，仅用类目
        variant2 = copy.deepcopy(payload)
        variant2.pop("advancedKeywordList", None)
        variant2.pop("searchType", None)
        if variant2.get("blogCateIds"):
            variants.append({
                "label": "category_only_from_narrow",
                "payload": variant2,
                "reason": "关键词无结果，降级到纯类目",
            })

    elif tag == "REGION_NOT_SUPPORTED":
        # 去掉地区限制
        variant = copy.deepcopy(payload)
        variant.pop("regionList", None)
        variants.append({
            "label": "drop_region",
            "payload": variant,
            "reason": "地区参数不被支持，移除地区过滤",
        })
        # 进一步：同时去掉地区 + 精简关键词
        variant2 = copy.deepcopy(variant)
        if variant2.get("advancedKeywordList"):
            variant2["advancedKeywordList"] = variant2["advancedKeywordList"][:2]
            variant2["searchType"] = "KEYWORD"
        variants.append({
            "label": "drop_region_lighten_keywords",
            "payload": variant2,
            "reason": "去掉地区同时精简关键词，扩大召回",
        })

    elif tag == "RATE_LIMIT":
        # rate limit 不在这里处理，由 execute_search 重试处理
        pass

    # 兜底：通用的语义回退
    if not variants:
        semantic = build_semantic_fallbacks(payload)
        # 只取前3个最轻量的回退
        variants.extend(semantic[:3])

    # 去重
    unique: list[dict] = []
    seen: set[str] = set()
    for item in variants:
        key = json.dumps(item["payload"], sort_keys=True, ensure_ascii=False)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def execute_search(path: str, token: Optional[str], payload: dict) -> dict:
    """
    Call the WotoHub search API with up to 2 retries on network errors
    and up to 3 retries on HTTP / 429 rate-limit errors (with back-off).

    Rate-limit retries preserve full search precision — unlike semantic
    fallbacks which reduce search scope, rate-limit back-off simply waits
    and re-attempts the *exact same payload*.
    """
    import time
    last_err: Optional[Exception]= None

    for attempt in range(2):
        try:
            result = request_json("POST", path, token, payload)

            # Check for rate-limit response (429)
            code = str(result.get("code", ""))
            message = str(result.get("message", "")).lower()
            is_rate_limit = (
                code == "429"
                or "rate limit" in message
                or "too many" in message
            )
            if is_rate_limit and attempt < 1:
                wait = 1.5 * (2 ** attempt)
                time.sleep(wait)
                continue

            return {
                "searchApi": "clawSearch" if token else "openSearch",
                "path": path,
                "usedToken": bool(token),
                "payload": payload,
                "result": result,
            }
        except Exception as e:
            last_err = e
            if attempt < 1:
                time.sleep(1.0 * (attempt + 1))

    return {
        "searchApi": "clawSearch" if token else "openSearch",
        "path": path,
        "usedToken": bool(token),
        "payload": payload,
        "result": {"code": -1, "message": f"All attempts failed: {last_err}", "data": None},
    }


def extract_blogger_items(search_output: dict) -> list[dict]:
    """
    Extract the blogger list from an API response.

    Supports two WotoHub response structures:
    - Wrapped:  response['result']['data']['bloggerList']  (clawSearch)
    - Flat:     response['data']['bloggerList']           (openSearch)

    Also checks for blogger list directly at response root for robustness.
    """
    # Try the wrapped path first (result.data.*)
    result = search_output.get('result', {})
    data = result.get('data') if isinstance(result, dict) else None

    # Try flat path: response.data.bloggerList (openSearch has no 'result' wrapper)
    if data is None:
        data = search_output.get('data')

    if isinstance(data, dict):
        for key in WOTO_BLOGGER_KEYS:
            if isinstance(data.get(key), list):
                return [x for x in data[key] if isinstance(x, dict)]
    elif isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]

    # Blogger list may be directly at the root level
    for key in WOTO_BLOGGER_KEYS:
        if isinstance(search_output.get(key), list):
            return [x for x in search_output[key] if isinstance(x, dict)]

    # No known key matched — log explicitly so it's not silent
    import sys
    resp_keys = list(search_output.keys()) if isinstance(search_output, dict) else type(search_output).__name__
    print(f"# [WARNING] No blogger list found. Checked top-level + result.data + data. "
          f"Response keys: {resp_keys}", file=sys.stderr)
    return []


def _normalize_text(value) -> str:
    if value is None:
        return ''
    if isinstance(value, dict):
        return ' '.join(_normalize_text(v) for v in value.values())
    if isinstance(value, list):
        return ' '.join(_normalize_text(v) for v in value)
    return ' '.join(str(value).split()).strip().lower()


def _payload_terms(payload: dict) -> list[str]:
    terms = []
    for item in payload.get('advancedKeywordList', []) or []:
        if isinstance(item, dict):
            value = (item.get('value') or '').strip().lower()
            if value:
                terms.append(value)
    return terms[:8]


def _split_semantic_tokens(terms: list[str]) -> list[str]:
    tokens = []
    for term in terms or []:
        for part in str(term).replace('/', ' ').replace('-', ' ').split():
            part = part.strip().lower()
            if len(part) >= 3:
                tokens.append(part)
    return list(dict.fromkeys(tokens))[:20]


def analyze_historical_content(item: dict, payload: dict) -> dict:
    blob_parts = []
    samples = []
    for key in CONTENT_TEXT_KEYS:
        text = _normalize_text(item.get(key))
        if text:
            blob_parts.append(text)
            if len(samples) < 3:
                samples.append(text[:120])
    for key in LIST_CONTENT_KEYS:
        value = item.get(key)
        text = _normalize_text(value)
        if text:
            blob_parts.append(text)
            if len(samples) < 3:
                samples.append(text[:120])

    tags = [str(x).strip() for x in (item.get('tagList') or []) if str(x).strip()]
    payload_terms = _payload_terms(payload)
    blob = ' '.join(blob_parts)
    matched_terms = [term for term in payload_terms if term and term in blob]

    signals = []
    score = 0
    if matched_terms:
        score += min(15, 5 * len(matched_terms))
        signals.append('历史内容包含搜索关键词')
    if item.get('hasProduct'):
        score += 8
        signals.append('历史内容含带货商品')
    if tags:
        score += min(8, len(tags) * 2)
        signals.append('标签信息较完整')
    if blob:
        score += 4
        signals.append('可提取到历史标题/描述')

    return {
        'score': score,
        'matchedTerms': matched_terms[:5],
        'tagCount': len(tags),
        'contentSamples': samples,
        'signals': signals,
        'hasHistorySignals': bool(blob or tags or item.get('hasProduct')),
    }


def _pick_first(item: dict, *keys, default=None):
    for key in keys:
        value = item.get(key)
        if value not in (None, '', []):
            return value
    return default


def _to_int(value, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default


def _to_float(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def build_quality_signals(item: dict, payload: dict, history: Optional[dict]= None) -> tuple[list[str], list[str]]:
    history = history or {}
    fit_signals: list[str] = []
    risk_signals: list[str] = []

    tags = [str(x).strip().lower() for x in (item.get('tagList') or []) if str(x).strip()]
    category_text = str(_pick_first(item, 'blogCateName', 'blogCateNames', 'categoryName', 'categoryNames', default='') or '').lower()
    payload_terms = _payload_terms(payload)
    semantic_tokens = _split_semantic_tokens(payload_terms)
    matched_terms = history.get('matchedTerms') or []
    history_signals = history.get('signals') or []

    tag_blob = ' '.join(tags)
    category_blob = category_text
    payload_token_hits = []
    semantic_token_hits = []
    for term in payload_terms:
        token = str(term).strip().lower()
        if not token:
            continue
        if token in tag_blob or token in category_blob:
            payload_token_hits.append(token)
    for token in semantic_tokens:
        if token in tag_blob or token in category_blob:
            semantic_token_hits.append(token)

    if payload.get('hasEmail') and item.get('hasEmail'):
        fit_signals.append('email_available')
    if matched_terms:
        fit_signals.append('history_matches_product_semantics')
    if payload_token_hits:
        fit_signals.append('tag_or_category_matches_payload_terms')
    elif semantic_token_hits:
        fit_signals.append('tag_or_category_matches_semantic_tokens')
    if item.get('hasProduct'):
        fit_signals.append('has_product_content_signal')
    if history_signals:
        fit_signals.append('creator_profile_has_relevant_vertical_signal')

    broad_tag_tokens = {'lifestyle', 'family', 'daily life', 'vlog', 'entertainment', 'blogger', '影视娱乐', '情感与关系'}
    broad_hits = [tag for tag in tags if any(tok in tag for tok in broad_tag_tokens)]
    if broad_hits and not payload_token_hits and not semantic_token_hits and not matched_terms:
        risk_signals.append('broad_profile_without_specific_match')

    if tags and len(tags) >= 3 and not payload_token_hits and not semantic_token_hits and not matched_terms:
        risk_signals.append('adjacent_or_mixed_category_profile')

    if payload_terms and not matched_terms and not payload_token_hits and not semantic_token_hits:
        risk_signals.append('weak_semantic_fit')

    if not tags and not category_text and not history.get('hasHistorySignals'):
        risk_signals.append('thin_metadata')

    try:
        fans = int(float(item.get('fansNum') or item.get('fans') or 0))
    except Exception:
        fans = 0
    if fans > 1000000 and not matched_terms and not payload_token_hits:
        risk_signals.append('very_large_creator_may_reduce_fit_precision')

    return list(dict.fromkeys(fit_signals))[:5], list(dict.fromkeys(risk_signals))[:5]


def score_influencer(item: dict, payload: dict) -> dict:
    nickname = item.get('nickname') or item.get('bloggerName') or item.get('nickName')
    fans = item.get('fansNum') or item.get('fans') or 0
    try:
        fans = int(float(fans))
    except Exception:
        fans = 0

    interactive = item.get('interactiveRateAvg') or item.get('interactiveRate') or item.get('engagementRate') or 0
    try:
        interactive = float(interactive)
        if interactive <= 1:
            interactive *= 100
    except Exception:
        interactive = 0.0

    history = analyze_historical_content(item, payload)

    score = 0
    reasons = []
    if payload.get('hasEmail') and item.get('hasEmail'):
        score += 25
        reasons.append('有邮箱，可直接触达')
    if interactive >= 5:
        score += 20
        reasons.append('互动率高')
    elif interactive >= 3:
        score += 12
        reasons.append('互动率不错')
    if 10000 <= fans <= 500000:
        score += 15
        reasons.append('粉丝量处于常用合作区间')
    elif fans > 500000:
        score += 8
        reasons.append('粉丝规模较大')
    if item.get('hasProduct'):
        score += 10
        reasons.append('已有商品内容信号')
    if item.get('viewAvg') or item.get('productVideoViewAvg30d'):
        score += 5
        reasons.append('有观看数据')
    if history['score']:
        score += min(history['score'], 10)
        if history['matchedTerms']:
            reasons.append('历史内容命中搜索词')

    if score >= 45:
        tier = '优先发送'
    elif score >= 28:
        tier = '观察'
    else:
        tier = '跳过'

    blogger_id = _pick_first(item, 'bEsId', 'besId', 'bloggerId', 'id', default='')
    wotohub_link = f"https://www.wotohub.com/kocNewDetail?id={blogger_id}" if blogger_id else None

    avg_views = _to_int(_pick_first(item, 'viewAvg', 'avgView', 'averageView', 'avgViews', 'videoAvgView', 'productVideoViewAvg30d'))
    avg_engagement = round(interactive, 2)
    wotohub_score = _to_float(_pick_first(item, 'score', 'bloggerScore', 'wotohubScore', 'starScore'))
    country = _pick_first(item, 'countryName', 'country', 'countryEn', 'regionZh', 'region')
    category = _pick_first(item, 'blogCateName', 'blogCateNames', 'categoryName', 'categoryNames')
    if isinstance(category, list):
        category = ' / '.join(str(x).strip() for x in category if str(x).strip())
    gmv30d = _to_float(_pick_first(item, 'gmv30d', 'gpm30d', 'productGmv30d', 'gmvLast30d', 'thirtyDayGmv'))
    original_link = _pick_first(item, 'link', 'bloggerLink', 'homeLink', 'homepage', 'originUrl', 'url')

    fit_signals, risk_signals = build_quality_signals(item, payload, history)

    return {
        'nickname': nickname,
        'fansNum': fans,
        'avgViews': avg_views,
        'interactiveRate': avg_engagement,
        'hasEmail': bool(item.get('hasEmail')),
        'matchScore': score,
        'matchTier': tier,
        'matchReasons': reasons,
        'fitSignals': fit_signals,
        'riskSignals': risk_signals,
        'region': item.get('regionZh') or item.get('region'),
        'country': country,
        'category': category,
        'wotohubScore': wotohub_score,
        'gmv30d': gmv30d,
        'tagList': item.get('tagList') or [],
        'historyAnalysis': history,
        'link': original_link,          # 博主原始链接（TikTok/YouTube/Instagram 主页）
        'originalLink': original_link,
        'wotohubLink': wotohub_link,        # WotoHub 博主分析页
        'besId': blogger_id,
        'raw': item,
    }


def _format_value(value, field: str = '') -> str:
    if value in (None, ''):
        return '-'
    if field in {'fans', 'avgViews'}:
        try:
            return f"{int(float(value)):,}"
        except Exception:
            return str(value)
    if field in {'avgEngagementRate'}:
        try:
            num = float(value)
            if num <= 1:
                num *= 100
            return f"{num:.2f}%"
        except Exception:
            return str(value)
    if field in {'wotohubScore', 'gmv30d', 'matchScore'}:
        try:
            num = float(value)
            return f"{num:,.2f}" if not num.is_integer() else f"{int(num):,}"
        except Exception:
            return str(value)
    if field in {'tags'} and isinstance(value, list):
        return ' / '.join(str(v).strip() for v in value if str(v).strip()) or '-'
    return str(value)


def render_markdown_table(rows: list[dict], columns: Optional[list[str]]= None) -> str:
    if not rows:
        return '暂无结果'
    columns = columns or [
        'channelName', 'fans', 'avgViews', 'avgEngagementRate', 'platform',
        'gmv30d', 'originalLink', 'tags', 'wotohubLink', 'advantages'
    ]
    headers = {
        'rank': '排名',
        'channelName': '频道名',
        'fans': '粉丝数',
        'avgViews': '平均观看量',
        'avgEngagementRate': '平均互动率',
        'platform': '平台',
        'wotohubCategory': 'WotoHub分类',
        'wotohubScore': 'WotoHub评分',
        'country': '国家',
        'gmv30d': '近30天GMV',
        'originalLink': '博主主页',
        'wotohubLink': 'WotoHub分析',
        'tags': '标签',
        'advantages': '优势',
        'besId': 'besId',
        'matchScore': '匹配分',
        'matchTier': '匹配等级',
    }
    lines = [
        '| ' + ' | '.join(headers.get(col, col) for col in columns) + ' |',
        '| ' + ' | '.join('---' for _ in columns) + ' |',
    ]
    for row in rows:
        values = []
        for col in columns:
            cell = _format_value(row.get(col), col).replace('\n', ' ').replace('|', '\\|')
            values.append(cell)
        lines.append('| ' + ' | '.join(values) + ' |')
    return '\n'.join(lines)


def render_plaintext_table(rows: list[dict], columns: Optional[list[str]]= None) -> str:
    if not rows:
        return '暂无结果'
    columns = columns or [
        'channelName', 'fans', 'avgViews', 'avgEngagementRate', 'platform',
        'gmv30d', 'originalLink', 'tags', 'wotohubLink', 'advantages'
    ]
    headers = {
        'rank': '排名',
        'channelName': '频道名',
        'fans': '粉丝数',
        'avgViews': '平均观看量',
        'avgEngagementRate': '平均互动率',
        'platform': '平台',
        'wotohubCategory': 'WotoHub分类',
        'wotohubScore': 'WotoHub评分',
        'country': '国家',
        'gmv30d': '近30天GMV',
        'originalLink': '博主主页',
        'wotohubLink': 'WotoHub分析',
        'tags': '标签',
        'advantages': '优势',
        'besId': 'besId',
        'matchScore': '匹配分',
        'matchTier': '匹配等级',
    }
    widths = {col: len(headers.get(col, col)) for col in columns}
    formatted_rows = []
    for row in rows:
        formatted = {col: _format_value(row.get(col), col).replace('\n', ' ') for col in columns}
        formatted_rows.append(formatted)
        for col in columns:
            widths[col] = min(max(widths[col], len(formatted[col])), 80)
    header_line = ' | '.join(headers.get(col, col).ljust(widths[col]) for col in columns)
    sep_line = '-+-'.join('-' * widths[col] for col in columns)
    body_lines = []
    for row in formatted_rows:
        body_lines.append(' | '.join(row[col][:widths[col]].ljust(widths[col]) for col in columns))
    return '\n'.join([header_line, sep_line, *body_lines])


def build_relaxation_suggestions(payload: dict) -> list[str]:
    suggestions = []
    if payload.get('hasEmail'):
        suggestions.append('可先取消“必须有邮箱”筛选，扩大召回后再二次筛选')
    if payload.get('minFansNum'):
        suggestions.append('可适当降低最低粉丝门槛，例如从当前值下调 30%-50%')
    if payload.get('advancedKeywordList'):
        suggestions.append('可减少关键词数量，只保留 1-2 个核心关键词')
    if payload.get('blogCateIds'):
        suggestions.append('可放宽 WotoHub 分类，先保留一级/二级类目')
    if payload.get('regionList'):
        suggestions.append('可放宽国家范围，先测试相近市场或去掉地区限制')
    if payload.get('blogLangs'):
        suggestions.append('可放宽语言限制，优先保留英语或目标市场主语言')
    if not suggestions:
        suggestions.append('可放宽平台、地区、粉丝量或关键词条件后重试')
    return suggestions[:4]


def render_priority_recommendations(scored: list[dict], limit: int = 10) -> str:
    if not scored:
        return '暂无优先推荐结果'

    intro = f"我已经先跑出一批候选博主，下面这 {min(len(scored), limit)} 个里有几位是更值得优先看的："
    blocks = []
    for item in scored[:limit]:
        reasons = item.get('matchReasons') or []
        reason_text = '；'.join(str(x).strip() for x in reasons[:3] if str(x).strip()) or '综合匹配度较高'
        fans = _format_value(item.get('fansNum'), 'fans')
        interactive = _format_value(item.get('interactiveRate'), 'avgEngagementRate')
        gmv = _format_value(item.get('gmv30d'), 'gmv30d')
        homepage = item.get('originalLink') or item.get('link') or '-'
        wotohub_link = item.get('wotohubLink') or '-'
        bes_id = item.get('besId') or '-'
        action = item.get('matchTier') or '观察'
        lines = [
            str(item.get('nickname') or '未知博主'),
            '',
            f'建议动作：{action}',
            f'粉丝：{fans}',
            f'平均互动率：{interactive}',
        ]
        if gmv not in ('-', '0'):
            lines.append(f'近30日 GMV：{gmv}')
        lines.extend([
            f'主页：{homepage}',
            f'WotoHub 分析：{wotohub_link}',
            f'besId：{bes_id}',
            f'理由：{reason_text}',
        ])
        blocks.append('\n'.join(lines))

    return intro + '\n\n' + '\n\n'.join(blocks)


def rank_recommendations(search_output: dict) -> tuple[list[dict], list[dict], dict]:
    """Recall 已结束后，对候选达人做排序与展示素材准备。

    语义/检索召回层与排序层在这里做轻量职责分离：
    - search API / fallback 属于 recall
    - score / fit / risk / 展示素材属于 ranking
    """
    payload = search_output.get('payload', {})
    raw_items = extract_blogger_items(search_output)
    scored = [score_influencer(item, payload) for item in raw_items[:RECOMMENDATION_MAX_ITEMS]]
    scored.sort(key=lambda x: x['matchScore'], reverse=True)
    return raw_items, scored, payload


def enrich_recommendations(search_output: dict) -> dict:
    raw_items, scored, payload = rank_recommendations(search_output)
    table_rows = []
    for idx, item in enumerate(scored, 1):
        reasons = item.get('matchReasons') or []
        fit_signals = item.get('fitSignals') or []
        risk_signals = item.get('riskSignals') or []
        fit_text = '；'.join(str(x).strip() for x in fit_signals[:2] if str(x).strip())
        risk_text = '；'.join(str(x).strip() for x in risk_signals[:2] if str(x).strip())
        advantages_parts = [str(x).strip() for x in reasons[:3] if str(x).strip()]
        if fit_text:
            advantages_parts.append(f"fit={fit_text}")
        if risk_text:
            advantages_parts.append(f"risk={risk_text}")
        advantages = '；'.join(advantages_parts) or '基础执行排序结果'
        username = _pick_first(item.get('raw', {}), 'username', 'uniqueId', 'handle') or item.get('nickname')
        table_rows.append({
            'rank': idx,
            'channelName': username,
            'fans': item.get('fansNum'),
            'avgViews': item.get('avgViews'),
            'avgEngagementRate': item.get('interactiveRate'),
            'platform': _pick_first(item.get('raw', {}), 'platform', default=payload.get('platform')),
            'wotohubCategory': item.get('category'),
            'wotohubScore': item.get('wotohubScore'),
            'country': item.get('country') or item.get('region'),
            'gmv30d': item.get('gmv30d'),
            'originalLink': item.get('originalLink') or item.get('link'),
            'tags': item.get('tagList') or [],
            'wotohubLink': item.get('wotohubLink'),
            'advantages': advantages,
            'besId': item.get('besId'),
            'matchScore': item.get('matchScore'),
            'matchTier': item.get('matchTier'),
        })
    display = build_recommendation_display(table_rows, scored, payload)
    return {
        'count': len(scored),
        'recallCount': len(raw_items),
        'rankingMode': 'script-first',
        'recommendationLayers': {
            'recall': 'search_api_result',
            'ranking': 'score_influencer',
            'presentation': 'build_recommendation_display',
        },
        'topRecommendations': scored[:10],
        'tableRows': table_rows,
        'tableColumns': display['tableColumns'],
        'summary': display['summary'],
        'priorityText': display['priorityText'],
        'markdownTable': display['markdownTable'],
        'plainTextTable': display['plainTextTable'],
        'markdownDisplayText': display['markdownDisplayText'],
        'plainTextDisplay': display['plainTextDisplay'],
        'displayText': display['displayText'],
        'emptyState': display['emptyState'],
    }


def main():
    ap = argparse.ArgumentParser(description="Call WotoHub search API")
    ap.add_argument("--token")
    ap.add_argument("--payload-file", help="JSON file from build_search_payload.py; accepts full result or payload-only JSON")
    ap.add_argument("--platform")
    ap.add_argument("--page-num", type=int, default=1)
    ap.add_argument("--page-size", type=int, default=20,
                    help="results per page (default: 20; increase for more results)")
    ap.add_argument("--min-fans", type=int)
    ap.add_argument("--max-fans", type=int)
    ap.add_argument("--min-interactive-rate", type=int)
    ap.add_argument("--has-email", action="store_true")
    ap.add_argument("--sort")
    ap.add_argument("--sort-order", choices=["asc", "desc"])
    ap.add_argument("--lang", action="append")
    ap.add_argument("--cate", action="append")
    ap.add_argument("--region", action="append")
    ap.add_argument("--keyword", action="append", help="advanced keyword; can be repeated")
    ap.add_argument("--exclude-contacted", action="store_true",
                    help="filter out bloggers already contacted (requires token, uses searchFilterList)")
    ap.add_argument("--retry-fallbacks", action="store_true", help="retry with semantic smaller payload variants when first search fails")
    ap.add_argument("--debug", action="store_true", help="include attempted payload variants and recommendation scoring")
    args = ap.parse_args()

    # ── Page-size tip ──────────────────────────────────────────────────────────
    if args.page_size == 20:
        print("# [TIP] page-size 默认为 20条，数据量较少。", file=sys.stderr)
        print("#       如需更多结果，请使用 --page-size 50 或 --page-size 200。", file=sys.stderr)
        print("#       例如：python3 scripts/claw_search.py --token YOUR_API_KEY --page-size 50 ...", file=sys.stderr)

    token = get_token(args.token, required=False)
    path = claw_search_path() if token else open_search_path()

    payload = load_payload_arg(args.payload_file)
    if payload is None:
        if not args.platform:
            ap.error('either --payload-file, stdin payload, or --platform is required')
        payload = build_payload_from_args(args)

    payload = normalize_search_payload(payload)

    # ── Exclude contacted bloggers ─────────────────────────────────────────────
    if args.exclude_contacted:
        if not token:
            print("# [WARNING] --exclude-contacted requires --token; ignoring filter.", file=sys.stderr)
        else:
            payload['searchFilterList'] = ['THIS_UNTOUCH']

    attempts = []
    first = execute_search(path, token, payload)
    attempts.append({'label': 'initial', 'reason': '原始 payload', 'payload': payload, 'result': first.get('result')})
    best_output = first

    if args.retry_fallbacks and not is_search_success(first.get('result', {})):
        # 优先使用错误驱动的精准回退；若无可用策略则降级到通用语义回退
        if any(
            _error_tag(first.get('result', {}))[0] != "UNKNOWN"
            for _ in (first,)
        ):
            fallback_fn = build_error_driven_fallbacks
        else:
            fallback_fn = build_semantic_fallbacks

        for variant in fallback_fn(payload, first.get('result', {})):
            current = execute_search(path, token, variant['payload'])
            attempts.append({
                'label': variant['label'],
                'reason': variant['reason'],
                'payload': variant['payload'],
                'result': current.get('result'),
            })
            best_output = current
            if is_search_success(current.get('result', {})):
                break

    output = dict(best_output)
    recommendations = enrich_recommendations(best_output)
    output['recommendations'] = recommendations
    output['markdownTable'] = recommendations.get('markdownTable')
    output['plainTextTable'] = recommendations.get('plainTextTable')
    output['summary'] = recommendations.get('summary')
    output['displayText'] = recommendations.get('displayText')
    if args.debug:
        output['attempts'] = attempts
        output['recommendationPreview'] = recommendations
    print_json(output)


if __name__ == "__main__":
    main()
