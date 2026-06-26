#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按配置文件执行多任务定时群发（用户会话，独立 CLI 子命令）。"""

from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from telethon.errors import FloodWaitError

from tg_monitor_kit.config import Config, load_config
from tg_monitor_kit.session_runtime import cleanup_temp_session_files, create_temp_session_client

# 高风险功能校验
if os.getenv("ENABLE_HIGH_RISK_OPERATIONS", "false").lower() != "true":
    print("""
⚠️  定时群发为高风险功能，默认禁用！
如需启用，请先设置环境变量 ENABLE_HIGH_RISK_OPERATIONS="true"
使用前请确认您的行为符合Telegram服务条款，禁止用于发送垃圾消息、骚扰他人等非法用途，否则后果自负。
""")
    exit(1)

BJ_TZ = timezone(timedelta(hours=8))
DEFAULT_TASK_FILE = Path("config") / "scheduled_tasks.json"
MIN_INTERVAL_HOURS = 0.5
MAX_TASKS = 20


@dataclass
class ScheduledTask:
    name: str
    target_group_id: int
    message: str
    interval_hours: float
    next_run: datetime


def beijing_now() -> datetime:
    return datetime.now(BJ_TZ)


async def _call_with_flood_retry(coro_factory, label: str):
    while True:
        try:
            return await coro_factory()
        except FloodWaitError as e:
            wait = int(e.seconds) + 1
            print(f"⏳ FloodWait（{label}）：等待 {wait} 秒后重试…")
            await asyncio.sleep(wait)


def _scheduled_tasks_file(cfg: Config) -> Path:
    return (cfg.project_root / DEFAULT_TASK_FILE).resolve()


def _validate_task(raw: dict, idx: int) -> tuple[bool, str]:
    required = ("name", "target_group_id", "message", "interval_hours")
    missing = [k for k in required if k not in raw]
    if missing:
        return False, f"第 {idx} 个任务缺少字段: {', '.join(missing)}"
    if not str(raw["name"]).strip():
        return False, f"第 {idx} 个任务 name 不能为空"
    if not str(raw["message"]).strip():
        return False, f"第 {idx} 个任务 message 不能为空"
    try:
        int(raw["target_group_id"])
    except (ValueError, TypeError):
        return False, f"第 {idx} 个任务 target_group_id 必须为整数"
    try:
        interval = float(raw["interval_hours"])
    except (ValueError, TypeError):
        return False, f"第 {idx} 个任务 interval_hours 必须为数字"
    if interval < MIN_INTERVAL_HOURS:
        return False, f"第 {idx} 个任务 interval_hours 不能小于 {MIN_INTERVAL_HOURS}"
    return True, ""


def load_scheduled_tasks(cfg: Config) -> list[ScheduledTask]:
    path = _scheduled_tasks_file(cfg)
    if not path.is_file():
        print(f"❌ 未找到定时群发配置文件：{path}")
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"❌ 读取定时群发配置失败（JSON 格式错误）：{exc}")
        return []

    raw_tasks = data.get("tasks")
    if not isinstance(raw_tasks, list):
        print("❌ 配置格式错误：顶层必须包含 tasks 数组。")
        return []
    if not raw_tasks:
        print("❌ 未配置任务：tasks 为空。")
        return []
    if len(raw_tasks) > MAX_TASKS:
        print(f"❌ 已拒绝启动：任务数量不能超过 {MAX_TASKS}。当前为 {len(raw_tasks)}。")
        return []

    now = beijing_now()
    tasks: list[ScheduledTask] = []
    for idx, raw in enumerate(raw_tasks, start=1):
        if not isinstance(raw, dict):
            print(f"❌ 第 {idx} 个任务格式错误：必须是对象。")
            return []
        ok, reason = _validate_task(raw, idx)
        if not ok:
            print(f"❌ 配置校验失败：{reason}")
            return []
        task = ScheduledTask(
            name=str(raw["name"]).strip(),
            target_group_id=int(raw["target_group_id"]),
            message=str(raw["message"]),
            interval_hours=float(raw["interval_hours"]),
            next_run=now,
        )
        tasks.append(task)
    return tasks


async def _run_task_once(client, task: ScheduledTask):
    started = beijing_now().strftime("%Y-%m-%d %H:%M:%S")
    print(
        f"📨 开始发送 | 任务: {task.name} | 群ID: {task.target_group_id} | "
        f"北京时间: {started}"
    )
    try:
        await _call_with_flood_retry(
            lambda: client.send_message(task.target_group_id, task.message),
            f"send:{task.name}",
        )
        print(f"✅ 发送成功 | 任务: {task.name}")
    except Exception as exc:
        print(f"❌ 发送失败 | 任务: {task.name} | 错误: {type(exc).__name__}: {exc}")
    finally:
        task.next_run = beijing_now() + timedelta(hours=task.interval_hours)
        print(
            f"⏰ 下次发送 | 任务: {task.name} | "
            f"北京时间: {task.next_run.strftime('%Y-%m-%d %H:%M:%S')}"
        )


async def run_send_daemon() -> None:
    cfg = load_config()
    tasks = load_scheduled_tasks(cfg)
    if not tasks:
        return

    task_path = _scheduled_tasks_file(cfg)
    try:
        temp = create_temp_session_client(cfg, "send")
    except FileNotFoundError as exc:
        print(f"❌ {exc}")
        return
    client = temp.client
    await client.start()
    print(
        f"🚀 定时群发服务已启动（北京时间）。配置文件: {task_path}，"
        f"任务数: {len(tasks)}。"
    )
    try:
        while True:
            now = beijing_now()
            due = [t for t in tasks if t.next_run <= now]
            if due:
                for t in due:
                    await _run_task_once(client, t)
                continue
            next_time = min(t.next_run for t in tasks)
            sleep_seconds = max(1, int((next_time - now).total_seconds()))
            print(
                f"🕒 当前无到期任务，{sleep_seconds} 秒后检查（下次触发北京时间: "
                f"{next_time.strftime('%Y-%m-%d %H:%M:%S')}）。"
            )
            await asyncio.sleep(sleep_seconds)
    finally:
        await client.disconnect()
        cleanup_temp_session_files(temp.temp_session_base)
        print("✅ 定时群发服务已停止，Telegram 连接已断开。")


__all__ = ["run_send_daemon"]
