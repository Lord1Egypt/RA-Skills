#!/usr/bin/env python3
"""
extract_usage_signals.py — 扫描 ZCode / Codex / Claude Code session 目录提取可归因使用信号

只读扫描以下数据源：
  - ZCode:  .zcode/cli/agents/sess_*/agent_*/ 目录，从 metadata.json 和 transcript.jsonl 提取
  - Codex:  .codex/sessions/2026/{month}/{day}/rollout-*.jsonl，从 response_item 提取
  - Claude: .claude/projects/{project_name}/*.jsonl，从 assistant/tool_use 事件提取

输出 JSON 用于 audit_skill_plugin_issues.py 的 usage_evidence 字段。

CLI:
    python extract_usage_signals.py --agents-dir <path> --json
    python extract_usage_signals.py --agents-dir <path> --since 30d --json
    python extract_usage_signals.py --agents-dir <path> --scan-clients all --summary
    python extract_usage_signals.py --agents-dir <path> --scan-clients zcode,codex --summary
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


def parse_since(since: str | None) -> datetime | None:
    """Parse --since flag like '30d', '7d', '24h'. Returns cutoff datetime or None."""
    if not since:
        return None
    m = re.match(r"^(\d+)([dh])$", since.strip())
    if not m:
        raise ValueError(f"Invalid --since value: {since}. Use format like '30d' or '24h'.")
    n, unit = int(m.group(1)), m.group(2)
    delta = timedelta(days=n) if unit == "d" else timedelta(hours=n)
    return datetime.now(timezone.utc) - delta


def safe_json_load(path: Path) -> dict | None:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def extract_mcp_server(tool_name: str) -> str | None:
    """mcp__firecrawl__firecrawl_search -> firecrawl. Returns None for non-MCP tools."""
    if not tool_name.startswith("mcp__"):
        return None
    parts = tool_name.split("__")
    if len(parts) >= 2:
        return parts[1]
    return None


def extract_skill_invocation(prompt_text: str) -> str | None:
    """Try to detect skill invocations from prompt text. Look for Skill tool patterns."""
    return None


def is_mcp_tool_name(name: str) -> bool:
    """Check if a tool name indicates an MCP call."""
    if not name:
        return False
    return name.startswith("mcp__") or name.startswith("mcp.")


def parse_timestamp_iso(ts_str: str | None) -> str | None:
    """Normalize an ISO timestamp string for comparison. Returns original string or None."""
    if not ts_str:
        return None
    return ts_str


# ---------------------------------------------------------------------------
# Python package call detection
# ---------------------------------------------------------------------------

_PYTHON_PKG_FROM_PATTERN = re.compile(r'from\s+([\w.]+)\s+import')
_PYTHON_PKG_IMPORT_PATTERN = re.compile(r'^import\s+([\w.]+)', re.MULTILINE)
_PYTHON_PKG_BASH_PATTERN = re.compile(
    r"""python\s+-c\s+["'][^"']*?(?:from|import)\s+([\w.]+)""",
    re.IGNORECASE,
)

# Standard library modules to exclude from package call tracking (noise reduction)
_STDLIB_PACKAGES = frozenset({
    "__future__", "abc", "argparse", "ast", "asyncio", "base64", "builtins",
    "collections", "contextlib", "copy", "csv", "ctypes", "dataclasses",
    "datetime", "decimal", "difflib", "enum", "functools", "glob", "gzip",
    "hashlib", "html", "http", "importlib", "inspect", "io", "itertools",
    "json", "logging", "math", "multiprocessing", "operator", "os", "pathlib",
    "pickle", "platform", "pprint", "queue", "random", "re", "secrets",
    "shlex", "shutil", "signal", "socket", "sqlite3", "ssl", "statistics",
    "string", "struct", "subprocess", "sys", "tarfile", "tempfile",
    "textwrap", "threading", "time", "traceback", "types", "typing",
    "unittest", "urllib", "uuid", "warnings", "weakref", "xml", "zipfile",
    "zoneinfo",
})


def _extract_pkg_name(dotted: str) -> str | None:
    """Extract the top-level package name from a dotted import path.

    'playwright.sync_api' -> 'playwright'
    'yt_dlp' -> 'yt_dlp'
    Returns None if empty or only stdlib.
    """
    pkg = dotted.strip().split(".")[0]
    if not pkg or pkg in _STDLIB_PACKAGES:
        return None
    return pkg


def extract_python_package_calls(transcript_path: Path) -> dict[str, int]:
    """Scan transcript.jsonl for Python package usage via Bash/Write/Edit tool calls.

    Detects:
      - Bash commands:  python -c "from X ..." / "import X"
      - Write/Edit of .py files:  from X import ... / import X

    Returns {package_name: call_count}.
    """
    pkg_counter: Counter = Counter()

    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("type") != "tool_call_scheduled":
                    continue
                payload = d.get("payload", {})
                tool_name = payload.get("toolName", "")
                if not tool_name:
                    continue

                inp = payload.get("input", {})

                # --- Bash: scan command field for python -c imports ---
                if tool_name == "Bash":
                    cmd = inp.get("command", "")
                    if not cmd:
                        continue

                    # Pattern: python -c "from X import Y" or python -c "import X"
                    for m in _PYTHON_PKG_BASH_PATTERN.finditer(cmd):
                        pkg = _extract_pkg_name(m.group(1))
                        if pkg:
                            pkg_counter[pkg] += 1

                    # Also catch inline python without -c wrapper in command text
                    for m in _PYTHON_PKG_FROM_PATTERN.finditer(cmd):
                        pkg = _extract_pkg_name(m.group(1))
                        if pkg:
                            pkg_counter[pkg] += 1

                    for m in _PYTHON_PKG_IMPORT_PATTERN.finditer(cmd):
                        pkg = _extract_pkg_name(m.group(1))
                        if pkg:
                            pkg_counter[pkg] += 1

                # --- Write / Edit for .py files: scan content for imports ---
                elif tool_name in ("Write", "Edit"):
                    file_path = inp.get("file_path", "")
                    if not file_path.lower().endswith(".py"):
                        continue

                    # Write -> content; Edit -> new_string
                    content = inp.get("content") or inp.get("new_string", "")
                    if not content:
                        continue

                    for m in _PYTHON_PKG_FROM_PATTERN.finditer(content):
                        pkg = _extract_pkg_name(m.group(1))
                        if pkg:
                            pkg_counter[pkg] += 1

                    for m in _PYTHON_PKG_IMPORT_PATTERN.finditer(content):
                        pkg = _extract_pkg_name(m.group(1))
                        if pkg:
                            pkg_counter[pkg] += 1
    except Exception:
        pass

    return dict(pkg_counter)


