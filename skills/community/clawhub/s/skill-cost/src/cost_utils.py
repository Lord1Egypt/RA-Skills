"""Shared utilities for skill-cost: JSONL parsing, skill attribution, model pricing."""

import sys
import io
import json
import re
from pathlib import Path
from datetime import datetime, timedelta, timezone

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

DEFAULT_AGENTS_DIR = Path.home() / ".openclaw" / "agents"
SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"

SKILL_PATH_RE = re.compile(
    r"[~/.]*/\.?openclaw/workspace/skills/([a-zA-Z0-9_-]+)/",
)

# Pricing per 1M tokens (USD), as of March 2026
MODEL_PRICING = {
    "claude-opus-4-6": {"input": 15.0, "output": 75.0, "cache_read": 1.50, "cache_write": 18.75},
    "claude-sonnet-4-5-20250929": {"input": 3.0, "output": 15.0, "cache_read": 0.30, "cache_write": 3.75},
    "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0, "cache_read": 0.30, "cache_write": 3.75},
    "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.0, "cache_read": 0.08, "cache_write": 1.0},
    "gpt-4o": {"input": 2.50, "output": 10.0, "cache_read": 1.25, "cache_write": 2.50},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60, "cache_read": 0.075, "cache_write": 0.15},
    "gpt-4.1": {"input": 2.0, "output": 8.0, "cache_read": 0.50, "cache_write": 2.0},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60, "cache_read": 0.10, "cache_write": 0.40},
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40, "cache_read": 0.025, "cache_write": 0.10},
    "o3": {"input": 2.0, "output": 8.0, "cache_read": 0.50, "cache_write": 2.0},
    "o3-mini": {"input": 1.10, "output": 4.40, "cache_read": 0.275, "cache_write": 1.10},
    "o4-mini": {"input": 1.10, "output": 4.40, "cache_read": 0.275, "cache_write": 1.10},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.0, "cache_read": 0.315, "cache_write": 1.25},
    "gemini-2.5-flash": {"input": 0.15, "output": 0.60, "cache_read": 0.0375, "cache_write": 0.15},
}

FALLBACK_PRICING = {"input": 3.0, "output": 15.0, "cache_read": 0.30, "cache_write": 3.75}

CATEGORY_BUILTIN = "(built-in)"
CATEGORY_CONVERSATION = "(conversation)"

_skill_tool_map: dict[str, str] | None = None


def discover_skill_tools() -> dict[str, str]:
    """Scan installed skills to build a tool_name -> skill_name mapping.

    Reads the `tools` field from each skill's SKILL.md frontmatter.
    """
    global _skill_tool_map
    if _skill_tool_map is not None:
        return _skill_tool_map

    _skill_tool_map = {}
    if not SKILLS_DIR.is_dir():
        return _skill_tool_map

    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        try:
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            fm = _parse_frontmatter(text)
            skill_name = fm.get("name", skill_dir.name)
            for tool in fm.get("tools", []):
                _skill_tool_map[tool] = skill_name
        except OSError:
            continue

    return _skill_tool_map


def _parse_frontmatter(text: str) -> dict:
    """Minimal YAML frontmatter parser — handles simple key: value and lists."""
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip()
    result: dict = {}
    current_key = None
    for line in block.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- ") and current_key is not None:
            val = stripped[2:].strip().strip("'\"")
            if isinstance(result.get(current_key), list):
                result[current_key].append(val)
            continue
        if ":" in stripped:
            key, _, val = stripped.partition(":")
            key = key.strip()
            val = val.strip().strip("'\"")
            if val == "" or val == ">":
                result[key] = []
                current_key = key
            else:
                result[key] = val
                current_key = key
    return result


def _extract_command_str(tc: dict) -> str:
    """Extract the command string from a toolCall, handling multiple field names and formats."""
    for field in ("arguments", "input", "params"):
        val = tc.get(field)
        if val is None:
            continue
        if isinstance(val, dict):
            return val.get("command", "") or val.get("cmd", "") or ""
        if isinstance(val, str):
            return val
    return ""


EXEC_TOOL_NAMES = {"bash", "shell", "terminal", "exec", "Bash", "Shell"}


def attribute_skill(tool_calls: list[dict]) -> dict[str, int]:
    """Given a list of toolCall objects, return {skill_name: call_count}.

    Attribution priority:
    1. Bash/exec command path matching (~/.openclaw/workspace/skills/<name>/)
    2. Tool name -> skill mapping from SKILL.md discovery
    3. Fallback to CATEGORY_BUILTIN
    """
    if not tool_calls:
        return {CATEGORY_CONVERSATION: 1}

    skill_map = discover_skill_tools()
    counts: dict[str, int] = {}

    for tc in tool_calls:
        name = tc.get("name", "")
        skill = None

        if name in EXEC_TOOL_NAMES:
            cmd = _extract_command_str(tc)
            match = SKILL_PATH_RE.search(cmd)
            if match:
                skill = match.group(1)

        if skill is None and name in skill_map:
            skill = skill_map[name]

        if skill is None:
            skill = CATEGORY_BUILTIN

        counts[skill] = counts.get(skill, 0) + 1

    return counts


