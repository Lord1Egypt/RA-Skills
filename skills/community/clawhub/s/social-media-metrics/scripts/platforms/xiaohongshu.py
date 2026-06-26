from __future__ import annotations

import re
import sys
from urllib.parse import quote

from .base import BasePlatform, MetricsResult
from utils.browser import BrowserManager, parse_follower_text, extract_follower_count

_FANS_WITH_SEP_RE = re.compile(
    r"粉丝[\s·•・:：\-]*(\d[\d,.]*\s*[万亿kKmMbB]?)\+?"
)

_LOGIN_KEYWORDS = ("登录后查看", "登录后推荐")

_LOGIN_TIMEOUT_SECONDS = 120


class XiaohongshuPlatform(BasePlatform):
    name = "xiaohongshu"

    @staticmethod
    def _has_login_wall(body_text: str) -> bool:
        return any(kw in body_text for kw in _LOGIN_KEYWORDS)

    async def _ensure_logged_in(self, page) -> bool:
        """Wait for user to log in via QR code if a login wall is detected.
        Returns True when logged in, False on timeout."""
        body_text = await page.inner_text("body")
        if not self._has_login_wall(body_text):
            return True

        print(
            "\n[xiaohongshu] 需要登录，请在弹出的 Chrome 窗口中扫描二维码登录 "
            f"(等待 {_LOGIN_TIMEOUT_SECONDS} 秒)...",
            file=sys.stderr,
        )

        polls = _LOGIN_TIMEOUT_SECONDS // 2
        for i in range(polls):
            await page.wait_for_timeout(2000)
            body_text = await page.inner_text("body")
            if not self._has_login_wall(body_text):
                print("[xiaohongshu] 登录成功！", file=sys.stderr)
                return True

        print("[xiaohongshu] 登录等待超时", file=sys.stderr)
        return False

    async def fetch_by_url(self, url: str) -> MetricsResult:
        mgr = await BrowserManager.get_instance()
        async with mgr.new_cdp_page() as page:
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(3000)

                if not await self._ensure_logged_in(page):
                    return self._error_result(
                        "Xiaohongshu requires login. Please retry and scan "
                        "the QR code in the Chrome window.",
                        url=url,
                    )

                await page.reload(wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)

                count = None

                fans_selectors = [
                    '.user-info .fans .count',
                    '[class*="fans"] [class*="count"]',
                    '.info-part .count',
                ]
                for sel in fans_selectors:
                    el = await page.query_selector(sel)
                    if el:
                        text = (await el.inner_text()).strip()
                        count = parse_follower_text(text)
                        if count is not None:
                            break

                if count is None:
                    all_els = await page.query_selector_all("span, div, a")
                    for el in all_els:
                        text = (await el.inner_text()).strip()
                        if not text or len(text) > 80:
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
                    '.user-name, [class*="username"], [class*="nickname"]'
                )
                username = (await name_el.inner_text()).strip() if name_el else None

                return MetricsResult(
                    platform=self.name,
                    username=username,
                    url=url,
                    metrics={"followers": count},
                )
            except Exception as e:
                return self._error_result(f"Browser scraping error: {e}", url=url)

    async def _click_user_tab(self, page) -> bool:
        """Switch to the '用户' (Users) tab via dispatchEvent."""
        clicked = await page.evaluate("""() => {
            const el = document.querySelector('#user.channel');
            if (!el) return false;
            el.dispatchEvent(
                new MouseEvent('click', {bubbles: true, cancelable: true})
            );
            return true;
        }""")
        if clicked:
            await page.wait_for_timeout(3000)
        return clicked

    async def _find_first_user_card(self, page):
        """Return the first user-card profile link that is an actual search
        result (skip sidebar navigation links like '我')."""
        links = await page.query_selector_all('a[href*="/user/profile/"]')
        for link in links:
            href = await link.get_attribute("href") or ""
            text = (await link.inner_text()).strip()
            if not text or text == "我":
                continue
            if "channel_type" not in href and len(text) < 5:
                continue
            return link
        return None

    async def fetch_by_nickname(self, nickname: str) -> MetricsResult:
        search_url = (
            "https://www.xiaohongshu.com/search_result"
            f"?keyword={quote(nickname)}&source=web_explore_feed"
        )
        mgr = await BrowserManager.get_instance()
        async with mgr.new_cdp_page() as page:
            try:
                await page.goto(
                    search_url, wait_until="domcontentloaded", timeout=30000
                )
                await page.wait_for_timeout(3000)

                logged_in = await self._ensure_logged_in(page)
                if not logged_in:
                    return self._error_result(
                        "Xiaohongshu requires login. Please retry and scan "
                        "the QR code in the Chrome window.",
                        username=nickname,
                    )

                # 登录成功后重新导航到搜索页
                await page.goto(
                    search_url, wait_until="domcontentloaded", timeout=30000
                )
                await page.wait_for_timeout(3000)

                # 切换到"用户"标签页（dispatchEvent 触发 Vue 路由）
                await self._click_user_tab(page)

                user_link = await self._find_first_user_card(page)
                if not user_link:
                    return self._error_result(
                        f"User '{nickname}' not found on Xiaohongshu",
                        username=nickname,
                    )

                href = await user_link.get_attribute("href")
                if href and not href.startswith("http"):
                    href = "https://www.xiaohongshu.com" + href

                # 用户卡片内含 "粉丝・2.1万"，从卡片文本直接提取粉丝数
                card_text = (await user_link.inner_text()).strip()
                count = None
                m = _FANS_WITH_SEP_RE.search(card_text)
                if m:
                    count = parse_follower_text(m.group(1))
                if count is None:
                    count = extract_follower_count(card_text)

                if count is not None:
                    return MetricsResult(
                        platform=self.name,
                        username=nickname,
                        url=href,
                        metrics={"followers": count},
                    )

                # 搜索结果未提取到粉丝数，跳转到用户主页获取
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
