"""Xiaohongshu MCP Client"""

import httpx
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List
from datetime import datetime


class Settings(BaseSettings):
    """Client settings"""
    base_url: str = "http://localhost:18060"
    timeout: int = 60
    verify_ssl: bool = True

    model_config = {
        "env_prefix": "XHS_",
        "env": {
            "base_url": ["XHS_MCP_BASE_URL", "XHS_BASE_URL"]
        }
    }


class XiaohongshuClient:
    """Xiaohongshu MCP REST API Client"""

    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        """Initialize client"""
        settings = Settings()
        self.base_url = base_url or settings.base_url
        self.timeout = timeout or settings.timeout
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            verify=settings.verify_ssl
        )

    def __enter__(self):
        """Enter context"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context"""
        self.close()

    def close(self):
        """Close client"""
        self.client.close()

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            if hasattr(e, 'response') and e.response:
                try:
                    error_data = e.response.json()
                    raise Exception(f"API Error: {error_data.get('error', 'Unknown error')}")
                except:
                    pass
            raise Exception(f"HTTP Error: {str(e)}")

    def check_login_status(self) -> Dict[str, Any]:
        """Check login status"""
        return self._request("GET", "/api/v1/login/status")

    def get_login_qrcode(self) -> Dict[str, Any]:
        """Get login QR code"""
        return self._request("GET", "/api/v1/login/qrcode")

    def delete_cookies(self) -> Dict[str, Any]:
        """Delete cookies"""
        return self._request("DELETE", "/api/v1/login/cookies")

    def publish_content(
        self,
        title: str,
        content: str,
        images: List[str],
        tags: Optional[List[str]] = None,
        visibility: Optional[str] = None,
        schedule_at: Optional[datetime] = None,
        is_original: Optional[bool] = None,
        products: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Publish content"""
        data = {
            "title": title,
            "content": content,
            "images": images
        }
        if tags:
            data["tags"] = tags
        if visibility:
            data["visibility"] = visibility
        if schedule_at:
            data["schedule_at"] = schedule_at.isoformat()
        if is_original is not None:
            data["is_original"] = is_original
        if products:
            data["products"] = products
        return self._request("POST", "/api/v1/publish", json=data)

    def publish_video(
        self,
        title: str,
        content: str,
        video: str,
        tags: Optional[List[str]] = None,
        visibility: Optional[str] = None,
        schedule_at: Optional[datetime] = None,
        products: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Publish video"""
        data = {
            "title": title,
            "content": content,
            "video": video
        }
        if tags:
            data["tags"] = tags
        if visibility:
            data["visibility"] = visibility
        if schedule_at:
            data["schedule_at"] = schedule_at.isoformat()
        if products:
            data["products"] = products
        return self._request("POST", "/api/v1/publish_video", json=data)

    def list_feeds(self) -> Dict[str, Any]:
        """List feeds"""
        return self._request("GET", "/api/v1/feeds/list")

    def search_feeds(
        self,
        keyword: str,
        sort_by: Optional[str] = None,
        note_type: Optional[str] = None,
        publish_time: Optional[str] = None,
        search_scope: Optional[str] = None,
        location: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search feeds"""
        data = {
            "keyword": keyword,
            "filters": {}
        }
        if sort_by:
            data["filters"]["sort_by"] = sort_by
        if note_type:
            data["filters"]["note_type"] = note_type
        if publish_time:
            data["filters"]["publish_time"] = publish_time
        if search_scope:
            data["filters"]["search_scope"] = search_scope
        if location:
            data["filters"]["location"] = location
        return self._request("POST", "/api/v1/feeds/search", json=data)

    def get_feed_detail(
        self,
        feed_id: str,
        xsec_token: str,
        load_all_comments: bool = False,
        comment_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get feed detail"""
        data = {
            "feed_id": feed_id,
            "xsec_token": xsec_token,
            "load_all_comments": load_all_comments
        }
        if comment_config:
            data["comment_config"] = comment_config
        return self._request("POST", "/api/v1/feeds/detail", json=data)

    def get_user_profile(self, user_id: str, xsec_token: str) -> Dict[str, Any]:
        """Get user profile"""
        data = {
            "user_id": user_id,
            "xsec_token": xsec_token
        }
        return self._request("POST", "/api/v1/user/profile", json=data)

    def get_my_profile(self) -> Dict[str, Any]:
        """Get my profile"""
        return self._request("GET", "/api/v1/user/me")

    def post_comment(self, feed_id: str, xsec_token: str, content: str) -> Dict[str, Any]:
        """Post comment"""
        data = {
            "feed_id": feed_id,
            "xsec_token": xsec_token,
            "content": content
        }
        return self._request("POST", "/api/v1/feeds/comment", json=data)

    def reply_comment(
        self,
        feed_id: str,
        xsec_token: str,
        content: str,
        comment_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Reply comment"""
        data = {
            "feed_id": feed_id,
            "xsec_token": xsec_token,
            "content": content
        }
        if comment_id:
            data["comment_id"] = comment_id
        if user_id:
            data["user_id"] = user_id
        return self._request("POST", "/api/v1/feeds/comment/reply", json=data)
