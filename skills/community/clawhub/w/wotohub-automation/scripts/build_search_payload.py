#!/usr/bin/env python3
import argparse
import html
import json
import os
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional, Union
from urllib.parse import urlparse

import claw_search
# product_resolve imported locally to avoid circular import
from semantic_layer import SemanticLayer
from category_inference import load_categories, build_category_ids, map_semantic_labels_to_category_ids, map_semantic_labels_with_scores
from query_constraints import load_region_keywords, load_lang_keywords, infer_regions, infer_languages, infer_values, infer_sort, build_region_list

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEARCH_PAGE_SIZE = 50
MAX_SEARCH_PAGE_SIZE = 200

DOMAIN_PLATFORM_MAP = {
    'tiktok.com': 'tiktok',
    'shop.tiktok.com': 'tiktok',
    'amazon.com': 'amazon',
    'amazon.co.uk': 'amazon',
    'amazon.de': 'amazon',
    'amazon.co.jp': 'amazon',
    'myshopify.com': 'shopify',
}




def unique_keep_order(items):
    out = []
    seen = set()
    for item in items:
        # Skip empty/null sentinels
        if item is None:
            continue
        if isinstance(item, str):
            item = item.strip()
            if not item:
                continue
            key = item  # string itself is hashable
        elif isinstance(item, (int, float, bool)):
            key = item  # primitives are hashable
        elif isinstance(item, (dict, list)):
            # dict/list are unhashable → serialize to stable string key
            try:
                key = json.dumps(item, ensure_ascii=False, sort_keys=True)
            except Exception:
                key = str(item)
        else:
            # fallback for other unhashable types
            key = str(item)

        # Skip empty containers after normalization
        if isinstance(key, str) and not key:
            continue

        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def _keyword_value(item: Any) -> tuple[str, bool]:
    if isinstance(item, dict):
        return str(item.get('value') or '').strip(), bool(item.get('exclude', False))
    return str(item or '').strip(), False


BROAD_KEYWORD_TOKENS = {
    'lifestyle', 'family', 'daily use', 'useful', 'quality', 'premium',
    'innovative', 'creator', 'influencer', 'blogger', 'content', 'video'
}

SEARCH_JUNK_PATTERNS = [
    r'\bwith email\b',
    r'\b(has|with) emails?\b',
    r'\bconsumer product\b',
    r'\bproduct from url\b',
    r'\bcreator(s)?\b',
    r'\binfluencer(s)?\b',
    r'\bblogger(s)?\b',
    r'\breviewer(s)?\b',
    r'\bchannel(s)?\b',
    r'\bvideo(s)?\b',
    r'\bminutes?\b',
    r'\bfind\b',
    r'\blooking for\b',
    r'\bpaid collaboration\b',
    r'\baffiliate\b',
    r'\bsample\b',
    r'帮我',
    r'最合适',
    r'这个skill',
    r'wotohub-automation',
    r'找一批',
]

FEATURE_SELLING_POINT_PATTERNS = [
    r'\b\d+\s*(w|wh|mah|ah|v|mph)\b',
    r'\bhydraulic brakes?\b',
    r'\bfat tire(s)?\b',
    r'\bbattery\b',
    r'\bspeed\b',
    r'\bpower\b',
    r'\btorque\b',
]

CONTENT_SEARCH_TOKENS = {
    'review', 'reviews', 'test ride', 'riding', 'ride', 'comparison', 'unboxing',
    'tutorial', 'motocross', 'powersports', 'gear', 'outdoor', 'trail'
}

HIGH_SIGNAL_SINGLE_TERMS = {'powersports', 'motocross', 'trail'}
GENERIC_CONTENT_TERMS = {'review', 'reviews', 'ride', 'riding', 'gear', 'outdoor'}


def _is_searchable_keyword(term: str) -> bool:
    text = re.sub(r'\s+', ' ', str(term or '').strip().lower())
    if not text:
        return False
    if text in BROAD_KEYWORD_TOKENS:
        return False
    if len(text) > 48:
        return False
    if any(re.search(pattern, text) for pattern in SEARCH_JUNK_PATTERNS):
        return False
    if any(re.search(pattern, text) for pattern in FEATURE_SELLING_POINT_PATTERNS):
        return False
    if re.search(r'\b\d+\s*[-–]?\s*\d*\s*(min|mins|minute|minutes)\b', text):
        return False
    token_len = len(text.split())
    if token_len >= 5:
        return False
    if token_len == 1 and text in GENERIC_CONTENT_TERMS:
        return False
    if token_len >= 4 and not any(token in text for token in ['review', 'ebike', 'e-bike', 'dirt bike', 'motorcycle', 'test ride', 'motocross', 'powersports']):
        return False
    return True


def _keyword_priority(term: str) -> tuple[int, int, int]:
    text = (term or '').strip().lower()
    if not text:
        return (99, 99, 99)
    token_len = len(text.split())
    has_content_signal = any(token in text for token in CONTENT_SEARCH_TOKENS)
    if text in BROAD_KEYWORD_TOKENS:
        return (6, token_len, 99)
    if token_len == 1 and text in HIGH_SIGNAL_SINGLE_TERMS:
        return (1, 0, -len(text))
    if has_content_signal and 1 < token_len <= 3:
        return (0, token_len, -len(text))
    if token_len == 2:
        return (2, 0, -len(text))
    if token_len == 1:
        return (3, 0, -len(text))
    if token_len == 3:
        return (4, 0, -len(text))
    return (5, token_len, -len(text))


def to_advanced_keywords(keywords: list[str]) -> list[dict]:
    return focus_advanced_keywords(keywords, limit=8)


def focus_advanced_keywords(keywords: list[Any], limit: int = 5) -> list[dict]:
    focused: list[dict] = []
    seen = set()
    candidates = []
    for item in unique_keep_order(keywords):
        value, exclude = _keyword_value(item)
        if not value:
            continue
        normalized = re.sub(r'\s+', ' ', value.strip().lower())
        if normalized in seen:
            continue
        seen.add(normalized)
        if not _is_searchable_keyword(value):
            continue
        candidates.append({'value': value, 'exclude': exclude})

    for item in sorted(candidates, key=lambda x: _keyword_priority(x['value'])):
        focused.append(item)
        if len(focused) >= limit:
            break
    return focused


def _normalize_explicit_codes(values: Union[list[Any], Any], mapping: dict[str, str]) -> list[str]:
    if values in (None, '', [], {}):
        return []
    if not isinstance(values, list):
        values = [values]
    out = []
    for value in values:
        raw = str(value or '').strip()
        if not raw:
            continue
        key = raw.lower()
        normalized = mapping.get(key) or mapping.get(re.sub(r'[\s（）()\-_/]+', '', key)) or key
        if normalized not in out:
            out.append(normalized)
    return out


