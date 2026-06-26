"""
collectors/wechat.py — Enterprise WeChat (WeCom) Collector

# ⚠️ EXPERIMENTAL: WeChat collector is a stub implementation.
# Core methods return empty results.

Collects messages and files from Enterprise WeChat (企业微信).
Note: Personal WeChat (itchat) is no longer maintained and is NOT supported.
Only Enterprise WeChat API is supported.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from .base import MemoryCollector, RawMemory, CollectionResult, CollectorStatus

logger = logging.getLogger(__name__)


class WeChatConfig:
    """Enterprise WeChat API configuration."""
    def __init__(self, corp_id: str = "", corp_secret: str = "",
                 agent_id: str = "", tenant_id: str = "work",
                 reliability_score: float = 0.85):
        self.corp_id = corp_id
        self.corp_secret = corp_secret
        self.agent_id = agent_id
        self.tenant_id = tenant_id
        self.reliability_score = reliability_score


class WeChatCollector(MemoryCollector):
    """WeChat Work message collector.

    ⚠️ STUB IMPLEMENTATION — _fetch_messages() returns empty list.
    To implement, override _fetch_messages() with actual WeChat Work API calls.

    Data flow:
    1. Authenticate with WeCom API
    2. Fetch recent messages (incremental since last_sync)
    3. Filter out trivial/system messages
    4. Return as RawMemory items
    """

    def __init__(self, config: WeChatConfig | dict | None = None):
        if isinstance(config, WeChatConfig):
            cfg = config
        else:
            d = config or {}
            cfg = WeChatConfig(
                corp_id=d.get("corp_id", ""),
                corp_secret=d.get("corp_secret", ""),
                agent_id=d.get("agent_id", ""),
                tenant_id=d.get("tenant_id", "work"),
                reliability_score=d.get("reliability_score", 0.85),
            )
        super().__init__(config={
            "corp_id": cfg.corp_id,
            "corp_secret": cfg.corp_secret,
            "agent_id": cfg.agent_id,
            "tenant_id": cfg.tenant_id,
            "reliability_score": cfg.reliability_score,
        })
        self._wc_config = cfg
        self._access_token = ""
        self._token_expires = 0.0
        self._is_implemented = False

    def get_source_id(self) -> str:
        return "enterprise_wechat"

    def test_connection(self) -> dict:
        """Test WeCom API connectivity.

        Returns NOT_IMPLEMENTED status because the core API integration
        (_fetch_messages) is a placeholder that always returns empty results.
        """
        logger.warning(
            "WeChat: test_connection 返回 NOT_IMPLEMENTED — "
            "核心 API 集成（_fetch_messages）为占位实现，尚未对接真实 API"
        )
        self.status = CollectorStatus.NOT_IMPLEMENTED
        return {
            "connected": False,
            "not_implemented": True,
            "message": "企业微信收集器为占位实现，核心 API（_fetch_messages）尚未对接真实接口，无法获取数据",
        }

    async def collect(self, since: float | None = None) -> CollectionResult:
        """Collect messages from Enterprise WeChat."""
        result = CollectionResult(
            source=self.get_source_id(),
            started_at=time.time(),
            status=CollectorStatus.SYNCING,
        )

        if not self._wc_config.corp_id:
            result.status = CollectorStatus.ERROR
            result.errors.append("No API credentials configured")
            result.finished_at = time.time()
            return result

        try:
            token = self._get_access_token()
            if not token:
                raise RuntimeError("Failed to get access token")

            # Fetch messages
            messages = self._fetch_messages(token, since)
            result.total_available = len(messages)

            if not messages:
                logger.warning(
                    "WeChat: collect() 未获取到任何数据 — "
                    "_fetch_messages 为占位实现，始终返回空列表。"
                    "请完成企业微信消息 API 集成后再使用此收集器"
                )
                result.warnings.append(
                    "企业微信收集器尚未实现：核心 API（_fetch_messages）为占位实现，"
                    "始终返回空列表。请完成企业微信会话内容存档 API 集成后再使用此收集器"
                )

            for msg in messages:
                try:
                    raw = self._process_message(msg)
                    if raw:
                        result.items.append(raw)
                        result.collected_count += 1
                    else:
                        result.skipped_count += 1
                except Exception as e:
                    result.error_count += 1
                    result.errors.append(str(e))

            self.last_sync = time.time()
            self._collect_count += result.collected_count
            result.status = CollectorStatus.IDLE

        except Exception as e:
            result.status = CollectorStatus.ERROR
            result.errors.append(str(e))
            self._error_count += 1

        result.finished_at = time.time()
        return result

    def _get_access_token(self) -> str:
        """Get or refresh WeCom access token."""
        if self._access_token and time.time() < self._token_expires:
            return self._access_token

        try:
            import urllib.request
            url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
            body = json.dumps({
                "corpid": self._wc_config.corp_id,
                "corpsecret": self._wc_config.corp_secret,
            }).encode("utf-8")
            req = urllib.request.Request(url, data=body, method="POST")
            req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                if data.get("errcode") == 0:
                    self._access_token = data["access_token"]
                    self._token_expires = time.time() + 7200
                    return self._access_token
                else:
                    logger.error("WeChat token error: %s", data.get("errmsg"))
        except Exception as e:
            logger.error("WeChat token request failed: %s", e)

        return ""

    # ⚠️ EXPERIMENTAL — 此方法为占位实现，尚未完成 API 对接，不建议在生产环境使用
    def _fetch_messages(self, token: str, since: float | None) -> list[dict]:
        """Fetch messages from WeCom API.

        ⚠️ 占位实现：始终返回空列表，API 集成待完成。
        生产环境应调用企业微信会话内容存档 API
        """
        logger.warning(
            "WeChat: _fetch_messages 为占位实现，始终返回空列表。"
            "需对接企业微信会话内容存档 API"
        )
        return []

    def _process_message(self, msg: dict) -> RawMemory | None:
        """Process a WeCom message into a RawMemory."""
        content = msg.get("content", "")
        if not content or len(content) < 5:
            return None

        # Filter trivial messages
        trivial = {"ok", "好的", "收到", "嗯", "1", "+1", "👍"}
        if content.strip() in trivial:
            return None

        return RawMemory(
            content=content,
            source="enterprise_wechat",
            source_id=msg.get("msgid", ""),
            timestamp=msg.get("msgtime", 0) / 1000,
            metadata={
                "from_user": msg.get("from", {}),
                "to_user": msg.get("tolist", []),
                "msg_type": msg.get("msgtype", "text"),
                "tenant_id": self._wc_config.tenant_id,
            },
        )
