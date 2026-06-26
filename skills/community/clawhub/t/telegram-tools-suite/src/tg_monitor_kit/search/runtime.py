#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""固定关键词搜索超级群（用户会话），结果推送与 Excel 导出。"""

import asyncio
import json
import os
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from telethon import TelegramClient
from telethon.errors import FloodWaitError, RPCError
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.contacts import SearchRequest
from telethon.tl.types import Channel
from openpyxl import Workbook

from tg_monitor_kit.config import Config, load_config
from tg_monitor_kit.session_runtime import cleanup_temp_session_files, create_temp_session_client

NOTIFY_TARGET = "me"

DEFAULT_FIXED_KEYWORDS = []

DEFAULT_SEARCH_LIMIT = 40
DEFAULT_ACTIVITY_SAMPLE = 200
TG_MAX_MESSAGE = 3500
BJ_TZ = timezone(timedelta(hours=8))
DEFAULT_RUN_ON_STARTUP = True
DEFAULT_SCHEDULE_HOUR = 18
DEFAULT_SCHEDULE_MINUTE = 30
DEFAULT_EXCEL_OUTPUT_DIR = "daily_group_search"
DEFAULT_EXCEL_HEADERS = [
    "查询时间(北京时间)",
    "命中关键词",
    "群名称",
    "群类型",
    "公开信息",
    "链接",
    "群ID",
    "成员数",
    "创建时间近似(北京时间)",
    "最近消息时间(北京时间)",
    "活跃度_24h_样本",
    "活跃度_7d_样本",
    "活跃度样本总量",
    "可发言(推断)",
]

FIXED_KEYWORDS = list(DEFAULT_FIXED_KEYWORDS)
SEARCH_LIMIT = DEFAULT_SEARCH_LIMIT
ACTIVITY_SAMPLE = DEFAULT_ACTIVITY_SAMPLE
RUN_ON_STARTUP = DEFAULT_RUN_ON_STARTUP
SCHEDULE_HOUR = DEFAULT_SCHEDULE_HOUR
SCHEDULE_MINUTE = DEFAULT_SCHEDULE_MINUTE
EXCEL_OUTPUT_DIR = DEFAULT_EXCEL_OUTPUT_DIR
EXCEL_HEADERS = list(DEFAULT_EXCEL_HEADERS)

_project_root = None


def _ensure_root(cfg: Config):
    global _project_root
    _project_root = str(cfg.project_root)


def _read_non_comment_lines(path: Path):
    if not path.is_file():
        return []
    items = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        text = raw.strip()
        if not text or text.startswith("#"):
            continue
        items.append(text)
    return items


def _load_search_settings(cfg: Config):
    global FIXED_KEYWORDS, SEARCH_LIMIT, ACTIVITY_SAMPLE
    global RUN_ON_STARTUP, SCHEDULE_HOUR, SCHEDULE_MINUTE
    global EXCEL_OUTPUT_DIR, EXCEL_HEADERS

    root = Path(cfg.project_root)

    kw_file_raw = os.environ.get("TG_GROUP_SEARCH_KEYWORDS_FILE", "").strip()
    if kw_file_raw:
        kw_file = Path(kw_file_raw).expanduser()
        if not kw_file.is_absolute():
            kw_file = root / kw_file
    else:
        kw_file = root / "config" / "group_search_keywords.txt"
    FIXED_KEYWORDS = _read_non_comment_lines(kw_file) or list(DEFAULT_FIXED_KEYWORDS)

    settings_file_raw = os.environ.get("TG_GROUP_SEARCH_SETTINGS_FILE", "").strip()
    if settings_file_raw:
        settings_file = Path(settings_file_raw).expanduser()
        if not settings_file.is_absolute():
            settings_file = root / settings_file
    else:
        settings_file = root / "config" / "group_search.json"

    data = {}
    if settings_file.is_file():
        try:
            data = json.loads(settings_file.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"⚠️ 读取 group_search 配置失败，使用默认配置：{exc}")
            data = {}

    SEARCH_LIMIT = int(data.get("search_limit", DEFAULT_SEARCH_LIMIT))
    ACTIVITY_SAMPLE = int(data.get("activity_sample", DEFAULT_ACTIVITY_SAMPLE))
    RUN_ON_STARTUP = bool(data.get("run_on_startup", DEFAULT_RUN_ON_STARTUP))
    SCHEDULE_HOUR = int(data.get("schedule_hour", DEFAULT_SCHEDULE_HOUR))
    SCHEDULE_MINUTE = int(data.get("schedule_minute", DEFAULT_SCHEDULE_MINUTE))
    EXCEL_OUTPUT_DIR = str(data.get("excel_output_dir", DEFAULT_EXCEL_OUTPUT_DIR))
    EXCEL_HEADERS = data.get("excel_headers", list(DEFAULT_EXCEL_HEADERS))


