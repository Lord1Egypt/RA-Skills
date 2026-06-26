#!/usr/bin/env python3
from typing import Optional
"""
Ultra-light fallback product analysis layer.

Design intent:
- NOT the primary product understanding engine
- Primary analysis should come from the model layer
- This file only provides conservative, generic, low-risk local extraction
  for fallback / 补位场景

What it should do:
- normalize text
- detect URL/source host
- extract price / price tier
- extract a rough product name hint
- extract a small set of generic keyword hints
- provide safe default platform / region / language hints

What it should NOT do:
- act as a heavy product classifier
- aggressively infer product category ids
- aggressively infer creator types / audiences
- replace model-based semantic understanding
"""

import argparse
import json
import re
from urllib.parse import urlparse

from query_constraints import build_region_list


KEYWORD_STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
    'this', 'that', 'these', 'those', 'it', 'its', 'has', 'have', 'had',
    'not', 'no', 'nor', 'so', 'yet', 'both', 'each', 'few', 'all', 'any',
    'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten',
    'ml', 'oz', 'g', 'kg', 'lb', 'pcs', 'pack', 'set', 'box', 'bottle', 'piece',
    'size', 'color', 'colour', 'type', 'style', 'new', 'best', 'top', 'free',
    'buy', 'shop', 'price', 'sale', 'deal', 'save', 'shipping',
    'discover', 'exclusive', 'eligible', 'now', 'online',
    'item', 'brand', 'page', 'link', 'source', 'official', 'store', 'product',
    'amazon', 'tiktok', 'youtube', 'instagram', 'shop', 'http', 'https', 'www', 'com', 'pdp',
}


GENERIC_FUNCTION_HINTS = {
    'portable': ['travel', 'compact', '便携'],
    'wireless': ['wireless', 'bluetooth', 'cordless', '无线'],
    'waterproof': ['waterproof', 'water resistant', '防水'],
    'rechargeable': ['rechargeable', 'usb-c', 'usb c', '可充电'],
    '4k': ['4k', 'uhd'],
}


GENERIC_TARGET_AREAS = {
    'oral': ['oral', 'tooth', 'teeth', 'dental', 'mouth', '口腔'],
    'face': ['facial', 'skin', 'facial skin', '面部'],
    'hair': ['hair', 'scalp', '头发'],
    'pet': ['pet ', 'cat ', 'dog ', '宠物'],
    'baby': ['baby ', 'child', '儿童', '母婴'],
    'home': ['home ', 'household', '家居'],
    'outdoor': ['outdoor', 'camping', 'hiking', '户外'],
}


SEMANTIC_PHRASE_MAP = {
    '净水器': ['water filter', 'water filtration'],
    '滤水器': ['water filter'],
    'reverse osmosis': ['reverse osmosis', 'ro water system'],
    'under sink': ['under sink water filter'],
    'portable': ['portable'],
    '露营': ['camping'],
    '旅行': ['travel'],
    '测评': ['review'],
    '户外': ['outdoor'],
    '电动牙刷': ['electric toothbrush', 'oral care'],
}


def extract_semantic_selling_points(text: str) -> tuple[list[str], list[str], list[str]]:
    lowered = text.lower()
    selling_points: list[str] = []
    creator_angles: list[str] = []
    keyword_hints: list[str] = []

    for phrase, mapped in SEMANTIC_PHRASE_MAP.items():
        if phrase in text or phrase in lowered:
            keyword_hints.extend(mapped)

    chunks = [seg.strip() for seg in re.split(r'[，,;；。.!！?？/\|]+', text) if seg.strip()]
    for chunk in chunks:
        chunk_low = chunk.lower()
        if any(tok in chunk for tok in ['主打', '适合', '用于']) or any(tok in chunk_low for tok in ['portable', 'travel', 'camping', 'review', 'outdoor', 'under sink', 'reverse osmosis']):
            selling_points.append(chunk[:80])
        if any(tok in chunk for tok in ['达人', '博主']) or any(tok in chunk_low for tok in ['review', 'outdoor', 'lifestyle', 'youtube']):
            creator_angles.append(chunk[:60])

    keyword_hints.extend(re.findall(r'\b[a-z][a-z0-9\-]{3,30}\b', lowered))
    keyword_hints = [x for x in keyword_hints if x not in KEYWORD_STOPWORDS]

    def _unique(items: list[str], limit: int) -> list[str]:
        out = []
        seen = set()
        for item in items:
            value = str(item or '').strip()
            if not value:
                continue
            key = value.lower()
            if key in seen:
                continue
            seen.add(key)
            out.append(value)
            if len(out) >= limit:
                break
        return out

    return _unique(selling_points, 4), _unique(creator_angles, 4), _unique(keyword_hints, 8)


