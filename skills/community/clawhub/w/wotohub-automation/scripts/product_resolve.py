#!/usr/bin/env python3
from typing import Optional
import argparse
import json
import random
import re
from pathlib import Path
from urllib.parse import urlparse

import html
import sys

import platform_resolver
import product_analyze
from semantic_layer import SemanticLayer
from url_fetcher import fetch_url_text, strip_html

_URL_MODEL_ANALYSIS_PROMPT = (Path(__file__).resolve().parents[1] / 'prompts' / 'url-model-analysis.md').read_text()

# ── Pre-compiled regex for clean_url_page_text (avoids re-compiling on every call) ──
_RE_HTML_ENTITY   = re.compile(r'&#x?[0-9a-fA-F]+;')
_RE_HTML_NAMED    = re.compile(r'\b(?:x27|amp|nbsp|quot)\b', re.IGNORECASE)
_RE_LONG_ALNUM    = re.compile(r'\b[A-Z0-9]{10,}\b')
_RE_LONG_DIGIT    = re.compile(r'\b\d{10,}\b')
_RE_WHITESPACE    = re.compile(r'\s+')
_RE_ANTI_BOT      = re.compile(r'(access denied|forbidden|captcha|verify you are human|robot check|security check|request blocked)', re.IGNORECASE)
_RE_PRODUCTY_HINT = re.compile(r'(add to cart|buy now|product details|specifications|features|price|sale)', re.IGNORECASE)


def _model_to_product_summary(model_output: dict) -> dict:
    """
    Extract a productSummary dict from a model_analysis schema.

    This provides the backward-compatible productSummary block that
    run_campaign.py and email generation code expects, while keeping
    the full model schema available in the 'analysis' field.
    """
    product = model_output.get("product", {}) or {}
    marketing = model_output.get("marketing", {}) or {}

    return {
        "productName": product.get("productName") or product.get("productType"),
        "productTypeHint": product.get("productType"),
        "detectedForms": product.get("categoryForms") or [],
        "sellingPoints": product.get("coreBenefits") or [],
        "detectedFunctions": product.get("functions") or [],
        "detectedTargetAreas": product.get("targetAreas") or [],
        "targetAudiences": product.get("targetAudiences") or [],
        "priceHint": None,  # use None to avoid build_payload confusion with tier strings
        "priceTier": product.get("priceTier", "unknown"),
        "platformHints": marketing.get("platformPreference") or ["tiktok"],
        "contentAngles": marketing.get("contentAngles") or [],
        "creatorTypes": marketing.get("creatorTypes") or [],
        "brand": product.get("brand"),
    }


def _clean(text: Optional[str]) -> Optional[str]:
    """Decode HTML entities (&#x27;, &amp;, &#39;, etc.) and strip excess whitespace."""
    if not text:
        return text
    # html.unescape handles named entities (&amp;, &quot;, etc.)
    # and hexadecimal numeric entities (&#x27;) natively.
    # For decimal numeric entities like &#39; that some pages emit,
    # do a supplemental pass.
    text = html.unescape(text)
    text = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), text)
    return ' '.join(text.split())


def is_url(value: str) -> bool:
    v = value.strip()
    return v.startswith('http://') or v.startswith('https://')


def validate_input(value: str) -> tuple[bool, str]:
    """Validate input length and format."""
    MAX_URL_LENGTH = 2048
    MAX_TEXT_LENGTH = 5000

    if not value or not value.strip():
        return False, "输入不能为空"

    if is_url(value):
        if len(value) > MAX_URL_LENGTH:
            return False, f"URL 过长（最多 {MAX_URL_LENGTH} 字符，当前 {len(value)} 字符）"
    else:
        if len(value) > MAX_TEXT_LENGTH:
            return False, f"描述文本过长（最多 {MAX_TEXT_LENGTH} 字符，当前 {len(value)} 字符）"

    return True, ""