def normalize_platform(platform: Optional[str], source_host: Optional[str]= None) -> str:
    candidate = (platform or '').strip().lower()
    creator_platforms = {'tiktok', 'youtube', 'instagram'}
    if candidate in creator_platforms:
        return candidate
    host = (source_host or '').lower()
    for suffix, mapped in DOMAIN_PLATFORM_MAP.items():
        if (host == suffix or host.endswith('.' + suffix)) and mapped in creator_platforms:
            return mapped
    return 'tiktok'


def infer_platform_from_url_or_host(raw: Optional[str], source_host: Optional[str]= None) -> Optional[str]:
    host = (source_host or '').lower()
    if not host and raw:
        try:
            host = urlparse(raw).netloc.lower()
        except Exception:
            host = ''
    for suffix, mapped in DOMAIN_PLATFORM_MAP.items():
        if host == suffix or host.endswith('.' + suffix):
            return mapped
    return None




def build_keyword_list_from_analysis(analysis: dict) -> list[str]:
    product = analysis.get('productSummary', {})
    search = analysis.get('searchConditions', {})
    marketing = analysis.get('marketing', {}) or {}
    model_product = analysis.get('product', {}) or {}

    raw = []
    raw.extend(search.get('keywords', []))
    raw.extend(marketing.get('contentAngles', []))
    raw.extend(product.get('creatorAngles', []))
    raw.extend(product.get('detectedForms', []))
    raw.extend(product.get('categoryForms', []))
    raw.extend(marketing.get('creatorTypes', []))
    raw.extend([model_product.get('productSubtype'), model_product.get('productType')])
    return unique_keep_order([x for x in raw if x not in (None, '', [], {})])[:12]


def extract_semantic_keywords(semantic: Optional[dict]) -> list[str]:
    if not semantic:
        return []
    clusters = semantic.get('semanticBrief', {}).get('keyword_clusters', {})
    ordered = []
    for key in ('core', 'benefit', 'scenario', 'creator'):
        item = clusters.get(key) or {}
        ordered.extend(item.get('value') or [])
    return unique_keep_order(ordered)[:12]




def merge_category_ids(query: str, analysis: dict, data, by_code, children, category_index, allow_query_inference: bool = False):
    """Merge category ids conservatively.

    Primary path: trust model/analysis output.
    Optional weak fallback: allow query/category inference only when explicitly enabled.
    """
    analysis_ids = analysis.get('searchConditions', {}).get('blogCateIds', [])
    if analysis_ids:
        return unique_keep_order(analysis_ids), []
    if not allow_query_inference:
        return [], []
    inferred_ids, matches = build_category_ids(query, data, by_code, category_index)
    merged = unique_keep_order(inferred_ids)
    return merged, matches


EXPLORATORY_QUERY_TOKENS = {
    'broad', 'broad search', 'explore', 'exploration', 'discovery', 'discover',
    '广搜', '宽搜', '探索', '先试试', '先跑一批', '先广撒网', '不限类目'
}


def _coerce_list(value: Any) -> list[str]:
    if value in (None, '', [], {}):
        return []
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    text = str(value).strip()
    return [text] if text else []


def _is_category_like_signal(value: str) -> bool:
    text = str(value or '').strip().lower()
    if not text:
        return False
    normalized = re.sub(r'\s+', ' ', text)
    if len(normalized) > 48:
        return False
    noisy_tokens = ['帮我', '推荐', '找', '达人', '红人', 'creator', 'influencer', 'tiktok', 'youtube', '美国', '英国', '推广']
    noisy_hit_count = sum(1 for token in noisy_tokens if token in normalized)
    if noisy_hit_count >= 2:
        return False
    if noisy_hit_count >= 1 and (len(normalized) >= 18 or len(normalized.split()) >= 4):
        return False
    return True


def build_semantic_input_from_model_analysis(model_analysis: Optional[dict]) -> dict:
    model_analysis = model_analysis or {}
    product = model_analysis.get('product') or {}
    marketing = model_analysis.get('marketing') or {}
    constraints = model_analysis.get('constraints') or {}

    def _value(values: Any) -> dict:
        normalized = _coerce_list(values)
        return {'value': normalized} if normalized else {}

    return {
        'semanticBrief': {
            'product': {
                'category_forms': _value([
                    *(_coerce_list(product.get('categoryForms'))),
                    *(_coerce_list(product.get('productSubtype'))),
                    *(_coerce_list(product.get('productType'))),
                ]),
                'functions': _value(product.get('functions') or product.get('coreBenefits') or product.get('features')),
            },
            'keyword_clusters': {
                'core': _value([
                    *(_coerce_list(product.get('productName'))),
                    *(_coerce_list(product.get('productSubtype'))),
                    *(_coerce_list(product.get('productType'))),
                    *(_coerce_list(product.get('categoryForms'))),
                ]),
                'benefit': _value(product.get('coreBenefits') or product.get('features') or product.get('functions')),
                'creator': _value(marketing.get('creatorTypes') or marketing.get('contentAngles')),
            },
            'constraints': {
                'regions': _value(constraints.get('regions')),
                'languages': _value(constraints.get('languages')),
                'has_email': {'value': constraints.get('hasEmail')} if constraints.get('hasEmail') is not None else {},
                'min_fans': {'value': constraints.get('minFansNum')} if constraints.get('minFansNum') is not None else {},
                'max_fans': {'value': constraints.get('maxFansNum')} if constraints.get('maxFansNum') is not None else {},
            },
            'marketing': {
                'creator_types': _value(marketing.get('creatorTypes') or marketing.get('contentAngles')),
            },
        },
        'strategies': [],
    }


def should_expect_category_mapping(analysis: Optional[dict], semantic: Optional[dict]= None, query: Optional[str]= None) -> bool:
    analysis = analysis or {}
    search = analysis.get('searchConditions', {}) or {}
    product = analysis.get('productSummary', {}) or {}
    model_product = analysis.get('product', {}) or {}
    semantic_brief = (semantic or {}).get('semanticBrief', {}) if isinstance(semantic, dict) else {}
    semantic_product = semantic_brief.get('product', {}) or {}
    keyword_clusters = semantic_brief.get('keyword_clusters', {}) or {}
    clarifications = analysis.get('clarificationsNeeded') or []

    if unique_keep_order(search.get('blogCateIds', []) or []):
        return True

    query_l = (query or '').lower()
    if any(token in query_l for token in EXPLORATORY_QUERY_TOKENS):
        return False

    clarification_fields = {
        str(item.get('field') or '').strip().lower()
        for item in clarifications
        if isinstance(item, dict)
    }
    if 'productsemantics' in clarification_fields:
        has_explicit_category_semantics = any([
            _coerce_list(model_product.get('productType')),
            _coerce_list(model_product.get('productSubtype')),
            _coerce_list(model_product.get('categoryForms')),
            _coerce_list(product.get('productTypeHint')),
            _coerce_list(product.get('detectedForms')),
            _coerce_list((semantic_product.get('category_forms') or {}).get('value')),
        ])
        if not has_explicit_category_semantics:
            return False

    structured_signals = [
        *(_coerce_list(model_product.get('productType'))),
        *(_coerce_list(model_product.get('productSubtype'))),
        *(_coerce_list(model_product.get('categoryForms'))),
        *(_coerce_list(product.get('productTypeHint'))),
        *(_coerce_list(product.get('detectedForms'))),
        *(_coerce_list((semantic_product.get('category_forms') or {}).get('value'))),
        *(_coerce_list((semantic_product.get('functions') or {}).get('value'))),
        *(_coerce_list((keyword_clusters.get('core') or {}).get('value'))),
        *(_coerce_list((keyword_clusters.get('benefit') or {}).get('value'))),
    ]
    structured_signals = [item for item in structured_signals if len(item) >= 2 and _is_category_like_signal(item)]
    if not structured_signals:
        return False

    return True


