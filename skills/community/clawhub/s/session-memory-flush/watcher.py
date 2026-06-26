#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw session memory flush watcher.

优先读取 ~/.openclaw/openclaw.json 中 agents.defaults.model.primary 指定的模型做 LLM 摘要。
如果无法读取或调用失败，自动降级为轻量规则摘要，保证标准交付后仍能运行。
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
import shutil
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


HOME = Path.home()
OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", HOME / ".openclaw")).expanduser()
WORKSPACE_DIR = Path(os.environ.get("OPENCLAW_WORKSPACE", OPENCLAW_HOME / "workspace")).expanduser()
SKILL_DIR = Path(__file__).resolve().parent
STATE_FILE = SKILL_DIR / "state" / "flushed_sessions.json"
PROMPT_FILE = SKILL_DIR / "summarize_prompt.md"
OPENCLAW_CONFIG = OPENCLAW_HOME / "openclaw.json"
DEFAULT_AGENT_ID = os.environ.get("OPENCLAW_AGENT_ID", "main")
DEFAULT_WORKSPACE_FALLBACK = OPENCLAW_HOME / "workspace"

MAX_MESSAGES = int(os.environ.get("SESSION_MEMORY_MAX_MESSAGES", "80"))
MAX_CHARS = int(os.environ.get("SESSION_MEMORY_MAX_CHARS", "24000"))


