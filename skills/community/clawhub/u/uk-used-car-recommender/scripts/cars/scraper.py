from __future__ import annotations

import json
import re
from typing import Any

import requests
from bs4 import BeautifulSoup, Tag

from .urls import CLIENT_SORT_VALUES

_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
}

_LISTING_ID_RE = re.compile(r"/(\d+)(?:[/?#]|$)")
_MAKE_PATH_RE = re.compile(r"/p/([^/]+)/")

# 品牌 slug → 规范显示名称（特殊写法或含连字符的品牌）
_MAKE_DISPLAY_NAMES: dict[str, str] = {
    "mercedes-benz": "Mercedes-Benz",
    "mg-motor-uk": "MG",
    "alfa-romeo": "Alfa Romeo",
    "aston-martin": "Aston Martin",
    "land-rover": "Land Rover",
    "rolls-royce": "Rolls-Royce",
    "bentley-motors": "Bentley",
    "daf-trucks": "DAF Trucks",
    "great-wall": "Great Wall",
    "mitsubishi-cv": "Mitsubishi CV",
    "mitsubishi-fuso": "Mitsubishi Fuso",
    "renault-trucks": "Renault Trucks",
    "isuzu-trucks": "Isuzu Trucks",
    "byd": "BYD",
    "bmw": "BMW",
    "mg": "MG",
    "ds": "DS",
}


def _make_slug_to_display(slug: str) -> str:
    """将 Gumtree URL 中的品牌 slug 转换为可读品牌名称。"""
    if not slug:
        return slug
    if slug in _MAKE_DISPLAY_NAMES:
        return _MAKE_DISPLAY_NAMES[slug]
    # 默认：连字符换空格，每词首字母大写
    return " ".join(word.capitalize() for word in slug.split("-"))


def _extract_make_from_url(url: str | None) -> str | None:
    """从帖子 URL 路径 /p/{make}/{title}/{id} 中提取品牌名称。"""
    if not url:
        return None
    m = _MAKE_PATH_RE.search(url)
    if not m:
        return None
    return _make_slug_to_display(m.group(1))


# ── JSON-LD 提取 ──────────────────────────────────────────────────────────────

def _extract_json_ld_urls(soup: BeautifulSoup) -> dict[str, str]:
    """从 JSON-LD 结构化数据中提取 listing URL（id → absolute url）。"""
    url_by_id: dict[str, str] = {}
    for script in soup.find_all("script", type="application/ld+json"):
        if not isinstance(script, Tag):
            continue
        try:
            data = json.loads(script.string or "")
        except (json.JSONDecodeError, AttributeError):
            continue
        entries = data if isinstance(data, list) else [data]
        for entry in entries:
            if not isinstance(entry, dict) or entry.get("@type") != "SearchResultsPage":
                continue
            main_entity = entry.get("mainEntity") or {}
            for item in main_entity.get("itemListElement") or []:
                url = str(item.get("url") or "")
                if not url:
                    continue
                match = _LISTING_ID_RE.search(url)
                if match:
                    url_by_id[match.group(1)] = url
    return url_by_id


# ── 内联 JS 数据提取 ──────────────────────────────────────────────────────────

def _extract_js_array(html: str, var_name: str) -> list[dict[str, Any]]:
    """从内联 <script> 中提取 window.<var_name> = [...] 的 JSON 数组。"""
    pattern = re.compile(
        rf"window\.{re.escape(var_name)}\s*=\s*(\[[\s\S]*?\])\s*;",
        re.MULTILINE,
    )
    match = pattern.search(html)
    if not match:
        return []
    try:
        result = json.loads(match.group(1))
        return result if isinstance(result, list) else []
    except json.JSONDecodeError:
        return []


# ── DOM 汽车属性提取 ──────────────────────────────────────────────────────────

def _card_text(card: Tag, selector: str) -> str | None:
    """从卡片中按 data-q 属性提取文本。"""
    el = card.find(attrs={"data-q": selector})
    if not isinstance(el, Tag):
        return None
    text = " ".join(el.get_text().split()).strip()
    return text or None


