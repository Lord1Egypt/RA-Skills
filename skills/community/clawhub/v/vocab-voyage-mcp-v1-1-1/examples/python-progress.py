#!/usr/bin/env python3
"""Fetch the auth-only `get_my_progress` widget result from the Vocab Voyage
MCP server. Set VV_MCP_TOKEN in your environment first."""

import json
import os
import sys
import urllib.request

ENDPOINT = "https://gponcrussdahcdyrlhcr.supabase.co/functions/v1/mcp-server"

token = os.environ.get("VV_MCP_TOKEN")
if not token:
    print("Set VV_MCP_TOKEN first (generate at https://vocab.voyage/developers/auth)", file=sys.stderr)
    sys.exit(1)

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {"name": "get_my_progress", "arguments": {}},
}

req = urllib.request.Request(
    ENDPOINT,
    data=json.dumps(payload).encode("utf-8"),
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}",
    },
)

with urllib.request.urlopen(req) as resp:
    print(json.dumps(json.loads(resp.read()), indent=2))