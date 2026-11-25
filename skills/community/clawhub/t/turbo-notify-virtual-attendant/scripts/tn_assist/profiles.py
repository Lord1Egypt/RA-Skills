"""How the unattended runner starts a model, one fresh process per work item.

A **contact** (and a summary) process gets no tools, no MCP server and no credential. An
**administrator or attendant** process gets the read-only Turbo Notify tools and nothing else; the
API key reaches it only through the one variable its MCP configuration names. Every process
starts in an empty directory and never sees the owner's own instruction files (verified with
canaries; see the spec, Outcomes S2).
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

KEY_ENV = "TURBO_NOTIFY_API_KEY"
MCP_NAME = "turbo-notify"
ADMIN_READ_TOOLS = (
    "list_messages", "get_message", "get_message_status", "list_contacts", "get_contact",
    "list_groups", "get_group", "list_numbers", "get_number", "get_message_quota",
    "get_contact_quota", "get_usage", "list_events",
)  # fmt: skip
SUPPORTED = ("claude-code", "codex")
Role = Literal["contact", "compaction", "admin", "attendant"]
Harness = Literal["claude-code", "codex"]
_KEEP = ("HOME", "PATH", "LANG", "LC_ALL", "TMPDIR", "USER", "LOGNAME", "SHELL", "TERM")
_KEEP_PREFIXES = ("ANTHROPIC_", "OPENAI_", "CLAUDE_CONFIG", "XDG_")
_CODEX_FEATURES_OFF = (
    "shell_tool", "unified_exec", "apps", "code_mode_host", "multi_agent", "goals",
    "image_generation", "plugins", "hooks", "skill_search",
)  # fmt: skip


class UnsupportedHarness(Exception):
    """This harness cannot be started with a tool restriction that was proven to hold."""


@dataclass(frozen=True)
class Child:
    argv: list[str]
    env: dict[str, str]
    cwd: Path
    stdin: str
    output_file: Path | None = None


def _base_env(source: Mapping[str, str]) -> dict[str, str]:
    env = {k: v for k, v in source.items() if k in _KEEP or k.startswith(_KEEP_PREFIXES)}
    env.pop(KEY_ENV, None)
    return env


def _has_tools(role: Role) -> bool:
    return role in ("admin", "attendant")


def build_child(
    harness: str,
    role: Role,
    prompt: str,
    *,
    scratch: Path,
    mcp_url: str,
    key: str | None,
    base_env: Mapping[str, str],
    model: str | None = None,
) -> Child:
    if harness not in SUPPORTED:
        raise UnsupportedHarness(harness)
    cwd = scratch / "cwd"
    cwd.mkdir(parents=True, exist_ok=True)
    env = _base_env(base_env)
    if _has_tools(role):
        if not key:
            raise ValueError("an administrator process needs the API key")
        env[KEY_ENV] = key
    if harness == "claude-code":
        return _claude(role, prompt, scratch, cwd, mcp_url, env, model)
    return _codex(role, prompt, scratch, cwd, mcp_url, env, base_env, model)


def _claude(
    role: Role,
    prompt: str,
    scratch: Path,
    cwd: Path,
    mcp_url: str,
    env: dict[str, str],
    model: str | None,
) -> Child:
    servers: dict[str, object] = {}
    if _has_tools(role):
        servers[MCP_NAME] = {
            "type": "http",
            "url": mcp_url,
            "headers": {"Authorization": "Bearer ${" + KEY_ENV + "}"},
        }
    config = scratch / "mcp.json"
    config.write_text(json.dumps({"mcpServers": servers}), encoding="utf-8")
    argv = [
        "claude", "-p", "--strict-mcp-config", "--mcp-config", str(config),
        "--setting-sources", "", "--tools", "", "--disable-slash-commands",
        "--max-turns", "8" if _has_tools(role) else "2",
    ]  # fmt: skip
    if _has_tools(role):
        argv += ["--allowedTools", *[f"mcp__{MCP_NAME}__{t}" for t in ADMIN_READ_TOOLS]]
    if model:
        argv += ["--model", model]
    env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    env["CLAUDE_CODE_DISABLE_CLAUDE_MDS"] = "1"
    return Child(argv, env, cwd, prompt)


def _codex(
    role: Role,
    prompt: str,
    scratch: Path,
    cwd: Path,
    mcp_url: str,
    env: dict[str, str],
    base_env: Mapping[str, str],
    model: str | None,
) -> Child:
    # The flags that ignore user configuration still read AGENTS.md from CODEX_HOME, so the child
    # gets its own CODEX_HOME that holds nothing but a link to the login.
    home = scratch / "codex-home"
    home.mkdir(parents=True, exist_ok=True)
    real = Path(
        base_env.get("CODEX_HOME") or Path(base_env.get("HOME", "~")) / ".codex"
    ).expanduser()
    link = home / "auth.json"
    if not link.exists() and (real / "auth.json").exists():
        link.symlink_to(real / "auth.json")
    out = scratch / "answer.txt"
    argv = [
        "codex", "exec", "--skip-git-repo-check", "--ephemeral", "--ignore-user-config",
        "--ignore-rules", "-s", "read-only", "-C", str(cwd), "-c", 'approval_policy="never"',
        "-o", str(out),
    ]  # fmt: skip
    # MCP tools reach the model through the code-mode host in this Codex, so an administrator
    # process keeps it (its script sandbox has no process.env and imports nothing: tested with a
    # canary key) and a customer process, which has no MCP server, turns it off.
    for feature in _CODEX_FEATURES_OFF:
        if feature == "code_mode_host" and _has_tools(role):
            continue
        argv += ["--disable", feature]
    if _has_tools(role):
        tools = json.dumps(list(ADMIN_READ_TOOLS))
        argv += [
            "-c", f'mcp_servers.{MCP_NAME}.url="{mcp_url}"',
            "-c", f'mcp_servers.{MCP_NAME}.bearer_token_env_var="{KEY_ENV}"',
            "-c", f"mcp_servers.{MCP_NAME}.enabled_tools={tools}",
            "-c", f'mcp_servers.{MCP_NAME}.default_tools_approval_mode="approve"',
        ]  # fmt: skip
    if model:
        argv += ["-m", model]
    env["CODEX_HOME"] = str(home)
    return Child(argv, env, cwd, prompt, out)
