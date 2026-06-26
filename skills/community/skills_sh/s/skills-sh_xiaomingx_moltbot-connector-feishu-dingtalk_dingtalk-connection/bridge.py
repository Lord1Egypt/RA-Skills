#!/usr/bin/env python3
"""
DingTalk ↔ Moltbot bridge.

Receives messages from DingTalk outgoing webhook,
forwards them to Moltbot Gateway, and sends replies back.
"""
from __future__ import annotations

import asyncio
import hmac
import json
import os
import re
import time
import uuid
from typing import Any, Dict, Optional
from urllib.parse import unquote

from aiohttp import ClientSession, web
import websockets

PORT = int(os.getenv("DINGTALK_PORT", "3210"))
PATH = os.getenv("DINGTALK_PATH", "/dingtalk")
SIGNING_SECRET = os.getenv("DINGTALK_SIGNING_SECRET", "")
CLAWDBOT_CONFIG_PATH = os.getenv("CLAWDBOT_CONFIG_PATH", "~/.clawdbot/clawdbot.json")
CLAWDBOT_AGENT_ID = os.getenv("CLAWDBOT_AGENT_ID", "main")
THINKING_THRESHOLD_MS = int(os.getenv("DINGTALK_THINKING_THRESHOLD_MS", "2500"))
BOT_ID = os.getenv("DINGTALK_BOT_ID", "")
BOT_NAME = os.getenv("DINGTALK_BOT_NAME", "")

SEEN_TTL_MS = 10 * 60 * 1000
_seen: Dict[str, float] = {}


class GatewayConfig:
    def __init__(self, port: int, token: str) -> None:
        self.port = port
        self.token = token


def resolve_path(path: str) -> str:
    return os.path.expanduser(path)


def must_read(path: str, label: str) -> str:
    resolved = resolve_path(path)
    if not os.path.exists(resolved):
        raise RuntimeError(f"{label} not found: {resolved}")
    with open(resolved, "r", encoding="utf-8") as f:
        value = f.read().strip()
    if not value:
        raise RuntimeError(f"{label} is empty: {resolved}")
    return value


def load_gateway_config() -> GatewayConfig:
    raw = must_read(CLAWDBOT_CONFIG_PATH, "Clawdbot config")
    data = json.loads(raw)
    port = int(data.get("gateway", {}).get("port", 18789))
    token = data.get("gateway", {}).get("auth", {}).get("token")
    if not token:
        raise RuntimeError("gateway.auth.token missing in Clawdbot config")
    return GatewayConfig(port=port, token=str(token))


def is_duplicate(message_id: Optional[str]) -> bool:
    if not message_id:
        return False
    now = time.time() * 1000
    expired = [k for k, ts in _seen.items() if now - ts > SEEN_TTL_MS]
    for k in expired:
        _seen.pop(k, None)
    if message_id in _seen:
        return True
    _seen[message_id] = now
    return False


def extract_text(payload: Dict[str, Any]) -> str:
    text_field = payload.get("text")
    if isinstance(text_field, dict) and text_field.get("content"):
        return str(text_field["content"]).strip()
    if isinstance(text_field, str):
        return text_field.strip()
    if isinstance(payload.get("content"), str):
        return payload["content"].strip()
    msg = payload.get("msg") or {}
    if isinstance(msg, dict) and msg.get("text", {}).get("content"):
        return str(msg["text"]["content"]).strip()
    return ""


def should_respond_in_group(text: str, payload: Dict[str, Any]) -> bool:
    if payload.get("isInAtList"):
        return True
    at_users = payload.get("atUsers") or []
    if BOT_ID and any(user.get("dingtalkId") == BOT_ID or user.get("staffId") == BOT_ID or user.get("userId") == BOT_ID for user in at_users):
        return True
    if BOT_NAME and BOT_NAME in text:
        return True
    lowered = text.lower()
    if text.endswith("?") or text.endswith("？"):
        return True
    if any(word in lowered.split() for word in ["why", "how", "what", "when", "where", "who", "help"]):
        return True
    verbs = ["帮", "麻烦", "请", "能否", "可以", "解释", "看看", "排查", "分析", "总结", "写", "改", "修", "查", "对比", "翻译"]
    if any(v in text for v in verbs):
        return True
    if lowered.startswith(("alen", "clawdbot", "bot", "assistant")):
        return True
    return False


