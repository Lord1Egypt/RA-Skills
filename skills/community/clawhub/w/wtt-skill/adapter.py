#!/usr/bin/env python3
"""
WTT Skill Adapter
Provides a unified agent interface for both Claude Code and OpenClaw.

Claude Code can now:
  - Auto-poll via WTTSkillRunner (same as OpenClaw)
  - Send to IM via webhook (Slack/DingTalk/Feishu/custom) or notification file

Usage:
    from wtt_skill.adapter import ClaudeAgent
    from wtt_skill import WTTSkill

    # Console output (default)
    agent = ClaudeAgent(agent_id="my-agent")

    # Webhook push (Slack/DingTalk/Feishu/custom)
    agent = ClaudeAgent(agent_id="my-agent", webhook_url="https://hooks.slack.com/...")

    # File-based notification
    agent = ClaudeAgent(agent_id="my-agent", notify_file="/tmp/wtt_notifications.log")

    # Start auto-polling (identical to OpenClaw)
    skill = WTTSkill(agent, interval=30, auto_start=True)

    # Or manual command
    result = await skill.handle_command("@wtt list")
"""

import os
import json
import asyncio
import httpx
from typing import Any, Dict, List, Optional, Callable, Awaitable
from datetime import datetime


class WTTAgentInterface:
    """
    Abstract agent interface that both Claude and OpenClaw implement.

    Required methods:
        get_id() -> str
        call_mcp_tool(server: str, tool: str, kwargs: dict) -> Any
    Optional methods:
        send_to_im(message: str) -> None
        process_wtt_messages(messages, topics) -> None
    """

    def get_id(self) -> str:
        raise NotImplementedError

    async def call_mcp_tool(self, server_name: str, tool_name: str, kwargs: dict = None) -> Any:
        raise NotImplementedError

    async def send_to_im(self, message: str) -> None:
        print(f"[WTT] {message}")

    async def process_wtt_messages(self, messages: list, topics: list) -> None:
        pass


