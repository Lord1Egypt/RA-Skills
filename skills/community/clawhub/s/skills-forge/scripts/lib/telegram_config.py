import os
from pathlib import Path
from typing import Optional


DEFAULT_ENV_FILES = [
    Path.home() / ".openclaw" / "telegram.env",
    Path.home() / ".openclaw" / "skill-forge.env",
    Path.home() / ".openclaw" / ".env",
    Path.home() / ".openclaw" / "workspace" / "telegram.env",
    Path.home() / ".openclaw" / "workspace" / ".env",
]

TOKEN_ALIASES = [
    "TELEGRAM_BOT_TOKEN",
    "OPENCLAW_TELEGRAM_BOT_TOKEN",
]

CHAT_ID_ALIASES = [
    "TELEGRAM_CHAT_ID",
    "OPENCLAW_TELEGRAM_CHAT_ID",
]


def load_env_file(path: Optional[str]) -> Optional[Path]:
    if not path:
        return None
    env_path = Path(path).expanduser()
    if not env_path.exists():
        return None
    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return env_path


def load_default_env_files(extra_env_file: str = "") -> list[str]:
    loaded = []
    explicit = load_env_file(extra_env_file)
    if explicit:
        loaded.append(str(explicit))
    for candidate in DEFAULT_ENV_FILES:
        loaded_path = load_env_file(str(candidate))
        if loaded_path:
            loaded.append(str(loaded_path))
    return loaded


def first_present(names: list[str]) -> tuple[Optional[str], Optional[str]]:
    for name in names:
        value = os.getenv(name)
        if value:
            return name, value
    return None, None


def discover_telegram_config(
    token_env: str = "TELEGRAM_BOT_TOKEN",
    chat_id_env: str = "TELEGRAM_CHAT_ID",
    env_file: str = "",
    load_defaults: bool = True,
) -> dict:
    loaded_files = load_default_env_files(env_file) if load_defaults else []
    if not load_defaults and env_file:
        explicit = load_env_file(env_file)
        loaded_files = [str(explicit)] if explicit else []
    token_names = [token_env, *[name for name in TOKEN_ALIASES if name != token_env]]
    chat_names = [chat_id_env, *[name for name in CHAT_ID_ALIASES if name != chat_id_env]]
    token_name, token = first_present(token_names)
    chat_name, chat_id = first_present(chat_names)
    return {
        "available": bool(token and chat_id),
        "token_env": token_name,
        "chat_id_env": chat_name,
        "loaded_env_files": loaded_files,
        "required_env": [token_env, chat_id_env],
    }
