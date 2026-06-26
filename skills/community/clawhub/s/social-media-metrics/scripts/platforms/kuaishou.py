from __future__ import annotations

import re

from .base import BasePlatform, MetricsResult
from utils.browser import BrowserManager, parse_follower_text, extract_follower_count

_HOMEPAGE_URL = "https://www.kuaishou.com/?isHome=1&source=NewReco"


class KuaishouPlatform(BasePlatform):
    name = "kuaishou"

    _MAX_RETRIES = 3
    _MIN_RETRIES = 2

    async def _click_user_tab(self, page) -> None:
        """Switch to the '用户' (user) tab on the search results page."""
        for selector in (
            'div[class*="tab"] >> text="用户"',
            'a:text-is("用户")',
            'div:text-is("用户")',
            'span:text-is("用户")',
        ):
            try:
                el = page.locator(selector).first
                await el.wait_for(state="visible", timeout=3000)
                await el.click()
                await page.wait_for_timeout(3000)
                return
            except Exception:
                continue

    async def _try_extract_followers(self, page) -> int | None:
        """Attempt to extract follower count from the current page state."""
        follower_el = await page.query_selector(
            'span[class*="fan"] span[class*="count"]'
        )
        count = None
        if follower_el:
            text = (await follower_el.inner_text()).strip()
            count = parse_follower_text(text)

        if count is None:
            all_spans = await page.query_selector_all("span, div")
            for span in all_spans:
                text = (await span.inner_text()).strip()
                if not text or len(text) > 50:
                    continue
                c = extract_follower_count(text)
                if c is not None:
                    count = c
                    break

        if count is None:
            body_text = await page.inner_text("body")
            count = extract_follower_count(body_text)

        return count

    async def fetch_by_url(self, url: str) -> MetricsResult:
        mgr = await BrowserManager.get_instance()
        async with mgr.new_cdp_page() as page:
            try:
                last_error = None
                for attempt in range(1, self._MAX_RETRIES + 1):
                    await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    await page.wait_for_timeout(3000)

                    count = await self._try_extract_followers(page)
                    if count is not None:
                        break

                    if attempt < self._MIN_RETRIES:
                        continue

                    body_text = await page.inner_text("body")
                    if "粉丝" in body_text:
                        continue
                    if attempt >= self._MAX_RETRIES:
                        if "登录" in body_text:
                            last_error = (
                                "Kuaishou profile requires login to view follower data. "
                                "The web version does not expose this without authentication."
                            )
                        else:
                            last_error = "Could not find follower count element"

                if count is None:
                    return self._error_result(
                        last_error or "Could not find follower count element",
                        url=url,
                    )

                name_el = await page.query_selector('h1, span[class*="name"]')
                username = (await name_el.inner_text()).strip() if name_el else None

                return MetricsResult(
                    platform=self.name,
                    username=username,
                    url=url,
                    metrics={"followers": count},
                )
            except Exception as e:
                return self._error_result(f"Browser scraping error: {e}", url=url)

    async def fetch_by_nickname(self, nickname: str) -> MetricsResult:
        search_url = f"https://www.kuaishou.com/search/video?searchKey={nickname}"
        mgr = await BrowserManager.get_instance()
        async with mgr.new_cdp_page() as page:
            try:
                await page.goto(
                    search_url, wait_until="domcontentloaded", timeout=30000
                )
                await page.wait_for_timeout(3000)

                await self._click_user_tab(page)

                card = page.locator(".user-card").first
                try:
                    await card.wait_for(state="visible", timeout=5000)
                except Exception:
                    return self._error_result(
                        f"User '{nickname}' not found on Kuaishou",
                        username=nickname,
                    )

                context = page.context
                async with context.expect_page(timeout=10000) as new_page_info:
                    await card.click()

                profile_page = await new_page_info.value
                try:
                    await profile_page.wait_for_load_state("domcontentloaded")
                    await profile_page.wait_for_timeout(5000)

                    profile_url = profile_page.url
                    count = await self._try_extract_followers(profile_page)
                    if count is None:
                        return self._error_result(
                            "Could not find follower count on profile page",
                            url=profile_url,
                            username=nickname,
                        )

                    name_el = await profile_page.query_selector(
                        'h1, span[class*="name"]'
                    )
                    username = (
                        (await name_el.inner_text()).strip() if name_el else nickname
                    )

                    return MetricsResult(
                        platform=self.name,
                        username=username,
                        url=profile_url,
                        metrics={"followers": count},
                    )
                finally:
                    await profile_page.close()
            except Exception as e:
                return self._error_result(f"Search error: {e}", username=nickname)
