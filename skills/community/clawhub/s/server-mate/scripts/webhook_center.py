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

def send_telegram_document(
    bot_token: str,
    chat_id: str,
    file_path: str,
    caption: str = "",
    timeout_seconds: int = 30,
) -> dict[str, Any]:
    """Upload a local file to a Telegram chat via sendDocument (multipart/form-data).

    Uses only the standard library (urllib + email.mime) so no extra packages
    are required.  Returns the same shape dict as :func:`post_json`.
    """
    import email.generator
    import email.mime.multipart
    import email.mime.application
    import email.mime.text
    import io
    import os

    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

    # Build a multipart body with stdlib email.mime
    msg = email.mime.multipart.MIMEMultipart("form-data")

    def _attach_field(name: str, value: str) -> None:
        part = email.mime.text.MIMEText(value, _charset="utf-8")
        part.add_header("Content-Disposition", "form-data", name=name)
        # MIMEText adds unwanted headers; strip them down to just what we need.
        for key in ("Content-Type", "MIME-Version"):
            if key in part:
                del part[key]
        msg.attach(part)

    _attach_field("chat_id", str(chat_id))
    if caption:
        _attach_field("caption", caption[:1024])  # Telegram caption limit

    filename = os.path.basename(file_path)
    try:
        with open(file_path, "rb") as fh:
            file_bytes = fh.read()
    except OSError as exc:
        return {
            "ok": False,
            "http_status": None,
            "body_text": "",
            "body_json": None,
            "error": f"Cannot read file {file_path!r}: {exc}",
        }

    doc_part = email.mime.application.MIMEApplication(file_bytes, Name=filename)
    doc_part.add_header("Content-Disposition", "form-data", name="document", filename=filename)
    msg.attach(doc_part)

    # Serialise the MIME message into raw bytes and extract the boundary.
    buf = io.BytesIO()
    gen = email.generator.BytesGenerator(buf, mangle_from_=False)
    gen.flatten(msg)
    raw = buf.getvalue()

    # The MIME envelope starts with headers; we only want the body part.
    # Split on the first blank line (\r\n\r\n or \n\n).
    sep = b"\r\n\r\n" if b"\r\n\r\n" in raw else b"\n\n"
    body = raw.split(sep, 1)[1] if sep in raw else raw

    # Extract the Content-Type header which contains the boundary.
    content_type = msg.get("Content-Type", "")

    request = urllib.request.Request(
        url=url,
        data=body,
        headers={"Content-Type": content_type},
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


def send_telegram_document_to_channels(
    config: dict[str, Any],
    file_path: str,
    caption: str = "",
    channels: Iterable[str] | None = None,
    timeout_seconds: int = 30,
) -> list[dict[str, Any]]:
    """Send a file to every enabled Telegram channel in the configuration.

    Non-telegram channels in the active channel list are silently skipped
    because they do not support binary file uploads.
    """
    results: list[dict[str, Any]] = []
    for channel, channel_config in get_active_channels(config, channels):
        if channel != "telegram":
            continue
        bot_token = str(channel_config.get("bot_token") or "").strip()
        chat_id = str(channel_config.get("chat_id") or "").strip()
        if not bot_token or not chat_id:
            continue
        effective_timeout = max(int(channel_config.get("timeout_seconds", timeout_seconds)), 10)
        response = send_telegram_document(
            bot_token=bot_token,
            chat_id=chat_id,
            file_path=file_path,
            caption=caption,
            timeout_seconds=effective_timeout,
        )
        response["channel"] = "telegram"
        response["success"] = bool(response.get("body_json", {}) or {} and
                                   response.get("body_json", {}).get("ok"))
        if isinstance(response.get("body_json"), dict):
            response["success"] = bool(response["body_json"].get("ok"))
        results.append(response)
    return results


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