def beijing_str(dt):
    if dt is None:
        return "N/A"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(BJ_TZ).strftime("%Y-%m-%d %H:%M:%S")


def _title_match_and(channel: Channel, right: str) -> bool:
    blob = f"{channel.title or ''} {(channel.username or '')}".lower()
    r = (right or "").strip().lower()
    if not r:
        return True
    if r in blob:
        return True
    if r == "ads" or r == "ad":
        return bool(re.search(r"\bads\b", blob) or "广告" in blob)
    return False


async def _call_with_flood_retry(coro_factory, label: str):
    while True:
        try:
            return await coro_factory()
        except FloodWaitError as e:
            wait = int(e.seconds) + 1
            print(f"⏳ FloodWait（{label}）：等待 {wait} 秒…")
            await asyncio.sleep(wait)


async def search_supergroups_for_keyword(client: TelegramClient, keyword: str):
    kw = keyword.strip()
    if not kw:
        return []

    if "+" in kw:
        left, right = kw.split("+", 1)
        left, right = left.strip(), right.strip()
        if not left:
            return []

        async def do_search(q):
            return await client(SearchRequest(q=q, limit=SEARCH_LIMIT))

        result = await _call_with_flood_retry(lambda: do_search(left), f"Search:{left}")
        supergroups = []
        for chat in result.chats:
            if isinstance(chat, Channel) and chat.megagroup and _title_match_and(chat, right):
                supergroups.append(chat)
        return supergroups

    async def do_search_full():
        return await client(SearchRequest(q=kw, limit=SEARCH_LIMIT))

    result = await _call_with_flood_retry(do_search_full, f"Search:{kw}")
    return [c for c in result.chats if isinstance(c, Channel) and c.megagroup]


async def get_member_count(client: TelegramClient, ch: Channel):
    try:
        full = await _call_with_flood_retry(
            lambda: client(GetFullChannelRequest(channel=ch)),
            f"FullChannel:{ch.id}",
        )
        n = getattr(full.full_chat, "participants_count", None)
        return n, full
    except (RPCError, ValueError, TypeError) as e:
        print(f"⚠️ 取成员数失败 {getattr(ch, 'title', ch.id)}: {e}")
        return None, None


def describe_speakability(ch: Channel, full) -> str:
    if ch.broadcast:
        return "广播频道（通常仅管理员/关联讨论组可发帖）"
    if not ch.megagroup:
        return "未知"
    if full is None:
        return "未知（未取到完整信息）"
    dbr = getattr(full.full_chat, "default_banned_rights", None)
    if dbr is None:
        return "未知（无 default_banned_rights）"
    if getattr(dbr, "send_messages", False):
        return "默认禁言（新成员不可发言）"
    return "默认可发言"


def describe_public(ch: Channel) -> str:
    if ch.username:
        return f"公开（@{ch.username}）"
    return "无公开用户名（链接不可用）"


