from __future__ import annotations

import re

from .base import BasePlatform, MetricsResult
from utils.browser import BrowserManager, parse_follower_text


class InstagramPlatform(BasePlatform):
    name = "instagram"

    async def _dismiss_login_popup(self, page) -> None:
        """Close the Instagram login/signup popup if it appears."""
        close_selectors = [
            'div[role="dialog"] button svg[aria-label="Close"]',
            'div[role="dialog"] button svg[aria-label="关闭"]',
            'div[role="dialog"] div[role="button"]:has(svg)',
        ]
        for sel in close_selectors:
            btn = await page.query_selector(sel)
            if btn:
                await btn.click()
                await page.wait_for_timeout(1000)
                return
        # Last resort: press Escape to dismiss any overlay
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(1000)

    async def fetch_by_url(self, url: str) -> MetricsResult:
        mgr = await BrowserManager.get_instance()
        async with mgr.new_page() as page:
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(3000)

                # Instagram often requires login; try meta tags first
                meta_el = await page.query_selector(
                    'meta[property="og:description"]'
                )
                if meta_el:
                    content = await meta_el.get_attribute("content") or ""
                    # e.g. "12.3M Followers, 100 Following, 500 Posts ..."
                    m = re.match(
                        r"([\d,.]+[kKmMbB]?)\s*Followers", content
                    )
                    if m:
                        count = parse_follower_text(m.group(1))
                        title_el = await page.query_selector(
                            'meta[property="og:title"]'
                        )
                        username = None
                        if title_el:
                            title = await title_el.get_attribute("content") or ""
                            # "Name (@handle) • Instagram photos and videos"
                            name_m = re.match(r"(.+?)\s*\(", title)
                            username = name_m.group(1).strip() if name_m else title.split("•")[0].strip()

                        handle = self._extract_handle(url)
                        return MetricsResult(
                            platform=self.name,
                            username=username,
                            uid=handle,
                            url=url,
                            metrics={"followers": count},
                        )

                # Dismiss login popup before reading DOM
                await self._dismiss_login_popup(page)
                await page.wait_for_timeout(1000)

                # Try DOM selectors for follower count
                follower_el = await page.query_selector(
                    'a[href*="/followers/"] span, '
                    'li:has(a[href*="/followers/"]) span'
                )
                if follower_el:
                    text = (await follower_el.inner_text()).strip()
                    count = parse_follower_text(text)
                    if count is not None:
                        return MetricsResult(
                            platform=self.name,
                            uid=self._extract_handle(url),
                            url=url,
                            metrics={"followers": count},
                        )

                # Fallback: scan header section text for follower patterns
                # e.g. "1115帖子 2174粉丝 307关注" or "2,174 followers"
                header = await page.query_selector("header section, header")
                if header:
                    header_text = (await header.inner_text()).strip()
                    count = self._parse_followers_from_text(header_text)
                    if count is not None:
                        return MetricsResult(
                            platform=self.name,
                            uid=self._extract_handle(url),
                            url=url,
                            metrics={"followers": count},
                        )

                return self._error_result(
                    "Could not find follower count. "
                    "Instagram may require login for this profile.",
                    url=url,
                )
            except Exception as e:
                return self._error_result(f"Browser scraping error: {e}", url=url)

    @staticmethod
    def _parse_followers_from_text(text: str) -> int | None:
        """Extract follower count from visible profile header text."""
        # Chinese: "2174粉丝" or "2,174粉丝"
        m = re.search(r"([\d,.]+[kKmMbB万亿]?)\s*粉丝", text)
        if m:
            return parse_follower_text(m.group(1))
        # English: "2,174 followers"
        m = re.search(r"([\d,.]+[kKmMbB]?)\s*followers", text, re.IGNORECASE)
        if m:
            return parse_follower_text(m.group(1))
        return None

    async def fetch_by_nickname(self, nickname: str) -> MetricsResult:
        handle = nickname.lstrip("@")
        url = f"https://www.instagram.com/{handle}/"
        result = await self.fetch_by_url(url)
        result.username = result.username or nickname
        return result

    @staticmethod
    def _extract_handle(url: str) -> str | None:
        m = re.search(r"instagram\.com/([^/?&]+)", url)
        return m.group(1) if m else None
