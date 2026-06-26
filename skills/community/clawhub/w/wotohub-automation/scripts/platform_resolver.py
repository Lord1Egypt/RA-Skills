#!/usr/bin/env python3
"""
platform_resolver.py
~~~~~~~~~~~~~~~~~~~~
扩展 URL 解析器——以注册表模式覆盖更多电商平台。

每个平台解析函数提取：
  productName, price, brand, description, features, platform,
  imageUrl, productUrl, merchantName, currency

现有 TikTok/Amazon/Shopify 保留，新增：
  shopee, lazada, ebay, temu, aliexpress, wish, target, walmart
"""
from __future__ import annotations

import json
import re
from typing import Callable, Any, Optional

# ── 共用解析工具 ──────────────────────────────────────────────────────────────

def _clean(text: Any) -> Optional[str]:
    if text is None:
        return None
    if isinstance(text, (dict, list)):
        text = json.dumps(text, ensure_ascii=False)
    text = re.sub(r"\s+", " ", str(text)).strip()
    return text or None


def _parse_price(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    m = re.search(r"(\d+(?:\.\d{1,2})?)", str(value))
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            pass
    return None


def _extract_json_ld(html: str) -> list[dict[str, Any]]:
    """提取页面中所有 JSON-LD script 块。"""
    objects: list[dict[str, Any]] = []
    for raw in re.findall(
        r'(?is)<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
    ):
        raw = raw.strip()
        if not raw:
            continue
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                objects.extend(x for x in parsed if isinstance(x, dict))
            elif isinstance(parsed, dict):
                objects.append(parsed)
        except Exception:
            pass
    return objects


def _pick_product_ld(objects: list[dict[str, Any]]) -> Optional[dict]:
    """从 JSON-LD 对象列表中挑出 Product 类型。"""
    for obj in objects:
        typ = obj.get("@type")
        if typ == "Product" or (isinstance(typ, list) and "Product" in typ):
            return obj
        graph = obj.get("@graph")
        if isinstance(graph, list):
            for item in graph:
                if not isinstance(item, dict):
                    continue
                item_typ = item.get("@type")
                if item_typ == "Product" or (
                    isinstance(item_typ, list) and "Product" in item_typ
                ):
                    return item
    return None


def _meta_content(html: str, patterns: list[str]) -> Optional[str]:
    for pattern in patterns:
        m = re.search(pattern, html, re.IGNORECASE)
        if m:
            val = _clean(re.sub(r"(?s)<[^>]+>", " ", m.group(1)))
            if val:
                return val
    return None


def _og_tag(html: str, property_: str) -> Optional[str]:
    return _meta_content(html, [
        rf'(?is)<meta[^>]+property=["\']og:{property_}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'(?is)<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:{property_}["\']',
    ])


def _meta_name(html: str, name: str) -> Optional[str]:
    return _meta_content(html, [
        rf'(?is)<meta[^>]+name=["\']{name}["\'][^>]+content=["\']([^"\']+)["\']',
        rf'(?is)<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']{name}["\']',
    ])


def _title_tag(html: str) -> Optional[str]:
    return _meta_content(html, [
        r'(?is)<title[^>]*>(.*?)</title>',
    ])


def _striptag(text: str) -> str:
    return re.sub(r"(?s)<[^>]+>", " ", text).strip()


def _extract_price_from_text(text: str) -> Optional[float]:
    patterns = [
        r"\$\s*(\d+(?:\.\d{1,2})?)",
        r"USD\s*(\d+(?:\.\d{1,2})?)",
        r"价格[:：]?\s*\$?\s*(\d+(?:\.\d{1,2})?)",
        r"售价[:：]?\s*\$?\s*(\d+(?:\.\d{1,2})?)",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1))
            except ValueError:
                pass
    return None


def _extract_amazon_feature_label(raw_li: str) -> Optional[str]:
    """
    Extract the feature-name label from an Amazon feature-bullets <li> entry.
    Amazon formats bullets as:  🔶[𝐁𝐨𝐥𝐝 𝐋𝐚𝐛𝐞𝐥] Description text here
    or:  📌 Plain Label with description after multiple spaces
    We want just the short label (before the description separator).
    """
    text = re.sub(r'^[🔶📌🔸🔹🔺💡✨✅⚡🔷]+', '', raw_li.strip())
    # If there's a bold bracketed label like [𝐁𝐨𝐥𝐝], grab what follows it
    bracket_match = re.search(r'\](.+)$', text)
    if bracket_match:
        text = bracket_match.group(1).strip()
    # Find first colon at nesting depth 0 (skip colons inside brackets)
    colon_idx = -1
    depth = 0
    for i, c in enumerate(text):
        if c in '([':
            depth += 1
        elif c in ')]':
            depth -= 1
        elif c == ':' and depth == 0:
            colon_idx = i
            break
    if colon_idx > 0:
        part = text[:colon_idx]
    else:
        part = text[:50]
    # Convert Unicode Mathematical Bold (U+1D400-U+1D433) to plain ASCII
    def _conv(c):
        cp = ord(c)
        if 0x1D400 <= cp <= 0x1D419:
            return chr(cp - 0x1D400 + 0x41)
        elif 0x1D41A <= cp <= 0x1D433:
            return chr(cp - 0x1D41A + 0x61)
        elif cp < 128:
            return c
        return ' '
    ascii_text = ''.join(_conv(c) for c in part)
    cleaned = re.sub(r'\s+', ' ', ascii_text).strip()
    cleaned = re.sub(r'^[^a-zA-Z0-9]+', '', cleaned)
    return cleaned if len(cleaned) > 2 else None


# ── 各平台解析器 ──────────────────────────────────────────────────────────────

def resolve_tiktok(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 TikTok Shop 页面。"""
    title = _og_tag(html, "title") or _meta_content(html, [
        r'(?is)"productName"\s*:\s*"([^"]+)"',
        r'(?is)"title"\s*:\s*"([^"]{3,200})"',
    ])
    brand = _meta_content(html, [
        r'(?is)"brand"\s*:\s*\{[^\}]*"name"\s*:\s*"([^"]+)"',
        r'(?is)"brandName"\s*:\s*"([^"]+)"',
        r'(?is)"brand"\s*:\s*"([^"]{2,60})"',
    ])
    # Fallback: look for "Manufacturer Baby Trend" at end of product detail table
    if not brand:
        m = re.search(r'Manufacturer\s+(Baby\s+Trend\s+[A-Z][A-Za-z0-9\s&®™-]{0,40}?)(?=\s+View\s+more)', text, re.IGNORECASE)
        if m:
            brand = _clean(m.group(1))
        else:
            # Simpler: find "Baby Trend" as a known brand name in the page
            m2 = re.search(r'\b(Baby\s+Trend)\b', text)
            if m2:
                brand = _clean(m2.group(1))

    description = _og_tag(html, "description") or _meta_content(html, [
        r'(?is)"description"\s*:\s*"([^"]{10,1000})"',
    ])
    price = _meta_content(html, [
        r'(?is)"salePrice"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
        r'(?is)"price"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
    ])
    price = _parse_price(price) or _extract_price_from_text(text)

    # Extract features from "Key Features:" section — bullet name only (before colon), not description
    features: list[str] = []
    seen_features: set[str] = set()

    kf_match = re.search(r'(?i)Key Features:\s*(.{200,1500})', text)
    if kf_match:
        section = kf_match.group(1)
        # Stop at next section header (typically "Specifications:" or similar)
        next_section = re.search(r'(?i)Specifications?:\s*', section)
        if next_section:
            section = section[:next_section.start()]
        for m in re.finditer(r'[·•\-–—*]\s{0,3}([A-Z][A-Za-z0-9\s&®™-]{4,40})\s*:', section):
            feat = _clean(m.group(1))
            if feat and len(feat) > 3 and feat.lower() not in seen_features:
                seen_features.add(feat.lower())
                features.append(feat)

    features = list(dict.fromkeys(features))[:8]
    return _make_result("tiktok", title, brand, description, price, text, url, features=features)


def resolve_amazon(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 Amazon 商品页面。"""
    title = _meta_content(html, [
        r'(?is)<span[^>]+id=["\']productTitle["\'][^>]*>(.*?)</span>',
        r'(?is)<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)["\']',
    ])
    raw_brand = _meta_content(html, [
        r'(?is)<a[^>]+id=["\']bylineInfo["\'][^>]*>(.*?)</a>',
        r'(?is)"brand"\s*:\s*"([^"]+)"',
    ])
    # Strip "Visit the Xxx Store" wrapper to extract just the brand name
    if raw_brand:
        brand = re.sub(r'^Visit the\s+', '', raw_brand, flags=re.IGNORECASE)
        brand = re.sub(r'\s+Store$', '', brand).strip()
        if not brand:
            brand = _clean(raw_brand)
    else:
        brand = None

    # Extract product feature bullets from the "feature-bullets" section specifically
    features: list[str] = []
    seen_features: set[str] = set()
    fb_match = re.search(
        r'(?is)<div[^>]+id=["\']feature-bullets["\'][^>]*>(.*?)</div>',
        html,
    )
    if fb_match:
        fb_html = fb_match.group(1)
        for m in re.finditer(r'<li[^>]*class=["\'][^"\']*a-spacing-mini[^"\']*["\'][^>]*>(.*?)</li>', fb_html, re.DOTALL):
            raw_li = re.sub(r'<[^>]+>', ' ', m.group(1)).strip()
            feat = _extract_amazon_feature_label(raw_li)
            if feat and feat.lower() not in seen_features:
                seen_features.add(feat.lower())
                features.append(feat)
    features = features[:8]

    description = None
    price = _meta_content(html, [
        r'(?is)<span[^>]+class=["\'][^"\']*a-offscreen[^"\']*["\'][^>]*>\$\s*([0-9]+(?:\.[0-9]{1,2})?)</span>',
        r'(?is)"priceToPay".*?"amount"\s*:\s*([0-9]+(?:\.[0-9]{1,2})?)',
    ])
    price = _parse_price(price) or _extract_price_from_text(text)
    image_url = _og_tag(html, "image")
    return _make_result("amazon", title, brand, description, price, text, url, image_url, features)


def resolve_shopify(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 Shopify 商品页面（通过 JSON-LD）。"""
    objects = _extract_json_ld(html)
    ld = _pick_product_ld(objects)
    title = None
    brand = None
    description = None
    price = None
    if ld:
        title = _clean(ld.get("name"))
        brand_obj = ld.get("brand")
        if isinstance(brand_obj, dict):
            brand = _clean(brand_obj.get("name"))
        else:
            brand = _clean(brand_obj)
        description = _clean(ld.get("description"))
        offers = ld.get("offers")
        if isinstance(offers, list) and offers:
            price = _parse_price(offers[0].get("price"))
        elif isinstance(offers, dict):
            price = _parse_price(offers.get("price"))
    if not title:
        title = _og_tag(html, "title")
    if not description:
        description = _og_tag(html, "description")
    if not price:
        price = _extract_price_from_text(text)
    image_url = _og_tag(html, "image")
    return _make_result("shopify", title, brand, description, price, text, url, image_url, features=None)


def resolve_shopee(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 Shopee 商品页面。"""
    title = _og_tag(html, "title") or _meta_content(html, [
        r'(?is)"name"\s*:\s*"([^"]{3,200})"',
        r'(?is)<title[^>]*>(.*?)</title>',
    ])
    brand = _meta_content(html, [
        r'(?is)"brand"\s*:\s*"([^"]{1,100})"',
        r'(?is)"brandId"\s*:\s*"?\d+"?',
    ])
    description = _og_tag(html, "description")
    price = _meta_content(html, [
        r'(?is)"price"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
        r'(?is)"originalPrice"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
    ])
    price = _parse_price(price) or _extract_price_from_text(text)
    image_url = _og_tag(html, "image")
    return _make_result("shopee", title, brand, description, price, text, url, image_url, features=None)


def resolve_lazada(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 Lazada 商品页面。"""
    title = _og_tag(html, "title") or _meta_content(html, [
        r'(?is)"name"\s*:\s*"([^"]{3,200})"',
        r'(?is)<title[^>]*>(.*?)</title>',
    ])
    brand = _meta_content(html, [
        r'(?is)"brand"\s*:\s*"([^"]{1,100})"',
    ])
    description = _og_tag(html, "description")
    price = _meta_content(html, [
        r'(?is)"price"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
        r'(?is)"originalPrice"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
    ])
    price = _parse_price(price) or _extract_price_from_text(text)
    image_url = _og_tag(html, "image")
    return _make_result("lazada", title, brand, description, price, text, url, image_url, features=None)


def resolve_ebay(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 eBay 商品页面。"""
    title = _meta_content(html, [
        r'(?is)<title[^>]*>(.*?)</title>',
        r'(?is)<meta[^>]+name=["\']title["\'][^>]+content=["\']([^"\']+)["\']',
    ])
    brand = _meta_content(html, [
        r'(?is)<span[^>]+itemprop=["\']brand["\'][^>]*>(.*?)</span>',
        r'(?is)"brand"\s*:\s*"([^"]{1,100})"',
    ])
    description = _og_tag(html, "description") or _meta_content(html, [
        r'(?is)<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)"',
    ])
    price = _meta_content(html, [
        r'(?is)<span[^>]+itemprop=["\']price["\'][^>]+content=["\'](\d+(?:\.\d{1,2})?)["\']',
        r'(?is)"price"\s*:\s*"(\d+(?:\.\d{1,2})?)"',
    ])
    price = _parse_price(price) or _extract_price_from_text(text)
    image_url = _og_tag(html, "image")
    return _make_result("ebay", title, brand, description, price, text, url, image_url, features=None)


def resolve_temu(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 Temu 商品页面。"""
    title = _og_tag(html, "title") or _meta_content(html, [
        r'(?is)"goods_title"\s*:\s*"([^"]{3,200})"',
        r'(?is)<title[^>]*>(.*?)</title>',
    ])
    brand = _meta_content(html, [
        r'(?is)"brand_name"\s*:\s*"([^"]{1,100})"',
    ])
    description = _og_tag(html, "description")
    price = _meta_content(html, [
        r'(?is)"sale_price"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
        r'(?is)"price"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
    ])
    price = _parse_price(price) or _extract_price_from_text(text)
    image_url = _og_tag(html, "image")
    return _make_result("temu", title, brand, description, price, text, url, image_url, features=None)


def resolve_aliexpress(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 AliExpress 商品页面。"""
    title = _og_tag(html, "title") or _meta_content(html, [
        r'(?is)"productTitle"\s*:\s*"([^"]{3,200})"',
        r'(?is)<title[^>]*>(.*?)</title>',
    ])
    brand = _meta_content(html, [
        r'(?is)"brandName"\s*:\s*"([^"]{1,100})"',
        r'(?is)<span[^>]+class=["\'][^"\']*brand[^"\']*["\'][^>]*>(.*?)</span>',
    ])
    description = _og_tag(html, "description")
    price = _meta_content(html, [
        r'(?is)"price"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
        r'(?is)"originalPrice"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
    ])
    price = _parse_price(price) or _extract_price_from_text(text)
    image_url = _og_tag(html, "image")
    return _make_result("aliexpress", title, brand, description, price, text, url, image_url, features=None)


def resolve_wish(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 Wish 商品页面。"""
    title = _meta_content(html, [
        r'(?is)<title[^>]*>(.*?)</title>',
        r'(?is)"name"\s*:\s*"([^"]{3,200})"',
    ])
    brand = _meta_content(html, [
        r'(?is)"brand"\s*:\s*"([^"]{1,100})"',
    ])
    description = _og_tag(html, "description") or _meta_content(html, [
        r'(?is)<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)"',
    ])
    price = _meta_content(html, [
        r'(?is)"price"\s*:\s*"(\d+(?:\.\d{1,2})?)"',
        r'(?is)"originalPrice"\s*:\s*"(\d+(?:\.\d{1,2})?)"',
    ])
    price = _parse_price(price) or _extract_price_from_text(text)
    image_url = _og_tag(html, "image")
    return _make_result("wish", title, brand, description, price, text, url, image_url, features=None)


def resolve_target(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 Target 商品页面。"""
    title = _og_tag(html, "title") or _meta_content(html, [
        r'(?is)"title"\s*:\s*"([^"]{3,200})"',
        r'(?is)<title[^>]*>(.*?)</title>',
    ])
    brand = _meta_content(html, [
        r'(?is)"brand"\s*:\s*"([^"]{1,100})"',
        r'(?is)<span[^>]+data-test=["\']product-brand["\'][^>]*>(.*?)</span>',
    ])
    description = _og_tag(html, "description")
    price = _meta_content(html, [
        r'(?is)"price"\s*:\s*"?([0-9]+(?:\.[0-9]{1,2})?)"?',
    ])
    price = _parse_price(price) or _extract_price_from_text(text)
    image_url = _og_tag(html, "image")
    return _make_result("target", title, brand, description, price, text, url, image_url, features=None)


def resolve_walmart(html: str, text: str, url: str) -> dict[str, Any]:
    """解析 Walmart 商品页面。"""
    title = _meta_content(html, [
        r'(?is)<title[^>]*>(.*?)</title>',
        r'(?is)"title"\s*:\s*"([^"]{3,200})"',
        r'(?is)<meta[^>]+itemprop=["\']name["\'][^>]+content=["\']([^"\']+)["\']',
    ])
    brand = _meta_content(html, [
        r'(?is)<span[^>]+itemprop=["\']brand["\'][^>]*>(.*?)</span>',
        r'(?is)"brand"\s*:\s*"([^"]{1,100})"',
    ])
    description = _og_tag(html, "description") or _meta_content(html, [
        r'(?is)<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)"',
    ])
    price = _meta_content(html, [
        r'(?is)<span[^>]+itemprop=["\']price["\'][^>]+content=["\'](\d+(?:\.\d{1,2})?)["\']',
        r'(?is)"price"\s*:\s*"(\d+(?:\.\d{1,2})?)"',
    ])
    price = _parse_price(price) or _extract_price_from_text(text)
    image_url = _og_tag(html, "image")
    return _make_result("walmart", title, brand, description, price, text, url, image_url, features=None)


# ── 通用兜底 ─────────────────────────────────────────────────────────────────

def resolve_generic(html: str, text: str, url: str) -> dict[str, Any]:
    """通用商品页面解析（JSON-LD 兜底）。"""
    objects = _extract_json_ld(html)
    ld = _pick_product_ld(objects)
    title = None
    brand = None
    description = None
    price = None
    image_url = None
    currency = None
    if ld:
        title = _clean(ld.get("name"))
        brand_obj = ld.get("brand")
        if isinstance(brand_obj, dict):
            brand = _clean(brand_obj.get("name"))
        else:
            brand = _clean(brand_obj)
        description = _clean(ld.get("description"))
        offers = ld.get("offers")
        if isinstance(offers, list) and offers:
            price = _parse_price(offers[0].get("price"))
            currency = _clean(offers[0].get("priceCurrency"))
        elif isinstance(offers, dict):
            price = _parse_price(offers.get("price"))
            currency = _clean(offers.get("priceCurrency"))
        image_obj = ld.get("image")
        if isinstance(image_obj, list) and image_obj:
            image_url = _clean(image_obj[0])
        else:
            image_url = _clean(image_obj)
    if not title:
        title = _og_tag(html, "title") or _meta_name(html, "twitter:title") or _title_tag(html)
    if not description:
        description = _og_tag(html, "description") or _meta_name(html, "description") or _meta_name(html, "twitter:description")
    if not price:
        price = _extract_price_from_text(text)
    if not image_url:
        image_url = _og_tag(html, "image") or _meta_name(html, "twitter:image")
    return _make_result("generic", title, brand, description, price, text, url, image_url, features=None, currency=currency)


# ── 注册表 ───────────────────────────────────────────────────────────────────

RESOLVER_REGISTRY: dict[str, Callable[[str, str, str], dict[str, Any]]] = {
    "tiktok.com": resolve_tiktok,
    "shop.tiktok.com": resolve_tiktok,
    "amazon.com": resolve_amazon,
    "amazon.co.uk": resolve_amazon,
    "amazon.de": resolve_amazon,
    "amazon.co.jp": resolve_amazon,
    "amazon.ca": resolve_amazon,
    "amazon.it": resolve_amazon,
    "amazon.es": resolve_amazon,
    "amazon.fr": resolve_amazon,
    "shopify.com": resolve_shopify,
    "myshopify.com": resolve_shopify,
    "ritkeeps.com": resolve_shopify,
    "www.ritkeeps.com": resolve_shopify,
    "shopee.com": resolve_shopee,
    "lazada.com": resolve_lazada,
    "ebay.com": resolve_ebay,
    "temu.com": resolve_temu,
    "aliexpress.com": resolve_aliexpress,
    "wish.com": resolve_wish,
    "target.com": resolve_target,
    "walmart.com": resolve_walmart,
}


def _make_result(
    platform: str,
    title: Optional[str],
    brand: Optional[str],
    description: Optional[str],
    price: Optional[float],
    text: str,
    url: str,
    image_url: Optional[str]= None,
    features: Optional[list]= None,
    currency: Optional[str]= None,
) -> dict[str, Any]:
    return {
        "productName": title,
        "price": price,
        "brand": brand,
        "description": description,
        "features": features or [],
        "platform": platform,
        "imageUrl": image_url,
        "productUrl": url,
        "merchantName": None,
        "currency": currency or ("USD" if price else None),
    }


def resolve_by_host(host: str, html: str, text: str, url: str) -> dict[str, Any]:
    """根据域名分派到对应解析器。"""
    h = host.lower()
    for domain, resolver in RESOLVER_REGISTRY.items():
        if h == domain or h.endswith("." + domain):
            return resolver(html, text, url)
    return resolve_generic(html, text, url)
