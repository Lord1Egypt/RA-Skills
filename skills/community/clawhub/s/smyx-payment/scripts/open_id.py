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
    env_workspace = os.environ.get("OPENCLAW_WORKSPACE")
    if env_workspace:
        return Path(env_workspace)
    # /root/.openclaw/workspace/skills/smyx_payment/scripts/open_id.py -> workspace root = parents[3]
    return Path(__file__).resolve().parents[3]


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


def get_payment_card_display_account() -> str:
    """Return the plaintext account that must be shown on payment cards.

    与 resolve_recharge_account 逻辑一致，确保用户看到的账户就是实际充值的账户

    Returns:
        支付卡片上显示的账户名
    """
    account, source = resolve_recharge_account(None)

    # 敏感标识符脱敏显示（正常情况下不应该走到这里，因为优先使用 User_xxx）
    if _is_sensitive_identifier(account):
        # 显示前8位 + ...，既标识又保护隐私
        return f"{account[:8]}..."

    # User_xxx 或手机号直接显示
    return account


def resolve_recharge_account(explicit_internal_account: Optional[str] = None) -> Tuple[str, str]:
    """Resolve the account used by payment order creation.

    🔴 关键规则：优先使用 User_xxx 格式的本地充值账户，而非 API Key
    - API Key 仅用于请求层鉴权，不作为用户账户标识
    - User_xxx 是用户可识别的本地充值账户

    Returns:
        (account, source): source is "default_local_user" | "explicit" | "api_key_file".
    """
    # 1. 优先使用显式传入的账户
    if explicit_internal_account and str(explicit_internal_account).strip():
        return str(explicit_internal_account).strip(), "explicit"

    # 2. 优先获取本地默认 User_xxx 账户（这是用户看到的充值账户）
    try:
        from skills.smyx_common.scripts.util import OpenIdUtil
        user_account = OpenIdUtil.get_or_create_default_open_id()
        if user_account and user_account.startswith("User_"):
            # 同时设置 API Key 到请求层（如果有）
            api_key = read_api_key_file()
            if api_key:
                _set_request_layer_api_key(api_key)
            return user_account, "default_local_user"
    except Exception:
        pass

    # 3. 降级方案：如果获取 User_xxx 失败，再使用 API Key
    api_key = read_api_key_file()
    if api_key:
        _set_request_layer_api_key(api_key)
        return api_key, "api_key_file"

    # 4. 最终兜底：创建默认 User_xxx 账户
    return get_or_create_default_recharge_account(), "default_local_user"


def resolve_open_id(explicit_open_id: Optional[str] = None) -> Tuple[str, str]:
    """Backward-compatible wrapper for existing internal callers."""
    return resolve_recharge_account(explicit_open_id)


def require_open_id(explicit_open_id: Optional[str] = None) -> str:
    """Backward-compatible wrapper: always returns an account, never asks the user."""
    account, _source = resolve_recharge_account(explicit_open_id)
    return account