def infer_source_platform(host: str) -> Optional[str]:
    h = host.lower()
    if 'tiktok' in h:
        return 'TikTok Shop'
    if 'amazon' in h:
        return 'Amazon'
    if 'shopify' in h or 'myshopify' in h:
        return 'Shopify'
    if 'shopee' in h:
        return 'Shopee'
    if 'lazada' in h:
        return 'Lazada'
    if 'ebay' in h:
        return 'eBay'
    if 'temu' in h:
        return 'Temu'
    if 'aliexpress' in h:
        return 'AliExpress'
    if 'wish' in h:
        return 'Wish'
    if 'target' in h:
        return 'Target'
    if 'walmart' in h:
        return 'Walmart'
    return None


def first_non_empty(*values):
    for value in values:
        if isinstance(value, str):
            value = value.strip()
        if value not in (None, '', [], {}):
            return value
    return None


def make_analysis_text(url: str, title: Optional[str], description: Optional[str], body_text: str, brand: Optional[str]= None, price=None, features: Optional[list]= None) -> str:
    chunks = []
    chunks.append(url)
    if title:
        chunks.append(f'产品名称: {title}')
    if brand:
        chunks.append(f'品牌: {brand}')
    if price is not None:
        chunks.append(f'价格: ${price}')
    if features:
        chunks.append(f'产品特色: {", ".join(features)}')
    if description:
        chunks.append(f'产品描述: {description}')
    compact_body = body_text[:4000]
    if compact_body:
        chunks.append(f'页面正文: {compact_body}')
    return '\n'.join(chunks)


def clean_url_page_text(raw_text: str, url: Optional[str]= None) -> dict:
    text = raw_text or ''
    removed_tokens = []
    notes = []

    if url:
        text = text.replace(url, ' ')
    text = html.unescape(text)
    text = _RE_HTML_ENTITY.sub(' ', text)
    text = _RE_HTML_NAMED.sub(' ', text)
    text = _RE_LONG_ALNUM.sub(' ', text)
    text = _RE_LONG_DIGIT.sub(' ', text)

    tokens = re.split(r'\s+', text)
    kept = []
    noise_tokens = {
        'products', 'shop', 'source', 'detail', 'fit', 'x27', 'amp', 'nbsp',
        'quot', 'th', 'dp', 'product_detail', 'www', 'http', 'https',
    }
    for tok in tokens:
        t = tok.strip(" ,.;:!?()[]{}<>\"'")
        if not t:
            continue
        low = t.lower()
        if low in noise_tokens:
            removed_tokens.append(low)
            continue
        kept.append(t)

    cleaned = ' '.join(kept).strip()
    cleaned = _RE_WHITESPACE.sub(' ', cleaned)
    if len(cleaned) > 8000:
        cleaned = cleaned[:8000]
        notes.append('cleaned text truncated to 8000 chars')
    if removed_tokens:
        notes.append('removed noisy url/html tokens before analysis')
    return {
        'cleanedText': cleaned,
        'removedTokens': list(dict.fromkeys(removed_tokens))[:100],
        'notes': notes,
    }


def assess_page_quality(url: str, html: str, text: str, resolved_product: Optional[dict]= None) -> dict:
    resolved_product = resolved_product or {}
    anti_bot = bool(_RE_ANTI_BOT.search(html or '') or _RE_ANTI_BOT.search(text or ''))
    host = ''
    try:
        host = urlparse(url).netloc.lower()
    except Exception:
        host = ''
    product_signals = 0
    for key in ('productName', 'brand', 'description', 'price'):
        if resolved_product.get(key) not in (None, '', []):
            product_signals += 1
    if _RE_PRODUCTY_HINT.search(text or ''):
        product_signals += 1
    weak_title = str(resolved_product.get('title') or resolved_product.get('productName') or '').strip()
    weak_desc = str(resolved_product.get('description') or '').strip()
    weak_page = len(text or '') < 500 or (product_signals <= 2 and len(weak_desc) < 40)
    blocked_like_tiktok = ('tiktok.com' in host and weak_page)
    quality = 'high' if product_signals >= 4 and not anti_bot and not blocked_like_tiktok else ('medium' if product_signals >= 3 and not anti_bot and not blocked_like_tiktok else 'low')
    likely_non_product = (product_signals <= 1 and not anti_bot) or blocked_like_tiktok or (not weak_title and weak_page)
    return {
        'quality': quality,
        'antiBotDetected': anti_bot,
        'likelyNonProductPage': likely_non_product,
        'productSignalCount': product_signals,
        'recommendedAction': 'fallback_to_user_input' if anti_bot or likely_non_product else 'continue',
    }


