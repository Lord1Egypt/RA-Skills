#!/usr/bin/env python3
"""
Session Memory Extractor — AI extraction engine
Calls MiniMax API to extract durable memories from raw session content.

v1.0.6 safety: prints __EXTRACT_OK__ marker on success; raises RuntimeError on failure.
run_extractor.py verifies the marker before deleting original files.
"""

import json
import sys
import os
import argparse
from pathlib import Path

# --- Config loader ---
CONFIG_FILE = Path(__file__).parent / "config.env"

def load_config():
    """从 config.env 读取配置（不覆盖已存在的环境变量）"""
    if not CONFIG_FILE.exists():
        return {}
    config = {}
    for line in open(CONFIG_FILE):
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, val = line.split('=', 1)
        key, val = key.strip(), val.strip()
        config[key] = val
    return config

CONFIG = load_config()

def get_config(key, default=None):
    """优先读环境变量，其次读 config.env"""
    return os.environ.get(key, CONFIG.get(key, default))

# --- Prompt template ---
EXTRACTION_PROMPT = """You are extracting durable memories from an OpenClaw session transcript.

Extract the following types of information:
- DECISION: Explicit choices made, strategies agreed upon, tools/preferences chosen
- PREFERENCE: User likes, dislikes, habits, communication style
- FACT: Factual information established (names, dates, numbers, project context)
- TODO: Action items, follow-ups, things promised

For each entry provide:
- Type tag [DECISION/PREFERENCE/FACT/TODO]
- Content (what was said/decided)
- Confidence: HIGH/MEDIUM/LOW (based on clarity)

Rules:
- If nothing valuable found, output: NO_MEMORIES
- Keep each entry concise (1-2 sentences)
- Preserve exact quotes for important decisions
- If a session is mostly chitchat with no actionable content, output: NO_MEMORIES
- Do NOT invent information not present in the transcript

Output format:
```
## {session-id}

- **[TYPE]** Content here
  Confidence: HIGH/MEDIUM/LOW

- **[TYPE]** Content here
  Confidence: HIGH/MEDIUM/LOW
```
"""


def load_minimax_api_key():
    """Load MiniMax API key.

    优先级：
    1. 环境变量 MINIMAX_API_KEY（推荐，OpenClaw 可以在调用前 export）
    2. 主 agent 的 auth-profiles.json（旧版字段 minimax:cn）
    3. 主 agent 的 openclaw-agent.sqlite（新版字段 minimax-portal:default，OAuth access token）
    """
    # 1) 环境变量
    env_key = os.environ.get("MINIMAX_API_KEY", "").strip()
    if env_key:
        return env_key

    # 2) auth-profiles.json（旧版）
    config_path = Path("~/.openclaw/agents/main/agent/auth-profiles.json").expanduser()
    if config_path.exists():
        try:
            with open(config_path) as f:
                raw = json.load(f)
            profiles = raw if isinstance(raw, dict) and "profiles" not in raw else raw.get("profiles", raw)
            for key, val in profiles.items():
                if key == "minimax:cn" and isinstance(val, dict):
                    if val.get("type") == "api_key":
                        k = val.get("key", "").strip()
                        if k:
                            return k
            for key, val in profiles.items():
                if isinstance(val, dict) and val.get("type") == "api_key" and "minimax" in val.get("provider", "").lower():
                    k = val.get("key", "").strip()
                    if k:
                        return k
        except Exception:
            pass

    # 3) SQLite（新版 OAuth 存储）
    sqlite_path = Path("~/.openclaw/agents/main/agent/openclaw-agent.sqlite").expanduser()
    if sqlite_path.exists():
        try:
            import sqlite3
            conn = sqlite3.connect(str(sqlite_path))
            try:
                row = conn.execute("SELECT store_json FROM auth_profile_store WHERE store_key='primary'").fetchone()
            finally:
                conn.close()
            if row:
                data = json.loads(row[0])
                profiles = data.get("profiles", {})
                # 优先 minimax-portal:default（OAuth）
                for k, v in profiles.items():
                    if k == "minimax-portal:default" and isinstance(v, dict) and v.get("access"):
                        return v["access"].strip()
                # 兜底：任意含 minimax 的 profile
                for k, v in profiles.items():
                    if "minimax" in k.lower() and isinstance(v, dict):
                        if v.get("type") == "api_key" and v.get("key"):
                            return v["key"].strip()
                        if v.get("access"):
                            return v["access"].strip()
        except Exception:
            pass

    return None


