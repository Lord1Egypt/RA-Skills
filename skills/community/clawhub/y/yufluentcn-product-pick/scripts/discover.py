"""Browser Service 候选品发现（run.py --discover 模式）。"""

from __future__ import annotations

import os
import re
from typing import Any
from urllib.parse import quote_plus, urlencode

import requests

DEFAULT_BROWSER_URL = "http://127.0.0.1:9222"
DEFAULT_TIMEOUT = 120.0

DISCOVER_SOURCES = frozenset({"amazon_serp", "amazon_bs", "tiktok_trending"})


class DiscoverError(RuntimeError):
    """Browser 发现失败。"""


def browser_service_url(explicit: str | None = None) -> str:
    raw = (explicit or os.getenv("BROWSER_SERVICE_URL") or DEFAULT_BROWSER_URL).strip()
    return raw.rstrip("/")


def amazon_search_url(query: str, *, host: str = "www.amazon.com") -> str:
    q = str(query or "").strip()
    if not q:
        raise DiscoverError("搜索关键词为空")
    return f"https://{host}/s?{urlencode({'k': q})}"


def amazon_bs_search_url(query: str, *, host: str = "www.amazon.com") -> str:
    q = str(query or "").strip()
    if not q:
        raise DiscoverError("搜索关键词为空")
    return f"https://{host}/s?{urlencode({'k': q, 's': 'exact-aware-popularity-rank'})}"


def tiktok_shop_search_url(query: str) -> str:
    q = str(query or "").strip()
    if not q:
        raise DiscoverError("搜索关键词为空")
    return f"https://www.tiktok.com/shop/search?q={quote_plus(q)}"


def resolve_discover_url(source: str, search_query: str) -> str:
    key = str(source or "").strip().lower()
    if key == "amazon_serp":
        return amazon_search_url(search_query)
    if key == "amazon_bs":
        return amazon_bs_search_url(search_query)
    if key == "tiktok_trending":
        return tiktok_shop_search_url(search_query)
    raise DiscoverError(f"未知 discover-source: {source}")


def _csv_cell(value: str) -> str:
    text = str(value or "").replace("\n", " ").strip()
    if "," in text or '"' in text:
        return '"' + text.replace('"', '""') + '"'
    return text


def format_product_candidates_table(rows: list[dict[str, str]]) -> str:
    header = (
        "platform,asin,title,bsr,price,rating,review_count,url,serp_rank,discover_source"
    )
    lines = [header]
    for row in rows:
        lines.append(
            ",".join(
                [
                    row.get("platform", ""),
                    row.get("asin", ""),
                    _csv_cell(row.get("title", "")),
                    _csv_cell(row.get("bsr", "")),
                    row.get("price", ""),
                    row.get("rating", ""),
                    row.get("review_count", ""),
                    row.get("url", ""),
                    row.get("serp_rank", ""),
                    row.get("discover_source", ""),
                ]
            )
        )
    return "\n".join(lines)


def _post_json(base_url: str, path: str, payload: dict[str, Any] | None = None) -> dict[str, Any]:
    url = f"{base_url}{path}"
    try:
        res = requests.post(url, json=payload or {}, timeout=DEFAULT_TIMEOUT)
        res.raise_for_status()
        data = res.json()
        if not isinstance(data, dict):
            raise DiscoverError(f"Browser 返回非 JSON 对象: {path}")
        return data
    except requests.RequestException as exc:
        raise DiscoverError(
            f"Browser Service 请求失败 ({url}): {exc}. "
            "请确认 BROWSER_SERVICE_URL 已配置且服务已启动。"
        ) from exc


def _get_json(base_url: str, path: str, *, params: dict[str, str] | None = None) -> dict[str, Any]:
    url = f"{base_url}{path}"
    try:
        res = requests.get(url, params=params or {}, timeout=DEFAULT_TIMEOUT)
        res.raise_for_status()
        data = res.json()
        if not isinstance(data, dict):
            raise DiscoverError(f"Browser 返回非 JSON 对象: {path}")
        return data
    except requests.RequestException as exc:
        raise DiscoverError(f"Browser Service 请求失败 ({url}): {exc}") from exc


def browser_open(base_url: str, url: str) -> dict[str, Any]:
    return _post_json(base_url, "/v1/browser/open", {"url": url})


