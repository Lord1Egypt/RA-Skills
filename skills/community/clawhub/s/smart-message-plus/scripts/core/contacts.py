#!/usr/bin/env python3
"""smart-message-plus: contact aliases (single/members) + group aliases."""
from __future__ import annotations

import re

from . import config as C

# wecom webhook key（UUID 形态）
_WECOM_KEY_RE = re.compile(r"^[0-9a-fA-F-]{30,50}$")


def _empty() -> dict:
    return {"contacts": {}, "groups": {}}


def load() -> dict:
    data = C.load_json("contacts.json", _empty())
    data.setdefault("contacts", {})
    data.setdefault("groups", {})
    return data


def save(data: dict) -> None:
    C.save_json("contacts.json", data, secret=True)


def resolve_contact(alias: str, provider: str) -> list[str] | None:
    """Resolve a contact alias -> list of provider-native user ids.
    Returns None if alias unknown. Raises ValueError if alias exists but has
    no id for this provider."""
    data = load()
    ent = data["contacts"].get(alias)
    if ent is None:
        return None
    if ent.get("type") == "single":
        uid = (ent.get("ids") or {}).get(provider, "")
        if not uid:
            raise ValueError(
                f"联系人「{alias}」没有 {provider} 的标识。"
                f"用 --save-contact 补充，如: --save-contact {alias} single \"{provider}:<用户ID>\""
            )
        return [uid]
    if ent.get("type") == "members":
        members = ent.get("members") or []
        out: list[str] = []
        missing: list[str] = []
        for m in members:
            sub = resolve_contact(m, provider)
            if sub is None:
                missing.append(m)
            else:
                out.extend(sub)
        if missing:
            raise ValueError(
                f"多人别名「{alias}」中的成员未定义: {', '.join(missing)}"
            )
        return out
    raise ValueError(f"联系人「{alias}」类型异常: {ent.get('type')}")


def resolve_group(alias_or_id: str, provider: str) -> str | None:
    """Resolve group alias -> chat id. If input already looks like a native
    chat id, return as-is. Returns None if unknown alias."""
    if provider == "dingtalk" and (alias_or_id.startswith("cid") or alias_or_id.startswith("chat")):
        return alias_or_id
    if provider == "feishu" and alias_or_id.startswith("oc_"):
        return alias_or_id
    # wecom webhook 模式：完整 webhook URL 或裸 key（UUID 形态）直接放行
    if provider == "wecom" and (
        alias_or_id.startswith("http") or _WECOM_KEY_RE.match(alias_or_id)
    ):
        return alias_or_id
    data = load()
    ent = data["groups"].get(alias_or_id)
    if ent is None:
        return None
    if ent.get("provider") and ent["provider"] != provider:
        raise ValueError(
            f"群「{alias_or_id}」属于 {ent['provider']}，当前 provider 是 {provider}。"
            f"请加 --provider {ent['provider']} 或换群。"
        )
    return ent.get("chat_id", "")


def save_contact(alias: str, ctype: str, value: str, note: str = "") -> dict:
    """value formats:
    single : "dingtalk:0144...,feishu:ou_xxx"  (comma-separated provider:id)
    members: "alias1,alias2,alias3"
    """
    data = load()
    if ctype == "single":
        ids = {}
        for pair in value.split(","):
            pair = pair.strip()
            if not pair:
                continue
            if ":" not in pair:
                raise ValueError(
                    f"single 联系人格式: provider:id（如 dingtalk:0144xxx），收到: {pair}"
                )
            prov, uid = pair.split(":", 1)
            prov, uid = prov.strip(), uid.strip()
            if prov not in ("dingtalk", "feishu", "wecom"):
                raise ValueError(f"未知 provider: {prov}")
            ids[prov] = uid
        if not ids:
            raise ValueError("至少提供一个 provider:id")
        ent = {"type": "single", "ids": ids}
    elif ctype == "members":
        members = [m.strip() for m in value.split(",") if m.strip()]
        if not members:
            raise ValueError("members 列表为空")
        ent = {"type": "members", "members": members}
    else:
        raise ValueError(f"不支持的联系人类型: {ctype}（支持 single/members）")
    if note:
        ent["note"] = note
    data["contacts"][alias] = ent
    save(data)
    return ent


def save_group(alias: str, provider: str, chat_id: str, note: str = "") -> dict:
    data = load()
    ent = {"provider": provider, "chat_id": chat_id}
    if note:
        ent["note"] = note
    data["groups"][alias] = ent
    save(data)
    return ent


def remove(alias: str) -> bool:
    data = load()
    removed = False
    if alias in data["contacts"]:
        del data["contacts"][alias]
        removed = True
    if alias in data["groups"]:
        del data["groups"][alias]
        removed = True
    if removed:
        save(data)
    return removed


def list_all() -> dict:
    return load()