def build_url_model_input(url: str, fetched_html: str, cleaned_text: str, resolved_product: Optional[dict]= None, debug: bool = False) -> dict:
    host = ''
    try:
        host = urlparse(url).netloc
    except Exception:
        pass
    resolved_product = resolved_product or {}
    prompt_path = str(Path(__file__).resolve().parents[1] / 'prompts' / 'url-model-analysis.md')
    page_block = {
        'htmlLength': len(fetched_html or ''),
        'cleanedTextLength': len(cleaned_text or ''),
        'cleanedTextPreview': (cleaned_text or '')[:1000],
    }
    if debug:
        page_block['cleanedText'] = cleaned_text
    return {
        'source': {'url': url, 'host': host},
        'page': page_block,
        'resolvedSignals': {
            'title': resolved_product.get('title') or resolved_product.get('productName'),
            'brand': resolved_product.get('brand'),
            'price': resolved_product.get('price'),
            'currency': resolved_product.get('currency'),
            'description': resolved_product.get('description'),
            'features': resolved_product.get('features') or [],
            'platform': resolved_product.get('platform') or resolved_product.get('sourcePlatform'),
        },
        'instruction': '请根据以上 URL 页面信息，输出 model_analysis schema。',
        'promptPath': prompt_path,
    }


def _fallback_user_prompt() -> str:
    return (
        "我暂时不能稳定读取这个商品链接，但不影响继续做达人推荐。\n"
        "你直接按下面这个格式补充任意 2-4 项就行：\n"
        "- 产品名称：\n"
        "- 核心卖点：\n"
        "- 价格区间：\n"
        "- 目标市场：\n"
        "- 适合的达人类型："
    )


def _build_host_url_analysis_request(
    *,
    url: str,
    fallback_reason: str,
    source_host: Optional[str]= None,
    source_platform: Optional[str]= None,
    resolved_product: Optional[dict]= None,
    page_quality: Optional[dict]= None,
    fetch: Optional[dict]= None,
    error: Optional[str]= None,
) -> dict:
    resolved_product = resolved_product or {}
    page_quality = page_quality or {}
    fetch = fetch or {}
    return {
        'task': 'generate_host_analysis_for_url_product',
        'mode': 'host_url_analysis_request',
        'input': {
            'url': url,
            'fallbackReason': fallback_reason,
            'fetchError': error,
            'partialSignals': {
                'sourceHost': source_host,
                'sourcePlatform': source_platform,
                'title': resolved_product.get('title') or resolved_product.get('productName'),
                'description': resolved_product.get('description'),
                'price': resolved_product.get('price'),
                'brand': resolved_product.get('brand'),
                'currency': resolved_product.get('currency'),
                'imageUrl': resolved_product.get('imageUrl'),
                'features': resolved_product.get('features') or [],
            },
            'pageQuality': page_quality,
            'fetch': {
                'sourceHost': source_host,
                'sourcePlatform': source_platform,
                'statusCode': fetch.get('statusCode'),
                'finalUrl': fetch.get('finalUrl') or url,
                'contentType': fetch.get('contentType'),
                'contentLength': fetch.get('contentLength'),
            },
        },
        'deliveryContract': {
            'canonicalFields': ['hostAnalysis', 'productSummary'],
            'doNotReturn': ['searchPayload', 'blogCateIds', 'regionList'],
        },
        'runtimeHints': {
            'browserPreferred': True,
            'doNotReturnSearchPayload': True,
            'goal': 'recover_product_understanding_from_url',
        },
    }


