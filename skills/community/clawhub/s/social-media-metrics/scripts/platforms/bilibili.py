from __future__ import annotations

import re

import requests

from .base import BasePlatform, MetricsResult

API_STAT_URL = "https://api.bilibili.com/x/relation/stat"
API_USER_URL = "https://api.bilibili.com/x/space/acc/info"
SEARCH_URL = "https://api.bilibili.com/x/web-interface/search/type"


class BilibiliPlatform(BasePlatform):
    name = "bilibili"

    async def fetch_by_url(self, url: str) -> MetricsResult:
        uid = self._extract_uid(url)
        if not uid:
            return self._error_result(f"Cannot extract UID from URL: {url}", url=url)
        return await self._fetch_by_uid(uid, url)

    async def fetch_by_nickname(self, nickname: str) -> MetricsResult:
        uid = self._search_user(nickname)
        if not uid:
            return self._error_result(
                f"User '{nickname}' not found on Bilibili",
                username=nickname,
            )
        url = f"https://space.bilibili.com/{uid}"
        result = await self._fetch_by_uid(uid, url)
        result.username = nickname
        return result

    async def _fetch_by_uid(self, uid: str, url: str) -> MetricsResult:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com",
        }

        try:
            stat_resp = requests.get(
                API_STAT_URL, params={"vmid": uid}, headers=headers, timeout=10
            )
            stat_data = stat_resp.json()
            if stat_data.get("code") != 0:
                return self._error_result(
                    f"Bilibili API error: {stat_data.get('message', 'unknown')}",
                    uid=uid,
                    url=url,
                )
            followers = stat_data["data"]["follower"]
        except Exception as e:
            return self._error_result(f"Failed to fetch stats: {e}", uid=uid, url=url)

        username = None
        try:
            user_resp = requests.get(
                API_USER_URL, params={"mid": uid}, headers=headers, timeout=10
            )
            user_data = user_resp.json()
            if user_data.get("code") == 0:
                username = user_data["data"].get("name")
        except Exception:
            pass

        if not username:
            try:
                search_resp = requests.get(
                    SEARCH_URL,
                    params={"search_type": "bili_user", "keyword": uid},
                    headers=headers,
                    timeout=10,
                )
                search_data = search_resp.json()
                if search_data.get("code") == 0 and search_data["data"].get("result"):
                    for item in search_data["data"]["result"]:
                        if str(item["mid"]) == uid:
                            username = item["uname"]
                            break
            except Exception:
                pass

        return MetricsResult(
            platform=self.name,
            username=username,
            uid=uid,
            url=url,
            metrics={"followers": followers},
        )

    def _search_user(self, nickname: str) -> str | None:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://www.bilibili.com",
        }
        try:
            resp = requests.get(
                SEARCH_URL,
                params={"search_type": "bili_user", "keyword": nickname},
                headers=headers,
                timeout=10,
            )
            data = resp.json()
            if data.get("code") == 0 and data["data"].get("result"):
                return str(data["data"]["result"][0]["mid"])
        except Exception:
            pass
        return None

    @staticmethod
    def _extract_uid(url: str) -> str | None:
        m = re.search(r"bilibili\.com/(?:space/)?(\d+)", url)
        return m.group(1) if m else None
