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

    This value is intentionally the local default sys_user.username resolved
    through smyx_common UserDao rules, not any sensitive stored credential.
    """
    return get_or_create_default_recharge_account()


def resolve_recharge_account(explicit_internal_account: Optional[str] = None) -> Tuple[str, str]:
    """Resolve the account used by payment order creation.

    Returns:
        (account, source): source is "api_key_file" | "explicit" | "default_local_user".
    """
    api_key = read_api_key_file()
    if api_key:
        _set_request_layer_api_key(api_key)
        return api_key, "api_key_file"

    if explicit_internal_account and str(explicit_internal_account).strip():
        return str(explicit_internal_account).strip(), "explicit"

    return get_or_create_default_recharge_account(), "default_local_user"


def resolve_open_id(explicit_open_id: Optional[str] = None) -> Tuple[str, str]:
    """Backward-compatible wrapper for existing internal callers."""
    return resolve_recharge_account(explicit_open_id)


def require_open_id(explicit_open_id: Optional[str] = None) -> str:
    """Backward-compatible wrapper: always returns an account, never asks the user."""
    account, _source = resolve_recharge_account(explicit_open_id)
    return account
