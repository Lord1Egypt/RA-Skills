from __future__ import annotations

import json
import mimetypes
from pathlib import Path
from typing import Any

import requests

from .models import WeChatConfig
from .utils import trim_utf8_bytes

TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
DRAFT_ADD_URL = "https://api.weixin.qq.com/cgi-bin/draft/add"
PUBLISH_SUBMIT_URL = "https://api.weixin.qq.com/cgi-bin/freepublish/submit"
PUBLISH_GET_URL = "https://api.weixin.qq.com/cgi-bin/freepublish/get"
MATERIAL_ADD_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"


class WeChatPublishError(RuntimeError):
    pass


def normalize_wechat_title(text: str) -> str:
    value = " ".join((text or "").strip().split())
    return value[:64].strip() or "未命名文章"


class WeChatClient:
    def __init__(self, config: WeChatConfig, timeout: int = 30):
        self.config = config
        self.timeout = timeout

    def get_token(self) -> str:
        if not self.config.app_id or not self.config.app_secret:
            raise WeChatPublishError("配置缺少微信公众号 app_id 或 app_secret")

        response = requests.get(
            TOKEN_URL,
            params={
                "grant_type": "client_credential",
                "appid": self.config.app_id,
                "secret": self.config.app_secret,
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        data = response.json()
        if data.get("errcode", 0) != 0:
            raise WeChatPublishError(f"获取 access_token 失败: {data}")
        token = data.get("access_token")
        if not token:
            raise WeChatPublishError("获取 access_token 失败: 响应缺少 access_token")
        return token

    def _post_json(self, url: str, params: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
        response = requests.post(
            url,
            params=params,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return json.loads(response.content.decode("utf-8"))

    def upload_material(self, token: str, file_path: Path, material_type: str = "image") -> dict[str, Any]:
        mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
        with file_path.open("rb") as handle:
            response = requests.post(
                MATERIAL_ADD_URL,
                params={"access_token": token, "type": material_type},
                files={"media": (file_path.name, handle, mime)},
                timeout=self.timeout,
            )
        response.raise_for_status()
        data = response.json()
        if data.get("errcode", 0) != 0:
            raise WeChatPublishError(f"上传素材失败: {data}")
        return data

    def create_draft(
        self,
        token: str,
        title: str,
        author: str,
        digest: str,
        content_html: str,
        source_url: str,
        thumb_media_id: str,
    ) -> str:
        payload = {
            "articles": [
                {
                    "title": normalize_wechat_title(title),
                    "author": trim_utf8_bytes(author or self.config.author, 16),
                    "digest": trim_utf8_bytes((digest or "").strip(), 120) or "文章摘要",
                    "content": content_html,
                    "content_source_url": (source_url or "")[:200],
                    "thumb_media_id": thumb_media_id,
                    "need_open_comment": 1 if self.config.open_comment else 0,
                    "only_fans_can_comment": 1 if self.config.fans_only_comment else 0,
                }
            ]
        }
        data = self._post_json(DRAFT_ADD_URL, {"access_token": token}, payload)
        if data.get("errcode", 0) != 0:
            raise WeChatPublishError(f"创建草稿失败: {data}")
        media_id = data.get("media_id")
        if not media_id:
            raise WeChatPublishError("创建草稿失败: 响应缺少 media_id")
        return media_id

    def submit_publish(self, token: str, media_id: str) -> str:
        data = self._post_json(PUBLISH_SUBMIT_URL, {"access_token": token}, {"media_id": media_id})
        if data.get("errcode", 0) != 0:
            raise WeChatPublishError(f"提交发布失败: {data}")
        publish_id = data.get("publish_id")
        if not publish_id:
            raise WeChatPublishError("提交发布失败: 响应缺少 publish_id")
        return publish_id

    def get_publish_status(self, token: str, publish_id: str) -> dict[str, Any]:
        data = self._post_json(PUBLISH_GET_URL, {"access_token": token}, {"publish_id": publish_id})
        if data.get("errcode", 0) != 0:
            raise WeChatPublishError(f"查询发布状态失败: {data}")
        return data
