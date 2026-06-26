#!/usr/bin/env python3
"""Parse AI coding tool conversation history files.

Supports:
  - Claude Code:  ~/.claude/projects/<path>/*.jsonl
  - Codex CLI:    ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl
  - OpenClaw:     ~/.openclaw/agents/<agentId>/sessions/*.jsonl
  - Gemini CLI:   ~/.gemini/tmp/<hash>/chats/*.json
"""

import json
import sys
import os
import glob
import platform
import re
from datetime import datetime, timezone
from pathlib import Path


ERROR_KEYWORDS = [
    "error", "Error", "ERROR", "failed", "Failed", "FAILED",
    "exception", "Exception", "traceback", "Traceback",
    "TypeError", "SyntaxError", "ReferenceError", "ModuleNotFoundError",
    "ImportError", "ValueError", "KeyError", "AttributeError",
    "RuntimeError", "FileNotFoundError", "PermissionError",
    "ENOENT", "EACCES", "segfault", "panic", "SIGABRT",
]


def _has_error(text: str) -> bool:
    return any(kw in text for kw in ERROR_KEYWORDS)


def _file_info(filepath: str) -> dict:
    stat = os.stat(filepath)
    return {
        "path": filepath,
        "modified": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
        "size_kb": round(stat.st_size / 1024, 1),
    }


def _parse_jsonl(filepath: str, max_lines: int = 0) -> list:
    """Parse JSONL file. If file > 10MB, only read last 5000 lines."""
    file_size = os.path.getsize(filepath)
    messages = []

    if file_size > 10 * 1024 * 1024:  # > 10MB
        # Read only the tail of large files
        import collections
        tail = collections.deque(maxlen=5000)
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    tail.append(line)
        for line in tail:
            try:
                messages.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    messages.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return messages


def _extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            p.get("text", "") for p in content
            if isinstance(p, dict) and p.get("type") == "text"
        )
    return ""


def _build_summary(tool, user_msgs, assistant_msgs, tool_uses, errors):
    return {
        "tool": tool,
        "total_user_msgs": len(user_msgs),
        "total_assistant_msgs": len(assistant_msgs),
        "total_tool_uses": len(tool_uses),
        "total_errors": len(errors),
        "user_messages": user_msgs[-20:],
        "assistant_messages": assistant_msgs[-10:],
        "tool_uses": tool_uses[-20:],
        "errors": errors,
    }


# --- Claude Code ---

def find_claude(project_dir: str) -> list:
    normalized = project_dir.replace("/", "-")
    if not normalized.startswith("-"):
        normalized = "-" + normalized
    claude_projects = os.path.expanduser("~/.claude/projects")
    conversations = []
    if os.path.isdir(claude_projects):
        for entry in os.listdir(claude_projects):
            entry_path = os.path.join(claude_projects, entry)
            if os.path.isdir(entry_path) and normalized in entry:
                for f in glob.glob(os.path.join(entry_path, "*.jsonl")):
                    info = _file_info(f)
                    info["tool"] = "claude_code"
                    info["project"] = entry
                    conversations.append(info)
    conversations.sort(key=lambda x: x["modified"], reverse=True)
    return conversations


def summarize_claude(filepath: str) -> dict:
    messages = _parse_jsonl(filepath)
    user_msgs, asst_msgs, tool_uses, errors = [], [], [], []
    for msg in messages:
        t = msg.get("type", "")
        ts = msg.get("timestamp", "")
        if t == "user":
            content = _extract_text(msg.get("message", {}).get("content", msg.get("content", "")))
            if content:
                user_msgs.append({"content": content[:500], "timestamp": ts})
        elif t == "assistant":
            content = _extract_text(msg.get("message", {}).get("content", ""))
            if content:
                asst_msgs.append({"content": content[:500], "timestamp": ts})
        elif t == "tool_use":
            tool_uses.append({
                "tool": msg.get("tool_name", "unknown"),
                "input_preview": str(msg.get("tool_input", ""))[:200],
                "timestamp": ts,
            })
        elif t == "tool_result":
            output = msg.get("tool_output", {})
            content = str(output.get("stderr", "") or output.get("stdout", output.get("output", "")) if isinstance(output, dict) else output)
            if _has_error(content):
                errors.append({"tool": msg.get("tool_name", "unknown"), "error": content[:500], "timestamp": ts})
    return _build_summary("claude_code", user_msgs, asst_msgs, tool_uses, errors)


# --- Codex CLI ---

def find_codex(project_dir: str = None) -> list:
    codex_sessions = os.path.expanduser("~/.codex/sessions")
    conversations = []
    if not os.path.isdir(codex_sessions):
        return conversations
    for f in glob.glob(os.path.join(codex_sessions, "**", "rollout-*.jsonl"), recursive=True):
        info = _file_info(f)
        info["tool"] = "codex_cli"
        info["project"] = os.path.dirname(f).replace(codex_sessions, "").strip("/")
        conversations.append(info)
    history = os.path.expanduser("~/.codex/history.jsonl")
    if os.path.isfile(history):
        info = _file_info(history)
        info["tool"] = "codex_cli"
        info["project"] = "global_history"
        conversations.append(info)
    conversations.sort(key=lambda x: x["modified"], reverse=True)
    return conversations


