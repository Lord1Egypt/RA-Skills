#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从项目根清单文件批量加群（用户会话），可选按北京时间定时重复执行。"""

from __future__ import annotations

import asyncio
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from telethon import TelegramClient
from telethon.errors import FloodWaitError, UserAlreadyParticipantError
from telethon.tl.functions.messages import ImportChatInviteRequest

from tg_monitor_kit.config import Config, load_config
from tg_monitor_kit.session_runtime import cleanup_temp_session_files, create_temp_session_client

# 高风险功能校验
if os.getenv("ENABLE_HIGH_RISK_OPERATIONS", "false").lower() != "true":
    print("""
⚠️  批量加群为高风险功能，默认禁用！
如需启用，请先设置环境变量 ENABLE_HIGH_RISK_OPERATIONS="true"
使用前请确认您的行为符合Telegram服务条款，禁止用于非法用途，否则后果自负。
""")
    exit(1)

NOTIFY_TARGET = "me"
BJ_TZ = timezone(timedelta(hours=8))

RUN_ON_STARTUP = True
SCHEDULE_HOUR = 9
SCHEDULE_MINUTE = 0

DEFAULT_LIST_BASENAME = "join_targets.txt"
MIN_DELAY_BETWEEN_JOINS_SEC = 30 * 60
DELAY_BETWEEN_JOINS_SEC = float(os.environ.get("TG_JOIN_DELAY_SEC", str(MIN_DELAY_BETWEEN_JOINS_SEC)))
MAX_JOINS_PER_RUN = int(os.environ.get("TG_MAX_JOINS_PER_RUN", "20"))
MAX_ALLOWED_JOINS_PER_RUN = 20
REQUIRE_PERSISTENT_JOIN_ENV = "TG_ENABLE_PERSISTENT_JOIN"


def _seconds_until_next_schedule(hour=SCHEDULE_HOUR, minute=SCHEDULE_MINUTE) -> int:
    now = datetime.now(BJ_TZ)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return max(1, int((target - now).total_seconds()))


async def _call_with_flood_retry(coro_factory, label: str):
    while True:
        try:
            return await coro_factory()
        except FloodWaitError as e:
            wait = int(e.seconds) + 1
            print(f"⏳ FloodWait（{label}）：等待 {wait} 秒…")
            await asyncio.sleep(wait)


def list_file_path(cfg: Config) -> Path:
    raw = os.environ.get("TG_JOIN_LIST_FILE", "").strip()
    if raw:
        p = Path(raw).expanduser()
        if not p.is_absolute():
            return (cfg.project_root / p).resolve()
        return p.resolve()
    return (cfg.project_root / DEFAULT_LIST_BASENAME).resolve()


def _normalize_join_arg(raw: str) -> str:
    s = raw.strip()
    if not s:
        return ""
    if s.startswith("@") and "t.me" not in s and "/" not in s[1:]:
        return s[1:].strip()
    return s


def _dedupe_key(raw: str) -> str:
    s = _normalize_join_arg(raw)
    if not s:
        return ""
    if re.match(r"^https?://t\.me/", s, re.I):
        return s.split("?", 1)[0].rstrip("/").lower()
    if s.startswith("@"):
        return s[1:].lower()
    if "/" not in s:
        return s.lower()
    return s


def _extract_invite_hash(s: str) -> str | None:
    s = s.strip()
    m = re.search(r"t\.me/\+([A-Za-z0-9_-]+)", s, re.I)
    if m:
        return m.group(1)
    m = re.search(r"joinchat/([A-Za-z0-9_-]+)", s, re.I)
    if m:
        return m.group(1)
    return None


def load_target_lines(cfg: Config) -> list[str]:
    path = list_file_path(cfg)
    if not path.is_file():
        print(f"⚠️ 清单文件不存在: {path}")
        return []
    out: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"❌ 无法读取清单: {e}")
        return []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out


async def _join_with_invite_hash(client: TelegramClient, hash_str: str, label: str):
    async def do_import():
        return await client(ImportChatInviteRequest(hash_str))

    await _call_with_flood_retry(do_import, f"import_invite:{label}")


async def join_one_line(client: TelegramClient, raw: str) -> tuple[str, str]:
    label = raw.strip()[:120] if raw.strip() else "(空)"
    arg = _normalize_join_arg(raw)
    if not arg:
        return "skip", "空行"

    try:

        async def do_join():
            return await client.join_chat(arg)

        await _call_with_flood_retry(do_join, f"join:{label}")
        return "ok", "已发送加群请求/已加入"
    except UserAlreadyParticipantError:
        return "already", "已在群内"
    except Exception as e:
        h = _extract_invite_hash(arg)
        if h:
            try:
                await _join_with_invite_hash(client, h, label)
                return "ok", "已通过邀请链接加入"
            except UserAlreadyParticipantError:
                return "already", "已在群内"
            except Exception as e2:
                return "fail", f"{type(e2).__name__}: {e2}"
        return "fail", f"{type(e).__name__}: {e}"