def _extract_dom_car_attrs(soup: BeautifulSoup) -> dict[str, dict[str, str | None]]:
    """
    从搜索结果卡片中提取汽车专属 DOM 属性。

    返回 {listing_id: {year, mileage, fuel_type, engine_size, seller_type,
                        price_display, location, title, number_of_images, image_url}} 。
    """
    result: dict[str, dict[str, str | None]] = {}
    for card in soup.find_all("article", attrs={"data-q": "search-result"}):
        if not isinstance(card, Tag):
            continue
        anchor = card.find("a", attrs={"data-q": "search-result-anchor"})
        if not isinstance(anchor, Tag):
            continue
        href = str(anchor.get("href") or "")
        match = _LISTING_ID_RE.search(href)
        if not match:
            continue
        listing_id = match.group(1)

        # 提取图片 URL
        image_url: str | None = None
        img_tag = card.find("img", attrs={"data-q": "tile-image"})
        if isinstance(img_tag, Tag):
            # 优先使用 src，如果是懒加载则使用 data-src 或 data-lazy
            image_url = (
                str(img_tag.get("src") or "")
                or str(img_tag.get("data-src") or "")
                or str(img_tag.get("data-lazy") or "")
            )
            # 过滤掉占位符图片和空字符串
            if image_url and ("placeholder" in image_url.lower() or "data:image" in image_url):
                image_url = None
            # 如果是相对路径，转为绝对路径
            if image_url and not image_url.startswith("http"):
                image_url = f"https://www.gumtree.com{image_url}" if image_url.startswith("/") else None
        
        # 如果找不到带 data-q="tile-image" 的，尝试查找任何卡片内的图片
        if not image_url:
            img_tag = card.find("img")
            if isinstance(img_tag, Tag):
                image_url = (
                    str(img_tag.get("src") or "")
                    or str(img_tag.get("data-src") or "")
                    or str(img_tag.get("data-lazy") or "")
                )
                if image_url and ("placeholder" in image_url.lower() or "data:image" in image_url):
                    image_url = None
                if image_url and not image_url.startswith("http"):
                    image_url = f"https://www.gumtree.com{image_url}" if image_url.startswith("/") else None

        img_counter = _card_text(card, "tile-image-counter-label")
        result[listing_id] = {
            "year": _card_text(card, "motors-year"),
            "mileage": _card_text(card, "motors-mileage"),
            "fuel_type": _card_text(card, "motors-fuel-type"),
            "engine_size": _card_text(card, "motors-engine-size"),
            "seller_type_display": _card_text(card, "motors-seller-type"),
            "price_display": _card_text(card, "tile-price"),
            "location": _card_text(card, "tile-location"),
            "title": _card_text(card, "tile-title"),
            "url": (
                f"https://www.gumtree.com{href}"
                if href.startswith("/")
                else href
            ),
            "number_of_images": img_counter,
            "image_url": image_url or None,
        }
    return result


# ── DOM 降级解析 ──────────────────────────────────────────────────────────────

def _parse_listings_from_dom(
    soup: BeautifulSoup,
    url_by_id: dict[str, str],
    car_attrs: dict[str, dict[str, str | None]],
    limit: int,
) -> list[dict[str, Any]]:
    """降级方案：直接从 article 卡片 DOM 解析帖子信息。"""
    items: list[dict[str, Any]] = []
    for listing_id, attrs in car_attrs.items():
        resolved_url = attrs.get("url") or url_by_id.get(listing_id)
        items.append({
            "listing_id": listing_id,
            "title": attrs.get("title"),
            "price": attrs.get("price_display"),
            "price_pennies": None,
            "price_display": attrs.get("price_display"),
            "location": attrs.get("location"),
            "url": resolved_url,
            "age": None,
            "is_trade": (attrs.get("seller_type_display") or "").lower() == "trade" or None,
            "category": _extract_make_from_url(resolved_url),
            "category_id": None,
            "promotions": [],
            "number_of_images": attrs.get("number_of_images"),
            "image_url": attrs.get("image_url"),
            "is_delivery": None,
            "is_gbg_verified": None,
            "year": attrs.get("year"),
            "mileage": attrs.get("mileage"),
            "fuel_type": attrs.get("fuel_type"),
            "engine_size": attrs.get("engine_size"),
            "seller_type_display": attrs.get("seller_type_display"),
        })
        if len(items) >= limit:
            break
    return items


# ── 帖子标准化 ────────────────────────────────────────────────────────────────

def _normalise_listing(
    row: dict[str, Any],
    url: str | None,
    car_attrs: dict[str, str | None] | None,
) -> dict[str, Any]:
    """将 gumtreeDataLayer.listListingDetails 中的原始条目转为统一结构，
    并合并 DOM 中提取的汽车专属属性。"""
    listing_id = str(row.get("id") or "")
    if not listing_id:
        url_path = str(row.get("url") or row.get("path") or "")
        m = _LISTING_ID_RE.search(url_path)
        if m:
            listing_id = m.group(1)
    attrs = car_attrs or {}
    resolved_url = url or attrs.get("url")
    make_name = _extract_make_from_url(resolved_url)
    return {
        "listing_id": listing_id,
        "title": row.get("name") or row.get("title"),
        "price": row.get("price"),
        "price_pennies": row.get("pricePennies"),
        "price_display": attrs.get("price_display"),
        "location": row.get("location") or attrs.get("location"),
        "url": resolved_url,
        "age": row.get("age"),
        "is_trade": row.get("isTrade"),
        "category": make_name,
        "category_id": row.get("categoryId"),
        "promotions": row.get("promotions") if isinstance(row.get("promotions"), list) else [],
        "number_of_images": row.get("numberOfImages"),
        "image_url": attrs.get("image_url"),
        "is_delivery": row.get("isDelivery"),
        "is_gbg_verified": row.get("isGBGVerified"),
        # 汽车专属属性（从 DOM 提取）
        "year": attrs.get("year"),
        "mileage": attrs.get("mileage"),
        "fuel_type": attrs.get("fuel_type"),
        "engine_size": attrs.get("engine_size"),
        "seller_type_display": attrs.get("seller_type_display"),
    }