def browser_extract(base_url: str, tab_id: str, *, schema: str) -> dict[str, Any]:
    return _post_json(
        base_url,
        f"/v1/browser/{tab_id}/extract",
        {"extract_schema": schema},
    )


def browser_snapshot(base_url: str, tab_id: str) -> dict[str, Any]:
    return _get_json(base_url, f"/v1/browser/{tab_id}/snapshot", params={"format": "markdown"})


def amazon_listing_url(asin: str, *, host: str = "www.amazon.com") -> str:
    a = str(asin or "").strip().upper()
    if len(a) != 10:
        raise DiscoverError(f"无效 ASIN: {asin}")
    return f"https://{host}/dp/{a}"


def _listing_row_from_extract(
    extracted: dict[str, Any],
    *,
    platform: str,
    discover_source: str,
    serp_rank: str = "",
) -> dict[str, str]:
    data = extracted.get("data") if isinstance(extracted.get("data"), dict) else {}
    asin = str(data.get("asin") or "").strip()
    return {
        "platform": platform,
        "asin": asin,
        "title": str(data.get("title") or "").strip()[:200],
        "bsr": str(data.get("bsr") or "").strip()[:200],
        "price": str(data.get("price") or "").strip()[:40],
        "rating": str(data.get("rating") or "").strip()[:20],
        "review_count": str(data.get("review_count") or "").strip()[:20],
        "url": str(extracted.get("url") or data.get("url") or "").strip(),
        "serp_rank": serp_rank,
        "discover_source": discover_source,
    }


def _serp_rows_from_extract(
    extracted: dict[str, Any],
    *,
    discover_source: str,
) -> list[dict[str, str]]:
    data = extracted.get("data") if isinstance(extracted.get("data"), dict) else {}
    rows: list[dict[str, str]] = []
    for item in data.get("query_results") or []:
        if not isinstance(item, dict) or item.get("sponsored"):
            continue
        asin = str(item.get("asin") or "").strip()
        title = str(item.get("title") or "").strip()
        if not asin and not title:
            continue
        rows.append(
            {
                "platform": "amazon",
                "asin": asin,
                "title": title[:200],
                "bsr": "",
                "price": str(item.get("price") or "").strip()[:40],
                "rating": str(item.get("rating") or "").strip()[:20],
                "review_count": "",
                "url": amazon_listing_url(asin) if asin else "",
                "serp_rank": str(item.get("rank") or ""),
                "discover_source": discover_source,
            }
        )
    return rows


def _tiktok_row_from_extract(
    extracted: dict[str, Any],
    *,
    discover_source: str,
) -> dict[str, str]:
    data = extracted.get("data") if isinstance(extracted.get("data"), dict) else {}
    sold = str(data.get("sold") or "").strip()
    return {
        "platform": "tiktok",
        "asin": "",
        "title": str(data.get("title") or "").strip()[:200],
        "bsr": sold,
        "price": str(data.get("price") or "").strip()[:40],
        "rating": str(data.get("rating") or "").strip()[:20],
        "review_count": "",
        "url": str(extracted.get("url") or data.get("url") or "").strip(),
        "serp_rank": "",
        "discover_source": discover_source,
    }


_TIKTOK_PRODUCT_URL_RE = re.compile(
    r"https?://(?:www\.)?tiktok\.com/shop/(?:product|p)/[^\s\)\]\"']+",
    re.I,
)


def _tiktok_product_urls_from_snapshot(snapshot: dict[str, Any], *, limit: int) -> list[str]:
    content = str(snapshot.get("content") or snapshot.get("markdown") or "")
    found: list[str] = []
    for match in _TIKTOK_PRODUCT_URL_RE.findall(content):
        url = match.rstrip(".,)")
        if url not in found:
            found.append(url)
        if len(found) >= limit:
            break
    return found