async def run_join_round(client: TelegramClient, cfg: Config) -> dict[str, int]:
    started_bj = datetime.now(BJ_TZ).strftime("%Y-%m-%d %H:%M:%S")
    lines = load_target_lines(cfg)
    path = list_file_path(cfg)
    print(f"【批量加群】北京时间 {started_bj}，清单: {path}，共 {len(lines)} 行（去重前）")

    stats = {"ok": 0, "already": 0, "fail": 0, "skip": 0}
    seen_keys: set[str] = set()
    attempts = 0

    for raw in lines:
        if attempts >= MAX_JOINS_PER_RUN:
            print(f"⏸️ 已达本回合上限 MAX_JOINS_PER_RUN={MAX_JOINS_PER_RUN}，余下条目下次再处理。")
            break
        key = _dedupe_key(raw)
        if not key:
            stats["skip"] += 1
            continue
        if key in seen_keys:
            continue
        seen_keys.add(key)
        attempts += 1

        status, detail = await join_one_line(client, raw)
        stats[status] = stats.get(status, 0) + 1
        sym = {"ok": "✅", "already": "ℹ️", "fail": "❌", "skip": "⏭️"}.get(status, "·")
        print(f"  {sym} {raw[:100]!r} → {status}: {detail}")

        await asyncio.sleep(DELAY_BETWEEN_JOINS_SEC)

    summary = (
        f"【批量加群】北京时间 {datetime.now(BJ_TZ).strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"清单: {path}\n"
        f"成功: {stats['ok']}, 已在群: {stats['already']}, 失败: {stats['fail']}, 跳过: {stats['skip']}"
    )
    print(summary)
    if attempts > 0 or lines:
        try:

            async def _send():
                return await client.send_message(NOTIFY_TARGET, summary)

            await _call_with_flood_retry(_send, "join_summary")
        except Exception as e:
            print(f"⚠️ 推送汇总失败: {e}")
    return stats


def _validate_join_limits() -> tuple[bool, str]:
    if DELAY_BETWEEN_JOINS_SEC < MIN_DELAY_BETWEEN_JOINS_SEC:
        return (
            False,
            f"❌ 已拒绝启动：TG_JOIN_DELAY_SEC 不能小于 {MIN_DELAY_BETWEEN_JOINS_SEC} 秒（30分钟）。",
        )
    if MAX_JOINS_PER_RUN > MAX_ALLOWED_JOINS_PER_RUN:
        return (
            False,
            f"❌ 已拒绝启动：TG_MAX_JOINS_PER_RUN 不能大于 {MAX_ALLOWED_JOINS_PER_RUN}。",
        )
    if MAX_JOINS_PER_RUN <= 0:
        return False, "❌ 已拒绝启动：TG_MAX_JOINS_PER_RUN 必须大于 0。"
    return True, ""


async def run_join_daemon(once: bool = False) -> None:
    ok, reason = _validate_join_limits()
    if not ok:
        print(reason)
        return

    if not once and os.environ.get(REQUIRE_PERSISTENT_JOIN_ENV, "").strip().lower() != "true":
        print(
            "⚠️ 出于风控考虑，join 长驻模式默认关闭。"
            f"如需开启，请显式设置 {REQUIRE_PERSISTENT_JOIN_ENV}=true 后重试。"
        )
        return

    cfg = load_config()
    try:
        temp = create_temp_session_client(cfg, "join")
    except FileNotFoundError as exc:
        print(f"❌ {exc}")
        return
    client = temp.client
    await client.start()
    print("已连接 Telegram，批量加群任务（join）已启动（使用临时会话副本）。")
    try:
        if once:
            await run_join_round(client, cfg)
            return
        if RUN_ON_STARTUP:
            await run_join_round(client, cfg)
        while True:
            wait_seconds = _seconds_until_next_schedule(SCHEDULE_HOUR, SCHEDULE_MINUTE)
            print(
                f"⏰ 下次批量加群将在 {wait_seconds} 秒后"
                f"（北京时间 {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d}）"
            )
            await asyncio.sleep(wait_seconds)
            await run_join_round(client, cfg)
    finally:
        await client.disconnect()
        cleanup_temp_session_files(temp.temp_session_base)
    print("✅ 已断开 Telegram 连接。")


__all__ = ["run_join_daemon"]
