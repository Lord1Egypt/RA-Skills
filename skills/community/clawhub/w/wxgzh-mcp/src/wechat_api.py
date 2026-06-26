"""WeChat Official Account API wrapper."""
import time
import requests
from typing import Optional, Dict, Any, List


class WeChatAPIError(Exception):
    """WeChat API error."""

    def __init__(self, message: str, code: int, raw: Dict = None):
        super().__init__(message)
        self.code = code
        self.raw = raw or {}


class WeChatAPI:
    """WeChat Official Account API client.

    Supports:
    - Access token management (auto-cached)
    - Image/thumb upload
    - Draft management
    - Material listing
    """

    BASE_URL = "https://api.weixin.qq.com/cgi-bin"

    def __init__(self, app_id: str = None, app_secret: str = None, proxy: str = None):
        """Initialize WeChat API client.

        Args:
            app_id: WeChat Official Account AppID
            app_secret: WeChat Official Account AppSecret
            proxy: HTTP proxy URL (optional)
        """
        from .config import get_config

        cfg = get_config()
        self.app_id = app_id or cfg.app_id
        self.app_secret = app_secret or cfg.app_secret
        self.proxy = proxy or cfg.proxy
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0

    def _get_proxies(self) -> Optional[Dict[str, str]]:
        """Get HTTP proxies dict."""
        if self.proxy:
            return {"http": self.proxy, "https": self.proxy}
        return None

    def _request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        json_data: Dict = None,
        data=None,
        timeout: int = 30,
    ) -> Dict[str, Any]:
        """Make HTTP request to WeChat API."""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        proxies = self._get_proxies()

        # Build headers
        headers = {"Content-Type": "application/json; charset=utf-8"}

        # If data is already encoded, use it directly
        if data is not None:
            resp = requests.request(
                method=method,
                url=url,
                params=params,
                data=data,
                proxies=proxies,
                timeout=timeout,
                headers=headers,
            )
        else:
            resp = requests.request(
                method=method,
                url=url,
                params=params,
                json=json_data,
                proxies=proxies,
                timeout=timeout,
                headers=headers,
            )

        resp.raise_for_status()

        # Handle both JSON and non-JSON responses
        content_type = resp.headers.get("Content-Type", "")
        if "application/json" in content_type:
            result = resp.json()
        else:
            result = {"raw": resp.text}

        # Check for WeChat API errors
        if isinstance(result, dict) and result.get("errcode") and result["errcode"] != 0:
            raise WeChatAPIError(
                result.get("errmsg", "Unknown error"),
                result["errcode"],
                result,
            )

        return result

    def get_access_token(self, force_refresh: bool = False) -> str:
        """Get access token, using cached if valid.

        Args:
            force_refresh: Force refresh token even if current one is valid.

        Returns:
            Access token string.

        Raises:
            WeChatAPIError: If API call fails.
        """
        # Return cached token if still valid (with 60s buffer)
        if not force_refresh and self._access_token and time.time() < self._token_expires_at - 60:
            return self._access_token

        result = self._request(
            "GET",
            "/token",
            params={
                "grant_type": "client_credential",
                "appid": self.app_id,
                "secret": self.app_secret,
            },
        )

        self._access_token = result["access_token"]
        self._token_expires_at = time.time() + result.get("expires_in", 7200)

        return self._access_token

    def upload_image(self, image_path: str) -> Dict[str, Any]:
        """Upload image to WeChat server (for article content).

        Args:
            image_path: Local path to the image file.

        Returns:
            Dict with media_id and url.
        """
        token = self.get_access_token()
        url = f"{self.BASE_URL}/media/uploadimg"
        params = {"access_token": token, "type": "image"}

        with open(image_path, "rb") as f:
            files = {"media": (image_path.split("/")[-1], f, "image/png")}
            resp = requests.post(
                url, params=params, files=files, proxies=self._get_proxies(), timeout=60
            )

        result = resp.json()
        if result.get("errcode") and result["errcode"] != 0:
            raise WeChatAPIError(
                result.get("errmsg", "Upload failed"),
                result["errcode"],
                result,
            )

        return result

    def upload_thumb(self, thumb_path: str) -> str:
        """Upload thumb/cover image, return media_id.

        Args:
            thumb_path: Local path to the thumb image file.

        Returns:
            media_id string.
        """
        token = self.get_access_token()
        url = f"{self.BASE_URL}/material/add_material"
        params = {"access_token": token, "type": "thumb"}

        with open(thumb_path, "rb") as f:
            files = {"media": (thumb_path.split("/")[-1], f, "image/jpeg")}
            resp = requests.post(
                url, params=params, files=files, proxies=self._get_proxies(), timeout=60
            )

        result = resp.json()
        if result.get("errcode") and result["errcode"] != 0:
            raise WeChatAPIError(
                result.get("errmsg", "Upload thumb failed"),
                result["errcode"],
                result,
            )

        return result["media_id"]

    def add_draft(
        self,
        title: str,
        content: str,
        author: str = None,
        thumb_media_id: str = None,
        digest: str = None,
    ) -> Dict[str, Any]:
        """Create a draft article.

        Args:
            title: Article title (max 64 chars).
            content: Article content in HTML format.
            author: Author name (max 8 chars).
            thumb_media_id: Cover image media_id.
            digest: Article summary (max 54 chars).

        Returns:
            Dict with media_id of created draft.
        """
        token = self.get_access_token()
        url = f"{self.BASE_URL}/draft/add"
        params = {"access_token": token}

        articles = [
            {
                "title": title,
                "author": author or "",
                "digest": digest or "",
                "content": content,
                "thumb_media_id": thumb_media_id or "",
                "need_open_comment": 1,
                "only_fans_can_comment": 0,
            }
        ]

        # Use ensure_ascii=False to send UTF-8 directly (avoids Unicode escape issues)
        import json

        json_str = json.dumps({"articles": articles}, ensure_ascii=False)
        result = self._request(
            "POST",
            "/draft/add",
            params=params,
            data=json_str.encode("utf-8"),
        )

        return result

    def get_draft_count(self) -> int:
        """Get total count of drafts."""
        token = self.get_access_token()
        result = self._request(
            "GET",
            "/draft/count",
            params={"access_token": token},
        )
        return result.get("total_count", 0)

    def get_draft_list(self, offset: int = 0, count: int = 20) -> Dict[str, Any]:
        """Get draft list.

        Args:
            offset: Offset for pagination.
            count: Number of items to return (max 20).

        Returns:
            Dict with item list and total count.
        """
        token = self.get_access_token()
        result = self._request(
            "POST",
            "/draft/batchget",
            params={"access_token": token},
            json_data={"offset": offset, "count": count, "no_content": 0},
        )
        return result

    def get_draft(self, media_id: str) -> Dict[str, Any]:
        """Get single draft detail.

        Args:
            media_id: The draft media_id.

        Returns:
            Draft content.
        """
        token = self.get_access_token()
        result = self._request(
            "POST",
            "/draft/get",
            params={"access_token": token},
            json_data={"media_id": media_id},
        )
        return result

    def delete_draft(self, media_id: str) -> Dict[str, Any]:
        """Delete a draft.

        Args:
            media_id: The draft media_id to delete.

        Returns:
            Success status.
        """
        token = self.get_access_token()
        result = self._request(
            "POST",
            "/draft/delete",
            params={"access_token": token},
            json_data={"media_id": media_id},
        )
        return result

    def publish_draft(self, media_id: str) -> Dict[str, Any]:
        """Publish a draft (submit for review).

        Note: Only available for certified accounts.

        Args:
            media_id: The draft media_id to publish.

        Returns:
            Publish result.
        """
        token = self.get_access_token()
        result = self._request(
            "POST",
            "/freepublish/submit",
            params={"access_token": token},
            json_data={"media_id": media_id},
        )
        return result

    def batch_get_material(
        self, type_: str = "image", offset: int = 0, count: int = 20
    ) -> List[Dict]:
        """Get permanent materials list.

        Args:
            type_: Material type: "image", "video", "voice", "news"
            offset: Offset for pagination.
            count: Number of items to return (max 20).

        Returns:
            List of materials.
        """
        token = self.get_access_token()
        result = self._request(
            "POST",
            "/material/batchget_material",
            params={"access_token": token},
            json_data={"type": type_, "offset": offset, "count": count},
        )
        return result.get("item", [])


# Singleton instance
_api: Optional[WeChatAPI] = None


def get_api() -> WeChatAPI:
    """Get global API instance."""
    global _api
    if _api is None:
        _api = WeChatAPI()
    return _api