# ── 主搜索函数 ────────────────────────────────────────────────────────────────

def _parse_year(value: str | None) -> int:
    """将年份字符串解析为整数，无法解析时返回 0。"""
    if not value:
        return 0
    m = re.search(r"\d{4}", value)
    return int(m.group()) if m else 0


def _parse_mileage(value: str | None) -> int:
    """将里程字符串（如 '15,419 miles'）解析为整数，无法解析时返回 -1。"""
    if not value:
        return -1
    digits = re.sub(r"[^\d]", "", value)
    return int(digits) if digits else -1


def _client_sort(items: list[dict[str, Any]], sort: str) -> list[dict[str, Any]]:
    """对结果列表按年份或里程进行本地排序。"""
    if sort == "year_newest_first":
        return sorted(items, key=lambda x: _parse_year(x.get("year")), reverse=True)
    if sort == "year_oldest_first":
        return sorted(
            items,
            key=lambda x: (_parse_year(x.get("year")) == 0, _parse_year(x.get("year"))),
        )
    if sort == "mileage_lowest_first":
        return sorted(
            items,
            key=lambda x: (_parse_mileage(x.get("mileage")) < 0, _parse_mileage(x.get("mileage"))),
        )
    if sort == "mileage_highest_first":
        return sorted(items, key=lambda x: _parse_mileage(x.get("mileage")), reverse=True)
    return items


def run_car_search(
    search_url: str,
    limit: int = 10,
    sort: str | None = None,
    mock_html: str | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    """
    抓取并解析 Gumtree 二手车搜索结果页。

    优先从 window.gumtreeDataLayer 提取结构化数据；
    若失败则降级为 DOM 解析。
    """
    # ── 获取 HTML ─────────────────────────────────────────────────────────────
    if mock_html is not None:
        html = mock_html
        status = 200
    else:
        session = requests.Session()
        session.headers.update(_DEFAULT_HEADERS)
        try:
            response = session.get(search_url, timeout=timeout)
            status = response.status_code
            html = response.text
        except requests.RequestException as exc:
            return {
                "ok": False,
                "error": f"请求失败: {exc}",
                "items": [],
                "total": 0,
                "search_url": search_url,
            }

    if status != 200:
        return {
            "ok": False,
            "error": f"HTTP {status}",
            "items": [],
            "total": 0,
            "search_url": search_url,
        }

    soup = BeautifulSoup(html, "lxml")
    url_by_id = _extract_json_ld_urls(soup)
    car_attrs_by_id = _extract_dom_car_attrs(soup)

    # ── 尝试从 gumtreeDataLayer 提取 ─────────────────────────────────────────
    gumtree_layer = _extract_js_array(html, "gumtreeDataLayer")
    page_declaration = next(
        (e for e in gumtree_layer if isinstance(e, dict) and e.get("event") == "pageDeclaration"),
        None,
    )

    total_results: int | None = None
    page_number: int | None = None
    search_category_name: str | None = None
    search_location_name: str | None = None
    source: str

    if page_declaration and isinstance(page_declaration.get("listListingDetails"), list):
        raw_listings: list[Any] = page_declaration["listListingDetails"]
        search_bar = page_declaration.get("searchBar") or {}
        search_category_name = search_bar.get("categoryName")
        search_location_name = search_bar.get("locationName")

        # 从 dataLayer 获取总数和页码
        data_layer = _extract_js_array(html, "dataLayer")
        srp_event = next(
            (e for e in data_layer if isinstance(e, dict) and e.get("name") == "SrpViewEvent"),
            None,
        )
        if srp_event and isinstance(srp_event.get("s"), dict):
            s = srp_event["s"]
            total_results = s.get("tr")
            page_number = s.get("pn")

        items: list[dict[str, Any]] = []
        for row in raw_listings:
            if not isinstance(row, dict):
                continue
            listing_id = str(row.get("id") or "")
            if not listing_id:
                url_path = str(row.get("url") or row.get("path") or "")
                m = _LISTING_ID_RE.search(url_path)
                if m:
                    listing_id = m.group(1)
            url = url_by_id.get(listing_id)
            car_attrs = car_attrs_by_id.get(listing_id)
            items.append(_normalise_listing(row, url, car_attrs))

        source = "gumtreeDataLayer"
    else:
        # 降级为 DOM 解析
        items = _parse_listings_from_dom(soup, url_by_id, car_attrs_by_id, limit * 3)
        source = "dom-fallback"

    # 对年份/里程排序做本地二次排序，确保结果严格有序
    if sort and sort in CLIENT_SORT_VALUES:
        items = _client_sort(items, sort)

    limited = items[:limit]
    return {
        "ok": True,
        "source": source,
        "search_url": search_url,
        "total_results": total_results,
        "page_number": page_number,
        "search_category_name": search_category_name,
        "search_location_name": search_location_name,
        "total": len(limited),
        "items": limited,
    }
