#!/usr/bin/env python3
"""Webhook delivery helpers for Server-Mate alerts and reports."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterable


SUPPORTED_CHANNELS = ("dingtalk", "wecom", "feishu", "telegram")
SEVERITY_RANK = {"info": 0, "warning": 1, "critical": 2}


def normalize_channel_names(channels: Iterable[str] | None) -> list[str]:
    if not channels:
        return []
    normalized = []
    for channel in channels:
        name = str(channel or "").strip().lower()
        if name and name not in normalized:
            normalized.append(name)
    return normalized


def get_active_channels(
    config: dict[str, Any],
    channels: Iterable[str] | None = None,
) -> list[tuple[str, dict[str, Any]]]:
    notifications = config.get("notifications", {})
    webhooks = notifications.get("webhooks", {})
    requested = normalize_channel_names(channels) or list(SUPPORTED_CHANNELS)

    active = []
    for name in requested:
        channel_config = webhooks.get(name) or {}
        if not isinstance(channel_config, dict):
            continue
        if not channel_config.get("enabled"):
            continue
        if name == "telegram":
            bot_token = str(channel_config.get("bot_token") or os.getenv("TELEGRAM_BOT_TOKEN") or "").strip()
            chat_id = str(channel_config.get("chat_id") or os.getenv("TELEGRAM_CHAT_ID") or "").strip()
            if not bot_token or not chat_id:
                continue
            channel_config = dict(channel_config)
            channel_config["bot_token"] = bot_token
            channel_config["chat_id"] = chat_id
            channel_config["url"] = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        elif not str(channel_config.get("url") or "").strip():
            continue
        active.append((name, channel_config))
    return active


def markdown_to_feishu_post(title: str, markdown: str) -> dict[str, Any]:
    content = []
    for line in markdown.strip().splitlines():
        if not line.strip():
            continue
        content.append([{"tag": "text", "text": line}])
    if not content:
        content = [[{"tag": "text", "text": title}]]
    return {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": title,
                    "content": content,
                }
            }
        },
    }


def build_markdown_payload(
    channel: str,
    title: str,
    markdown: str,
    channel_config: dict[str, Any],
) -> dict[str, Any]:
    if channel == "telegram":
        return {
            "chat_id": str(channel_config.get("chat_id") or ""),
            "text": telegram_markdown(title, markdown),
            "parse_mode": "Markdown",
            "disable_web_page_preview": bool(channel_config.get("disable_web_page_preview", True)),
        }
    if channel == "dingtalk":
        return {
            "msgtype": "markdown",
            "markdown": {"title": title, "text": markdown},
            "at": {"isAtAll": bool(channel_config.get("at_all", False))},
        }
    if channel == "wecom":
        return {
            "msgtype": "markdown",
            "markdown": {"content": markdown},
        }
    if channel == "feishu":
        return markdown_to_feishu_post(title, markdown)
    raise ValueError(f"Unsupported webhook channel: {channel}")


def parse_response_body(raw_body: bytes) -> tuple[str, dict[str, Any] | None]:
    text = raw_body.decode("utf-8", errors="replace")
    try:
        return text, json.loads(text)
    except json.JSONDecodeError:
        return text, None


def response_is_success(
    channel: str,
    status_code: int,
    body_json: dict[str, Any] | None,
) -> bool:
    if status_code < 200 or status_code >= 300:
        return False
    if body_json is None:
        return False
    if channel == "dingtalk":
        return str(body_json.get("errcode")) == "0"
    if channel == "wecom":
        return str(body_json.get("errcode")) == "0"
    if channel == "feishu":
        return str(body_json.get("code")) == "0"
    if channel == "telegram":
        return bool(body_json.get("ok"))
    return False


def telegram_markdown(title: str, markdown: str) -> str:
    lines: list[str] = [f"*{title.replace('*', '')}*"]
    for raw_line in markdown.strip().splitlines():
        line = raw_line.rstrip()
        if not line:
            lines.append("")
            continue
        if line.startswith("# "):
            lines.append(f"*{line[2:].strip().replace('*', '')}*")
            continue
        if line.startswith("## "):
            lines.append(f"*{line[3:].strip().replace('*', '')}*")
            continue
        lines.append(line.replace("`", ""))
    return "\n".join(lines).strip()


def post_json(
    url: str,
    payload: dict[str, Any],
    timeout_seconds: int = 10,
) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url=url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw_body = response.read()
            body_text, body_json = parse_response_body(raw_body)
            return {
                "ok": True,
                "http_status": response.status,
                "body_text": body_text,
                "body_json": body_json,
            }
    except urllib.error.HTTPError as exc:
        raw_body = exc.read()
        body_text, body_json = parse_response_body(raw_body)
        return {
            "ok": False,
            "http_status": exc.code,
            "body_text": body_text,
            "body_json": body_json,
            "error": str(exc),
        }
    except urllib.error.URLError as exc:
        return {
            "ok": False,
            "http_status": None,
            "body_text": "",
            "body_json": None,
            "error": str(exc),
        }


def send_markdown_message(
    config: dict[str, Any],
    title: str,
    markdown: str,
    channels: Iterable[str] | None = None,
) -> list[dict[str, Any]]:
    results = []
    for channel, channel_config in get_active_channels(config, channels):
        payload = build_markdown_payload(channel, title, markdown, channel_config)
        timeout_seconds = max(int(channel_config.get("timeout_seconds", 10)), 1)
        response = post_json(channel_config["url"], payload, timeout_seconds)
        response["channel"] = channel
        response["success"] = response_is_success(
            channel,
            int(response["http_status"] or 0),
            response.get("body_json"),
        )
        results.append(response)
    return results