def summarize_codex(filepath: str) -> dict:
    messages = _parse_jsonl(filepath)
    user_msgs, asst_msgs, tool_uses, errors = [], [], [], []
    for msg in messages:
        role = msg.get("role", msg.get("type", ""))
        content = _extract_text(msg.get("content", ""))[:500]
        ts = msg.get("timestamp", msg.get("created_at", ""))
        if role in ("user", "human"):
            if content:
                user_msgs.append({"content": content, "timestamp": ts})
        elif role in ("assistant", "model"):
            if content:
                asst_msgs.append({"content": content, "timestamp": ts})
            for tc in (msg.get("tool_calls", msg.get("function_calls", [])) or []):
                tool_uses.append({
                    "tool": tc.get("function", {}).get("name", tc.get("name", "unknown")),
                    "input_preview": str(tc.get("function", {}).get("arguments", tc.get("input", "")))[:200],
                    "timestamp": ts,
                })
        elif role == "tool":
            if _has_error(content):
                errors.append({"tool": msg.get("name", "unknown"), "error": content[:500], "timestamp": ts})
    return _build_summary("codex_cli", user_msgs, asst_msgs, tool_uses, errors)


# --- OpenClaw ---

def find_openclaw(project_dir: str = None) -> list:
    openclaw_dir = os.path.expanduser("~/.openclaw/agents")
    conversations = []
    if not os.path.isdir(openclaw_dir):
        return conversations
    for agent_dir in os.listdir(openclaw_dir):
        sessions_dir = os.path.join(openclaw_dir, agent_dir, "sessions")
        if not os.path.isdir(sessions_dir):
            continue
        for f in glob.glob(os.path.join(sessions_dir, "*.jsonl")):
            info = _file_info(f)
            info["tool"] = "openclaw"
            info["project"] = agent_dir
            conversations.append(info)
    conversations.sort(key=lambda x: x["modified"], reverse=True)
    return conversations[:20]


def summarize_openclaw(filepath: str) -> dict:
    messages = _parse_jsonl(filepath)
    user_msgs, asst_msgs, tool_uses, errors = [], [], [], []
    for msg in messages:
        t = msg.get("type", "")
        ts = msg.get("timestamp", "")
        if t == "session":
            continue
        if t == "message":
            inner = msg.get("message", {})
            role = inner.get("role", "")
            content = _extract_text(inner.get("content", ""))[:500]
            if role == "user" and content:
                user_msgs.append({"content": content, "timestamp": ts})
            elif role == "assistant" and content:
                asst_msgs.append({"content": content, "timestamp": ts})
                if _has_error(content):
                    errors.append({"tool": "openclaw", "error": content[:500], "timestamp": ts})
            elif role == "toolResult" and content:
                if _has_error(content):
                    errors.append({"tool": "openclaw", "error": content[:500], "timestamp": ts})
            # Extract tool calls from assistant content blocks
            raw_content = inner.get("content", [])
            if isinstance(raw_content, list):
                for block in raw_content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        tool_uses.append({
                            "tool": block.get("name", "unknown"),
                            "input_preview": str(block.get("input", ""))[:200],
                            "timestamp": ts,
                        })
        else:
            # Fallback: try role-based parsing
            role = msg.get("role", "")
            content = _extract_text(msg.get("content", ""))[:500]
            if role == "user" and content:
                user_msgs.append({"content": content, "timestamp": ts})
            elif role == "assistant" and content:
                asst_msgs.append({"content": content, "timestamp": ts})
    return _build_summary("openclaw", user_msgs, asst_msgs, tool_uses, errors)


# --- Gemini CLI ---

def find_gemini(project_dir: str = None) -> list:
    gemini_tmp = os.path.expanduser("~/.gemini/tmp")
    conversations = []
    if not os.path.isdir(gemini_tmp):
        return conversations
    for hash_dir in os.listdir(gemini_tmp):
        chats_dir = os.path.join(gemini_tmp, hash_dir, "chats")
        if not os.path.isdir(chats_dir):
            continue
        for f in glob.glob(os.path.join(chats_dir, "*.json")):
            info = _file_info(f)
            info["tool"] = "gemini_cli"
            info["project"] = hash_dir[:12]
            conversations.append(info)
    conversations.sort(key=lambda x: x["modified"], reverse=True)
    return conversations[:20]


