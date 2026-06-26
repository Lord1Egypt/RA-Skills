#!/usr/bin/env python3
"""
WTT Skill Launcher
Supports WebSocket (real-time bidirectional) and polling (fallback).
In WebSocket mode, send/receive share one connection without relying on MCP server polling.
"""
import asyncio
import json
import os
import re
import signal
import sys
import logging
import uuid
import unicodedata
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

_DEFAULT_WS_URL = "wss://www.waxbyte.com/ws"


def _resolve_ws_url(ws_url: str = None) -> str:
    """Resolve WS URL from explicit param → env var → default."""
    if ws_url:
        return ws_url
    env_url = os.getenv("WTT_WS_URL", "")
    if env_url:
        return env_url
    api_url = os.getenv("WTT_API_URL", "")
    if api_url:
        # Derive ws(s):// from http(s)://
        return api_url.replace("https://", "wss://").replace("http://", "ws://").rstrip("/") + "/ws"
    return _DEFAULT_WS_URL


class WTTSkillRunner:
    """WTT Skill runner - WebSocket-first runtime."""

    def __init__(self, agent, interval: int = 30, mode: str = "websocket",
                 ws_url: str = None):
        self.agent = agent
        self.interval = interval
        self.mode = mode
        self.ws_url = _resolve_ws_url(ws_url)
        self.running = False
        self.task: Optional[asyncio.Task] = None
        self._ws = None
        self._ws_connected = False
        self._reconnect_delay = 2
        self._pending_requests: Dict[str, asyncio.Future] = {}
        self._subscribed_topics: Dict[str, dict] = {}  # topic_id -> topic metadata cache
        self._recent_notifications: Dict[str, float] = {}
        self._recent_thinking_markers: Dict[str, float] = {}  # topic_id -> ts

        try:
            from wtt_skill.handler import WTTSkillHandler, WTTPoller
        except ImportError:
            from handler import WTTSkillHandler, WTTPoller
        self.handler = WTTSkillHandler(agent, ws_runner=self)
        self.poller = WTTPoller(agent)

    def _notification_key(self, message: dict) -> str:
        # Prefer stable message id to avoid over-suppressing IM notifications
        mid = message.get("id") or message.get("message_id")
        if mid:
            return f"mid:{mid}"
        topic_id = message.get("topic_id", "")
        sender = message.get("sender_id", "")
        content = (message.get("content") or "").strip()
        return f"{topic_id}|{sender}|{content[:300]}"

    def _should_notify(self, message: dict, ttl_sec: int = 20) -> bool:
        # Temporary: always notify to guarantee IM visibility for topic feed debugging.
        # We'll reintroduce bounded dedupe once the stream is stable.
        return True

    def _is_task_trigger_message(self, message: dict) -> bool:
        content = (message.get("content") or "").strip()
        if not content:
            return False
        lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
        if not lines:
            return False
        old_fmt = all(ln.startswith("title=") or ln.startswith("description=") for ln in lines)
        new_fmt = any("Task Title:" in ln for ln in lines) and any("Task Desc:" in ln for ln in lines)
        return old_fmt or new_fmt

    _PROGRESS_PATTERNS_IM = [
        re.compile(r'^Time:\s*\d{1,2}:\d{2}:\d{2}\s*\n\s*Progress:\s*\d+%', re.MULTILINE),
        re.compile(r'^Status:\s*\[Task:', re.MULTILINE),
        re.compile(r'^\[STATUS\]\s*(Started|Completed)', re.MULTILINE),
        re.compile(r'^Plan Mode result:', re.MULTILINE),
        re.compile(r'^Plan Mode结果', re.MULTILINE),
        re.compile(r'^Progress:\s*\d+%\s*$', re.MULTILINE),
        re.compile(r'^\[TASK_STATUS\]', re.MULTILINE),
        re.compile(r'^\[TASK_RUN\]', re.MULTILINE),
    ]

    def _should_suppress_im(self, message: dict) -> bool:
        """Suppress progress/status messages from IM unless env override."""
        if os.getenv("WTT_IM_SHOW_PROGRESS", "0").lower() in ("1", "true", "yes"):
            return False
        content = (message.get("content") or "").strip()
        if not content:
            return False
        return any(p.search(content) for p in self._PROGRESS_PATTERNS_IM)

    def _humanize_notification(self, message: dict) -> str:
        content = (message.get("content") or "").strip()
        topic_id = message.get("topic_id", "")
        if not content:
            return ""
        # prepend topic marker so IM stream can be clearly identified and searchable
        out = f"[Topic:{topic_id}]\n{content}" if topic_id else content
        # Telegram practical safety: avoid overlong push body
        if len(out) > 3500:
            out = out[:3500] + "\n...(truncated)"
        return out

    def _mark_thinking_pushed(self, topic_id: str):
        if not topic_id:
            return
        self._recent_thinking_markers[topic_id] = asyncio.get_event_loop().time()

    def _recently_pushed_thinking(self, topic_id: str, ttl_sec: int = 15) -> bool:
        if not topic_id:
            return False
        now = asyncio.get_event_loop().time()
        self._recent_thinking_markers = {
            k: ts for k, ts in self._recent_thinking_markers.items() if (now - ts) < ttl_sec
        }
        return topic_id in self._recent_thinking_markers

    async def start(self):
        """Start message intake"""
        if self.running:
            print("⚠️  WTT Skill is already running")
            return

        self.running = True

        if self.mode == "websocket":
            self.task = asyncio.create_task(self._ws_loop())
            print(f"✅ WTT Skill started [WebSocket real-time mode]")
            print(f"   WebSocket: {self.ws_url}/{self.agent.get_id()}")
            print("   Notifications and reasoning via WebSocket only")
        else:
            self.task = asyncio.create_task(self._poll_loop())
            print(f"✅ WTT Skill started [polling mode], every {self.interval}s")

    async def stop(self):
        """Stop"""
        if not self.running:
            return
        self.running = False
        if self._ws:
            try:
                await self._ws.close()
            except Exception:
                pass
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        print("✅ WTT Skill stopped")

    # ── WebSocket Bidirectional ────────────────────────────────────

    async def send_action(self, action: str, payload: dict = None, timeout: float = 15) -> dict:
        """Send an action to WTT server via WebSocket and wait for result.
        
        Returns the action result data, or raises on error/timeout.
        Falls back to None if WS not connected (caller should use MCP fallback).
        """
        if not self._ws_connected or not self._ws:
            return None

        request_id = str(uuid.uuid4())[:8]
        msg = {"action": action, "request_id": request_id, **(payload or {})}

        future: asyncio.Future = asyncio.get_event_loop().create_future()
        self._pending_requests[request_id] = future

        try:
            await self._ws.send(json.dumps(msg, ensure_ascii=False, default=str))
            result = await asyncio.wait_for(future, timeout=timeout)
            if not result.get("ok"):
                raise RuntimeError(result.get("error", "Unknown error"))
            return result.get("data")
        except asyncio.TimeoutError:
            raise RuntimeError(f"WS action '{action}' timed out after {timeout}s")
        finally:
            self._pending_requests.pop(request_id, None)

    async def _ws_loop(self):
        """WebSocket main loop: bidirectional + auto-reconnect"""
        try:
            import websockets
        except ImportError:
            print("❌ websockets package not installed; cannot start WebSocket mode")
            print("   Install: pip install websockets")
            return

        agent_id = self.agent.get_id()
        url = f"{self.ws_url}/{agent_id}"

        while self.running:
            try:
                async with websockets.connect(url, ping_interval=30, ping_timeout=10) as ws:
                    self._ws = ws
                    self._ws_connected = True
                    self._reconnect_delay = 2
                    print(f"🔗 WebSocket connected: {url}")

                    heartbeat_task = asyncio.create_task(self._heartbeat(ws))
                    # Refresh topic cache after message loop starts
                    refresh_task = asyncio.create_task(self._refresh_subscribed_topics())

                    try:
                        async for raw in ws:
                            if raw == "pong":
                                continue
                            try:
                                data = json.loads(raw)
                                await self._dispatch_ws_data(data)
                            except json.JSONDecodeError:
                                logger.warning("Non-JSON message: %s", raw[:100])
                    finally:
                        self._ws_connected = False
                        self._ws = None
                        heartbeat_task.cancel()
                        refresh_task.cancel()
                        for t in (heartbeat_task, refresh_task):
                            try:
                                await t
                            except (asyncio.CancelledError, Exception):
                                pass
                        # Cancel any pending requests
                        for rid, fut in self._pending_requests.items():
                            if not fut.done():
                                fut.set_exception(ConnectionError("WebSocket disconnected"))
                        self._pending_requests.clear()

            except asyncio.CancelledError:
                break
            except Exception as e:
                self._ws_connected = False
                self._ws = None
                print(f"⚠️  WebSocket disconnected: {e}")
                print(f"   {self._reconnect_delay}s then reconnect...")
                await asyncio.sleep(self._reconnect_delay)
                self._reconnect_delay = min(self._reconnect_delay * 1.5, 30)

    async def _dispatch_ws_data(self, data: dict):
        """Route incoming WS data: action results vs push messages."""
        msg_type = data.get("type", "")
        print(f"[WS DEBUG] Received message type: {msg_type}", flush=True)
        
        # Action result — resolve the pending future
        if msg_type == "action_result":
            request_id = data.get("request_id", "")
            future = self._pending_requests.get(request_id)
            if future and not future.done():
                future.set_result(data)
            return

        # Push message — handle asynchronously to avoid blocking action_result handling
        if msg_type == "new_message":
            print(f"[WS DEBUG] Handling new_message", flush=True)
            asyncio.create_task(self._handle_ws_message(data))

        # Task status change — trigger execution of new todo tasks
        if msg_type == "task_status":
            asyncio.create_task(self._handle_task_status_event(data))

    async def _refresh_subscribed_topics(self):
        """Fetch and cache subscribed topics (for task detection)."""
        try:
            result = await self.send_action("subscribed", {}, timeout=10)
            if result and isinstance(result, list):
                self._subscribed_topics = {t["id"]: t for t in result if "id" in t}
                print(f"📋 Cached {len(self._subscribed_topics)} subscribed topics")
        except Exception as e:
            print(f"⚠️ Failed to fetch subscribed topic list: {e}")

    async def _heartbeat(self, ws):
        """Send periodic ping keepalive"""
        while True:
            try:
                await asyncio.sleep(25)
                await ws.send("ping")
            except asyncio.CancelledError:
                break
            except Exception:
                break

    async def _handle_task_status_event(self, data: dict):
        """Handle task_status WS events — auto-execute new todo tasks on subscribed topics."""
        try:
            # Payload can be flat (task_id, status, topic_id) or nested under "task"
            task = data.get("task") or data.get("data") or {}
            status = str(task.get("status") or data.get("status") or "").lower()
            if status != "todo":
                return
            task_id = str(task.get("id") or task.get("task_id") or data.get("task_id") or "")
            topic_id = str(task.get("topic_id") or data.get("topic_id") or "")
            title = str(task.get("title") or data.get("title") or "")
            description = str(task.get("description") or data.get("description") or "")
            exec_mode = str(task.get("exec_mode") or data.get("exec_mode") or "reasoning")
            task_type = str(task.get("type") or task.get("task_type") or data.get("task_type") or "feature")
            if not task_id or not topic_id:
                return

            # Canonicalize with task table to avoid WS payload/task_id mismatch misrouting.
            if hasattr(self.agent, '_get_task'):
                canonical = await self.agent._get_task(task_id)
                if canonical:
                    canonical_topic = str(canonical.get("topic_id") or topic_id)
                    canonical_title = str(canonical.get("title") or "")

                    def _norm(s: str) -> str:
                        return re.sub(r"\s+", "", (s or "").strip().lower())

                    if topic_id and canonical_topic and canonical_topic != topic_id:
                        print(f"⚠️ [WS] Skip todo task due topic mismatch event_topic={topic_id} db_topic={canonical_topic} task={task_id[:12]}")
                        return
                    if title and canonical_title and _norm(title) != _norm(canonical_title):
                        print(f"⚠️ [WS] Skip todo task due title mismatch event={title[:24]!r} db={canonical_title[:24]!r} task={task_id[:12]}")
                        return

                    topic_id = canonical_topic or topic_id
                    title = canonical_title or title
                    description = str(canonical.get("description") or description)
                    exec_mode = str(canonical.get("exec_mode") or exec_mode)
                    task_type = str(canonical.get("task_type") or canonical.get("type") or task_type)

            # Only handle tasks on topics we're subscribed to
            if topic_id not in self._subscribed_topics:
                return

            if hasattr(self.agent, '_remember_topic_task_hint'):
                self.agent._remember_topic_task_hint(topic_id, task_id)

            print(f"📋 [WS] New todo task: {title[:30]} ({task_id[:12]})")
            if hasattr(self.agent, '_execute_task_run'):
                import asyncio
                asyncio.create_task(
                    self.agent._execute_task_run(topic_id, task_id, exec_mode, task_type, title, description)
                )
        except Exception as e:
            print(f"⚠️ _handle_task_status_event error: {e}")

    async def _handle_ws_message(self, data: dict):
        """Handle pushed WebSocket messages"""
        msg_type = data.get("type")
        if msg_type != "new_message":
            return

        message = data.get("message", {})
        topic_id = message.get("topic_id", "")

        # Auto-refresh cache when we receive a message for an unknown topic (e.g. newly created P2P)
        if topic_id and topic_id not in self._subscribed_topics:
            await self._refresh_subscribed_topics()

        content = (message.get("content") or "").strip()
        sender_id = str(message.get("sender_id") or "")
        sender_type = str(message.get("sender_type") or "").lower()

        # Consistent UX: only show thinking marker when inference will actually trigger
        will_infer = self._should_trigger_inference(message, topic_id)
        if sender_type == "human" and topic_id and content and will_infer and (not self._recently_pushed_thinking(topic_id)):
            await self._push_to_im(f"[Topic:{topic_id}]\n🤔 Agent thinking...")
            self._mark_thinking_pushed(topic_id)

        # Suppress duplicate thinking marker if upstream echoed it and we just pushed one
        if sender_id == self.agent.get_id() and "🤔 Agent thinking" in content and self._recently_pushed_thinking(topic_id):
            should_push = False
        else:
            should_push = self._should_notify(message) and (not self._should_suppress_im(message))

        if should_push:
            notification = self._humanize_notification(message)
            if notification:
                print(f"\n📬 {notification}\n")
                await self._push_to_im(notification)

        # Inference gating: only trigger for P2P / task topics, or @mention in discussion
        if hasattr(self.agent, "process_wtt_messages") and self._should_trigger_inference(message, topic_id):
            topic_meta = self._subscribed_topics.get(topic_id)
            topics_ctx = [topic_meta] if topic_meta else []
            try:
                infer_timeout = int(os.getenv("WTT_INFER_TIMEOUT", "1800"))
                await asyncio.wait_for(
                    self.agent.process_wtt_messages([message], topics_ctx),
                    timeout=infer_timeout,
                )
            except asyncio.TimeoutError:
                print(f"⚠️ Auto-reasoning timeout (>{infer_timeout}s)")
            except Exception as e:
                print(f"❌ Auto-reasoning failed: {e}")
        elif hasattr(self.agent, "process_wtt_messages"):
            print(f"⏭️ Skipped inference for topic {topic_id[:12]} (no @mention or broadcast)")

    # ── Polling Mode ────────────────────────────────────────────────

    async def _poll_loop(self):
        """Background polling loop"""
        print(f"🔄 Start polling WTT messages (interval: {self.interval}s）")

        while self.running:
            try:
                await self._do_single_poll()
                await asyncio.sleep(self.interval)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"❌ Polling error: {e}")
                await asyncio.sleep(self.interval)

    async def _do_single_poll(self):
        """Execute one polling round"""
        if self.mode == "websocket":
            return
        try:
            polled = await self.poller.poll_raw()
            if polled:
                messages = polled.get("messages", [])
                topics = polled.get("topics", [])

                # Only notify via polling when WS is disconnected to avoid duplicates
                if not self._ws_connected:
                    for m in messages:
                        if self._should_notify(m) and not self._should_suppress_im(m):
                            notification = self._humanize_notification(m)
                            if notification:
                                print(f"\n📬 {notification}\n")
                                await self._push_to_im(notification)

                # Inference gating: filter to messages that should trigger inference
                if hasattr(self.agent, "process_wtt_messages"):
                    infer_msgs = [m for m in messages if self._should_trigger_inference(m, m.get("topic_id", ""))]
                    if infer_msgs:
                        try:
                            await asyncio.wait_for(
                                self.agent.process_wtt_messages(infer_msgs, topics),
                                timeout=45,
                            )
                        except asyncio.TimeoutError:
                            print("⚠️ Auto-reasoning timeout，已跳过本轮")
                        except Exception as e:
                            print(f"❌ Auto-reasoning failed: {e}")
                    skipped = len(messages) - len(infer_msgs)
                    if skipped:
                        print(f"⏭️ Skipped inference for {skipped} message(s) (no @mention or broadcast)")
        except Exception as e:
            print(f"❌ Single poll failed: {e}")

    # ── Inference Gating ─────────────────────────────────────────────

    @staticmethod
    def _normalize_mention_token(raw: str) -> str:
        text = unicodedata.normalize("NFKC", str(raw or "")).strip().lstrip("@").lower()
        # Keep only unicode letters/digits to make @yz_agent and @yz-agent equivalent.
        return "".join(ch for ch in text if ch.isalnum())

    @classmethod
    def _extract_mentions(cls, content: str) -> list[str]:
        mentions = set()
        for m in re.finditer(r"(^|[^\w])@([\w\.-]{1,64})", str(content or ""), re.UNICODE):
            token = cls._normalize_mention_token(m.group(2) or "")
            if token:
                mentions.add(token)
        return list(mentions)

    @classmethod
    def _build_agent_aliases(cls, agent_id: str, agent_name: str) -> set[str]:
        aliases = set()

        def add(v: str):
            t = cls._normalize_mention_token(v)
            if t:
                aliases.add(t)

        add(agent_id)
        add(agent_name)
        if agent_name:
            add(agent_name.replace(" ", "_"))
            add(agent_name.replace(" ", "-"))

        return aliases

    def _is_mentioned(self, message: dict) -> bool:
        """Check if this agent is @mentioned in content or runner-targeted by backend."""
        my_id = self.agent.get_id() if hasattr(self.agent, "get_id") else ""
        my_name = ""
        if hasattr(self.agent, "get_name"):
            my_name = self.agent.get_name() or ""
        elif hasattr(self.agent, "name"):
            my_name = self.agent.name or ""

        # Backend-enriched runner targeting (task-linked topics).
        runner_id = str(message.get("runner_agent_id") or message.get("runnerAgentId") or "")
        runner_name = str(message.get("runner_agent_name") or message.get("runnerAgentName") or "")
        aliases = self._build_agent_aliases(my_id, my_name)
        if runner_id and self._normalize_mention_token(runner_id) in aliases:
            return True
        if runner_name and self._normalize_mention_token(runner_name) in aliases:
            return True

        mentions = self._extract_mentions(str(message.get("content") or ""))
        if not mentions:
            return False

        return any(m in aliases for m in mentions)

    def _should_trigger_inference(self, message: dict, topic_id: str) -> bool:
        """Decide whether a message should trigger agent inference.

        Rules:
        - Own messages: never (avoid echo loops)
        - Agent-sent messages: only if explicitly @mentioned (prevents infinite agent loops)
        - Human P2P messages: always
        - Human task-linked messages: always
        - Human discussion messages: only if @mentioned
        - Broadcast / other subscribed topics: never
        """
        sender_id = str(message.get("sender_id") or "")
        my_id = self.agent.get_id() if hasattr(self.agent, "get_id") else ""

        # Never infer on own messages
        if sender_id == my_id:
            return False

        sender_type = str(message.get("sender_type") or "").lower()
        topic_meta = self._subscribed_topics.get(topic_id, {})
        topic_type = (topic_meta.get("type") or topic_meta.get("topic_type") or "").lower()
        topic_name = topic_meta.get("name") or ""

        # Agent-to-agent: only respond if explicitly @mentioned (prevents infinite loops)
        if sender_type == "agent":
            return self._is_mentioned(message)

        # From here: sender is human (or unknown)

        # P2P topics — always respond to human messages
        if topic_type == "p2p" or topic_name.startswith("private://"):
            return True

        # Task-linked topics — always respond to human messages
        if topic_meta.get("task_id"):
            return True

        # Discussion topics — only respond when @mentioned
        if topic_type == "discussion":
            return self._is_mentioned(message)

        # Broadcast and other topic types — do not auto-infer
        return False

    # ── Common ──────────────────────────────────────────────────────

    async def _push_to_im(self, message: str):
        """Push message to IM"""
        try:
            if hasattr(self.agent, "send_to_im"):
                await self.agent.send_to_im(message)
            elif hasattr(self.agent, "notify"):
                await self.agent.notify(message)
            elif hasattr(self.agent, "send_message"):
                await self.agent.send_message(message)
            else:
                print(f"💬 [IM Push] {message}")
        except Exception as e:
            print(f"❌ Failed to push to IM: {e}")

    async def handle_command(self, command: str) -> str:
        """Handle user command"""
        return await self.handler.handle_command(command)

    @property
    def is_ws_connected(self) -> bool:
        return self._ws_connected


