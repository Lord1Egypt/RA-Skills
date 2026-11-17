"""仿真浏览器 RPA 示例常量。"""

from __future__ import annotations

import os
from pathlib import Path

from jiangchang_skill_core import config

SKILL_SLUG = "example-simulator-browser-rpa"
LOG_LOGGER_NAME = "openclaw.skill.example_simulator_browser_rpa"

TARGET_PLATFORM = "sim_batch"
LEASE_HOLDER = "example-simulator-browser-rpa"
LEASE_TTL_SEC = "1800"

DEFAULT_TIMEOUT_MS = 15_000
LOGIN_NAVIGATE_TIMEOUT_MS = 30_000
SUBMIT_NAVIGATE_TIMEOUT_MS = 60_000
DEFAULT_PORTAL_LOGIN_WAIT_SEC = 120

DEFAULT_DEMO_LOGIN_ID = "demo001"
DEFAULT_DEMO_PASSWORD = "demo-password"
DEFAULT_DEMO_CAPTCHA = "0000"
DEFAULT_DEMO_TOKEN_PIN = "123456"

ENV_SIMULATOR_BASE_URL = "SIMULATOR_BASE_URL"
ENV_SIMULATOR_PASSWORD = "SIMULATOR_PASSWORD"
ENV_SIMULATOR_TOKEN_PIN = "SIMULATOR_TOKEN_PIN"
ENV_PORTAL_LOGIN_WAIT_SEC = "PORTAL_LOGIN_WAIT_SEC"

_EXAMPLE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DEMO_APP_PATH = _EXAMPLE_ROOT / "sandbox" / "demo_app.html"


def portal_login_wait_sec() -> int:
    raw = (
        os.getenv(ENV_PORTAL_LOGIN_WAIT_SEC)
        or config.get(ENV_PORTAL_LOGIN_WAIT_SEC)
        or str(DEFAULT_PORTAL_LOGIN_WAIT_SEC)
    )
    try:
        return max(1, int(str(raw).strip()))
    except (TypeError, ValueError):
        return DEFAULT_PORTAL_LOGIN_WAIT_SEC


def resolve_simulator_base_url() -> str:
    env = (os.getenv(ENV_SIMULATOR_BASE_URL) or "").strip()
    if env:
        return env.rstrip("/")
    return DEFAULT_DEMO_APP_PATH.as_uri()
