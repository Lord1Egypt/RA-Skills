#!/usr/bin/env python3
"""
RankClaw MCP stdio bridge.
Wraps the HTTP MCP endpoint at https://api.rankclaw.com/api/mcp/
as a stdio MCP server for use with nanoclaw and other MCP clients
that only support stdio transport.

Usage (in nanoclaw .mcp.json):
{
  "mcpServers": {
    "rankclaw": {
      "command": "python3",
      "args": ["/path/to/rankclaw_mcp_bridge.py"]
    }
  }
}
"""
import json
import sys
import urllib.request
import urllib.error

MCP_URL = "https://api.rankclaw.com/api/mcp/"

def call_mcp(body: dict) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        MCP_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return {"jsonrpc": "2.0", "id": body.get("id"), "error": {"code": -32000, "message": str(e)}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            body = json.loads(line)
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}) + "\n")
            sys.stdout.flush()
            continue

        result = call_mcp(body)
        sys.stdout.write(json.dumps(result) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
