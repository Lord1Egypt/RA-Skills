from __future__ import annotations

import asyncio
import hashlib
import json
import re
from urllib.parse import quote

from models import ListingItem, SearchIntent
from price_utils import parse_price_kr


def _run_async(coro_factory):
    try:
        return asyncio.run(coro_factory())
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro_factory())
        finally:
            loop.close()


def _is_valid_title(title: str) -> bool:
    if not title or len(title.strip()) < 2:
        return False
    bad = ("판매완료", "예약중", "거래완료", "광고", "No Title")
    return not any(token.lower() in title.lower() for token in bad)


def _extract_article_id(link: str) -> str:
    for pattern in (r"/products/(\d+)", r"-(\d+)(?:/|\?|$)", r"/articles/(\d+)"):
        m = re.search(pattern, link)
        if m:
            return m.group(1)
    return "hash_" + hashlib.sha1(link.encode("utf-8")).hexdigest()[:12]


def _location_from_text(text: str) -> str | None:
    m = re.search(r"(서울|부산|대구|인천|광주|대전|울산|세종|경기|강원|충북|충남|전북|전남|경북|경남|제주)[^\n|,/]{0,20}", text or "")
    return m.group(0).strip() if m else None


def _passes_filters(item: ListingItem, intent: SearchIntent) -> bool:
    title = (item.title or "").lower()
    if intent.exclude_terms and any(term.lower() in title for term in intent.exclude_terms):
        return False
    price = item.parse_price()
    if intent.min_price and price and price < intent.min_price:
        return False
    if intent.max_price and price and price > intent.max_price:
        return False
    if intent.location and item.market == "danggeun":
        if not item.location or intent.location.lower() not in item.location.lower():
            return False
    return True


async def _search_danggeun(page, intent: SearchIntent) -> list[ListingItem]:
    url = f"https://www.daangn.com/kr/buy-sell/?search={quote(intent.keyword)}&sort=recent"
    await page.goto(url, wait_until="domcontentloaded")
    await page.wait_for_timeout(1200)
    items: list[ListingItem] = []
    try:
        scripts = await page.locator("script[type='application/ld+json']").all_text_contents()
        for script_text in scripts:
            try:
                data = json.loads(script_text)
            except Exception:
                continue
            nodes = data if isinstance(data, list) else [data]
            for node in nodes:
                if not isinstance(node, dict) or node.get("@type") != "ItemList":
                    continue
                for entry in node.get("itemListElement", [])[: max(20, intent.limit * 3)]:
                    product = entry.get("item", {}) if isinstance(entry, dict) else {}
                    if not isinstance(product, dict):
                        continue
                    link = product.get("url") or ""
                    if link.startswith("/"):
                        link = "https://www.daangn.com" + link
                    title = str(product.get("name") or "").strip()
                    if not _is_valid_title(title):
                        continue
                    offers = product.get("offers") or {}
                    raw_price = offers.get("price") if isinstance(offers, dict) else None
                    price_text = f"{int(float(raw_price)):,}원" if raw_price else "가격문의"
                    description = str(product.get("description") or "")
                    items.append(ListingItem(
                        market="danggeun",
                        article_id=_extract_article_id(link),
                        title=title,
                        price_text=price_text,
                        link=link,
                        query=intent.raw_query,
                        thumbnail=product.get("image"),
                        location=_location_from_text(description),
                    ))
                    if len(items) >= intent.limit * 2:
                        return items
            if items:
                return items
    except Exception:
        pass
    cards = page.locator("a[data-gtm='search_article'][href^='/kr/buy-sell/']")
    count = min(await cards.count(), max(20, intent.limit * 3))
    for i in range(count):
        card = cards.nth(i)
        href = (await card.get_attribute("href") or "").strip()
        if not href:
            continue
        link = "https://www.daangn.com" + href if href.startswith("/") else href
        text = (await card.inner_text() or "").strip()
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            continue
        title = lines[0]
        if not _is_valid_title(title):
            continue
        price_text = next((line for line in lines[1:] if any(ch.isdigit() for ch in line)), "가격문의")
        items.append(ListingItem("danggeun", _extract_article_id(link), title, price_text, link, intent.raw_query, location=_location_from_text(text)))
    return items


