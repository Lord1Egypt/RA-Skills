"""
collectors/dingtalk.py — DingTalk AI Recording Collector

# ⚠️ EXPERIMENTAL: DingTalk collector is a stub implementation.
# Core methods return empty results.

Collects meeting transcripts and AI summaries from DingTalk's AI recording feature.
Supports incremental collection since last sync time.

Requires: dingtalk-sdk (optional, falls back to REST API)
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from typing import Any

from .base import MemoryCollector, RawMemory, CollectionResult, CollectorStatus

logger = logging.getLogger(__name__)


class DingTalkConfig:
    """DingTalk API configuration."""
    def __init__(self, app_key: str = "", app_secret: str = "",
                 corp_id: str = "", tenant_id: str = "work",
                 reliability_score: float = 0.9):
        self.app_key = app_key
        self.app_secret = app_secret
        self.corp_id = corp_id
        self.tenant_id = tenant_id
        self.reliability_score = reliability_score


class DingTalkCollector(MemoryCollector):
    """DingTalk AI recording collector.

    ⚠️ STUB IMPLEMENTATION — _fetch_recordings() returns empty list.
    To implement, override _fetch_recordings() with actual DingTalk API calls.

    Data flow:
    1. Authenticate with DingTalk OpenAPI
    2. Fetch AI recording list (incremental since last_sync)
    3. For each recording, fetch transcript + AI summary
    4. Return as RawMemory items

    Note: Without valid API credentials, collect() returns empty results.
    """

    def __init__(self, config: DingTalkConfig | dict | None = None):
        if isinstance(config, DingTalkConfig):
            cfg = config
        else:
            d = config or {}
            cfg = DingTalkConfig(
                app_key=d.get("app_key", ""),
                app_secret=d.get("app_secret", ""),
                corp_id=d.get("corp_id", ""),
                tenant_id=d.get("tenant_id", "work"),
                reliability_score=d.get("reliability_score", 0.9),
            )
        super().__init__(config={
            "app_key": cfg.app_key,
            "app_secret": cfg.app_secret,
            "corp_id": cfg.corp_id,
            "tenant_id": cfg.tenant_id,
            "reliability_score": cfg.reliability_score,
        })
        self._ding_config = cfg
        self._access_token = ""
        self._token_expires = 0.0
        self._is_implemented = False

    def get_source_id(self) -> str:
        return "dingtalk"

    def test_connection(self) -> dict:
        """Test DingTalk API connectivity.

        Returns NOT_IMPLEMENTED status because the core API integration
        (_fetch_recordings) is a placeholder that always returns empty results.
        """
        logger.warning(
            "DingTalk: test_connection 返回 NOT_IMPLEMENTED — "
            "核心 API 集成（_fetch_recordings）为占位实现，尚未对接真实 API"
        )
        self.status = CollectorStatus.NOT_IMPLEMENTED
        return {
            "connected": False,
            "not_implemented": True,
            "message": "DingTalk 收集器为占位实现，核心 API（_fetch_recordings）尚未对接真实接口，无法获取数据",
        }

    async def collect(self, since: float | None = None) -> CollectionResult:
        """Collect AI recordings from DingTalk."""
        result = CollectionResult(
            source=self.get_source_id(),
            started_at=time.time(),
            status=CollectorStatus.SYNCING,
        )

        if not self._ding_config.app_key:
            result.status = CollectorStatus.ERROR
            result.errors.append("No API credentials configured")
            result.finished_at = time.time()
            return result

        try:
            # Step 1: Get access token
            token = self._get_access_token()
            if not token:
                raise RuntimeError("Failed to get access token")

            # Step 2: Fetch recordings list
            since_ms = int((since or 0) * 1000)
            recordings = self._fetch_recordings(token, since_ms)
            result.total_available = len(recordings)

            if not recordings:
                logger.warning(
                    "DingTalk: collect() 未获取到任何数据 — "
                    "_fetch_recordings 为占位实现，始终返回空列表。"
                    "请完成钉钉 AI 录音 API 集成后再使用此收集器"
                )
                result.warnings.append(
                    "DingTalk 收集器尚未实现：核心 API（_fetch_recordings）为占位实现，"
                    "始终返回空列表。请完成钉钉 AI 录音 API 集成后再使用此收集器"
                )

            # Step 3: Process each recording
            for rec in recordings:
                try:
                    raw = self._process_recording(token, rec)
                    if raw:
                        result.items.append(raw)
                        result.collected_count += 1
                    else:
                        result.skipped_count += 1
                except Exception as e:
                    result.error_count += 1
                    result.errors.append(str(e))
                    logger.warning("DingTalk: Failed to process recording: %s", e)

            self.last_sync = time.time()
            self._collect_count += result.collected_count
            result.status = CollectorStatus.IDLE

        except Exception as e:
            result.status = CollectorStatus.ERROR
            result.errors.append(str(e))
            self._error_count += 1
            logger.error("DingTalk collection failed: %s", e)

        result.finished_at = time.time()
        return result

    def _get_access_token(self) -> str:
        """Get or refresh DingTalk access token."""
        if self._access_token and time.time() < self._token_expires:
            return self._access_token

        # Try using dingtalk-sdk if available
        try:
            import dingtalk_sdk  # type: ignore
            # Use SDK to get token
            client = dingtalk_sdk.DingTalkClient(
                app_key=self._ding_config.app_key,
                app_secret=self._ding_config.app_secret,
            )
            token_info = client.get_access_token()
            self._access_token = token_info.get("access_token", "")
            self._token_expires = time.time() + 7200
            return self._access_token
        except ImportError:
            pass

        # Fallback: REST API (POST to avoid secrets in URL)
        try:
            import urllib.request
            url = "https://oapi.dingtalk.com/gettoken"
            body = json.dumps({
                "appkey": self._ding_config.app_key,
                "appsecret": self._ding_config.app_secret,
            }).encode("utf-8")
            req = urllib.request.Request(url, data=body, method="POST")
            req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                if data.get("errcode") == 0:
                    self._access_token = data["access_token"]
                    self._token_expires = time.time() + 7200
                    return self._access_token
        except Exception as e:
            logger.error("DingTalk token request failed: %s", e)

        return ""

    # ⚠️ EXPERIMENTAL — 此方法为占位实现，尚未完成 API 对接，不建议在生产环境使用
    def _fetch_recordings(self, token: str, since_ms: int) -> list[dict]:
        """Fetch AI recording list from DingTalk.

        ⚠️ 占位实现：始终返回空列表，API 集成待完成。
        生产环境应调用 GET /v1.0/smartWork/aiRecoding/list
        """
        logger.warning(
            "DingTalk: _fetch_recordings 为占位实现，始终返回空列表。"
            "需对接钉钉 AI 录音 API (GET /v1.0/smartWork/aiRecoding/list)"
        )
        return []

    def _process_recording(self, token: str, recording: dict) -> RawMemory | None:
        """Process a single recording into a RawMemory."""
        transcript = recording.get("transcript", "")
        if not transcript or len(transcript) < 10:
            return None

        return RawMemory(
            content=transcript,
            source="dingtalk",
            source_id=f"recording_{recording.get('recordingId', '')}",
            timestamp=recording.get("startTime", 0) / 1000,
            metadata={
                "meeting_title": recording.get("title", ""),
                "participants": recording.get("participants", []),
                "duration": recording.get("duration", 0),
                "ai_summary": recording.get("summary", ""),
                "tenant_id": self._ding_config.tenant_id,
            },
            content_type="text",
        )
