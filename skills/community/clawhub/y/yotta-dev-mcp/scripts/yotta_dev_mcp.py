#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta-dev-mcp — deterministic development tools exposed over stdio MCP.

Protocol support is dual-era:
  * modern: MCP 2026-07-28, server/discover + per-request _meta
  * legacy: initialize handshake with protocolVersion 2025-11-25

Tools are local, deterministic and read-only unless a tool explicitly documents
an opt-in write or an explicit execution flag.
"""

import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import dev_engine as engine  # noqa: E402

VERSION = engine.VERSION
TOOL_NAME = "yotta-dev-mcp"
MCP_PROTOCOL_MODERN = "2026-07-28"
MCP_PROTOCOL_LEGACY = "2025-11-25"
SERVER_INFO = {"name": TOOL_NAME, "version": VERSION}

# 工具分组（v0.2.2）：与元忆 `--tools core|full` 同口径。core 是给「需要在上下文里
# 常驻工具表」的宿主用小档（5 工具，schema 远低于 8000 字符硬上限）；full 保持 18 工具。
CORE_TOOL_NAMES = (
    "repo_map",
    "find_code",
    "review_code",
    "review_diff",
    "verify_change",
)
TOOL_PROFILES = ("core", "full")
DEFAULT_TOOL_PROFILE = "full"


def normalize_tool_profile(value):
    profile = str(value or "").strip().lower() or DEFAULT_TOOL_PROFILE
    if profile not in TOOL_PROFILES:
        raise ValueError("未知工具分组: %s（可用: core / full）" % value)
    return profile


def _text_result(payload):
    return {
        "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)}],
        "isError": False,
    }


def _tool_error(message):
    return {
        "content": [{"type": "text", "text": str(message)}],
        "isError": True,
    }


def _tool(name, arguments):
    try:
        result = engine.dispatch(name, arguments)
    except Exception as exc:  # noqa: BLE001
        return _tool_error("%s 失败: %s" % (name, exc))
    if name == "compress_output" and isinstance(result, dict):
        return {
            "content": [{"type": "text", "text": result.get("text", "")}],
            "isError": False,
        }
    return _text_result(result)


TOOL_HANDLERS = {
    name: (lambda arguments, tool_name=name: _tool(tool_name, arguments))
    for name in ("repo_map", "system_model", "architecture_review", "impact_analysis",
                 "verify_change", "self_test", "run_adapter", "find_code", "compress_output",
                 "review_code", "review_diff", "mcp_doctor",
                 "scan_secrets", "scan_dependencies", "check_publish_readiness",
                 "run_checks", "scaffold_skill", "workflow_state")
}


def _all_tools():
    return [
        {
            "name": "repo_map",
            "description": (
                "Map a local repository's source modules, imports and entrypoints. "
                "Use when starting work in an unfamiliar codebase or when you need a "
                "small structural overview before editing."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository or source directory"},
                    "max_files": {"type": "integer", "minimum": 1,
                                  "description": "Maximum source files to inspect (default 2000)"},
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "system_model",
            "description": (
                "Build a deterministic system model (modules, imports, entrypoints, "
                "tests, configs, data stores) and attach layer data from the "
                ".yotta/architecture.json contract. Returns PASS, FAIL or UNKNOWN "
                "plus the unknowns that still need evidence. Read-only."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository or source directory"},
                    "max_files": {"type": "integer", "minimum": 1,
                                  "description": "Maximum source files to inspect (default 2000)"},
                    "contract_file": {
                        "type": "string",
                        "description": "Contract path relative to the repository root "
                                       "(default .yotta/architecture.json)",
                    },
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "architecture_review",
            "description": (
                "Review a local repository against the .yotta/architecture.json contract: "
                "dependency rules, boundary visibility and data ownership, each finding "
                "with file, line and severity. critical/high findings fail the review; "
                "medium/low are advisory; unverifiable items become UNKNOWN. Read-only."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository or source directory"},
                    "max_files": {"type": "integer", "minimum": 1,
                                  "description": "Maximum source files to inspect (default 2000)"},
                    "contract_file": {
                        "type": "string",
                        "description": "Contract path relative to the repository root "
                                       "(default .yotta/architecture.json)",
                    },
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "impact_analysis",
            "description": (
                "Build the change impact cone for local changes: reverse-dependency "
                "consumers, affected layers, boundaries, data stores and invariants, "
                "mapped tests, an explainable blast radius and rollback probes. Accepts "
                "changed_files, a unified diff or target symbols. Read-only."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository or source directory"},
                    "changed_files": {
                        "type": "array", "items": {"type": "string"},
                        "description": "Repository-relative changed files",
                    },
                    "diff": {"type": "string",
                             "description": "Unified diff text to read changed files from"},
                    "symbols": {
                        "type": "array", "items": {"type": "string"},
                        "description": "Target symbols; their definition sites become the change",
                    },
                    "depth": {"type": "integer", "minimum": 1, "maximum": 10,
                              "description": "Reverse-dependency depth (default 3)"},
                    "max_files": {"type": "integer", "minimum": 1,
                                  "description": "Maximum source files to inspect (default 2000)"},
                    "contract_file": {
                        "type": "string",
                        "description": "Contract path relative to the repository root "
                                       "(default .yotta/architecture.json)",
                    },
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "verify_change",
            "description": (
                "Run the L0-L5 verification ladder for a local change and return "
                "a deterministic evidence ledger. L0 syntax/contract and L1 "
                "architecture checks run by default; L2-L4 require a whitelisted "
                ".yotta/verification.json check plus allow_execute=true. L5 is "
                "always recorded as manual work. Read-only unless execution is "
                "explicitly enabled."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository or source directory"},
                    "changed_files": {
                        "type": "array", "items": {"type": "string"},
                        "description": "Repository-relative changed files",
                    },
                    "diff": {"type": "string",
                             "description": "Unified diff text to read changed files from"},
                    "symbols": {
                        "type": "array", "items": {"type": "string"},
                        "description": "Target symbols; their definition sites become the change",
                    },
                    "depth": {"type": "integer", "minimum": 1, "maximum": 10,
                              "description": "Reverse-dependency depth (default 3)"},
                    "levels": {
                        "type": "array",
                        "items": {"enum": ["L0", "L1", "L2", "L3", "L4", "L5"]},
                        "description": "Additional verification levels; L2-L4 require "
                                       "a policy and explicit execution",
                    },
                    "allow_execute": {
                        "type": "boolean",
                        "description": "Must be true to run whitelisted policy checks; default false",
                    },
                    "timeout": {"type": "integer", "minimum": 1, "maximum": 600,
                                "description": "Upper bound for each check in seconds (default 120)"},
                    "max_files": {"type": "integer", "minimum": 1,
                                  "description": "Maximum source files to inspect (default 2000)"},
                    "contract_file": {
                        "type": "string",
                        "description": "Contract path relative to the repository root "
                                       "(default .yotta/architecture.json)",
                    },
                    "policy_file": {
                        "type": "string",
                        "description": "Verification policy path relative to the repository root "
                                       "(default .yotta/verification.json)",
                    },
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "self_test",
            "description": (
                "Run deterministic integrity checks on yotta-dev-mcp itself: "
                "required files, version alignment, protocol/tool schema drift, "
                "fail-closed write gates and seeded-defect counterexamples. Use "
                "installed mode for a skill copy and source mode for the checkout. "
                "Test-suite execution requires allow_execute=true; read-only by default."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string",
                             "description": "Source checkout or installed skill directory"},
                    "mode": {
                        "type": "string",
                        "enum": ["auto", "source", "installed"],
                        "description": "auto detects source vs installed layout",
                    },
                    "allow_execute": {
                        "type": "boolean",
                        "description": "Run the project test suite; default false",
                    },
                    "timeout": {"type": "integer", "minimum": 1, "maximum": 600,
                                "description": "Test timeout in seconds (default 120)"},
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "run_adapter",
            "description": (
                "Probe or explicitly run an optional local architecture adapter. "
                "action=list only inspects project-local node_modules/.bin, venv and "
                "PATH for import-linter, dependency-cruiser and Repomix; action=run "
                "requires allow_execute=true. The adapter never installs packages, "
                "downloads files or accepts arbitrary argv. Missing tools or configs "
                "return UNKNOWN with the next step."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "action": {
                        "type": "string",
                        "enum": ["list", "run"],
                        "description": "list probes capability; run executes one adapter",
                    },
                    "path": {"type": "string", "description": "Repository root"},
                    "adapter": {
                        "type": "string",
                        "enum": ["import-linter", "dependency-cruiser", "repomix"],
                        "description": "Adapter id; required when action=run",
                    },
                    "allow_execute": {
                        "type": "boolean",
                        "description": "Must be true to run an adapter; default false",
                    },
                    "timeout": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 600,
                        "description": "Adapter timeout in seconds (default 120)",
                    },
                    "max_chars": {
                        "type": "integer",
                        "minimum": 1000,
                        "maximum": 1000000,
                        "description": "Repomix output cap in characters (default 120000)",
                    },
                    "token_budget": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 500000,
                        "description": "Optional Repomix token budget",
                    },
                    "target": {
                        "type": "string",
                        "description": "Repository-relative adapter target (default .)",
                    },
                },
                "required": ["action", "path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "find_code",
            "description": (
                "Find a symbol, definition or text in local source files with bounded "
                "results. Use when locating where a function, class or string lives."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository, file or directory"},
                    "query": {"type": "string", "description": "Symbol or text to find"},
                    "extensions": {"type": "array", "items": {"type": "string"},
                                   "description": "Optional file extensions such as .py or .ts"},
                    "max_results": {"type": "integer", "minimum": 1,
                                    "description": "Maximum matches (default 100)"},
                    "context_lines": {"type": "integer", "minimum": 0, "maximum": 5,
                                      "description": "Context lines around each match"},
                },
                "required": ["path", "query"],
                "additionalProperties": False,
            },
        },
        {
            "name": "compress_output",
            "description": (
                "Compress long logs or command output while preserving errors, "
                "tracebacks, warnings, head and tail lines. Use before putting long "
                "tool output into the context window."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to compress"},
                    "file": {"type": "string", "description": "Read text from this file instead"},
                    "max_chars": {"type": "integer", "minimum": 20,
                                  "description": "Output character budget (default 4000)"},
                    "head_lines": {"type": "integer", "minimum": 0},
                    "tail_lines": {"type": "integer", "minimum": 0},
                },
                "additionalProperties": False,
            },
        },
        {
            "name": "review_code",
            "description": (
                "Run deterministic local code review rules and return evidence with "
                "file, line, rule, severity and suggestion. Use for a focused review "
                "before commit or PR."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File or repository path"},
                    "text": {"type": "string", "description": "Review this text instead"},
                    "max_findings": {"type": "integer", "minimum": 1},
                },
                "additionalProperties": False,
            },
        },
        {
            "name": "review_diff",
            "description": (
                "Review only added lines in a git diff or unified diff. Use when "
                "reviewing a patch or before opening a pull request."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "diff_text": {"type": "string", "description": "Unified diff content"},
                    "path": {"type": "string", "description": "Git repository path"},
                    "base": {"type": "string", "description": "Optional git base revision"},
                    "max_findings": {"type": "integer", "minimum": 1},
                },
                "additionalProperties": False,
            },
        },
        {
            "name": "mcp_doctor",
            "description": (
                "Broad, read-only health check for installed skills and MCP client "
                "configuration. Discovers Codex, Cursor, WorkBuddy, OpenCode, Claude "
                "Code and other known hosts (plus project-level configs), parses JSON, "
                "JSONC and a narrow TOML subset, and always returns a coverage report "
                "with checked / missing / unsupported / unverified hosts. Only server "
                "names are returned; commands, args and env values are never included. "
                "A clean result applies only to the covered scope: read coverage and "
                "coverage_confidence before treating it as all-clear."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "skills_dirs": {"type": "array", "items": {"type": "string"}},
                    "config_paths": {"type": "array", "items": {"type": "string"}},
                    "include_defaults": {
                        "type": "boolean",
                        "description": "Also scan the built-in host registry when config_paths is supplied",
                    },
                },
                "additionalProperties": False,
            },
        },
        {
            "name": "scan_secrets",
            "description": (
                "Scan local source, configuration and env files for credentials "
                "and high-entropy tokens, returning redacted evidence. Use before "
                "commit, publishing or sharing a repository."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File or repository path"},
                    "text": {"type": "string", "description": "Scan this text instead"},
                    "max_findings": {"type": "integer", "minimum": 1},
                    "include_git_history": {"type": "boolean", "description": "Also scan bounded git history; default false"},
                },
                "additionalProperties": False,
            },
        },
        {
            "name": "scan_dependencies",
            "description": (
                "Inspect local dependency manifests and lockfiles for missing "
                "locks, unpinned ranges, insecure sources and local-only paths. "
                "Offline heuristic only; no package-existence lookup."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Repository path"},
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "check_publish_readiness",
            "description": (
                "Check a local package or skill for version alignment, required "
                "release files, repository metadata and public publish access. "
                "Use before tagging or publishing."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Package or skill directory"},
                },
                "required": ["path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "run_checks",
            "description": (
                "Run a whitelisted test, lint or compile check in a local project "
                "and return a bounded structured summary. Execution is explicit: "
                "use only when the user asks to run checks."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "kind": {
                        "type": "string",
                        "enum": ["python-unittest", "pytest", "python-compile", "npm-test", "npm-lint"],
                    },
                    "cwd": {"type": "string", "description": "Project directory"},
                    "timeout": {"type": "integer", "minimum": 1, "maximum": 600},
                    "allow_execute": {"type": "boolean", "description": "Must be true; default false"},
                },
                "required": ["kind", "cwd"],
                "additionalProperties": False,
            },
        },
        {
            "name": "scaffold_skill",
            "description": (
                "Plan or create a minimal skill scaffold with SKILL.md, package.json, "
                "README, changelog and a starter script. Dry-run is the default."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Lower-case skill slug"},
                    "output_dir": {"type": "string", "description": "Parent output directory"},
                    "description": {"type": "string"},
                    "apply": {"type": "boolean", "description": "Write files; default false"},
                },
                "required": ["name", "output_dir"],
                "additionalProperties": False,
            },
        },
        {
            "name": "workflow_state",
            "description": (
                "Read .workflow state files and optionally append one log line with "
                "an explicit date. Use for session recovery and handoff checks."
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "root": {"type": "string", "description": "Project root"},
                    "action": {"type": "string", "enum": ["read", "append-log", "append-file"]},
                    "date": {"type": "string", "description": "YYYY-MM-DD for append-log"},
                    "text": {"type": "string"},
                    "file": {"type": "string", "enum": ["STATE.md", "TASKS.md", "DECISIONS.md", "ROADMAP.md"]},
                    "apply": {"type": "boolean", "description": "Write; default false"},
                },
                "required": ["root"],
                "additionalProperties": False,
            },
        },
    ]


def mcp_tools(profile=None):
    """按工具分档返回 tools/list 内容（core 5 个 / full 18 个）。"""
    tools = _all_tools()
    if normalize_tool_profile(profile) == "core":
        by_name = {tool["name"]: tool for tool in tools}
        return [by_name[name] for name in CORE_TOOL_NAMES]
    return tools


def _req_version(params):
    meta = (params or {}).get("_meta") or {}
    return meta.get("io.modelcontextprotocol/protocolVersion")


def _modern_ok(payload, cache=None):
    out = {"resultType": "complete"}
    out.update(payload)
    out["_meta"] = {"io.modelcontextprotocol/serverInfo": dict(SERVER_INFO)}
    if cache:
        out["ttlMs"] = cache[0]
        out["cacheScope"] = cache[1]
    return out


def _unsupported_version(rid, protocol_version):
    return {
        "jsonrpc": "2.0",
        "id": rid,
        "error": {
            "code": -32022,
            "message": "Unsupported protocol version",
            "data": {"supported": [MCP_PROTOCOL_MODERN], "requested": protocol_version},
        },
    }


def handle_message(msg, tool_profile=None):
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0":
        rid = msg.get("id") if isinstance(msg, dict) else None
        return {"jsonrpc": "2.0", "id": rid,
                "error": {"code": -32600, "message": "invalid request"}}
    method = msg.get("method")
    rid = msg.get("id")
    if rid is None or method is None:
        return None
    params = msg.get("params") or {}
    protocol_version = _req_version(params)
    if protocol_version is not None:
        if protocol_version != MCP_PROTOCOL_MODERN:
            return _unsupported_version(rid, protocol_version)
        if method == "server/discover":
            return {
                "jsonrpc": "2.0",
                "id": rid,
                "result": _modern_ok({
                    "supportedVersions": [MCP_PROTOCOL_MODERN],
                    "capabilities": {"tools": {}},
                    "instructions": (
                        "yotta-dev-mcp exposes deterministic local development tools. "
                        "Prefer repo_map/find_code before editing, review_diff before PR, "
                        "review_code for focused review, compress_output for long logs and "
                        "mcp_doctor for local configuration checks. Use system_model and "
                        "architecture_review for architecture contracts, impact_analysis and "
                        "verify_change for change-centered evidence, self_test for integrity "
                        "checks, and run_adapter to probe or explicitly run optional local "
                        "architecture adapters. Tools are offline and read-only unless an "
                        "explicit write or execute flag is set. Current tool profile: "
                        + normalize_tool_profile(tool_profile)
                        + " (start with --tools core|full)."
                    ),
                }, (3600000, "public")),
            }
        if method == "ping":
            return {"jsonrpc": "2.0", "id": rid, "result": _modern_ok({})}
        if method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": rid,
                "result": _modern_ok({"tools": mcp_tools(tool_profile)}, (300000, "public")),
            }
        if method == "tools/call":
            name = params.get("name")
            arguments = params.get("arguments") or {}
            if (normalize_tool_profile(tool_profile) == "core"
                    and name not in CORE_TOOL_NAMES):
                return {
                    "jsonrpc": "2.0",
                    "id": rid,
                    "result": _modern_ok(_tool_error(
                        "工具 %s 属于 full 分组，当前以 --tools core 启动。"
                        "需要完整工具集时请用 --tools full 重新启动。" % name)),
                }
            handler = TOOL_HANDLERS.get(name)
            if not handler:
                return {
                    "jsonrpc": "2.0",
                    "id": rid,
                    "result": _modern_ok(_tool_error("未知工具: %s" % name)),
                }
            return {"jsonrpc": "2.0", "id": rid, "result": _modern_ok(handler(arguments))}
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": rid,
                "error": {
                    "code": -32601,
                    "message": "initialize removed in MCP 2026-07-28; use server/discover",
                },
            }
        return {"jsonrpc": "2.0", "id": rid,
                "error": {"code": -32601, "message": "Method not found: " + str(method)}}

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": rid,
            "result": {
                "protocolVersion": MCP_PROTOCOL_LEGACY,
                "capabilities": {"tools": {}},
                "serverInfo": SERVER_INFO,
                "instructions": (
                    "yotta-dev-mcp exposes deterministic local development tools. "
                    "Current tool profile: %s (%d tools). Use --tools full to expose all tools."
                    % (normalize_tool_profile(tool_profile), len(mcp_tools(tool_profile)))
                ),
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": rid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid,
                "result": {"tools": mcp_tools(tool_profile)}}
    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if (normalize_tool_profile(tool_profile) == "core"
                and name not in CORE_TOOL_NAMES):
            return {"jsonrpc": "2.0", "id": rid, "result": _tool_error(
                "工具 %s 属于 full 分组，当前以 --tools core 启动。"
                "需要完整工具集时请用 --tools full 重新启动。" % name)}
        handler = TOOL_HANDLERS.get(name)
        if not handler:
            return {
                "jsonrpc": "2.0",
                "id": rid,
                "result": _tool_error("未知工具: %s" % name),
            }
        return {"jsonrpc": "2.0", "id": rid, "result": handler(arguments)}
    return {"jsonrpc": "2.0", "id": rid,
            "error": {"code": -32601, "message": "Method not found: " + str(method)}}


def parse_args(argv):
    """解析启动参数：`--tools core|full`（默认 full）、`--version`、`--help`。"""
    profile = DEFAULT_TOOL_PROFILE
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--tools":
            index += 1
            if index >= len(argv):
                sys.stderr.write("用法错误: --tools 需要一个值（core / full）\n")
                raise SystemExit(2)
            raw = argv[index]
        elif arg.startswith("--tools="):
            raw = arg.split("=", 1)[1]
        elif arg in ("--version", "-v"):
            print("%s %s" % (TOOL_NAME, VERSION))
            raise SystemExit(0)
        elif arg in ("--help", "-h"):
            print("用法: yotta-dev-mcp [--tools core|full]")
            print("  core: 5 工具（%s）" % " / ".join(CORE_TOOL_NAMES))
            print("  full: 18 工具（默认）")
            raise SystemExit(0)
        else:
            sys.stderr.write("用法错误: 未知参数 %s\n" % arg)
            raise SystemExit(2)
        try:
            profile = normalize_tool_profile(raw)
        except ValueError as exc:
            sys.stderr.write("用法错误: %s\n" % exc)
            raise SystemExit(2)
        index += 1
    return profile


def main():
    tool_profile = parse_args(sys.argv[1:])
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            response = {"jsonrpc": "2.0", "id": None,
                        "error": {"code": -32700, "message": "parse error"}}
        else:
            response = handle_message(message, tool_profile)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