def resolve_category_strategy(analysis: dict, semantic: Optional[dict], query: str, data, by_code, children=None, category_index=None, args=None) -> dict:
    search = analysis.get('searchConditions', {}) or {}
    if category_index is None and isinstance(children, dict):
        category_index = children
    explicit_ids = unique_keep_order(search.get('blogCateIds', []) or [])
    if explicit_ids:
        return {
            'status': 'resolved',
            'strategy': 'category_plus_keyword',
            'confidenceLevel': 'high',
            'mustApplyBlogCateIds': True,
            'categoryMappingExpected': True,
            'reasonSummary': 'analysis provided explicit blogCateIds',
            'mapping': {
                'selectedBlogCateIds': explicit_ids,
                'matchedCategories': [],
                'mappingWarnings': [],
                'mappingErrors': [],
            },
            'decision': {
                'applyBlogCateIds': True,
                'applyKeywordSearch': True,
                'keywordRole': 'refinement',
                'categoryRole': 'primary_filter',
                'preferredDepth': 'level_2',
                'maxCategoryCount': 2,
                'fallbackMode': 'broad_category_plus_keyword',
            },
        }

    semantic_resolution = map_semantic_labels_with_scores(semantic, data, by_code, category_index)
    strategy = semantic_resolution.get('strategy', 'keyword_only')
    confidence = semantic_resolution.get('confidenceLevel', 'low')
    selected = semantic_resolution.get('selectedBlogCateIds', [])
    category_expected = should_expect_category_mapping(analysis, semantic, query=query)

    if strategy == 'category_plus_keyword':
        status = 'resolved'
        reason = 'high-confidence semantic category mapping'
        preferred_depth = 'level_2'
    elif strategy == 'broad_category_plus_keyword':
        status = 'partially_resolved'
        reason = 'medium-confidence category mapping; use broad category with keywords'
        preferred_depth = 'level_1'
    elif category_expected:
        status = 'blocked'
        reason = 'category mapping expected from semantic input, but no stable blogCateIds were produced'
        preferred_depth = 'level_1'
    else:
        status = 'keyword_only'
        reason = 'no stable category mapping; rely on keyword search'
        preferred_depth = 'level_1'

    return {
        'status': status,
        'strategy': strategy,
        'confidenceLevel': confidence,
        'mustApplyBlogCateIds': bool(semantic_resolution.get('mustApplyBlogCateIds')) or bool(category_expected),
        'categoryMappingExpected': bool(category_expected),
        'reasonSummary': reason,
        'modelCategoryIntent': {
            'candidateCategoryLabels': semantic_resolution.get('candidateCategoryLabels', []),
            'primaryCategoryLabel': (semantic_resolution.get('candidateCategoryLabels') or [None])[0],
            'secondaryCategoryLabels': (semantic_resolution.get('candidateCategoryLabels') or [])[1:3],
        },
        'mapping': {
            'matchedCategories': semantic_resolution.get('matchedCategories', []),
            'selectedBlogCateIds': selected[:2] if strategy == 'category_plus_keyword' else selected[:1],
            'mappingWarnings': semantic_resolution.get('mappingWarnings', []),
            'mappingErrors': ['category_mapping_missing'] if category_expected and not selected else [],
        },
        'decision': {
            'applyBlogCateIds': strategy in {'category_plus_keyword', 'broad_category_plus_keyword'} and bool(selected),
            'applyKeywordSearch': False if status == 'blocked' else True,
            'keywordRole': 'refinement' if strategy != 'keyword_only' else ('blocked_pending_category_mapping' if status == 'blocked' else 'primary_recall'),
            'categoryRole': 'primary_filter' if strategy == 'category_plus_keyword' else ('broad_filter' if strategy == 'broad_category_plus_keyword' else ('required_but_missing' if status == 'blocked' else 'disabled')),
            'preferredDepth': preferred_depth,
            'maxCategoryCount': 2,
            'fallbackMode': 'blocked_pending_category_mapping' if status == 'blocked' else ('keyword_only' if strategy == 'keyword_only' else 'broad_category_plus_keyword'),
        },
    }


def _resolve_page_size(raw_value: Optional[int]) -> int:
    try:
        value = int(raw_value or DEFAULT_SEARCH_PAGE_SIZE)
    except Exception:
        value = DEFAULT_SEARCH_PAGE_SIZE
    if value <= 0:
        value = DEFAULT_SEARCH_PAGE_SIZE
    return min(value, MAX_SEARCH_PAGE_SIZE)


