#!/usr/bin/env python3
"""skillgate-mcp — MCP Server for SkillGate

Exposes SkillGate as MCP tools so AI agents can call it directly.

SECURITY BOUNDARY: this server performs static scanning only — it imports
and calls SkillGate's in-process scan functions; it never spawns subprocesses,
never executes scanned code, and makes no network requests.

Usage (in your MCP config):
    "skillgate": {
      "command": "python",
      "args": ["/path/to/skillgate-mcp.py"]
    }
"""
from __future__ import annotations

import dataclasses
import json
import sys
from pathlib import Path

# In-process imports (no subprocess)
sys.path.insert(0, str(Path(__file__).parent))
import skillgate  # noqa: E402
import skillbench  # noqa: E402


def _scan_result_to_dict(result) -> dict:
    d = dataclasses.asdict(result)
    d["trust_score"] = result.trust_score
    d["grade"] = result.grade
    d["critical_count"] = result.critical_count
    d["high_count"] = result.high_count
    return d


def send_message(msg: dict):
    """Send a JSON-RPC message over stdout."""
    print(json.dumps(msg), flush=True)


def handle_initialize(params: dict) -> dict:
    """Handle initialize request."""
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {}
        },
        "serverInfo": {
            "name": "skillgate",
            "version": "0.1.0"
        }
    }


def handle_tools_list(params: dict) -> dict:
    """Handle tools/list request."""
    return {
        "tools": [
            {
                "name": "scan_skill",
                "description": "Scan an AI agent skill for security issues and get a Trust Score. "
                               "Use this BEFORE installing or publishing any skill. "
                               "Returns a 0-100 trust score, grade, and list of findings.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "skill_dir": {
                            "type": "string",
                            "description": "Path to the skill directory to scan"
                        },
                        "fail_under": {
                            "type": "integer",
                            "description": "Optional: fail if trust score is below this threshold (e.g. 90)",
                            "default": None
                        }
                    },
                    "required": ["skill_dir"]
                }
            },
            {
                "name": "bench_skill",
                "description": "Run capability benchmarks on a skill to verify it actually works. "
                               "Use this after security scan to confirm the skill functions correctly.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "skill_dir": {
                            "type": "string",
                            "description": "Path to the skill directory to benchmark"
                        }
                    },
                    "required": ["skill_dir"]
                }
            }
        ]
    }


def handle_tools_call(params: dict) -> dict:
    """Handle tools/call request."""
    tool_name = params.get("name")
    args = params.get("arguments", {})

    if tool_name == "scan_skill":
        skill_dir = args.get("skill_dir", "")
        fail_under = args.get("fail_under")
        try:
            result = skillgate.scan_skill(skill_dir)
            out = _scan_result_to_dict(result)
            findings = []
            for f in out.get("findings", []):
                findings.append({
                    "severity": f.get("severity"),
                    "category": f.get("category"),
                    "message": f.get("message"),
                    "file": f.get("file"),
                    "line": f.get("line"),
                })
            out["findings"] = findings
            # Enforce the advertised security threshold: when fail_under is
            # provided and the trust score falls below it, the call FAILS.
            # The threshold is never silently ignored.
            if fail_under is not None:
                try:
                    threshold = int(fail_under)
                except (TypeError, ValueError):
                    return {
                        "content": [{"type": "text", "text": json.dumps(
                            {"error": f"fail_under 必须是整数，收到: {fail_under!r}"},
                            ensure_ascii=False)}],
                        "isError": True,
                    }
                if result.trust_score < threshold:
                    return {
                        "content": [{"type": "text", "text": json.dumps(
                            {"error": f"Trust Score {result.trust_score} 低于阈值 {threshold}，拒绝通过",
                             "trust_score": result.trust_score,
                             "fail_under": threshold,
                             "grade": result.grade}, ensure_ascii=False)}],
                        "isError": True,
                    }
            text = json.dumps(out, indent=2, ensure_ascii=False)
            return {"content": [{"type": "text", "text": text}]}
        except Exception as e:
            return {
                "content": [{"type": "text", "text": json.dumps({"error": str(e)}, ensure_ascii=False)}],
                "isError": True,
            }

    elif tool_name == "bench_skill":
        skill_dir = args.get("skill_dir", "")
        skill_name, tests = skillbench.resolve_tests(skill_dir)
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "skill": skill_name,
                        "dry_run": True,
                        "tests": tests,
                        "note": "dry-run preview only; execution happens in the repository tests/ pytest suite"
                    }, indent=2, ensure_ascii=False)
                }
            ]
        }

    else:
        return {
            "content": [{"type": "text", "text": f"Unknown tool: {tool_name}"}],
            "isError": True
        }


def main():
    """Main MCP server loop: read JSON-RPC from stdin, write responses to stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = msg.get("method", "")
        msg_id = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            result = handle_initialize(params)
        elif method == "tools/list":
            result = handle_tools_list(params)
        elif method == "tools/call":
            result = handle_tools_call(params)
        elif method == "notifications/initialized":
            # Just acknowledge, no response needed
            continue
        else:
            result = {"error": f"Unknown method: {method}"}

        response = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": result
        }
        send_message(response)


if __name__ == "__main__":
    main()
