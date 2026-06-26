#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared runtime helpers for soyoung-clinic-tools."""

from __future__ import annotations

import hashlib
import json
import os
import re
import secrets
import stat
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Optional


STATE_ROOT = Path.home() / ".openclaw" / "state" / "soyoung-clinic-tools" / "workspaces"
WORKSPACE_ENV_KEYS = (
    "SOYOUNG_WORKSPACE_KEY",
    "OPENCLAW_WORKSPACE_KEY",
    "OPENCLAW_WORKSPACE_ID",
    "OPENCLAW_AGENT_ID",
    "OPENCLAW_WORKSPACE",
    "OPENCLAW_WORKSPACE_DIR",
)
PROTECTED_APPOINTMENT_ACTIONS = {
    "appointment_query",
    "appointment_create",
    "appointment_update",
    "appointment_cancel",
}


class SoyoungRuntimeError(RuntimeError):
    """Raised when the caller violates runtime constraints."""


@dataclass
class MessageContext:
    workspace_key: str
    chat_type: str
    chat_id: str
    sender_open_id: str
    sender_name: Optional[str]
    mentions: list[str]
    tenant_key: Optional[str] = None
    message_id: Optional[str] = None


@dataclass
class StatePaths:
    workspace_key: str
    workspace_dir: Path
    binding_file: Path
    api_key_file: Path
    location_file: Path
    pending_dir: Path
    audit_dir: Path


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_now() -> str:
    return utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def gen_api_request_id() -> str:
    ts = utc_now().strftime("%Y%m%dT%H%M%S")
    rand = secrets.token_hex(6).upper()
    return f"SY-{ts}-{rand}"


def read_debug_mode(paths: "StatePaths") -> bool:
    debug_file = paths.workspace_dir / "debug_mode"
    if debug_file.exists():
        return debug_file.read_text().strip().lower() in ("1", "true", "yes")
    # 与 load_api_key 保持一致：当前 workspace 无配置时兜底读 default workspace
    if paths.workspace_key != "default":
        default_debug_file = STATE_ROOT / "default" / "debug_mode"
        if default_debug_file.exists():
            return default_debug_file.read_text().strip().lower() in ("1", "true", "yes")
    return os.environ.get("SOYOUNG_DEBUG", "false").lower() in ("1", "true", "yes")


def write_debug_mode(paths: "StatePaths", enabled: bool) -> None:
    paths.workspace_dir.mkdir(parents=True, exist_ok=True)
    (paths.workspace_dir / "debug_mode").write_text("true" if enabled else "false")


DEFAULT_API_BASE_URL = "https://skill.soyoung.com"


def read_api_base_url(paths: "StatePaths") -> str:
    url_file = paths.workspace_dir / "api_base_url"
    if url_file.exists():
        return url_file.read_text().strip()
    return DEFAULT_API_BASE_URL


def write_api_base_url(paths: "StatePaths", url: str) -> None:
    paths.workspace_dir.mkdir(parents=True, exist_ok=True)
    (paths.workspace_dir / "api_base_url").write_text(url)


def reset_api_base_url(paths: "StatePaths") -> None:
    url_file = paths.workspace_dir / "api_base_url"
    if url_file.exists():
        url_file.unlink()