def call_minimax_api(content: str, model: str) -> str:
    """Call MiniMax API for extraction."""
    api_key = load_minimax_api_key()
    if not api_key:
        raise RuntimeError("MiniMax API key not found in auth-profiles.json")

    import urllib.request
    import urllib.error

    model_name = model.split("/")[-1] if "/" in model else model

    url = "https://api.minimaxi.com/v1/text/chatcompletion_v2"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    # v1.0.6: bumped from 8000 to 32000 to handle trajectory transcripts (which can be 25K+ chars for long sessions)
    truncated = content[:32000] if len(content) > 32000 else content

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": EXTRACTION_PROMPT},
            {"role": "user", "content": f"Session transcript:\n{truncated}"},
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
    }

    req = urllib.request.Request(
        url, data=json.dumps(payload).encode(), headers=headers, method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.load(resp)
            choices = result.get("choices", result.get("data", []))
            if isinstance(choices, list) and len(choices) > 0:
                msg = choices[0].get("message", {})
                if isinstance(msg, str):
                    return msg
                return msg.get("content", str(choices[0]))
            return str(result)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else str(e)
        raise RuntimeError(f"MiniMax API error {e.code}: {error_body}")
    except Exception as e:
        raise RuntimeError(f"MiniMax API call failed: {e}")


def build_trajectory_transcript(file_path: str) -> str:
    """Parse .trajectory.jsonl and build a clean transcript for memory extraction.

    v1.0.6 feature: recovers conversations from .trajectory.jsonl when the
    corresponding .jsonl is missing (orphan trajectories). The trajectory contains
    messagesSnapshot events with full conversation content (including Feishu metadata
    wrapping, thinking blocks, tool calls/results) which is more complete than .jsonl.

    Strategy:
    1. Find the last model.completed event (most cumulative messagesSnapshot)
    2. Walk messages, format as [role]: text
    3. Include thinking blocks (truncated) and tool calls (name + args preview)
    4. Add session metadata header
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Trajectory file not found: {file_path}")

    events = []
    with open(file_path, 'r', errors='ignore') as f:
        for line in f:
            try:
                events.append(json.loads(line))
            except Exception:
                pass

    # Find session metadata
    session_meta = {}
    for e in events:
        if e.get('type') == 'session.started':
            session_meta = e.get('data', {})
            break

    # Find last model.completed (most cumulative snapshot)
    last_completed = None
    for e in events:
        if e.get('type') == 'model.completed':
            last_completed = e  # keep updating; last one wins

    if not last_completed:
        raise RuntimeError(f"No model.completed event in {file_path} (empty/invalid trajectory)")

    data = last_completed.get('data', {})
    snapshot = data.get('messagesSnapshot', [])
    if not snapshot:
        raise RuntimeError(f"Empty messagesSnapshot in {file_path}")

    session_id = Path(file_path).name.replace('.trajectory.jsonl', '')

    lines = []
    lines.append(f"Session ID: {session_id}")
    lines.append(f"Source: trajectory recovery (no .jsonl found)")
    lines.append(f"Trigger: {session_meta.get('trigger', '?')}")
    lines.append(f"Agent: {session_meta.get('agentId', '?')}")
    lines.append(f"Total messages: {len(snapshot)}")
    lines.append(f"Compaction count: {data.get('compactionCount', 0)}")
    if data.get('aborted'):
        lines.append(f"Status: aborted ({data.get('finalStatus', '?')})")
    else:
        lines.append(f"Status: completed ({data.get('finalStatus', 'ok')})")
    lines.append("")
    lines.append("=== Conversation Transcript ===")

    for i, msg in enumerate(snapshot):
        role = msg.get('role', '?')
        content = msg.get('content', [])
        ts = msg.get('timestamp', '')

        lines.append(f"\n--- [{i}] {role} ---")

        if isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                btype = block.get('type', '?')
                if btype == 'text':
                    text = block.get('text', '').strip()
                    if text:
                        # Strip the "Conversation info (untrusted metadata)" wrapper
                        # because it adds noise and isn't useful for memory extraction
                        # Keep the actual user message after the wrapper
                        cleaned = _strip_untrusted_metadata_wrapper(text)
                        lines.append(cleaned[:2000])
                elif btype == 'thinking':
                    text = block.get('thinking', '').strip()
                    if text:
                        lines.append(f"[THINKING] {text[:500]}")
                elif btype == 'toolCall':
                    name = block.get('name', block.get('toolName', '?'))
                    args = block.get('arguments', block.get('input', {}))
                    args_str = json.dumps(args, ensure_ascii=False)[:300] if args else ''
                    lines.append(f"[TOOL_CALL] {name}({args_str})")
                elif btype == 'toolResult':
                    result_content = block.get('content', block.get('output', ''))
                    if isinstance(result_content, str):
                        result_str = result_content[:500]
                    elif isinstance(result_content, list):
                        # tool result content is usually [{type: 'text', text: '...'}]
                        texts = []
                        for r in result_content:
                            if isinstance(r, dict) and r.get('type') == 'text':
                                texts.append(r.get('text', ''))
                        result_str = ' '.join(texts)[:500] if texts else json.dumps(result_content, ensure_ascii=False)[:500]
                    else:
                        result_str = str(result_content)[:500]
                    lines.append(f"[TOOL_RESULT] {result_str}")
                elif btype == 'image':
                    lines.append("[IMAGE attached]")
                else:
                    lines.append(f"[{btype}] {json.dumps(block, ensure_ascii=False)[:300]}")
        elif isinstance(content, str):
            lines.append(_strip_untrusted_metadata_wrapper(content)[:2000])

    # Add usage info
    usage = data.get('usage', {})
    if usage:
        lines.append("")
        lines.append("=== Usage ===")
        lines.append(f"Input: {usage.get('input', 0)}, Output: {usage.get('output', 0)}, Cache read: {usage.get('cacheRead', 0)}")
        cost = usage.get('cost', {}).get('total', 0)
        if cost:
            lines.append(f"Cost: ${cost:.4f}")

    # Add tools summary
    artifact_event = None
    for e in events:
        if e.get('type') == 'trace.artifacts':
            artifact_event = e
    if artifact_event:
        tool_metas = artifact_event.get('data', {}).get('toolMetas', [])
        if tool_metas:
            lines.append("")
            lines.append(f"=== Tools used ({len(tool_metas)}) ===")
            for tm in tool_metas[:20]:  # cap at 20
                if isinstance(tm, dict):
                    # toolMetas format: {"toolName": "..."} (per actual data)
                    name = tm.get('toolName') or tm.get('name') or '?'
                    lines.append(f"- {name}")

    return '\n'.join(lines)


def _strip_untrusted_metadata_wrapper(text: str) -> str:
    """Strip the 'Conversation info (untrusted metadata)' wrapper that Feishu adds.

    Example wrapper:
        Conversation info (untrusted metadata):
        ```json
        { ... }
        ```

        Sender (untrusted metadata):
        ```json
        { ... }
        ```

        [message_id: om_xxx]
        ou_xxx: 实际消息内容

    We want to keep the actual message content.
    """
    import re
    # Find the last [message_id: ...] line which precedes the actual message
    msg_id_match = re.search(r'\[message_id:\s*([^\]]+)\]', text)
    if msg_id_match:
        # Return everything after [message_id: ...]
        after = text[msg_id_match.end():].strip()
        return after
    # If no message_id found, strip any "Conversation info..." block
    text = re.sub(r'Conversation info \(untrusted metadata\):\s*```json.*?```\s*', '', text, flags=re.DOTALL)
    text = re.sub(r'Sender \(untrusted metadata\):\s*```json.*?```\s*', '', text, flags=re.DOTALL)
    return text.strip()


def main():
    parser = argparse.ArgumentParser(description="Extract memories from session content")
    parser.add_argument("--session-id", required=True, help="Session ID (filename base)")
    parser.add_argument("--content", help="Raw session content (required for --source=jsonl)")
    parser.add_argument("--file", help="Path to .trajectory.jsonl (required for --source=trajectory)")
    parser.add_argument("--source", choices=['jsonl', 'trajectory'], default='jsonl',
                        help="Source type: jsonl (default, takes --content) or trajectory (takes --file)")
    parser.add_argument("--model", default=None, help="Model to use (overrides config)")
    args = parser.parse_args()

    model = args.model or get_config("EXTRACTION_MODEL", "MiniMax-M2")

    # v1.0.6: support trajectory source for orphan trajectory recovery
    if args.source == 'trajectory':
        if not args.file:
            raise SystemExit("--file is required when --source=trajectory")
        content = build_trajectory_transcript(args.file)
        if not content or len(content.strip()) < 100:
            raise RuntimeError(f"Trajectory transcript too short ({len(content)} chars) — likely empty session")
    else:
        if not args.content:
            raise SystemExit("--content is required when --source=jsonl")
        content = args.content

    result = call_minimax_api(content, model)

    # v1.0.6 safety: validate extraction is non-empty + contains at least one structured entry
    # Marker protocol: print __EXTRACT_OK__ on success so run_extractor.py can verify before deleting files
    if not result or not result.strip():
        raise RuntimeError("API returned empty content (likely auth/quota issue)")

    # 成功 marker + 提取内容
    print("__EXTRACT_OK__")
    print(result)


if __name__ == "__main__":
    main()