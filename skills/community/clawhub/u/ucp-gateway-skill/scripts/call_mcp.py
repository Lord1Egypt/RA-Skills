#!/usr/bin/env python3
"""Small JSON-RPC helper for The Agent Times UCP Gateway MCP endpoint."""

import json
import os
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

DEFAULT_GATEWAY = "https://ucpgateway.theagenttimes.com/mcp"
COMMON_SHOPPING_TOOLS = [
    "shopping_product_search",
    "shopping_cart_create",
    "shopping_checkout_create",
]


class CallMcpError(Exception):
    """Raised for safe, user-facing MCP helper failures."""


def usage(stream=sys.stdout):
    stream.write(
        """Usage:
  python3 scripts/call_mcp.py <tool_name> '<json-arguments>'
  python3 scripts/call_mcp.py --initialize
  python3 scripts/call_mcp.py --tools
  python3 scripts/call_mcp.py --tool <tool_name>
  python3 scripts/call_mcp.py --shopping-tools
  python3 scripts/call_mcp.py --resources
  python3 scripts/call_mcp.py --resource <uri>
  python3 scripts/call_mcp.py --prompts
  python3 scripts/call_mcp.py --prompt <name> [--prompt-arg key=value ...]

Examples:
  python3 scripts/call_mcp.py --initialize
  python3 scripts/call_mcp.py --tools
  python3 scripts/call_mcp.py --tool shopping_product_search
  python3 scripts/call_mcp.py --shopping-tools
  python3 scripts/call_mcp.py --resource ucp://gateway/skill-runtime-guide
  python3 scripts/call_mcp.py --prompt ucp-skill-runtime-guide --prompt-arg shopping_goal='trail running shoes'
  python3 scripts/call_mcp.py shopping_product_search '{"query":"trail running shoes","limit":5}'
  python3 scripts/call_mcp.py shopping_product_get '{"product_id":"provider-product-id","merchant_domain":"merchant.example"}'

The full JSON-RPC response is printed, including result.next_step and result.structuredContent.next_step.
Tool names, descriptions, and input field descriptions are discovered from live MCP tools/list.
Discovery modes do not require ./.ucpgateway/agent.json.
If ./.ucpgateway/agent.json exists, agent_id is injected automatically for Shopping tools when absent.
"""
    )


def has_flag(argv, name):
    return name in argv


def flag_value(argv, name):
    try:
        index = argv.index(name)
    except ValueError:
        return None
    if index + 1 >= len(argv):
        return None
    value = argv[index + 1]
    if value.startswith("--"):
        return None
    return value


def parse_prompt_args(argv):
    parsed = {}
    i = 0
    while i < len(argv):
        if argv[i] != "--prompt-arg":
            i += 1
            continue
        if i + 1 >= len(argv) or argv[i + 1].startswith("--") or "=" not in argv[i + 1]:
            raise CallMcpError("--prompt-arg must be provided as key=value")
        key, value = argv[i + 1].split("=", 1)
        if not key:
            raise CallMcpError("--prompt-arg key must not be empty")
        parsed[key] = value
        i += 2
    return parsed


def discovery_request(argv):
    if has_flag(argv, "--initialize"):
        return {"method": "initialize"}
    if has_flag(argv, "--tools"):
        return {"method": "tools/list"}
    if has_flag(argv, "--resources"):
        return {"method": "resources/list"}
    if has_flag(argv, "--resource"):
        uri = flag_value(argv, "--resource")
        if not uri:
            raise CallMcpError("--resource requires a URI")
        return {"method": "resources/read", "params": {"uri": uri}}
    if has_flag(argv, "--prompts"):
        return {"method": "prompts/list"}
    if has_flag(argv, "--prompt"):
        name = flag_value(argv, "--prompt")
        if not name:
            raise CallMcpError("--prompt requires a prompt name")
        return {"method": "prompts/get", "params": {"name": name, "arguments": parse_prompt_args(argv)}}
    return None