# ---------------------------------------------------------------------------
# Headroom proxy activity detection
# ---------------------------------------------------------------------------

def detect_headroom_proxy_activity(allow_external: bool = False) -> dict:
    """Detect if headroom proxy is active and collect performance stats.

    Tries:
      1. Check for headroom python process via `tasklist` (Windows) or `ps` (Unix)
      2. Run `headroom perf` to collect compression statistics

    Returns dict with 'detected', 'mode', 'stats', 'data_source', 'note'.
    Always returns; never raises.
    """
    result: dict = {
        "detected": False,
        "mode": None,
        "stats": None,
        "data_source": "unavailable",
        "note": None,
    }

    if not allow_external:
        result["note"] = "外部命令探测默认禁用（保持只读承诺）；传 --allow-external-commands 启用"
        return result

    try:
        import subprocess

        headroom_bin = None
        # 1. Check for headroom process
        process_found = False
        try:
            if sys.platform == "win32":
                proc = subprocess.run(
                    ["tasklist", "/FI", "IMAGENAME eq python.exe", "/V"],
                    capture_output=True, text=True, timeout=10,
                )
                if "headroom" in proc.stdout.lower():
                    process_found = True
            else:
                proc = subprocess.run(
                    ["ps", "aux"],
                    capture_output=True, text=True, timeout=10,
                )
                if "headroom" in proc.stdout.lower():
                    process_found = True
        except Exception:
            pass

        # 2. Find headroom binary
        which_result = subprocess.run(
            ["which", "headroom"] if sys.platform != "win32" else ["where", "headroom"],
            capture_output=True, text=True, timeout=10,
        )
        if which_result.returncode == 0:
            headroom_bin = which_result.stdout.strip().split("\n")[0].strip()
        # Fallback: common install locations
        if not headroom_bin:
            for candidate in [
                "/c/Python312/Scripts/headroom",
                "/usr/local/bin/headroom",
                os.path.expanduser("~/.local/bin/headroom"),
            ]:
                if os.path.exists(candidate):
                    headroom_bin = candidate
                    break

        # 3. Run headroom perf
        if headroom_bin:
            perf_result = subprocess.run(
                [headroom_bin, "perf"], capture_output=True, text=True, timeout=30,
            )
            if perf_result.returncode == 0:
                output = perf_result.stdout
                stats = _parse_headroom_perf(output)
                if stats:
                    result["detected"] = process_found or stats["tokens_saved"] > 0
                    result["mode"] = "proxy"
                    result["stats"] = stats
                    result["data_source"] = "observed (headroom perf command)"
                    result["note"] = (
                        "headroom 通过 proxy 拦截 LLM 请求做透明压缩，不通过 MCP tool 命名空间调用"
                    )

    except Exception:
        pass

    return result


def _parse_headroom_perf(output: str) -> dict | None:
    """Parse headroom perf command output into structured stats.

    Expected output format:
      Requests:     52
      Tokens:       2,601,493 -> 2,425,867 (12.0% reduction)
      Total saved:  313,284 tokens
    """
    try:
        stats = {}
        # Requests
        m = re.search(r"Requests:\s+(\d+)", output)
        if m:
            stats["requests"] = int(m.group(1))
        # Reduction percent
        m = re.search(r"\(([\d.]+)%\s+reduction\)", output)
        if m:
            stats["reduction_percent"] = float(m.group(1))
        # Tokens saved
        m = re.search(r"Total saved:\s+([\d,]+)\s+tokens?", output)
        if m:
            stats["tokens_saved"] = int(m.group(1).replace(",", ""))
        # Input tokens
        m = re.search(r"Tokens:\s+([\d,]+)\s*->", output)
        if m:
            stats["input_tokens"] = int(m.group(1).replace(",", ""))
        # Output tokens
        m = re.search(r"->\s+([\d,]+)\s*\(", output)
        if m:
            stats["output_tokens"] = int(m.group(1).replace(",", ""))

        # Estimate cost savings (rough: ~$2.5/M input tokens for Claude)
        if stats.get("tokens_saved"):
            stats["estimated_cost_saved_usd"] = round(
                stats["tokens_saved"] / 1_000_000 * 2.5, 2
            )

        if stats:
            return stats
    except Exception:
        pass
    return None


# ---------------------------------------------------------------------------
# ZCode parser
# ---------------------------------------------------------------------------