def parse_iso_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def normalize_chat_type(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    if value == "p2p":
        return "direct"
    if value in {"direct", "group"}:
        return value
    return value


def sanitize_workspace_key(raw: Optional[str]) -> str:
    value = (raw or "").strip()
    if not value:
        return "default"
    value = re.sub(r"[^A-Za-z0-9._-]+", "_", value)
    value = value.strip("._-")
    return value[:120] or "default"


def resolve_workspace_key(explicit: Optional[str] = None) -> str:
    if explicit and explicit.strip():
        return sanitize_workspace_key(explicit)
    for env_key in WORKSPACE_ENV_KEYS:
        env_value = os.environ.get(env_key)
        if env_value and env_value.strip():
            return sanitize_workspace_key(env_value)
    return "default"


def get_state_paths(workspace_key: Optional[str] = None) -> StatePaths:
    resolved = resolve_workspace_key(workspace_key)
    workspace_dir = STATE_ROOT / resolved
    return StatePaths(
        workspace_key=resolved,
        workspace_dir=workspace_dir,
        binding_file=workspace_dir / "binding.json",
        api_key_file=workspace_dir / "api_key.txt",
        location_file=workspace_dir / "location.json",
        pending_dir=workspace_dir / "pending",
        audit_dir=workspace_dir / "audit",
    )


def ensure_workspace_dirs(paths: StatePaths) -> None:
    paths.workspace_dir.mkdir(parents=True, exist_ok=True)
    paths.pending_dir.mkdir(parents=True, exist_ok=True)
    paths.audit_dir.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> Optional[dict[str, Any]]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def mask_api_key(api_key: str) -> str:
    if len(api_key) < 8:
        return "****"
    return f"{api_key[:4]}****{api_key[-4:]}"


def load_api_key(paths: StatePaths, input_api_key: Optional[str] = None) -> Optional[str]:
    if input_api_key:
        return input_api_key.strip()
    if paths.api_key_file.exists():
        value = paths.api_key_file.read_text(encoding="utf-8").strip()
        return value or None
    # 当前 workspace 未配置 key 时，尝试从 default workspace 兜底读取，
    # 避免平台注入的 workspace key 与用户实际配置 key 所在 workspace 不一致时报错。
    if paths.workspace_key != "default":
        default_key_file = STATE_ROOT / "default" / "api_key.txt"
        if default_key_file.exists():
            value = default_key_file.read_text(encoding="utf-8").strip()
            if value:
                return value
    env_key = os.environ.get("SOYOUNG_CLINIC_API_KEY")
    return env_key.strip() if env_key else None


def save_api_key(paths: StatePaths, api_key: str) -> None:
    ensure_workspace_dirs(paths)
    paths.api_key_file.write_text(api_key.strip(), encoding="utf-8")
    paths.api_key_file.chmod(stat.S_IRUSR | stat.S_IWUSR)


def delete_api_key(paths: StatePaths) -> bool:
    if paths.api_key_file.exists():
        paths.api_key_file.unlink()
        return True
    return False


def load_binding(paths: StatePaths) -> Optional[dict[str, Any]]:
    return read_json(paths.binding_file)


def save_binding(paths: StatePaths, binding: dict[str, Any]) -> None:
    ensure_workspace_dirs(paths)
    write_json(paths.binding_file, binding)


def delete_binding(paths: StatePaths) -> bool:
    if paths.binding_file.exists():
        paths.binding_file.unlink()
        return True
    return False


def load_location(paths: StatePaths) -> Optional[dict[str, Any]]:
    return read_json(paths.location_file)


def save_location(
    paths: StatePaths,
    *,
    city: str,
    district: Optional[str],
    street: Optional[str],
    updated_by_open_id: Optional[str],
    updated_by_name: Optional[str],
) -> dict[str, Any]:
    ensure_workspace_dirs(paths)
    location = {
        "version": 1,
        "city": city,
        "district": district or None,
        "street": street or None,
        "updatedAt": iso_now(),
        "updatedByOpenId": updated_by_open_id,
        "updatedByName": updated_by_name,
    }
    write_json(paths.location_file, location)
    return location


def build_context_from_args(args: Any, *, require: bool = False) -> Optional[MessageContext]:
    workspace_key = resolve_workspace_key(getattr(args, "workspace_key", None))
    chat_type = normalize_chat_type(getattr(args, "chat_type", None))
    chat_id = getattr(args, "chat_id", None)
    sender_open_id = getattr(args, "sender_open_id", None)
    if require:
        missing = []
        if not chat_type:
            missing.append("--chat-type")
        if not chat_id:
            missing.append("--chat-id")
        if not sender_open_id:
            missing.append("--sender-open-id")
        if missing:
            raise SoyoungRuntimeError(
                "缺少上下文参数："
                + "、".join(missing)
                + "。请把当前消息的 MessageContext 传给脚本。"
            )
    if not chat_type and not chat_id and not sender_open_id:
        return None
    mentions = list(getattr(args, "mention_open_id", None) or [])
    return MessageContext(
        workspace_key=workspace_key,
        chat_type=chat_type or "unknown",
        chat_id=chat_id or "",
        sender_open_id=sender_open_id or "",
        sender_name=getattr(args, "sender_name", None),
        mentions=mentions,
        tenant_key=getattr(args, "tenant_key", None),
        message_id=getattr(args, "message_id", None),
    )


def ensure_direct_message(ctx: MessageContext, operation_name: str) -> None:
    if ctx.chat_type != "direct":
        raise SoyoungRuntimeError(
            f"❌ {operation_name} 只能由主人在私聊中操作，API Key 绝不能发送到多人群聊。"
        )


def ensure_owner(ctx: MessageContext, binding: dict[str, Any], operation_name: str) -> None:
    owner_open_id = binding.get("ownerOpenId")
    if not owner_open_id:
        raise SoyoungRuntimeError("❌ 当前 workspace 尚未绑定 API Key 主人。")
    if ctx.sender_open_id != owner_open_id:
        owner_name = binding.get("ownerName") or owner_open_id
        raise SoyoungRuntimeError(
            f"❌ {operation_name}仅允许 API Key 主人操作，当前主人是 {owner_name}。"
        )


def build_binding(
    *,
    ctx: MessageContext,
    api_key: str,
) -> dict[str, Any]:
    return {
        "version": 1,
        "platform": "feishu",
        "workspaceKey": ctx.workspace_key,
        "ownerOpenId": ctx.sender_open_id,
        "ownerName": ctx.sender_name,
        "tenantKey": ctx.tenant_key,
        "apiKeyMasked": mask_api_key(api_key),
        "apiKeyStoredAt": iso_now(),
        "boundAt": iso_now(),
        "boundFromChatType": ctx.chat_type,
        "boundFromChatId": ctx.chat_id,
    }


def audit_event(paths: StatePaths, event: str, payload: dict[str, Any]) -> None:
    ensure_workspace_dirs(paths)
    logfile = paths.audit_dir / f"{utc_now().strftime('%Y-%m-%d')}.jsonl"
    record = {"ts": iso_now(), "event": event, "workspaceKey": paths.workspace_key}
    record.update(payload)
    with logfile.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def format_binding_summary(binding: dict[str, Any]) -> str:
    owner_name = binding.get("ownerName") or binding.get("ownerOpenId", "未知")
    return (
        f"主人：{owner_name}\n"
        f"Open ID：{binding.get('ownerOpenId', '未知')}\n"
        f"绑定时间：{binding.get('boundAt', '未知')}\n"
        f"Key 预览：{binding.get('apiKeyMasked', '未知')}"
    )


def build_request_preview(action: str, params: dict[str, Any]) -> str:
    if action == "appointment_query":
        return "查询我的预约"
    if action == "appointment_create":
        return (
            f"提交预约：机构 {params.get('hospital_id')}，"
            f"{params.get('start_time')} - {params.get('end_time')}"
        )
    if action == "appointment_update":
        return (
            f"修改预约 {params.get('booking_id')}：机构 {params.get('hospital_id')}，"
            f"{params.get('start_time')} - {params.get('end_time')}"
        )
    if action == "appointment_cancel":
        return f"取消预约 {params.get('booking_id')}"
    return action


def make_params_digest(action: str, params: dict[str, Any]) -> str:
    payload = {"action": action, "params": params}
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


PENDING_MAX_PER_SENDER = 3       # 同一 sender 最多同时存在的 pending 审批单数
PENDING_CLEANUP_AGE_HOURS = 24   # 已终态审批单在磁盘上保留的小时数


def clean_expired_pending(paths: StatePaths) -> None:
    """将超时 pending 标记为 expired，并删除超过保留期的已终态审批单。"""
    cutoff_ts = utc_now().timestamp() - PENDING_CLEANUP_AGE_HOURS * 3600
    for file in sorted(paths.pending_dir.glob("*.json")):
        pending = read_json(file)
        if not pending:
            try:
                file.unlink()
            except Exception:
                pass
            continue
        if pending.get("status") == "pending":
            pending = _expire_pending_if_needed(paths, pending)
        if pending.get("status") in {"expired", "consumed", "rejected"}:
            try:
                created_str = pending.get("createdAt", "")
                if created_str and parse_iso_datetime(created_str).timestamp() < cutoff_ts:
                    file.unlink()
            except Exception:
                pass


def check_pending_approval_limit(paths: StatePaths, sender_open_id: str) -> None:
    """防止同一用户在群聊中刷屏创建过多审批单。"""
    active_count = 0
    for file in paths.pending_dir.glob("*.json"):
        pending = read_json(file)
        if not pending:
            continue
        pending = _expire_pending_if_needed(paths, pending)
        if (
            pending.get("status") == "pending"
            and pending.get("requestedByOpenId") == sender_open_id
        ):
            active_count += 1
    if active_count >= PENDING_MAX_PER_SENDER:
        raise SoyoungRuntimeError(
            f"❌ 待审批请求过多：您已有 {active_count} 个未处理的审批单，"
            "请等待主人处理后再发起新请求。"
        )


def create_pending_approval(
    paths: StatePaths,
    *,
    ctx: MessageContext,
    binding: dict[str, Any],
    action: str,
    params: dict[str, Any],
    expires_in_minutes: int = 10,
) -> dict[str, Any]:
    ensure_workspace_dirs(paths)
    clean_expired_pending(paths)
    check_pending_approval_limit(paths, ctx.sender_open_id)
    request_id = secrets.token_hex(3).upper()
    now = utc_now()
    pending = {
        "version": 1,
        "requestId": request_id,
        "workspaceKey": paths.workspace_key,
        "platform": "feishu",
        "tenantKey": ctx.tenant_key,
        "chatId": ctx.chat_id,
        "chatType": "group",
        "action": action,
        "requestedByOpenId": ctx.sender_open_id,
        "requestedByName": ctx.sender_name,
        "ownerOpenId": binding.get("ownerOpenId"),
        "ownerName": binding.get("ownerName"),
        "createdAt": now.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "expiresAt": (now + timedelta(minutes=expires_in_minutes))
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "status": "pending",
        "params": params,
        "paramsDigest": make_params_digest(action, params),
        "previewText": build_request_preview(action, params),
    }
    write_json(paths.pending_dir / f"{request_id}.json", pending)
    audit_event(
        paths,
        "approval_created",
        {
            "requestId": request_id,
            "action": action,
            "chatId": ctx.chat_id,
            "senderOpenId": ctx.sender_open_id,
            "ownerOpenId": binding.get("ownerOpenId"),
        },
    )
    return pending


def load_pending(paths: StatePaths, request_id: str) -> Optional[dict[str, Any]]:
    return read_json(paths.pending_dir / f"{request_id}.json")


def save_pending(paths: StatePaths, pending: dict[str, Any]) -> None:
    write_json(paths.pending_dir / f"{pending['requestId']}.json", pending)


def _expire_pending_if_needed(paths: StatePaths, pending: dict[str, Any]) -> dict[str, Any]:
    if pending.get("status") != "pending":
        return pending
    expires_at = pending.get("expiresAt")
    if expires_at and parse_iso_datetime(expires_at) <= utc_now():
        pending["status"] = "expired"
        save_pending(paths, pending)
    return pending


def resolve_pending_request(
    paths: StatePaths,
    *,
    owner_open_id: str,
    chat_id: str,
    request_id: Optional[str],
) -> dict[str, Any]:
    if request_id:
        pending = load_pending(paths, request_id)
        if not pending:
            raise SoyoungRuntimeError(f"❌ 未找到审批单 #{request_id}。")
        pending = _expire_pending_if_needed(paths, pending)
        return pending

    candidates: list[dict[str, Any]] = []
    for file in paths.pending_dir.glob("*.json"):
        pending = read_json(file)
        if not pending:
            continue
        pending = _expire_pending_if_needed(paths, pending)
        if pending.get("status") != "pending":
            continue
        if pending.get("ownerOpenId") != owner_open_id:
            continue
        if pending.get("chatId") != chat_id:
            continue
        candidates.append(pending)

    if not candidates:
        raise SoyoungRuntimeError("❌ 当前群里没有待处理的审批单。")
    if len(candidates) > 1:
        raise SoyoungRuntimeError("❌ 当前群里有多个待审批请求，请使用“确认 #审批单号”。")
    return candidates[0]


def format_pending_prompt(pending: dict[str, Any]) -> str:
    requester = pending.get("requestedByName") or pending.get("requestedByOpenId") or "某成员"
    owner = pending.get("ownerName") or pending.get("ownerOpenId") or "主人"
    return (
        f"⏸️ 需要主人确认\n\n"
        f"• 申请人：{requester}\n"
        f"• 操作：{pending.get('previewText', pending.get('action', '未知操作'))}\n"
        f"• 审批单号：#{pending.get('requestId')}\n"
        f"• 过期时间：{pending.get('expiresAt')}\n\n"
        f"请主人 {owner} 在同一群里回复：确认 #{pending.get('requestId')}\n"
        f"如需拒绝，请回复：拒绝 #{pending.get('requestId')}"
    )


def authorize_protected_action(
    paths: StatePaths,
    *,
    ctx: Optional[MessageContext],
    binding: Optional[dict[str, Any]],
    action: str,
    params: dict[str, Any],
) -> dict[str, Any]:
    if action not in PROTECTED_APPOINTMENT_ACTIONS:
        return {"type": "allow"}
    if not ctx:
        raise SoyoungRuntimeError(
            "❌ 高风险预约操作必须传入消息上下文（chatType/chatId/senderOpenId）。"
        )
    if not binding:
        raise SoyoungRuntimeError(
            "❌ 当前 workspace 尚未绑定 API Key 主人，请先由主人在私聊中配置 API Key。"
        )
    if ctx.sender_open_id == binding.get("ownerOpenId"):
        return {"type": "allow"}
    if ctx.chat_type != "group":
        owner = binding.get("ownerName") or binding.get("ownerOpenId") or "主人"
        raise SoyoungRuntimeError(
            f"❌ 该操作仅允许主人本人私聊操作，或在群聊中 @主人 {owner} 发起审批。"
        )
    if binding.get("ownerOpenId") not in set(ctx.mentions):
        raise SoyoungRuntimeError("❌ 群聊中的高风险预约操作必须先 @主人 发起审批。")
    pending = create_pending_approval(
        paths,
        ctx=ctx,
        binding=binding,
        action=action,
        params=params,
    )
    return {"type": "need_approval", "pending": pending}


RATE_LIMIT_DEDUP_WINDOW_SECS = 30   # 同一 sender + 门店 + 日期的去重窗口（秒）
RATE_LIMIT_GLOBAL_MAX = 3           # 全局滑动窗口最多创建次数
RATE_LIMIT_GLOBAL_WINDOW_SECS = 60  # 全局频率窗口（秒）


def check_create_rate_limit(
    paths: "StatePaths",
    *,
    sender_open_id: str,
    hospital_id: Optional[int] = None,
    date_str: Optional[str] = None,
) -> None:
    """防止批量/重复预约提交。

    两道防线：
    1. 去重：同一 sender + 同一门店 + 同一日期在 RATE_LIMIT_DEDUP_WINDOW_SECS 内重复提交 → 拒绝
    2. 全局频率：同一 sender 在 RATE_LIMIT_GLOBAL_WINDOW_SECS 内超过 RATE_LIMIT_GLOBAL_MAX 次 → 拒绝
    """
    rate_file = paths.workspace_dir / "rate_limit_create.json"
    now_ts = utc_now().timestamp()

    data: dict[str, list[dict]] = {}
    if rate_file.exists():
        try:
            data = json.loads(rate_file.read_text(encoding="utf-8"))
        except Exception:
            data = {}

    key = sender_open_id or "anon"
    records: list[dict] = data.get(key, [])

    # 只保留全局窗口内的记录，清理过期条目
    active = [r for r in records if now_ts - r.get("ts", 0) < RATE_LIMIT_GLOBAL_WINDOW_SECS]

    # 去重：同一门店 + 同一日期在短窗口内已有记录
    if hospital_id is not None and date_str:
        same_slot = [
            r for r in active
            if now_ts - r.get("ts", 0) < RATE_LIMIT_DEDUP_WINDOW_SECS
            and r.get("hospital_id") == hospital_id
            and r.get("date") == date_str
        ]
        if same_slot:
            raise SoyoungRuntimeError(
                f"❌ 重复提交：该门店 {date_str} 的预约刚刚已提交，"
                f"请勿在 {RATE_LIMIT_DEDUP_WINDOW_SECS} 秒内重复预约同一时段。"
            )

    # 全局频率限制
    if len(active) >= RATE_LIMIT_GLOBAL_MAX:
        raise SoyoungRuntimeError(
            f"❌ 操作过于频繁：{RATE_LIMIT_GLOBAL_WINDOW_SECS} 秒内最多提交 "
            f"{RATE_LIMIT_GLOBAL_MAX} 次预约，请稍后再试。"
        )

    # 写入本次记录
    active.append({"ts": now_ts, "hospital_id": hospital_id, "date": date_str})
    data[key] = active
    paths.workspace_dir.mkdir(parents=True, exist_ok=True)
    rate_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def mark_pending_rejected(
    paths: StatePaths,
    *,
    pending: dict[str, Any],
    ctx: MessageContext,
) -> dict[str, Any]:
    pending = _expire_pending_if_needed(paths, pending)
    if pending.get("status") != "pending":
        raise SoyoungRuntimeError("❌ 该审批单已失效，无法再拒绝。")
    if ctx.chat_id != pending.get("chatId"):
        raise SoyoungRuntimeError("❌ 只能在原群聊中处理该审批单。")
    if ctx.sender_open_id != pending.get("ownerOpenId"):
        raise SoyoungRuntimeError("❌ 只有 API Key 主人可以拒绝该审批单。")
    pending["status"] = "rejected"
    pending["rejectedAt"] = iso_now()
    pending["rejectedByOpenId"] = ctx.sender_open_id
    pending["rejectedByName"] = ctx.sender_name
    save_pending(paths, pending)
    audit_event(
        paths,
        "approval_rejected",
        {
            "requestId": pending.get("requestId"),
            "action": pending.get("action"),
            "chatId": pending.get("chatId"),
            "ownerOpenId": ctx.sender_open_id,
        },
    )
    return pending


def mark_pending_consumed(
    paths: StatePaths,
    *,
    pending: dict[str, Any],
    ctx: MessageContext,
) -> dict[str, Any]:
    pending = _expire_pending_if_needed(paths, pending)
    if pending.get("status") != "pending":
        raise SoyoungRuntimeError("❌ 该审批单已失效，无法再确认。")
    if ctx.chat_id != pending.get("chatId"):
        raise SoyoungRuntimeError("❌ 只能在原群聊中处理该审批单。")
    if ctx.sender_open_id != pending.get("ownerOpenId"):
        raise SoyoungRuntimeError("❌ 只有 API Key 主人可以确认该审批单。")
    pending["status"] = "consumed"
    pending["approvedAt"] = iso_now()
    pending["approvedByOpenId"] = ctx.sender_open_id
    pending["approvedByName"] = ctx.sender_name
    save_pending(paths, pending)
    audit_event(
        paths,
        "approval_consumed",
        {
            "requestId": pending.get("requestId"),
            "action": pending.get("action"),
            "chatId": pending.get("chatId"),
            "ownerOpenId": ctx.sender_open_id,
        },
    )
    return pending