async def activity_and_earliest(client: TelegramClient, ch: Channel):
    now = datetime.now(timezone.utc)
    d1 = now - timedelta(days=1)
    d7 = now - timedelta(days=7)
    c24, c7, total = 0, 0, 0
    latest = None
    try:
        async for m in client.iter_messages(ch, limit=ACTIVITY_SAMPLE):
            if not m or not m.date:
                continue
            total += 1
            md = m.date
            if md.tzinfo is None:
                md = md.replace(tzinfo=timezone.utc)
            if latest is None or md > latest:
                latest = md
            if md >= d1:
                c24 += 1
            if md >= d7:
                c7 += 1
    except (RPCError, ValueError, TypeError) as e:
        print(f"⚠️ 拉消息样本失败 {getattr(ch, 'title', ch.id)}: {e}")
        return None, None, None, None, None, str(e)

    earliest = None
    try:
        async for m in client.iter_messages(ch, limit=1, reverse=True):
            if m and m.date:
                earliest = m.date
                if earliest.tzinfo is None:
                    earliest = earliest.replace(tzinfo=timezone.utc)
            break
    except (RPCError, ValueError, TypeError) as e:
        print(f"⚠️ 取最早消息失败 {getattr(ch, 'title', ch.id)}: {e}")

    return c24, c7, total, latest, earliest, None


def channel_kind(ch: Channel) -> str:
    if ch.megagroup:
        return "超级群"
    if ch.broadcast:
        return "频道"
    return "群组/其他"


def format_one_block(ch: Channel, keyword: str, member_count, full, act) -> str:
    c24, c7, sample_total, latest, earliest, act_err = act
    link = f"https://t.me/{ch.username}" if ch.username else "N/A"
    lines = [
        f"关键词: {keyword}",
        f"群名称: {ch.title or 'N/A'}",
        f"类型: {channel_kind(ch)}",
        f"公开: {describe_public(ch)}",
        f"链接: {link}",
        f"群 ID: {ch.id}",
        f"成员数: {member_count if member_count is not None else 'N/A'}",
        f"创建时间(近似): 最早可见消息（北京时间） {beijing_str(earliest)}",
        f"最近消息（北京时间）: {beijing_str(latest)}",
    ]
    if act_err:
        lines.append(f"活跃度: 无法统计（{act_err}）")
    else:
        lines.append(
            f"活跃度(样本最近{ACTIVITY_SAMPLE}条): 24h={c24}/{sample_total}, 7d={c7}/{sample_total}"
        )
    lines.append(f"可发言(推断): {describe_speakability(ch, full)}")
    lines.append("-" * 40)
    return "\n".join(lines)


def chunk_text(text: str, max_len: int = TG_MAX_MESSAGE - 200):
    if len(text) <= max_len:
        return [text]
    parts = []
    buf = []
    cur = 0
    for line in text.splitlines():
        line_len = len(line) + 1
        if cur + line_len > max_len and buf:
            parts.append("\n".join(buf))
            buf = [line]
            cur = line_len
        else:
            buf.append(line)
            cur += line_len
    if buf:
        parts.append("\n".join(buf))
    return parts


def _seconds_until_next_schedule(hour=SCHEDULE_HOUR, minute=SCHEDULE_MINUTE):
    now = datetime.now(BJ_TZ)
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if now >= target:
        target += timedelta(days=1)
    return max(1, int((target - now).total_seconds()))