def build_payload_from_analysis(query: str, analysis: dict, args, region_keywords, lang_keywords, data, by_code, children, category_index):
    # Sanitize HTML entities before any processing
    query = html.unescape(query)
    q = query.lower()
    product = analysis.get('productSummary', {})
    search = analysis.get('searchConditions', {})

    fallback_meta = analysis.get('fallback') or {}
    if fallback_meta.get('active'):
        return {
            'query': query,
            'matchedCategories': [],
            'payload': None,
            'analysis': {
                'productSummary': product,
                'searchConditions': search,
            },
            'fallback': fallback_meta,
            'needsUserInput': True,
        }

    # In input/analysis mode, prefer consuming analysis + semantic output.
    # Query-string inference should be a last-resort fallback, not the main path.
    allow_query_inference = bool(getattr(args, 'allow_query_inference', False))
    inferred_regions = infer_regions(q, region_keywords) if allow_query_inference else []
    inferred_langs = infer_languages(q, lang_keywords) if allow_query_inference else []
    blog_cate_ids, matches = merge_category_ids(query, analysis, data, by_code, children, category_index, allow_query_inference=allow_query_inference)

    resolved_platform = infer_platform_from_url_or_host(args.input, product.get('sourceHost') or analysis.get('sourceHost'))
    chosen_platform = args.platform
    if args.platform == 'auto':
        chosen_platform = resolved_platform or search.get('platforms', ['tiktok'])[0]

    semantic = None
    if getattr(args, 'semantic_mode', 'disabled') != 'disabled':
        semantic = build_semantic_input_from_model_analysis(analysis)

    semantic_constraints = (semantic or {}).get('semanticBrief', {}).get('constraints', {})
    semantic_regions = _normalize_explicit_codes((semantic_constraints.get('regions') or {}).get('value') or [], region_keywords)
    semantic_langs = _normalize_explicit_codes((semantic_constraints.get('languages') or {}).get('value') or [], lang_keywords)
    semantic_keywords = extract_semantic_keywords(semantic)
    semantic_category_ids, semantic_matches = map_semantic_labels_to_category_ids(semantic, data, by_code, category_index)
    category_resolution = resolve_category_strategy(analysis, semantic, query, data, by_code, children, category_index, args)

    # Prefer structured analysis / semantic output. Query-string inference is last fallback only.
    analysis_regions = _normalize_explicit_codes(product.get('regionHints') or search.get('regions') or [], region_keywords)
    analysis_langs = _normalize_explicit_codes(product.get('languageHints') or search.get('languages') or [], lang_keywords)
    explicit_regions = _normalize_explicit_codes(getattr(args, 'region', None), region_keywords)
    explicit_langs = _normalize_explicit_codes(getattr(args, 'lang', None), lang_keywords)
    explicit_ids = unique_keep_order(search.get('blogCateIds', []) or [])
    analysis_keywords = build_keyword_list_from_analysis(analysis)

    regions = explicit_regions or analysis_regions or semantic_regions or inferred_regions
    langs = explicit_langs or analysis_langs or semantic_langs or inferred_langs
    keywords = unique_keep_order([*semantic_keywords, *analysis_keywords])[:12]
    advanced_keywords = search.get('advancedKeywordList') or focus_advanced_keywords(keywords)

    payload = {
        'platform': normalize_platform(chosen_platform, product.get('sourceHost') or analysis.get('sourceHost')),
        'pageNum': args.page_num,
        'pageSize': _resolve_page_size(getattr(args, 'page_size', None)),
        'hasEmail': True,
        'searchFilterList': ['THIS_UNTOUCH'] if getattr(args, 'exclude_contacted', True) else [],
    }
    semantic_has_email = (semantic_constraints.get('has_email') or {}).get('value')
    if regions:
        payload['regionList'] = build_region_list(regions)
    if langs:
        payload['blogLangs'] = langs
    semantic_min_fans = (semantic_constraints.get('min_fans') or {}).get('value')
    semantic_max_fans = (semantic_constraints.get('max_fans') or {}).get('value')
    if args.has_email:
        payload['hasEmail'] = True
    elif semantic_has_email is not None:
        payload['hasEmail'] = bool(semantic_has_email)
    elif search.get('hasEmail') is not None:
        payload['hasEmail'] = bool(search.get('hasEmail'))

    if args.min_fans is not None:
        payload['minFansNum'] = args.min_fans
    elif semantic_min_fans is not None:
        payload['minFansNum'] = semantic_min_fans
    elif search.get('minFansNum') is not None:
        payload['minFansNum'] = search.get('minFansNum')
    if args.max_fans is not None:
        payload['maxFansNum'] = args.max_fans
    elif semantic_max_fans is not None:
        payload['maxFansNum'] = semantic_max_fans
    elif search.get('maxFansNum') is not None:
        payload['maxFansNum'] = search.get('maxFansNum')
    if args.min_interactive_rate is not None:
        payload['minInteractiveRate'] = args.min_interactive_rate
    selected_category_ids = category_resolution.get('mapping', {}).get('selectedBlogCateIds', [])
    if category_resolution.get('decision', {}).get('applyBlogCateIds') and selected_category_ids:
        payload['blogCateIds'] = unique_keep_order(selected_category_ids)

    resolved_match_items = category_resolution.get('mapping', {}).get('matchedCategories') or []
    if resolved_match_items:
        matched_categories_output = [
            {
                'dictValue': m.get('displayName') or m.get('dictValue'),
                'dictCode': m.get('blogCateId') or m.get('dictCode'),
                'level': m.get('level') or m.get('col2'),
                'parent': m.get('parent') or m.get('col3'),
                'source': m.get('source'),
                'label': m.get('label'),
                'score': m.get('score'),
            }
            for m in resolved_match_items[:10]
        ]
    else:
        matched_categories_output = [
            {
                'dictValue': m.get('dictValue'),
                'dictCode': m.get('dictCode'),
                'level': m.get('col2'),
                'parent': m.get('col3'),
            }
            for m in unique_keep_order([*semantic_matches, *matches])[:10]
        ]

    if category_resolution.get('status') == 'blocked':
        return {
            'query': query,
            'matchedCategories': matched_categories_output,
            'payload': None,
            'analysis': {
                'productSummary': product,
                'searchConditions': search,
            },
            'categoryResolution': category_resolution,
            'payloadMode': category_resolution.get('strategy'),
            'payloadDecisionSummary': {
                'blogCateIdsApplied': False,
                'advancedKeywordListApplied': False,
                'reason': category_resolution.get('reasonSummary'),
            },
            'payloadProvenance': {
                'fallbackApplied': False,
                'fallbackReason': 'category_mapping_missing',
                'strategy': category_resolution.get('strategy'),
            },
            'needsUserInput': True,
            'error': {
                'code': 'CATEGORY_MAPPING_REQUIRED',
                'message': 'This search should produce blogCateIds first. Refine host semantic category labels or product type before using advancedKeywordList as refinement.',
                'details': {
                    'candidateCategoryLabels': category_resolution.get('modelCategoryIntent', {}).get('candidateCategoryLabels') or [],
                    'mappingWarnings': category_resolution.get('mapping', {}).get('mappingWarnings') or [],
                },
            },
        }

    if category_resolution.get('decision', {}).get('applyKeywordSearch') and advanced_keywords:
        keyword_limit = 5 if category_resolution.get('strategy') == 'category_plus_keyword' else 8
        payload['searchType'] = 'KEYWORD'
        payload['advancedKeywordList'] = advanced_keywords[:keyword_limit]

    payload_provenance = {
        'platform': 'analysis_explicit' if resolved_platform or search.get('platforms') else 'default',
        'regions': 'explicit_args' if explicit_regions else ('analysis_explicit' if analysis_regions else ('semantic_constraints' if semantic_regions else ('query_inference' if inferred_regions else 'default'))),
        'languages': 'explicit_args' if explicit_langs else ('analysis_explicit' if analysis_langs else ('semantic_constraints' if semantic_langs else ('query_inference' if inferred_langs else 'default'))),
        'keywords': 'analysis_search_hints' if analysis_keywords else ('semantic_keyword_clusters' if semantic_keywords else 'fallback'),
        'blogCateIds': 'analysis_explicit' if explicit_ids else ('semantic_category_resolution' if selected_category_ids else ('query_inference' if blog_cate_ids else 'disabled')),
        'minFansNum': 'explicit_args' if args.min_fans is not None else ('semantic_constraints' if semantic_min_fans is not None else ('analysis_explicit' if search.get('minFansNum') is not None else 'default')),
        'maxFansNum': 'explicit_args' if args.max_fans is not None else ('semantic_constraints' if semantic_max_fans is not None else ('analysis_explicit' if search.get('maxFansNum') is not None else 'default')),
        'hasEmail': 'explicit_args' if args.has_email else ('semantic_constraints' if semantic_has_email is not None else ('analysis_explicit' if search.get('hasEmail') is not None else 'default')),
        'searchType': 'keyword_strategy' if payload.get('advancedKeywordList') else ('category_only' if payload.get('blogCateIds') else 'default'),
        'fallbackApplied': False,
        'fallbackReason': None,
        'strategy': category_resolution.get('strategy'),
    }

    result = {
        'query': query,
        'matchedCategories': matched_categories_output,
        'payload': payload,
        'analysis': {
            'productSummary': product,
            'searchConditions': search,
        },
        'categoryResolution': category_resolution,
        'payloadMode': category_resolution.get('strategy'),
        'payloadDecisionSummary': {
            'blogCateIdsApplied': bool(payload.get('blogCateIds')),
            'advancedKeywordListApplied': bool(payload.get('advancedKeywordList')),
            'reason': category_resolution.get('reasonSummary'),
        },
        'payloadProvenance': payload_provenance,
    }
    if semantic:
        result['semantic'] = semantic
        preferred = next((s for s in semantic.get('strategies', []) if s.get('name') == getattr(args, 'strategy', 'balanced')), None)
        if preferred:
            strategy_payload = preferred.get('payloadDraft') or {}
            result['payloadFromStrategy'] = strategy_payload
            merged_payload = dict(payload)
            # Let strategy fill blanks and gently override soft fields, but keep explicit query/arg constraints authoritative.
            for key, value in strategy_payload.items():
                if key not in merged_payload or merged_payload.get(key) in (None, [], {}):
                    merged_payload[key] = value
                elif key in {'advancedKeywordList', 'blogCateIds'} and value:
                    merged_payload[key] = value
                elif key in {'minFansNum', 'maxFansNum'} and getattr(args, 'min_fans' if key == 'minFansNum' else 'max_fans', None) is None:
                    merged_payload[key] = value
            if strategy_payload.get('searchType') and merged_payload.get('advancedKeywordList'):
                merged_payload['searchType'] = strategy_payload['searchType']
            result['payload'] = merged_payload
    return result


