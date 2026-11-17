#!/usr/bin/env python3
"""smart-message-plus: multi-account management (cross-provider) + token cache."""
from __future__ import annotations

import time

from . import config as C

PROVIDERS = ("dingtalk", "feishu", "wecom")

# provider -> required + optional credential fields
PROVIDER_FIELDS = {
    "dingtalk": {
        "required": ["app_key", "app_secret"],
        "optional": ["robot_code", "agent_id"],
    },
    "feishu": {
        "required": ["app_id", "app_secret"],
        "optional": [],
    },
    # wecom 当前为群机器人 webhook 模式：无需企业凭证。
    # webhook_url 可选（作为默认群）；群 webhook 推荐用 --save-group 管理。
    # 预留 wecom-app 模式字段：corp_id / corp_secret / agent_id（需企业可信 IP）。
    "wecom": {
        "required": [],
        "optional": ["webhook_url", "corp_id", "corp_secret", "agent_id"],
    },
}


def _empty() -> dict:
    return {"default": "", "accounts": {}}


def load() -> dict:
    return C.load_json("accounts.json", _empty())


def save(cfg: dict) -> None:
    C.save_json("accounts.json", cfg, secret=True)


def get(slug_or_name: str = "", provider: str = "") -> tuple[str, dict]:
    """Resolve account by slug/name; fall back to default, then to the only
    account of the given provider. Returns (slug, account). Raises ValueError."""
    cfg = load()
    accounts = cfg.get("accounts", {})
    if not accounts:
        raise ValueError(
            "未配置任何账号。先执行 --save-account 保存钉钉/飞书应用凭证。"
        )
    if slug_or_name:
        if slug_or_name in accounts:
            return slug_or_name, accounts[slug_or_name]
        for slug, acc in accounts.items():
            if acc.get("name") == slug_or_name:
                return slug, acc
        raise ValueError(f"账号不存在: {slug_or_name}（--list-accounts 查看）")
    if provider:
        matches = [(s, a) for s, a in accounts.items() if a.get("provider") == provider]
        default_slug = cfg.get("default", "")
        if default_slug in accounts and accounts[default_slug].get("provider") == provider:
            return default_slug, accounts[default_slug]
        if len(matches) == 1:
            return matches[0]
        if not matches:
            raise ValueError(f"没有 provider={provider} 的账号（--list-accounts 查看）")
        raise ValueError(
            f"provider={provider} 有多个账号（{', '.join(s for s, _ in matches)}），请用 --account 指定"
        )
    default_slug = cfg.get("default", "")
    if default_slug and default_slug in accounts:
        return default_slug, accounts[default_slug]
    if len(accounts) == 1:
        slug = next(iter(accounts))
        return slug, accounts[slug]
    raise ValueError("存在多个账号且未设置默认，请用 --account 指定或 --set-default-account 设置")


def save_account(slug: str, provider: str, name: str, creds: dict) -> None:
    if provider not in PROVIDERS:
        raise ValueError(f"不支持的 provider: {provider}（支持: {', '.join(PROVIDERS)}）")
    spec = PROVIDER_FIELDS[provider]
    missing = [f for f in spec["required"] if not creds.get(f)]
    if missing:
        raise ValueError(f"缺少必填凭证字段: {', '.join(missing)}")
    cfg = load()
    entry = {"provider": provider, "name": name or slug}
    for f in spec["required"] + spec["optional"]:
        if creds.get(f):
            entry[f] = creds[f]
    # dingtalk: robot_code defaults to app_key
    if provider == "dingtalk" and not entry.get("robot_code"):
        entry["robot_code"] = entry["app_key"]
    cfg.setdefault("accounts", {})[slug] = entry
    if not cfg.get("default"):
        cfg["default"] = slug
    save(cfg)


def remove_account(slug: str) -> bool:
    cfg = load()
    if slug not in cfg.get("accounts", {}):
        return False
    del cfg["accounts"][slug]
    if cfg.get("default") == slug:
        cfg["default"] = next(iter(cfg["accounts"]), "")
    save(cfg)
    _drop_token(slug)
    return True


def set_default(slug_or_name: str) -> str:
    slug, _ = get(slug_or_name)
    cfg = load()
    cfg["default"] = slug
    save(cfg)
    return slug


def list_accounts() -> list[dict]:
    cfg = load()
    out = []
    for slug, acc in cfg.get("accounts", {}).items():
        out.append(
            {
                "slug": slug,
                "provider": acc.get("provider"),
                "name": acc.get("name"),
                "is_default": slug == cfg.get("default"),
                "key_masked": C.mask_secret(
                    acc.get("app_key") or acc.get("app_id") or ""
                ),
            }
        )
    return out


# ---------------- token cache ----------------

_EARLY_REFRESH = 300  # refresh 5 min before expiry


def get_cached_token(slug: str) -> str:
    cache = C.load_json("token_cache.json", {})
    ent = cache.get(slug)
    if ent and ent.get("expires_at", 0) > time.time() + _EARLY_REFRESH:
        return ent.get("token", "")
    return ""


def store_token(slug: str, token: str, expires_in: int) -> None:
    cache = C.load_json("token_cache.json", {})
    cache[slug] = {"token": token, "expires_at": time.time() + int(expires_in)}
    C.save_json("token_cache.json", cache, secret=True)


def _drop_token(slug: str) -> None:
    cache = C.load_json("token_cache.json", {})
    if slug in cache:
        del cache[slug]
        C.save_json("token_cache.json", cache, secret=True)


def invalidate_token(slug: str) -> None:
    _drop_token(slug)
