from __future__ import annotations

import re
from urllib.parse import quote

from .base import BasePlatform, MetricsResult
from utils.browser import BrowserManager, parse_follower_text, extract_follower_count


class TikTokPlatform(BasePlatform):
    name = "tiktok"

    async def fetch_by_url(self, url: str) -> MetricsResult:
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(3000)

                follower_el = await page.query_selector(
                    '[data-e2e="followers-count"]'
                )
                if not follower_el:
                    follower_el = await page.query_selector(
                        'strong[title*="Follower"], strong[data-e2e="followers-count"]'
                    )

                if not follower_el:
                    return self._error_result(
                        "Could not find follower count element", url=url
                    )

                text = (await follower_el.inner_text()).strip()
                count = parse_follower_text(text)

                name_el = await page.query_selector(
                    'h1[data-e2e="user-title"], h2[data-e2e="user-subtitle"]'
                )
                username = (await name_el.inner_text()).strip() if name_el else None

                handle = self._extract_handle(url)

                return MetricsResult(
                    platform=self.name,
                    username=username,
                    uid=handle,
                    url=url,
                    metrics={"followers": count},
                )
            except Exception as e:
                return self._error_result(f"Browser scraping error: {e}", url=url)

    async def fetch_by_nickname(self, nickname: str) -> MetricsResult:
        handle = nickname if nickname.startswith("@") else f"@{nickname}"
        url = f"https://www.tiktok.com/{handle}"
        result = await self.fetch_by_url(url)
        if result.success:
            result.username = result.username or nickname
            return result

        search_result = await self._fetch_by_search(nickname)
        search_result.username = search_result.username or nickname
        return search_result

    async def _fetch_by_search(self, nickname: str) -> MetricsResult:
        """Fallback: use TikTok search page to locate user profile and metrics."""
        search_url = f"https://www.tiktok.com/search/user?q={quote(nickname)}"
        mgr = await BrowserManager.get_instance()

        profile_url = None
        search_count = None

        async with mgr.new_page() as page:
            try:
                await page.goto(
                    search_url, wait_until="domcontentloaded", timeout=30000
                )
                await page.wait_for_timeout(5000)

                profile_url, search_count = await self._find_user_in_search(
                    page, nickname
                )
            except Exception as e:
                return self._error_result(f"Search error: {e}", username=nickname)

        if profile_url:
            if not profile_url.startswith("http"):
                profile_url = "https://www.tiktok.com" + profile_url
            result = await self.fetch_by_url(profile_url)
            if result.success:
                return result

        if search_count is not None:
            return MetricsResult(
                platform=self.name,
                username=nickname,
                url=profile_url or search_url,
                uid=self._extract_handle(profile_url) if profile_url else None,
                metrics={"followers": search_count},
            )

        return self._error_result(
            f"User '{nickname}' not found on TikTok", username=nickname
        )

    async def _find_user_in_search(
        self, page, nickname: str
    ) -> tuple[str | None, int | None]:
        """Find user profile link and follower count from search results.

        Returns (profile_url, follower_count). Prefers the card whose text
        contains *nickname* so we skip unrelated video-creator links.
        """
        links = await page.query_selector_all('a[href*="/@"]')
        for link in links:
            href = await link.get_attribute("href") or ""
            if not re.search(r"/@[\w.]+$", href) or not await link.is_visible():
                continue
            try:
                text = await link.inner_text()
            except Exception:
                continue
            if nickname not in text:
                continue
            count = self._parse_follower_from_card(text)
            return href, count

        # No card matching nickname — try the first valid profile link
        for link in links:
            href = await link.get_attribute("href") or ""
            if not re.search(r"/@[\w.]+$", href) or not await link.is_visible():
                continue
            return href, None

        return None, None

    @staticmethod
    def _parse_follower_from_card(text: str) -> int | None:
        """Parse follower count from a TikTok user card text.

        Handles formats like '149\\n粉丝', '2.1万\\n粉丝', '149 Followers'.
        """
        m = re.search(
            r"([\d,.]+\s*[万亿kKmMbB]?)\s*(?:粉丝|[Ff]ollowers?)", text
        )
        if m:
            return parse_follower_text(m.group(1).strip())
        return None

    @staticmethod
    def _extract_handle(url: str) -> str | None:
        if not url:
            return None
        m = re.search(r"tiktok\.com/@([^/?&]+)", url)
        return m.group(1) if m else None
