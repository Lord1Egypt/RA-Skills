#!/usr/bin/env python3
"""MCP server exposing unified_search as a tool for ACP agents (Claude CLI etc.)."""

import subprocess
import sys
import os
from mcp.server.fastmcp import FastMCP

UNIFIED_SEARCH_BIN = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "scripts",
    "unified-search.sh",
)

mcp = FastMCP("unified_search", instructions="""
unified_search — Multi-engine search (Tavily + Exa + Google) optimized for Chinese queries.
Use this for web searches, information gathering, and fact-checking.
""")

@mcp.tool(
    name="unified_search",
    description=(
        "Search the web using multiple search engines (Tavily, Exa, Google). "
        "Optimized for Chinese and English queries. "
        "Use this for information gathering, fact-checking, research, and current events."
    ),
)
def unified_search(query: str) -> str:
    """Run unified-search.sh with the given query and return results."""
    env = os.environ.copy()
    env.setdefault("OPENCLAW_CONFIG", os.path.expanduser("~/.openclaw/openclaw.json"))

    result = subprocess.run(
        ["bash", UNIFIED_SEARCH_BIN, query],
        capture_output=True,
        text=True,
        timeout=120,
        env=env,
    )

    if result.returncode != 0:
        # Return partial output on failure
        output = (result.stdout or "") + "\n" + (result.stderr or "")
        return f"[Search exited with code {result.returncode}]\n{output.strip()}"
    return result.stdout.strip()


if __name__ == "__main__":
    mcp.run(transport="stdio")
