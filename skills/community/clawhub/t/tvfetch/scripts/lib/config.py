"""
Hierarchical configuration resolver for tvfetch skill.

Resolution order for TV_AUTH_TOKEN (highest to lowest):
  1. --token CLI flag
  2. TV_AUTH_TOKEN environment variable
  3. ~/.tvfetch/.env file
  4. keyring (if installed): keyring.get_password("tvfetch", "auth_token")
  5. .env in current working directory
  6. Anonymous fallback: "unauthorized_user_token"

Usage:
  python config.py --show          # Print resolved config
  python config.py --check-auth-quiet  # One-line auth status for hooks
"""

from __future__ import annotations

import base64
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

ANONYMOUS_TOKEN = "unauthorized_user_token"
DEFAULT_TVFETCH_DIR = Path.home() / ".tvfetch"
DEFAULT_CACHE_PATH = DEFAULT_TVFETCH_DIR / "cache.db"
DEFAULT_ENV_PATH = DEFAULT_TVFETCH_DIR / ".env"


@dataclass
class Config:
    """Resolved tvfetch configuration."""

    auth_token: str
    auth_source: str       # "cli_flag" | "env" | ".env" | "keyring" | "cwd_env" | "anonymous"
    cache_path: Path
    mock_mode: bool
    log_level: str
    proxy_url: str | None
    fallback_enabled: bool
    timeout: int

    @property
    def is_anonymous(self) -> bool:
        return self.auth_token == ANONYMOUS_TOKEN


def _load_env_file(path: Path) -> dict[str, str]:
    """Parse a simple KEY=VALUE .env file. Ignores comments and blank lines."""
    result: dict[str, str] = {}
    if not path.is_file():
        return result
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, _, val = line.partition("=")
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def _resolve_auth_token(cli_token: str | None = None) -> tuple[str, str]:
    """Return (token, source) by walking the resolution chain."""
    # 1. CLI flag
    if cli_token:
        return cli_token, "cli_flag"

    # 2. Environment variable
    env_token = os.environ.get("TV_AUTH_TOKEN", "").strip()
    if env_token and env_token != ANONYMOUS_TOKEN:
        return env_token, "env"

    # 3. ~/.tvfetch/.env
    home_env = _load_env_file(DEFAULT_ENV_PATH)
    if home_env.get("TV_AUTH_TOKEN"):
        return home_env["TV_AUTH_TOKEN"], ".env"

    # 4. Keyring (optional)
    try:
        import keyring
        kr_token = keyring.get_password("tvfetch", "auth_token")
        if kr_token:
            return kr_token, "keyring"
    except (ImportError, Exception):
        pass

    # 5. .env in current working directory
    cwd_env = _load_env_file(Path.cwd() / ".env")
    if cwd_env.get("TV_AUTH_TOKEN"):
        return cwd_env["TV_AUTH_TOKEN"], "cwd_env"

    # 6. Anonymous fallback
    return ANONYMOUS_TOKEN, "anonymous"


def validate_token(token: str) -> tuple[bool, str]:
    """
    Check JWT structure and expiry without making a network call.
    Returns (is_valid, reason_string).
    """
    if token == ANONYMOUS_TOKEN:
        return True, "anonymous"

    parts = token.split(".")
    if len(parts) != 3:
        return False, "not a valid JWT (expected 3 dot-separated parts)"

    try:
        padded = parts[1] + "=" * (-len(parts[1]) % 4)
        payload = json.loads(base64.b64decode(padded))
        exp = payload.get("exp")
        if exp and exp < time.time():
            return False, f"expired at {datetime.fromtimestamp(exp).isoformat()}"
        return True, "valid"
    except Exception as exc:
        return False, f"decode error: {exc}"


def get_config(cli_token: str | None = None) -> Config:
    """Build fully resolved Config from all sources."""
    token, source = _resolve_auth_token(cli_token)

    # Load additional settings from env or .env
    home_env = _load_env_file(DEFAULT_ENV_PATH)

    cache_path = Path(
        os.environ.get("TVFETCH_CACHE_PATH", "")
        or home_env.get("TVFETCH_CACHE_PATH", "")
        or str(DEFAULT_CACHE_PATH)
    )

    return Config(
        auth_token=token,
        auth_source=source,
        cache_path=cache_path,
        mock_mode=os.environ.get("TVFETCH_MOCK", home_env.get("TVFETCH_MOCK", "0")) == "1",
        log_level=os.environ.get("TVFETCH_LOG_LEVEL", home_env.get("TVFETCH_LOG_LEVEL", "WARNING")),
        proxy_url=os.environ.get("TVFETCH_PROXY", home_env.get("TVFETCH_PROXY", "")) or None,
        fallback_enabled=os.environ.get(
            "TVFETCH_FALLBACK", home_env.get("TVFETCH_FALLBACK", "true")
        ).lower() in ("true", "1", "yes"),
        timeout=int(os.environ.get("TVFETCH_TIMEOUT", home_env.get("TVFETCH_TIMEOUT", "120"))),
    )


def show_config(config: Config | None = None) -> None:
    """Print resolved config to stdout."""
    cfg = config or get_config()
    valid, reason = validate_token(cfg.auth_token)
    token_preview = cfg.auth_token[:20] + "..." if len(cfg.auth_token) > 20 else cfg.auth_token

    print("=== TVFETCH CONFIG ===")
    print(f"AUTH_MODE: {'anonymous' if cfg.is_anonymous else 'token'}")
    print(f"AUTH_SOURCE: {cfg.auth_source}")
    print(f"TOKEN_PREVIEW: {token_preview}")
    print(f"TOKEN_VALID: {valid} ({reason})")
    print(f"CACHE_PATH: {cfg.cache_path}")
    print(f"MOCK_MODE: {cfg.mock_mode}")
    print(f"FALLBACK: {cfg.fallback_enabled}")
    print(f"TIMEOUT: {cfg.timeout}s")
    if cfg.proxy_url:
        print(f"PROXY: {cfg.proxy_url}")
    print("=== END ===")


def check_auth_quiet() -> None:
    """One-line auth status for hook scripts."""
    token, source = _resolve_auth_token()
    if token == ANONYMOUS_TOKEN:
        print("TVFETCH AUTH: anonymous (daily/weekly/monthly get full history — set TV_AUTH_TOKEN for more intraday bars)")
    else:
        valid, reason = validate_token(token)
        if valid:
            print(f"TVFETCH AUTH: token found (source: {source})")
        else:
            print(f"TVFETCH AUTH: token EXPIRED ({reason}) — run: python auth_mgr.py set NEW_TOKEN")


if __name__ == "__main__":
    if "--show" in sys.argv:
        show_config()
    elif "--check-auth-quiet" in sys.argv:
        check_auth_quiet()
    else:
        show_config()