def parse_transcript_tools(transcript_path: Path) -> tuple[list[str], list[dict]]:
    """
    Parse transcript.jsonl, return (tool_names, mcp_calls).
    mcp_calls is list of {"tool": str, "ts": str|None}.
    """
    tool_names: list[str] = []
    mcp_calls: list[dict] = []
    skill_invocations: list[str] = []

    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue
                if d.get("type") != "tool_call_scheduled":
                    continue
                payload = d.get("payload", {})
                tool_name = payload.get("toolName", "")
                if not tool_name:
                    continue
                ts = d.get("ts") or d.get("timestamp")
                tool_names.append(tool_name)
                if tool_name.startswith("mcp__"):
                    mcp_calls.append({"tool": tool_name, "ts": ts})
                # Skill invocations appear via Skill tool
                if tool_name == "Skill":
                    skill_arg = payload.get("input", {}).get("skill", "")
                    if skill_arg:
                        skill_invocations.append(skill_arg)
    except Exception:
        pass

    return tool_names, mcp_calls, skill_invocations


def scan_agent_dir(agent_dir: Path, since_cutoff: datetime | None, client_name: str = "zcode") -> dict | None:
    """Scan a single agent_*/ directory. Returns None if filtered out or unparseable."""
    meta = safe_json_load(agent_dir / "metadata.json")
    if not meta:
        return None

    # Time filter
    created_at_str = meta.get("createdAt")
    if since_cutoff and created_at_str:
        try:
            created = datetime.fromisoformat(created_at_str.replace("Z", "+00:00"))
            if created < since_cutoff:
                return None
        except Exception:
            pass

    profile_id = meta.get("profileId") or meta.get("profileSnapshot", {}).get("name", "unknown")
    profile_snapshot = meta.get("profileSnapshot", {})

    # Aggregate tools from transcript
    transcript_path = agent_dir / "transcript.jsonl"
    tool_counter: Counter = Counter()
    mcp_calls: list[dict] = []
    skill_invocations: list[str] = []
    python_package_calls: dict[str, int] = {}

    if transcript_path.exists():
        tools, mcp_calls, skill_invocations = parse_transcript_tools(transcript_path)
        tool_counter = Counter(tools)
        python_package_calls = extract_python_package_calls(transcript_path)

    return {
        "agent_id": agent_dir.name,
        "session_id": meta.get("parentSessionId"),
        "profile_id": profile_id,
        "profile_name": profile_snapshot.get("name", profile_id),
        "profile_description": profile_snapshot.get("description", ""),
        "profile_tools": profile_snapshot.get("tools", []),
        "profile_model": profile_snapshot.get("model"),
        "status": meta.get("status"),
        "total_tool_use_count": meta.get("totalToolUseCount"),
        "total_tokens": meta.get("totalTokens"),
        "input_tokens": meta.get("usage", {}).get("inputTokens"),
        "output_tokens": meta.get("usage", {}).get("outputTokens"),
        "cache_read_tokens": meta.get("usage", {}).get("cacheReadTokens"),
        "total_duration_ms": meta.get("totalDurationMs"),
        "created_at": created_at_str,
        "completed_at": meta.get("completedAt"),
        "tool_distribution": dict(tool_counter),
        "mcp_calls": mcp_calls,
        "skill_invocations": skill_invocations,
        "python_package_calls": python_package_calls,
    }


def scan_zcode_agents(agents_dir: Path, since_cutoff: datetime | None) -> dict:
    """
    Scan .zcode/cli/agents/ directory.
    Returns dict with 'agent_records', 'sessions_scanned', 'status'.
    """
    agent_records: list[dict] = []
    session_count = 0

    if not agents_dir.exists() or not agents_dir.is_dir():
        return {
            "agent_records": [],
            "sessions_scanned": 0,
            "status": "unavailable",
            "reason": f"Path does not exist: {agents_dir}",
        }

    for session_dir in sorted(agents_dir.iterdir()):
        if not session_dir.is_dir() or not session_dir.name.startswith("sess_"):
            continue
        session_count += 1
        for agent_dir in session_dir.iterdir():
            if not agent_dir.is_dir() or not agent_dir.name.startswith("agent_"):
                continue
            record = scan_agent_dir(agent_dir, since_cutoff)
            if record:
                agent_records.append(record)

    status = "observed" if agent_records else "no_data"
    return {
        "agent_records": agent_records,
        "sessions_scanned": session_count,
        "status": status,
    }


# ---------------------------------------------------------------------------
# Codex parser
# ---------------------------------------------------------------------------

def scan_codex_sessions(codex_dir: Path, since_cutoff: datetime | None) -> dict:
    """
    Scan .codex/sessions/ directory.
    Structure: {year}/{month}/{day}/rollout-<timestamp>-<uuid>.jsonl

    Event format (response_item with payload.type='custom_tool_call'):
      {"timestamp":"...", "type":"response_item",
       "payload":{"type":"custom_tool_call","name":"<tool_name>", ...}}

    Returns dict with 'agent_records', 'sessions_scanned', 'status'.
    Each record is a synthetic dict compatible with aggregate_signals().
    """
    agent_records: list[dict] = []
    session_files_scanned = 0

    if not codex_dir.exists() or not codex_dir.is_dir():
        return {
            "agent_records": [],
            "sessions_scanned": 0,
            "status": "unavailable",
            "reason": f"Path does not exist: {codex_dir}",
        }

    # Walk year/month/day structure
    for year_dir in sorted(codex_dir.iterdir()):
        if not year_dir.is_dir():
            continue
        for month_dir in sorted(year_dir.iterdir()):
            if not month_dir.is_dir():
                continue
            for day_dir in sorted(month_dir.iterdir()):
                if not day_dir.is_dir():
                    continue
                for fname in sorted(day_dir.iterdir()):
                    if not fname.is_file() or not fname.name.endswith(".jsonl"):
                        continue
                    session_files_scanned += 1
                    record = _parse_codex_session_file(fname, since_cutoff)
                    if record:
                        agent_records.append(record)

    status = "observed" if agent_records else "no_data"
    return {
        "agent_records": agent_records,
        "sessions_scanned": session_files_scanned,
        "status": status,
    }