def run_search(payload: dict, token: Optional[str]= None, retry_fallbacks: bool = False, debug: bool = False) -> dict:
    path = claw_search.claw_search_path() if token else claw_search.open_search_path()
    attempts = []
    first = claw_search.execute_search(path, token, payload)
    attempts.append({'label': 'initial', 'reason': '原始 payload', 'payload': payload, 'result': first.get('result')})
    best_output = first

    if retry_fallbacks and not claw_search.is_search_success(first.get('result', {})):
        for variant in claw_search.build_semantic_fallbacks(payload):
            current = claw_search.execute_search(path, token, variant['payload'])
            attempts.append({
                'label': variant['label'],
                'reason': variant['reason'],
                'payload': variant['payload'],
                'result': current.get('result'),
            })
            best_output = current
            if claw_search.is_search_success(current.get('result', {})):
                break

    output = dict(best_output)
    if debug:
        output['attempts'] = attempts
        output['recommendationPreview'] = claw_search.enrich_recommendations(best_output)
    return output


def _ensure_router_executor_defaults() -> None:
    try:
        from router_launcher_env import ensure_router_executor_env
    except Exception:
        return
    os.environ.update(ensure_router_executor_env(skill_root=ROOT, env=os.environ))



def _try_resolve_url_fallback_via_host_executor(raw_input: str, resolved: dict) -> tuple[Optional[dict], Optional[dict], Optional[dict]]:
    host_request = (resolved or {}).get('hostUrlAnalysisRequest')
    if not isinstance(host_request, dict) or not host_request:
        return None, None, None

    try:
        from orchestrator import UpperLayerOrchestrator
    except Exception as exc:
        return None, None, {
            'code': 'HOST_ANALYSIS_BRIDGE_IMPORT_FAILED',
            'message': f'Failed to import orchestrator bridge: {exc}',
            'details': {'hostUrlAnalysisRequest': host_request},
        }

    orchestrator = UpperLayerOrchestrator(token=None)
    executor = orchestrator._get_host_analysis_executor(config={})
    if not executor:
        return None, None, {
            'code': 'HOST_ANALYSIS_EXECUTOR_MISSING',
            'message': 'URL fallback produced hostUrlAnalysisRequest, but no host analysis executor is configured.',
            'details': {'hostUrlAnalysisRequest': host_request},
        }

    try:
        payload = orchestrator._run_host_analysis_executor(request=host_request, executor_spec=executor)
        extracted = orchestrator._extract_host_analysis_payload(payload)
        analysis = extracted.get('analysis')
        product_summary = extracted.get('productSummary')
        if not isinstance(analysis, dict) or not analysis:
            return None, None, {
                'code': 'HOST_ANALYSIS_EXECUTOR_EMPTY',
                'message': 'Host analysis executor ran but returned no usable analysis payload.',
                'details': {
                    'executor': orchestrator._describe_executor(executor),
                    'hostUrlAnalysisRequest': host_request,
                },
            }

        import product_resolve
        rewritten = product_resolve.resolve_product(
            raw_input,
            timeout=0,
            host_analysis=analysis,
            product_summary=product_summary,
        )
        return rewritten.get('analysis'), rewritten.get('productSummary'), None
    except Exception as exc:
        return None, None, {
            'code': 'HOST_ANALYSIS_EXECUTOR_FAILED',
            'message': f'Host analysis executor failed: {exc}',
            'details': {'hostUrlAnalysisRequest': host_request},
        }



