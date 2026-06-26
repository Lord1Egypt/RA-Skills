"""Runtime session helpers for long-running tasks.

Use a temporary session copy per daemon process to reduce sqlite lock contention
across monitor/search/join/send-schedule when they run concurrently.
"""

from __future__ import annotations

import os
import shutil
import uuid
from dataclasses import dataclass

from telethon import TelegramClient

from tg_monitor_kit.config import Config


@dataclass(frozen=True)
class TempSessionClient:
    client: TelegramClient
    temp_session_base: str

    @property
    def temp_session_path(self) -> str:
        return f"{self.temp_session_base}.session"


def create_temp_session_client(cfg: Config, purpose: str) -> TempSessionClient:
    """Create a TelegramClient bound to a temporary copied session file."""
    original_base = cfg.session_file_base
    original_session = f"{original_base}.session"
    if not os.path.exists(original_session):
        raise FileNotFoundError(
            f"未找到会话文件：{original_session}。"
            "请先执行登录（tg-monitor auth + tg-monitor login）后再运行对应命令。"
        )

    temp_session_base = f"{original_base}_{purpose}_{uuid.uuid4().hex[:8]}"
    temp_session = f"{temp_session_base}.session"
    shutil.copy2(original_session, temp_session)

    client = TelegramClient(
        temp_session_base,
        cfg.api_id,
        cfg.api_hash,
        proxy=cfg.proxy,
    )
    return TempSessionClient(client=client, temp_session_base=temp_session_base)


def cleanup_temp_session_files(temp_session_base: str) -> None:
    """Best-effort cleanup for temporary Telethon sqlite session files."""
    candidates = [
        f"{temp_session_base}.session",
        f"{temp_session_base}.session-journal",
        f"{temp_session_base}.session-wal",
        f"{temp_session_base}.session-shm",
        f"{temp_session_base}-journal",
        f"{temp_session_base}-wal",
        f"{temp_session_base}-shm",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
