"""account-manager CLI 集成（仅 subprocess，不 import 兄弟 skill 内部模块）。"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from typing import Any, Dict, List, Optional

from jiangchang_skill_core.runtime_env import get_sibling_skills_root

from util.constants import LEASE_HOLDER, LEASE_TTL_SEC, TARGET_PLATFORM
from util.logging import mask_text

logger = logging.getLogger(__name__)

PLACEHOLDER_PLATFORM = TARGET_PLATFORM

ACCOUNT_SETUP_MESSAGE = (
    f"未找到可用的 {PLACEHOLDER_PLATFORM} 账号，所以还没有打开浏览器。"
    f"请先在 account-manager 中添加 platform={PLACEHOLDER_PLATFORM}、"
    "status=active、带 profile_dir 的账号后重新运行。"
)

LEASE_BUSY_MESSAGE = "目标平台账号当前被其他任务占用，请等待释放租约后重试。"


class AccountManagerError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def mask_login_id(login_id: str) -> str:
    return mask_text(login_id)


def _resolve_account_manager_main() -> str:
    """解析 account-manager CLI 入口路径。

    优先级：ACCOUNT_MANAGER_ROOT → get_sibling_skills_root → 开发机兜底。
    """
    env_root = (os.getenv("ACCOUNT_MANAGER_ROOT") or "").strip()
    if env_root and os.path.isfile(os.path.join(env_root, "scripts", "main.py")):
        return os.path.join(os.path.abspath(env_root), "scripts", "main.py")

    scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_root = get_sibling_skills_root(scripts_dir)
    candidate = os.path.join(skills_root, "account-manager", "scripts", "main.py")
    if os.path.isfile(candidate):
        return candidate

    dev = r"D:\OpenClaw\client-commons\account-manager\scripts\main.py"
    if os.path.isfile(dev):
        return dev

    raise AccountManagerError(
        "ACCOUNT_NOT_FOUND",
        "未找到 account-manager，请配置 ACCOUNT_MANAGER_ROOT 或安装 account-manager 技能。",
    )


def _parse_last_json(stdout: str) -> Any:
    lines = [ln.strip() for ln in (stdout or "").splitlines() if ln.strip()]
    for raw in reversed(lines):
        if raw.startswith("ERROR:"):
            continue
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            continue
    raise AccountManagerError("UNKNOWN_ERROR", "stdout 中没有可解析的 JSON。")


def _run_argv(argv_suffix: List[str]) -> subprocess.CompletedProcess[str]:
    main_py = _resolve_account_manager_main()
    env = os.environ.copy()
    return subprocess.run(
        [sys.executable, main_py, *argv_suffix],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )


def _normalize_error_code(raw: str) -> str:
    code = (raw or "").strip()
    if code.startswith("ERROR:"):
        code = code[6:]
    return code


def _validate_pick_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("success") is False:
        err = payload.get("error") if isinstance(payload.get("error"), dict) else {}
        code = _normalize_error_code(str(err.get("code") or ""))
        message = str(err.get("message") or "")
        if code == "LEASE_CONFLICT" or "LEASE_CONFLICT" in code:
            raise AccountManagerError("LEASE_CONFLICT", LEASE_BUSY_MESSAGE)
        if code in ("NO_ACCOUNT", "ACCOUNT_NOT_FOUND") or "NO_ACCOUNT" in code:
            raise AccountManagerError("NO_ACCOUNT", message or "没有可用账号。")
        raise AccountManagerError(code or "PICK_WEB_FAILED", message or "pick-web 失败。")

    if not isinstance(payload, dict):
        raise AccountManagerError("ACCOUNT_NOT_FOUND", "pick-web 返回格式异常。")
    if not payload.get("profile_dir"):
        raise AccountManagerError("ACCOUNT_NOT_FOUND", "pick-web 返回的账号缺少 profile_dir。")
    return payload


def _pick_web_with_lease(platform: str) -> Dict[str, Any]:
    proc = _run_argv(
        [
            "account",
            "pick-web",
            "--platform",
            platform,
            "--lease",
            "--holder",
            LEASE_HOLDER,
            "--ttl-sec",
            LEASE_TTL_SEC,
        ]
    )
    out = proc.stdout or ""
    if proc.returncode != 0 and not out.strip():
        raise AccountManagerError(
            "PICK_WEB_FAILED",
            (proc.stderr or "").strip() or "pick-web 子进程失败",
        )
    payload = _parse_last_json(out)
    if isinstance(payload, dict) and payload.get("success") is False:
        return _validate_pick_payload(payload)
    if not isinstance(payload, dict):
        raise AccountManagerError("ACCOUNT_NOT_FOUND", "pick-web 返回格式异常。")
    return payload


def _pick_by_id(platform: str, account_id: int) -> Dict[str, Any]:
    proc = _run_argv(["account", "get", str(account_id)])
    out = proc.stdout or ""
    if proc.returncode != 0 or out.startswith("ERROR:"):
        raise AccountManagerError("ACCOUNT_NOT_FOUND", f"指定账号 {account_id} 不存在或获取失败。")
    raw = _parse_last_json(out)
    if isinstance(raw, dict) and "data" in raw and isinstance(raw["data"], dict):
        data = raw["data"]
    elif isinstance(raw, dict):
        data = raw
    else:
        raise AccountManagerError("ACCOUNT_NOT_FOUND", "account get 返回非对象 JSON。")

    platform_key = str(data.get("platform_key") or "").lower()
    if platform_key != platform.lower():
        raise AccountManagerError(
            "ACCOUNT_NOT_FOUND",
            f"账号 {account_id} 不是 {platform} 平台账号。",
        )
    profile_dir = str(data.get("profile_dir") or "").strip()
    if not profile_dir:
        raise AccountManagerError("ACCOUNT_NOT_FOUND", f"账号 {account_id} 缺少 profile_dir。")
    data["profile_dir"] = profile_dir
    data["lease_token"] = ""
    return data


def pick_web_account(platform: str, account_id: Optional[str] = None) -> dict:
    """获取网页账号（profile_dir + lease_token）。"""
    platform_key = (platform or PLACEHOLDER_PLATFORM).strip() or PLACEHOLDER_PLATFORM

    if account_id:
        try:
            aid = int(account_id)
        except (TypeError, ValueError):
            raise AccountManagerError("ACCOUNT_NOT_FOUND", f"账号 ID 无效：{account_id}")
        return _pick_by_id(platform_key, aid)

    try:
        return _pick_web_with_lease(platform_key)
    except AccountManagerError as exc:
        if exc.code in ("NO_ACCOUNT", "ACCOUNT_NOT_FOUND") or "NO_ACCOUNT" in exc.code:
            raise AccountManagerError("ACCOUNT_SETUP_REQUIRED", ACCOUNT_SETUP_MESSAGE) from exc
        raise


def release_lease(lease_token: Optional[str]) -> None:
    token = (lease_token or "").strip()
    if not token:
        return
    try:
        proc = _run_argv(["lease", "release", token])
        if proc.returncode != 0:
            logger.warning("lease_release_failed stdout=%s", (proc.stdout or "").strip())
    except Exception:
        logger.warning("lease_release_exception", exc_info=True)
