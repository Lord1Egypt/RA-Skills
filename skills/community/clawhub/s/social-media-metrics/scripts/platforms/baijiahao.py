from __future__ import annotations

import re

from .base import BasePlatform, MetricsResult
from utils.browser import BrowserManager, parse_follower_text, extract_follower_count


class BaijihaoPlatform(BasePlatform):
    name = "baijiahao"

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
                    for kw in ("粉丝", "关注"):
                        c = extract_follower_count(text, kw)
                        if c is not None:
                            count = c
                            break
                    if count is not None:
                        break

                if count is None:
                    body_text = await page.inner_text("body")
                    count = extract_follower_count(body_text)

                if count is None:
                    return self._error_result(
                        "Could not find follower count element", url=url
                    )

                name_el = await page.query_selector(
                    '.author-name, [class*="name"], h1'
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
        search_url = f"https://www.baidu.com/s?wd={nickname}+百家号"
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                await page.goto(
                    search_url, wait_until="domcontentloaded", timeout=30000
                )
                await page.wait_for_timeout(3000)

                bjh_link = await page.query_selector(
                    'a[href*="baijiahao.baidu.com"], a[href*="author.baidu.com"]'
                )
                if not bjh_link:
                    return self._error_result(
                        f"User '{nickname}' not found on Baijiahao", username=nickname
                    )

                href = await bjh_link.get_attribute("href")
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
