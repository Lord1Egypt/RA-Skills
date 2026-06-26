#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Westmoon token storage helpers.
"""

import json
import os
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class TokenInfo:
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 0
    expires_at: float = 0.0
    user_info: Dict[str, Any] = field(default_factory=dict)
    created_at: float = 0.0

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = time.time()
        if not self.expires_at and self.expires_in:
            self.expires_at = self.created_at + self.expires_in

    @property
    def authorization_header(self) -> str:
        return f"{self.token_type} {self.access_token}".strip()

    @property
    def is_expired(self) -> bool:
        if not self.access_token:
            return True
        if self.expires_at <= 0:
            return False
        return time.time() > max(self.expires_at - 300, self.created_at)

    @property
    def expire_datetime(self) -> str:
        if self.expires_at <= 0:
            return "未知"
        return datetime.fromtimestamp(self.expires_at).strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenInfo":
        return cls(**data)


class TokenManager:
    DEFAULT_STORAGE_DIR = Path.home() / ".westmoon-user-login"
    DEFAULT_TOKEN_FILE = DEFAULT_STORAGE_DIR / "tokens.json"
    DEFAULT_PENDING_FILE = DEFAULT_STORAGE_DIR / "pending_login.json"

    def __init__(self, token_file: Optional[str] = None) -> None:
        self.token_file = Path(token_file) if token_file else self.DEFAULT_TOKEN_FILE
        self.pending_file = self.DEFAULT_PENDING_FILE
        self._ensure_storage_dir()
        self._token_info: Optional[TokenInfo] = None
        self._load_tokens()

    def _ensure_storage_dir(self) -> None:
        self.token_file.parent.mkdir(parents=True, exist_ok=True)
        os.chmod(self.token_file.parent, 0o700)

    def _load_tokens(self) -> None:
        if not self.token_file.exists():
            return
        try:
            with self.token_file.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, dict) and data.get("access_token"):
                self._token_info = TokenInfo.from_dict(data)
        except Exception as exc:
            print(f"[TokenManager] 加载登录态失败: {exc}")

    def _save_tokens(self) -> bool:
        if self._token_info is None:
            return True
        try:
            temp_file = self.token_file.with_suffix(".tmp")
            with temp_file.open("w", encoding="utf-8") as handle:
                json.dump(self._token_info.to_dict(), handle, indent=2, ensure_ascii=False)
            os.chmod(temp_file, 0o600)
            temp_file.replace(self.token_file)
            return True
        except Exception as exc:
            print(f"[TokenManager] 保存登录态失败: {exc}")
            return False

    def save_token(self, token_info: TokenInfo) -> bool:
        self._token_info = token_info
        return self._save_tokens()

    def get_token(self) -> Optional[TokenInfo]:
        if self._token_info is None:
            return None
        if self._token_info.is_expired:
            return None
        return self._token_info

    def get_stored_token(self) -> Optional[TokenInfo]:
        return self._token_info

    def get_authorization_header(self) -> Optional[str]:
        token = self.get_token()
        if not token:
            return None
        return token.authorization_header

    def remove_token(self) -> bool:
        self._token_info = None
        try:
            if self.token_file.exists():
                self.token_file.unlink()
            return True
        except Exception as exc:
            print(f"[TokenManager] 删除登录态失败: {exc}")
            return False

    def get_token_summary(self) -> Optional[Dict[str, Any]]:
        token = self._token_info
        if not token:
            return None
        user_info = token.user_info or {}
        return {
            "token_type": token.token_type,
            "has_access_token": bool(token.access_token),
            "has_refresh_token": bool(token.refresh_token),
            "expires_at": token.expire_datetime,
            "is_expired": token.is_expired,
            "user_id": user_info.get("id") or user_info.get("uid") or user_info.get("user_id"),
            "nickname": user_info.get("nickname") or user_info.get("name"),
        }

    def print_summary(self) -> None:
        summary = self.get_token_summary()
        if not summary:
            print("[TokenManager] 没有存储的登录态")
            return
        print("[TokenManager] 当前登录态")
        print("-" * 60)
        for key, value in summary.items():
            print(f"{key}: {value}")
        print("-" * 60)

    def save_pending_login(self, scan_token: str, poll_interval_ms: int = 2000) -> None:
        payload = {
            "scan_token": scan_token,
            "poll_interval_ms": poll_interval_ms,
            "created_at": time.time(),
        }
        with self.pending_file.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False)
        os.chmod(self.pending_file, 0o600)

    def load_pending_login(self, max_age_seconds: int = 300) -> Optional[Dict[str, Any]]:
        if not self.pending_file.exists():
            return None
        try:
            with self.pending_file.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
            created_at = float(payload.get("created_at", 0))
            if time.time() - created_at > max_age_seconds:
                self.clear_pending_login()
                return None
            if not payload.get("scan_token"):
                self.clear_pending_login()
                return None
            return payload
        except Exception:
            return None

    def clear_pending_login(self) -> None:
        if self.pending_file.exists():
            self.pending_file.unlink()
