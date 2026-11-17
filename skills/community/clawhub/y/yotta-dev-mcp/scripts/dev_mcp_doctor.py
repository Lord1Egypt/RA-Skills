#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Broad, read-only MCP client config discovery for mcp_doctor.

The module deliberately separates discovery from parsing:

* a declarative host registry describes candidate paths, formats and keys;
* parsers only extract server names (never commands, args or env values);
* every registry entry appears in a coverage report, so a caller can never
  mistake "the one file I happened to parse" for "all configs are healthy".

Python 3.8+ standard library only. No network, no writes.
"""

from __future__ import annotations

import fnmatch
import glob
import json
import os
import re
from pathlib import Path

from dev_common import _frontmatter_name, _frontmatter_version, _read_text

VERSION = 1
DEFAULT_MAX_CONFIG_BYTES = 2_000_000
DEFAULT_MAX_CONFIGS = 500
DEFAULT_MAX_SKILL_DIRS = 120

DEFAULT_JSON_KEYS = ("mcpServers", "mcp", "servers", "context_servers")
DEFAULT_TOML_KEYS = ("mcp_servers",)


def _host(host_id, label, candidates, formats=("json",), server_keys=None,
          tier="verified", note="", exclude=()):
    return {
        "id": host_id,
        "label": label,
        "candidates": list(candidates),
        "formats": list(formats),
        "server_keys": list(server_keys or DEFAULT_JSON_KEYS),
        "tier": tier,
        "note": note,
        "exclude": list(exclude),
    }


def _builtin_hosts():
    """A broad, tiered registry.

    ``verified`` means the path/format is documented or directly observed.
    ``unverified`` means the path is a best-effort candidate: if it exists it
    is parsed, but a missing file is reported as a coverage gap instead of
    being silently treated as "not installed".
    """
    return [
        _host(
            "codex", "Codex",
            [
                "{codex_home}/config.toml",
                "{home}/.codex/config.toml",
                "{codex_home}/config.json",
                "{codex_home}/mcp.json",
                "{home}/.codex/config.json",
                "{home}/.codex/mcp.json",
            ],
            formats=("toml", "json"),
            server_keys=("mcp_servers",) + DEFAULT_JSON_KEYS,
        ),
        _host(
            "claude-code", "Claude Code",
            [
                "{claude_config_dir}/settings.json",
                "{home}/.claude/settings.json",
                "{home}/.claude.json",
                "{cwd}/.mcp.json",
            ],
        ),
        _host(
            "cursor", "Cursor",
            ["{home}/.cursor/mcp.json", "{cwd}/.cursor/mcp.json"],
        ),
        _host(
            "opencode", "OpenCode",
            [
                "{xdg_config_home}/opencode/opencode.jsonc",
                "{xdg_config_home}/opencode/opencode.json",
                "{home}/.config/opencode/opencode.jsonc",
                "{home}/.config/opencode/opencode.json",
                "{cwd}/opencode.jsonc",
                "{cwd}/opencode.json",
            ],
            formats=("jsonc", "json"),
            server_keys=("mcp", "mcpServers", "servers"),
        ),
        _host(
            "workbuddy", "WorkBuddy",
            [
                "{home}/.workbuddy/mcp.json",
                "{home}/.workbuddy/connectors/*/mcp.json",
            ],
            exclude=("**/connectors-marketplace/**",),
        ),
        _host(
            "windsurf", "Windsurf",
            [
                "{home}/.codeium/windsurf/mcp_config.json",
                "{home}/.codeium/windsurf/mcp.json",
            ],
        ),
        _host(
            "continue", "Continue",
            ["{home}/.continue/config.json", "{home}/.continue/config.yaml"],
            formats=("json", "yaml"),
        ),
        _host(
            "gemini", "Gemini CLI",
            ["{home}/.gemini/settings.json", "{home}/.gemini/mcp.json"],
        ),
        _host(
            "qwen", "Qwen Code",
            ["{home}/.qwen/settings.json", "{home}/.qwen/mcp.json"],
        ),
        _host(
            "trae", "Trae Code CLI",
            ["{home}/.traecli/mcp.json", "{home}/.trae/mcp.json"],
        ),
        _host(
            "trae-cn", "Trae IDE",
            ["{home}/.trae-cn/mcp.json"],
        ),
        _host(
            "comate", "Comate",
            ["{home}/.comate/mcp.json", "{home}/.comate/settings.json"],
        ),
        _host(
            "codebuddy", "CodeBuddy Code",
            ["{home}/.codebuddy/mcp.json", "{home}/.codebuddy/settings.json"],
        ),
        _host(
            "kimi", "Kimi Code CLI",
            ["{home}/.kimi/mcp.json", "{home}/.kimi/settings.json"],
        ),
        _host(
            "kiro", "Kiro",
            ["{home}/.kiro/mcp.json", "{home}/.kiro/settings.json"],
        ),
        _host(
            "vscode", "VS Code",
            [
                "{cwd}/.vscode/mcp.json",
                "{env:APPDATA}/Code/User/mcp.json",
                "{xdg_config_home}/Code/User/mcp.json",
            ],
        ),
        _host(
            "zed", "Zed",
            [
                "{xdg_config_home}/zed/settings.json",
                "{home}/.config/zed/settings.json",
            ],
            server_keys=("context_servers", "mcpServers", "mcp", "servers"),
        ),
        _host(
            "goose", "Goose",
            ["{xdg_config_home}/goose/config.yaml", "{home}/.config/goose/config.yaml"],
            formats=("yaml",),
            note="Goose YAML is reported as unsupported, never silently skipped.",
        ),
        # The following paths are useful best-effort candidates but are not
        # claimed as verified. If they are missing they show up as coverage
        # gaps, which keeps "all_clear" honest.
        _host("cline", "Cline", ["{home}/.cline/mcp.json", "{home}/.config/cline/mcp.json"], tier="unverified"),
        _host("roo-code", "Roo Code", ["{home}/.roo/mcp.json", "{home}/.config/roo/mcp.json"], tier="unverified"),
        _host("amp", "Amp", ["{home}/.config/amp/settings.json"], tier="unverified"),
        _host("lm-studio", "LM Studio", ["{home}/.lmstudio/mcp.json", "{home}/.cache/lm-studio/mcp.json"], tier="unverified"),
        _host("jetbrains", "JetBrains", ["{cwd}/.idea/mcp.json", "{home}/.config/JetBrains/*/mcp.json"], tier="unverified"),
        _host("warp", "Warp", ["{home}/.warp/mcp.json"], tier="unverified"),
        _host("5ire", "5ire", ["{home}/.5ire/mcp.json"], tier="unverified"),
        _host("witsy", "Witsy", ["{home}/.witsy/mcp.json"], tier="unverified"),
        _host("enconvo", "Enconvo", ["{home}/.enconvo/mcp.json"], tier="unverified"),
        _host("chatwise", "ChatWise", ["{home}/.chatwise/mcp.json"], tier="unverified"),
        _host("jan", "Jan", ["{home}/.jan/mcp.json"], tier="unverified"),
        _host("msty", "Msty", ["{home}/.msty/mcp.json"], tier="unverified"),
        _host("boltai", "BoltAI", ["{home}/.boltai/mcp.json"], tier="unverified"),
        _host("copilot-cli", "GitHub Copilot CLI", ["{home}/.copilot/mcp-config.json"], tier="unverified"),
        _host("factory-droid", "Factory Droid", ["{home}/.factory/mcp.json"], tier="unverified"),
        _host("qoder", "Qoder", ["{home}/.qoder/mcp.json"], tier="unverified"),
        _host("lingma", "Lingma", ["{home}/.lingma/mcp.json"], tier="unverified"),
        # Hosts with no verified config path are still surfaced as named gaps.
        _host("windsurf-cascade", "Windsurf Cascade", [], tier="unverified",
              note="config path not verified; use config_paths to add it explicitly"),
        _host("cursor-cli", "Cursor CLI", [], tier="unverified",
              note="config path not verified; Cursor desktop config is covered by the cursor host"),
    ]


def _builtin_skill_hosts():
    """Skill directories aligned with the installer host map."""
    return [
        _host("codex", "Codex", ["{codex_home}/skills", "{home}/.codex/skills"]),
        _host("claude", "Claude Code", ["{claude_config_dir}/skills", "{home}/.claude/skills"]),
        _host("cursor", "Cursor", ["{home}/.cursor/skills", "{home}/.agents/skills"]),
        _host("opencode", "OpenCode", ["{xdg_config_home}/opencode/skills", "{home}/.config/opencode/skills"]),
        _host("gemini", "Gemini CLI", ["{home}/.gemini/skills", "{home}/.agents/skills"]),
        _host("goose", "Goose", ["{home}/.config/goose/skills", "{home}/.agents/skills"]),
        _host("amp", "Amp", ["{home}/.config/agents/skills", "{home}/.agents/skills"]),
        _host("windsurf", "Windsurf", ["{home}/.codeium/windsurf/skills"]),
        _host("workbuddy", "WorkBuddy", ["{home}/.workbuddy/skills"]),
        _host("kiro", "Kiro", ["{home}/.kiro/skills"]),
        _host("trae", "Trae Code CLI", ["{home}/.traecli/skills"]),
        _host("trae-cn", "Trae IDE", ["{home}/.trae-cn/skills"]),
        _host("qwen", "Qwen Code", ["{home}/.qwen/skills"]),
        _host("comate", "Comate", ["{home}/.comate/skills"]),
        _host("codebuddy", "CodeBuddy Code", ["{home}/.codebuddy/skills"]),
        _host("kimi", "Kimi Code CLI", ["{home}/.kimi/skills"]),
        _host("agents", "AGENTS.md", ["{home}/.agents/skills"]),
    ]


def _environment(environ, home):
    env = dict(environ or {})
    return {
        "home": str(home),
        "cwd": "",
        "codex_home": env.get("CODEX_HOME") or str(Path(home) / ".codex"),
        "xdg_config_home": env.get("XDG_CONFIG_HOME") or str(Path(home) / ".config"),
        "claude_config_dir": env.get("CLAUDE_CONFIG_DIR") or str(Path(home) / ".claude"),
        "environ": env,
    }


def _expand_candidate(pattern, home, cwd, environ):
    roots = [Path(home)]
    for name in ("USERPROFILE", "HOME"):
        value = environ.get(name) if environ else None
        if not value:
            continue
        candidate = Path(value)
        if _normalise_path(candidate) not in {_normalise_path(item) for item in roots}:
            roots.append(candidate)

    results = []
    skipped = None
    for root in roots:
        values = _environment(environ, root)
        values["cwd"] = str(cwd)

        def replace(match, values=values):
            token = match.group(1)
            if token in values and token != "environ":
                return values[token]
            if token.startswith("env:"):
                return values["environ"].get(token[4:], "")
            return match.group(0)

        expanded = re.sub(r"\{([^{}]+)\}", replace, pattern)
        if re.search(r"\{[^{}]+\}", expanded):
            skipped = "unresolved-placeholder:" + pattern
            continue
        if any(char in expanded for char in "*?["):
            results.extend(Path(item) for item in glob.glob(expanded, recursive=True))
        else:
            results.append(Path(expanded))
    if not results and skipped:
        return [], skipped
    return sorted(set(results), key=lambda item: _normalise_path(item)), None


def _normalise_path(path):
    try:
        return str(Path(path).resolve())
    except OSError:
        return str(path)


def _excluded(path, patterns):
    text = str(path).replace("\\", "/")
    return any(fnmatch.fnmatch(text, pattern.replace("\\", "/")) for pattern in patterns)


def _strip_jsonc_comments(text):
    out = []
    index = 0
    in_string = False
    quote = ""
    escaped = False
    while index < len(text):
        char = text[index]
        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                in_string = False
            index += 1
            continue
        if char in ('"', "'"):
            in_string = True
            quote = char
            out.append(char)
            index += 1
            continue
        if char == "/" and index + 1 < len(text) and text[index + 1] == "/":
            index += 2
            while index < len(text) and text[index] not in "\r\n":
                index += 1
            continue
        if char == "/" and index + 1 < len(text) and text[index + 1] == "*":
            index += 2
            while index + 1 < len(text) and not (text[index] == "*" and text[index + 1] == "/"):
                index += 1
            index += 2
            continue
        out.append(char)
        index += 1
    return "".join(out)


def _strip_jsonc_trailing_commas(text):
    out = []
    index = 0
    in_string = False
    quote = ""
    escaped = False
    while index < len(text):
        char = text[index]
        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                in_string = False
            index += 1
            continue
        if char in ('"', "'"):
            in_string = True
            quote = char
            out.append(char)
            index += 1
            continue
        if char == ",":
            lookahead = index + 1
            while lookahead < len(text) and text[lookahead].isspace():
                lookahead += 1
            if lookahead < len(text) and text[lookahead] in "}]":
                index += 1
                continue
        out.append(char)
        index += 1
    return "".join(out)


def _strip_jsonc(text):
    return _strip_jsonc_trailing_commas(_strip_jsonc_comments(text))


def _collect_json_servers(payload, keys):
    if not isinstance(payload, dict):
        return [], "", "top-level-json-value-is-not-an-object"
    names = set()
    used = []
    for key in keys:
        if key not in payload:
            continue
        value = payload.get(key)
        if not isinstance(value, dict):
            return [], key, "mcp-key-is-not-an-object"
        used.append(key)
        if key == "mcp" and isinstance(value.get("servers"), dict):
            names.update(str(name) for name in value["servers"].keys())
        else:
            names.update(str(name) for name in value.keys())
    return sorted(names), ",".join(used), None


def _parse_toml_servers(text):
    names = set()
    section = None
    inline_value = False
    saw_root = False
    header_re = re.compile(
        r"^\s*\[\s*mcp_servers\s*\.\s*(?:\"([^\"]+)\"|'([^']+)'|([A-Za-z0-9_.-]+))\s*\]\s*(?:#.*)?$"
    )
    root_re = re.compile(r"^\s*\[\s*mcp_servers\s*\]\s*(?:#.*)?$")
    for line in text.splitlines():
        match = header_re.match(line)
        if match:
            names.add(next(group for group in match.groups() if group is not None))
            section = "child"
            continue
        if root_re.match(line):
            saw_root = True
            section = "root"
            continue
        if section == "root" and re.match(r"^\s*[A-Za-z0-9_.-]+\s*=", line):
            inline_value = True
    if inline_value:
        return [], "mcp_servers", "toml-inline-mcp-servers-not-supported"
    if names:
        return sorted(names), "mcp_servers", None
    if saw_root:
        return [], "mcp_servers", None
    return [], "", None


def _parse_config(path, fmt, keys, max_bytes):
    try:
        size = path.stat().st_size
    except OSError as exc:
        return {"ok": False, "kind": "error", "reason": "%s: %s" % (path, exc)}
    if size > max_bytes:
        return {
            "ok": False,
            "kind": "unsupported",
            "reason": "%s: file exceeds max_config_bytes=%d" % (path, max_bytes),
        }
    try:
        text = _read_text(path)
    except (OSError, ValueError) as exc:
        return {"ok": False, "kind": "error", "reason": "%s: %s" % (path, exc)}
    suffix = path.suffix.lower()
    if fmt in ("yaml", "yml") or suffix in (".yaml", ".yml"):
        return {"ok": False, "kind": "unsupported", "reason": "%s: yaml-not-supported" % path}
    if fmt == "toml" or suffix == ".toml":
        servers, key, reason = _parse_toml_servers(text)
        if reason:
            return {"ok": False, "kind": "unsupported", "reason": "%s: %s" % (path, reason)}
        return {"ok": True, "format": "toml", "key": key, "servers": servers}
    if fmt == "jsonc" or suffix == ".jsonc":
        text = _strip_jsonc(text)
        parse_format = "jsonc"
    else:
        parse_format = "json"
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "kind": "error",
            "reason": "%s: json parse error at line %d column %d: %s" % (
                path, exc.lineno, exc.colno, exc.msg),
        }
    servers, key, reason = _collect_json_servers(payload, keys)
    if reason:
        return {"ok": False, "kind": "unsupported", "reason": "%s: %s" % (path, reason)}
    return {"ok": True, "format": parse_format, "key": key, "servers": servers}


def _read_json_array_or_pathsep(value):
    if not value:
        return []
    text = str(value).strip()
    if text.startswith("["):
        try:
            payload = json.loads(text)
            return [str(item) for item in payload] if isinstance(payload, list) else []
        except json.JSONDecodeError:
            return []
    return [item for item in text.split(os.pathsep) if item]


def _custom_hosts(environ, home, cwd):
    hosts = []
    registry_path = environ.get("YOTTA_DEV_MCP_CONFIG_REGISTRY")
    if registry_path:
        path = Path(registry_path)
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            payload = None
        if isinstance(payload, dict) and isinstance(payload.get("hosts"), list):
            for index, item in enumerate(payload["hosts"]):
                if not isinstance(item, dict) or not item.get("id"):
                    continue
                hosts.append(_host(
                    str(item["id"]),
                    str(item.get("label") or item["id"]),
                    [str(value) for value in item.get("candidates", [])],
                    formats=item.get("formats") or ("json",),
                    server_keys=item.get("server_keys") or DEFAULT_JSON_KEYS,
                    tier="custom",
                    note=str(item.get("note") or "custom-registry"),
                ))
    extra = _read_json_array_or_pathsep(environ.get("YOTTA_DEV_MCP_CONFIG_PATHS"))
    if extra:
        hosts.append(_host("custom-paths", "Custom config paths", extra, tier="custom",
                           note="from YOTTA_DEV_MCP_CONFIG_PATHS"))
    return hosts


def _custom_skill_hosts(environ):
    extra = _read_json_array_or_pathsep(environ.get("YOTTA_DEV_MCP_SKILL_DIRS"))
    if not extra:
        return []
    return [_host("custom-skills", "Custom skill paths", extra, tier="custom",
                  note="from YOTTA_DEV_MCP_SKILL_DIRS")]


def default_config_paths(home=None, cwd=None, environ=None):
    home = Path(home) if home is not None else Path.home()
    cwd = Path(cwd) if cwd is not None else Path.cwd()
    environ = dict(environ if environ is not None else os.environ)
    paths = []
    for host in _builtin_hosts():
        for pattern in host["candidates"]:
            expanded, _ = _expand_candidate(pattern, home, cwd, environ)
            paths.extend(expanded)
    return sorted(set(paths), key=lambda item: str(item))


def default_skill_dirs(home=None, cwd=None, environ=None):
    home = Path(home) if home is not None else Path.home()
    cwd = Path(cwd) if cwd is not None else Path.cwd()
    environ = dict(environ if environ is not None else os.environ)
    paths = []
    for host in _builtin_skill_hosts():
        for pattern in host["candidates"]:
            expanded, _ = _expand_candidate(pattern, home, cwd, environ)
            paths.extend(expanded)
    return sorted(set(paths), key=lambda item: str(item))


def _scan_skills(hosts, home, cwd, environ, max_skill_dirs):
    skills = []
    coverage = []
    seen = {}
    for host in hosts:
        found = []
        candidate_paths = []
        skipped = []
        for pattern in host["candidates"]:
            expanded, reason = _expand_candidate(pattern, home, cwd, environ)
            if reason:
                skipped.append(reason)
                continue
            for path in expanded:
                candidate_paths.append(_normalise_path(path))
                if path.is_dir():
                    found.append(path)
        for root in found[:max_skill_dirs]:
            try:
                children = sorted(root.iterdir(), key=lambda item: item.name)
            except OSError:
                continue
            for child in children:
                skill_file = child / "SKILL.md"
                if not child.is_dir() or not skill_file.is_file():
                    continue
                try:
                    text = _read_text(skill_file)
                except (OSError, ValueError):
                    continue
                key = _normalise_path(skill_file)
                entry = seen.get(key)
                if entry is None:
                    entry = {
                        "name": _frontmatter_name(text) or child.name,
                        "version": _frontmatter_version(text),
                        "path": key,
                        "hosts": [host["id"]],
                    }
                    seen[key] = entry
                    skills.append(entry)
                elif host["id"] not in entry["hosts"]:
                    entry["hosts"].append(host["id"])
        if found:
            status = "checked"
        elif skipped:
            status = "missing"
        elif host["tier"] == "unverified":
            status = "unverified"
        else:
            status = "missing"
        coverage.append({
            "host": host["id"],
            "label": host["label"],
            "tier": host["tier"],
            "status": status,
            "candidate_paths": sorted(set(candidate_paths)),
            "checked_paths": sorted(set(_normalise_path(path) for path in found)),
            "count": sum(1 for item in seen.values() if host["id"] in item["hosts"]),
            "reason": host.get("note", ""),
        })
    return skills, coverage


def mcp_doctor(skills_dirs=None, config_paths=None, include_defaults=None,
               home=None, cwd=None, environ=None, max_configs=DEFAULT_MAX_CONFIGS,
               max_config_bytes=DEFAULT_MAX_CONFIG_BYTES, include_unverified=True):
    home = Path(home) if home is not None else Path.home()
    cwd = Path(cwd) if cwd is not None else Path.cwd()
    environ = dict(environ if environ is not None else os.environ)

    config_scope = "default"
    skills_scope = "default"
    default_coverage_skipped = False

    if skills_dirs:
        skill_hosts = [_host("explicit", "Explicit skill dirs", [str(item) for item in skills_dirs],
                             tier="custom", note="from skills_dirs")]
        skills_scope = "explicit"
    else:
        skill_hosts = _builtin_skill_hosts() + _custom_skill_hosts(environ)

    if config_paths and include_defaults is not True:
        hosts = [_host("explicit", "Explicit config paths", [str(item) for item in config_paths],
                       formats=("json", "jsonc", "toml", "yaml"),
                       server_keys=DEFAULT_JSON_KEYS + DEFAULT_TOML_KEYS,
                       tier="custom", note="from config_paths")]
        config_scope = "explicit"
        default_coverage_skipped = True
    else:
        hosts = _builtin_hosts() + _custom_hosts(environ, home, cwd)
        if config_paths:
            hosts.append(_host("explicit", "Explicit config paths",
                               [str(item) for item in config_paths],
                               formats=("json", "jsonc", "toml", "yaml"),
                               server_keys=DEFAULT_JSON_KEYS + DEFAULT_TOML_KEYS,
                               tier="custom", note="from config_paths"))
            config_scope = "default+explicit"

    if not include_unverified:
        hosts = [host for host in hosts if host["tier"] != "unverified"]

    configs = []
    coverage = []
    issues = []
    coverage_gaps = []
    seen_paths = {}
    for host in hosts:
        checked = []
        unsupported = []
        errors = []
        candidate_paths = []
        skipped = []
        seen_host_paths = set()
        for pattern in host["candidates"]:
            expanded, reason = _expand_candidate(pattern, home, cwd, environ)
            if reason:
                skipped.append(reason)
                continue
            for path in expanded:
                if _excluded(path, host.get("exclude", ())):
                    continue
                candidate_paths.append(_normalise_path(path))
                if not path.is_file():
                    continue
                normalised = _normalise_path(path)
                if normalised in seen_host_paths:
                    continue
                seen_host_paths.add(normalised)
                if len(checked) + len(unsupported) + len(errors) >= max_configs:
                    break
                formats = host["formats"] or ("json",)
                selected = formats[0] if len(formats) == 1 else None
                parsed = _parse_config(path, selected, host["server_keys"], max_config_bytes)
                if parsed.get("ok"):
                    item = {
                        "host": host["id"],
                        "path": _normalise_path(path),
                        "format": parsed["format"],
                        "key": parsed.get("key", ""),
                        "servers": parsed.get("servers", []),
                    }
                    key = item["path"]
                    existing = seen_paths.get(key)
                    if existing is None:
                        seen_paths[key] = item
                        configs.append(item)
                    elif host["id"] not in existing.get("also_hosts", []):
                        existing.setdefault("also_hosts", []).append(host["id"])
                    checked.append(item)
                elif parsed.get("kind") == "unsupported":
                    unsupported.append(parsed["reason"])
                    issues.append(parsed["reason"])
                else:
                    errors.append(parsed["reason"])
                    issues.append(parsed["reason"])
        if checked and not unsupported and not errors:
            status = "checked"
        elif checked:
            status = "checked-with-gaps"
        elif unsupported:
            status = "unsupported"
        elif errors:
            status = "error"
        elif skipped:
            status = "missing"
        elif host["tier"] == "unverified":
            status = "unverified"
        else:
            status = "missing"
        coverage.append({
            "host": host["id"],
            "label": host["label"],
            "tier": host["tier"],
            "status": status,
            "candidate_paths": sorted(set(candidate_paths)),
            "checked_paths": sorted(set(item["path"] for item in checked)),
            "unsupported_paths": sorted(set(item.split(":", 1)[0] for item in unsupported)),
            "error_paths": sorted(set(item.split(":", 1)[0] for item in errors)),
            "configs": checked,
            "servers": sorted(set(name for item in checked for name in item["servers"])),
            "reason": unsupported[0] if unsupported else (errors[0] if errors else host.get("note", "")),
        })
        if status == "unverified":
            coverage_gaps.append("%s: config path/format not verified" % host["id"])
        if unsupported or errors:
            coverage_gaps.append("%s: unsupported or unreadable config file(s)" % host["id"])
        if skipped and host["tier"] in ("unverified", "custom"):
            coverage_gaps.append("%s: skipped candidates (%s)" % (host["id"], ", ".join(skipped)))

    skills, skills_coverage = _scan_skills(skill_hosts, home, cwd, environ, DEFAULT_MAX_SKILL_DIRS)
    for entry in skills_coverage:
        if entry["status"] == "unverified":
            coverage_gaps.append("skills/%s: skill directory not verified" % entry["host"])

    configs.sort(key=lambda item: item["path"])
    coverage.sort(key=lambda item: item["host"])
    skills.sort(key=lambda item: (item["name"], item["path"]))
    skills_coverage.sort(key=lambda item: item["host"])
    issues = sorted(set(issues))
    coverage_gaps = sorted(set(coverage_gaps))

    counts = {
        "checked_hosts": sum(1 for item in coverage if item["status"].startswith("checked")),
        "missing_hosts": sum(1 for item in coverage if item["status"] == "missing"),
        "unsupported_hosts": sum(1 for item in coverage if item["status"] == "unsupported"),
        "error_hosts": sum(1 for item in coverage if item["status"] == "error"),
        "unverified_hosts": sum(1 for item in coverage if item["status"] == "unverified"),
    }
    unknown_hosts = [item["host"] for item in coverage if item["status"] == "unverified"]
    checked_scope_clear = not issues and not counts["unsupported_hosts"] and not counts["error_hosts"]
    full_coverage = not unknown_hosts and config_scope == "default" and not coverage_gaps
    all_clear = bool(full_coverage and checked_scope_clear)
    summary = dict(counts)
    summary.update({
        "hosts_total": len(coverage),
        "configs_found": len(configs),
        "servers_total": len(set(name for item in configs for name in item["servers"])),
        "all_clear": all_clear,
        "checked_scope_clear": checked_scope_clear,
        "full_coverage": full_coverage,
        "coverage_confidence": "full" if full_coverage else "partial",
        "issues": len(issues),
    })
    return {
        "skills": skills,
        "mcp_configs": configs,
        "coverage": coverage,
        "skills_coverage": skills_coverage,
        "unknown_hosts": sorted(unknown_hosts),
        "coverage_gaps": coverage_gaps,
        "issues": issues,
        "summary": summary,
        "scope": config_scope,
        "skills_scope": skills_scope,
        "default_coverage_skipped": default_coverage_skipped,
        "checked_skills": len(skills),
        "checked_configs": len(configs),
        "checked_hosts": counts["checked_hosts"],
    }