def read_agent_id(root):
    agent_path = root / ".ucpgateway" / "agent.json"
    try:
        with agent_path.open("r", encoding="utf-8") as handle:
            agent = json.load(handle)
    except FileNotFoundError as exc:
        raise CallMcpError("Missing agent_id and ./.ucpgateway/agent.json not found. Run init/register first or provide agent_id in the JSON arguments.") from exc
    except json.JSONDecodeError as exc:
        raise CallMcpError(f"./.ucpgateway/agent.json is not valid JSON: {exc.msg}.") from exc
    agent_id = agent.get("agent_id") if isinstance(agent, dict) else None
    if not agent_id:
        raise CallMcpError("./.ucpgateway/agent.json does not contain agent_id. Re-register or provide agent_id in the JSON arguments.")
    return agent_id


def post_json(url, payload, timeout=60):
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"content-type": "application/json", "accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            return json.loads(body), exc.code
        except json.JSONDecodeError:
            raise CallMcpError(f"Gateway HTTP {exc.code}: {body[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise CallMcpError(f"Could not reach UCP Gateway MCP endpoint: {exc.reason}") from exc

    try:
        return json.loads(body), 200
    except json.JSONDecodeError as exc:
        raise CallMcpError("Gateway response was not valid JSON.") from exc


def tool_descriptor_request(argv):
    if has_flag(argv, "--shopping-tools"):
        return COMMON_SHOPPING_TOOLS
    if has_flag(argv, "--tool"):
        name = flag_value(argv, "--tool")
        if not name:
            raise CallMcpError("--tool requires a tool name")
        return [name]
    return None


def print_tool_descriptors(gateway, names, stdout, stderr):
    response, http_status = post_json(
        gateway,
        {"jsonrpc": "2.0", "id": str(uuid.uuid4()), "method": "tools/list"},
    )
    tools = (((response or {}).get("result") or {}).get("tools") or []) if isinstance(response, dict) else []
    by_name = {tool.get("name"): tool for tool in tools if isinstance(tool, dict)}
    selected = [by_name[name] for name in names if name in by_name]
    missing = [name for name in names if name not in by_name]
    print(
        json.dumps(
            {
                "source": "tools/list",
                "gateway": gateway,
                "tools": selected,
                "missing": missing,
                "note": "Tool names, descriptions, and input field descriptions are authoritative from the live MCP tools/list response.",
            },
            indent=2,
        ),
        file=stdout,
    )
    if http_status >= 400:
        print(f"call_mcp: gateway returned HTTP {http_status}", file=stderr)
        return 1
    if missing:
        print(f"call_mcp: tool descriptor(s) not found: {', '.join(missing)}", file=stderr)
        return 1
    return 0


def build_tool_request(argv, root):
    tool = argv[0]
    try:
        arguments = json.loads(argv[1]) if len(argv) > 1 else {}
    except json.JSONDecodeError as exc:
        raise CallMcpError(f"Tool arguments must be valid JSON: {exc.msg}.") from exc
    if not isinstance(arguments, dict):
        raise CallMcpError("Tool arguments JSON must be an object.")

    if not arguments.get("agent_id") and tool not in {"register_ucp_profile", "get_ucp_profile"}:
        arguments = {"agent_id": read_agent_id(root), **arguments}
    return {"method": "tools/call", "params": {"name": tool, "arguments": arguments}}


def run(argv=None, cwd=None, stdout=None, stderr=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr
    if "--help" in argv or not argv:
        usage(stdout)
        return 0

    root = Path(cwd or os.getcwd())
    gateway = os.environ.get("UCP_GATEWAY_MCP_URL") or DEFAULT_GATEWAY
    descriptor_names = tool_descriptor_request(argv)
    if descriptor_names is not None:
        return print_tool_descriptors(gateway, descriptor_names, stdout, stderr)

    request = discovery_request(argv)
    if request is None:
        if argv[0].startswith("--"):
            raise CallMcpError(f"Unknown option {argv[0]}")
        request = build_tool_request(argv, root)

    response, http_status = post_json(gateway, {"jsonrpc": "2.0", "id": str(uuid.uuid4()), **request})
    print(json.dumps(response, indent=2), file=stdout)
    if http_status >= 400:
        print(f"call_mcp: gateway returned HTTP {http_status}", file=stderr)
        return 1
    return 0


def main():
    try:
        return run()
    except CallMcpError as exc:
        print(f"call_mcp: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
