"""
XHS Expert - API客户端核心
签名算法、Cookie管理、统一请求封装
"""

import asyncio
import hashlib
import json
import random
import time
from pathlib import Path
from typing import Dict, Any, Optional

import httpx


XHS_API_BASE = "https://edith.xiaohongshu.com"
XHS_SEARCH_BASE = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
XHS_WEB_BASE = "https://www.xiaohongshu.com"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


class SignType:
    SEARCH = "search"
    FEED = "feed"
    USER = "user"
    INTERACT = "interact"


class XHSClientConfig:
    def __init__(
        self,
        cookies_path: Optional[Path] = None,
        device_id: str = "",
        a1: str = "",
        web_session: str = ""
    ):
        self.cookies_path = cookies_path or (
            Path.home() / ".config" / "xiaohongshu" / "cookies.json"
        )
        self.cookies_path.parent.mkdir(parents=True, exist_ok=True)
        self.device_id = device_id
        self.a1 = a1
        self.web_session = web_session


class XHSClient:
    """
    小红书API客户端

    核心功能：
    - 自动签名（简化版，生产环境需逆向完整签名算法）
    - Cookie持久化
    - 请求重试
    """

    def __init__(self, config: Optional[XHSClientConfig] = None):
        self.config = config or XHSClientConfig()
        self.client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        self._cookies: Dict[str, str] = {}
        self._headers = self._build_headers()

    def _build_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Origin": XHS_WEB_BASE,
            "Referer": XHS_WEB_BASE,
            "X-s": "",
            "X-t": "",
            "X-b": "",
            "Content-Type": "application/json;charset=UTF-8"
        }

    async def load_cookies(self) -> bool:
        """从文件加载Cookie"""
        if not self.config.cookies_path.exists():
            return False

        try:
            with open(self.config.cookies_path, "r", encoding="utf-8") as f:
                cookies_data = json.load(f)

            self._cookies = cookies_data.get("cookies", {})
            self._headers["X-s"] = cookies_data.get("x_s", "")
            self._headers["X-t"] = cookies_data.get("x_t", "")
            self.config.device_id = cookies_data.get("device_id", "")
            self.config.a1 = cookies_data.get("a1", "")

            return True
        except Exception:
            return False

    async def save_cookies(self):
        """保存Cookie到文件"""
        cookies_data = {
            "cookies": self._cookies,
            "x_s": self._headers.get("X-s", ""),
            "x_t": self._headers.get("X-t", ""),
            "device_id": self.config.device_id,
            "a1": self.config.a1,
            "updated_at": time.time()
        }

        with open(self.config.cookies_path, "w", encoding="utf-8") as f:
            json.dump(cookies_data, f, ensure_ascii=False, indent=2)

    def set_cookies(self, cookies: Dict[str, str]):
        """直接设置Cookie"""
        self._cookies.update(cookies)

    def _generate_sign(self, url: str, body: str, sign_type: str) -> Dict[str, str]:
        """
        生成签名（简化版）

        完整签名算法需要逆向小红书JS，简化版适用于部分场景。
        生产环境建议使用浏览器注入或Selenium获取真实签名。
        """
        timestamp = str(int(time.time() * 1000))
        random_str = "".join(
            random.choices(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
                k=32
            )
        )

        sign_factor = f"{url}{body}{timestamp}{random_str}"
        sign = hashlib.sha256(sign_factor.encode()).hexdigest()

        self._headers["X-s"] = sign
        self._headers["X-t"] = timestamp
        self._headers["X-b"] = random_str[:16]

        return {"X-s": sign, "X-t": timestamp, "X-b": random_str[:16]}

    async def request(
        self,
        method: str,
        url: str,
        data: Optional[Dict] = None,
        sign_type: str = SignType.FEED,
        retry: int = 3
    ) -> Dict[str, Any]:
        """统一请求方法"""
        body = json.dumps(data) if data else ""

        for attempt in range(retry):
            try:
                self._generate_sign(url, body, sign_type)

                headers = self._headers.copy()
                if self._cookies:
                    headers["Cookie"] = "; ".join(f"{k}={v}" for k, v in self._cookies.items())

                if method.upper() == "GET":
                    response = await self.client.get(url, headers=headers)
                else:
                    response = await self.client.post(url, headers=headers, content=body)

                result = response.json()

                if result.get("success") or result.get("code") == 0:
                    return result.get("data", result)

                if result.get("code") == 400007:
                    raise Exception("登录态失效，请重新登录")

                raise Exception(f"API错误: {result}")

            except Exception as e:
                if attempt == retry - 1:
                    raise
                await asyncio.sleep(2 ** attempt)

    async def search_notes(
        self,
        keyword: str,
        page: int = 1,
        page_size: int = 20,
        sort: str = "general"
    ) -> Dict[str, Any]:
        """搜索笔记"""
        url = XHS_SEARCH_BASE
        data = {
            "keyword": keyword,
            "page": page,
            "page_size": page_size,
            "sort": sort,
            "note_type": 0,
            "ext_flags": [],
            "image_formats": ["jpg", "webp", "avif"]
        }

        return await self.request("POST", url, data, SignType.SEARCH)

    async def get_note_detail(
        self,
        note_id: str,
        xsec_source: str = "",
        xsec_token: str = ""
    ) -> Dict[str, Any]:
        """获取笔记详情"""
        url = f"{XHS_API_BASE}/api/sns/web/v1/feed"
        data = {
            "source_note_id": note_id,
            "image_formats": ["jpg", "webp", "avif"],
            "extra": {"need_body_topic": "1"},
            "xsec_source": xsec_source,
            "xsec_token": xsec_token
        }

        return await self.request("POST", url, data, SignType.FEED)

    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """获取用户信息"""
        url = f"{XHS_API_BASE}/api/sns/web/v1/user/info"
        data = {"target_user_id": user_id}

        return await self.request("POST", url, data, SignType.USER)

    async def like_note(self, note_id: str, action: str = "add") -> Dict[str, Any]:
        """点赞笔记"""
        url = f"{XHS_API_BASE}/api/sns/web/v1/interact/like"
        data = {
            "target_id": note_id,
            "action": action,
            "type": "note"
        }

        return await self.request("POST", url, data, SignType.INTERACT)

    async def collect_note(
        self,
        note_id: str,
        collect_id: str = "",
        action: str = "add"
    ) -> Dict[str, Any]:
        """收藏笔记"""
        url = f"{XHS_API_BASE}/api/sns/web/v1/interact/collect"
        data = {
            "target_id": note_id,
            "collect_id": collect_id,
            "action": action
        }

        return await self.request("POST", url, data, SignType.INTERACT)

    async def post_comment(
        self,
        note_id: str,
        content: str,
        target_comment_id: str = ""
    ) -> Dict[str, Any]:
        """发表评论"""
        url = f"{XHS_API_BASE}/api/sns/web/v2/comment/add"
        data = {
            "note_id": note_id,
            "content": content,
            "target_comment_id": target_comment_id,
            "at_users": []
        }

        return await self.request("POST", url, data, SignType.INTERACT)

    async def follow_user(self, user_id: str, action: str = "add") -> Dict[str, Any]:
        """关注用户"""
        url = f"{XHS_API_BASE}/api/sns/web/v1/user/follow"
        data = {
            "target_user_id": user_id,
            "action": action
        }

        return await self.request("POST", url, data, SignType.INTERACT)

    async def get_comments(
        self,
        note_id: str,
        cursor: str = "",
        top_comment_id: str = "",
        count: int = 50
    ) -> Dict[str, Any]:
        """获取评论"""
        url = f"{XHS_API_BASE}/api/sns/web/v2/comment/page"
        data = {
            "note_id": note_id,
            "cursor": cursor,
            "top_comment_id": top_comment_id,
            "count": count
        }

        return await self.request("POST", url, data, SignType.FEED)

    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
