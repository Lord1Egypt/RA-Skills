from __future__ import annotations

import re

from .base import BasePlatform, MetricsResult
from utils.browser import BrowserManager, parse_follower_text, extract_follower_count


class WechatVideoPlatform(BasePlatform):
    name = "wechat_video"

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

                if count is not None:
                    name_el = await page.query_selector(
                        'h1, h2, [class*="nickname"], [class*="name"]'
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

                return self._error_result(
                    "Could not find follower count element. "
                    "WeChat Video (视频号) profiles may require login.",
                    url=url,
                )
            except Exception as e:
                return self._error_result(f"Browser scraping error: {e}", url=url)

    async def fetch_by_nickname(self, nickname: str) -> MetricsResult:
        return self._error_result(
            "WeChat Video (视频号) does not support search by nickname via web. "
            "Please provide a direct profile URL from channels.weixin.qq.com.",
            username=nickname,
        )
