from __future__ import annotations

import json
import os
import re
from urllib.parse import quote

import requests
from playwright.async_api import Page

from .base import BasePlatform, MetricsResult
from utils.browser import BrowserManager, parse_follower_text

YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"

_CONSENT_BUTTON_SELECTORS = (
    'button[aria-label*="Accept"]',
    'button[aria-label*="Reject"]',
    'tp-yt-paper-button[aria-label*="Accept"]',
    'button:has-text("Accept all")',
    'button:has-text("Reject all")',
    'button:has-text("同意")',
)


class YouTubePlatform(BasePlatform):
    name = "youtube"

    def __init__(self) -> None:
        self.api_key = os.environ.get("YOUTUBE_API_KEY")

    async def fetch_by_url(self, url: str) -> MetricsResult:
        handle_or_id = self._extract_identifier(url)
        if not handle_or_id:
            return self._error_result(f"Cannot parse YouTube URL: {url}", url=url)

        if self.api_key:
            result = await self._fetch_via_api(handle_or_id, url)
            if result.success:
                return result

        return await self._fetch_via_browser(url)

    async def fetch_by_nickname(self, nickname: str) -> MetricsResult:
        handle = nickname if nickname.startswith("@") else f"@{nickname}"
        url = f"https://www.youtube.com/{handle}"

        if self.api_key:
            result = await self._fetch_via_api(handle, url)
            if result.success:
                return result

        result = await self._fetch_via_browser(url)
        if result.success:
            return result

        return await self._search_and_fetch(nickname)

    async def _fetch_via_api(self, identifier: str, url: str) -> MetricsResult:
        try:
            if identifier.startswith("@"):
                params = {"part": "snippet,statistics", "forHandle": identifier, "key": self.api_key}
            elif identifier.startswith("UC"):
                params = {"part": "snippet,statistics", "id": identifier, "key": self.api_key}
            else:
                params = {"part": "snippet,statistics", "forHandle": f"@{identifier}", "key": self.api_key}

            resp = requests.get(
                f"{YOUTUBE_API_BASE}/channels", params=params, timeout=10
            )
            data = resp.json()

            if "items" not in data or not data["items"]:
                return self._error_result("Channel not found via API", url=url)

            channel = data["items"][0]
            stats = channel["statistics"]
            snippet = channel["snippet"]

            return MetricsResult(
                platform=self.name,
                username=snippet.get("title"),
                uid=channel["id"],
                url=url,
                metrics={
                    "followers": int(stats.get("subscriberCount", 0)),
                    "total_views": int(stats.get("viewCount", 0)),
                    "video_count": int(stats.get("videoCount", 0)),
                },
            )
        except Exception as e:
            return self._error_result(f"YouTube API error: {e}", url=url)

    @staticmethod
    async def _dismiss_consent(page: Page) -> None:
        for btn_sel in _CONSENT_BUTTON_SELECTORS:
            btn = await page.query_selector(btn_sel)
            if btn:
                await btn.click()
                await page.wait_for_timeout(1000)
                break

    async def _fetch_via_browser(self, url: str) -> MetricsResult:
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await self._dismiss_consent(page)
                await page.wait_for_timeout(2000)

                count = None
                username = None

                # Strategy 1: extract from ytInitialData JS variable (most reliable,
                # works even when DOM hasn't finished rendering the SPA)
                count, username = await self._extract_from_yt_initial_data(page)

                # Strategy 2: DOM selectors (multiple variations)
                if count is None:
                    await page.wait_for_timeout(3000)
                    subscriber_selectors = [
                        "#subscriber-count",
                        "yt-formatted-string#subscriber-count",
                        "#channel-header yt-formatted-string#subscriber-count",
                        'yt-content-metadata-view-model span[role="text"]',
                        "ytd-c4-tabbed-header-renderer .yt-core-attributed-string--link-inherit-color",
                    ]
                    for sel in subscriber_selectors:
                        try:
                            await page.wait_for_selector(sel, timeout=3000)
                        except Exception:
                            continue
                        el = await page.query_selector(sel)
                        if el:
                            text = (await el.inner_text()).strip()
                            if text and any(c.isdigit() for c in text):
                                num_part = text.split(" ")[0] if " " in text else text
                                num_part = re.sub(r"[^\d.,kKmMbB万亿]", "", num_part)
                                count = parse_follower_text(num_part)
                                if count is not None:
                                    break

                # Strategy 3: scan visible text for subscriber pattern
                if count is None:
                    body_text = await page.inner_text("body")
                    m = re.search(
                        r"([\d,.]+\s*[KkMmBb万亿]?)\s*(?:subscribers?|位订阅者|订阅者)",
                        body_text,
                    )
                    if m:
                        raw = re.sub(r"[^\d.,kKmMbB万亿]", "", m.group(1))
                        count = parse_follower_text(raw)

                if count is None:
                    return self._error_result(
                        "Could not find subscriber count element", url=url
                    )

                # Get channel name from DOM if ytInitialData didn't provide it
                if not username:
                    title_selectors = [
                        "yt-formatted-string.ytd-channel-name",
                        "#channel-name yt-formatted-string",
                        "#text.ytd-channel-name",
                        "ytd-channel-name yt-formatted-string#text",
                    ]
                    for sel in title_selectors:
                        el = await page.query_selector(sel)
                        if el:
                            username = (await el.inner_text()).strip()
                            if username:
                                break

                return MetricsResult(
                    platform=self.name,
                    username=username,
                    url=url,
                    metrics={"followers": count},
                )
            except Exception as e:
                return self._error_result(f"Browser scraping error: {e}", url=url)

    @staticmethod
    async def _extract_from_yt_initial_data(page: Page) -> tuple[int | None, str | None]:
        """Extract subscriber count and channel title from YouTube's embedded ytInitialData."""
        try:
            yt_data = await page.evaluate("window.ytInitialData")
        except Exception:
            return None, None

        if not isinstance(yt_data, dict):
            return None, None

        header = yt_data.get("header", {})
        count = None
        username = None

        # Layout A: c4TabbedHeaderRenderer (classic)
        c4 = header.get("c4TabbedHeaderRenderer", {})
        if c4:
            sub_text = c4.get("subscriberCountText", {}).get("simpleText", "")
            if sub_text:
                m = re.search(r"([\d,.]+\s*[KkMmBb万亿]?)", sub_text)
                if m:
                    count = parse_follower_text(
                        re.sub(r"[^\d.,kKmMbB万亿]", "", m.group(1))
                    )
            username = c4.get("title", "") or None

        # Layout B: pageHeaderRenderer (new layout)
        if count is None:
            ph = header.get("pageHeaderRenderer", {}).get("content", {}).get(
                "pageHeaderViewModel", {}
            )
            metadata = ph.get("metadata", {}).get("contentMetadataViewModel", {})
            for row in metadata.get("metadataRows", []):
                for part in row.get("metadataParts", []):
                    text = part.get("text", {}).get("content", "")
                    if re.search(r"subscri|订阅", text, re.IGNORECASE):
                        m = re.search(r"([\d,.]+\s*[KkMmBb万亿]?)", text)
                        if m:
                            count = parse_follower_text(
                                re.sub(r"[^\d.,kKmMbB万亿]", "", m.group(1))
                            )
                            break
                if count is not None:
                    break
            if not username:
                title_obj = ph.get("title", {})
                username = (
                    title_obj.get("dynamicTextViewModel", {})
                    .get("text", {})
                    .get("content")
                ) or title_obj.get("content") or None

        return count, username

    async def _search_and_fetch(self, query: str) -> MetricsResult:
        """Fallback: search YouTube for the query and scrape the first channel result."""
        search_url = f"https://www.youtube.com/results?search_query={quote(query)}"
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                await self._dismiss_consent(page)
                await page.wait_for_timeout(3000)

                channel_url = await self._find_first_channel_link(page)
                if not channel_url:
                    return self._error_result(
                        f"No channel found in YouTube search for: {query}",
                        url=search_url,
                    )
            except Exception as e:
                return self._error_result(f"YouTube search error: {e}", url=search_url)

        return await self._fetch_via_browser(channel_url)

    @staticmethod
    async def _find_first_channel_link(page: Page) -> str | None:
        """Extract the first channel URL from a YouTube search results page."""
        selectors = [
            "ytd-channel-renderer a#main-link",
            "ytd-channel-renderer a#avatar-section",
            "ytd-channel-renderer a.channel-link",
        ]
        for sel in selectors:
            el = await page.query_selector(sel)
            if el:
                href = await el.get_attribute("href")
                if href:
                    if href.startswith("/"):
                        return f"https://www.youtube.com{href}"
                    return href

        all_links = await page.query_selector_all("a[href]")
        for link in all_links:
            href = await link.get_attribute("href") or ""
            if re.search(r"youtube\.com/@[^/]+$", href) or re.match(r"^/@[^/]+$", href):
                parent = await link.evaluate(
                    "el => el.closest('ytd-video-renderer, ytd-channel-renderer, ytd-search-pyve-renderer')"
                )
                if parent is not None:
                    if href.startswith("/"):
                        return f"https://www.youtube.com{href}"
                    return href

        # Last resort: any /@handle link found on the page (first occurrence)
        all_links = await page.query_selector_all('a[href*="/@"]')
        for link in all_links:
            href = await link.get_attribute("href") or ""
            if "/@" in href:
                if href.startswith("/"):
                    return f"https://www.youtube.com{href}"
                return href

        return None

    @staticmethod
    def _extract_identifier(url: str) -> str | None:
        m = re.search(r"youtube\.com/(?:@|channel/|c/)([^/?&]+)", url)
        return m.group(1) if m else None