def main():
    ap = argparse.ArgumentParser(description='Build clawSearch payload from natural language hints or resolved product input')
    ap.add_argument('--query', help='natural language search query')
    ap.add_argument('--input', help='product url or product description; resolves product first and then builds payload')
    ap.add_argument('--platform', default='auto')
    ap.add_argument('--page-num', type=int, default=1)
    ap.add_argument('--page-size', type=int, default=DEFAULT_SEARCH_PAGE_SIZE)
    ap.add_argument('--has-email', action='store_true')
    ap.add_argument('--region', action='append')
    ap.add_argument('--lang', action='append')
    ap.add_argument('--min-fans', type=int)
    ap.add_argument('--max-fans', type=int)
    ap.add_argument('--min-interactive-rate', type=int)
    ap.add_argument('--resolve-timeout', type=int, default=20)
    ap.add_argument('--semantic-mode', choices=['disabled', 'mock', 'external'], default='mock', help='semantic enrichment mode; external is reserved hook')
    ap.add_argument('--strategy', choices=['precision_first', 'balanced', 'exploration_first'], default='balanced', help='preferred semantic strategy label')
    ap.add_argument('--payload-only', action='store_true', help='print payload only')
    ap.add_argument('--output', help='write JSON result to file')
    ap.add_argument('--run-search', action='store_true', help='call claw_search.py immediately after building payload')
    ap.add_argument('--token', help='optional token used only with --run-search')
    ap.add_argument('--retry-fallbacks', action='store_true', help='retry with smaller payload variants when search fails')
    ap.add_argument('--debug-search', action='store_true', help='include attempted payload variants and recommendation preview')
    ap.add_argument('--allow-query-inference', action='store_true', help='allow weak script-side query/category inference only as explicit fallback')
    args = ap.parse_args()

    if not args.query and not args.input:
        ap.error('one of --query or --input is required')

    data, by_code, children, category_index = load_categories()
    region_keywords = load_region_keywords()
    lang_keywords = load_lang_keywords()
    _ensure_router_executor_defaults()

    if args.input:
        import product_resolve
        resolved = product_resolve.resolve_product(args.input, timeout=args.resolve_timeout)
        analysis = resolved.get('analysis')
        product_summary = resolved.get('productSummary')
        bridge_error = None
        bridge_resolved = False
        if not isinstance(analysis, dict) or not analysis:
            analysis, product_summary, bridge_error = _try_resolve_url_fallback_via_host_executor(args.input, resolved)
            bridge_resolved = isinstance(analysis, dict) and bool(analysis)
        base_query = args.query or args.input
        resolved_fallback = (resolved or {}).get('fallback') or {}
        if not isinstance(analysis, dict) or not analysis:
            result = {
                'query': base_query,
                'matchedCategories': [],
                'payload': None,
                'analysis': {
                    'productSummary': product_summary or {},
                    'searchConditions': {},
                },
                'resolved': {
                    'mode': resolved.get('mode'),
                    'resolvedFrom': resolved.get('resolvedFrom'),
                    'fetch': resolved.get('fetch'),
                    'resolvedProduct': resolved.get('resolvedProduct'),
                    'fallback': resolved.get('fallback'),
                    'hostUrlAnalysisRequest': resolved.get('hostUrlAnalysisRequest'),
                },
                'needsUserInput': True,
                'error': bridge_error or {
                    'code': 'PRODUCT_ANALYSIS_UNAVAILABLE',
                    'message': 'Resolved product input did not produce usable analysis.',
                    'details': {'fallback': resolved_fallback},
                },
            }
        else:
            analysis = dict(analysis)
            if resolved_fallback.get('active') and not bridge_resolved:
                analysis['fallback'] = resolved_fallback
            if isinstance(product_summary, dict) and product_summary and not analysis.get('productSummary'):
                analysis['productSummary'] = product_summary
            result = build_payload_from_analysis(base_query, analysis, args, region_keywords, lang_keywords, data, by_code, children, category_index)
            result['resolved'] = {
                'mode': resolved.get('mode'),
                'resolvedFrom': resolved.get('resolvedFrom'),
                'fetch': resolved.get('fetch'),
                'resolvedProduct': resolved.get('resolvedProduct'),
                'fallback': resolved.get('fallback'),
                'hostUrlAnalysisRequest': resolved.get('hostUrlAnalysisRequest'),
            }
    else:
        query = html.unescape(args.query)
        q = query.lower()
        blog_cate_ids = []
        matches = []
        inferred_regions = infer_regions(q, region_keywords) if args.allow_query_inference else []
        inferred_langs = infer_languages(q, lang_keywords) if args.allow_query_inference else []
        explicit_regions = _normalize_explicit_codes(getattr(args, 'region', None), region_keywords)
        explicit_langs = _normalize_explicit_codes(getattr(args, 'lang', None), lang_keywords)
        sort_pair = infer_sort(q) if args.allow_query_inference else None
        keyword_terms = [seg.strip() for seg in re.split(r'[，,;；/\|]+', query) if seg.strip()][:8]
        seeded_keyword_terms = unique_keep_order(keyword_terms)
        advanced_keywords = focus_advanced_keywords(seeded_keyword_terms, limit=8)

        chosen_platform = args.platform if args.platform != 'auto' else 'tiktok'
        payload = {
            'platform': normalize_platform(chosen_platform),
            'pageNum': args.page_num,
            'pageSize': _resolve_page_size(getattr(args, 'page_size', None)),
            'hasEmail': True,
            'searchFilterList': ['THIS_UNTOUCH'] if getattr(args, 'exclude_contacted', True) else [],
        }
        regions = explicit_regions or inferred_regions
        if regions:
            payload['regionList'] = build_region_list(regions)
        langs = explicit_langs or inferred_langs
        if langs:
            payload['blogLangs'] = langs
        if args.min_fans is not None:
            payload['minFansNum'] = args.min_fans
        if args.max_fans is not None:
            payload['maxFansNum'] = args.max_fans
        if args.min_interactive_rate is not None:
            payload['minInteractiveRate'] = args.min_interactive_rate
        if sort_pair:
            payload['searchSort'], payload['sortOrder'] = sort_pair
        if advanced_keywords:
            payload['searchType'] = 'KEYWORD'
            payload['advancedKeywordList'] = advanced_keywords

        semantic = None
        if args.semantic_mode != 'disabled':
            semantic = {"semanticBrief": {}, "strategies": []}
            semantic_constraints = (semantic or {}).get('semanticBrief', {}).get('constraints', {})
            semantic_regions = _normalize_explicit_codes((semantic_constraints.get('regions') or {}).get('value') or [], region_keywords)
            semantic_langs = _normalize_explicit_codes((semantic_constraints.get('languages') or {}).get('value') or [], lang_keywords)
            semantic_keywords = extract_semantic_keywords(semantic)
            semantic_category_ids, semantic_matches = map_semantic_labels_to_category_ids(semantic, data, by_code, category_index) if args.allow_query_inference else ([], [])
            if semantic_regions and 'regionList' not in payload:
                payload['regionList'] = build_region_list(semantic_regions)
            if semantic_langs and 'blogLangs' not in payload:
                payload['blogLangs'] = semantic_langs
            merged_keyword_terms = unique_keep_order([*semantic_keywords, *seeded_keyword_terms])
            if merged_keyword_terms:
                payload['searchType'] = 'KEYWORD'
                payload['advancedKeywordList'] = focus_advanced_keywords(merged_keyword_terms, limit=8)
            if semantic_category_ids:
                payload['blogCateIds'] = semantic_category_ids
                matches = semantic_matches
            if (semantic_constraints.get('has_email') or {}).get('value') is True:
                payload['hasEmail'] = True
            if payload.get('minFansNum') is None and (semantic_constraints.get('min_fans') or {}).get('value') is not None:
                payload['minFansNum'] = (semantic_constraints.get('min_fans') or {}).get('value')
            if payload.get('maxFansNum') is None and (semantic_constraints.get('max_fans') or {}).get('value') is not None:
                payload['maxFansNum'] = (semantic_constraints.get('max_fans') or {}).get('value')

        payload_provenance = {
            'platform': 'explicit_args' if args.platform != 'auto' else 'default',
            'regions': 'explicit_args' if explicit_regions else ('query_inference' if inferred_regions else 'default'),
            'languages': 'explicit_args' if explicit_langs else ('query_inference' if inferred_langs else 'default'),
            'keywords': 'query_terms' if advanced_keywords else ('semantic_keyword_clusters' if semantic and semantic.get('semanticBrief') else 'fallback'),
            'blogCateIds': 'semantic_category_resolution' if payload.get('blogCateIds') else 'disabled',
            'minFansNum': 'explicit_args' if args.min_fans is not None else ('semantic_constraints' if semantic and (semantic.get('semanticBrief', {}).get('constraints', {}).get('min_fans') or {}).get('value') is not None else 'default'),
            'maxFansNum': 'explicit_args' if args.max_fans is not None else ('semantic_constraints' if semantic and (semantic.get('semanticBrief', {}).get('constraints', {}).get('max_fans') or {}).get('value') is not None else 'default'),
            'hasEmail': 'default',
            'searchType': 'keyword_strategy' if payload.get('advancedKeywordList') else ('category_only' if payload.get('blogCateIds') else 'default'),
            'fallbackApplied': False,
            'fallbackReason': None,
            'strategy': 'keyword_only',
        }

        result = {
            'query': query,
            'matchedCategories': [
                {
                    'dictValue': m.get('displayName') or m.get('dictValue'),
                    'dictCode': m.get('blogCateId') or m.get('dictCode'),
                    'level': m.get('level') or m.get('col2'),
                    'parent': m.get('parent') or m.get('col3'),
                    'source': m.get('source'),
                    'label': m.get('label'),
                    'score': m.get('score'),
                }
                for m in matches[:10]
            ],
            'payload': payload,
            'payloadProvenance': payload_provenance,
        }
        if semantic:
            result['semantic'] = semantic
            preferred = next((s for s in semantic.get('strategies', []) if s.get('name') == args.strategy), None)
            if preferred:
                strategy_payload = preferred.get('payloadDraft') or {}
                result['payloadFromStrategy'] = strategy_payload
                merged_payload = dict(payload)
                for key, value in strategy_payload.items():
                    if key not in merged_payload or merged_payload.get(key) in (None, [], {}):
                        merged_payload[key] = value
                    elif key in {'advancedKeywordList', 'blogCateIds'} and value:
                        merged_payload[key] = value
                    elif key in {'minFansNum', 'maxFansNum'} and getattr(args, 'min_fans' if key == 'minFansNum' else 'max_fans', None) is None:
                        merged_payload[key] = value
                if strategy_payload.get('searchType') and merged_payload.get('advancedKeywordList'):
                    merged_payload['searchType'] = strategy_payload['searchType']
                result['payload'] = merged_payload

    if result.get('needsUserInput'):
        output_obj = result['payload'] if args.payload_only and not args.run_search else result
        if args.output:
            Path(args.output).write_text(json.dumps(output_obj, ensure_ascii=False, indent=2))
        print(json.dumps(output_obj, ensure_ascii=False, indent=2))
        return

    if args.run_search:
        search_output = run_search(
            result['payload'],
            token=args.token,
            retry_fallbacks=args.retry_fallbacks,
            debug=args.debug_search,
        )
        result['search'] = search_output

    output_obj = result['payload'] if args.payload_only and not args.run_search else result
    if args.output:
        Path(args.output).write_text(json.dumps(output_obj, ensure_ascii=False, indent=2))
    print(json.dumps(output_obj, ensure_ascii=False, indent=2))




