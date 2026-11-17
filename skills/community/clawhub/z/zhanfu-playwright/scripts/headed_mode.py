"""站斧 Playwright 强制有界面模式（禁止无头）。"""

from __future__ import annotations

import os

# 小龙虾 / CI 等环境可能注入的无头相关变量
_HEADLESS_ENV_KEYS = (
    "PLAYWRIGHT_HEADLESS",
    "HEADLESS",
    "PW_HEADLESS",
    "CHROME_HEADLESS",
)


def ensure_headed_mode() -> None:
    """脚本入口调用：强制 Playwright 不使用无头模式。"""
    for key in _HEADLESS_ENV_KEYS:
        os.environ[key] = "0"


def headed_launch_options() -> dict:
    """若必须 chromium.launch()，使用此参数（仍优先 connect_over_cdp）。"""
    ensure_headed_mode()
    return {"headless": False}


def assert_not_headless_launch(headless: bool | None) -> None:
    if headless:
        raise RuntimeError("站斧自动化禁止使用无头模式（headless=True）")