def export_search_excel(rows):
    base_dir = _project_root or os.getcwd()
    output_dir = os.path.join(base_dir, EXCEL_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now(BJ_TZ).strftime("%Y-%m-%d")
    ts = datetime.now(BJ_TZ).strftime("%H%M%S")
    output_path = os.path.join(output_dir, f"{date_str}_1830群搜索_{ts}.xlsx")

    wb = Workbook()
    ws = wb.active
    ws.title = "群搜索结果"
    ws.append(EXCEL_HEADERS)
    for row in rows:
        ws.append(row)
    wb.save(output_path)
    return output_path


async def run_search_once(client: TelegramClient):
    started_bj = datetime.now(BJ_TZ).strftime("%Y-%m-%d %H:%M:%S")
    print(f"开始按固定关键词搜索（北京时间 {started_bj}）…")
    aggregated = {}
    for keyword in FIXED_KEYWORDS:
        try:
            found = await search_supergroups_for_keyword(client, keyword)
            print(f"「{keyword}」→ {len(found)} 个超级群（过滤后）")
            for ch in found:
                if ch.id not in aggregated:
                    aggregated[ch.id] = (ch, set())
                aggregated[ch.id][1].add(keyword)
        except Exception as e:
            print(f"❌ 关键词「{keyword}」搜索失败: {e}")
        await asyncio.sleep(2)

    if not aggregated:
        msg = f"【群搜索】北京时间 {started_bj}\n未搜索到任何超级群结果。"
        print(msg)
        await client.send_message(NOTIFY_TARGET, msg)
        return

    excel_rows = []
    header = (
        f"【群搜索】北京时间 {datetime.now(BJ_TZ).strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"共 {len(aggregated)} 个去重后的超级群，逐项信息如下：\n\n"
    )

    blocks = []
    for _, (ch, kws) in aggregated.items():
        member_count, full = await get_member_count(client, ch)
        act = await activity_and_earliest(client, ch)
        kw_str = "、".join(sorted(kws))
        blocks.append(format_one_block(ch, kw_str, member_count, full, act))
        c24, c7, sample_total, latest, earliest, act_err = act
        speakability = describe_speakability(ch, full)
        excel_rows.append(
            [
                started_bj,
                kw_str,
                ch.title or "N/A",
                channel_kind(ch),
                describe_public(ch),
                f"https://t.me/{ch.username}" if ch.username else "N/A",
                ch.id,
                member_count if member_count is not None else "N/A",
                beijing_str(earliest),
                beijing_str(latest),
                c24 if c24 is not None else "N/A",
                c7 if c7 is not None else "N/A",
                sample_total if sample_total is not None else "N/A",
                speakability if not act_err else f"{speakability} / 活跃度统计异常",
            ]
        )
        await asyncio.sleep(1.5)

    body = "\n".join(blocks)
    full_report = header + body

    print(full_report)

    chunks = chunk_text(full_report)
    n_chunks = len(chunks)
    for i, piece in enumerate(chunks):
        suffix = f"\n\n[分段 {i + 1}/{n_chunks}]" if n_chunks > 1 else ""
        text_to_send = piece + suffix

        async def _send(t=text_to_send):
            return await client.send_message(NOTIFY_TARGET, t)

        try:
            await _call_with_flood_retry(_send, "send_message")
        except Exception as e:
            print(f"❌ 推送分段失败: {e}")

    output_path = export_search_excel(excel_rows)
    excel_msg = f"📊 群搜索Excel已生成：{output_path}"
    print(excel_msg)
    await _call_with_flood_retry(lambda: client.send_message(NOTIFY_TARGET, excel_msg), "send_excel_path")


async def run_search_daemon():
    cfg = load_config()
    _ensure_root(cfg)
    _load_search_settings(cfg)

    try:
        temp = create_temp_session_client(cfg, "search")
    except FileNotFoundError as exc:
        print(f"❌ {exc}")
        return

    client = temp.client
    await client.start()
    print("已连接 Telegram，进入每日定时搜索模式。")
    try:
        if RUN_ON_STARTUP:
            await run_search_once(client)
        while True:
            wait_seconds = _seconds_until_next_schedule(SCHEDULE_HOUR, SCHEDULE_MINUTE)
            print(
                f"⏰ 下次自动搜索将在 {wait_seconds} 秒后"
                f"（北京时间 {SCHEDULE_HOUR:02d}:{SCHEDULE_MINUTE:02d}）"
            )
            await asyncio.sleep(wait_seconds)
            await run_search_once(client)
    finally:
        await client.disconnect()
        cleanup_temp_session_files(temp.temp_session_base)
    print("✅ 已完成并断开连接。")


__all__ = ["run_search_daemon"]
