"""TelegramClient factory."""

from __future__ import annotations

from telethon import TelegramClient

from tg_monitor_kit.config import Config, load_config


def build_client(cfg: Config | None = None) -> TelegramClient:
    if cfg is None:
        cfg = load_config()
    return TelegramClient(
        cfg.session_file_base,
        cfg.api_id,
        cfg.api_hash,
        proxy=cfg.proxy,
    )