def deep_get(obj: Any, *path: str) -> Any:
    current = obj
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def load_json_file(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def load_openclaw_config() -> Dict[str, Any]:
    return load_json_file(OPENCLAW_CONFIG)


def session_agent_id(session: Optional[Dict[str, Any]] = None) -> str:
    if isinstance(session, dict):
        value = session.get("agentId") or session.get("agent_id")
        if value:
            return str(value)
    return DEFAULT_AGENT_ID


def load_agent_models(agent_id: Optional[str] = None) -> Dict[str, Any]:
    resolved = agent_id or DEFAULT_AGENT_ID
    models_file = OPENCLAW_HOME / "agents" / resolved / "agent" / "models.json"
    return load_json_file(models_file)


def session_memory_config() -> Dict[str, Any]:
    cfg = load_openclaw_config()
    for path in (
        ("sessionMemoryFlush",),
        ("skills", "sessionMemoryFlush"),
    ):
        value = deep_get(cfg, *path)
        if isinstance(value, dict):
            return value
    return {}


def positive_int(value: Any) -> Optional[int]:
    if value in (None, ""):
        return None
    try:
        parsed = int(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def resolve_idle_minutes(session_type: str) -> int:
    env_name = "SESSION_MEMORY_GROUP_IDLE_MINUTES" if session_type == "group" else "SESSION_MEMORY_DM_IDLE_MINUTES"
    env_value = positive_int(os.environ.get(env_name))
    if env_value:
        return env_value

    custom = session_memory_config()
    custom_value = None
    if session_type == "group":
        custom_value = (
            positive_int(custom.get("groupIdleMinutes"))
            or positive_int(deep_get(custom, "idleMinutes", "group"))
        )
    else:
        custom_value = (
            positive_int(custom.get("dmIdleMinutes"))
            or positive_int(custom.get("directIdleMinutes"))
            or positive_int(deep_get(custom, "idleMinutes", "dm"))
            or positive_int(deep_get(custom, "idleMinutes", "direct"))
        )
    if custom_value:
        return custom_value

    cfg = load_openclaw_config()
    if session_type == "group":
        config_value = (
            positive_int(deep_get(cfg, "session", "resetByType", "group", "idleMinutes"))
            or positive_int(deep_get(cfg, "session", "reset", "idleMinutes"))
            or positive_int(deep_get(cfg, "session", "idleMinutes"))
        )
        return config_value or 30

    config_value = (
        positive_int(deep_get(cfg, "session", "resetByType", "direct", "idleMinutes"))
        or positive_int(deep_get(cfg, "session", "resetByType", "dm", "idleMinutes"))
        or positive_int(deep_get(cfg, "session", "reset", "idleMinutes"))
        or positive_int(deep_get(cfg, "session", "idleMinutes"))
    )
    return config_value or 5


def resolve_timer_minutes() -> int:
    env_value = positive_int(os.environ.get("SESSION_MEMORY_TIMER_MINUTES"))
    if env_value:
        return env_value

    custom = session_memory_config()
    custom_value = (
        positive_int(custom.get("timerMinutes"))
        or positive_int(deep_get(custom, "schedule", "timerMinutes"))
    )
    if custom_value:
        return custom_value

    dm_idle = resolve_idle_minutes("dm")
    group_idle = resolve_idle_minutes("group")
    return max(1, min(dm_idle, group_idle) - 1)


def resolve_scan_window_minutes(session_type: str) -> int:
    env_name = "SESSION_MEMORY_SCAN_WINDOW_GROUP" if session_type == "group" else "SESSION_MEMORY_SCAN_WINDOW_DM"
    env_value = positive_int(os.environ.get(env_name))
    if env_value:
        return env_value

    custom = session_memory_config()
    custom_value = None
    if session_type == "group":
        custom_value = (
            positive_int(custom.get("groupScanWindowMinutes"))
            or positive_int(deep_get(custom, "scanWindowMinutes", "group"))
        )
    else:
        custom_value = (
            positive_int(custom.get("dmScanWindowMinutes"))
            or positive_int(custom.get("directScanWindowMinutes"))
            or positive_int(deep_get(custom, "scanWindowMinutes", "dm"))
            or positive_int(deep_get(custom, "scanWindowMinutes", "direct"))
        )
    if custom_value:
        return custom_value

    idle_minutes = resolve_idle_minutes(session_type)
    return min(resolve_timer_minutes(), max(1, idle_minutes - 1))


def resolve_default_agent_id(cfg: Optional[Dict[str, Any]] = None) -> str:
    config = cfg if isinstance(cfg, dict) else load_openclaw_config()
    candidates = (
        deep_get(config, "agents", "default"),
        deep_get(config, "agents", "defaultAgentId"),
        deep_get(config, "agents", "defaults", "id"),
    )
    for value in candidates:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return "main"


def resolve_agent_workspace_dir(agent_id: Optional[str] = None) -> Path:
    cfg = load_openclaw_config()
    resolved_agent_id = (agent_id or DEFAULT_AGENT_ID or "main").strip() or "main"

    agents = deep_get(cfg, "agents", "list")
    if isinstance(agents, list):
        for item in agents:
            if not isinstance(item, dict):
                continue
            item_id = str(item.get("id") or item.get("agentId") or "").strip()
            if item_id != resolved_agent_id:
                continue
            configured = item.get("workspace")
            if isinstance(configured, str) and configured.strip():
                return Path(configured).expanduser()

    default_workspace = deep_get(cfg, "agents", "defaults", "workspace")
    default_workspace_path = (
        Path(default_workspace).expanduser()
        if isinstance(default_workspace, str) and default_workspace.strip()
        else DEFAULT_WORKSPACE_FALLBACK
    )

    if resolved_agent_id == resolve_default_agent_id(cfg):
        return default_workspace_path
    return default_workspace_path.parent / f"workspace-{resolved_agent_id}"


def resolve_memory_dir(session: Optional[Dict[str, Any]] = None) -> Path:
    configured = os.environ.get("SESSION_MEMORY_OUTPUT_DIR", "").strip()
    if configured:
        return Path(configured).expanduser()
    custom_output_dir = session_memory_config().get("outputDir")
    if isinstance(custom_output_dir, str) and custom_output_dir.strip():
        return Path(custom_output_dir).expanduser()

    agent_workspace = resolve_agent_workspace_dir(session_agent_id(session))
    workspace_memory = agent_workspace / "memory"
    if agent_workspace.exists() or workspace_memory.exists():
        return workspace_memory
    return OPENCLAW_HOME / "memory"


def now_local() -> dt.datetime:
    return dt.datetime.now().astimezone()


def parse_time(value: Any) -> Optional[dt.datetime]:
    if not value:
        return None
    if isinstance(value, (int, float)):
        seconds = value / 1000 if value > 10_000_000_000 else value
        return dt.datetime.fromtimestamp(seconds, tz=dt.timezone.utc).astimezone()
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.datetime.now().astimezone().tzinfo)
    return parsed.astimezone()


def run_openclaw_sessions() -> List[Dict[str, Any]]:
    openclaw_bin = os.environ.get("OPENCLAW_BIN", "").strip() or shutil.which("openclaw")
    if not openclaw_bin:
        raise RuntimeError("openclaw command not found; set OPENCLAW_BIN to the absolute path")

    cmd = [openclaw_bin, "sessions", "--all-agents", "--json"]
    proc = subprocess.run(
        cmd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed: {proc.stderr.strip()}")
    data = json.loads(proc.stdout)
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    if isinstance(data, dict):
        for key in ("sessions", "items", "data"):
            value = data.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
    return []


def load_state() -> Dict[str, Any]:
    if not STATE_FILE.exists():
        return {"flushed_sessions": {}}
    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {"flushed_sessions": {}}
    if not isinstance(data, dict):
        return {"flushed_sessions": {}}
    data.setdefault("flushed_sessions", {})
    return data


def save_state(state: Dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.replace(STATE_FILE)


def get_first(session: Dict[str, Any], names: Iterable[str]) -> Any:
    for name in names:
        if name in session and session[name] not in (None, ""):
            return session[name]
    return None


def session_id_of(session: Dict[str, Any]) -> Optional[str]:
    value = get_first(session, ("sessionId", "session_id", "id"))
    return str(value) if value else None


def session_type_of(session: Dict[str, Any]) -> str:
    raw = str(get_first(session, ("type", "chatType", "conversationType", "scope")) or "").lower()
    if "group" in raw or "room" in raw:
        return "group"
    return "dm"


def last_activity_of(session: Dict[str, Any]) -> Optional[dt.datetime]:
    return parse_time(
        get_first(
            session,
            (
                "lastActivityAt",
                "last_activity_at",
                "updatedAt",
                "updated_at",
                "lastMessageAt",
                "last_message_at",
                "createdAt",
                "created_at",
            ),
        )
    )


def idle_policy(session_type: str) -> Tuple[int, int]:
    if session_type == "group":
        return resolve_idle_minutes("group"), resolve_scan_window_minutes("group")
    return resolve_idle_minutes("dm"), resolve_scan_window_minutes("dm")


def should_flush(session: Dict[str, Any], force: bool = False) -> Tuple[bool, str]:
    if force:
        return True, "forced"
    typ = session_type_of(session)
    idle_minutes, scan_window = idle_policy(typ)
    last_activity = last_activity_of(session)
    if not last_activity:
        return False, "missing lastActivityAt"
    elapsed = (now_local() - last_activity).total_seconds() / 60
    remaining = idle_minutes - elapsed
    if remaining <= scan_window:
        return True, f"{typ} idle remaining {remaining:.1f}min <= {scan_window}min"
    return False, f"{typ} idle remaining {remaining:.1f}min"


def find_transcript(session_id: str, session: Dict[str, Any]) -> Optional[Path]:
    candidates: List[Path] = []
    for key in ("transcriptPath", "transcript_path", "jsonlPath", "jsonl_path", "path"):
        value = session.get(key)
        if value:
            candidates.append(Path(str(value)).expanduser())

    agent_id = session_agent_id(session)
    candidates.extend(
        [
            OPENCLAW_HOME / "agents" / agent_id / "sessions" / f"{session_id}.jsonl",
            OPENCLAW_HOME / "agents" / agent_id / "sessions" / f"{session_id}.trajectory.jsonl",
            OPENCLAW_HOME / "agents" / "*" / "sessions" / f"{session_id}.jsonl",
            OPENCLAW_HOME / "agents" / "*" / "sessions" / f"{session_id}.trajectory.jsonl",
            OPENCLAW_HOME / "sessions" / f"{session_id}.jsonl",
            OPENCLAW_HOME / "logs" / f"{session_id}.jsonl",
        ]
    )

    for item in candidates:
        if "*" in str(item):
            matches = list(OPENCLAW_HOME.glob(str(item.relative_to(OPENCLAW_HOME))))
            existing = [p for p in matches if p.is_file()]
            if existing:
                return max(existing, key=lambda p: p.stat().st_mtime)
        elif item.is_file():
            return item
    return find_recent_jsonl_by_name(session_id)


def find_recent_jsonl_by_name(session_id: str) -> Optional[Path]:
    matches = list(OPENCLAW_HOME.rglob(f"{session_id}.jsonl"))
    matches.extend(OPENCLAW_HOME.rglob(f"{session_id}.trajectory.jsonl"))
    if matches:
        return max(matches, key=lambda p: p.stat().st_mtime)
    partial = list(OPENCLAW_HOME.rglob(f"*{session_id}*.jsonl"))
    if partial:
        return max(partial, key=lambda p: p.stat().st_mtime)
    return None


def iter_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                yield value


def flatten_content(content: Any) -> Optional[str]:
    if isinstance(content, str):
        return content.strip() or None
    if isinstance(content, dict):
        return flatten_content(content.get("text") or content.get("content") or content.get("message"))
    if isinstance(content, list):
        parts = []
        for item in content:
            text = flatten_content(item)
            if text:
                parts.append(text)
        joined = "\n".join(parts).strip()
        return joined or None
    return None


def message_text(obj: Dict[str, Any]) -> Optional[Tuple[str, str]]:
    payload = obj.get("message") if isinstance(obj.get("message"), dict) else None
    role = str(
        obj.get("role")
        or (payload or {}).get("role")
        or obj.get("type")
        or obj.get("sender")
        or "unknown"
    )
    content = flatten_content(
        obj.get("content")
        or obj.get("text")
        or payload
        or obj.get("message")
    )
    if not content:
        return None
    return role, content


def extract_trajectory_messages(obj: Dict[str, Any]) -> List[Tuple[str, str]]:
    if obj.get("traceSchema") != "openclaw-trajectory":
        return []
    data = obj.get("data") if isinstance(obj.get("data"), dict) else {}
    items: List[Tuple[str, str]] = []

    prompt = flatten_content(data.get("prompt") or data.get("finalPromptText"))
    if prompt:
        items.append(("user", prompt))

    for message in data.get("messagesSnapshot") or []:
        if not isinstance(message, dict):
            continue
        role = str(message.get("role") or "unknown")
        if role not in {"user", "assistant", "system"}:
            continue
        content = flatten_content(message.get("content"))
        if content and len(content) <= 4000:
            items.append((role, content))

    for text in data.get("assistantTexts") or []:
        content = flatten_content(text)
        if content:
            items.append(("assistant", content))

    return items


def read_transcript_text(path: Path) -> str:
    messages: List[str] = []
    for obj in iter_jsonl(path):
        trajectory_items = extract_trajectory_messages(obj)
        if trajectory_items:
            for role, content in trajectory_items:
                messages.append(f"{role}: {content}")
            continue
        item = message_text(obj)
        if item:
            role, content = item
            messages.append(f"{role}: {content}")
    tail = dedupe(messages)[-MAX_MESSAGES:]
    text = "\n\n".join(tail)
    if len(text) > MAX_CHARS:
        text = text[-MAX_CHARS:]
    return text


def resolve_model_config(session: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, str]]:
    env_base_url = os.environ.get("SESSION_MEMORY_LLM_BASE_URL", "").rstrip("/")
    env_api_key = os.environ.get("SESSION_MEMORY_LLM_API_KEY", "")
    env_model = os.environ.get("SESSION_MEMORY_LLM_MODEL", "")
    env_api = os.environ.get("SESSION_MEMORY_LLM_API", "openai-chat-completions")
    if env_base_url and env_api_key and env_model:
        return {
            "base_url": env_base_url,
            "api_key": env_api_key,
            "model": env_model,
            "api": env_api,
            "source": "env",
        }

    cfg = load_openclaw_config()
    primary = (
        cfg.get("agents", {})
        .get("defaults", {})
        .get("model", {})
        .get("primary")
    )
    if not isinstance(primary, str) or "/" not in primary:
        return None

    provider_id, model_id = primary.split("/", 1)
    agent_id = session_agent_id(session)

    provider = load_agent_models(agent_id).get("providers", {}).get(provider_id, {})
    source = f"models.json:{agent_id}:{primary}"
    if not isinstance(provider, dict) or not provider:
        provider = cfg.get("models", {}).get("providers", {}).get(provider_id, {})
        source = f"openclaw.json:{primary}"
    if not isinstance(provider, dict):
        return None

    base_url = str(provider.get("baseUrl") or provider.get("base_url") or "").rstrip("/")
    api_key = str(provider.get("apiKey") or provider.get("api_key") or "")
    api = str(provider.get("api") or "openai-chat-completions")
    if not (base_url and api_key and model_id):
        return None
    return {
        "base_url": base_url,
        "api_key": api_key,
        "model": model_id,
        "api": api,
        "source": source,
        "agent_id": agent_id,
    }


def call_llm_summary(transcript: str, session: Optional[Dict[str, Any]] = None) -> Optional[str]:
    model_cfg = resolve_model_config(session)
    if not model_cfg:
        return None
    prompt = PROMPT_FILE.read_text(encoding="utf-8") if PROMPT_FILE.exists() else ""
    api = model_cfg["api"]
    if api == "openai-responses":
        return call_openai_responses_summary(model_cfg, prompt, transcript)
    return call_chat_completions_summary(model_cfg, prompt, transcript)


def call_chat_completions_summary(model_cfg: Dict[str, str], prompt: str, transcript: str) -> Optional[str]:
    payload = {
        "model": model_cfg["model"],
        "messages": [
            {"role": "system", "content": prompt or "请总结 session 中值得长期记住的信息。"},
            {"role": "user", "content": transcript},
        ],
        "temperature": 0.2,
    }
    req = urllib.request.Request(
        f"{model_cfg['base_url']}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {model_cfg['api_key']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    choices = data.get("choices") or []
    if not choices:
        return None
    message = choices[0].get("message") or {}
    content = message.get("content")
    return content.strip() if isinstance(content, str) and content.strip() else None


def call_openai_responses_summary(model_cfg: Dict[str, str], prompt: str, transcript: str) -> Optional[str]:
    payload = {
        "model": model_cfg["model"],
        "input": [
            {"role": "system", "content": prompt or "请总结 session 中值得长期记住的信息。"},
            {"role": "user", "content": transcript},
        ],
        "stream": True,
    }
    req = urllib.request.Request(
        f"{model_cfg['base_url']}/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {model_cfg['api_key']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, TimeoutError):
        return None

    text = extract_responses_sse_text(body)
    if text:
        return text

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    return extract_responses_text(data)


def extract_responses_sse_text(body: str) -> Optional[str]:
    chunks: List[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip()
        if not line.startswith("data: "):
            continue
        payload = line[6:]
        if not payload or payload == "[DONE]":
            continue
        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "response.output_text.delta":
            delta = event.get("delta")
            if isinstance(delta, str) and delta:
                chunks.append(delta)
        elif event.get("type") == "response.output_text.done" and not chunks:
            text = event.get("text")
            if isinstance(text, str) and text:
                chunks.append(text)
    joined = "".join(chunks).strip()
    return joined or None


def extract_responses_text(data: Dict[str, Any]) -> Optional[str]:
    direct = data.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    chunks: List[str] = []
    output = data.get("output")
    if isinstance(output, list):
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for part in content:
                if not isinstance(part, dict):
                    continue
                text = part.get("text")
                if isinstance(text, str) and text.strip():
                    chunks.append(text.strip())
    if chunks:
        return "\n".join(chunks).strip()
    return None


def local_summary(transcript: str) -> str:
    lines = [line.strip() for line in transcript.splitlines() if line.strip()]
    useful: List[str] = []
    keywords = (
        "结论",
        "决定",
        "方案",
        "配置",
        "路径",
        "命令",
        "问题",
        "风险",
        "待办",
        "todo",
        "TODO",
        "openclaw",
        "session",
        "skill",
        "memory",
        "好用",
        "更喜欢",
        "偏向",
        "更适合",
        "不如",
        "没有",
    )
    for line in lines:
        if any(k in line for k in keywords):
            useful.append(clean_line(line))
    if not useful:
        useful = [clean_line(x) for x in lines[-12:]]
    useful = dedupe(useful)[:18]
    if not useful:
        return "无重要可回收记忆"
    joined = "\n".join(f"- {x[:220]}" for x in useful if x)
    return (
        "- 本轮目标：从即将 idle 释放的 session 中回收关键上下文。\n"
        "- 已完成事项：已读取 session 聊天记录并提取高价值信息。\n"
        "- 重要决策：\n"
        f"{joined}\n"
        "- 用户偏好：保留明确表达的偏好、交付要求和配置要求。\n"
        "- 待办事项：后续新 session 可基于本摘要继续追问。\n"
        "- 风险和未完成上下文：本地规则摘要可能不如 LLM 摘要完整。"
    )


def clean_line(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"^(user|assistant|system|unknown)\s*:\s*", "", text, flags=re.I)
    return text


def dedupe(items: Iterable[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        key = item[:120]
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def build_memory_entry(session: Dict[str, Any], session_id: str, summary: str) -> str:
    ts = now_local().strftime("%Y-%m-%d %H:%M")
    typ = session_type_of(session)
    channel = get_first(session, ("channel", "channelId", "provider")) or "unknown"
    agent_id = session_agent_id(session)
    return (
        f"\n## {ts} 会话摘要\n\n"
        f"来源：agent={agent_id} / {channel} / {typ} / sessionId={session_id}\n\n"
        f"{summary.strip()}\n"
    )


def append_memory(entry: str, session: Optional[Dict[str, Any]] = None) -> Path:
    memory_dir = resolve_memory_dir(session)
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = memory_dir / f"{now_local().strftime('%Y-%m-%d')}.md"
    with path.open("a", encoding="utf-8") as f:
        f.write(entry)
        if not entry.endswith("\n"):
            f.write("\n")
    return path


def process_session(
    session: Dict[str, Any],
    state: Dict[str, Any],
    dry_run: bool = False,
    force: bool = False,
) -> Optional[str]:
    session_id = session_id_of(session)
    if not session_id:
        return None
    agent_id = session_agent_id(session)
    state_key = f"{agent_id}:{session_id}"
    flushed = state.setdefault("flushed_sessions", {})
    if state_key in flushed and not force:
        return f"skip {session_id}: already flushed for agent={agent_id}"

    ok, reason = should_flush(session, force=force)
    if not ok:
        return f"skip {session_id}: {reason}"

    transcript_path = find_transcript(session_id, session)
    if not transcript_path:
        return f"skip {session_id}: transcript jsonl not found"

    transcript = read_transcript_text(transcript_path)
    if not transcript.strip():
        return f"skip {session_id}: empty transcript"

    summary = call_llm_summary(transcript, session=session) or local_summary(transcript)
    if "无重要可回收记忆" in summary:
        return f"skip {session_id}: no important memory"

    entry = build_memory_entry(session, session_id, summary)
    if dry_run:
        return f"dry-run {session_id}: would write {len(entry)} chars from {transcript_path}"

    memory_path = append_memory(entry, session=session)
    flushed[state_key] = {
        "agent_id": agent_id,
        "session_id": session_id,
        "flushed_at": now_local().isoformat(),
        "memory_path": str(memory_path),
        "transcript_path": str(transcript_path),
        "reason": reason,
    }
    save_state(state)
    return f"flushed {session_id}: {memory_path}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="run one scan and exit")
    parser.add_argument("--dry-run", action="store_true", help="print actions without writing memory")
    parser.add_argument("--force-session", help="force flush one sessionId")
    args = parser.parse_args()

    state = load_state()
    try:
        sessions = run_openclaw_sessions()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    matched = 0
    for session in sessions:
        sid = session_id_of(session)
        force = bool(args.force_session and sid == args.force_session)
        if args.force_session and not force:
            continue
        result = process_session(session, state, dry_run=args.dry_run, force=force)
        if result:
            matched += 1
            print(result)

    if args.force_session and matched == 0:
        print(f"ERROR: session not found: {args.force_session}", file=sys.stderr)
        return 2
    if not args.once:
        print("This script is intended to be run by timer with --once.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
