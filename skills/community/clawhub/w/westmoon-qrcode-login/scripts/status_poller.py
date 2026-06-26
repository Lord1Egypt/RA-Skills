#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Westmoon login-status polling helpers.
"""

import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, Optional

import requests


class LoginStatus(Enum):
    WAITING = "waiting"
    SCANNED = "scanned"
    CONFIRMED = "confirmed"
    EXPIRED = "expired"
    CANCELED = "canceled"
    REJECTED = "rejected"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass
class StatusResult:
    status: LoginStatus
    status_str: str
    message: str
    access_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    raw_response: Optional[Dict] = None
    raw_http_response: Optional[requests.Response] = None


class StatusPoller:
    STATUS_MAP = {
        "waiting": LoginStatus.WAITING,
        "pending": LoginStatus.WAITING,
        "scanned": LoginStatus.SCANNED,
        "confirmed": LoginStatus.CONFIRMED,
        "success": LoginStatus.CONFIRMED,
        "expired": LoginStatus.EXPIRED,
        "invalid": LoginStatus.EXPIRED,
        "canceled": LoginStatus.CANCELED,
        "cancelled": LoginStatus.CANCELED,
        "rejected": LoginStatus.REJECTED,
    }

    def __init__(
        self,
        base_url: str,
        poll_endpoint: str,
        poll_interval_ms: int = 2000,
        timeout_seconds: int = 300,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.poll_endpoint = poll_endpoint
        self.poll_interval_ms = poll_interval_ms
        self.timeout_seconds = timeout_seconds
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
                ),
                "Accept": "application/json, text/plain, */*",
            }
        )

    def check_status(self, scan_token: str, source: str = "xpw") -> StatusResult:
        url = f"{self.base_url}{self.poll_endpoint}"
        try:
            response = self.session.get(
                url,
                params={"scan_token": scan_token, "source": source},
                timeout=15,
            )
            response.raise_for_status()
            result = response.json()
            if result.get("code") != 0:
                return StatusResult(
                    status=LoginStatus.ERROR,
                    status_str="error",
                    message=result.get("msg", "轮询失败"),
                    raw_response=result,
                    raw_http_response=response,
                )
            data = result.get("data") or {}
            status_str = str(data.get("status") or "unknown").lower()
            mapped = self.STATUS_MAP.get(status_str, LoginStatus.UNKNOWN)
            return StatusResult(
                status=mapped,
                status_str=status_str,
                message=self._message_for_status(mapped),
                access_token=data.get("access_token", ""),
                refresh_token=data.get("refresh_token", ""),
                token_type=data.get("token_type", "Bearer"),
                expires_in=int(data.get("expires_in") or 0),
                raw_response=result,
                raw_http_response=response,
            )
        except requests.RequestException as exc:
            return StatusResult(
                status=LoginStatus.ERROR,
                status_str="error",
                message=f"请求失败: {exc}",
            )

    def poll_until_complete(
        self,
        scan_token: str,
        source: str = "xpw",
        on_status_change: Optional[Callable[[StatusResult], None]] = None,
    ) -> StatusResult:
        started_at = time.time()
        last_status: Optional[LoginStatus] = None
        while time.time() - started_at < self.timeout_seconds:
            result = self.check_status(scan_token, source=source)
            if result.status != last_status and on_status_change:
                on_status_change(result)
            if result.status in {
                LoginStatus.CONFIRMED,
                LoginStatus.EXPIRED,
                LoginStatus.CANCELED,
                LoginStatus.REJECTED,
                LoginStatus.ERROR,
            }:
                return result
            last_status = result.status
            time.sleep(self.poll_interval_ms / 1000)
        return StatusResult(
            status=LoginStatus.ERROR,
            status_str="timeout",
            message="轮询超时",
        )

    @staticmethod
    def _message_for_status(status: LoginStatus) -> str:
        mapping = {
            LoginStatus.WAITING: "等待扫码",
            LoginStatus.SCANNED: "已扫码，等待确认",
            LoginStatus.CONFIRMED: "已确认登录",
            LoginStatus.EXPIRED: "二维码已过期",
            LoginStatus.CANCELED: "用户已取消",
            LoginStatus.REJECTED: "用户已拒绝",
            LoginStatus.ERROR: "请求失败",
            LoginStatus.UNKNOWN: "未知状态",
        }
        return mapping.get(status, "未知状态")