def _parse_codex_session_file(filepath: Path, since_cutoff: datetime | None) -> dict | None:
    """
    Parse a single Codex session jsonl file.
    Returns a record dict or None (filtered by time / unparseable).
    """
    tool_names: list[str] = []
    mcp_calls: list[dict] = []
    min_ts: str | None = None
    python_package_counter: Counter = Counter()

    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue

                ts = d.get("timestamp") or d.get("ts")

                if since_cutoff:
                    try:
                        if not ts or datetime.fromisoformat(ts.replace("Z", "+00:00")) < since_cutoff:
                            continue
                    except (ValueError, TypeError):
                        continue

                # Track earliest timestamp for time filtering
                if ts and (min_ts is None or ts < min_ts):
                    min_ts = ts

                # Codex tool calls are in response_item with type custom_tool_call
                if d.get("type") != "response_item":
                    continue
                payload = d.get("payload", {})
                if payload.get("type") not in {"custom_tool_call", "function_call"}:
                    continue
                tool_name = payload.get("name", "")
                if not tool_name:
                    continue
                tool_names.append(tool_name)
                if is_mcp_tool_name(tool_name):
                    mcp_calls.append({"tool": tool_name, "ts": ts})

                # Extract Python package usage from Bash/Write/Edit tool inputs
                tool_input = payload.get("input", payload.get("arguments", {}))
                if isinstance(tool_input, str):
                    try:
                        tool_input = json.loads(tool_input)
                    except (ValueError, TypeError):
                        tool_input = {}
                if not isinstance(tool_input, dict):
                    tool_input = {}

                if tool_name == "Bash":
                    cmd = tool_input.get("command", "")
                    if cmd:
                        for m in _PYTHON_PKG_BASH_PATTERN.finditer(cmd):
                            pkg = _extract_pkg_name(m.group(1))
                            if pkg:
                                python_package_counter[pkg] += 1
                        for m in _PYTHON_PKG_FROM_PATTERN.finditer(cmd):
                            pkg = _extract_pkg_name(m.group(1))
                            if pkg:
                                python_package_counter[pkg] += 1
                        for m in _PYTHON_PKG_IMPORT_PATTERN.finditer(cmd):
                            pkg = _extract_pkg_name(m.group(1))
                            if pkg:
                                python_package_counter[pkg] += 1

                elif tool_name in ("Write", "Edit"):
                    file_path = tool_input.get("file_path", "")
                    if file_path.lower().endswith(".py"):
                        content = tool_input.get("content") or tool_input.get("new_string", "")
                        if content:
                            for m in _PYTHON_PKG_FROM_PATTERN.finditer(content):
                                pkg = _extract_pkg_name(m.group(1))
                                if pkg:
                                    python_package_counter[pkg] += 1
                            for m in _PYTHON_PKG_IMPORT_PATTERN.finditer(content):
                                pkg = _extract_pkg_name(m.group(1))
                                if pkg:
                                    python_package_counter[pkg] += 1
    except Exception:
        return None

    if since_cutoff and min_ts is None:
        return None
    # Time filter using earliest timestamp retained inside the requested window.
    if since_cutoff and min_ts:
        try:
            created = datetime.fromisoformat(min_ts.replace("Z", "+00:00"))
            if created < since_cutoff:
                return None
        except Exception:
            pass

    # Extract session identifier from filename
    # rollout-2026-07-25T11-20-53-<uuid>.jsonl
    session_id = filepath.stem
    # Shorten to a readable id
    agent_id = f"codex_{session_id[-36:]}" if len(session_id) > 36 else f"codex_{session_id}"

    return {
        "agent_id": agent_id,
        "session_id": session_id,
        "profile_id": "codex",
        "profile_name": "Codex",
        "profile_description": "Codex CLI sessions",
        "profile_tools": [],
        "profile_model": None,
        "status": "completed",
        "total_tool_use_count": len(tool_names),
        "total_tokens": None,
        "input_tokens": None,
        "output_tokens": None,
        "cache_read_tokens": None,
        "total_duration_ms": None,
        "created_at": min_ts,
        "completed_at": None,
        "tool_distribution": dict(Counter(tool_names)),
        "mcp_calls": mcp_calls,
        "skill_invocations": [],
        "python_package_calls": dict(python_package_counter),
    }


# ---------------------------------------------------------------------------
# Claude Code parser
# ---------------------------------------------------------------------------

def scan_claude_projects(claude_dir: Path, since_cutoff: datetime | None) -> dict:
    """
    Scan .claude/projects/ directory.
    Structure: {project_name}/*.jsonl

    Event format (assistant type with tool_use content):
      {"type":"assistant", "message":{"content":[{"type":"tool_use","name":"<tool_name>",...}]}}

    Returns dict with 'agent_records', 'sessions_scanned', 'status'.
    """
    agent_records: list[dict] = []
    session_files_scanned = 0

    if not claude_dir.exists() or not claude_dir.is_dir():
        return {
            "agent_records": [],
            "sessions_scanned": 0,
            "status": "unavailable",
            "reason": f"Path does not exist: {claude_dir}",
        }

    for proj_dir in sorted(claude_dir.iterdir()):
        if not proj_dir.is_dir():
            continue
        for fname in sorted(proj_dir.iterdir()):
            if not fname.is_file() or not fname.name.endswith(".jsonl"):
                continue
            # Skip files in memory/ directories
            if "memory" in proj_dir.name.lower() or "memory" in str(fname.relative_to(claude_dir)).lower():
                continue
            session_files_scanned += 1
            record = _parse_claude_session_file(fname, since_cutoff)
            if record:
                agent_records.append(record)

    status = "observed" if agent_records else "no_data"
    return {
        "agent_records": agent_records,
        "sessions_scanned": session_files_scanned,
        "status": status,
    }