def summarize_gemini(filepath: str) -> dict:
    user_msgs, asst_msgs, tool_uses, errors = [], [], [], []
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return _build_summary("gemini_cli", [], [], [], [])

    messages = data if isinstance(data, list) else data.get("messages", data.get("history", []))
    if not isinstance(messages, list):
        return _build_summary("gemini_cli", [], [], [], [])

    for msg in messages:
        if not isinstance(msg, dict):
            continue
        role = msg.get("role", msg.get("author", ""))
        content = _extract_text(msg.get("content", msg.get("parts", msg.get("text", ""))))[:500]
        ts = msg.get("timestamp", msg.get("createTime", ""))

        if role in ("user", "human"):
            if content:
                user_msgs.append({"content": content, "timestamp": ts})
        elif role in ("model", "assistant"):
            if content:
                asst_msgs.append({"content": content, "timestamp": ts})
            if _has_error(content):
                errors.append({"tool": "gemini_cli", "error": content[:500], "timestamp": ts})
            # Tool calls
            for part in (msg.get("parts", []) if isinstance(msg.get("parts"), list) else []):
                if isinstance(part, dict) and part.get("functionCall"):
                    fc = part["functionCall"]
                    tool_uses.append({
                        "tool": fc.get("name", "unknown"),
                        "input_preview": str(fc.get("args", ""))[:200],
                        "timestamp": ts,
                    })

    return _build_summary("gemini_cli", user_msgs, asst_msgs, tool_uses, errors)


# --- Unified Interface ---

TOOL_FINDERS = {
    "claude_code": find_claude,
    "codex_cli": find_codex,
    "openclaw": find_openclaw,
    "gemini_cli": find_gemini,
}

TOOL_SUMMARIZERS = {
    "claude_code": summarize_claude,
    "codex_cli": summarize_codex,
    "openclaw": summarize_openclaw,
    "gemini_cli": summarize_gemini,
}


def detect_tools(project_dir: str) -> dict:
    found = {}
    for tool_name, finder in TOOL_FINDERS.items():
        try:
            convos = finder(project_dir)
            if convos:
                found[tool_name] = {
                    "count": len(convos),
                    "most_recent": convos[0]["modified"],
                    "conversations": convos[:5],
                }
        except Exception:
            continue
    return found


def auto_summary(filepath: str, tool: str = None) -> dict:
    if tool and tool in TOOL_SUMMARIZERS:
        return TOOL_SUMMARIZERS[tool](filepath)
    # Auto detect
    if ".codex" in filepath:
        return summarize_codex(filepath)
    elif ".openclaw" in filepath:
        return summarize_openclaw(filepath)
    elif ".gemini" in filepath:
        return summarize_gemini(filepath)
    else:
        return summarize_claude(filepath)


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_conversations.py <command> [args]")
        print()
        print("Commands:")
        print("  detect <project_dir>      Detect all AI tools with conversation history")
        print("  list <tool> [project_dir]  List conversations for a specific tool")
        print("  list-all [project_dir]     List conversations from all detected tools")
        print("  summary <file> [tool]      Summarize a conversation file")
        print()
        print("Supported tools: claude_code, codex_cli, openclaw, gemini_cli")
        sys.exit(1)

    command = sys.argv[1]

    if command == "detect":
        project_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
        result = detect_tools(project_dir)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif command == "list":
        if len(sys.argv) < 3:
            print("Usage: parse_conversations.py list <tool> [project_dir]")
            sys.exit(1)
        tool = sys.argv[2]
        project_dir = sys.argv[3] if len(sys.argv) > 3 else os.getcwd()
        if tool not in TOOL_FINDERS:
            print(f"Unknown tool: {tool}. Supported: {', '.join(TOOL_FINDERS.keys())}")
            sys.exit(1)
        convos = TOOL_FINDERS[tool](project_dir)
        print(json.dumps(convos, indent=2, ensure_ascii=False))

    elif command == "list-all":
        project_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
        all_convos = []
        for tool_name, finder in TOOL_FINDERS.items():
            try:
                all_convos.extend(finder(project_dir))
            except Exception:
                continue
        all_convos.sort(key=lambda x: x["modified"], reverse=True)
        # 只显示最近 30 个，带编号
        for i, c in enumerate(all_convos[:30]):
            size_str = f"{c['size_kb']:.0f}KB" if c['size_kb'] < 1024 else f"{c['size_kb']/1024:.1f}MB"
            mod = c['modified'][:16].replace('T', ' ')
            print(f"[{i+1:2d}] {c['tool']:12s} {mod} {size_str:>8s}  {os.path.basename(c['path'])}")
        # 同时输出 JSON 到 stderr 供程序读取
        print(json.dumps(all_convos[:30], ensure_ascii=False), file=sys.stderr)

    elif command == "summary":
        if len(sys.argv) < 3:
            print("Usage: parse_conversations.py summary <file> [tool]")
            sys.exit(1)
        filepath = sys.argv[2]
        tool = sys.argv[3] if len(sys.argv) > 3 else None
        result = auto_summary(filepath, tool)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
