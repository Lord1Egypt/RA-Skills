from __future__ import annotations

import re
from urllib.parse import quote

from .base import BasePlatform, MetricsResult
from utils.browser import BrowserManager, parse_follower_text, extract_follower_count

_USER_LINK_SELECTORS = [
    'a[href*="/c/user/token/"]',
    'a[href*="/c/user/"]',
    'a[href*="toutiao.com"][href*="user"]',
]


class ToutiaoPlatform(BasePlatform):
    name = "toutiao"

    async def fetch_by_url(self, url: str) -> MetricsResult:
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(3000)

                count = None
                all_elements = await page.query_selector_all("span, div, p")
                for el in all_elements:
                    text = (await el.inner_text()).strip()
                    if not text or len(text) > 50:
                        continue
                    c = extract_follower_count(text)
                    if c is not None:
                        count = c
                        break

                if count is None:
                    body_text = await page.inner_text("body")
                    count = extract_follower_count(body_text)

                if count is None:
                    return self._error_result(
                        "Could not find follower count element", url=url
                    )

                name_el = await page.query_selector(
                    '.user-name, [class*="name"] span, h1'
                )
                username = (
                    (await name_el.inner_text()).strip() if name_el else None
                )

                return MetricsResult(
                    platform=self.name,
                    username=username,
                    url=url,
                    metrics={"followers": count},
                )
            except Exception as e:
                return self._error_result(f"Browser scraping error: {e}", url=url)

    async def fetch_by_nickname(self, nickname: str) -> MetricsResult:
        search_url = (
            "https://so.toutiao.com/search"
            f"?dvpf=pc&keyword={quote(nickname)}"
            "&source=search_subtab_switch&pd=user"
            "&action_type=search_subtab_switch"
            "&page_num=0&from=media&cur_tab_title=media"
        )
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                await page.goto(
                    search_url, wait_until="domcontentloaded", timeout=30000
                )
                await page.wait_for_timeout(3000)

                user_link = None
                for selector in _USER_LINK_SELECTORS:
                    user_link = await page.query_selector(selector)
                    if user_link:
                        break

                if not user_link:
                    user_link = await self._find_user_link_by_click(page)

                if not user_link:
                    return self._error_result(
                        f"User '{nickname}' not found on Toutiao", username=nickname
                    )

                href = await user_link.get_attribute("href")
                if href and not href.startswith("http"):
                    href = "https://www.toutiao.com" + href

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

    @staticmethod
    async def _find_user_link_by_click(page) -> object | None:
        """Fallback: locate the first clickable user card element."""
        for selector in (
            '[class*="user"] a[href]',
            '.search-card a[href]',
            '[class*="result"] a[href*="user"]',
            '[class*="card"] a[href]',
        ):
            el = await page.query_selector(selector)
            if el:
                href = await el.get_attribute("href")
                if href and "user" in href:
                    return el
        return None