def _parse_claude_session_file(filepath: Path, since_cutoff: datetime | None) -> dict | None:
    """
    Parse a single Claude Code session jsonl file.
    Returns a record dict or None (filtered by time / unparseable).
    """
    tool_names: list[str] = []
    mcp_calls: list[dict] = []
    min_ts: str | None = None
    session_id: str | None = None
    python_package_counter: Counter = Counter()

    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except Exception:
                    continue

                # Capture sessionId from any event
                sid = d.get("sessionId")
                if sid:
                    session_id = sid

                ts = d.get("timestamp") or d.get("ts")
                if ts and (min_ts is None or ts < min_ts):
                    min_ts = ts

                # Claude Code tool_use events are in 'assistant' type messages
                if d.get("type") not in ("assistant",):
                    continue
                msg = d.get("message", {})
                content = msg.get("content", [])
                if not isinstance(content, list):
                    continue
                for c in content:
                    if not isinstance(c, dict):
                        continue
                    if c.get("type") != "tool_use":
                        continue
                    tool_name = c.get("name", "")
                    if not tool_name:
                        continue
                    tool_names.append(tool_name)
                    if is_mcp_tool_name(tool_name):
                        mcp_calls.append({"tool": tool_name, "ts": ts})

                    # Extract Python package usage from Bash/Write/Edit tool inputs
                    tool_input = c.get("input", {})

                    if tool_name == "Bash":
                        cmd = tool_input.get("command", "")
                        if cmd:
                            for m in _PYTHON_PKG_BASH_PATTERN.finditer(cmd):
                                pkg = _extract_pkg_name(m.group(1))
                                if pkg:
                                    python_package_counter[pkg] += 1
                            for m in _PYTHON_PKG_FROM_PATTERN.finditer(cmd):
                                pkg = _extract_pkg_name(m.group(1))
                                if pkg:
                                    python_package_counter[pkg] += 1
                            for m in _PYTHON_PKG_IMPORT_PATTERN.finditer(cmd):
                                pkg = _extract_pkg_name(m.group(1))
                                if pkg:
                                    python_package_counter[pkg] += 1

                    elif tool_name in ("Write", "Edit"):
                        file_path = tool_input.get("file_path", "")
                        if file_path.lower().endswith(".py"):
                            content = tool_input.get("content") or tool_input.get("new_string", "")
                            if content:
                                for m in _PYTHON_PKG_FROM_PATTERN.finditer(content):
                                    pkg = _extract_pkg_name(m.group(1))
                                    if pkg:
                                        python_package_counter[pkg] += 1
                                for m in _PYTHON_PKG_IMPORT_PATTERN.finditer(content):
                                    pkg = _extract_pkg_name(m.group(1))
                                    if pkg:
                                        python_package_counter[pkg] += 1
    except Exception:
        return None

    # Time filter
    if since_cutoff and min_ts:
        try:
            created = datetime.fromisoformat(min_ts.replace("Z", "+00:00"))
            if created < since_cutoff:
                return None
        except Exception:
            pass

    # Identify project name from path
    # Path: .../projects/{project_name}/{uuid}.jsonl
    project_name = "unknown"
    try:
        parent = filepath.parent
        if parent.name and parent.name != "projects":
            project_name = parent.name
    except Exception:
        pass

    agent_id = f"claude_{filepath.stem[:36]}"

    return {
        "agent_id": agent_id,
        "session_id": session_id or filepath.stem,
        "profile_id": f"claude:{project_name}",
        "profile_name": f"Claude Code ({project_name})",
        "profile_description": f"Claude Code sessions in project {project_name}",
        "profile_tools": [],
        "profile_model": None,
        "status": "completed",
        "total_tool_use_count": len(tool_names),
        "total_tokens": None,
        "input_tokens": None,
        "output_tokens": None,
        "cache_read_tokens": None,
        "total_duration_ms": None,
        "created_at": min_ts,
        "completed_at": None,
        "tool_distribution": dict(Counter(tool_names)),
        "mcp_calls": mcp_calls,
        "skill_invocations": [],
        "python_package_calls": dict(python_package_counter),
    }


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate_signals(
    agent_records: list[dict],
    clients_scanned: list[str] | None = None,
    client_results: dict | None = None,
) -> dict:
    """Aggregate per-agent records into summary signals.

    Args:
        agent_records: Combined list of records from all scanned clients.
        clients_scanned: List of client names that were requested to scan.
        client_results: Dict mapping client name -> scan result dict (with status, agents_scanned, etc.)
    """
    if clients_scanned is None:
        clients_scanned = ["zcode"]

    # 1. Agent dispatch stats (by profile_id)
    profile_groups: dict[str, list[dict]] = defaultdict(list)
    for rec in agent_records:
        profile_groups[rec["profile_id"]].append(rec)

    agent_dispatch_stats = []
    for profile_id, recs in profile_groups.items():
        durations = [r["total_duration_ms"] or 0 for r in recs if r["total_duration_ms"]]
        tokens = [r["total_tokens"] or 0 for r in recs if r["total_tokens"]]
        last_dispatch = max(
            (r["created_at"] for r in recs if r["created_at"]), default=None
        )
        merged_tools: Counter = Counter()
        for r in recs:
            merged_tools.update(r["tool_distribution"])
        agent_dispatch_stats.append(
            {
                "profile_id": profile_id,
                "profile_name": recs[0]["profile_name"],
                "dispatch_count": len(recs),
                "avg_duration_ms": sum(durations) // len(durations) if durations else 0,
                "avg_tokens": sum(tokens) // len(tokens) if tokens else 0,
                "last_dispatch": last_dispatch,
                "top_tools": dict(merged_tools.most_common(10)),
            }
        )
    agent_dispatch_stats.sort(key=lambda x: x["dispatch_count"], reverse=True)

    # 2. Tool call distribution (all agents combined)
    tool_totals: Counter = Counter()
    for rec in agent_records:
        tool_totals.update(rec["tool_distribution"])

    # 3. MCP usage evidence
    mcp_by_server: dict[str, dict] = defaultdict(
        lambda: {"tool_calls": 0, "last_used": None, "tools_used": Counter(), "observed_in_clients": set()}
    )
    for rec in agent_records:
        for call in rec["mcp_calls"]:
            server = extract_mcp_server(call["tool"])
            if not server:
                continue
            mcp_by_server[server]["tool_calls"] += 1
            mcp_by_server[server]["observed_in_clients"].add(_infer_client_name(rec))
            mcp_by_server[server]["tools_used"][call["tool"]] += 1
            ts = call.get("ts")
            if ts:
                if not mcp_by_server[server]["last_used"] or ts > mcp_by_server[server]["last_used"]:
                    mcp_by_server[server]["last_used"] = ts

    mcp_usage_evidence = []
    for server, info in sorted(mcp_by_server.items(), key=lambda x: x[1]["tool_calls"], reverse=True):
        evidence = {
            "mcp_server": server,
            "tool_calls": info["tool_calls"],
            "last_used": info["last_used"],
            "tools_used": dict(info["tools_used"]),
            "observed_in_clients": sorted(info["observed_in_clients"]),
            "status": "observed",
        }
        mcp_usage_evidence.append(evidence)

    # 4. Skill invocation evidence
    skill_counter: Counter = Counter()
    for rec in agent_records:
        for s in rec["skill_invocations"]:
            skill_counter[s] += 1
    skill_invocation_evidence = [
        {"skill_id": s, "invocations": c} for s, c in skill_counter.most_common()
    ]

    # 5. Python package usage (new in v9.1.0)
    pkg_by_name: dict[str, dict] = defaultdict(
        lambda: {"call_count": 0, "observed_in_clients": set(), "timestamps": []}
    )
    for rec in agent_records:
        client_name = _infer_client_name(rec)
        for pkg, count in rec.get("python_package_calls", {}).items():
            info = pkg_by_name[pkg]
            info["call_count"] += count
            info["observed_in_clients"].add(client_name)
            if rec.get("created_at"):
                info["timestamps"].append(rec["created_at"])

    python_package_usage = []
    for pkg, info in sorted(pkg_by_name.items(), key=lambda x: x[1]["call_count"], reverse=True):
        timestamps = sorted(t for t in info["timestamps"] if t)
        entry = {
            "package": pkg,
            "call_count": info["call_count"],
            "observed_in_clients": sorted(info["observed_in_clients"]),
            "first_seen": timestamps[0] if timestamps else None,
            "last_seen": timestamps[-1] if timestamps else None,
        }
        python_package_usage.append(entry)

    # 6. Time range
    all_times = [r["created_at"] for r in agent_records if r["created_at"]]
    time_range = [min(all_times), max(all_times)] if all_times else None

    # 7. Client scan summary
    if client_results is None:
        client_results = {}

    scan_summary = {
        "agents_scanned": len(agent_records),
        "time_range": time_range,
        "clients_scanned": clients_scanned,
        "client_status": {name: client_results.get(name, {}).get("status", "unavailable") for name in clients_scanned},
        "coverage_complete": False,
        "coverage_note": "显式工具事件抽样；嵌套 exec、隐式 Skill 与日志缺失可能漏计，零记录不是零使用。",
        "sessions_scanned": 0,
        "transcripts_parsed": 0,
    }

    # Add per-client counts
    for client_name in clients_scanned:
        cr = client_results.get(client_name, {})
        count_key = f"{client_name}_sessions" if client_name != "zcode" else "zcode_agents"
        if client_name == "zcode":
            scan_summary[count_key] = cr.get("agents_scanned", 0)
            scan_summary["sessions_scanned"] = cr.get("sessions_scanned", 0)
            scan_summary["transcripts_parsed"] = sum(
                1 for r in agent_records if r["tool_distribution"]
            )
        else:
            scan_summary[count_key] = cr.get("sessions_scanned", 0)

    return {
        "scan_summary": scan_summary,
        "agent_dispatch_stats": agent_dispatch_stats,
        "tool_call_distribution": dict(tool_totals.most_common()),
        "mcp_usage_evidence": mcp_usage_evidence,
        "skill_invocation_evidence": skill_invocation_evidence,
        "python_package_usage": python_package_usage,
    }


