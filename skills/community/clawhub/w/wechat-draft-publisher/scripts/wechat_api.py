"""
微信公众号 API 模块
支持：获取 access_token、上传图片素材、新增草稿、发布草稿
"""

import json
import os
import time
import requests


class WeChatAPI:
    """微信公众号 API 客户端"""

    BASE_URL = "https://api.weixin.qq.com/cgi-bin"

    def __init__(self, appid: str = None, appsecret: str = None):
        self.appid = appid or os.environ.get("WECHAT_APPID", "")
        self.appsecret = appsecret or os.environ.get("WECHAT_APPSECRET", "")
        self._access_token = None
        self._token_expires_at = 0

        if not self.appid or not self.appsecret:
            raise ValueError(
                "需要设置环境变量 WECHAT_APPID 和 WECHAT_APPSECRET，"
                "或在初始化时传入 appid 和 appsecret"
            )

    def get_access_token(self) -> str:
        """获取 access_token，自动缓存和刷新"""
        if self._access_token and time.time() < self._token_expires_at - 300:
            return self._access_token

        url = f"{self.BASE_URL}/token"
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.appsecret,
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()

        if "access_token" not in data:
            raise RuntimeError(f"获取 access_token 失败: {data}")

        self._access_token = data["access_token"]
        self._token_expires_at = time.time() + data.get("expires_in", 7200)
        return self._access_token

    def upload_article_image(self, image_path: str) -> str:
        """
        上传文章内容中的图片（返回 URL，用于文章正文内嵌图片）
        注意：此接口上传的图片不占用素材库额度
        """
        token = self.get_access_token()
        url = f"{self.BASE_URL}/media/uploadimg?access_token={token}"

        with open(image_path, "rb") as f:
            files = {"media": (os.path.basename(image_path), f, "image/png")}
            resp = requests.post(url, files=files, timeout=30)

        data = resp.json()
        if "url" not in data:
            raise RuntimeError(f"上传文章图片失败: {data}")

        return data["url"]

    def upload_thumb_image(self, image_path: str) -> str:
        """
        上传封面图片为永久素材（返回 media_id，用于草稿封面）
        """
        token = self.get_access_token()
        url = f"{self.BASE_URL}/material/add_material?access_token={token}&type=image"

        with open(image_path, "rb") as f:
            files = {"media": (os.path.basename(image_path), f, "image/png")}
            resp = requests.post(url, files=files, timeout=30)

        data = resp.json()
        if "media_id" not in data:
            raise RuntimeError(f"上传封面图片失败: {data}")

        return data["media_id"]

    def add_draft(
        self,
        title: str,
        content: str,
        thumb_media_id: str,
        author: str = "",
        digest: str = "",
        content_source_url: str = "",
    ) -> str:
        """
        新增草稿
        返回草稿的 media_id
        """
        token = self.get_access_token()
        url = f"{self.BASE_URL}/draft/add?access_token={token}"

        article = {
            "title": title,
            "author": author,
            "digest": digest,
            "content": content,
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 1,
            "only_fans_can_comment": 0,
        }
        if content_source_url:
            article["content_source_url"] = content_source_url

        payload = {"articles": [article]}
        resp = requests.post(
            url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            timeout=15,
        )

        data = resp.json()
        if "media_id" not in data:
            raise RuntimeError(f"新增草稿失败: {data}")

        return data["media_id"]

    def submit_publish(self, media_id: str) -> str:
        """
        发布草稿（提交发布任务）
        返回 publish_id
        """
        token = self.get_access_token()
        url = f"{self.BASE_URL}/freepublish/submit?access_token={token}"

        payload = {"media_id": media_id}
        resp = requests.post(url, json=payload, timeout=15)

        data = resp.json()
        if data.get("errcode", 0) != 0:
            raise RuntimeError(f"发布草稿失败: {data}")

        return data.get("publish_id", "")