async def _search_bunjang(page, intent: SearchIntent) -> list[ListingItem]:
    url = f"https://m.bunjang.co.kr/search/products?q={quote(intent.keyword)}&order=date"
    await page.goto(url, wait_until="domcontentloaded")
    await page.wait_for_timeout(1200)
    cards = page.locator("a[data-pid]")
    items: list[ListingItem] = []
    count = min(await cards.count(), max(20, intent.limit * 3))
    for i in range(count):
        card = cards.nth(i)
        pid = (await card.get_attribute("data-pid") or "").strip()
        if not pid:
            continue
        text = (await card.inner_text() or "").strip()
        lines = [line.strip() for line in text.splitlines() if line.strip() and line.strip() not in {"배송비포함", "검수가능", "·"}]
        if not lines:
            continue
        title = lines[0]
        if not _is_valid_title(title):
            continue
        price_text = next((line for line in lines[1:] if any(ch.isdigit() for ch in line)), "가격문의")
        location = None
        for line in reversed(lines):
            compact = line.replace(",", "").replace(" ", "")
            if line == title or compact.isdigit() or compact.endswith("원"):
                continue
            location = None if "지역정보없음" in compact else line
            break
        items.append(ListingItem("bunjang", pid, title, price_text, f"https://m.bunjang.co.kr/products/{pid}", intent.raw_query, location=location))
    return items


async def _search_joonggonara(page, intent: SearchIntent) -> list[ListingItem]:
    url = "https://search.naver.com/search.naver?where=article&query=" + quote(f"{intent.keyword} site:cafe.naver.com/joonggonara")
    await page.goto(url, wait_until="domcontentloaded")
    await page.wait_for_timeout(1200)
    selectors = ["a.title_link", "a.api_txt_lines.total_tit", "a[href*='cafe.naver.com/joonggonara']"]
    items: list[ListingItem] = []
    seen: set[str] = set()
    for selector in selectors:
        loc = page.locator(selector)
        count = min(await loc.count(), max(20, intent.limit * 3))
        for i in range(count):
            el = loc.nth(i)
            link = (await el.get_attribute("href") or "").strip()
            title = " ".join((await el.inner_text() or "").split())
            if not link or "joonggonara" not in link and "cafe.naver.com" not in link:
                continue
            if not _is_valid_title(title):
                continue
            article_id = _extract_article_id(link)
            if article_id in seen:
                continue
            seen.add(article_id)
            items.append(ListingItem("joonggonara", article_id, title, "가격문의", link, intent.raw_query))
        if items:
            return items
    return items


async def _search_async(intent: SearchIntent) -> list[ListingItem]:
    from playwright.async_api import async_playwright

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        out: list[ListingItem] = []
        try:
            for market in intent.markets:
                if market == "danggeun":
                    out.extend(await _search_danggeun(page, intent))
                elif market == "bunjang":
                    out.extend(await _search_bunjang(page, intent))
                elif market == "joonggonara":
                    out.extend(await _search_joonggonara(page, intent))
        finally:
            await context.close()
            await browser.close()
    deduped: list[ListingItem] = []
    seen_keys: set[str] = set()
    for item in out:
        key = item.article_key()
        if key in seen_keys:
            continue
        seen_keys.add(key)
        if _passes_filters(item, intent):
            deduped.append(item)
    deduped.sort(key=lambda row: (row.market, row.parse_price() or 0))
    return deduped[: intent.limit]


def search_markets(intent: SearchIntent) -> list[ListingItem]:
    return _run_async(lambda: _search_async(intent))
