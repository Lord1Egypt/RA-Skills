"""Load settings from environment and optional .env file."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Tuple


def _try_load_dotenv(project_root: Path) -> None:
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    env_path = project_root / ".env"
    if env_path.is_file():
        load_dotenv(env_path)


def find_project_root() -> Path:
    if os.environ.get("TG_PROJECT_ROOT"):
        return Path(os.environ["TG_PROJECT_ROOT"]).resolve()
    here = Path(__file__).resolve()
    for p in [here.parent] + list(here.parents):
        if (p / "pyproject.toml").is_file():
            return p
    return Path.cwd().resolve()


def get_web_output_dir() -> Path:
    """Directory for web scraper Excel output; does not require Telegram API env vars."""
    root = find_project_root()
    _try_load_dotenv(root)
    raw = os.environ.get("TG_MONITOR_WEB_OUTPUT_DIR")
    if raw:
        return Path(raw).expanduser().resolve()
    return root / "output_web"


@dataclass(frozen=True)
class Config:
    api_id: int
    api_hash: str
    session_name: str
    proxy: Tuple[str, str, int]
    project_root: Path
    phone: str | None

    @property
    def session_file_base(self) -> str:
        """Path prefix for Telethon session (no .session suffix)."""
        session_dir = self.project_root / "userdata"
        session_dir.mkdir(parents=True, exist_ok=True)
        return str(session_dir / self.session_name)

    def web_output_dir(self) -> Path:
        return get_web_output_dir()


def _parse_proxy() -> Tuple[str, str, int]:
    host = os.environ.get("TELEGRAM_PROXY_HTTP_HOST", "127.0.0.1")
    port = int(os.environ.get("TELEGRAM_PROXY_HTTP_PORT", "1087"))
    return ("http", host, port)


def load_config() -> Config:
    root = find_project_root()
    _try_load_dotenv(root)
    api_id_s = os.environ.get("TELEGRAM_API_ID", "").strip()
    api_hash = os.environ.get("TELEGRAM_API_HASH", "").strip()
    if not api_id_s or not api_hash:
        raise RuntimeError(
            "缺少 TELEGRAM_API_ID 或 TELEGRAM_API_HASH。"
            "请在项目根目录复制 .env.example 为 .env 并填写，或设置环境变量。"
        )
    api_id = int(api_id_s)
    session_name = os.environ.get("TELEGRAM_SESSION_NAME", "tg_monitor_session").strip() or "tg_monitor_session"
    phone = os.environ.get("TELEGRAM_PHONE", "").strip() or None
    return Config(
        api_id=api_id,
        api_hash=api_hash,
        session_name=session_name,
        proxy=_parse_proxy(),
        project_root=root,
        phone=phone,
    )


def proxy_tuple_for_telethon(cfg: Config) -> Tuple[Any, ...]:
    return cfg.proxy