def _discover_amazon(
    *,
    base_url: str,
    search_query: str,
    discover_source: str,
    max_candidates: int,
    enrich_listings: bool,
) -> list[dict[str, str]]:
    start_url = resolve_discover_url(discover_source, search_query)
    opened = browser_open(base_url, start_url)
    tab_id = str(opened.get("tab_id") or "").strip()
    if not tab_id:
        raise DiscoverError("Browser open 未返回 tab_id")

    serp = browser_extract(base_url, tab_id, schema="amazon_serp")
    serp_rows = _serp_rows_from_extract(serp, discover_source=discover_source)
    if not serp_rows:
        raise DiscoverError(f"Amazon 未发现候选品（source={discover_source}, query={search_query!r}）")

    targets = serp_rows[: max(1, max_candidates)]
    if not enrich_listings:
        return targets

    rows: list[dict[str, str]] = []
    for base_row in targets:
        asin = base_row.get("asin") or ""
        if not asin:
            rows.append(base_row)
            continue
        listing_open = browser_open(base_url, amazon_listing_url(asin))
        lid = str(listing_open.get("tab_id") or "").strip()
        if not lid:
            rows.append(base_row)
            continue
        listing_ex = browser_extract(base_url, lid, schema="amazon_listing")
        detail = _listing_row_from_extract(
            listing_ex,
            platform="amazon",
            discover_source=discover_source,
            serp_rank=base_row.get("serp_rank", ""),
        )
        if not detail.get("price") and base_row.get("price"):
            detail["price"] = base_row["price"]
        if not detail.get("rating") and base_row.get("rating"):
            detail["rating"] = base_row["rating"]
        rows.append(detail)
    return rows or targets


def _discover_tiktok(
    *,
    base_url: str,
    search_query: str,
    discover_source: str,
    max_candidates: int,
) -> list[dict[str, str]]:
    start_url = resolve_discover_url(discover_source, search_query)
    opened = browser_open(base_url, start_url)
    tab_id = str(opened.get("tab_id") or "").strip()
    if not tab_id:
        raise DiscoverError("Browser open 未返回 tab_id")

    snapshot = browser_snapshot(base_url, tab_id)
    product_urls = _tiktok_product_urls_from_snapshot(snapshot, limit=max_candidates)
    rows: list[dict[str, str]] = []

    if product_urls:
        for url in product_urls:
            item_open = browser_open(base_url, url)
            iid = str(item_open.get("tab_id") or "").strip()
            if not iid:
                continue
            extracted = browser_extract(base_url, iid, schema="tiktok_product")
            rows.append(_tiktok_row_from_extract(extracted, discover_source=discover_source))
            if len(rows) >= max_candidates:
                break

    if rows:
        return rows

    extracted = browser_extract(base_url, tab_id, schema="tiktok_product")
    data = extracted.get("data") if isinstance(extracted.get("data"), dict) else {}
    if data.get("title") or data.get("price"):
        return [_tiktok_row_from_extract(extracted, discover_source=discover_source)]

    generic = browser_extract(base_url, tab_id, schema="generic")
    gdata = generic.get("data") if isinstance(generic.get("data"), dict) else {}
    preview = str(gdata.get("text_preview") or gdata.get("title") or "")[:500]
    if not preview:
        raise DiscoverError(f"TikTok Shop 未发现候选品（query={search_query!r}）")
    return [
        {
            "platform": "tiktok",
            "asin": "",
            "title": f"{search_query[:180]} (search snapshot)",
            "bsr": "",
            "price": "",
            "rating": "",
            "review_count": "",
            "url": start_url,
            "serp_rank": "",
            "discover_source": discover_source,
        }
    ]


def discover_candidates(
    discover_source: str,
    search_query: str,
    *,
    max_candidates: int = 20,
    browser_url: str | None = None,
) -> str:
    """
    通过 Browser Service 发现候选品，返回 product_candidates CSV 文本。
    """
    source = str(discover_source or "").strip().lower()
    if source not in DISCOVER_SOURCES:
        raise DiscoverError(f"未知 discover-source: {discover_source}")

    query = str(search_query or "").strip()
    if not query:
        raise DiscoverError("search-query 为空")

    limit = max(1, min(int(max_candidates), 50))
    base = browser_service_url(browser_url)

    if source in ("amazon_serp", "amazon_bs"):
        rows = _discover_amazon(
            base_url=base,
            search_query=query,
            discover_source=source,
            max_candidates=limit,
            enrich_listings=True,
        )
    else:
        rows = _discover_tiktok(
            base_url=base,
            search_query=query,
            discover_source=source,
            max_candidates=limit,
        )

    if not rows:
        raise DiscoverError("未发现任何候选品")
    return format_product_candidates_table(rows)


def resolve_search_query(args: Any) -> str:
    return str(getattr(args, "search_query", None) or getattr(args, "niche", None) or "").strip()