def _infer_client_name(record: dict) -> str:
    """Guess which client an agent record comes from based on its profile_id/agent_id."""
    agent_id = record.get("agent_id", "")
    if agent_id.startswith("codex_"):
        return "codex"
    if agent_id.startswith("claude_"):
        return "claude"
    return "zcode"


def merge_with_mcp_config(signals: dict, mcp_config_path: Path | None, clients_scanned: list[str] | None = None) -> dict:
    """Cross-reference observed MCP servers with configured ones."""
    if clients_scanned is None:
        clients_scanned = ["zcode"]

    configured: set[str] = set()
    if mcp_config_path and mcp_config_path.exists():
        cfg = safe_json_load(mcp_config_path)
        if cfg and isinstance(cfg, dict):
            servers = cfg.get("mcp", {}).get("servers", {})
            if not servers:
                servers = cfg.get("mcpServers", {})
            configured = set(servers.keys())

    signals.setdefault("mcp_usage_evidence", [])
    observed = {m["mcp_server"] for m in signals["mcp_usage_evidence"] if m.get("status") == "observed"}
    never_observed = sorted(configured - observed)

    # Mark configured-but-never-seen MCP servers with clients info
    for server in never_observed:
        signals["mcp_usage_evidence"].append(
            {
                "mcp_server": server,
                "tool_calls": 0,
                "last_used": None,
                "tools_used": {},
                "status": "configured_never_observed",
                "never_observed_in_scanned_clients": clients_scanned,
            }
        )

    # Preserve actual event provenance; requested scan scope is not observed usage.
    for entry in signals["mcp_usage_evidence"]:
        if entry["status"] == "observed":
            entry.setdefault("observed_in_clients", [])

    # v9.1.0: Cross-reference MCP servers with Python package usage
    python_pkg_map = {
        p["package"]: p["call_count"]
        for p in signals.get("python_package_usage", [])
    }
    # Known MCP servers that have a corresponding pip package used via direct Python import
    MCP_TO_PYTHON_MAP = {
        "playwright": "playwright",
        # Add more mappings as they are discovered:
        # "codegraph": "codegraph",
        # headroom, firecrawl, github, rival-search, windows-mcp have no direct pip counterpart
    }

    for entry in signals["mcp_usage_evidence"]:
        server = entry["mcp_server"]

        # v9.1.0: Headroom proxy mode detection
        if server == "headroom":
            hr = signals.get("headroom_proxy_activity", {})
            if hr.get("detected"):
                stats = hr.get("stats", {})
                tok = stats.get("tokens_saved", 0)
                entry["working_mode"] = "proxy_active"
                entry["proxy_stats"] = stats
                # Override status to reflect proxy activity
                entry["status"] = "configured_never_observed" if entry["tool_calls"] == 0 else entry["status"]
                entry["status_note"] = (
                    f"MCP 可归因调用 {entry['tool_calls']} 次；proxy 探测记录："
                    f"已处理 {stats.get('requests', '?')} 请求，"
                    f"压缩 {stats.get('reduction_percent', '?')}%，"
                    f"节省约 {tok:,} tokens"
                )
            else:
                entry["working_mode"] = "proxy_unconfirmed"
                entry["status_note"] = "proxy 运行状态未验证；未探测或探测不可用不能证明服务未运行。"

        # v9.1.0: Cross-reference MCP servers with Python package usage
        py_pkg = MCP_TO_PYTHON_MAP.get(server)
        if py_pkg:
            py_count = python_pkg_map.get(py_pkg, 0)
            note = None
            if py_count > 0 and entry["tool_calls"] == 0:
                note = f"本次记录未检出 MCP 调用，同名 Python 包可归因调用 {py_count} 次（独立通道，覆盖不完整）"
            elif py_count > 0:
                note = f"MCP tool 被调用 {entry['tool_calls']} 次，同名 Python 包被调用 {py_count} 次（独立通道）"
            entry["related_python_package"] = {
                "name": py_pkg,
                "call_count": py_count,
                "note": note,
            }

    signals["mcp_config_crossref"] = {
        "configured_count": len(configured),
        "configured_servers": sorted(configured),
        "observed_count": len(observed),
        "never_observed_count": len(never_observed),
        "never_observed_servers": never_observed,
        "clients_scanned_count": len(clients_scanned),
        "clients_scanned": clients_scanned,
    }
    return signals


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser(
        description="Scan ZCode / Codex / Claude session directories for attributable usage signals."
    )
    parser.add_argument(
        "--agents-dir",
        required=True,
        help="Path to .zcode/cli/agents/ directory.",
    )
    parser.add_argument(
        "--mcp-config",
        default=None,
        help="Path to ZCode config.json for MCP cross-reference.",
    )
    parser.add_argument(
        "--since",
        default=None,
        help="Time window: '30d' or '24h'. Omit for full history.",
    )
    parser.add_argument("--json", action="store_true", help="Output JSON.")
    parser.add_argument("--summary", action="store_true", help="Human-readable summary.")
    parser.add_argument(
        "--allow-external-commands",
        action="store_true",
        help="允许执行 tasklist/ps/headroom 等外部命令探测（默认关闭，保持只读承诺）",
    )
    parser.add_argument(
        "--scan-clients",
        default="zcode",
        help="Comma-separated list of clients to scan: zcode, codex, claude, or all. (default: zcode)",
    )
    parser.add_argument(
        "--codex-dir",
        default=os.path.expanduser("~/.codex/sessions"),
        help="Path to Codex sessions directory. (default: ~/.codex/sessions)",
    )
    parser.add_argument(
        "--claude-dir",
        default=os.path.expanduser("~/.claude/projects"),
        help="Path to Claude Code projects directory. (default: ~/.claude/projects)",
    )
    args = parser.parse_args()

    # Parse --scan-clients
    raw_clients = args.scan_clients.strip().lower()
    if raw_clients == "all":
        clients_to_scan = ["zcode", "codex", "claude"]
    else:
        clients_to_scan = [c.strip() for c in raw_clients.split(",") if c.strip()]

    since_cutoff = None
    if args.since:
        try:
            since_cutoff = parse_since(args.since)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2

    # -----------------------------------------------------------------------
    # Scan each requested client
    # -----------------------------------------------------------------------
    all_records: list[dict] = []
    client_results: dict[str, dict] = {}

    # 1. ZCode
    if "zcode" in clients_to_scan:
        agents_dir = Path(args.agents_dir)
        zcode_result = scan_zcode_agents(agents_dir, since_cutoff)
        zcode_result["agents_scanned"] = len(zcode_result["agent_records"])
        all_records.extend(zcode_result["agent_records"])
        client_results["zcode"] = zcode_result
    else:
        client_results["zcode"] = {"status": "skipped", "sessions_scanned": 0, "agents_scanned": 0}

    # 2. Codex
    if "codex" in clients_to_scan:
        codex_dir = Path(args.codex_dir)
        codex_result = scan_codex_sessions(codex_dir, since_cutoff)
        codex_result["agents_scanned"] = len(codex_result["agent_records"])
        all_records.extend(codex_result["agent_records"])
        client_results["codex"] = codex_result
    else:
        client_results["codex"] = {"status": "skipped", "sessions_scanned": 0, "agents_scanned": 0}

    # 3. Claude
    if "claude" in clients_to_scan:
        claude_dir = Path(args.claude_dir)
        claude_result = scan_claude_projects(claude_dir, since_cutoff)
        claude_result["agents_scanned"] = len(claude_result["agent_records"])
        all_records.extend(claude_result["agent_records"])
        client_results["claude"] = claude_result
    else:
        client_results["claude"] = {"status": "skipped", "sessions_scanned": 0, "agents_scanned": 0}

    # -----------------------------------------------------------------------
    # Aggregate
    # -----------------------------------------------------------------------
    signals = aggregate_signals(all_records, clients_scanned=clients_to_scan, client_results=client_results)

    # v9.1.0: Detect headroom proxy activity (live check, not transcript-based)
    headroom_proxy = detect_headroom_proxy_activity(args.allow_external_commands)
    signals["headroom_proxy_activity"] = headroom_proxy

    # Cross-reference with MCP config
    mcp_config_path = Path(args.mcp_config) if args.mcp_config else None
    signals = merge_with_mcp_config(signals, mcp_config_path, clients_scanned=clients_to_scan)

    # -----------------------------------------------------------------------
    # Output
    # -----------------------------------------------------------------------
    if args.json:
        print(json.dumps(signals, ensure_ascii=False, indent=2))
    else:
        # Human-readable summary
        print(f"=== Usage Signals Scan ===")
        print(f"Clients scanned: {', '.join(clients_to_scan)}")
        print()

        for client_name in clients_to_scan:
            cr = client_results.get(client_name, {})
            status = cr.get("status", "unknown")
            print(f"--- {client_name} ---")
            print(f"  Status:    {status}")
            if cr.get("reason"):
                print(f"  Reason:    {cr['reason']}")
            if client_name == "zcode":
                print(f"  Sessions:  {cr.get('sessions_scanned', 0)}")
                print(f"  Agents:    {cr.get('agents_scanned', 0)}")
            else:
                print(f"  Sessions:  {cr.get('sessions_scanned', 0)}")
                print(f"  Records:   {cr.get('agents_scanned', 0)}")
            print()

        if 'zcode' in clients_to_scan:
            print(f"ZCode sessions: {signals['scan_summary']['sessions_scanned']}")
        print(f"Total records: {signals['scan_summary']['agents_scanned']}")
        print(f"Time range: {signals['scan_summary']['time_range']}")
        print()

        print("--- Agent dispatch ---")
        for stat in signals["agent_dispatch_stats"]:
            print(f"  {stat['profile_id']:30s} {stat['dispatch_count']:4d}x  avg {stat['avg_duration_ms']}ms  {stat['avg_tokens']}tok")
        print()

        print("--- Top tools ---")
        for tool, cnt in list(signals["tool_call_distribution"].items())[:15]:
            print(f"  {tool:40s} {cnt}")
        print()

        print("--- MCP evidence ---")
        for m in signals["mcp_usage_evidence"]:
            extra = ""
            if m.get("observed_in_clients"):
                extra = f"  clients={m['observed_in_clients']}"
            if m.get("never_observed_in_scanned_clients"):
                extra = f"  never_in={m['never_observed_in_scanned_clients']}"
            # Show related_python_package cross-reference if available
            rpp = m.get("related_python_package")
            if rpp:
                note = rpp.get("note") or f"Python包调用 {rpp['call_count']}次"
                extra += f"  [py:{rpp['name']}={rpp['call_count']} {note}]"
            # Show headroom proxy mode info
            wm = m.get("working_mode")
            if wm:
                extra += f"  [mode={wm}]"
            sn = m.get("status_note")
            if sn:
                extra += f"  note={sn[:80]}"
            print(f"  {m['mcp_server']:20s} calls={m['tool_calls']:4d}  status={m['status']}{extra}")
        print()

        print("--- Python package usage ---")
        ppu = signals.get("python_package_usage", [])
        if ppu:
            for p in ppu[:10]:
                clients = ",".join(p["observed_in_clients"])
                print(f"  {p['package']:25s} calls={p['call_count']:4d}  clients=[{clients}]  last={p.get('last_seen','?')[:19]}")
            if len(ppu) > 10:
                print(f"  ... ({len(ppu) - 10} more packages)")
        else:
            print("  (none detected)")
        print()

        print(f"--- MCP config crossref ---")
        xref = signals.get("mcp_config_crossref", {})
        print(f"  Configured: {xref.get('configured_count', 0)}, Observed: {xref.get('observed_count', 0)}, Never seen: {xref.get('never_observed_count', 0)}")
        print(f"  Clients scanned: {xref.get('clients_scanned', [])}")
        if xref.get("never_observed_servers"):
            print(f"  Never observed: {', '.join(xref['never_observed_servers'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