def normalize_text(text: str) -> str:
    return re.sub(r'\s+', ' ', (text or '').strip())


def is_url(value: str) -> bool:
    v = (value or '').strip()
    return v.startswith('http://') or v.startswith('https://')


def extract_source_host(text: str) -> Optional[str]:
    if is_url(text):
        try:
            return urlparse(text).netloc
        except Exception:
            return None
    return None


def infer_platform_from_host_or_text(text: str, source_host: Optional[str]= None) -> list[str]:
    host = (source_host or '').lower()
    lowered = text.lower()
    found = []
    if 'tiktok' in host or 'tiktok' in lowered:
        found.append('tiktok')
    if 'instagram' in host or 'instagram' in lowered or 'reels' in lowered:
        found.append('instagram')
    if 'youtube' in host or 'youtube' in lowered:
        found.append('youtube')
    return found or ['tiktok', 'instagram', 'youtube']


def infer_regions(text: str) -> list[str]:
    lowered = text.lower()
    mapping = {
        'us': ['united states', 'america', '美国'],
        'gb': ['united kingdom', '英国'],
        'au': ['australia', '澳大利亚'],
        'de': ['germany', '德国'],
        'fr': ['france', '法国'],
        'ca': ['canada', '加拿大'],
        'jp': ['japan', '日本'],
        'kr': ['korea', '韩国'],
    }
    found = []
    for code, aliases in mapping.items():
        for alias in aliases:
            if alias in lowered and code not in found:
                found.append(code)
    if re.search(r'\busa\b|\bus\b', lowered) and 'us' not in found:
        found.append('us')
    if re.search(r'\buk\b', lowered) and 'gb' not in found:
        found.append('gb')
    if re.search(r'\bca\b', lowered) and 'ca' not in found:
        found.append('ca')
    if re.search(r'\bau\b', lowered) and 'au' not in found:
        found.append('au')
    return found or ['us']


def infer_languages(regions: list[str]) -> list[str]:
    lang_map = {
        'us': 'en', 'gb': 'en', 'au': 'en', 'ca': 'en',
        'de': 'de', 'fr': 'fr', 'jp': 'ja', 'kr': 'ko',
    }
    out = []
    for region in regions:
        lang = lang_map.get(region)
        if lang and lang not in out:
            out.append(lang)
    return out or ['en']


