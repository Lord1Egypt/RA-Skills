from __future__ import annotations

import getpass
import sys
from typing import Any

import requests

from toupiaoya.config import load_config, save_config, token_from_config
from toupiaoya.constants import CONFIG_PATH, CONFIG_TOKEN_KEY, DEFAULT_TIMEOUT, PASSPORT_PROFILE_URL


def cmd_login() -> None:
    """交互式登录：将 X-Openclaw-Token 写入 ~/.toupiaoya/config.json（推荐）。"""
    existing = load_config()
    print("交互式登录：令牌输入时不会回显。", file=sys.stderr)
    token = getpass.getpass("X-Openclaw-Token: ").strip()
    if not token:
        print("未输入令牌，已取消。", file=sys.stderr)
        sys.exit(1)
    merged = dict(existing)
    merged[CONFIG_TOKEN_KEY] = token
    save_config(merged)
    print(f"已保存至 {CONFIG_PATH}（{CONFIG_TOKEN_KEY}）。", file=sys.stderr)


def auth_status(access_token: str) -> dict[str, Any]:
    headers = {"X-Openclaw-Token": access_token}
    res = requests.get(url=PASSPORT_PROFILE_URL, headers=headers, timeout=DEFAULT_TIMEOUT)
    if res.status_code != 200:
        return {"success": False, "code": 1002, "msg": "认证失败"}
    return {"success": True, "code": 200, "msg": "认证成功"}


def resolve_token(cli_token: str | None) -> str:
    cfg = load_config()
    return (cli_token or "").strip() or token_from_config(cfg)
