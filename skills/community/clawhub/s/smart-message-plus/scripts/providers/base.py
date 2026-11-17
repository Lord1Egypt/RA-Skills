#!/usr/bin/env python3
"""smart-message-plus: provider adapter interface + capability matrix."""
from __future__ import annotations

from abc import ABC, abstractmethod


class SendResult:
    def __init__(self, ok: bool, msg_id: str = "", detail: str = "", extra: dict | None = None):
        self.ok = ok
        self.msg_id = msg_id
        self.detail = detail
        self.extra = extra or {}

    def __repr__(self):
        return f"SendResult(ok={self.ok}, msg_id={self.msg_id!r}, detail={self.detail!r})"


class Provider(ABC):
    """Adapter interface. Not every provider supports everything —
    capabilities() declares support; unsupported ops raise NotSupported."""

    name = "base"

    def __init__(self, account_slug: str, account: dict, cfg: dict):
        self.slug = account_slug
        self.account = account
        self.cfg = cfg
        self.timeout = int(cfg.get("http_timeout", 15))

    # ---- capability matrix ----
    @classmethod
    def capabilities(cls) -> dict:
        return {
            "p2p_text": False, "p2p_markdown": False,
            "group_text": False, "group_markdown": False,
            "image": False, "file": False,
            "mention": False, "mention_all": False,
            "recall": False,
            "resolve_by_mobile": False, "resolve_by_email": False,
            "org_lookup_builtin": False,
            "card": False,
            "create_group": False,
        }

    # ---- token ----
    @abstractmethod
    def get_token(self) -> str: ...

    @abstractmethod
    def test(self) -> tuple[bool, str]:
        """Connectivity + credential check. Returns (ok, human message)."""

    # ---- resolve ----
    @abstractmethod
    def resolve_user(self, raw: str) -> str:
        """mobile/email/native-id -> native user id. Raises ValueError with
        actionable guidance when not resolvable."""

    # ---- send ----
    @abstractmethod
    def send_p2p(self, user_ids: list[str], text: str, markdown: bool = False) -> SendResult: ...

    @abstractmethod
    def send_group(
        self, chat_id: str, text: str, markdown: bool = False,
        mention_ids: list[str] | None = None, mention_all: bool = False,
    ) -> SendResult: ...

    @abstractmethod
    def send_image_p2p(self, user_ids: list[str], path: str) -> SendResult: ...

    @abstractmethod
    def send_image_group(self, chat_id: str, path: str) -> SendResult: ...

    @abstractmethod
    def send_file_p2p(self, user_ids: list[str], path: str) -> SendResult: ...

    @abstractmethod
    def send_file_group(self, chat_id: str, path: str) -> SendResult: ...

    # ---- group management (v2.0) ----
    def create_group(self, name: str, owner_id: str, member_ids: list[str],
                     **kwargs) -> "SendResult":
        """Create a group chat. Returns SendResult with extra={'chat_id': ...}.
        Providers may accept extra kwargs (e.g. dingtalk: with_bot/template_id)."""
        raise NotSupported(f"{self.name} 未实现建群")

    def list_groups(self) -> list[dict]:
        """List groups the bot is in: [{'name', 'chat_id'}, ...]. Default: unsupported."""
        raise NotSupported(f"{self.name} 未实现群列表查询")

    # ---- card (v1.1) ----
    def send_card_p2p(self, user_ids: list[str], title: str, text: str,
                      buttons: list[tuple[str, str]] | None = None) -> SendResult:
        """buttons: [(label, url), ...]. Default: unsupported."""
        raise NotSupported(f"{self.name} 未实现卡片消息")

    def send_card_group(self, chat_id: str, title: str, text: str,
                        buttons: list[tuple[str, str]] | None = None) -> SendResult:
        raise NotSupported(f"{self.name} 未实现卡片消息")

    # ---- recall ----
    @abstractmethod
    def recall(self, log_entry: dict) -> tuple[bool, str]: ...

    # ---- org ----
    def org_resolve_department(self, dept_name: str) -> dict:
        """Returns {"dept_id", "dept_name", "member_ids": [...]}. Default: unsupported."""
        raise NotSupported(
            f"{self.name} 未实现内置组织架构查询。可在 config.json 配置 org_lookup.mode=custom + custom_url"
        )


class NotSupported(Exception):
    pass
