from __future__ import annotations

from .base import BasePlatform, MetricsResult
from utils.browser import BrowserManager, extract_follower_count


class HaokanPlatform(BasePlatform):
    name = "haokan"

    HOMEPAGE = "https://haokan.baidu.com/"

    async def fetch_by_url(self, url: str) -> MetricsResult:
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                # Visit homepage first to establish cookies and bypass CAPTCHA
                await page.goto(
                    self.HOMEPAGE, wait_until="domcontentloaded", timeout=30000
                )
                await page.wait_for_timeout(2000)

                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(3000)

                count = None
                body_text = await page.inner_text("body")
                count = extract_follower_count(body_text)

                if count is None:
                    return self._error_result(
                        "Could not find follower count element", url=url
                    )

                name_el = await page.query_selector(
                    '.userinfo-authorname, .author-name, [class*="username"], h1'
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
        search_url = f"https://haokan.baidu.com/haokan/wiseauthor?query={nickname}"
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                await page.goto(
                    search_url, wait_until="domcontentloaded", timeout=30000
                )
                await page.wait_for_timeout(3000)

                author_link = await page.query_selector(
                    'a[href*="haokan.baidu.com/author"]'
                )
                if not author_link:
                    return self._error_result(
                        f"User '{nickname}' not found on Haokan Video",
                        username=nickname,
                    )

                href = await author_link.get_attribute("href")
                if href:
                    if not href.startswith("http"):
                        href = "https:" + href
                    result = await self.fetch_by_url(href)
                    result.username = result.username or nickname
                    return result

                return self._error_result(
                    f"Could not resolve profile URL for '{nickname}'",
                    username=nickname,
                )
            except Exception as e:
                return self._error_result(f"Search error: {e}", username=nickname)