# ─── Compatibility shim for semantic/model layers ─────────────────────────────
# Higher-level semantic layers may import compile_payload to build a WotoHub
# payload from search hints. If the full compile_payload is not available, this shim
# returns the hints unchanged so the pipeline can still produce a basic payload.
def compile_payload(hints: dict, _extra: dict) -> dict:
    """Compile already-understood semantic hints into WotoHub search payload.

    Rules:
    - consume only fixed WotoHub-supported fields
    - blogCateIds is primary; advancedKeywordList is secondary refinement
    - do not invent semantics from raw user text here
    """
    payload = {
        "platform": hints.get("platform", "tiktok"),
        "blogLangs": hints.get("blogLangs", ["en"]),
        "hasEmail": hints.get("hasEmail", True),
        "regionList": hints.get("regionList", []),
    }
    if hints.get("minFansNum") is not None:
        payload["minFansNum"] = hints.get("minFansNum")
    if hints.get("maxFansNum") is not None:
        payload["maxFansNum"] = hints.get("maxFansNum")

    blog_cate_ids = unique_keep_order(hints.get("blogCateIds") or [])
    advanced_keywords = focus_advanced_keywords(hints.get("advancedKeywordList") or [], limit=5 if blog_cate_ids else 8)
    category_expected = bool(hints.get("categoryExpected") or (_extra or {}).get("categoryExpected"))

    if category_expected and not blog_cate_ids:
        raise ValueError("CATEGORY_MAPPING_REQUIRED: blogCateIds must be produced before advancedKeywordList can act as refinement on the main search chain.")

    if blog_cate_ids:
        payload["blogCateIds"] = blog_cate_ids
    if advanced_keywords:
        payload["searchType"] = hints.get("searchType", "KEYWORD")
        payload["advancedKeywordList"] = advanced_keywords

    return claw_search.normalize_search_payload(payload)


