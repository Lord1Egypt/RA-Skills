#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal OpenClaw message sender used for QR-code and status notifications."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class MessageTarget:
    channel: str
    target: str
    account: str = ""


def load_inbound_meta(raw_json: str | None = None, file_path: str | None = None) -> dict[str, Any] | None:
    if raw_json:
        return json.loads(raw_json)
    if file_path:
        return json.loads(Path(file_path).read_text(encoding="utf-8"))
    return None


def resolve_message_target(
    channel: str | None = None,
    target: str | None = None,
    account: str | None = None,
    inbound_meta_json: str | None = None,
    inbound_meta_file: str | None = None,
) -> MessageTarget | None:
    meta = load_inbound_meta(inbound_meta_json, inbound_meta_file)
    if meta:
        channel = channel or meta.get("channel")
        target = target or meta.get("chat_id")
        account = account or meta.get("account_id")

    channel = channel or os.environ.get("OPENCLAW_CHANNEL")
    target = target or os.environ.get("OPENCLAW_TARGET")
    account = account or os.environ.get("OPENCLAW_ACCOUNT") or ""

    if not channel or not target:
        return None
    return MessageTarget(channel=channel, target=target, account=account)


def _resolve_openclaw_executable() -> str:
    candidates = []
    direct = shutil.which("openclaw")
    if direct:
        candidates.append(direct)

    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if appdata:
            npm_cmd = Path(appdata) / "npm" / "openclaw.cmd"
            npm_exe = Path(appdata) / "npm" / "openclaw.exe"
            candidates.extend([str(npm_cmd), str(npm_exe)])
        local_npm = Path.home() / "AppData" / "Roaming" / "npm" / "openclaw.cmd"
        candidates.append(str(local_npm))

    for item in candidates:
        if item and Path(item).exists():
            return str(Path(item))
    return "openclaw"


class OpenClawMessenger:
    def __init__(self, message_target: MessageTarget):
        self.message_target = message_target
        self.openclaw_executable = _resolve_openclaw_executable()

    def is_ready(self) -> bool:
        return bool(self.message_target.channel and self.message_target.target)

    def _base_args(self) -> list[str]:
        args = [
            self.openclaw_executable,
            "message",
            "send",
            "--channel",
            self.message_target.channel,
            "--target",
            self.message_target.target,
        ]
        if self.message_target.account:
            args.extend(["--account", self.message_target.account])
        return args

    def send_text(self, text: str, timeout: int = 30) -> tuple[bool, str]:
        if not self.is_ready():
            return False, "消息发送器未就绪"
        args = self._base_args() + ["-m", text]
        return _run_openclaw(args, timeout)

    def send_image(self, image_path: str, caption: str = "", timeout: int = 30) -> tuple[bool, str]:
        if not self.is_ready():
            return False, "消息发送器未就绪"
        image = Path(image_path)
        if not image.exists():
            return False, f"图片不存在: {image}"
        args = self._base_args() + ["-m", caption or "请扫码登录", "--media", str(image.resolve())]
        return _run_openclaw(args, timeout)


def _run_openclaw(args: list[str], timeout: int) -> tuple[bool, str]:
    try:
        run_args = args
        if os.name == "nt" and args and args[0].lower().endswith((".cmd", ".bat")):
            run_args = [os.environ.get("COMSPEC", "cmd.exe"), "/c", *args]

        result = subprocess.run(
            run_args,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            encoding="utf-8",
            errors="ignore",
        )
        if result.returncode == 0:
            return True, (result.stdout or "消息发送成功").strip()
        return False, (result.stderr or result.stdout or "openclaw 执行失败").strip()
    except FileNotFoundError:
        return False, f"未找到 openclaw CLI: {args[0] if args else 'openclaw'}"
    except subprocess.TimeoutExpired:
        return False, "openclaw 发送超时"
    except Exception as exc:  # pragma: no cover - defensive
        return False, f"发送失败: {exc}"