def _build_host_url_analysis_writeback_result(
    *,
    raw: str,
    host_analysis: dict,
    product_summary: Optional[dict]= None,
) -> dict:
    product_summary = product_summary or _model_to_product_summary(host_analysis)
    product = (host_analysis or {}).get('product') or {}
    marketing = (host_analysis or {}).get('marketing') or {}
    host = urlparse(raw).netloc if is_url(raw) else None
    source_platform = infer_source_platform(host or '') if host else None
    resolved_product = {
        'sourcePlatform': source_platform,
        'sourceHost': host,
        'title': _clean(product.get('productName') or product_summary.get('productName')),
        'productName': _clean(product.get('productName') or product_summary.get('productName')),
        'brand': _clean(product.get('brand') or product_summary.get('brand')),
        'description': _clean(product.get('pageTitle') or product_summary.get('pageDescription')),
        'price': product.get('price') or product_summary.get('priceHint'),
        'currency': None,
        'storeName': None,
        'merchantName': None,
        'imageUrl': None,
        'productUrl': product.get('sourceUrl') or raw,
        'features': product.get('features') or product_summary.get('sellingPoints') or [],
        'platform': (marketing.get('platformPreference') or [None])[0],
        'siteParser': 'host_url_analysis_writeback',
    }
    product_summary = dict(product_summary or {})
    product_summary.setdefault('sourcePlatform', source_platform)
    product_summary.setdefault('sourceHost', host)
    product_summary.setdefault('productUrl', raw)
    return {
        'input': raw,
        'mode': 'url',
        'resolvedFrom': 'url_host_analysis_writeback',
        'fetch': None,
        'resolvedProduct': resolved_product,
        'analysis': host_analysis,
        'productSummary': product_summary,
        'fallback': None,
        'hostUrlAnalysisRequest': None,
    }