async def main():
    """Example: how to use WTTSkillRunner"""

    class MockAgent:
        def __init__(self, agent_id: str):
            self._agent_id = agent_id

        def get_id(self):
            return self._agent_id

        async def call_mcp_tool(self, server_name: str, tool_name: str, kwargs: dict = None):
            try:
                from wtt_skill.wtt_client import wtt_client
            except ImportError:
                from wtt_client import wtt_client
            if tool_name == "wtt_poll":
                return await wtt_client.poll_messages(kwargs["agent_id"])
            return {}

        async def send_to_im(self, message: str):
            print(f"\n{'='*80}")
            print("📱 Push to IM:")
            print(f"{'='*80}")
            print(message)
            print(f"{'='*80}\n")

    agent = MockAgent("demo_agent")

    # 先加入一个 topic（用于测试）
    try:
        from wtt_skill.wtt_client import wtt_client
    except ImportError:
        from wtt_client import wtt_client
    try:
        results = await wtt_client.find_topics("GitHub Trending")
        if results:
            topic_id = results[0]["id"]
            await wtt_client.join_topic(topic_id, agent.get_id())
            print("✅ Joined GitHub Trending topic")
    except Exception as e:
        print(f"⚠️  Failed to join topic: {e}")

    # 默认 WebSocket 模式
    runner = WTTSkillRunner(agent, interval=30, mode="websocket")

    def signal_handler(sig, frame):
        print("\n\n⚠️  Interrupt signal received, stopping...")
        asyncio.create_task(runner.stop())
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    await runner.start()

    print("\n" + "="*80)
    print("WTT Skill running...")
    print("="*80)
    print("• Mode: WebSocket real-time + polling fallback")
    print("• Polling interval: 30s (used when WebSocket disconnects)")
    print("• New messages are pushed to IM in real time")
    print("• Press Ctrl+C to stop")
    print("="*80 + "\n")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await runner.stop()
        await wtt_client.client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
