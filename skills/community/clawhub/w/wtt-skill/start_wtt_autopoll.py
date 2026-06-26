#!/usr/bin/env python3
from __future__ import annotations
"""
WTT Skill auto service (WebSocket real-time + polling fallback)
Runs in background, receives messages via WebSocket, and pushes to IM
"""
import asyncio
import sys
import os
import json
import re
import subprocess
import shutil
import time
import uuid
import urllib.request
import urllib.error
from typing import List, Tuple, Optional
from pathlib import Path
from datetime import datetime, timezone


def _load_local_env(env_path: str):
    """Load KEY=VALUE lines from .env into process env without overriding existing vars."""
    try:
        p = Path(env_path)
        if not p.exists() or not p.is_file():
            return
        for raw in p.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            key = k.strip()
            val = v.strip().strip('"').strip("'")
            if key and (key not in os.environ):
                os.environ[key] = val
    except Exception as e:
        print(f"⚠️ Failed to read .env({env_path}): {e}")

PLAN_PREFIX = "WTT_PLAN_JSON:"


def _acquire_pid_lock() -> bool:
    """Ensure only one instance runs. Returns True if lock acquired."""
    import fcntl
    pid_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".autopoll.pid")
    try:
        _acquire_pid_lock._fd = open(pid_path, "w")
        fcntl.flock(_acquire_pid_lock._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        _acquire_pid_lock._fd.write(str(os.getpid()))
        _acquire_pid_lock._fd.flush()
        return True
    except (OSError, IOError):
        print(f"⚠️ Another autopoll instance is already running (lock: {pid_path}). Exiting.")
        return False


if not _acquire_pid_lock():
    sys.exit(0)

# Path resolution: script is in skill dir; project_root is parent if mcp_server exists
_script_path = Path(__file__).resolve()
_skill_root = str(_script_path.parent)
_project_root = str(_script_path.parent.parent)
if not os.path.isdir(os.path.join(_project_root, "mcp_server")):
    _project_root = _skill_root

# Provide import paths for wtt_skill and mcp_server modules
sys.path.insert(0, _project_root)

# Load .env from skill dir (primary); migrate legacy path on first run
_skill_env_path = os.path.join(_skill_root, ".env")
_legacy_env_path = os.path.join(_project_root, ".env")

if os.path.exists(_skill_env_path):
    _load_local_env(_skill_env_path)
elif os.path.exists(_legacy_env_path):
    _load_local_env(_legacy_env_path)
    try:
        Path(_skill_root).mkdir(parents=True, exist_ok=True)
        Path(_skill_env_path).write_text(Path(_legacy_env_path).read_text(encoding="utf-8"), encoding="utf-8")
        print(f"ℹ️ Migrated legacy config into skill directory: {_skill_env_path}")
    except Exception as e:
        print(f"⚠️ Failed to migrate .env into skill directory: {e}")

try:
    from wtt_skill.runner import WTTSkillRunner
    from wtt_skill.wtt_client import wtt_client
except ImportError:
    # standalone layout: files live directly under skills/wtt
    from runner import WTTSkillRunner
    from wtt_client import wtt_client


def _resolve_local_agent_id() -> str:
    """Bootstrap agent id + token: read .env → register via API → local fallback."""
    explicit = os.getenv("WTT_AGENT_ID", "").strip()
    if explicit:
        return explicit

    import httpx
    api_url = os.getenv("WTT_API_URL", "https://www.waxbyte.com").rstrip("/")
    generated = ""
    token = ""
    try:
        resp = httpx.post(f"{api_url}/agents/register", json={"platform": "openclaw"}, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            generated = data.get("agent_id", "")
            token = data.get("agent_token", "")
    except Exception as e:
        print(f"⚠️ Agent registration API failed: {e}")

    if not generated:
        generated = f"agent-{uuid.uuid4().hex[:12]}"
        print(f"⚠️ API unreachable, using local fallback: {generated}")

    env_updates = {"WTT_AGENT_ID": generated}
    if token:
        env_updates["WTT_AGENT_TOKEN"] = token
    _upsert_env_file(env_updates)
    os.environ["WTT_AGENT_ID"] = generated
    if token:
        os.environ["WTT_AGENT_TOKEN"] = token
    print(f"✅ Registered agent_id={generated}")
    return generated


def _upsert_env_file(updates: dict[str, str]) -> None:
    """Write key=value pairs into the skill .env file (create or update)."""
    env_path = Path(_skill_root) / ".env"
    lines = []
    if env_path.exists() and env_path.is_file():
        lines = env_path.read_text(encoding="utf-8").splitlines()
    for k, v in updates.items():
        replaced = False
        for i, line in enumerate(lines):
            if line.strip().startswith(f"{k}="):
                lines[i] = f"{k}={v}"
                replaced = True
                break
        if not replaced:
            if lines and lines[-1].strip() != "":
                lines.append("")
            lines.append(f"{k}={v}")
    env_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


class OpenClawAgent:
    """OpenClaw Agent adapter"""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.openclaw_bin = os.getenv("OPENCLAW_BIN") or shutil.which("openclaw") or "openclaw"
        self._ws_runner = None  # set after WTTSkillRunner is created
        self._load_config()
        self.processed_message_ids = set()
        self.active_task_runs = set()
        self._task_dedup = set()
        self.subscribed_topics = set()  # populated from runner's _subscribed_topics
        self.max_concurrent_tasks = int(os.getenv("WTT_MAX_CONCURRENT_TASKS", "4"))
        self._task_semaphore = asyncio.Semaphore(self.max_concurrent_tasks)
        self._task_queue: list[str] = []  # task keys waiting for a slot
        self.reject_rerun_cooldown_sec = int(os.getenv("WTT_REJECT_RERUN_COOLDOWN", "120"))
        # Progress publishing: default OFF — only final result published to topic/IM
        self.publish_progress = os.getenv("WTT_PUBLISH_PROGRESS", "0").lower() in ("1", "true", "yes")
        self.task_progress_interval_sec = 60
        self.task_max_runtime_sec = int(os.getenv("WTT_TASK_MAX_RUNTIME", "600"))
        self.task_stale_timeout_sec = int(os.getenv("WTT_TASK_STALE_TIMEOUT", "900"))
        self.last_reject_rerun_ts = {}
        self.pending_reject_rerun = {}
        self.pending_task_input_queue = {}
        self._recent_self_published = {}
        self._task_topic_cache = {}  # topic_id -> (is_task_topic: bool, ts)
        self._recent_human_trigger = {}  # key(topic|sender|content) -> ts
        self._topic_task_hints = {}  # topic_id -> (task_id, ts), used for no-task_id dispatch recovery
        # non-task auto-reply guard (prevent agent<->agent ping-pong)
        self._topic_auto_guard = {}  # topic_id -> {last_ts, count, locked}
        self._task_watch_last_report = {}  # task_id -> last_report_no
        self._task_watch_first_seen = {}   # task_id -> monotonic start ts in current process
        self._task_recent_touch = {}       # task_id -> last local touch ts
        # task_id -> independent sessionKey (reused for follow-ups via sessions_send)
        self.task_session_keys: dict[str, str] = {}
        self.topic_session_keys: dict[str, str] = {}  # non-task topic_id -> independent sessionKey

    def _parse_csv(self, value: str) -> List[str]:
        return [x.strip() for x in (value or '').split(',') if x.strip()]

    def _parse_fallbacks(self, value: str) -> List[Tuple[str, str]]:
        pairs: List[Tuple[str, str]] = []
        for item in self._parse_csv(value):
            if ':' in item:
                ch, target = item.split(':', 1)
                ch = ch.strip()
                target = target.strip()
                if ch and target:
                    pairs.append((ch, target))
        return pairs

    def _load_config(self):
        """Read OpenClaw config (read-only fallback; does not rely on defaultTarget)."""
        # Auto-reasoning switch for topic/p2p streams (enabled by default)
        self.poll_llm_enabled = os.getenv("WTT_POLL_LLM", "1") == "1"
        self.poll_llm_marker = os.getenv("WTT_POLL_LLM_MARKER", "[AUTO-REASONED]")

        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        self.gateway_url = "http://127.0.0.1:18789"
        self.gateway_token = ""
        self._openclaw_send_disabled = False
        self._openclaw_send_disabled_reason = ""

        config = {}
        if os.path.exists(config_path):
            try:
                with open(config_path) as f:
                    config = json.load(f)
            except Exception as e:
                print(f"⚠️ Failed to read openclaw.json: {e}")
                config = {}

        channels_cfg = config.get('channels', {}) if isinstance(config, dict) else {}

        # channel: env first; otherwise first enabled channel; fallback telegram
        self.im_channel = os.getenv("WTT_IM_CHANNEL", "").strip()
        if not self.im_channel:
            fallback_ch = next((k for k, v in channels_cfg.items() if isinstance(v, dict) and v.get('enabled')), "")
            if not fallback_ch:
                fallback_ch = next(iter(channels_cfg.keys()), "") if isinstance(channels_cfg, dict) else ""
            self.im_channel = fallback_ch or "telegram"

        # target: env/fixed fallback only; do not read defaultTarget (deprecated in newer OpenClaw)
        target = os.getenv("WTT_IM_TARGET", "2105528675").strip()
        targets = os.getenv("WTT_IM_TARGETS", "").strip()
        self.im_targets = self._parse_csv(targets)
        if not self.im_targets and target:
            self.im_targets = [target]

        # fallback routes format: channel:target,channel:target
        self.im_fallback_routes = self._parse_fallbacks(os.getenv("WTT_IM_FALLBACKS", ""))

        # Derive tools/invoke endpoint and token only from OpenClaw config.
        # Do not depend on custom gateway URL/token values in skill .env.
        gw = config.get('gateway', {}) if isinstance(config, dict) else {}
        port = gw.get('port', 18789)
        self.gateway_url = f"http://127.0.0.1:{port}"
        self.gateway_token = (gw.get('auth', {}) or {}).get('token', "")

        # Reminder: sessions_* tools must be enabled in gateway.tools.allow.
        allow = set((gw.get('tools', {}) or {}).get('allow', []) or [])
        required = {"sessions_spawn", "sessions_send", "sessions_history"}
        missing = sorted(required - allow)
        if missing:
            print(
                "⚠️ Gateway tools.allow missing required session tools: "
                + ", ".join(missing)
                + ". Please enable: sessions_spawn, sessions_send, sessions_history"
                + " (optional: sessions_list)."
            )
    def get_id(self):
        return self.agent_id

    async def call_mcp_tool(self, server_name: str, tool_name: str, kwargs: dict = None):
        """Call MCP tool — WebSocket first, fallback to HTTP"""
        kwargs = kwargs or {}

        # WebSocket 快速路径
        if self._ws_runner and self._ws_runner.is_ws_connected:
            action_map = {
                "wtt_list": "list", "wtt_find": "find", "wtt_join": "join",
                "wtt_leave": "leave", "wtt_publish": "publish", "wtt_poll": "poll",
                "wtt_p2p": "p2p", "wtt_create": "create",
            }
            action = action_map.get(tool_name)
            if action:
                try:
                    result = await self._ws_runner.send_action(action, kwargs)
                    if result is not None:
                        return result
                except Exception as e:
                    print(f"⚠️ WS action '{action}' failed, falling back to HTTP: {e}")

        # HTTP 回退
        if tool_name == "wtt_list":
            return await wtt_client.list_topics()
        elif tool_name == "wtt_find":
            return await wtt_client.find_topics(kwargs.get("query", ""))
        elif tool_name == "wtt_join":
            return await wtt_client.join_topic(kwargs["topic_id"], kwargs["agent_id"])
        elif tool_name == "wtt_leave":
            return await wtt_client.leave_topic(kwargs["topic_id"], kwargs["agent_id"])
        elif tool_name == "wtt_publish":
            return await wtt_client.publish_message(
                kwargs["topic_id"],
                kwargs["sender_id"],
                kwargs["content"]
            )
        elif tool_name == "wtt_poll":
            return await wtt_client.poll_messages(kwargs["agent_id"])
        elif tool_name == "wtt_p2p":
            return await wtt_client.send_p2p(
                kwargs["sender_id"],
                kwargs["target_id"],
                kwargs["content"]
            )
        elif tool_name == "wtt_create":
            return await wtt_client.create_topic(kwargs)
        elif tool_name == "wtt_bind":
            return await wtt_client.generate_claim_code(kwargs.get("agent_id", self.agent_id))
        else:
            return {}

    async def _send_via_openclaw(self, channel: str, target: str, message: str, file_path: str = "", caption: str = "") -> bool:
        if self._openclaw_send_disabled:
            return False

        cmd = [
            self.openclaw_bin, "message", "send",
            "--channel", channel,
            "--target", target,
            "--message", message,
        ]
        if file_path:
            cmd.extend(["--path", file_path])
            if caption:
                cmd.extend(["--caption", caption])
        result = await asyncio.to_thread(
            subprocess.run,
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            print(f"✅ Message sent to {channel}:{target}")
            return True

        stderr_text = (result.stderr or "").strip()
        print(f"❌ OpenClaw message send failed: {channel}:{target} rc={result.returncode}")
        if stderr_text:
            print(stderr_text)

        # 若 OpenClaw 配置非法，避免每次轮询反复触发 CLI 校验，直接熔断本进程 IM 推送
        if (
            "Config invalid" in stderr_text
            or "Unrecognized key" in stderr_text
            or "Invalid config at" in stderr_text
        ):
            self._openclaw_send_disabled = True
            self._openclaw_send_disabled_reason = stderr_text.splitlines()[0] if stderr_text else "config invalid"
            print(f"⛔ OpenClaw IM push disabled (this process)：{self._openclaw_send_disabled_reason}")

        return False

    async def send_to_im(self, message: str, file_path: str = "", caption: str = ""):
        """Push messages via OpenClaw message channel (multi-target + fallback; attachments supported)."""
        try:
            if self._openclaw_send_disabled:
                print(f"⏭️ Skip IM push (disabled)：{self._openclaw_send_disabled_reason}")
                return
            if not self.im_channel:
                print("⚠️ IM channel not configured (WTT_IM_CHANNEL / openclaw.json channels)")
                return
            if not self.im_targets:
                print("⚠️ IM target not configured (WTT_IM_TARGETS / WTT_IM_TARGET)")
                return

            primary_ok = True
            for target in self.im_targets:
                ok = await self._send_via_openclaw(self.im_channel, target, message, file_path=file_path, caption=caption)
                primary_ok = primary_ok and ok

            if primary_ok:
                return

            if self.im_fallback_routes and not self._openclaw_send_disabled:
                print("⚠️ Primary route had failures, trying fallback routes...")
                for channel, target in self.im_fallback_routes:
                    await self._send_via_openclaw(channel, target, message, file_path=file_path, caption=caption)
        except Exception as e:
            print(f"❌ Failed to push to IM: {e}")

    def _invoke_tool_sync(self, tool: str, args: dict) -> dict:
        payload = json.dumps({"tool": tool, "action": "json", "args": args}).encode("utf-8")
        # Bypass system proxy for local gateway calls (avoids Privoxy 500 errors)
        no_proxy_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        # Adaptive timeout: history/status queries are fast; send/spawn can be slow
        if tool in ("sessions_history",):
            http_timeout = 30
        elif tool == "sessions_send":
            http_timeout = max(90, int(args.get("timeoutSeconds", 120)) + 30)
        else:
            http_timeout = 90
        last_err = None
        for suffix in ("/tools/invoke", "/v1/tools/invoke"):
            url = f"{self.gateway_url.rstrip('/')}{suffix}"
            req = urllib.request.Request(url, data=payload, method="POST")
            req.add_header("Content-Type", "application/json")
            if self.gateway_token:
                req.add_header("Authorization", f"Bearer {self.gateway_token}")
            try:
                with no_proxy_opener.open(req, timeout=http_timeout) as resp:
                    raw = resp.read().decode("utf-8", "ignore")
                data = json.loads(raw or "{}")
                if not data.get("ok", False):
                    err = data.get("error", {})
                    raise RuntimeError(f"invoke {tool} failed: {err.get('message', raw)}")
                result = data.get("result", {})
                if isinstance(result, dict) and isinstance(result.get("details"), dict):
                    return result.get("details", {})
                return result
            except Exception as e:
                last_err = e
                continue
        hint = (
            " Hint: check OpenClaw gateway is running and enable session tools in "
            "gateway.tools.allow (sessions_spawn, sessions_send, sessions_history"
            ", optionally sessions_list)."
        )
        raise RuntimeError(f"invoke {tool} failed on all endpoints: {last_err}.{hint}")

    async def _invoke_tool(self, tool: str, args: dict) -> dict:
        return await asyncio.to_thread(self._invoke_tool_sync, tool, args)

    def _extract_assistant_texts(self, history_result: dict) -> list[str]:
        texts: list[str] = []
        for m in history_result.get("messages", []) or []:
            if m.get("role") != "assistant":
                continue
            for c in m.get("content", []) or []:
                if isinstance(c, dict) and c.get("type") == "text" and c.get("text"):
                    texts.append(str(c.get("text")))
        return texts

    def _extract_assistant_error(self, history_result: dict) -> str:
        for m in history_result.get("messages", []) or []:
            if m.get("role") != "assistant":
                continue
            err = m.get("errorMessage")
            if err:
                return str(err)
        return ""

    async def _find_session_by_label(self, label: str) -> Optional[str]:
        """Best-effort session recovery by label (used after restart / label conflicts)."""
        if not label:
            return None
        try:
            listed = await self._invoke_tool("sessions_list", {"limit": 300, "messageLimit": 0})
            for s in (listed or {}).get("sessions", []) or []:
                if str(s.get("label") or "") == label:
                    key = s.get("key")
                    if key:
                        return str(key)
        except Exception as e:
            print(f"⚠️ sessions_list(label={label}) failed: {e}")
        return None

    async def _infer_with_openclaw(self, text: str, topic_id: str = "", title: str = "") -> str:
        """推理：spawn 独立 session（非 subagent )，轻量无父子通信开销。
        非 task topic 用一次性 session；topic_id 非空时可复用缓存 session。
        """
        # 尝试复用已有 topic session（非 task topic 也可维持对话上下文 )
        cached_key = self.topic_session_keys.get(topic_id) if topic_id else None
        last_err = None

        for attempt in range(3):
            try:
                started_at = int(time.time())
                last_minute_report = 0

                if cached_key:
                    # 已有 session → sessions_send 追加消息
                    send_result = await self._invoke_tool(
                        "sessions_send",
                        {"sessionKey": cached_key, "message": text, "timeoutSeconds": 60},
                    )
                    child = cached_key
                    # sessions_send 失败时降级为新建 session
                    if not send_result or send_result.get("error"):
                        cached_key = None
                        self.topic_session_keys.pop(topic_id, None)
                        raise RuntimeError("sessions_send failed, will retry with new session")
                else:
                    # 新建独立 session — delegate to _spawn_session_and_poll (polls main session for push result)
                    label = f"wtt-topic-{(topic_id or 'adhoc')[:12]}"
                    child, result = await self._spawn_session_and_poll(text, label=label)
                    if child and topic_id:
                        self.topic_session_keys[topic_id] = child
                    # Truncation recovery for non-task inference
                    if result and ("...(truncated)" in result or "…(truncated)" in result):
                        print(f"⚠️ infer: result truncated ({len(result)} chars), fetching from transcript")
                        full = await self._fetch_full_child_result(child)
                        if full and len(full) > len(result):
                            print(f"✅ infer: recovered {len(full)} chars from transcript")
                            result = full
                    if result and result.upper() != "READY":
                        if topic_id:
                            ts = time.strftime('%H:%M:%S')
                            if self.publish_progress:
                                try:
                                    await asyncio.wait_for(
                                        self._safe_publish(
                                            topic_id,
                                            f"Time: {ts}\n"
                                            f"Progress: 100%\n"
                                            f"Status: [Task: {title or 'general chat'}] reasoning completed"
                                        ),
                                        timeout=15,
                                    )
                                except asyncio.TimeoutError:
                                    pass
                        return result
                    raise RuntimeError("session infer timeout: no assistant text returned")
            except Exception as e:
                last_err = e
                cached_key = None  # 重试时强制新建 session
                if attempt < 2:
                    await asyncio.sleep(2 * (attempt + 1))
                    continue
                raise RuntimeError(str(last_err))

    async def _execute_by_agent(self, task_id: str, title: str, description: str, session_id: str, is_followup: bool = False, original_description: str = "") -> tuple[list[str], list[str], str, str, str]:
        """执行任务推理：每个 task 维护一个独立 session。
        首次运行 spawn 新 session，后续 follow-up 通过 sessions_send 追加。
        Session 销毁后从 OpenClaw 恢复对话历史（cleanup:'keep' 保留历史），
        通过 sessions_spawn(context=...) 注入新 session。
        不在 DB 存对话历史 — OpenClaw 本身就是对话历史的唯一存储源。
        若 OpenClaw 历史也丢失，退化为 rerun+follow：重新执行原始任务并附加 follow-up。
        """
        cached_key = self.task_session_keys.get(task_id)
        dead_session_key = None  # remember dead key for history recovery

        # 尝试从 DB 恢复 session key（进程重启后）
        if not cached_key:
            cached_key = await self._load_task_session_key_from_db(task_id)
            if cached_key:
                self.task_session_keys[task_id] = cached_key

        # Pre-validate: if we have a cached session, verify it's still alive
        if cached_key:
            alive = await self._check_session_alive(cached_key)
            if not alive:
                print(f"⚠️ Cached session {cached_key[:20]} for task {task_id[:12]} is dead, will spawn new")
                dead_session_key = cached_key  # keep for history recovery from OpenClaw
                self.task_session_keys.pop(task_id, None)
                # Don't clear session key from DB yet — we need it for history recovery
                cached_key = None

        # Recover context from OpenClaw when session is dead and we need follow-up
        recovered_context = ""
        if is_followup and not cached_key:
            recover_key = dead_session_key
            if not recover_key:
                # Process may have restarted — try loading the old key from DB
                recover_key = await self._load_task_session_key_from_db(task_id)
            if recover_key:
                recovered_context = await self._recover_history_from_openclaw(recover_key)
            # Now safe to clear the dead session key from DB
            if dead_session_key:
                await self._clear_task_session_key_in_db(task_id)

        if is_followup and cached_key:
            # 已有 session → sessions_send 追加消息（session 自带上下文）
            prompt = (
                f"User sent a follow-up for task '{title}':\n"
                f"{description}\n\n"
                "Based on prior context, return an updated final answer only."
            )
        elif is_followup and not cached_key and recovered_context:
            # Session dead, context recovered from OpenClaw — pass via context param
            prompt = (
                f"You are continuing a WTT task after session recovery.\n"
                f"Task title: {title}\n"
                f"User's follow-up:\n{description}\n\n"
                "The previous conversation history is provided as context. "
                "Based on ALL prior context, return an updated final answer only.\n"
                "Requirements:\n"
                "- Do not output STEP / MID / CHANGE / RESULT tags\n"
                "- Provide conclusion/judgment/solution/final answer directly\n"
            )
        elif is_followup and not cached_key and not recovered_context:
            # Session dead AND OpenClaw history gone → rerun original task + follow-up
            orig = original_description
            if not orig:
                # Fallback: fetch original description from DB (covers reject rerun where description may be empty)
                task_data = await self._get_task(task_id)
                orig = (task_data.get("description") or "").strip()
            if not orig:
                orig = title  # last resort
            print(f"🔄 Rerun+Follow: OpenClaw history lost for task {task_id[:12]}, re-executing original + follow-up")
            prompt = (
                "You are executing a WTT task. A previous session's history has been lost.\n"
                "Please re-execute the original task first, then address the follow-up.\n\n"
                f"=== Original Task ===\n"
                f"Title: {title}\n"
                f"Description: {orig}\n\n"
                f"=== Follow-up Request ===\n"
                f"{description}\n\n"
                "Requirements:\n"
                "- First fulfill the original task, then address the follow-up\n"
                "- Output only the final combined answer\n"
                "- Do not output STEP / MID / CHANGE / RESULT tags\n"
                "- Do not include process narration\n"
                "- Provide conclusion/judgment/solution/final answer directly\n"
            )
        else:
            prompt = (
                "You are executing a WTT task. Output only the final user-facing answer.\n"
                f"Task title: {title}\n"
                f"Task description: {description}\n"
                "Requirements:\n"
                "- Do not output STEP / MID / CHANGE / RESULT tags\n"
                "- Do not include process narration like 'I will.../next...'\n"
                "- Do not restate this prompt\n"
                "- Provide conclusion/judgment/solution/final answer directly\n"
                "- Use short bullets if needed; do not expose internal execution\n"
                "- Keep complete useful output; do not over-compress\n"
            )

        last_err = None
        for attempt in range(3):
            try:
                if cached_key and (is_followup or attempt > 0):
                    # 向已有 session 发送消息
                    merged = await self._send_and_poll(cached_key, prompt)
                    if merged is None:
                        # session 已过期/失效，清缓存重建
                        print(f"⚠️ Session dead for task {task_id[:12]}, clearing and retrying with new session")
                        dead_session_key = cached_key
                        self.task_session_keys.pop(task_id, None)
                        await self._clear_task_session_key_in_db(task_id)
                        cached_key = None
                        # Recover context from OpenClaw
                        if not recovered_context and dead_session_key:
                            recovered_context = await self._recover_history_from_openclaw(dead_session_key)
                        # If recovery also failed and this is a follow-up, rebuild prompt as rerun+follow
                        if is_followup and not recovered_context:
                            orig = original_description
                            if not orig:
                                task_data = await self._get_task(task_id)
                                orig = (task_data.get("description") or "").strip()
                            if not orig:
                                orig = title
                            print(f"🔄 Mid-exec rerun+follow: history lost for task {task_id[:12]}")
                            prompt = (
                                "You are executing a WTT task. A previous session's history has been lost.\n"
                                "Please re-execute the original task first, then address the follow-up.\n\n"
                                f"=== Original Task ===\n"
                                f"Title: {title}\n"
                                f"Description: {orig}\n\n"
                                f"=== Follow-up Request ===\n"
                                f"{description}\n\n"
                                "Requirements:\n"
                                "- First fulfill the original task, then address the follow-up\n"
                                "- Output only the final combined answer\n"
                                "- Do not output STEP / MID / CHANGE / RESULT tags\n"
                                "- Provide conclusion/judgment/solution/final answer directly\n"
                            )
                        raise RuntimeError("session send returned empty, will retry with new session")
                else:
                    # 创建新的独立 session (pass recovered_context via context param)
                    new_key, merged = await self._spawn_session_and_poll(
                        prompt,
                        label=f"wtt-task-{task_id[:12]}",
                        context=recovered_context,
                    )
                    if new_key:
                        self.task_session_keys[task_id] = new_key
                        await self._persist_task_session_key_to_db(task_id, new_key)
                        cached_key = new_key
                    if not merged:
                        raise RuntimeError("session returned empty result")

                steps, mids, changes, final = [], [], [], merged
                for line in (merged or "").splitlines():
                    s = line.strip()
                    if s.upper().startswith("STEP:"):
                        steps.append(s[5:].strip())
                    elif s.upper().startswith("MID:"):
                        mids.append(s[4:].strip())
                    elif s.upper().startswith("CHANGE:"):
                        changes.append(s[7:].strip())
                    elif s.upper().startswith("RESULT:"):
                        final = s[7:].strip()
                return steps[:3], mids[:3], changes[:5], final or "(no result)", (merged or final or "")
            except Exception as e:
                last_err = e
                if attempt < 2:
                    await asyncio.sleep(2 * (attempt + 1))
                    continue
                raise RuntimeError(str(last_err))

    async def _recover_history_from_openclaw(self, dead_session_key: str) -> str:
        """Try to extract conversation history from a dead OpenClaw session.
        OpenClaw keeps session history persisted (cleanup: 'keep') even after
        the session stops accepting new messages. Returns formatted context string
        or empty string if unavailable."""
        if not dead_session_key:
            return ""
        try:
            hist = await self._invoke_tool("sessions_history", {
                "sessionKey": dead_session_key,
                "limit": 30,
                "includeTools": False,
            })
            if not isinstance(hist, dict):
                return ""
            messages = hist.get("messages") or []
            if not messages:
                return ""
            # Build context from OpenClaw's native history (richer than our DB copy)
            parts = []
            total = 0
            for msg in messages:
                role = str(msg.get("role", "")).upper()
                text = str(msg.get("content") or msg.get("text") or "").strip()
                if not text or role not in ("USER", "ASSISTANT"):
                    continue
                entry = f"[{role}]: {text[:2000]}"
                if total + len(entry) > 6000:
                    break
                parts.append(entry)
                total += len(entry)
            if parts:
                print(f"🔄 Recovered {len(parts)} turns from dead OpenClaw session {dead_session_key[:20]}")
                return "\n---\n".join(parts)
        except Exception as e:
            print(f"🔍 Could not recover history from dead session {dead_session_key[:20]}: {e}")
        return ""

    async def _spawn_session_and_poll(self, prompt: str, label: str = "", context: str = "") -> tuple[Optional[str], Optional[str]]:
        """创建 subagent session 并通过轮询主 session 获取结果。
        Gateway 使用 auto-announce push 模式：子 session 完成后结果推送到 agent:main:main。
        返回 (sessionKey, assistant_text)。sessionKey 可缓存复用。
        """
        spawn_label = label or "wtt-task"
        child = None
        spawn_params = {
            "task": prompt,
            "label": spawn_label,
            "mode": "run",
            "cleanup": "keep",
            "runTimeoutSeconds": max(120, int(self.task_max_runtime_sec)),
            "timeoutSeconds": 30,
        }
        if context:
            spawn_params["context"] = context

        # Record main session message count BEFORE spawning
        pre_main_count = 0
        try:
            pre_hist = await self._invoke_tool("sessions_history", {"sessionKey": "agent:main:main", "limit": 100, "includeTools": False})
            pre_main_count = len((pre_hist or {}).get("messages", []) or [])
        except Exception:
            pass

        try:
            spawn = await self._invoke_tool("sessions_spawn", spawn_params)
            child = (spawn or {}).get("childSessionKey")
        except Exception as e:
            if "label already in use" in str(e) or "already in use" in str(e):
                child = await self._find_session_by_label(spawn_label)
                if child and not await self._check_session_alive(child):
                    child = None
                    unique_label = f"{spawn_label}-{int(time.time()) % 100000}"
                    spawn_params["label"] = unique_label
                    try:
                        spawn = await self._invoke_tool("sessions_spawn", spawn_params)
                        child = (spawn or {}).get("childSessionKey")
                    except Exception:
                        pass
            if not child:
                raise

        if not child:
            raise RuntimeError("sessions_spawn missing childSessionKey")

        # Extract suffix for matching in completion events (gateway abbreviates keys)
        child_suffix = child.rsplit(":", 1)[-1][-4:] if child else ""
        print(f"🔍 [spawn] child={child[:35]} suffix={child_suffix} label={spawn_label}")

        deadline = time.time() + max(150, int(self.task_max_runtime_sec) + 60)
        poll_interval = 3.0
        poll_count = 0
        while time.time() < deadline:
            try:
                hist = await self._invoke_tool("sessions_history", {
                    "sessionKey": "agent:main:main",
                    "limit": max(50, pre_main_count + 20),
                    "includeTools": False,
                })
            except Exception as poll_err:
                print(f"⚠️ [spawn_poll] main history error: {poll_err}")
                await asyncio.sleep(poll_interval)
                continue

            msgs = (hist or {}).get("messages", []) or []
            poll_count += 1

            # Scan for completion event matching our child session
            for i, m in enumerate(msgs):
                if m.get("role") != "user":
                    continue
                text_parts = []
                for c in (m.get("content") or []):
                    if isinstance(c, dict) and c.get("text"):
                        text_parts.append(str(c["text"]))
                full_text = "\n".join(text_parts)

                if "[Internal task completion event]" not in full_text:
                    continue
                if child_suffix not in full_text:
                    continue

                # Found our completion event
                print(f"🔍 [spawn_poll] Found completion event for {child_suffix} at msg[{i}] poll#{poll_count}")

                # Extract result from <<<BEGIN_UNTRUSTED_CHILD_RESULT>>> markers
                result_text = self._extract_child_result(full_text)

                # Check status
                if "status: failed" in full_text or "status: error" in full_text:
                    # Extract error details
                    for line in full_text.splitlines():
                        if line.strip().startswith("status:"):
                            err_detail = line.strip()
                            break
                    else:
                        err_detail = "unknown error"
                    # If there's a result despite failure, return it
                    if result_text and result_text != "(no output)":
                        if ("...(truncated)" in result_text or "\u2026(truncated)" in result_text) and child:
                            full_text_child = await self._fetch_full_child_result(child)
                            if full_text_child and len(full_text_child) > len(result_text):
                                result_text = full_text_child
                        return child, result_text
                    # Otherwise check if the assistant response after this event has useful text
                    if i + 1 < len(msgs) and msgs[i + 1].get("role") == "assistant":
                        asst_text = self._extract_text_from_message(msgs[i + 1])
                        if asst_text:
                            return child, asst_text
                    raise RuntimeError(f"subagent task failed: {err_detail}")

                # Success: return extracted result
                if result_text and result_text != "(no output)":
                    if ("...(truncated)" in result_text or "\u2026(truncated)" in result_text) and child:
                        print(f"\u26a0\ufe0f Result truncated by gateway, fetching full text from child session")
                        full_text_child = await self._fetch_full_child_result(child)
                        if full_text_child and len(full_text_child) > len(result_text):
                            result_text = full_text_child
                    return child, result_text
                # Fallback: use assistant response after completion event
                if i + 1 < len(msgs) and msgs[i + 1].get("role") == "assistant":
                    asst_text = self._extract_text_from_message(msgs[i + 1])
                    if asst_text:
                        return child, asst_text
                # Got event but no result yet (might still be processing)
                break

            if poll_count % 5 == 0:
                elapsed = int(time.time() - (deadline - max(150, int(self.task_max_runtime_sec) + 60)))
                print(f"🔍 [spawn_poll] Waiting for {child_suffix} poll#{poll_count} elapsed={elapsed}s main_msgs={len(msgs)}")

            await asyncio.sleep(poll_interval)
            poll_interval = min(poll_interval * 1.2, 8.0)

        print(f"⚠️ [spawn_poll] Timeout waiting for completion of {child[:30]}")
        return child, None

    @staticmethod
    def _extract_child_result(event_text: str) -> str:
        """Extract result text from between <<<BEGIN_UNTRUSTED_CHILD_RESULT>>> markers."""
        begin = "<<<BEGIN_UNTRUSTED_CHILD_RESULT>>>"
        end = "<<<END_UNTRUSTED_CHILD_RESULT>>>"
        idx_start = event_text.find(begin)
        if idx_start < 0:
            print(f"\U0001f50d [DEBUG] _extract_child_result: no BEGIN marker, event_len={len(event_text)}")
            return ""
        content_start = idx_start + len(begin)
        idx_end = event_text.find(end, content_start)
        if idx_end > content_start:
            extracted = event_text[content_start:idx_end].strip()
            print(f"\U0001f50d [DEBUG] _extract_child_result: full extraction len={len(extracted)}")
            return extracted
        # END marker missing (truncated) - extract everything after BEGIN
        extracted = event_text[content_start:].strip()
        print(f"\U0001f50d [DEBUG] _extract_child_result: no END marker (truncated), extracted len={len(extracted)}")
        return extracted

    async def _fetch_full_child_result(self, child_key: str) -> str:
        """Fetch full assistant response by reading child session transcript from disk.
        sessions_history API returns 0 messages for subagent sessions,
        so we bypass the API and read the .jsonl transcript file directly.
        sessions_list provides the transcriptPath mapping."""
        import glob as glob_mod
        import os
        try:
            # Step 1: Find transcript path via sessions_list
            transcript_path = None
            try:
                listed = await self._invoke_tool("sessions_list", {
                    "limit": 200, "messageLimit": 0,
                })
                details = listed if isinstance(listed, dict) else {}
                sessions = details.get("sessions") or []
                for s in sessions:
                    if s.get("key") == child_key:
                        transcript_path = s.get("transcriptPath")
                        break
            except Exception as e:
                print(f"\u26a0\ufe0f sessions_list failed: {e}")

            if not transcript_path:
                print(f"\u26a0\ufe0f No transcriptPath for {child_key[:35]}")
                return ""

            # Step 2: Locate file (live .jsonl or renamed .deleted.*)
            target = transcript_path
            if not os.path.exists(target):
                deleted = sorted(glob_mod.glob(f"{target}.deleted.*"))
                if deleted:
                    target = deleted[-1]
                else:
                    print(f"\u26a0\ufe0f Transcript not on disk: {transcript_path}")
                    return ""

            # Step 3: Parse JSONL, find longest non-SKIP assistant text
            import json as json_mod
            best = ""
            with open(target, "r") as f:
                for raw_line in f:
                    try:
                        entry = json_mod.loads(raw_line.strip())
                        msg = entry.get("message", {})
                        if msg.get("role") != "assistant":
                            continue
                        parts = []
                        for c in (msg.get("content") or []):
                            if isinstance(c, dict) and c.get("type") == "text":
                                t = (c.get("text") or "").strip()
                                if t and t not in ("ANNOUNCE_SKIP", "REPLY_SKIP"):
                                    parts.append(t)
                        if parts:
                            candidate = "\n".join(parts)
                            if len(candidate) > len(best):
                                best = candidate
                    except Exception:
                        continue

            if best:
                print(f"\u2705 Full text from transcript: {len(best)} chars (file: {os.path.basename(target)})")
            else:
                print(f"\u26a0\ufe0f No non-SKIP assistant text in {os.path.basename(target)}")
            return best
        except Exception as e:
            print(f"\u26a0\ufe0f Failed to read transcript: {e}")
            return ""

    @staticmethod
    def _extract_text_from_message(msg: dict) -> str:
        """Extract concatenated text from a message's content array."""
        parts = []
        for c in (msg.get("content") or []):
            if isinstance(c, dict) and c.get("text"):
                parts.append(str(c["text"]).strip())
        return "\n".join(parts)

    async def _check_session_alive(self, session_key: str) -> bool:
        """Check if a session is still alive. Uses sessions_history first,
        falls back to sessions_list if history returns empty (some gateways
        return empty dict for destroyed sessions instead of erroring)."""
        short_key = session_key[:20] if session_key else "?"
        try:
            hist = await self._invoke_tool("sessions_history", {"sessionKey": session_key, "limit": 1, "includeTools": False})
            if not isinstance(hist, dict):
                print(f"🔍 Session {short_key} health: history returned non-dict → DEAD")
                return False
            # If history returned messages, session is definitely alive
            msgs = hist.get("messages") or []
            if msgs:
                print(f"🔍 Session {short_key} health: has {len(msgs)} message(s) → ALIVE")
                return True
            # Empty messages could mean new session OR destroyed session.
            # Verify via sessions_list as second opinion.
            print(f"🔍 Session {short_key} health: history empty, checking sessions_list...")
            try:
                listed = await self._invoke_tool("sessions_list", {"limit": 200, "messageLimit": 0})
                all_sessions = (listed or {}).get("sessions", []) or []
                for s in all_sessions:
                    if s.get("key") == session_key:
                        print(f"🔍 Session {short_key} health: found in sessions_list → ALIVE")
                        return True
                print(f"🔍 Session {short_key} health: NOT in sessions_list ({len(all_sessions)} total) → DEAD")
                return False
            except Exception as e:
                print(f"🔍 Session {short_key} health: sessions_list failed ({e}), assume ALIVE")
                return True
        except Exception as e:
            print(f"🔍 Session {short_key} health: history error ({e}) → DEAD")
            return False

    async def _send_and_poll(self, session_key: str, message: str) -> Optional[str]:
        """向已有独立 session 发送消息，轮询获取最新 assistant 回复。"""
        short_key = session_key[:20] if session_key else "?"
        # Pre-flight: verify session is still alive
        if not await self._check_session_alive(session_key):
            print(f"⚠️ _send_and_poll: session {short_key} failed pre-flight → returning None")
            return None

        # 先获取当前 history 长度，以便只取新回复
        pre_hist = await self._invoke_tool("sessions_history", {"sessionKey": session_key, "limit": 50, "includeTools": False})
        pre_count = len(self._extract_assistant_texts(pre_hist))

        try:
            send_result = await self._invoke_tool(
                "sessions_send",
                {"sessionKey": session_key, "message": message, "timeoutSeconds": 90},
            )
        except Exception as e:
            err_msg = str(e).lower()
            if any(kw in err_msg for kw in ("not found", "invalid session", "expired", "terminated", "no such")):
                print(f"⚠️ session {session_key[:20]} is dead: {e}")
                return None
            raise

        if not send_result and send_result is not None:
            pass  # some gateways return empty on success

        # Phase 1: short wait for initial response (detect dead sessions fast)
        early_deadline = time.time() + 15
        poll_interval = 1.0
        got_early = False
        while time.time() < early_deadline:
            hist = await self._invoke_tool("sessions_history", {"sessionKey": session_key, "limit": 50, "includeTools": False})
            err = self._extract_assistant_error(hist)
            if err:
                raise RuntimeError(err)
            texts = self._extract_assistant_texts(hist)
            if texts and len(texts) > pre_count:
                result = texts[-1].strip()
                # Truncation recovery: if gateway truncated, fetch from transcript
                if "...(truncated)" in result or "…(truncated)" in result:
                    print(f"⚠️ _send_and_poll: result truncated ({len(result)} chars), fetching full from transcript")
                    full = await self._fetch_full_child_result(session_key)
                    if full and len(full) > len(result):
                        print(f"✅ _send_and_poll: recovered {len(full)} chars from transcript")
                        return full
                return result
            # Check if session is processing (messages count changed or status hints)
            await asyncio.sleep(poll_interval)
            poll_interval = min(poll_interval * 1.3, 5.0)

        # Phase 2: extended wait (session is likely still working, just slow)
        deadline = time.time() + max(90, int(self.task_max_runtime_sec) - 30)
        poll_interval = 2.0
        while time.time() < deadline:
            hist = await self._invoke_tool("sessions_history", {"sessionKey": session_key, "limit": 50, "includeTools": False})
            err = self._extract_assistant_error(hist)
            if err:
                raise RuntimeError(err)
            texts = self._extract_assistant_texts(hist)
            if texts and len(texts) > pre_count:
                result = texts[-1].strip()
                if "...(truncated)" in result or "…(truncated)" in result:
                    print(f"⚠️ _send_and_poll phase2: result truncated ({len(result)} chars), fetching full from transcript")
                    full = await self._fetch_full_child_result(session_key)
                    if full and len(full) > len(result):
                        print(f"✅ _send_and_poll: recovered {len(full)} chars from transcript")
                        return full
                return result
            await asyncio.sleep(poll_interval)
            poll_interval = min(poll_interval * 1.3, 5.0)

        print(f"⚠️ _send_and_poll: session {short_key} timed out after both phases → returning None")
        return None

    def _normalize_task_id(self, raw: str) -> str:
        """Normalize task id token to bare uuid if possible (e.g. TASK-<uuid> -> <uuid>)."""
        if not raw:
            return ""
        token = str(raw).strip()
        if token.upper().startswith("TASK-"):
            token = token[5:]
        m = re.search(r"([0-9a-fA-F]{8}-[0-9a-fA-F-]{10,}|[0-9a-fA-F-]{32,})", token)
        return m.group(1) if m else token

    def _extract_to_task_hint(self, content: str) -> str:
        """Extract to_task/task_id hint from system payloads like [TASK_INPUT] to_task=..."""
        if not content:
            return ""
        m = re.search(r"(?:to_task|task_id)=([^\s\n]+)", content)
        return self._normalize_task_id((m.group(1) if m else ""))

    def _remember_topic_task_hint(self, topic_id: str, task_id: str):
        tid = self._normalize_task_id(task_id)
        if not topic_id or not tid:
            return
        self._topic_task_hints[str(topic_id)] = (tid, time.time())
        if len(self._topic_task_hints) > 2000:
            self._topic_task_hints = dict(list(self._topic_task_hints.items())[-1000:])

    def _get_topic_task_hint(self, topic_id: str, ttl_sec: int = 900) -> str:
        if not topic_id:
            return ""
        item = self._topic_task_hints.get(str(topic_id))
        if not item:
            return ""
        task_id, ts = item
        if (time.time() - float(ts or 0)) > ttl_sec:
            self._topic_task_hints.pop(str(topic_id), None)
            return ""
        return self._normalize_task_id(task_id)

    def _task_runtime_meta(self, task: dict) -> dict:
        return {
            "task_id": self._normalize_task_id(task.get("id") or task.get("task_id") or ""),
            "title": str(task.get("title") or ""),
            "description": str(task.get("description") or ""),
            "exec_mode": str(task.get("exec_mode") or "reasoning"),
            "task_type": str(task.get("task_type") or task.get("type") or "feature"),
        }

    async def _resolve_task_for_topic(self, topic_id: str, title_hint: str = "", description_hint: str = "", prefer_pipeline: bool = False) -> dict:
        """Resolve task for a topic safely when incoming payload lacks task_id.

        Strategy (ID-first, no title routing):
        1) recent topic->task hint (from msg.task_id / to_task / task_id payloads)
        2) unique active pipeline task (when prefer_pipeline)
        3) unique active task (todo/doing)
        4) single candidate only
        Otherwise return empty task_id to avoid misrouting.
        """
        empty = {
            "task_id": "",
            "title": title_hint or "",
            "description": description_hint or "",
            "exec_mode": "reasoning",
            "task_type": "feature",
        }
        if not topic_id:
            return empty

        try:
            resp = await wtt_client.client.get(
                f"{wtt_client.api_url}/tasks",
                params={"limit": 500},
                timeout=15,
            )
            if resp.status_code >= 400:
                return empty
            payload = resp.json() if hasattr(resp, "json") else []
            tasks = payload if isinstance(payload, list) else payload.get("tasks", [])
        except Exception:
            return empty

        candidates = [
            t for t in (tasks or [])
            if str(t.get("topic_id") or "") == str(topic_id)
        ]
        if not candidates:
            return empty

        # newest first for deterministic fallback behavior
        candidates.sort(key=lambda x: (x.get("updated_at") or x.get("created_at") or ""), reverse=True)

        # 1) explicit recent hint from task-input/task-status context
        # Guard against stale hints on reused topics: accept hint only when it is still active.
        hinted_id = self._get_topic_task_hint(topic_id)
        if hinted_id:
            hinted = next((t for t in candidates if self._normalize_task_id(t.get("id") or "") == hinted_id), None)
            if hinted:
                hinted_status = str(hinted.get("status") or "").lower()
                hinted_mode = str(hinted.get("task_mode") or "").lower()
                if hinted_status in {"todo", "doing"} and ((not prefer_pipeline) or hinted_mode == "pipeline"):
                    return self._task_runtime_meta(hinted)

        # 2) pipeline-biased resolve (for pipeline auto-start/rerun paths)
        if prefer_pipeline:
            pipeline_active = [
                t for t in candidates
                if str(t.get("task_mode") or "").lower() == "pipeline"
                and str(t.get("status") or "").lower() in {"todo", "doing"}
            ]
            if len(pipeline_active) == 1:
                return self._task_runtime_meta(pipeline_active[0])

        # 3) unique active task
        active = [t for t in candidates if str(t.get("status") or "").lower() in {"todo", "doing"}]
        if len(active) == 1:
            return self._task_runtime_meta(active[0])

        # 5) single candidate only
        if len(candidates) == 1:
            return self._task_runtime_meta(candidates[0])

        print(
            f"⚠️ Ambiguous topic->task resolve skipped topic={topic_id} "
            f"title_hint={title_hint!r} candidates={len(candidates)}"
        )
        return empty

    def _extract_task_run(self, content: str):
        if not content:
            return None
        # 支持旧格式([TASK_RUN]/title=description=)与新结构化格式(Agent/Task Title/Task Desc)
        if all(x not in content for x in ["[TASK_RUN]", "title=", "Task Title:"]):
            return None
        task_id_raw = (re.search(r"task_id=([^\s\n]+)", content) or [None, None])[1]
        task_id = self._normalize_task_id(task_id_raw)
        runner = (re.search(r"runner=([^\s\n]+)", content) or [None, self.agent_id])[1]
        exec_mode = (re.search(r"exec_mode=([^\s\n]+)", content) or [None, "reasoning"])[1]
        task_type = (re.search(r"type=([^\s\n]+)", content) or [None, "feature"])[1]

        title = ""
        desc = ""

        m1 = re.search(r"title=([^\n]+)", content)
        m2 = re.search(r"Task Title:\s*([^\n]+)", content)
        if m1:
            title = m1.group(1).strip()
        elif m2:
            title = m2.group(1).strip()

        d1 = re.search(r"description=(.*)", content, re.DOTALL)
        d2 = re.search(r"Task Desc:\s*([^\n]+)", content)
        if d1:
            desc = d1.group(1).strip()
        elif d2:
            desc = d2.group(1).strip()

        if not title and not desc:
            return None
        return {"task_id": task_id, "runner": runner, "exec_mode": exec_mode, "task_type": task_type, "title": title, "description": desc}

    def _validate_result(self, task_type: str, result_text: str) -> tuple[bool, str]:
        rt = (result_text or "").strip()
        if not rt:
            return False, "empty result"
        # 用户Requirements:产物不过滤，统一原样回传
        return True, "ok"

    def _cache_self_published(self, topic_id: str, content: str):
        key = f"{topic_id}|{(content or '').strip()[:800]}"
        now = time.time()
        self._recent_self_published = {k: ts for k, ts in self._recent_self_published.items() if now - ts < 180}
        self._recent_self_published[key] = now

    def _is_recent_self_published(self, topic_id: str, content: str) -> bool:
        key = f"{topic_id}|{(content or '').strip()[:800]}"
        ts = self._recent_self_published.get(key)
        if not ts:
            return False
        return (time.time() - ts) < 180

    def _is_duplicate_human_trigger(self, topic_id: str, sender: str, content: str, ttl_sec: int = 30) -> bool:
        key = f"{topic_id}|{sender}|{(content or '').strip()[:800]}"
        now = time.time()
        self._recent_human_trigger = {
            k: ts for k, ts in self._recent_human_trigger.items() if now - ts < ttl_sec
        }
        if key in self._recent_human_trigger:
            return True
        self._recent_human_trigger[key] = now
        return False

    def _build_topic_type_index(self, topics: list | None) -> dict:
        idx = {}
        for t in (topics or []):
            tid = t.get("topic_id") or t.get("id")
            ttype = t.get("topic_type") or t.get("type")
            if tid and ttype:
                idx[str(tid)] = str(ttype).lower()
        return idx

    def _discuss_should_trigger(self, content: str) -> bool:
        text = (content or "").lower()
        if re.search(r"(^|\s)@all(\b|$)", text):
            return True
        aliases = [self.agent_id, os.getenv("WTT_AGENT_NAME", ""), os.getenv("WTT_DISPLAY_NAME", "")]
        aliases = [a.strip().lower().replace(" ", "") for a in aliases if a and a.strip()]
        compact = text.replace(" ", "")
        for a in aliases:
            if f"@{a}" in compact:
                return True
        return False

    async def _is_task_topic_by_id(self, topic_id: str, topics: list | None = None) -> bool:
        now = time.time()
        cached = self._task_topic_cache.get(topic_id)
        if cached and (now - cached[1]) < 120:
            return bool(cached[0])

        is_task_topic = False
        topic_meta = next((t for t in (topics or []) if t.get("id") == topic_id), None)
        if topic_meta:
            ttype = str(topic_meta.get("type") or topic_meta.get("topic_type") or "").lower()
            name = (topic_meta.get("name") or "").upper()
            # Hard guard: P2P / broadcast topics are not task topics
            if ttype in {"p2p", "broadcast"}:
                is_task_topic = False
            else:
                # task_id in subscribed payload can be noisy for non-task topics;
                # require TASK- prefix or fall back to tasks-table verification.
                is_task_topic = bool(name.startswith("TASK-"))

        if not is_task_topic:
            try:
                r = await wtt_client.client.get(f"{wtt_client.api_url}/topics/{topic_id}")
                if r.status_code < 400:
                    t = r.json() if hasattr(r, "json") else {}
                    ttype = str(t.get("type") or t.get("topic_type") or "").lower()
                    name = (t.get("name") or "").upper()
                    if ttype in {"p2p", "broadcast"}:
                        is_task_topic = False
                    else:
                        is_task_topic = name.startswith("TASK-")
            except Exception:
                pass

        # 最终兜底：从 tasks 反查 topic_id（避免 topic 元数据缺失导致漏判 )
        if not is_task_topic:
            try:
                tr = await wtt_client.client.get(f"{wtt_client.api_url}/tasks?limit=500")
                if tr.status_code < 400:
                    tasks = tr.json() if hasattr(tr, "json") else []
                    is_task_topic = any((x.get("topic_id") == topic_id) for x in (tasks or []))
            except Exception:
                pass

        self._task_topic_cache[topic_id] = (bool(is_task_topic), now)
        if len(self._task_topic_cache) > 2000:
            self._task_topic_cache = dict(list(self._task_topic_cache.items())[-1000:])
        return bool(is_task_topic)

    def _extract_asset_paths_and_urls(self, text: str) -> tuple[list[str], list[str]]:
        t = (text or "")
        # 本地文件：优先文档/压缩/代码产物
        file_pat = re.compile(r"(?:^|[\s\(\[\"'])((?:/|\./|\.\./)[^\s\]\)\"']+\.(?:md|pdf|docx|xlsx|csv|json|txt|zip|tar|gz|py|js|ts|cpp|c|h))(?:$|[\s\]\)\"'])")
        # URL：可直接在 WTT/IM 中点击下载
        url_pat = re.compile(r"https?://[^\s]+")

        paths = []
        for m in file_pat.findall(t):
            p = os.path.abspath(os.path.expanduser(m.strip()))
            if os.path.isfile(p) and p not in paths:
                paths.append(p)

        urls = []
        for u in url_pat.findall(t):
            u2 = u.strip().rstrip('.,);]')
            if u2 not in urls:
                urls.append(u2)

        return paths, urls

    async def _set_task_status(self, task_id: str, status: str):
        try:
            resp = await wtt_client.client.patch(
                f"{wtt_client.api_url}/tasks/{task_id}",
                json={"status": status},
            )
            if resp.status_code >= 400:
                print(f"⚠️ Failed to set task status task_id={task_id} status={status} code={resp.status_code} body={resp.text[:200]}")
        except Exception as e:
            print(f"⚠️ Task status update exception task_id={task_id} status={status}: {e}")


    async def _update_task_output(self, task_id: str, output: str):
        """Write result text to task output field."""
        try:
            r = await wtt_client.client.patch(
                f"{wtt_client.api_url}/tasks/{task_id}",
                json={"output": output[:50000]},
                headers={"Content-Type": "application/json"},
                timeout=15,
            )
            r.raise_for_status()
            print(f"\u2705 Task {task_id[:12]} output updated ({len(output)} chars)")
        except Exception as e:
            print(f"\u26a0\ufe0f _update_task_output failed: {e}")

    async def recover_zombie_doing_tasks(self):
        """On startup, reset any 'doing' tasks owned by this agent back to 'todo',
        then also pick up all 'todo' tasks and re-trigger them."""
        recovered = []
        try:
            # Phase 1: reset doing → todo
            resp = await wtt_client.client.get(
                f"{wtt_client.api_url}/tasks",
                params={"status": "doing", "limit": 100},
                timeout=15,
            )
            if resp.status_code < 400:
                tasks = resp.json() if hasattr(resp, "json") else []
                for t in (tasks or []):
                    owner = str(t.get("runner_agent_id") or t.get("owner_agent_id") or t.get("created_by") or "")
                    if owner != self.agent_id:
                        # Also check if task belongs to a topic this agent is subscribed to
                        topic_id_check = str(t.get("topic_id") or "")
                        if topic_id_check not in self.subscribed_topics:
                            continue
                    task_id = str(t.get("id") or "")
                    title = str(t.get("title") or "?")[:30]
                    topic_id = str(t.get("topic_id") or "")
                    if not task_id:
                        continue
                    await self._set_task_status(task_id, "todo")
                    recovered.append((task_id, topic_id, title))
                    print(f"♻️  Reset zombie doing task → todo: {title} ({task_id[:12]})")
                if recovered:
                    print(f"♻️  Recovered {len(recovered)} zombie doing tasks on startup")

            # Phase 2: collect all todo tasks and auto-retrigger
            resp2 = await wtt_client.client.get(
                f"{wtt_client.api_url}/tasks",
                params={"status": "todo", "limit": 50},
                timeout=15,
            )
            if resp2.status_code < 400:
                todo_tasks = resp2.json() if hasattr(resp2, "json") else []
                retrigger = []
                for t in (todo_tasks or []):
                    owner = str(t.get("runner_agent_id") or t.get("owner_agent_id") or t.get("created_by") or "")
                    if owner != self.agent_id:
                        topic_id_check = str(t.get("topic_id") or "")
                        if topic_id_check not in self.subscribed_topics:
                            continue
                    task_id = str(t.get("id") or "")
                    topic_id = str(t.get("topic_id") or "")
                    title = str(t.get("title") or "?")[:30]
                    desc = str(t.get("description") or "")
                    exec_mode = str(t.get("exec_mode") or "reasoning")
                    task_type = str(t.get("type") or "feature")
                    if not task_id or not topic_id:
                        continue
                    retrigger.append((task_id, topic_id, title, desc, exec_mode, task_type))

                if retrigger:
                    print(f"🔄 Auto-retriggering {len(retrigger)} todo tasks on startup")
                    for task_id, topic_id, title, desc, exec_mode, task_type in retrigger:
                        print(f"  🚀 Retriggering: {title} ({task_id[:12]})")
                        asyncio.create_task(
                            self._execute_task_run(
                                topic_id, task_id, exec_mode, task_type, title, desc
                            )
                        )
                        await asyncio.sleep(0.3)
        except Exception as e:
            print(f"⚠️ recover_zombie_doing_tasks error: {e}")

    async def _set_task_notes(self, task_id: str, notes: str):
        try:
            resp = await wtt_client.client.patch(
                f"{wtt_client.api_url}/tasks/{task_id}",
                json={"notes": notes},
            )
            if resp.status_code >= 400:
                print(f"⚠️ Failed to set task notes task_id={task_id} code={resp.status_code} body={resp.text[:200]}")
        except Exception as e:
            print(f"⚠️ Task notes update exception task_id={task_id}: {e}")

    async def _get_task(self, task_id: str) -> dict:
        try:
            resp = await wtt_client.client.get(f"{wtt_client.api_url}/tasks/{task_id}")
            if resp.status_code < 400:
                data = resp.json() if hasattr(resp, "json") else {}
                return data if isinstance(data, dict) else {}
        except Exception:
            pass
        return {}

    def _extract_task_session_key_from_notes(self, notes: str) -> Optional[str]:
        m = re.search(r"\[WTT_TASK_SESSION\]\s*([\w:\-]+)", notes or "")
        return m.group(1).strip() if m else None

    async def _load_task_session_key_from_db(self, task_id: str) -> Optional[str]:
        task = await self._get_task(task_id)
        notes = str(task.get("notes") or "")
        return self._extract_task_session_key_from_notes(notes)

    async def _persist_task_session_key_to_db(self, task_id: str, session_key: str):
        task = await self._get_task(task_id)
        notes = str(task.get("notes") or "")
        marker = f"[WTT_TASK_SESSION] {session_key}"
        if not notes:
            new_notes = marker
        elif "[WTT_TASK_SESSION]" in notes:
            new_notes = re.sub(r"\[WTT_TASK_SESSION\]\s*[\w:\-]+", marker, notes)
        else:
            new_notes = f"{notes}\n{marker}".strip()
        await self._set_task_notes(task_id, new_notes)

    async def _clear_task_session_key_in_db(self, task_id: str):
        task = await self._get_task(task_id)
        notes = str(task.get("notes") or "")
        if "[WTT_TASK_SESSION]" not in notes:
            return
        new_notes = re.sub(r"\n?\[WTT_TASK_SESSION\]\s*[\w:\-]+", "", notes).strip()
        await self._set_task_notes(task_id, new_notes)

    async def _plan_task_by_agent(self, task_id: str, title: str, description: str) -> dict:
        prompt = (
            "You are a task planner. Do Plan Mode first, then Agent Mode. Output planning JSON only.\n"
            f"Task title: {title}\nTask description: {description}\n"
            "Output strict JSON format: {\"goal\":\"...\",\"phases\":[{\"id\":\"p1\",\"title\":\"...\",\"subtasks\":[{\"id\":\"p1s1\",\"title\":\"...\"}]}]}\n"
            "Requirements:至少2个phase，每个phase至少2个subtask，标题具体可执行。"
        )
        text = await self._infer_with_openclaw(prompt)
        m = re.search(r"\{[\s\S]*\}", text)
        if not m:
            raise RuntimeError("plan json not found")
        obj = json.loads(m.group(0))
        if not isinstance(obj, dict) or not obj.get("goal") or not isinstance(obj.get("phases"), list):
            raise RuntimeError("invalid plan json")
        return obj

    async def _publish_task_status(self, topic_id: str, task_id: str, executor_label: str, session_id: str, phase: str, progress: int, action: str, elapsed_sec: int = 0):
        if not self.publish_progress:
            return
        if progress == 0:
            await self._safe_publish(topic_id, "[STATUS] Started...")
        elif progress == 100:
            await self._safe_publish(topic_id, "[STATUS] Completed")

    def _upload_file_to_wtt_sync(self, file_path: str) -> str:
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            raise RuntimeError(f"file not found: {file_path}")

        boundary = f"----WTTBoundary{int(time.time() * 1000)}"
        data = p.read_bytes()
        head = (
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"file\"; filename=\"{p.name}\"\r\n"
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode("utf-8")
        tail = f"\r\n--{boundary}--\r\n".encode("utf-8")
        body = head + data + tail

        req = urllib.request.Request(f"{wtt_client.api_url.rstrip('/')}/media/upload", data=body, method="POST")
        req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
        req.add_header("Content-Length", str(len(body)))
        no_proxy_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with no_proxy_opener.open(req, timeout=90) as resp:
            raw = resp.read().decode("utf-8", "ignore")
        out = json.loads(raw or "{}")
        url = out.get("url")
        if not url:
            raise RuntimeError(f"upload failed: {raw[:200]}")
        if url.startswith("/"):
            url = f"{wtt_client.api_url.rstrip('/')}{url}"
        return url

    async def _upload_file_to_wtt(self, file_path: str) -> str:
        return await asyncio.to_thread(self._upload_file_to_wtt_sync, file_path)

    async def _publish_assets(self, topic_id: str, task_id: str, session_id: str, executor_label: str, asset_paths: list[str], asset_urls: list[str]):
        # 按需保留：当前策略不发布 FILE/LINK
        return

    async def _safe_publish(self, topic_id: str, content: str, retries: int = 3):
        payload = (content or "").strip()
        if not payload:
            return True
        # Strip [Model: ... | Effort: ...] tags injected by inference gateway
        payload = re.sub(r'\s*\[Model:\s*[^\]]*\]', '', payload).strip()
        if not payload:
            return True

        # Prefer WebSocket publish when connected
        if self._ws_runner and self._ws_runner.is_ws_connected:
            try:
                result = await self._ws_runner.send_action("publish", {
                    "topic_id": topic_id,
                    "content": payload,
                })
                if result is not None:
                    self._cache_self_published(topic_id, payload)
                    return True
            except Exception as e:
                print(f"⚠️ WS publish failed, falling back to HTTP: {e}")
        last_err = None
        for i in range(retries):
            try:
                await wtt_client.publish_message(topic_id, self.agent_id, payload)
                self._cache_self_published(topic_id, payload)
                return True
            except Exception as e:
                last_err = e
                await asyncio.sleep(0.5 * (i + 1))
        print(f"❌ publish failed after retries topic={topic_id}: {last_err}")
        return False

    def _parse_iso_ts(self, value: str) -> datetime | None:
        try:
            if not value:
                return None
            v = str(value).strip()
            if v.endswith("Z"):
                v = v[:-1] + "+00:00"
            dt = datetime.fromisoformat(v)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except Exception:
            return None

    async def task_progress_watchdog(self):
        """Fallback progress reporter every 60s for doing tasks (protects against missing mid-progress after restart)."""
        while True:
            try:
                resp = await wtt_client.client.get(
                    f"{wtt_client.api_url}/tasks",
                    params={"status": "doing", "limit": 200},
                    timeout=30,
                )
                if resp.status_code >= 400:
                    await asyncio.sleep(30)
                    continue
                tasks = resp.json() if hasattr(resp, "json") else []
                active_ids = set()
                now_mono = time.time()
                for t in (tasks or []):
                    task_owner = str(t.get("runner_agent_id") or t.get("owner_agent_id") or t.get("created_by") or "")
                    if task_owner != self.agent_id:
                        topic_id_check = str(t.get("topic_id") or "")
                        if topic_id_check not in self.subscribed_topics:
                            continue
                    # Fallback only for tasks in status=doing
                    if str(t.get("status") or "").lower() != "doing":
                        continue
                    task_id = str(t.get("id") or "")
                    topic_id = str(t.get("topic_id") or "")
                    title = str(t.get("title") or "untitled task")
                    if not task_id or not topic_id:
                        continue

                    # Report only tasks touched by this process recently to avoid stale doing records
                    touched_at = float(self._task_recent_touch.get(task_id, 0) or 0)
                    if touched_at <= 0:
                        continue

                    active_ids.add(task_id)
                    if task_id not in self._task_watch_first_seen:
                        self._task_watch_first_seen[task_id] = now_mono
                        self._task_watch_last_report[task_id] = 0

                    elapsed = max(0, int(now_mono - float(self._task_watch_first_seen.get(task_id, now_mono))))
                    if elapsed < self.task_progress_interval_sec:
                        continue
                    report_no = elapsed // self.task_progress_interval_sec
                    if report_no <= int(self._task_watch_last_report.get(task_id, 0)):
                        continue
                    self._task_watch_last_report[task_id] = report_no
                    minute = max(1, elapsed // 60)
                    progress_pct = min(95, max(20, minute * 20))
                    ts = time.strftime('%H:%M:%S')
                    if self.publish_progress:
                        await self._safe_publish(
                            topic_id,
                            f"Time: {ts}\n"
                            f"Progress: {progress_pct}%\n"
                            f"Status: [Task: {title}] reasoning running(running {minute} min )"
                        )
                    else:
                        print(f"📊 [watchdog] task={task_id[:12]} {progress_pct}% running {minute}min", flush=True)

                    # Stale detection: force-reset tasks stuck too long
                    first_seen = float(self._task_watch_first_seen.get(task_id, now_mono))
                    age = now_mono - first_seen
                    if age > self.task_stale_timeout_sec:
                        print(f"💀 Task {task_id[:12]} ({title}) stuck for {int(age)}s > {self.task_stale_timeout_sec}s, force reset")
                        try:
                            await self._set_task_status(task_id, "todo")
                            if self.publish_progress:
                                await self._safe_publish(
                                    topic_id,
                                    f"Time: {ts}\nProgress: 0%\n"
                                    f"Status: [Task: {title}] Timed out after {minute} min, will retry"
                                )
                            key_to_remove = None
                            for k in list(self.active_task_runs):
                                if task_id in k:
                                    key_to_remove = k
                                    break
                            if key_to_remove:
                                self.active_task_runs.discard(key_to_remove)
                        except Exception as reset_err:
                            print(f"⚠️ Failed to reset stale task {task_id[:12]}: {reset_err}")

                # Cleanup tracker for tasks no longer in doing
                stale = [tid for tid in self._task_watch_first_seen.keys() if tid not in active_ids]
                for tid in stale:
                    self._task_watch_first_seen.pop(tid, None)
                    self._task_watch_last_report.pop(tid, None)
                # 定期清理过旧 touch
                now_ts = time.time()
                self._task_recent_touch = {
                    k: ts for k, ts in self._task_recent_touch.items()
                    if (now_ts - float(ts)) < max(3600, self.task_max_runtime_sec + 600)
                }
            except Exception as e:
                print(f"⚠️ task progress watchdog error: {e}")
            await asyncio.sleep(30)

    async def _execute_task_run(self, topic_id: str, task_id: str, exec_mode: str = "reasoning", task_type: str = "feature", title: str = "", description: str = "", extra_note: str = ""):
        key = f"{topic_id}:{task_id}"
        if key in self._task_dedup:
            return
        self._task_dedup.add(key)
        self._task_recent_touch[task_id] = time.time()

        # Concurrency gate: wait for a slot before spawning gateway sessions
        acquired = self._task_semaphore.locked()
        if acquired:
            queue_pos = len(self._task_queue) + 1
            self._task_queue.append(key)
            print(f"⏳ Task {task_id} queued (position {queue_pos}, max concurrent={self.max_concurrent_tasks})")
            if self.publish_progress:
                await self._safe_publish(
                    topic_id,
                    f"Time: {time.strftime('%H:%M:%S')}\n"
                    f"Progress: 0%\n"
                    f"Status: [Task: {title or 'untitled task'}] Queued (position {queue_pos})"
                )

        try:
            async with self._task_semaphore:
                if key in self._task_queue:
                    self._task_queue.remove(key)
                self.active_task_runs.add(key)
                print(f"🚀 Task {task_id} acquired slot (active={len(self.active_task_runs)}, max={self.max_concurrent_tasks})")
                await self._execute_task_run_inner(topic_id, task_id, exec_mode, task_type, title, description, extra_note)
        finally:
            self.active_task_runs.discard(key)
            self._task_dedup.discard(key)

    async def _execute_task_run_inner(self, topic_id: str, task_id: str, exec_mode: str = "reasoning", task_type: str = "feature", title: str = "", description: str = "", extra_note: str = ""):
        self._task_recent_touch[task_id] = time.time()
        try:
            # Mark task as 'doing' immediately on start
            await self._set_task_status(task_id, "doing")
            concurrent_no = len(self.active_task_runs)
            session_id = f"wtt-task-{task_id}-{int(asyncio.get_event_loop().time())}"
            executor_label = self.agent_id if concurrent_no <= 1 else f"subagent-auto-{concurrent_no-1}"

            # Plan Mode: plan before execution; Agent Mode (default): reason directly
            phase_titles = []
            if exec_mode == "plan":
                try:
                    plan_obj = await self._plan_task_by_agent(task_id, title, description)
                    notes = f"{PLAN_PREFIX}{json.dumps(plan_obj, ensure_ascii=False)}"
                    await self._set_task_notes(task_id, notes)
                    phases = plan_obj.get("phases", []) or []

                    plan_detail_lines = []
                    for i, p in enumerate(phases, start=1):
                        p_title = str((p or {}).get("title") or f"阶段{i}").strip()
                        phase_titles.append(p_title)
                        plan_detail_lines.append(f"{i}. {p_title}")
                        for j, st in enumerate((p or {}).get("subtasks", []) or [], start=1):
                            plan_detail_lines.append(f"   {i}.{j} {str((st or {}).get('title') or f'子任务{i}.{j}').strip()}")

                    plan_lines = [f"Plan Mode result: total {len(phases)} phases"] + (plan_detail_lines or ["(no phase details extracted)"])
                    if self.publish_progress:
                        await self._safe_publish(topic_id, "\n".join(plan_lines))
                except Exception as e:
                    if self.publish_progress:
                        await self._safe_publish(topic_id, f"Plan Mode结果：失败\n原因: {e}")

            started_at = int(time.time())
            runtime_action = "Agent is reasoning..."
            if extra_note:
                runtime_action = "Processing follow-up input and updating conclusion"

            ts0 = time.strftime('%H:%M:%S')
            if self.publish_progress:
                await self._safe_publish(
                    topic_id,
                    f"Time: {ts0}\n"
                    f"Progress: 0%\n"
                    f"Status: [Task: {title or 'untitled task'}] {runtime_action}"
                )

            result_text = "Task execution finished and result returned."
            artifact_raw = ""
            # Always run reasoning (Agent Mode goes straight here; Plan Mode plans first, then reasons)
            try:
                is_followup = bool(extra_note)
                if is_followup:
                    # Incremental: only send the new user input, not full description again
                    run_desc = extra_note.strip()
                else:
                    run_desc = description

                runtime_action = "Reasoning started, preparing final answer"

                # 执行推理：即时完成即时回写；进度上报改为独立 ticker（避免主执行链路阻塞时丢分钟上报 )
                exec_task = asyncio.create_task(self._execute_by_agent(
                    task_id, title, run_desc, session_id,
                    is_followup=is_followup,
                    original_description=description if is_followup else "",
                ))

                async def _task_progress_ticker():
                    last_report_no = 0
                    while not exec_task.done():
                        await asyncio.sleep(5)
                        elapsed = max(0, int(time.time()) - started_at)

                        if elapsed < self.task_progress_interval_sec:
                            continue
                        report_no = elapsed // self.task_progress_interval_sec
                        if report_no <= last_report_no:
                            continue
                        last_report_no = report_no
                        minute = max(1, elapsed // 60)
                        progress_pct = min(95, max(20, minute * 20))
                        ts = time.strftime('%H:%M:%S')
                        phase_action = runtime_action
                        if phase_titles:
                            idx = min(max(0, minute - 1), len(phase_titles) - 1)
                            phase_action = f"Executing phase: {phase_titles[idx]}"
                        # Guard: don't let a slow publish block the ticker
                        try:
                            if self.publish_progress:
                                await asyncio.wait_for(
                                    self._safe_publish(
                                        topic_id,
                                        f"Time: {ts}\n"
                                        f"Progress: {progress_pct}%\n"
                                        f"Status: [Task: {title or 'untitled task'}] {phase_action}(running {minute} min )"
                                    ),
                                    timeout=15,
                                )
                            else:
                                print(f"📊 [progress] task={task_id[:12]} {progress_pct}% {phase_action}", flush=True)
                        except asyncio.TimeoutError:
                            print(f"⚠️ progress ticker publish timeout (task={task_id})")

                ticker_task = asyncio.create_task(_task_progress_ticker())
                try:
                    steps, mids, changes, result_text, artifact_raw = await asyncio.wait_for(
                        exec_task,
                        timeout=self.task_max_runtime_sec,
                    )
                finally:
                    ticker_task.cancel()
                    try:
                        await ticker_task
                    except asyncio.CancelledError:
                        pass
            except Exception as e:
                result_text = f"Reasoning failed: {e}"

            # 完成上报 + 全量结果
            ts_done = time.strftime('%H:%M:%S')
            done_action = f"{title or 'untitled task'} task completed"
            if phase_titles:
                done_action = f"All phases completed (total {len(phase_titles)} phases )"
            if self.publish_progress:
                await self._safe_publish(
                    topic_id,
                    f"Time: {ts_done}\n"
                    f"Progress: 100%\n"
                    f"Status: [Task: {title or 'untitled task'}] {done_action}"
                )

            publish_text = (artifact_raw or "").strip() or (result_text or "").strip()
            if publish_text:
                await self._safe_publish(topic_id, publish_text)


            # Write result to task output field for wtt-web display
            if publish_text and task_id:
                try:
                    await self._update_task_output(task_id, publish_text)
                except Exception as e:
                    print(f"\u26a0\ufe0f Failed to update task output: {e}")
            await self._set_task_status(task_id, "review")
        except Exception as e:
            print(f"❌ TASK_RUN execution failed task_id={task_id}: {e}")
        finally:
            # reject 重跑优先
            key = f"{topic_id}:{task_id}"
            queued = self.pending_reject_rerun.pop(key, None)
            if queued:
                q_topic = queued.get("topic_id") or topic_id
                q_task = queued.get("task_id") or task_id
                q_comment = (queued.get("comment") or "").strip()
                q_reviewer = queued.get("reviewer") or "reviewer"
                retry_note = f"reviewer={q_reviewer}; reject_comment={q_comment}" if q_comment else f"reviewer={q_reviewer}; reject"
                asyncio.create_task(
                    self._execute_task_run(
                        q_topic,
                        q_task,
                        exec_mode=queued.get("exec_mode") or "reasoning",
                        task_type=queued.get("task_type") or "feature",
                        title=queued.get("title") or "",
                        description=queued.get("description") or "",
                        extra_note=retry_note,
                    )
                )
                print("🔁 Continue execution")
                return

            # 普通信息流 queue：当前任务完成后合并补充信息，避免一次输入触发多轮重复推理
            qlist = self.pending_task_input_queue.get(key) or []
            if qlist:
                self.pending_task_input_queue.pop(key, None)
                merged = []
                seen = set()
                for item in qlist:
                    t = (item or '').strip()
                    if not t or t in seen:
                        continue
                    seen.add(t)
                    merged.append(t)
                if merged:
                    next_item = "\n\n".join(merged)
                    asyncio.create_task(
                        self._execute_task_run(
                            topic_id,
                            task_id,
                            exec_mode=exec_mode,
                            task_type=task_type,
                            title=title,
                            description=description,
                            extra_note=next_item,
                        )
                    )
                    print(f"📥 Resumed from queue with merged follow-ups (count={len(merged)} 条 )")

    async def process_wtt_messages(self, messages, topics):
        """处理 poll/WS 信息流：优先处理 TASK_RUN；可选自动推理+IM回写。"""
        topic_type_index = self._build_topic_type_index(topics)

        for msg in messages:
            msg_id = msg.get("id") or msg.get("message_id")
            if not msg_id or msg_id in self.processed_message_ids:
                continue

            content = (msg.get("content") or "").strip()
            topic_id = msg.get("topic_id")
            sender = msg.get("sender_id", "unknown")
            sender_type = str(msg.get("sender_type") or "").lower()

            # Update topic->task hint cache early (helps later no-task_id dispatch recovery).
            msg_task_id = self._normalize_task_id(msg.get("task_id") or "")
            if topic_id and msg_task_id:
                self._remember_topic_task_hint(topic_id, msg_task_id)
            hint_from_payload = self._extract_to_task_hint(content)
            if topic_id and hint_from_payload:
                self._remember_topic_task_hint(topic_id, hint_from_payload)

            # 1) 收到任务下发消息后自动执行（仅系统/agent下发，不处理 human general chat )
            tr = self._extract_task_run(content)
            semantic_type = str(msg.get("semantic_type") or "").upper()
            is_dispatch_msg = semantic_type in {"TASK_REQUEST", "TASK_RUN"} or "[TASK_RUN]" in content or "title=" in content or "Task Title:" in content
            if tr and topic_id and (sender_type != "human" or is_dispatch_msg):
                runner = tr.get("runner")
                task_id = self._normalize_task_id(tr.get("task_id") or msg_task_id)
                exec_mode = tr.get("exec_mode") or "reasoning"
                task_type = tr.get("task_type") or "feature"
                title = tr.get("title") or msg.get("task_title") or ""
                description = tr.get("description") or ""

                if not task_id:
                    resolved = await self._resolve_task_for_topic(
                        topic_id,
                        title_hint=title,
                        description_hint=description,
                        prefer_pipeline=("Pipeline auto-start" in content or "Upstream completed" in content),
                    )
                    task_id = self._normalize_task_id(resolved.get("task_id") or "")
                    title = resolved.get("title") or title
                    description = resolved.get("description") or description
                    exec_mode = resolved.get("exec_mode") or exec_mode
                    task_type = resolved.get("task_type") or task_type

                if (not runner) or (runner == self.agent_id):
                    if not task_id:
                        print(f"⚠️ Skip dispatch without task_id topic={topic_id} title={title!r}")
                        self.processed_message_ids.add(msg_id)
                        continue
                    self._remember_topic_task_hint(topic_id, task_id)
                    asyncio.create_task(self._execute_task_run(topic_id, task_id, exec_mode, task_type, title, description))
                    print("🚀 Execution started")
                    self.processed_message_ids.add(msg_id)
                    continue

            # 1.1) TASK_REVIEW approve: explicitly do not trigger reasoning (status/audit only)
            if "[TASK_REVIEW]" in content and "action=approve" in content:
                self.processed_message_ids.add(msg_id)
                continue

            # 1.2) TASK_REVIEW reject：带 comment 重新发回 Agent 执行
            if "[TASK_REVIEW]" in content and "action=reject" in content and topic_id:
                rej_task_id_raw = (re.search(r"task_id=([^\s\n]+)", content) or [None, None])[1]
                rej_task_id = self._normalize_task_id(rej_task_id_raw)
                reviewer = (re.search(r"by=([^\s\n]+)", content) or [None, "reviewer"])[1]
                exec_mode = (re.search(r"exec_mode=([^\s\n]+)", content) or [None, "reasoning"])[1]
                task_type = (re.search(r"type=([^\s\n]+)", content) or [None, "feature"])[1]
                title = (re.search(r"\ntitle=(.*)\n", content) or [None, ""])[1].strip()
                description = (re.search(r"\ndescription=(.*)\ncomment=", content, re.DOTALL) or [None, ""])[1].strip()
                comment = (re.search(r"comment=(.*)", content, re.DOTALL) or [None, ""])[1].strip()
                if rej_task_id:
                    key = f"{topic_id}:{rej_task_id}"
                    now = time.time()
                    last_ts = self.last_reject_rerun_ts.get(key, 0)

                    # If same task is running: enqueue and rerun after current execution
                    if key in self._task_dedup:
                        self.pending_reject_rerun[key] = {
                            "topic_id": topic_id,
                            "task_id": rej_task_id,
                            "exec_mode": exec_mode,
                            "task_type": task_type,
                            "title": title,
                            "description": description,
                            "reviewer": reviewer,
                            "comment": comment,
                            "queued_at": int(now),
                        }
                    # 防抖2：短时间重复reject只触发一次
                    elif now - last_ts < self.reject_rerun_cooldown_sec:
                        print("⏭️ Rerun ignored (cooldown active)")
                    else:
                        self.last_reject_rerun_ts[key] = now
                        retry_note = f"reviewer={reviewer}; reject_comment={comment}" if comment else f"reviewer={reviewer}; reject"

                        asyncio.create_task(
                            self._execute_task_run(
                                topic_id,
                                rej_task_id,
                                exec_mode=exec_mode,
                                task_type=task_type,
                                title=title,
                                description=description,
                                extra_note=retry_note,
                            )
                        )
                        print("🔁 Rerun triggered")

            # 1.2) Auto-published messages from this agent: do not re-enter reasoning (anti-echo);
            #      manual inputs from same agent in wtt-web can still trigger reasoning.
            if sender == self.agent_id and self._is_recent_self_published(topic_id, content):
                self.processed_message_ids.add(msg_id)
                continue

            # 2) topic reasoning rules (task / p2p / discuss / subscriber)
            raw_task_id_meta = msg.get("task_id")
            # only UUID-like task_id should mark task topic; ignore pseudo ids like p2p-<topic>
            task_id_meta = str(raw_task_id_meta) if raw_task_id_meta and re.match(r"^[0-9a-fA-F-]{32,}$", str(raw_task_id_meta)) else None
            is_task_topic = bool(task_id_meta)
            if not is_task_topic and topic_id:
                is_task_topic = await self._is_task_topic_by_id(topic_id, topics)

            topic_type = str(msg.get("topic_type") or msg.get("type") or topic_type_index.get(str(topic_id), "")).lower()
            if (not topic_type) and topic_id:
                try:
                    tr = await wtt_client.client.get(f"{wtt_client.api_url}/topics/{topic_id}")
                    if tr.status_code < 400:
                        tj = tr.json() if hasattr(tr, "json") else {}
                        topic_type = str(tj.get("type") or tj.get("topic_type") or "").lower()
                except Exception:
                    pass

            is_system_msg = any(tag in content for tag in [
                "[TASK_RUN]", "[TASK_STATUS]", "[TASK_PLAN]", "[TASK_PART]",
                "[TASK_CHANGE]", "[TASK_SUMMARY]", "[TASK_BLOCKED]",
                "[TASK_ARTIFACT]", "[TASK_ASSET]", "[TASK_ASK]",
                "[TASK_REVIEW]", self.poll_llm_marker,
            ])

            # Non-task topic: decide whether to trigger thinking by topic type
            if not is_task_topic:
                should_think = False
                sender_kind = (sender_type or "").lower()

                # human message unlocks anti-loop guard
                if sender_kind == "human" and topic_id:
                    self._topic_auto_guard[topic_id] = {"last_ts": 0.0, "count": 0, "locked": False}

                if content and (not is_system_msg) and sender != self.agent_id and sender_kind != "system":
                    if topic_type == "p2p":
                        # p2p: human -> think; agent -> mention-triggered only
                        if sender_kind == "human":
                            should_think = True
                        elif sender_kind == "agent":
                            should_think = self._discuss_should_trigger(content)
                    elif topic_type in {"discussion", "collaborative"}:
                        # discuss: default no-reply; trigger on @all / @me only
                        should_think = self._discuss_should_trigger(content)
                    elif topic_type == "broadcast":
                        # subscriber topic: never think
                        should_think = False

                # Anti ping-pong for agent-origin triggers
                if should_think and topic_id and sender_kind == "agent":
                    now = time.time()
                    st = self._topic_auto_guard.get(topic_id, {"last_ts": 0.0, "count": 0, "locked": False})
                    if st.get("locked"):
                        should_think = False
                    elif now - float(st.get("last_ts") or 0.0) < 15:
                        should_think = False
                    elif int(st.get("count") or 0) >= 2:
                        st["locked"] = True
                        should_think = False
                    self._topic_auto_guard[topic_id] = st

                if should_think:
                    prompt = (
                        "You are a WTT topic assistant. Provide a concise and useful reply.\n"
                        "Rule: output final user-facing content only; no process narration.\n\n"
                        f"topic_type: {topic_type or 'unknown'}\n"
                        f"topic_id: {topic_id}\n"
                        f"sender: {sender}\n"
                        f"content:\n{content}\n"
                    )
                    try:
                        reasoning = await self._infer_with_openclaw(
                            prompt,
                            topic_id=topic_id or "",
                            title=(content[:24] + "...") if len(content) > 24 else content,
                        )
                        if topic_id and reasoning:
                            ok = await self._safe_publish(topic_id, reasoning)
                            if ok and sender_kind == "agent":
                                st = self._topic_auto_guard.get(topic_id, {"last_ts": 0.0, "count": 0, "locked": False})
                                st["last_ts"] = time.time()
                                st["count"] = int(st.get("count") or 0) + 1
                                self._topic_auto_guard[topic_id] = st
                    except Exception as e:
                        print(f"❌ 非task topic Reasoning failed: {e}")

                self.processed_message_ids.add(msg_id)
                continue

            # task topic：仅 human 消息触发（self/system 跳过 )
            if not content or is_system_msg or sender_type != "human" or sender == self.agent_id:
                self.processed_message_ids.add(msg_id)
                continue

            # Guard against rapid duplicate websocket deliveries of same human input
            if self._is_duplicate_human_trigger(topic_id or "", sender or "", content):
                self.processed_message_ids.add(msg_id)
                continue

            # Resolve concrete task id/meta for this task topic (chat/send path usually has no task_id in payload)
            resolved_task_id = task_id_meta
            resolved_title = msg.get("task_title") or ""
            resolved_desc = ""
            resolved_exec_mode = "reasoning"
            resolved_task_type = "feature"
            if topic_id and (not resolved_task_id):
                resolved = await self._resolve_task_for_topic(
                    topic_id,
                    title_hint=resolved_title,
                    description_hint=resolved_desc,
                    prefer_pipeline=False,
                )
                resolved_task_id = resolved.get("task_id") or resolved_task_id
                resolved_title = resolved.get("title") or resolved_title
                resolved_desc = resolved.get("description") or resolved_desc
                resolved_exec_mode = resolved.get("exec_mode") or resolved_exec_mode
                resolved_task_type = resolved.get("task_type") or resolved_task_type

            if topic_id and resolved_task_id:
                self._remember_topic_task_hint(topic_id, resolved_task_id)

            # Task running: queue user supplemental input and process after completion
            queue_key = f"{topic_id}:{resolved_task_id or 'unknown'}"
            if queue_key in self._task_dedup:
                q = self.pending_task_input_queue.get(queue_key) or []
                # avoid stacking duplicate supplements while current run is in progress
                if not q or q[-1].strip() != content.strip():
                    q.append(content)
                self.pending_task_input_queue[queue_key] = q
                self.processed_message_ids.add(msg_id)
                continue

            # Task topic human chat should run task flow (with progress + doing->review), not plain chat infer.
            if topic_id and resolved_task_id:
                asyncio.create_task(
                    self._execute_task_run(
                        topic_id,
                        resolved_task_id,
                        exec_mode=resolved_exec_mode,
                        task_type=resolved_task_type,
                        title=resolved_title,
                        description=resolved_desc,
                        extra_note=content,
                    )
                )
                self.processed_message_ids.add(msg_id)
                continue

            # Fallback: non-resolved messages use plain infer
            ctype = msg.get("content_type", "text")
            prompt = (
                "You are a WTT task assistant. The user sent a message in task dialog; provide a targeted reply.\n"
                "Reply directly to the user request; do not use rigid templates.\n\n"
                + (f"Task title: {resolved_title}\n" if resolved_title else "")
                + f"topic_id: {topic_id}\n"
                f"sender: {sender}\n"
                f"content_type: {ctype}\n"
                f"content:\n{content}\n"
            )

            try:
                reasoning = await self._infer_with_openclaw(
                    prompt,
                    topic_id=topic_id or "",
                    title=(resolved_title or content[:24] or "general chat"),
                )
                if topic_id:
                    await self._safe_publish(topic_id, reasoning)
            except Exception as e:
                print(f"❌ Reasoning failed: {e}")
            finally:
                self.processed_message_ids.add(msg_id)
                if len(self.processed_message_ids) > 5000:
                    self.processed_message_ids = set(list(self.processed_message_ids)[-3000:])


async def main():
    """Main function"""
    import sys
    # Enable line-buffered output
    sys.stdout.reconfigure(line_buffering=True)
    
    print("="*80, flush=True)
    print("WTT Skill real-time service (WebSocket only)", flush=True)
    print("="*80, flush=True)
    print(flush=True)

    # 创建 Agent（无感：优先读取已持久化 agent_id，不存在则自动生成 )
    agent_id = _resolve_local_agent_id()
    agent = OpenClawAgent(agent_id)

    # 创建并启动 WTT Runner（仅 WebSocket 链路 )
    interval = int(os.getenv("WTT_POLL_INTERVAL", "30"))
    api_base = os.getenv("WTT_API_URL", getattr(wtt_client, "api_url", "https://www.waxbyte.com"))
    default_ws_url = api_base.replace("https://", "wss://").replace("http://", "ws://").rstrip("/") + "/ws"
    ws_url = os.getenv("WTT_WS_URL", default_ws_url)
    mode = "websocket"
    runner = WTTSkillRunner(agent, interval=interval, mode=mode, ws_url=ws_url)
    agent._ws_runner = runner  # wire up WS runner for publish-over-WS
    await runner.start()
    # Sync subscribed topics from runner cache to agent for ownership checks
    agent.subscribed_topics = set(runner._subscribed_topics.keys())
    await agent.recover_zombie_doing_tasks()
    watchdog_task = asyncio.create_task(agent.task_progress_watchdog())

    print("\n" + "="*80, flush=True)
    print("✅ Service started", flush=True)
    print("="*80, flush=True)
    print(f"• Mode: {mode}", flush=True)
    if mode == "websocket":
        print(f"• WebSocket: {ws_url}/{agent.agent_id}", flush=True)
        print("• Notifications and reasoning via WebSocket only", flush=True)
    else:
        print(f"• Polling interval: {interval}s", flush=True)
    print(f"• Primary route: {agent.im_channel}:{','.join(agent.im_targets) if agent.im_targets else '(target not configured)'}", flush=True)
    if agent.im_fallback_routes:
        fallback_text = ', '.join([f"{c}:{t}" for c, t in agent.im_fallback_routes])
        print(f"• Fallback routes: {fallback_text}", flush=True)
    print("• Press Ctrl+C to stop", flush=True)
    print("="*80 + "\n", flush=True)

    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Stopping service...")
        watchdog_task.cancel()
        try:
            await watchdog_task
        except asyncio.CancelledError:
            pass
        await runner.stop()
        await wtt_client.client.aclose()
        print("✅ Service stopped")


if __name__ == "__main__":
    asyncio.run(main())