def extract_price(text: str):
    patterns = [
        r'\$\s*(\d+(?:\.\d{1,2})?)',
        r'USD\s*(\d+(?:\.\d{1,2})?)',
        r'价格[:：]?\s*\$?\s*(\d+(?:\.\d{1,2})?)',
        r'售价[:：]?\s*\$?\s*(\d+(?:\.\d{1,2})?)',
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                pass
    return None


def infer_price_tier(price: Optional[float]) -> str:
    if price is None:
        return 'unknown'
    if price <= 20:
        return 'low_price'
    if price <= 80:
        return 'mid_price'
    return 'high_price'


def extract_product_name(text: str) -> Optional[str]:
    clean = normalize_text(text)
    explicit_patterns = [
        r'产品名称[:：]\s*([^,，;；\n]{2,120})',
        r'product name[:：]?\s*([^,，;；\n]{2,120})',
        r'商品名称[:：]\s*([^,，;；\n]{2,120})',
        r'推广一款([^,，;；\n]{2,80})',
    ]
    for pattern in explicit_patterns:
        m = re.search(pattern, clean, re.IGNORECASE)
        if m:
            return m.group(1).strip()

    if len(clean) <= 120 and not is_url(clean):
        return clean[:80]
    return None


def detect_functions(text: str) -> list[str]:
    lowered = text.lower()
    found = []
    for func, aliases in GENERIC_FUNCTION_HINTS.items():
        for alias in aliases:
            # Use word-boundary check to avoid substring collisions:
            # e.g. "body" shouldn't match "body insert", "hair" shouldn't match "chair"
            pat = r'\b' + re.escape(alias) + r'\b'
            if re.search(pat, lowered):
                found.append(func)
                break
    return found[:6]


def detect_target_areas(text: str) -> list[str]:
    lowered = text.lower()
    found = []
    for area, aliases in GENERIC_TARGET_AREAS.items():
        for alias in aliases:
            pat = r'\b' + re.escape(alias) + r'\b'
            if re.search(pat, lowered):
                found.append(area)
                break
    return found[:5]


def build_keywords(text: str) -> list[str]:
    lowered = text.lower()

    preserved_phrases = [
        'face tracking', 'object tracking', '4k video', 'gimbal stabilization',
        'smart watch', 'electric toothbrush', 'water flosser', 'portable camera',
        'vlogging camera', 'flip screen', 'wireless earbuds', 'bluetooth speaker',
    ]

    out = []
    seen = set()

    for phrase in preserved_phrases:
        if phrase in lowered and phrase not in seen:
            seen.add(phrase)
            out.append(phrase)

    for token in re.findall(r'\b[a-z][a-z0-9\-]{2,30}\b', lowered):
        if token in KEYWORD_STOPWORDS:
            continue
        if token in seen:
            continue
        seen.add(token)
        out.append(token)
        if len(out) >= 10:
            break

    return out[:10]


def to_advanced_keywords(keywords: list[str]) -> list[dict]:
    out = []
    seen = set()
    for kw in keywords:
        low = kw.lower().strip()
        if not low or low in seen:
            continue
        seen.add(low)
        out.append({'value': kw, 'exclude': False})
    return out[:8]


def build_notes(platforms: list[str], regions: list[str], price_tier: str) -> list[str]:
    notes = []
    notes.append('这是本地保守补位结果，主分析应优先使用模型输出。')
    if price_tier == 'low_price':
        notes.append('价格偏低，通常更适合铺量型合作。')
    elif price_tier == 'high_price':
        notes.append('价格偏高，通常更适合高信任度垂类达人。')
    if 'tiktok' in platforms:
        notes.append('TikTok 适合短视频种草、开箱、场景化演示。')
    if 'youtube' in platforms:
        notes.append('YouTube 适合深度测评、教程、长视频搜索流量。')
    if 'instagram' in platforms:
        notes.append('Instagram 适合视觉种草、生活方式内容和 Reels。')
    if regions:
        notes.append(f"当前保守识别市场: {', '.join(regions)}")
    return notes[:5]


def analyze_input(raw_input: str) -> dict:
    """Conservative fallback analysis only."""
    text = normalize_text(raw_input)
    is_url_flag = is_url(text)
    source_host = extract_source_host(text) if is_url_flag else None

    product_name = extract_product_name(text)
    price = extract_price(text)
    price_tier = infer_price_tier(price)
    platforms = infer_platform_from_host_or_text(text, source_host)
    regions = infer_regions(text)
    languages = infer_languages(regions)
    functions = detect_functions(text)
    target_areas = detect_target_areas(text)
    keywords = build_keywords(text)
    selling_points, creator_angles, semantic_keywords = extract_semantic_selling_points(text)
    merged_keywords = []
    for source in (semantic_keywords, keywords):
        for item in source:
            if item not in merged_keywords:
                merged_keywords.append(item)
    advanced_keywords = to_advanced_keywords(merged_keywords)
    notes = build_notes(platforms, regions, price_tier)

    product_summary = {
        'productName': product_name,
        'productTypeHint': None,
        'detectedForms': [],
        'detectedFunctions': functions[:3],
        'detectedTargetAreas': target_areas[:3],
        'priceHint': price,
        'priceTier': price_tier,
        'platformHints': platforms[:3],
        'regionHints': regions[:2],
        'languageHints': languages[:2],
        'sellingPoints': selling_points,
        'targetAudiences': [],
        'creatorAngles': creator_angles,
        'keywordHints': merged_keywords[:6],
    }

    search_conditions = {
        'platforms': platforms,
        'regions': regions,
        'languages': languages,
        'blogCateIds': [],
        'keywords': merged_keywords[:6],
        'advancedKeywordList': advanced_keywords[:6],
        'minFansNum': None,
        'maxFansNum': None,
        'hasEmail': True,
        'notes': notes + ['fallback only: avoid treating this output as the primary semantic understanding layer.'],
        'payloadHints': {
            'platform': platforms[0] if platforms else 'tiktok',
            'blogCateIds': [],
            'regionList': build_region_list(regions),
            'blogLangs': languages,
            'hasEmail': True,
            'searchType': 'KEYWORD',
            'advancedKeywordList': advanced_keywords[:6],
        },
    }

    return {
        'input': raw_input,
        'normalizedInput': text,
        'isUrl': is_url_flag,
        'sourceHost': source_host,
        'analysisMode': 'fallback_light',
        'productSummary': product_summary,
        'searchConditions': search_conditions,
    }


def main():
    ap = argparse.ArgumentParser(description='Ultra-light fallback product analysis helper')
    ap.add_argument('--input', required=True, help='product url or product description')
    args = ap.parse_args()
    result = analyze_input(args.input)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