def get_usage_tokens(usage: dict) -> tuple[int, int, int, int]:
    """Extract token counts from usage dict, handling both field naming conventions.

    Returns (input_tokens, output_tokens, cache_read_tokens, cache_write_tokens).
    """
    input_t = usage.get("inputTokens") or usage.get("input") or 0
    output_t = usage.get("outputTokens") or usage.get("output") or 0
    cache_r = usage.get("cacheReadTokens") or usage.get("cacheRead") or 0
    cache_w = usage.get("cacheWriteTokens") or usage.get("cacheWrite") or 0
    return int(input_t), int(output_t), int(cache_r), int(cache_w)


def compute_cost(usage: dict, model: str) -> float:
    """Compute cost from usage dict. Prefers cost.total if available."""
    cost_obj = usage.get("cost", {})
    if isinstance(cost_obj, dict) and cost_obj.get("total", 0) > 0:
        return cost_obj["total"]

    model_key = _normalize_model(model)
    pricing = MODEL_PRICING.get(model_key, FALLBACK_PRICING)

    input_t, output_t, cache_r, cache_w = get_usage_tokens(usage)

    cost = (
        (input_t - cache_r - cache_w) * pricing["input"]
        + output_t * pricing["output"]
        + cache_r * pricing["cache_read"]
        + cache_w * pricing["cache_write"]
    ) / 1_000_000

    return max(cost, 0.0)


def _normalize_model(model: str) -> str:
    """Strip provider prefix (e.g. 'anthropic/claude-opus-4-6' -> 'claude-opus-4-6')."""
    if "/" in model:
        model = model.rsplit("/", 1)[-1]
    return model


def parse_time_filter(days: int | None = None, since: str | None = None) -> datetime | None:
    """Convert --days or --since to a UTC cutoff datetime."""
    if since:
        try:
            dt = datetime.strptime(since, "%Y-%m-%d")
            return dt.replace(tzinfo=timezone.utc)
        except ValueError:
            print(f"Error: Invalid date format '{since}'. Use YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    if days is not None:
        return datetime.now(timezone.utc) - timedelta(days=days)
    return None


def discover_agents(agents_dir: Path | None = None) -> list[tuple[str, Path]]:
    """Return list of (agent_name, sessions_dir) for all agents."""
    base = agents_dir or DEFAULT_AGENTS_DIR
    if not base.is_dir():
        return []
    result = []
    for agent_dir in sorted(base.iterdir()):
        if not agent_dir.is_dir():
            continue
        sessions = agent_dir / "sessions"
        if sessions.is_dir():
            result.append((agent_dir.name, sessions))
    return result


def iter_session_files(
    sessions_dir: Path, cutoff: datetime | None = None
) -> list[Path]:
    """List .jsonl files in a sessions directory, optionally filtered by mtime."""
    files = []
    for f in sessions_dir.iterdir():
        if f.suffix != ".jsonl":
            continue
        if cutoff:
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
            if mtime < cutoff:
                continue
        files.append(f)
    return sorted(files)


def parse_session_file(path: Path) -> list[dict]:
    """Parse a session JSONL file, returning all message entries."""
    entries = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    if entry.get("type") == "message":
                        entries.append(entry)
                except json.JSONDecodeError:
                    continue
    except OSError as e:
        print(f"Warning: Could not read {path}: {e}", file=sys.stderr)
    return entries


def extract_message_data(entry: dict) -> dict | None:
    """Extract skill attribution and usage data from a message entry.

    Returns dict with: skills, usage, model, timestamp, or None if not assistant.
    """
    msg = entry.get("message", {})
    if msg.get("role") != "assistant":
        return None

    usage = msg.get("usage")
    if not usage:
        return None

    model = msg.get("model", "unknown")
    timestamp = entry.get("timestamp", "")

    tool_calls = []
    for item in msg.get("content", []):
        if isinstance(item, dict) and item.get("type") == "toolCall":
            tool_calls.append(item)

    skills = attribute_skill(tool_calls)

    return {
        "skills": skills,
        "usage": usage,
        "model": model,
        "timestamp": timestamp,
    }


def format_tokens(n: int) -> str:
    """Format token count with K/M suffix for readability."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def format_cost(c: float) -> str:
    """Format cost as dollar string."""
    if c >= 1.0:
        return f"${c:.2f}"
    if c >= 0.01:
        return f"${c:.3f}"
    return f"${c:.4f}"