def build_payload_from_context(ctx: dict) -> dict:
    """Compile canonical semantic context into search payload.

    Release hard rule:
    - host/model layer may provide semantic analysis
    - search payload must still be compiled through the standard mapping chain
    - do not trust near-final searchPayloadHints for terminal fields like regionList/blogCateIds
    - fail fast when upper layer tries to bypass the compiler with malformed half-finished hints
    """
    marketing = ctx.get("marketingContext") or {}
    resolved = ctx.get("resolvedArtifacts") or {}
    product = ctx.get("productSignals") or {}
    follower_range = marketing.get("followerRange") or {}
    model_analysis = resolved.get("modelAnalysis") or {}
    search_payload_hints = dict((resolved.get("searchPayloadHints") or model_analysis.get("searchPayloadHints") or {}))

    constraints = model_analysis.get("constraints") or {}
    semantic_regions = marketing.get("targetMarkets") or constraints.get("regions") or []
    if isinstance(semantic_regions, str):
        semantic_regions = [semantic_regions]

    search_conditions = dict((model_analysis.get("searchConditions") or {}))
    explicit_blog_cate_ids = unique_keep_order(search_conditions.get("blogCateIds") or [])
    explicit_region_list = build_region_list(semantic_regions) if semantic_regions else []

    if search_payload_hints.get("regionList") and not explicit_region_list:
        raise ValueError(
            "Release rule violation: searchPayloadHints.regionList is not allowed without semantic targetMarkets/constraints.regions feeding standard region normalization."
        )

    raw_hint_blog_cate_ids = unique_keep_order(search_payload_hints.get("blogCateIds") or [])
    if raw_hint_blog_cate_ids and not explicit_blog_cate_ids:
        raise ValueError(
            "Release rule violation: searchPayloadHints.blogCateIds must come from standard category mapping, not direct injected near-final hints."
        )

    hints: dict[str, Any] = {}
    if search_payload_hints.get("platform"):
        hints["platform"] = search_payload_hints.get("platform")
    else:
        hints["platform"] = (marketing.get("platforms") or ["tiktok"])[0]

    if search_payload_hints.get("blogLangs"):
        hints["blogLangs"] = search_payload_hints.get("blogLangs")
    elif marketing.get("languages"):
        hints["blogLangs"] = marketing.get("languages")

    if search_payload_hints.get("minFansNum") is not None:
        hints["minFansNum"] = search_payload_hints.get("minFansNum")
    elif constraints.get("minFansNum") is not None:
        hints["minFansNum"] = constraints.get("minFansNum")
    elif follower_range.get("min") is not None:
        hints["minFansNum"] = follower_range.get("min")

    if search_payload_hints.get("maxFansNum") is not None:
        hints["maxFansNum"] = search_payload_hints.get("maxFansNum")
    elif constraints.get("maxFansNum") is not None:
        hints["maxFansNum"] = constraints.get("maxFansNum")
    elif follower_range.get("max") is not None:
        hints["maxFansNum"] = follower_range.get("max")

    if search_payload_hints.get("hasEmail") is not None:
        hints["hasEmail"] = search_payload_hints.get("hasEmail")

    if explicit_region_list:
        hints["regionList"] = explicit_region_list

    semantic = resolved.get("semantic") or build_semantic_input_from_model_analysis(model_analysis)
    data, by_code, children, category_index = load_categories()
    semantic_category_ids, semantic_matches = map_semantic_labels_to_category_ids(semantic, data, by_code, category_index)
    query_category_seed = " ".join(unique_keep_order([
        product.get("category"),
        product.get("productName"),
        (resolved.get("productSummary") or {}).get("productTypeHint"),
        *((resolved.get("productSummary") or {}).get("detectedForms") or []),
        (model_analysis.get("product") or {}).get("productSubtype"),
        (model_analysis.get("product") or {}).get("productType"),
        *((model_analysis.get("product") or {}).get("categoryForms") or []),
        product.get("rawInput"),
    ]))
    inferred_category_ids, inferred_matches = build_category_ids(query_category_seed, data, by_code, category_index) if query_category_seed else ([], [])
    category_resolution = resolve_category_strategy(
        model_analysis,
        semantic,
        product.get("rawInput") or product.get("productName") or "",
        data,
        by_code,
        children,
        category_index,
    )
    mapping = dict(category_resolution.get("mapping") or {})
    mapped_blog_cate_ids = unique_keep_order(mapping.get("selectedBlogCateIds") or [])
    if not mapped_blog_cate_ids:
        fallback_category_ids = unique_keep_order(semantic_category_ids or inferred_category_ids)
        fallback_matches = semantic_matches or inferred_matches
        if fallback_category_ids:
            mapped_blog_cate_ids = fallback_category_ids
            mapping["selectedBlogCateIds"] = mapped_blog_cate_ids
            if fallback_matches and not mapping.get("matchedCategories"):
                mapping["matchedCategories"] = fallback_matches
            if category_resolution.get("status") == "blocked":
                category_resolution["status"] = "partially_resolved" if len(mapped_blog_cate_ids) == 1 else "resolved"
                category_resolution["strategy"] = "broad_category_plus_keyword" if len(mapped_blog_cate_ids) == 1 else "category_plus_keyword"
                category_resolution["confidenceLevel"] = "medium" if len(mapped_blog_cate_ids) == 1 else "high"
                category_resolution["reasonSummary"] = "category inference fallback produced stable blogCateIds"
            decision = dict(category_resolution.get("decision") or {})
            decision["applyBlogCateIds"] = True
            if decision.get("categoryRole") in (None, "required_but_missing", "disabled"):
                decision["categoryRole"] = "broad_filter" if len(mapped_blog_cate_ids) == 1 else "primary_filter"
            if decision.get("keywordRole") == "blocked_pending_category_mapping":
                decision["keywordRole"] = "refinement"
            if decision.get("fallbackMode") == "blocked_pending_category_mapping":
                decision["fallbackMode"] = "broad_category_plus_keyword" if len(mapped_blog_cate_ids) == 1 else "category_plus_keyword"
            category_resolution["decision"] = decision
    elif semantic_matches and not mapping.get("matchedCategories"):
        mapping["matchedCategories"] = semantic_matches
    category_resolution["mapping"] = mapping
    if explicit_blog_cate_ids:
        hints["blogCateIds"] = explicit_blog_cate_ids
    elif mapped_blog_cate_ids:
        hints["blogCateIds"] = mapped_blog_cate_ids

    hints["categoryExpected"] = bool(category_resolution.get("categoryMappingExpected"))
    if hints["categoryExpected"] and not hints.get("blogCateIds"):
        raise ValueError(
            "CATEGORY_MAPPING_REQUIRED: semantic product/category inputs indicate this search should compile blogCateIds first. Refine productType/productSubtype/categoryForms before continuing."
        )

    if search_payload_hints.get("advancedKeywordList"):
        hints["advancedKeywordList"] = search_payload_hints.get("advancedKeywordList")
        if search_payload_hints.get("searchType"):
            hints["searchType"] = search_payload_hints.get("searchType")
    else:
        keyword_candidates = []
        for item in [
            *((model_analysis.get("marketing") or {}).get("contentAngles") or []),
            *((model_analysis.get("product") or {}).get("categoryForms") or []),
            (model_analysis.get("product") or {}).get("productSubtype"),
            (model_analysis.get("product") or {}).get("productType"),
            product.get("category"),
            *(marketing.get("creatorTypes") or []),
        ]:
            if item not in (None, "", [], {}):
                keyword_candidates.append(str(item))
        focused_keywords = focus_advanced_keywords(keyword_candidates, limit=5 if hints.get("blogCateIds") else 8)
        if focused_keywords:
            hints["advancedKeywordList"] = focused_keywords
            hints["searchType"] = "KEYWORD"

    payload = compile_payload(hints, {"categoryExpected": hints.get("categoryExpected")})
    resolved["categoryResolution"] = category_resolution
    return payload


if __name__ == '__main__':
    main()
