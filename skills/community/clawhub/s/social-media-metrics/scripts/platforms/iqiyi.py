from __future__ import annotations

import re

from .base import BasePlatform, MetricsResult
from utils.browser import BrowserManager, parse_follower_text, extract_follower_count


class IqiyiPlatform(BasePlatform):
    name = "iqiyi"

    async def fetch_by_url(self, url: str) -> MetricsResult:
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(5000)

                count = await self._extract_followers(page)

                if count is None:
                    return self._error_result(
                        "Could not find follower count element", url=url
                    )

                name_el = await page.query_selector(
                    '.user-name, [class*="nickname"], [class*="userName"],'
                    ' [class*="creator-name"], [class*="name"] > span, h1, h2'
                )
                username = None
                if name_el:
                    raw = (await name_el.inner_text()).strip()
                    username = raw.split("\n")[0].strip()

                return MetricsResult(
                    platform=self.name,
                    username=username,
                    url=url,
                    metrics={"followers": count},
                )
            except Exception as e:
                return self._error_result(f"Browser scraping error: {e}", url=url)

    @staticmethod
    async def _extract_followers(page) -> int | None:
        all_elements = await page.query_selector_all("span, div, p, em, a")
        for el in all_elements:
            text = (await el.inner_text()).strip()
            if not text or len(text) > 80:
                continue
            c = extract_follower_count(text, "粉丝")
            if c is not None:
                return c

        body_text = await page.inner_text("body")
        return extract_follower_count(body_text, "粉丝")

    async def fetch_by_nickname(self, nickname: str) -> MetricsResult:
        search_url = f"https://so.iqiyi.com/so/q_{nickname}?source=input&sr=user"
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                await page.goto(
                    search_url, wait_until="domcontentloaded", timeout=30000
                )
                await page.wait_for_timeout(3000)

                user_link = await page.query_selector(
                    'a[href*="/creator/"], a[href*="/u/"]'
                )
                if not user_link:
                    return self._error_result(
                        f"User '{nickname}' not found on iQiyi", username=nickname
                    )

                href = await user_link.get_attribute("href")
                if href and not href.startswith("http"):
                    href = "https://www.iqiyi.com" + href

                if href:
                    result = await self.fetch_by_url(href)
                    result.username = result.username or nickname
                    return result

                return self._error_result(
                    f"Could not resolve profile URL for '{nickname}'",
                    username=nickname,
                )
            except Exception as e:
                return self._error_result(f"Search error: {e}", username=nickname)