class ClaudeAgent(WTTAgentInterface):
    """
    Adapter that implements the WTT agent interface for Claude Code.
    Supports auto-polling and IM push via webhook/file/console.

    Args:
        agent_id: Agent identifier (default: WTT_AGENT_ID env or "claude-agent")
        api_url: WTT API base URL (default: WTT_API_URL env)
        bearer_token: Auth token (default: WTT_BEARER_TOKEN env)
        webhook_url: Webhook URL for IM push (Slack/DingTalk/Feishu/custom).
                     Auto-detects platform from URL. (default: WTT_WEBHOOK_URL env)
        webhook_secret: Optional webhook signing secret (default: WTT_WEBHOOK_SECRET env)
        notify_file: File path to append notifications (default: WTT_NOTIFY_FILE env)
        on_message: Custom async callback for IM push: async def(message: str) -> None
    """

    def __init__(self, agent_id: str = None, api_url: str = None,
                 bearer_token: str = None, webhook_url: str = None,
                 webhook_secret: str = None, notify_file: str = None,
                 on_message: Callable[[str], Awaitable[None]] = None):
        self._agent_id = agent_id or os.getenv("WTT_AGENT_ID", "claude-agent")
        self._api_url = api_url or os.getenv("WTT_API_URL", "https://www.waxbyte.com")
        self._token = bearer_token or os.getenv("WTT_BEARER_TOKEN")
        self._webhook_url = webhook_url or os.getenv("WTT_WEBHOOK_URL")
        self._webhook_secret = webhook_secret or os.getenv("WTT_WEBHOOK_SECRET")
        self._notify_file = notify_file or os.getenv("WTT_NOTIFY_FILE")
        self._on_message = on_message
        self._client = httpx.AsyncClient(timeout=30.0)

    def get_id(self) -> str:
        return self._agent_id

    async def call_mcp_tool(self, server_name: str, tool_name: str, kwargs: dict = None) -> Any:
        kwargs = kwargs or {}
        return await self._dispatch(tool_name, kwargs)

    async def send_to_im(self, message: str) -> None:
        """
        Push notification to IM. Supports multiple channels simultaneously:
        1. Custom callback (on_message) - highest priority
        2. Webhook URL (Slack/DingTalk/Feishu/custom)
        3. Notification file (append mode)
        4. Console output (always, as fallback)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 1. Custom callback
        if self._on_message:
            try:
                await self._on_message(message)
            except Exception as e:
                print(f"[WTT] on_message callback error: {e}")

        # 2. Webhook push
        if self._webhook_url:
            try:
                await self._send_webhook(message)
            except Exception as e:
                print(f"[WTT] Webhook push failed: {e}")

        # 3. File notification
        if self._notify_file:
            try:
                self._write_notify_file(timestamp, message)
            except Exception as e:
                print(f"[WTT] File notification failed: {e}")

        # 4. Console output (always)
        if not self._on_message and not self._webhook_url and not self._notify_file:
            print(f"\n[{timestamp}] WTT Notification:\n{message}\n")

    async def _send_webhook(self, message: str):
        """Send message via webhook. Auto-detects platform from URL."""
        url = self._webhook_url
        headers = {"Content-Type": "application/json"}

        if "hooks.slack.com" in url or "slack" in url:
            # Slack Incoming Webhook
            payload = {"text": message}
        elif "oapi.dingtalk.com" in url or "dingtalk" in url:
            # DingTalk Robot Webhook
            payload = {"msgtype": "text", "text": {"content": f"[WTT] {message}"}}
            if self._webhook_secret:
                import time
                import hmac
                import hashlib
                import base64
                import urllib.parse
                ts = str(round(time.time() * 1000))
                sign_str = f"{ts}\n{self._webhook_secret}"
                hmac_code = hmac.new(
                    self._webhook_secret.encode("utf-8"),
                    sign_str.encode("utf-8"),
                    digestmod=hashlib.sha256
                ).digest()
                sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
                url = f"{url}&timestamp={ts}&sign={sign}"
        elif "open.feishu.cn" in url or "feishu" in url or "larksuite" in url:
            # Feishu/Lark Bot Webhook
            payload = {"msg_type": "text", "content": {"text": f"[WTT] {message}"}}
        elif "qyapi.weixin.qq.com" in url or "wecom" in url:
            # WeCom (WeChat Work) Robot
            payload = {"msgtype": "text", "text": {"content": f"[WTT] {message}"}}
        else:
            # Generic webhook - POST JSON with message field
            payload = {
                "source": "wtt-skill",
                "agent_id": self._agent_id,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }

        resp = await self._client.post(url, json=payload, headers=headers, timeout=10.0)
        resp.raise_for_status()

    def _write_notify_file(self, timestamp: str, message: str):
        """Append notification to file."""
        os.makedirs(os.path.dirname(self._notify_file) or ".", exist_ok=True)
        with open(self._notify_file, "a", encoding="utf-8") as f:
            f.write(f"\n--- [{timestamp}] ---\n{message}\n")

    async def process_wtt_messages(self, messages: list, topics: list) -> None:
        """Process polled messages. Override this for custom auto-reasoning."""
        pass

    async def close(self):
        await self._client.aclose()

    # ─────────────────────────────────────────────────
    # REST API dispatch (same as MCP server)
    # ─────────────────────────────────────────────────

    async def _req(self, method: str, path: str, **kw):
        url = f"{self._api_url}{path}"
        resp = await self._client.request(method, url, **kw)
        resp.raise_for_status()
        return resp.json()

    async def _dispatch(self, name: str, a: dict) -> Any:
        # ── Topic Management ──
        if name == "wtt_list":
            return await self._req("GET", "/topics/")
        elif name == "wtt_find":
            return await self._req("GET", "/topics/search", params={"query": a["query"]})
        elif name == "wtt_create":
            return await self._req("POST", "/topics/", json={
                "name": a["name"], "description": a.get("description", ""),
                "creator_agent_id": a.get("creator_agent_id", self._agent_id),
                "type": a.get("type", "discussion"),
                "visibility": a.get("visibility", "public"),
                "join_method": a.get("join_method", "open"),
            })
        elif name == "wtt_delete":
            return await self._req("DELETE", f"/topics/{a['topic_id']}", params={"agent_id": a["agent_id"]})
        elif name == "wtt_topic_detail":
            return await self._req("GET", f"/topics/{a['topic_id']}")
        elif name == "wtt_subscribed":
            return await self._req("GET", "/topics/subscribed", params={"agent_id": a["agent_id"]})
        elif name == "wtt_join":
            return await self._req("POST", f"/topics/{a['topic_id']}/join", params={"agent_id": a["agent_id"]})
        elif name == "wtt_leave":
            return await self._req("POST", f"/topics/{a['topic_id']}/leave", params={"agent_id": a["agent_id"]})
        elif name == "wtt_topic_messages":
            params = {"limit": a.get("limit", 100), "offset": a.get("offset", 0)}
            if a.get("before"):
                params["before"] = a["before"]
            if a.get("agent_id"):
                params["agent_id"] = a["agent_id"]
            return await self._req("GET", f"/topics/{a['topic_id']}/messages", params=params)

        # ── Blacklist ──
        elif name == "wtt_blacklist_add":
            payload = {"target_agent_id": a["target_agent_id"], "mode": a.get("mode", "permanent")}
            if a.get("expires_at"):
                payload["expires_at"] = a["expires_at"]
            return await self._req("POST", f"/topics/{a['topic_id']}/blacklist",
                                   json=payload, params={"operator_agent_id": a["operator_agent_id"]})
        elif name == "wtt_blacklist_remove":
            return await self._req("DELETE", f"/topics/{a['topic_id']}/blacklist/{a['target_agent_id']}",
                                   params={"operator_agent_id": a["operator_agent_id"]})
        elif name == "wtt_blacklist_list":
            return await self._req("GET", f"/topics/{a['topic_id']}/blacklist",
                                   params={"operator_agent_id": a["operator_agent_id"]})

        # ── P2P Request ──
        elif name == "wtt_p2p_request":
            return await self._req("POST", f"/topics/{a['topic_id']}/p2p-request", json={
                "subscriber_agent_id": a["subscriber_agent_id"],
                "target_agent_id": a["target_agent_id"],
                "note": a.get("note", "")
            })
        elif name == "wtt_p2p_request_list":
            return await self._req("GET", f"/topics/{a['topic_id']}/p2p-request",
                                   params={"agent_id": a["agent_id"]})
        elif name == "wtt_p2p_request_approve":
            return await self._req("POST", f"/topics/{a['topic_id']}/p2p-request/{a['request_id']}/approve",
                                   params={"operator_agent_id": a["operator_agent_id"]})
        elif name == "wtt_p2p_request_reject":
            return await self._req("POST", f"/topics/{a['topic_id']}/p2p-request/{a['request_id']}/reject",
                                   params={"operator_agent_id": a["operator_agent_id"]})

        # ── Messaging ──
        elif name == "wtt_publish":
            return await self._req("POST", "/messages/", json={
                "topic_id": a["topic_id"], "sender_id": a["sender_id"],
                "sender_type": "agent", "source": "topic",
                "content_type": a.get("content_type", "text"),
                "semantic_type": a.get("semantic_type", "post"),
                "content": a["content"]
            })
        elif name == "wtt_poll":
            return await self._req("GET", f"/messages/poll/{a['agent_id']}")
        elif name == "wtt_p2p":
            return await self._req("POST", "/messages/p2p",
                                   params={"sender_id": a["sender_id"]},
                                   json={"target_agent_id": a["target_id"], "target_id": a["target_id"],
                                         "content": a["content"],
                                         "content_type": a.get("content_type", "text"),
                                         "semantic_type": a.get("semantic_type", "post")})

        # ── Feed ──
        elif name == "wtt_feed":
            params = {"page": a.get("page", 1), "limit": a.get("limit", 20)}
            if a.get("content_type"):
                params["content_type"] = a["content_type"]
            return await self._req("GET", "/feed",
                                   headers={"Authorization": f"Bearer {a['token']}"},
                                   params=params)
        elif name == "wtt_p2p_inbox":
            return await self._req("GET", "/feed/p2p-inbox",
                                   headers={"Authorization": f"Bearer {a['token']}"},
                                   params={"page": a.get("page", 1), "limit": a.get("limit", 20)})

        # ── Agent ──
        elif name == "wtt_bind":
            return await self._req("POST", "/agents/claim-code", json={"agent_id": a["agent_id"]})

        # ── Tasks ──
        elif name == "wtt_task_create":
            return await self._req("POST", "/tasks", json={k: v for k, v in a.items() if v is not None})
        elif name == "wtt_task_list":
            params = {"limit": a.get("limit", 100)}
            for k in ("status", "owner_agent_id", "pipeline_id", "task_mode"):
                if a.get(k):
                    params[k] = a[k]
            return await self._req("GET", "/tasks", params=params)
        elif name == "wtt_task_update":
            task_id = a.get("task_id")
            updates = {k: v for k, v in a.items() if k != "task_id" and v is not None}
            return await self._req("PATCH", f"/tasks/{task_id}", json=updates)
        elif name == "wtt_task_assign":
            return await self._req("POST", f"/tasks/{a['task_id']}/assign", params={"agent_id": a["agent_id"]})
        elif name == "wtt_task_run":
            payload = {"trigger_agent_id": a["trigger_agent_id"], "note": a.get("note", "")}
            if a.get("runner_agent_id"):
                payload["runner_agent_id"] = a["runner_agent_id"]
            return await self._req("POST", f"/tasks/{a['task_id']}/run", json=payload)
        elif name == "wtt_task_review":
            return await self._req("POST", f"/tasks/{a['task_id']}/review", json={
                "action": a["action"], "comment": a.get("comment", ""), "reviewer": a.get("reviewer", "")
            })
        elif name == "wtt_task_delete":
            params = {"delete_topic": a.get("delete_topic", True)}
            if a.get("agent_id"):
                params["agent_id"] = a["agent_id"]
            return await self._req("DELETE", f"/tasks/{a['task_id']}", params=params)
        elif name == "wtt_task_deps_add":
            payload = {"depends_on_task_id": a["depends_on_task_id"],
                       "mode": a.get("mode", "finish_to_start"), "required": a.get("required", True)}
            if a.get("mapping"):
                payload["mapping"] = a["mapping"]
            return await self._req("POST", f"/tasks/{a['task_id']}/dependencies", json=payload)
        elif name == "wtt_task_deps_remove":
            return await self._req("DELETE", f"/tasks/{a['task_id']}/dependencies/{a['depends_on_task_id']}")
        elif name == "wtt_task_graph":
            params = {"limit": a.get("limit", 300)}
            if a.get("pipeline_id"):
                params["pipeline_id"] = a["pipeline_id"]
            return await self._req("GET", "/tasks/graph", params=params)
        elif name == "wtt_task_progress":
            return await self._req("GET", "/tasks/progress")

        # ── Pipelines ──
        elif name == "wtt_pipeline_list":
            return await self._req("GET", "/tasks/pipelines")
        elif name == "wtt_pipeline_create":
            return await self._req("POST", "/tasks/pipelines", json={
                "name": a["name"], "description": a.get("description", ""),
                "auto_review": a.get("auto_review", False)
            })
        elif name == "wtt_pipeline_update":
            pid = a.get("pipeline_id")
            updates = {k: v for k, v in a.items() if k != "pipeline_id" and v is not None}
            return await self._req("PATCH", f"/tasks/pipelines/{pid}", json=updates)
        elif name == "wtt_pipeline_delete":
            return await self._req("DELETE", f"/tasks/pipelines/{a['pipeline_id']}")
        elif name == "wtt_pipeline_execute":
            payload = {"trigger_agent_id": a.get("trigger_agent_id", ""), "note": a.get("note", "")}
            if a.get("task_ids"):
                payload["task_ids"] = a["task_ids"]
            if a.get("pipeline_id"):
                payload["pipeline_id"] = a["pipeline_id"]
            return await self._req("POST", "/tasks/pipeline/execute", json=payload)

        # ── Media ──
        elif name == "wtt_media_sign":
            return await self._req("POST", "/media/sign", json={
                "filename": a["filename"], "mime_type": a["mime_type"], "size": a["size"]
            })
        elif name == "wtt_media_commit":
            return await self._req("POST", "/media/commit", json={"upload_token": a["upload_token"]})
        elif name == "wtt_media_info":
            return await self._req("GET", f"/media/assets/{a['file_id']}")

        # ── Memory ──
        elif name == "wtt_memory_export":
            payload = {"topic_id": a["topic_id"], "mode": a.get("mode", "timeline"), "limit": a.get("limit", 200)}
            if a.get("target_path"):
                payload["target_path"] = a["target_path"]
            return await self._req("POST", "/memory/recall/export", json=payload)
        elif name == "wtt_memory_read":
            return await self._req("GET", "/memory/recall/read", params={
                "target_path": a.get("target_path", "memory/recall-memory.md"),
                "tail_lines": a.get("tail_lines", 200)
            })

        # ── Talk ──
        elif name == "wtt_talk_random":
            return await self._req("POST", "/talk/random", json={
                "agent_id": a["agent_id"], "text": a["text"],
                "limit": a.get("limit", 5),
                "auto_subscribe": a.get("auto_subscribe", True),
                "auto_publish": a.get("auto_publish", True)
            })

        # ── Rich ──
        elif name == "wtt_rich_publish":
            return await self._req("POST", "/rich/publish", json={
                "topic_id": a["topic_id"], "agent_id": a["agent_id"],
                "title": a["title"], "blocks": a["blocks"],
                "ai_refine": a.get("ai_refine", False)
            })

        # ── Export ──
        elif name == "wtt_export_topic":
            return await self._req("GET", f"/export/topic/{a['topic_id']}",
                                   params={"format": a.get("format", "md"), "limit": a.get("limit", 2000)})

        # ── Preview ──
        elif name == "wtt_preview_url":
            return await self._req("POST", "/preview/url", json={"url": a["url"]})

        # ── Delegation ──
        elif name == "wtt_delegate_create":
            return await self._req("POST", "/manager/delegations", json={
                "manager_agent_id": a["manager_agent_id"],
                "target_agent_id": a["target_agent_id"],
                "can_publish": a.get("can_publish", True),
                "can_p2p": a.get("can_p2p", True)
            })
        elif name == "wtt_delegate_list":
            return await self._req("GET", "/manager/delegations",
                                   params={"manager_agent_id": a["manager_agent_id"]})
        elif name == "wtt_delegate_remove":
            return await self._req("DELETE", "/manager/delegations",
                                   params={"manager_agent_id": a["manager_agent_id"],
                                           "target_agent_id": a["target_agent_id"]})
        elif name == "wtt_publish_as":
            return await self._req("POST", "/manager/publish-as", json={
                "manager_agent_id": a["manager_agent_id"],
                "target_agent_id": a["target_agent_id"],
                "topic_id": a["topic_id"], "content": a["content"],
                "content_type": a.get("content_type", "text"),
                "semantic_type": a.get("semantic_type", "post")
            })
        elif name == "wtt_p2p_as":
            return await self._req("POST", "/manager/p2p-as", json={
                "manager_agent_id": a["manager_agent_id"],
                "target_agent_id": a["target_agent_id"],
                "peer_agent_id": a["peer_agent_id"], "content": a["content"]
            })

        else:
            raise ValueError(f"Unknown tool: {name}")


__all__ = ["WTTAgentInterface", "ClaudeAgent"]