def timing_safe_equal(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    return hmac.compare_digest(a.encode(), b.encode())


def verify_signature(request: web.Request) -> bool:
    if not SIGNING_SECRET:
        return True
    timestamp = request.headers.get("timestamp") or request.rel_url.query.get("timestamp")
    sign = request.headers.get("sign") or request.rel_url.query.get("sign")
    if not timestamp or not sign:
        return False
    decoded_sign = unquote(sign)
    string_to_sign = f"{timestamp}\n{SIGNING_SECRET}"
    expected = hmac.new(SIGNING_SECRET.encode(), string_to_sign.encode(), "sha256").digest()
    import base64

    expected_b64 = base64.b64encode(expected).decode()
    return timing_safe_equal(decoded_sign, expected_b64)


def build_session_key(payload: Dict[str, Any]) -> str:
    conversation_id = payload.get("conversationId") or payload.get("conversation_id")
    sender_id = (
        payload.get("senderId")
        or payload.get("senderStaffId")
        or payload.get("sender", {}).get("staffId")
        or payload.get("sender", {}).get("userId")
    )
    msg_id = payload.get("msgId") or payload.get("msg_id") or payload.get("messageId") or payload.get("msg", {}).get("id")
    return f"dingtalk:{conversation_id or sender_id or msg_id or uuid.uuid4()}"


async def ask_gateway(config: GatewayConfig, text: str, session_key: str) -> str:
    uri = f"ws://127.0.0.1:{config.port}"
    async with websockets.connect(uri) as ws:
        run_id: Optional[str] = None
        buf = ""
        while True:
            raw = await ws.recv()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue

            if msg.get("type") == "event" and msg.get("event") == "connect.challenge":
                await ws.send(
                    json.dumps(
                        {
                            "type": "req",
                            "id": "connect",
                            "method": "connect",
                            "params": {
                                "minProtocol": 3,
                                "maxProtocol": 3,
                                "client": {
                                    "id": "gateway-client",
                                    "version": "0.2.0",
                                    "platform": "macos",
                                    "mode": "backend",
                                },
                                "role": "operator",
                                "scopes": ["operator.read", "operator.write"],
                                "auth": {"token": config.token},
                                "locale": "zh-CN",
                                "userAgent": "dingtalk-moltbot-bridge",
                            },
                        }
                    )
                )
                continue

            if msg.get("type") == "res" and msg.get("id") == "connect":
                if not msg.get("ok"):
                    raise RuntimeError(msg.get("error", {}).get("message", "connect failed"))
                await ws.send(
                    json.dumps(
                        {
                            "type": "req",
                            "id": "agent",
                            "method": "agent",
                            "params": {
                                "message": text,
                                "agentId": CLAWDBOT_AGENT_ID,
                                "sessionKey": session_key,
                                "deliver": False,
                                "idempotencyKey": str(uuid.uuid4()),
                            },
                        }
                    )
                )
                continue

            if msg.get("type") == "res" and msg.get("id") == "agent":
                if not msg.get("ok"):
                    raise RuntimeError(msg.get("error", {}).get("message", "agent error"))
                payload = msg.get("payload", {})
                run_id = payload.get("runId")
                continue

            if msg.get("type") == "event" and msg.get("event") == "agent":
                payload = msg.get("payload") or {}
                if run_id and payload.get("runId") != run_id:
                    continue
                if payload.get("stream") == "assistant":
                    data = payload.get("data") or {}
                    if isinstance(data.get("text"), str):
                        buf = data["text"]
                    elif isinstance(data.get("delta"), str):
                        buf += data["delta"]
                    continue
                if payload.get("stream") == "lifecycle":
                    phase = payload.get("data", {}).get("phase")
                    if phase == "end":
                        return buf.strip()
                    if phase == "error":
                        raise RuntimeError(payload.get("data", {}).get("message", "agent error"))


async def send_dingtalk_text(session: ClientSession, webhook: str, text: str) -> None:
    async with session.post(webhook, json={"msgtype": "text", "text": {"content": text}}) as res:
        if res.status >= 400:
            detail = await res.text()
            raise RuntimeError(f"DingTalk send failed: {res.status} {detail}".strip())


async def process_message(
    payload: Dict[str, Any],
    config: GatewayConfig,
    session: ClientSession,
    session_webhook: str,
) -> Optional[Dict[str, Any]]:
    msg_id = payload.get("msgId") or payload.get("msg_id") or payload.get("messageId") or payload.get("msg", {}).get("id")
    if is_duplicate(msg_id):
        return None

    text = extract_text(payload)
    if not text:
        return None

    is_group = str(payload.get("conversationType", "")) == "2" or payload.get("chatType") == "group"
    if is_group:
        text = re.sub(r"@[^\s]+\\s*", "", text).strip()
        if not text or not should_respond_in_group(text, payload):
            return None

    session_key = build_session_key(payload)

    thinking_task: Optional[asyncio.Task[None]] = None

    async def send_thinking() -> None:
        await asyncio.sleep(max(0, THINKING_THRESHOLD_MS) / 1000)
        if session_webhook:
            try:
                await send_dingtalk_text(session, session_webhook, "Thinking...")
            except Exception:
                return

    if session_webhook and THINKING_THRESHOLD_MS > 0:
        thinking_task = asyncio.create_task(send_thinking())

    reply = ""
    try:
        reply = await ask_gateway(config, text, session_key)
    except Exception as exc:
        reply = f"(error) {exc}"
    finally:
        if thinking_task:
            thinking_task.cancel()

    trimmed = reply.strip()
    if not trimmed or trimmed == "NO_REPLY" or trimmed.endswith("NO_REPLY"):
        return None

    if session_webhook:
        await send_dingtalk_text(session, session_webhook, reply)
        return None

    return {"msgtype": "text", "text": {"content": reply}}


async def handle_request(request: web.Request) -> web.Response:
    if request.method == "GET":
        return web.Response(text="OK")

    if request.method != "POST" or request.path != PATH:
        return web.Response(status=404, text="Not Found")

    if not verify_signature(request):
        return web.Response(status=401, text="Invalid signature")

    try:
        payload = await request.json()
    except json.JSONDecodeError:
        return web.Response(status=400, text="Invalid JSON")

    if payload.get("challenge"):
        return web.json_response({"challenge": payload["challenge"]})

    session_webhook = payload.get("sessionWebhook") if isinstance(payload.get("sessionWebhook"), str) else ""

    config = request.app["gateway_config"]
    session = request.app["http_session"]

    if session_webhook:
        asyncio.create_task(process_message(payload, config, session, session_webhook))
        return web.Response(text="OK")

    response_payload = await process_message(payload, config, session, session_webhook)
    if response_payload:
        return web.json_response(response_payload)
    return web.Response(text="OK")


def main() -> None:
    config = load_gateway_config()
    app = web.Application()
    app["gateway_config"] = config
    app["http_session"] = None
    app.router.add_route("*", PATH, handle_request)

    async def on_startup(_: web.Application) -> None:
        app["http_session"] = ClientSession()

    async def on_cleanup(_: web.Application) -> None:
        session = app["http_session"]
        if session:
            await session.close()

    app.on_startup.append(on_startup)

    app.on_cleanup.append(on_cleanup)
    print(f"[OK] DingTalk bridge listening on :{PORT}{PATH}")
    web.run_app(app, port=PORT)


if __name__ == "__main__":
    main()
