#!/usr/bin/env python3
"""Internal identity resolution for smyx_payment.

Priority:
1. Workspace data/smyx-api-key.txt (same directory as smyx-common-claw.db)
2. Explicit upstream/internal identity parameter, when supplied by an upstream system
3. smyx_common OpenIdUtil default local user rule:
   - Reuse the first sys_user whose username starts with User_ and length is 11
   - If none exists, create and return User_{6 lowercase hex chars}

The payment skill must not ask users to input internal identity parameters.
smyx_payment must not read skills/smyx_common/scripts/config.yaml for apiKey/internal identity.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Tuple


def workspace_root() -> Path:
    """定位当前 agent 的 workspace 根目录。

    优先级：
      1. 环境变量 OPENCLAW_WORKSPACE
      2. smyx_common.AgentContextUtil.detect_current_agent_workspace()
         （“路径中第一个 /skills/ 之前就是 workspace 根”）
      3. 内建扣底：自己预扫描 __file__ 里首次出现的 /skills/，
         删除尾部 skills/... 后就是 workspace 根（避免 dirname 层数写死）
    """
    env_workspace = os.environ.get("OPENCLAW_WORKSPACE")
    if env_workspace:
        return Path(env_workspace)

    # 优先复用 smyx_common 的统一探测，保持与 vendored util.py 一致
    try:
        from skills.smyx_common.scripts.util import AgentContextUtil

        context = AgentContextUtil.detect_current_agent_workspace()
        root = context.get("workspace_root") if isinstance(context, dict) else None
        if root:
            return Path(root)
    except Exception:
        pass

    # 内建扣底：无需依赖 smyx_common，用同样的算法扫描 __file__
    current_path = str(Path(__file__).resolve())
    sep = os.sep
    marker = sep + "skills" + sep
    idx = current_path.find(marker)
    if idx > 0:
        return Path(current_path[:idx])

    # 真的什么都没匹配到（不可能发生），返回当前文件所在目录向上一层兄弟。
    return Path(__file__).resolve().parent


def api_key_file_path() -> Path:
    """Return workspace data/smyx-api-key.txt, colocated with smyx-common-claw.db."""
    return workspace_root() / "data" / "smyx-api-key.txt"


def read_api_key_file() -> Optional[str]:
    path = api_key_file_path()
    if not path.exists():
        return None
    try:
        value = path.read_text(encoding="utf-8").strip()
    except Exception:
        return None
    return value or None


def _set_request_layer_api_key(value: str) -> None:
    """Feed X-Api-Key into shared request layers when identity comes from api-key file."""
    try:
        from .config import ApiEnum
        ApiEnum.API_SECRET_KEY = value
    except Exception:
        pass
    try:
        from skills.smyx_common.scripts.config import ApiEnum as CommonApiEnum
        CommonApiEnum.API_SECRET_KEY = value
    except Exception:
        pass


def _is_sensitive_identifier(value: str) -> bool:
    """Check if value looks like a sensitive API key/token."""
    if not value or not isinstance(value, str):
        return False
    # User_xxx format is safe to display
    if value.startswith("User_") and len(value) == 11:
        return False
    # AK/SK format
    if value.lower().startswith(("ak_", "sk_", "pk_", "api_", "token_")):
        return True
    # Long mixed identifiers are treated as sensitive
    return len(value) >= 24 and any(c.isalpha() for c in value) and any(c.isdigit() for c in value)


def get_or_create_default_recharge_account() -> str:
    """Return a reusable local default recharge account via smyx_common rules.

    Rule source: skills.smyx_common.scripts.util.OpenIdUtil
    - Query UserDao for the first non-deleted username matching User_ + 6 chars
      (total length 11)
    - If not found, create User_{6 lowercase hex chars} in smyx-common-claw.db
    """
    from skills.smyx_common.scripts.util import OpenIdUtil

    return OpenIdUtil.get_or_create_default_open_id()


def _lookup_username_by_api_key(api_key: str) -> Optional[str]:
    """本地 smyx-common-claw.db 中用 API Key（realname）反查真实 username。

    RequestUtil.http_request 里 _get_or_create_user 已经把后端返回的
    username 保存到 sys_user。UserDao.get_by_username 内部用
    (username == x OR realname == x) AND 未删除的 OR 匹配，
    因此直接传入 api_key 即可命中 realname 列，无需自己拼 SQL。
    """
    if not api_key or not isinstance(api_key, str):
        return None
    try:
        from skills.smyx_common.scripts.dao import UserDao

        user = UserDao().get_by_username(api_key)
        return user.username if user and user.username else None
    except Exception:
        return None


def get_payment_card_display_account() -> str:
    """支付卡片上展示的账户名。

    展示优先级：
      1. 若为 API Key→本地 sys_user.realname 反查 username 展示真实账号；
      2. 未绑定到 username 时才对 API Key 脱敏展示；
      3. 非敏感标识符（如 User_xxx）直接原样展示。
    """
    account, source = resolve_recharge_account(None)

    # 来源为 api-key 文件时，优先反查真实 username
    if source == "api_key_file":
        real_username = _lookup_username_by_api_key(account)
        if real_username:
            return real_username
        # 未绑定到 username 时才脱敏，避免直接回显完整存根
        return f"{account[:8]}..."

    # 其他来源（explicit / default_local_user）
    if _is_sensitive_identifier(account):
        return f"{account[:8]}..."

    return account


def resolve_recharge_account(explicit_internal_account: Optional[str] = None) -> Tuple[str, str]:
    """Resolve the account used by payment order creation.

    严格按模块 docstring 声明的优先级解析：
      1. explicit（显式传入）
      2. workspace data/smyx-api-key.txt（若存在则视为已完成身份关联，最高业务优先级）
      3. 本地默认 User_xxx 账户（真正的兜底）

    Returns:
        (account, source): source is "explicit" | "api_key_file" | "default_local_user".
    """
    # 1. 显式传入的账户
    if explicit_internal_account and str(explicit_internal_account).strip():
        return str(explicit_internal_account).strip(), "explicit"

    # 2. smyx-api-key.txt（按 docstring 契约，优先级高于本地默认 User_xxx）
    api_key = read_api_key_file()
    if api_key:
        _set_request_layer_api_key(api_key)
        return api_key, "api_key_file"

    # 3. 兜底：本地默认 User_xxx 账户
    return get_or_create_default_recharge_account(), "default_local_user"


def resolve_open_id(explicit_open_id: Optional[str] = None) -> Tuple[str, str]:
    """Backward-compatible wrapper for existing internal callers."""
    return resolve_recharge_account(explicit_open_id)


def require_open_id(explicit_open_id: Optional[str] = None) -> str:
    """Backward-compatible wrapper: always returns an account, never asks the user."""
    account, _source = resolve_recharge_account(explicit_open_id)
    return account
