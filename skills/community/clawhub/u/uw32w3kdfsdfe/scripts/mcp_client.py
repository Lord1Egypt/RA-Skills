#!/usr/bin/env python3
"""
Generic MCP HTTP Client — Newegg PC Builder
============================================
Dynamically discovers and calls tools from an MCP endpoint.
No tool names or parameters are hard-coded; the LLM decides
which tool to use and how to fill parameters based on list_tools output.

Usage:
    python mcp_client.py list_tools
    python mcp_client.py call <tool_name> '<json_arguments>'
    python mcp_client.py call <tool_name> @args.json
    echo '{"question":"..."}' | python mcp_client.py call <tool_name> -

On Windows PowerShell, prefer single-quoted JSON (see skill doc) or @file / stdin
to avoid broken escaping with double quotes.
"""

import sys
import json
import os
import urllib.request
import urllib.error
import uuid

MCP_ENDPOINT = "https://apis.newegg.com/ex-mcp/endpoint/pcbuilder"
TIMEOUT = 30


# ── HTTP layer ────────────────────────────────────────────────────────────────

def _post(payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        MCP_ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read().decode("utf-8")

            # SSE stream: extract the last valid data: line
            if "text/event-stream" in content_type:
                last = None
                for line in raw.splitlines():
                    if line.startswith("data:"):
                        try:
                            last = json.loads(line[5:].strip())
                        except json.JSONDecodeError:
                            pass
                if last is None:
                    raise ValueError(f"No valid JSON in SSE stream:\n{raw[:400]}")
                return last

            return json.loads(raw)

    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body_text[:300]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Cannot reach {MCP_ENDPOINT}: {e.reason}") from e


# ── MCP protocol ──────────────────────────────────────────────────────────────

def _rpc(method: str, params: dict, req_id=None) -> dict:
    resp = _post({
        "jsonrpc": "2.0",
        "id": req_id or str(uuid.uuid4()),
        "method": method,
        "params": params,
    })
    if "error" in resp:
        raise RuntimeError(f"MCP error [{method}]: {resp['error']}")
    return resp.get("result", {})


def _initialize():
    _rpc("initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "newegg-skill-client", "version": "2.0"},
    }, req_id=1)


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_list_tools():
    """
    Discover all tools from the MCP server and print a structured summary
    optimised for LLM decision-making (tool selection + parameter mapping).
    """
    _initialize()
    result = _rpc("tools/list", {})
    tools = result.get("tools", [])

    if not tools:
        print("NO_TOOLS: The server returned no tools.")
        return

    # Emit a machine-readable block per tool so the LLM can parse easily
    print(f"TOOL_COUNT: {len(tools)}\n")
    for t in tools:
        name = t.get("name", "unknown")
        desc = t.get("description") or t.get("title") or "(no description)"
        schema = t.get("inputSchema", {})
        props = schema.get("properties", {})
        required = set(schema.get("required", []))

        print(f"=== TOOL: {name} ===")
        print(f"DESCRIPTION: {desc}")

        if props:
            print("PARAMETERS:")
            for param_name, param_schema in props.items():
                req_marker = "[required]" if param_name in required else "[optional]"
                ptype = param_schema.get("type", "any")
                pdesc = param_schema.get("description", "")
                enum_vals = param_schema.get("enum", [])
                enum_str = f" | values: {enum_vals}" if enum_vals else ""
                print(f"  - {param_name} ({ptype}) {req_marker}{enum_str}: {pdesc}")
        else:
            print("PARAMETERS: (none defined in schema)")

        print()

    print("---")
    print("INSTRUCTIONS FOR LLM:")
    print("1. Pick the tool whose DESCRIPTION + PARAMETERS best match the user request.")
    print("2. Build a JSON object using only parameters listed above.")
    print("3. For free-text parameters (question/query/text), put the user's intent as natural language.")
    print("4. Call: python scripts/mcp_client.py call <tool_name> '<json_args>'")
    print("   Windows: use single quotes, or @args.json / stdin '-' — see script docstring.")


def cmd_call_tool(tool_name: str, arguments: dict):
    """Call a specific tool and print the full response for LLM interpretation."""
    _initialize()
    result = _rpc("tools/call", {"name": tool_name, "arguments": arguments})

    # Unwrap content blocks if present
    content_blocks = result.get("content", [])
    is_error = result.get("isError", False)
    structured = result.get("structuredContent")

    print(f"TOOL: {tool_name}")
    print(f"IS_ERROR: {is_error}")
    print()

    # Prefer structuredContent (already parsed), else parse text blocks
    if structured:
        print("STRUCTURED_RESULT:")
        print(json.dumps(structured, indent=2, ensure_ascii=False))
    elif content_blocks:
        for block in content_blocks:
            btype = block.get("type", "text")
            if btype == "text":
                text = block.get("text", "")
                # Try to parse as JSON for nicer output
                try:
                    parsed = json.loads(text)
                    print("RESULT (parsed JSON):")
                    print(json.dumps(parsed, indent=2, ensure_ascii=False))
                except (json.JSONDecodeError, TypeError):
                    print("RESULT (text):")
                    print(text)
    else:
        print("RESULT:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

    print()
    print("---")
    print("INSTRUCTIONS FOR LLM:")
    print("- If IS_ERROR is true, report the error to the user.")
    print("- If all meaningful fields in RESULT are null, the service has no data for this query.")
    print("- Otherwise, extract build/compatibility/component info and present it clearly.")


def _load_call_arguments_raw(spec: str) -> str:
    """
    Resolve the third argument to call: inline JSON, '-' for stdin, or @path for a file.
    """
    if spec == "-":
        return sys.stdin.read()
    if spec.startswith("@"):
        path = spec[1:]
        if not path:
            raise ValueError("Empty path after @; use @C:\\path\\args.json or @args.json")
        path = os.path.expanduser(path)
        with open(path, encoding="utf-8-sig") as f:
            return f.read()
    return spec


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "list_tools":
        cmd_list_tools()

    elif command == "call":
        if len(sys.argv) < 3:
            print(
                "Usage: mcp_client.py call <tool_name> [json|@file|-]\n"
                "  json     Inline JSON object (use single quotes on PowerShell).\n"
                "  @path    Read JSON from a UTF-8 file (recommended on Windows).\n"
                "  -        Read JSON from stdin (e.g. pipe or redirect).",
                file=sys.stderr,
            )
            sys.exit(1)
        tool_name = sys.argv[2]
        raw_args = ""
        try:
            if len(sys.argv) > 3:
                raw_args = _load_call_arguments_raw(sys.argv[3])
            else:
                raw_args = "{}"
            arguments = json.loads(raw_args)
        except (json.JSONDecodeError, OSError, ValueError) as e:
            preview = raw_args if isinstance(raw_args, str) else ""
            if len(preview) > 120:
                preview = preview[:120] + "..."
            print(
                f"ERROR: arguments must be valid JSON.\n  Got: {preview!r}\n  {e}",
                file=sys.stderr,
            )
            print(
                "Hint (PowerShell): use single quotes around JSON, e.g.\n"
                "  python mcp_client.py call v2allin '{\"question\": \"your text\"}'\n"
                "Or put JSON in a file and run:\n"
                "  python mcp_client.py call v2allin @args.json",
                file=sys.stderr,
            )
            sys.exit(1)
        cmd_call_tool(tool_name, arguments)

    else:
        print(f"Unknown command: {command!r}\nUse: list_tools | call", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
