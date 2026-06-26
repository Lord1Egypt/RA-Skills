#!/usr/bin/env python3
"""Read-only deterministic auditor for agent skills and plugin folders.

Security boundary:
- does not install skills/plugins
- does not execute source files, package managers, hooks, or shell commands
- does not make network requests
- writes only when --output is explicitly provided
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.1"
MAX_TEXT_BYTES = 1_000_000

SCRIPT_SUFFIXES = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".rb",
    ".pl",
    ".php",
    ".toml",
}

ASSET_SUFFIXES = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".pdf",
    ".pptx",
    ".docx",
    ".xlsx",
    ".csv",
    ".zip",
}

def lit(*parts: str) -> str:
    return "".join(parts)


PATTERNS = {
    "secret_like": [
        re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
        re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"),
        re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
    ],
    "destructive_command": [
        re.compile(r"\brm\s+-rf\b"),
        re.compile(r"\bgit\s+reset\s+--hard\b"),
        re.compile(r"\bchmod\s+-R\s+777\b"),
        re.compile(r"\bdd\s+if=.*\bof="),
        re.compile(r"\bmkfs(?:\.[a-z0-9]+)?\b"),
    ],
    "shell_execution": [
        re.compile(r"\bsubprocess\.(?:run|Popen|call|check_call|check_output)\b"),
        re.compile(r"\bos\.system\b"),
        re.compile(r"\bchild_process\b"),
        re.compile(r"\beval\s*\("),
        re.compile(r"\bexec\s*\("),
    ],
    "network_call": [
        re.compile(r"https?://[^\s)'\"<>]+"),
        re.compile(r"\b(?:curl|wget)\s+"),
        re.compile(r"\bfetch\s*\("),
        re.compile(r"\brequests\.(?:get|post|put|delete|patch)\b"),
        re.compile(r"\baxios\.(?:get|post|put|delete|patch)\b"),
    ],
    "install_hook": [
        re.compile(rf'"{lit("post", "install")}"\s*:'),
        re.compile(rf'"{lit("pre", "install")}"\s*:'),
        re.compile(rf"\b{lit('post', 'install')}\b"),
    ],
    "credential_access": [
        re.compile(rf"\.{lit('s', 's', 'h')}/"),
        re.compile(rf"\.{lit('a', 'w', 's')}/"),
        re.compile(rf"\.{lit('c', 'o', 'n', 'f', 'i', 'g')}/"),
        re.compile(r"\bkeychain\b", re.IGNORECASE),
        re.compile(r"\bprintenv\b"),
        re.compile(r"\benv\s*>\b"),
    ],
    "claude_specific": [
        re.compile(r"\.claude(?:/|\\)"),
        re.compile(r"\.claude-plugin(?:/|\\)"),
        re.compile(r"\bClaude Code\b"),
        re.compile(r"\bCowork\b"),
        re.compile(r"\$" + lit("ARG", "UMENTS")),
        re.compile(r"\bclaude\s+plugin\b"),
    ],
    "codex_specific": [
        re.compile(r"\.codex(?:/|\\)"),
        re.compile(r"\.codex-plugin(?:/|\\)"),
        re.compile(r"\bAGENTS(?:\.override)?\.md\b"),
        re.compile(r"\bagents/openai\.yaml\b"),
        re.compile(r"\bcodex\s+plugin\b"),
    ],
    "gemini_specific": [
        re.compile(r"\.gemini(?:/|\\)"),
        re.compile(r"\bGEMINI\.md\b"),
        re.compile(r"\bgemini-extension\.json\b"),
        re.compile(r"\bgemini\s+(?:skills|extensions|mcp)\b"),
        re.compile(r"\brun_shell_command\b"),
    ],
    "dynamic_context": [
        re.compile(r"(?m)^!\s*`[^`]+`"),
    ],
    "invocation_control": [
        re.compile(r"(?m)^(disable-model-invocation|user-invocable|allowed-tools|disallowedTools|paths|context|agent|hooks)\s*:"),
    ],
    "hook_behavior": [
        re.compile(
            r"\b("
            + "|".join(
                [
                    lit("Pre", "Tool", "Use"),
                    lit("Post", "Tool", "Use"),
                    lit("User", "Prompt", "Submit"),
                    lit("Session", "Start"),
                    lit("Session", "End"),
                    lit("Subagent", "Start"),
                    lit("Subagent", "Stop"),
                ]
            )
            + r")\b"
        ),
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit an agent skill/plugin folder without executing it.")
    parser.add_argument("source", help="Path to a skill, plugin, or repository folder")
    parser.add_argument("--target-agent", help="Target agent name for compatibility mapping. Defaults to inferred runtime agent.")
    parser.add_argument("--mode", default="audit-only", choices=["audit-only", "port", "case-study"])
    parser.add_argument("--format", default="json", choices=["json", "markdown"], help="Output format")
    parser.add_argument("--output", help="Optional output file. Without this, report is printed to stdout.")
    return parser.parse_args()


def infer_target_agent(explicit: str | None) -> tuple[str, bool]:
    if explicit:
        return explicit, False

    env_pairs = {key.upper(): value.lower() for key, value in os.environ.items()}
    joined = " ".join(f"{key}={value}" for key, value in env_pairs.items())
    if "CODEX" in env_pairs or "codex" in joined:
        return "codex", True
    if "CLAUDECODE" in joined or "claude_code" in joined or "claude-code" in joined:
        return "claude", True
    if "CURSOR" in env_pairs or "cursor" in joined:
        return "cursor", True
    if "GEMINI" in env_pairs or "gemini" in joined:
        return "gemini", True
    return "codex", True


def relpath(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_hidden(rel: str) -> bool:
    return any(part.startswith(".") for part in rel.split("/"))


def is_binary(data: bytes) -> bool:
    if b"\x00" in data:
        return True
    sample = data[:4096]
    if not sample:
        return False
    non_text = sum(1 for byte in sample if byte < 9 or (13 < byte < 32))
    return non_text / len(sample) > 0.30


def read_text_sample(path: Path) -> tuple[str, bool]:
    data = path.read_bytes()[:MAX_TEXT_BYTES]
    binary = is_binary(data)
    if binary:
        return "", True
    return data.decode("utf-8", errors="replace"), False


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    raw = text[4:end].splitlines()
    data: dict[str, str] = {}
    current_key = ""
    block: list[str] = []
    for line in raw:
        if block and (line.startswith(" ") or line.strip() == ""):
            block.append(line.strip())
            continue
        if block and current_key:
            data[current_key] = "\n".join(block).strip()
            block = []
            current_key = ""
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if value in {"|", ">"}:
            current_key = key
            block = []
        else:
            data[key] = value
    if block and current_key:
        data[current_key] = "\n".join(block).strip()
    return data


def file_kind(path: Path, rel: str) -> str:
    name = path.name
    suffix = path.suffix.lower()
    parts = rel.split("/")
    if name in {
        "AGENTS.md",
        "AGENTS.override.md",
        "CLAUDE.md",
        "CLAUDE.local.md",
        "GEMINI.md",
    } or rel.endswith(("/CLAUDE.md", "/AGENTS.md", "/AGENTS.override.md", "/GEMINI.md")):
        return "instruction"
    if rel == "agents/openai.yaml":
        return "metadata"
    if name == "SKILL.md":
        return "skill"
    if name in {".mcp.json", "mcp.json"} or "mcp" in name.lower():
        return "mcp"
    if name in {"plugin.json", "manifest.json", "marketplace.json", "gemini-extension.json"} or ".claude-plugin" in parts or ".codex-plugin" in parts:
        return "manifest"
    if name in {"hooks.json"} or "hooks" in parts:
        return "hook"
    if "commands" in parts and suffix in {".md", ".txt", ".toml"}:
        return "command"
    if "agents" in parts and suffix in {".md", ".yaml", ".yml", ".json", ".toml"}:
        return "agent"
    if "policies" in parts and suffix == ".toml":
        return "hook"
    if suffix in SCRIPT_SUFFIXES or "scripts" in parts:
        return "script"
    if suffix in ASSET_SUFFIXES or "assets" in parts or "examples" in parts:
        return "asset"
    return "file"


def scan_patterns(text: str) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for category, patterns in PATTERNS.items():
        matches: set[str] = set()
        for pattern in patterns:
            for match in pattern.finditer(text):
                value = match.group(0)
                if category == "network_call" and value.startswith("http://www.w3.org/"):
                    continue
                if category == "secret_like":
                    value = redact(value)
                matches.add(value[:160])
        if matches:
            findings.append({"category": category, "matches": sorted(matches)})
    return findings


def redact(value: str) -> str:
    if len(value) <= 12:
        return "<redacted>"
    return f"{value[:6]}...{value[-4:]}"


def detected_ecosystems(inventory: dict[str, list[str]], security_findings: list[dict[str, Any]]) -> list[str]:
    ecosystems: set[str] = set()
    all_paths = " ".join(
        path
        for paths in inventory.values()
        for path in paths
    ).lower()
    categories = {finding["category"] for finding in security_findings}

    if ".claude" in all_paths or "claude_specific" in categories:
        ecosystems.add("claude")
    if ".codex" in all_paths or "codex_specific" in categories or any(path.endswith("AGENTS.md") for path in inventory["instruction_files"]):
        ecosystems.add("codex")
    if ".gemini" in all_paths or "gemini_specific" in categories or any(path.endswith("GEMINI.md") for path in inventory["instruction_files"]):
        ecosystems.add("gemini")
    if inventory["skill_files"]:
        ecosystems.add("agent-skills")
    return sorted(ecosystems)


def classify_source(inventory: dict[str, list[str]], has_plugin_dir: bool) -> str:
    has_skills = bool(inventory["skill_files"])
    has_commands = bool(inventory["command_files"])
    has_agents = bool(inventory["agent_files"])
    has_mcp = bool(inventory["mcp_files"])
    has_hooks = bool(inventory["hook_files"])
    has_instructions = bool(inventory["instruction_files"])
    has_manifest = bool(inventory["manifest_files"]) or has_plugin_dir
    has_extension = any(path.endswith("gemini-extension.json") for path in inventory["manifest_files"])

    if has_extension and has_mcp:
        return "mcp-backed-extension"
    if has_extension:
        return "extension"
    if has_manifest and has_mcp:
        return "mcp-backed-plugin"
    if has_manifest:
        return "plugin"
    if has_skills and (has_commands or has_agents or has_mcp or has_hooks):
        return "plugin"
    if has_skills and has_instructions:
        return "repo"
    if has_skills:
        return "skill"
    if has_commands:
        return "command-bundle"
    if has_agents:
        return "agent-bundle"
    if has_instructions:
        return "repo"
    return "unknown"


def compatibility_status(inventory: dict[str, list[str]], security_findings: list[dict[str, Any]]) -> dict[str, Any]:
    reasons: list[str] = []
    categories = {finding["category"] for finding in security_findings}
    if inventory["mcp_files"]:
        reasons.append("MCP configuration requires target-agent setup and credentials.")
    if inventory["command_files"]:
        reasons.append("Slash commands or command files must be rewritten as target-agent workflows.")
    if inventory["agent_files"]:
        reasons.append("Agent/subagent files may describe orchestration that is not directly portable.")
    if inventory["instruction_files"]:
        reasons.append("Project instruction files should be translated or bridged separately from skills.")
    if inventory["hook_files"]:
        reasons.append("Hooks require explicit lifecycle/event mapping before activation.")
    if "claude_specific" in categories:
        reasons.append("Claude-specific paths, commands, or runtime wording need adaptation.")
    if "codex_specific" in categories:
        reasons.append("Codex-specific paths, metadata, or runtime wording need adaptation.")
    if "gemini_specific" in categories:
        reasons.append("Gemini-specific paths, extensions, commands, or runtime wording need adaptation.")
    if "dynamic_context" in categories:
        reasons.append("Dynamic context injection needs target-specific rewriting or manual review.")
    if "invocation_control" in categories:
        reasons.append("Source-specific invocation control fields need target-specific mapping.")
    if {"secret_like", "destructive_command", "credential_access", "install_hook"} & categories:
        reasons.append("Security findings require review before installation or porting.")

    if {"secret_like", "destructive_command", "credential_access", "install_hook"} & categories:
        status = "unsupported"
    elif inventory["hook_files"]:
        status = "unsupported"
    elif inventory["mcp_files"]:
        status = "dependency-bound"
    elif inventory["command_files"] or inventory["agent_files"] or inventory["instruction_files"] or {"claude_specific", "codex_specific", "gemini_specific", "dynamic_context", "invocation_control"} & categories:
        status = "needs-adaptation"
    elif inventory["skill_files"]:
        status = "portable"
    else:
        status = "needs-adaptation"
        reasons.append("No standard SKILL.md files were found.")

    return {"status": status, "reasons": sorted(set(reasons))}


def risk_level(security_findings: list[dict[str, Any]], file_records: list[dict[str, Any]]) -> str:
    categories = {finding["category"] for finding in security_findings}
    if {"secret_like", "destructive_command", "credential_access", "install_hook"} & categories:
        return "high"
    if {"shell_execution", "network_call"} & categories:
        return "medium"
    if any(record["kind"] in {"script", "mcp"} or record["binary"] for record in file_records):
        return "medium"
    return "low"


def target_name_from_skill(path: str, frontmatter_by_file: dict[str, dict[str, str]]) -> str:
    frontmatter = frontmatter_by_file.get(path, {})
    name = frontmatter.get("name", "").strip()
    if name:
        return re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-") or "ported-skill"
    parent = Path(path).parent.name if Path(path).parent.name else Path(path).stem
    return re.sub(r"[^a-z0-9-]+", "-", parent.lower()).strip("-") or "ported-skill"


def target_project_instruction_file(target_agent: str) -> str:
    if target_agent == "codex":
        return "AGENTS.md"
    if target_agent in {"claude", "claude-code"}:
        return "CLAUDE.md"
    if target_agent in {"gemini", "gemini-cli"}:
        return "GEMINI.md"
    return "project-instructions.md"


def target_agent_file(source_path: str, target_agent: str) -> str:
    name = re.sub(r"[^a-z0-9-]+", "-", Path(source_path).stem.lower()).strip("-") or "agent"
    if target_agent == "codex":
        return f".codex/agents/{name}.toml"
    if target_agent in {"claude", "claude-code", "gemini", "gemini-cli"}:
        return f"agents/{name}.md"
    return f"references/agents/{name}.md"


def target_plugin_manifest(target_agent: str) -> str:
    if target_agent == "codex":
        return ".codex-plugin/plugin.json"
    if target_agent in {"claude", "claude-code"}:
        return ".claude-plugin/plugin.json"
    if target_agent in {"gemini", "gemini-cli"}:
        return "gemini-extension.json"
    return "references/plugin-plan.md"


def build_porting_map(root: Path, inventory: dict[str, list[str]], frontmatter_by_file: dict[str, dict[str, str]], target_agent: str) -> list[dict[str, str]]:
    source_name = re.sub(r"[^a-z0-9-]+", "-", root.name.lower()).strip("-") or "source"
    multi = len(inventory["skill_files"]) > 1 or bool(
        inventory["manifest_files"]
        or inventory["command_files"]
        or inventory["agent_files"]
        or inventory["mcp_files"]
        or inventory["hook_files"]
        or inventory["instruction_files"]
    )
    mapped: list[dict[str, str]] = []

    for skill_file in inventory["skill_files"]:
        skill_name = target_name_from_skill(skill_file, frontmatter_by_file)
        if multi:
            target = f"ports/{source_name}/{target_agent}/skills/{skill_name}/SKILL.md"
        else:
            target = f"skills/{target_agent}/{skill_name}/SKILL.md"
        mapped.append({"source": skill_file, "target": target, "action": "port-skill", "status": "translated"})

    for instruction_file in inventory["instruction_files"]:
        target = f"ports/{source_name}/{target_agent}/{target_project_instruction_file(target_agent)}"
        mapped.append({"source": instruction_file, "target": target, "action": "adapt-project-instructions", "status": "translated"})

    for command_file in inventory["command_files"]:
        mapped.append({"source": command_file, "target": f"ports/{source_name}/{target_agent}/references/commands.md", "action": "adapt-command", "status": "translated"})

    for agent_file in inventory["agent_files"]:
        mapped.append({"source": agent_file, "target": f"ports/{source_name}/{target_agent}/{target_agent_file(agent_file, target_agent)}", "action": "adapt-agent", "status": "partial"})

    for manifest_file in inventory["manifest_files"]:
        mapped.append({"source": manifest_file, "target": f"ports/{source_name}/{target_agent}/{target_plugin_manifest(target_agent)}", "action": "adapt-plugin-manifest", "status": "partial"})

    for mcp_file in inventory["mcp_files"]:
        mapped.append({"source": mcp_file, "target": f"ports/{source_name}/{target_agent}/references/dependencies.md", "action": "document-dependency", "status": "manual"})

    for hook_file in inventory["hook_files"]:
        mapped.append({"source": hook_file, "target": f"ports/{source_name}/{target_agent}/references/unsupported.md", "action": "document-hook", "status": "unsupported"})

    return mapped


def recommended_scope(root: Path, source_type: str, inventory: dict[str, list[str]]) -> dict[str, str]:
    skill_count = len(inventory["skill_files"])
    ecosystem = source_type in {"plugin", "mcp-backed-plugin", "extension", "mcp-backed-extension", "repo"} or skill_count > 1
    if source_type == "skill" and skill_count <= 1:
        return {
            "recommended_scope": "single-skill",
            "recommended_scope_reason": "The source appears to be one skill, so audit and port it as one target-agent skill.",
        }
    if ecosystem:
        return {
            "recommended_scope": "focused",
            "recommended_scope_reason": "The source is a multi-artifact ecosystem; recommend a focused first port based on named workflows or the most portable SKILL.md files.",
        }
    return {
        "recommended_scope": "unknown",
        "recommended_scope_reason": "The source does not expose enough standard skill structure to choose a port scope confidently.",
    }


def proposed_target_layout(root: Path, source_type: str, inventory: dict[str, list[str]], target_agent: str, porting: list[dict[str, str]]) -> str | None:
    source_name = re.sub(r"[^a-z0-9-]+", "-", root.name.lower()).strip("-") or "source"
    if source_type == "skill" and len(inventory["skill_files"]) <= 1 and porting:
        return str(Path(porting[0]["target"]).parent)
    if porting or source_type != "unknown":
        return f"ports/{source_name}/{target_agent}/"
    return None


def candidate_items(porting: list[dict[str, str]], inventory: dict[str, list[str]]) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    auto_port = [item for item in porting if item["action"] == "port-skill"]
    auto_adapt = [item for item in porting if item["action"] in {"adapt-project-instructions", "adapt-command", "adapt-agent", "adapt-plugin-manifest"}]
    dependencies = [item for item in porting if item["action"] == "document-dependency"]
    unsupported: list[dict[str, str]] = []
    for path in inventory["manifest_files"]:
        unsupported.append({"source": path, "reason": "Plugin marketplace or lifecycle behavior must be represented as target-agent notes or a plugin implementation plan."})
    for path in inventory["agent_files"]:
        unsupported.append({"source": path, "reason": "Subagent orchestration is not assumed to exist in the target agent."})
    for path in inventory["hook_files"]:
        unsupported.append({"source": path, "reason": "Hooks require target-specific lifecycle, matcher, input, and output mapping before activation."})
    return auto_port, auto_adapt, dependencies, unsupported


def layer_summary(inventory: dict[str, list[str]]) -> dict[str, int]:
    return {
        "project_instructions": len(inventory["instruction_files"]),
        "skills": len(inventory["skill_files"]),
        "commands": len(inventory["command_files"]),
        "agents": len(inventory["agent_files"]),
        "plugins": len(inventory["manifest_files"]),
        "mcp_tools": len(inventory["mcp_files"]),
        "hooks": len(inventory["hook_files"]),
    }


def conversion_status(porting: list[dict[str, str]]) -> dict[str, int]:
    counts = {"direct": 0, "translated": 0, "partial": 0, "unsupported": 0, "manual": 0}
    for item in porting:
        status = item.get("status", "partial")
        if status in counts:
            counts[status] += 1
    return counts


def manual_steps(report: dict[str, Any]) -> list[str]:
    steps: list[str] = []
    if report["dependency_bound_items"]:
        steps.append("Enable equivalent MCP servers/tools and provide credentials or subscriptions outside the skill package.")
    if report["unsupported_items"]:
        steps.append("Review unsupported orchestration or lifecycle behavior before relying on those workflows.")
    if report["security"]["risk_level"] != "low":
        steps.append("Review security findings before installing or running any source scripts.")
    if report["porting_map"]:
        if report["mode"] != "audit-only":
            steps.append("Validate staged files and install with the target agent's normal installer.")
    return steps


def audit(root: Path, target_agent: str, target_agent_inferred: bool, mode: str) -> dict[str, Any]:
    root = root.resolve()
    if not root.exists():
        raise SystemExit(f"Source path does not exist: {root}")
    if not root.is_dir():
        raise SystemExit(f"Source path must be a directory: {root}")

    inventory = {
        "instruction_files": [],
        "skill_files": [],
        "command_files": [],
        "agent_files": [],
        "mcp_files": [],
        "manifest_files": [],
        "hook_files": [],
        "script_files": [],
        "asset_files": [],
    }
    file_records: list[dict[str, Any]] = []
    security_findings: list[dict[str, Any]] = []
    frontmatter_by_file: dict[str, dict[str, str]] = {}
    has_plugin_dir = False

    for path in sorted(root.rglob("*"), key=lambda p: p.as_posix()):
        if path.is_dir():
            if path.name in {".claude-plugin", ".codex-plugin"}:
                has_plugin_dir = True
            continue
        rel = relpath(path, root)
        if rel.startswith(".git/") or "__pycache__" in rel.split("/") or path.suffix == ".pyc":
            continue
        kind = file_kind(path, rel)
        try:
            size = path.stat().st_size
            text, binary = read_text_sample(path)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except FileNotFoundError:
            continue
        record = {
            "path": rel,
            "kind": kind,
            "size_bytes": size,
            "sha256": digest,
            "hidden": is_hidden(rel),
            "binary": binary,
        }
        file_records.append(record)

        key = f"{kind}_files"
        if key in inventory:
            inventory[key].append(rel)

        if kind == "skill" and text:
            frontmatter_by_file[rel] = parse_frontmatter(text)

        if text:
            config_like = path.name in {"settings.json", "config.toml", "plugin.json", "gemini-extension.json"} or kind in {"manifest", "mcp"}
            if config_like and ('"mcpServers"' in text or "'mcpServers'" in text or "[mcp_servers." in text):
                if rel not in inventory["mcp_files"]:
                    inventory["mcp_files"].append(rel)
            if config_like and ("[hooks]" in text or '"hooks"' in text):
                if kind not in {"hook", "skill"} and rel not in inventory["hook_files"]:
                    inventory["hook_files"].append(rel)
            for finding in scan_patterns(text):
                security_findings.append({"file": rel, **finding})
        elif binary and (kind not in {"asset"} or size > 5_000_000):
            security_findings.append({"file": rel, "category": "binary_or_large_file", "matches": [f"{size} bytes"]})

    source_type = classify_source(inventory, has_plugin_dir)
    compatibility = compatibility_status(inventory, security_findings)
    ecosystems = detected_ecosystems(inventory, security_findings)
    porting = build_porting_map(root, inventory, frontmatter_by_file, target_agent)
    scope = recommended_scope(root, source_type, inventory)
    layout = proposed_target_layout(root, source_type, inventory, target_agent, porting)
    auto_port, auto_adapt, dependencies, unsupported = candidate_items(porting, inventory)

    source_name = re.sub(r"[^a-z0-9-]+", "-", root.name.lower()).strip("-") or "source"
    output_path = None
    if mode == "port":
        output_path = f"ports/{source_name}/{target_agent}/" if source_type != "skill" or len(inventory["skill_files"]) > 1 else None
        if output_path is None and porting:
            output_path = str(Path(porting[0]["target"]).parent)

    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "mode": mode,
        "target_agent": target_agent,
        "source": {
            "path": str(root),
            "name": source_name,
            "type": source_type,
            "detected_ecosystems": ecosystems,
        },
        "locations": {
            "source_read_from": str(root),
            "output_path": output_path,
            "installed": False,
        },
        "compatibility": compatibility,
        "recommendation": {
            "target_agent_inferred": target_agent_inferred,
            **scope,
            "proposed_target_layout": layout,
            "next_port_command": f"Use skill-port in port mode for {root} targeting {target_agent}." if porting else None,
        },
        "inventory": {
            "files_total": len(file_records),
            **{key: sorted(value) for key, value in inventory.items()},
            "files": file_records,
        },
        "layer_summary": layer_summary(inventory),
        "conversion_status": conversion_status(porting),
        "security": {
            "risk_level": risk_level(security_findings, file_records),
            "findings": sorted(security_findings, key=lambda item: (item["file"], item["category"])),
        },
        "porting_map": porting,
        "auto_port_candidates": auto_port,
        "auto_adaptation_candidates": auto_adapt,
        "dependency_bound_items": dependencies,
        "unsupported_items": unsupported,
        "remaining_manual_steps": [],
    }
    report["remaining_manual_steps"] = manual_steps(report)
    return report


def to_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Skill Port Audit: {report['source']['name']}",
        "",
        f"- Source: `{report['source']['path']}`",
        f"- Source type: `{report['source']['type']}`",
        f"- Detected ecosystems: `{', '.join(report['source']['detected_ecosystems']) or 'unknown'}`",
        f"- Target agent: `{report['target_agent']}`" + (" (inferred)" if report["recommendation"]["target_agent_inferred"] else ""),
        f"- Mode: `{report['mode']}`",
        f"- Compatibility: `{report['compatibility']['status']}`",
        f"- Security risk: `{report['security']['risk_level']}`",
        f"- Installed: `{str(report['locations']['installed']).lower()}`",
    ]
    if report["locations"]["output_path"]:
        lines.append(f"- Output path: `{report['locations']['output_path']}`")

    if report["compatibility"]["reasons"]:
        lines.extend(["", "## Compatibility Reasons"])
        lines.extend(f"- {reason}" for reason in report["compatibility"]["reasons"])

    lines.extend(["", "## Recommendation"])
    lines.append(f"- Scope: `{report['recommendation']['recommended_scope']}`")
    lines.append(f"- Reason: {report['recommendation']['recommended_scope_reason']}")
    if report["recommendation"]["proposed_target_layout"]:
        lines.append(f"- Proposed target layout: `{report['recommendation']['proposed_target_layout']}`")
    if report["recommendation"]["next_port_command"]:
        lines.append(f"- Next port command: {report['recommendation']['next_port_command']}")

    lines.extend(["", "## Inventory"])
    for key in ["instruction_files", "skill_files", "command_files", "agent_files", "mcp_files", "manifest_files", "hook_files", "script_files", "asset_files"]:
        lines.append(f"- {key}: {len(report['inventory'][key])}")

    lines.extend(["", "## Layer Summary"])
    for key, value in report["layer_summary"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Conversion Status"])
    for key, value in report["conversion_status"].items():
        lines.append(f"- {key}: {value}")

    if report["security"]["findings"]:
        lines.extend(["", "## Security Findings"])
        for finding in report["security"]["findings"]:
            lines.append(f"- `{finding['file']}`: {finding['category']} ({len(finding['matches'])} match(es))")

    if report["porting_map"]:
        lines.extend(["", "## Porting Map"])
        for item in report["porting_map"]:
            lines.append(f"- `{item['source']}` -> `{item['target']}` ({item['action']}, {item.get('status', 'partial')})")

    if report["auto_port_candidates"] or report["auto_adaptation_candidates"] or report["dependency_bound_items"] or report["unsupported_items"]:
        lines.extend(["", "## Automatic Work Available In Port Mode"])
        if report["auto_port_candidates"]:
            lines.append(f"- Port skill files: {len(report['auto_port_candidates'])}")
        if report["auto_adaptation_candidates"]:
            lines.append(f"- Adapt instructions, commands, agents, or plugin manifests: {len(report['auto_adaptation_candidates'])}")
        if report["dependency_bound_items"]:
            lines.append(f"- Stage dependency notes: {len(report['dependency_bound_items'])}")
        if report["unsupported_items"]:
            lines.append(f"- Stage unsupported-feature notes: {len(report['unsupported_items'])}")

    if report["remaining_manual_steps"]:
        lines.extend(["", "## Remaining Manual Steps"])
        lines.extend(f"- {step}" for step in report["remaining_manual_steps"])

    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    target_agent, inferred = infer_target_agent(args.target_agent)
    report = audit(Path(args.source), target_agent, inferred, args.mode)
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n" if args.format == "json" else to_markdown(report)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