def resolve_product(value: str, mode: str = 'auto', timeout: int = 20, debug: bool = False, host_analysis: Optional[dict]= None, product_summary: Optional[dict]= None) -> dict:
    raw = value.strip()

    # Validate input
    valid, error_msg = validate_input(raw)
    if not valid:
        return {
            'input': raw,
            'mode': mode,
            'resolvedFrom': None,
            'fetch': None,
            'resolvedProduct': None,
            'analysis': None,
            'productSummary': None,
            'fallback': {
                'active': True,
                'reason': 'INPUT_VALIDATION_FAILED',
                'userPrompt': error_msg,
            },
        }

    actual_mode = mode
    if mode == 'auto':
        actual_mode = 'url' if is_url(raw) else 'text'

    if actual_mode == 'url' and isinstance(host_analysis, dict) and host_analysis:
        return _build_host_url_analysis_writeback_result(
            raw=raw,
            host_analysis=host_analysis,
            product_summary=product_summary,
        )

    if actual_mode == 'text':
        model_output = SemanticLayer.analyze_model(raw)
        product_summary = _model_to_product_summary(model_output)
        return {
            'input': raw,
            'mode': 'text',
            'resolvedFrom': 'text',
            'fetch': None,
            'resolvedProduct': {
                'sourcePlatform': None,
                'sourceHost': None,
                'title': _clean(product_summary.get('productName')),
                'brand': ((model_output or {}).get('product') or {}).get('brand'),
                'description': None,
                'price': product_summary.get('priceHint'),
                'storeName': None,
            },
            'analysis': model_output,
            'productSummary': product_summary,
            'fallback': None,
        }

    if actual_mode != 'url':
        raise ValueError(f'Unsupported mode: {mode}')

    try:
        fetched = fetch_url_text(raw, timeout=timeout)
        html = fetched['html']
        text = strip_html(html)
        host = urlparse(raw).netloc
        parsed = platform_resolver.resolve_by_host(host, html, text, raw)
        source_platform = infer_source_platform(host) or parsed.get('platform')

        if not parsed.get('productName') or (parsed.get('platform') == 'generic' and len(text) > 200):
            generic_retry = platform_resolver.resolve_generic(html, text, raw)
            for key in ('productName', 'brand', 'description', 'price', 'features', 'imageUrl', 'currency'):
                if not parsed.get(key) and generic_retry.get(key) is not None:
                    parsed[key] = generic_retry.get(key)

        merged_title = first_non_empty(parsed.get('productName'))
        merged_description = first_non_empty(parsed.get('description'))
        merged_price = first_non_empty(parsed.get('price'))
        merged_brand = first_non_empty(parsed.get('brand'), parsed.get('merchantName'))
        store_name = first_non_empty(parsed.get('merchantName'))

        cleaned_info = clean_url_page_text(text, raw)
        analysis_text = cleaned_info.get('cleanedText') or text
        synthesized_input = make_analysis_text(raw, merged_title, merged_description, analysis_text, brand=merged_brand, price=merged_price, features=parsed.get('features'))
        model_output = SemanticLayer.analyze_model(
            synthesized_input,
            url=raw,
            page_title=merged_title,
            brand=merged_brand,
            price=merged_price,
            features=parsed.get('features'),
        )
        # Build a productSummary compat block from the model output + URL-extracted signals
        product_summary = _model_to_product_summary(model_output)
        product_summary['sourcePlatform'] = source_platform
        product_summary['sourceHost'] = host
        product_summary['pageTitle'] = merged_title
        product_summary['pageDescription'] = merged_description
        product_summary['storeName'] = store_name
        product_summary['brand'] = _clean(merged_brand) or product_summary.get('brand')
        product_summary['siteParser'] = parsed.get('platform') or 'generic'
        product_summary['currency'] = parsed.get('currency')
        product_summary['imageUrl'] = parsed.get('imageUrl')
        product_summary['productUrl'] = parsed.get('productUrl') or raw
        product_summary['features'] = parsed.get('features') or []
        product_summary['merchantName'] = parsed.get('merchantName')

        resolved_product = {
            'sourcePlatform': source_platform,
            'sourceHost': host,
            'title': _clean(merged_title),
            'productName': _clean(merged_title),
            'brand': _clean(merged_brand),
            'description': _clean(merged_description),
            'price': merged_price,
            'currency': parsed.get('currency'),
            'storeName': _clean(store_name),
            'merchantName': _clean(parsed.get('merchantName')),
            'imageUrl': parsed.get('imageUrl'),
            'productUrl': parsed.get('productUrl') or raw,
            'features': parsed.get('features') or [],
            'platform': parsed.get('platform'),
            'siteParser': parsed.get('platform') or 'generic',
        }
        page_quality = assess_page_quality(raw, html, text, resolved_product)
        host_lower = (host or '').lower()
        weak_signal_tiktok_shop = (
            'tiktok.com' in host_lower
            and '/shop/pdp/' in raw
            and page_quality.get('productSignalCount', 0) <= 3
            and not resolved_product.get('brand')
            and not resolved_product.get('price')
            and len(resolved_product.get('features') or []) < 2
        )
        if weak_signal_tiktok_shop:
            page_quality['likelyNonProductPage'] = True
            page_quality['recommendedAction'] = 'fallback_to_user_input'
            page_quality['quality'] = 'low'
        if page_quality.get('antiBotDetected') or page_quality.get('likelyNonProductPage'):
            prompt = _fallback_user_prompt()
            fetch_summary = {
                'statusCode': fetched.get('statusCode'),
                'finalUrl': fetched.get('finalUrl') or raw,
                'contentType': fetched.get('contentType'),
                'contentLength': fetched.get('contentLength'),
            }
            return {
                'input': raw,
                'mode': 'url',
                'resolvedFrom': 'url_low_confidence_fallback',
                'fetch': {
                    'url': raw,
                    'sourceHost': host,
                    'sourcePlatform': source_platform,
                    'bodyTextPreview': text[:800],
                    'bodyTextLength': len(text),
                    'statusCode': fetched.get('statusCode'),
                    'finalUrl': fetched.get('finalUrl') or raw,
                    'contentType': fetched.get('contentType'),
                    'contentLength': fetched.get('contentLength'),
                    'siteParser': parsed.get('platform') or 'generic',
                    'fetchAttempt': fetched.get('attempt'),
                    'headerProfile': fetched.get('headerProfile'),
                },
                'resolvedProduct': resolved_product,
                'analysis': None,
                'productSummary': None,
                'pageQuality': page_quality,
                'hostUrlAnalysisRequest': _build_host_url_analysis_request(
                    url=raw,
                    fallback_reason='url_page_low_confidence',
                    source_host=host,
                    source_platform=source_platform,
                    resolved_product=resolved_product,
                    page_quality=page_quality,
                    fetch=fetch_summary,
                ),
                'fallback': {
                    'active': True,
                    'reason': 'url_page_low_confidence',
                    'needsUserInput': True,
                    'userPrompt': prompt,
                    'requestedFields': ['productName', 'sellingPoints', 'priceRange', 'targetMarket', 'creatorTypes'],
                    'notes': ['URL page quality too low for reliable product extraction.']
                },
            }
        return {
            'input': raw,
            'mode': 'url',
            'resolvedFrom': 'url',
            'fetch': {
                'url': raw,
                'sourceHost': host,
                'sourcePlatform': source_platform,
                'title': merged_title,
                'description': merged_description,
                'bodyTextPreview': text[:1200],
                'bodyTextLength': len(text),
                'statusCode': fetched.get('statusCode'),
                'finalUrl': fetched.get('finalUrl') or raw,
                'contentType': fetched.get('contentType'),
                'contentLength': fetched.get('contentLength'),
                'siteParser': parsed.get('platform') or 'generic',
                'fetchAttempt': fetched.get('attempt'),
                'headerProfile': fetched.get('headerProfile'),
            },
            'resolvedProduct': resolved_product,
            'analysis': model_output,  # raw model schema — NOT adapted
            'productSummary': product_summary,
            'urlCleaning': {
                'cleanedTextPreview': cleaned_info.get('cleanedText', '')[:500],
                'removedTokens': cleaned_info.get('removedTokens', []),
                'notes': cleaned_info.get('notes', []),
            },
            'pageQuality': page_quality,
            'urlModelInput': build_url_model_input(raw, html, cleaned_info.get('cleanedText', ''), resolved_product, debug=debug),
            'fallback': None,
        }
    except Exception as e:
        host = urlparse(raw).netloc if is_url(raw) else None
        source_platform = infer_source_platform(host or '') if host else None
        prompt = _fallback_user_prompt()
        return {
            'input': raw,
            'mode': 'url',
            'resolvedFrom': 'url_fallback_text_only',
            'fetch': None,
            'resolvedProduct': {
                'sourcePlatform': source_platform,
                'sourceHost': host,
                'title': None,
                'brand': None,
                'description': None,
                'price': None,
                'storeName': None,
                'siteParser': None,
            },
            'analysis': None,
            'productSummary': None,
            'hostUrlAnalysisRequest': _build_host_url_analysis_request(
                url=raw,
                fallback_reason='url_fetch_unavailable',
                source_host=host,
                source_platform=source_platform,
                resolved_product={
                    'sourcePlatform': source_platform,
                    'sourceHost': host,
                    'title': None,
                    'brand': None,
                    'description': None,
                    'price': None,
                    'currency': None,
                    'imageUrl': None,
                    'features': [],
                },
                fetch={'finalUrl': raw},
                error=str(e),
            ),
            'fallback': {
                'active': True,
                'reason': 'url_fetch_unavailable',
                'error': str(e),
                'needsUserInput': True,
                'userPrompt': prompt,
                'requestedFields': [
                    'productName',
                    'sellingPoints',
                    'priceRange',
                    'targetMarket',
                    'creatorTypes'
                ],
                'suggestedReplyTemplate': {
                    '产品名称': '',
                    '核心卖点': '',
                    '价格区间': '',
                    '目标市场': '',
                    '适合的达人类型': ''
                },
                'notes': [
                    '当前 skill 不应把本地抓取能力作为硬依赖。',
                    '当 URL 抓取失败时，应该退回到用户补充商品信息的流程。'
                ]
            },
        }


def main():
    ap = argparse.ArgumentParser(description='Resolve product link or text into fetched details plus structured search hints')
    ap.add_argument('--input', required=True, help='product url or product description')
    ap.add_argument('--mode', choices=['auto', 'url', 'text'], default='auto')
    ap.add_argument('--timeout', type=int, default=12)
    args = ap.parse_args()
    result = resolve_product(args.input, mode=args.mode, timeout=args.timeout)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    fallback = (result or {}).get('fallback') or {}
    if fallback.get('active'):
        print('\n# FALLBACK_ACTIVE', file=sys.stderr)
        print(fallback.get('userPrompt', ''), file=sys.stderr)


if __name__ == '__main__':
    main()
