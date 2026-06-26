#!/usr/bin/env python3
"""
Veritier MCP Proxy - Standalone (v2)
=====================================
A lightweight stdio proxy that connects any MCP-compatible AI agent
to the Veritier fact-checking API.

Tools exposed:
  - extract_text      (consumes extractionsPerMonth quota)
  - extract_document  (consumes extractionsPerMonth quota)
  - verify_text       (consumes claimsPerMonth quota)
  - verify_document   (consumes claimsPerMonth quota)

Zero-quota Integration Testing
--------------------------------
Use a test API key (vt_test_...) to test your integration without consuming quota:
  - mock_claims (int 0-1000) on extract tools: returns deterministic mock claims
  - mock_verdict (bool) on verify tools: returns mock verdicts, all true or all false

With a test key, if you omit these params, test mode auto-activates with safe defaults.
See https://veritier.ai/docs#testing for full details.

Setup:
  1. pip install mcp httpx anyio
  2. Save this file anywhere on your machine
  3. Add to your MCP client config (e.g. .claude.json):

     {
       "mcpServers": {
         "veritier": {
           "command": "python",
           "args": ["/path/to/veritier_mcp_proxy.py"],
           "env": {
             "VERITIER_API_KEY": "vt_your_api_key_here"
           }
         }
       }
     }

  4. Get your free API key at https://veritier.ai/register
  5. For zero-quota testing, create a test key (vt_test_...) in your dashboard.

More info: https://veritier.ai/docs#mcp
"""

import anyio
import os
import sys

try:
    import httpx
except ImportError:
    print("Error: httpx is required. Install it with: pip install httpx", file=sys.stderr)
    sys.exit(1)

try:
    import mcp.types as types
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
except ImportError:
    print("Error: mcp is required. Install it with: pip install mcp", file=sys.stderr)
    sys.exit(1)

server = Server("veritier-mcp-proxy")

# SECURITY: The API endpoint is a hardcoded constant — it is never user-configurable
# and cannot be overridden by tool input or any other env var.
# VERITIER_API_KEY is used exclusively as a Bearer token in the Authorization header
# sent to https://api.veritier.ai only. It is never logged, stored, or forwarded
# to any other domain. This pattern is intentional API authentication, not exfiltration.
API_URL = "https://api.veritier.ai"  # hardcoded — not user-configurable
API_KEY = os.getenv("VERITIER_API_KEY", "")  # declared in SKILL.md openclaw.requires.env

if not API_KEY:
    print("Error: VERITIER_API_KEY environment variable is not set.", file=sys.stderr)
    print("Get your free API key at https://veritier.ai/register", file=sys.stderr)
    sys.exit(1)


def _auth_headers() -> dict:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }


def _format_results(data: dict) -> str:
    results = []
    for res in data.get("results", []):
        block = (
            f"Claim: '{res.get('claim')}'\n"
            f"  Verdict: {res.get('verdict')}\n"
            f"  Confidence: {res.get('confidence_score')}\n"
            f"  Explanation: {res.get('explanation')}"
        )
        if res.get("source_label"):
            block += f"\n  Source label: {res.get('source_label')}"
        sources = ", ".join(res.get("source_urls", []))
        block += f"\n  Sources: {sources or 'N/A'}"
        results.append(block)
    if data.get("warnings"):
        results.append("Warnings: " + "; ".join(data["warnings"]))
    if data.get("is_test"):
        results.append("[TEST MODE] is_test=true - mock response, no quota consumed.")
    return "\n\n".join(results) if results else "No falsifiable claims found in the text."


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="extract_text",
            description=(
                "Extracts every falsifiable claim from raw text without verifying them. "
                "Returns a list of isolated, objective statements. "
                "Consumes extractionsPerMonth quota (cheaper than verification). "
                "Pass mock_claims (int 0-1000) with a test key (vt_test_...) for zero-quota testing."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Raw text to extract claims from. Up to 32,000 characters.",
                    },
                    "mock_claims": {
                        "type": "integer",
                        "description": (
                            "Test mode only (requires a vt_test_... API key). "
                            "Integer 0-1000: number of mock claims to return without calling the LLM. "
                            "0 = empty list (tests your no-claims handling). "
                            "Omit for normal operation or auto-activation with test key."
                        ),
                        "minimum": 0,
                        "maximum": 1000,
                    },
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="extract_document",
            description=(
                "Fetches a publicly accessible URL and extracts falsifiable claims from its content. "
                "Consumes extractionsPerMonth quota. "
                "Pass mock_claims (int 0-1000) with a test key (vt_test_...) for zero-quota testing."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Publicly accessible URL to fetch and extract claims from.",
                    },
                    "mock_claims": {
                        "type": "integer",
                        "description": (
                            "Test mode only (requires a vt_test_... API key). "
                            "Integer 0-1000: number of mock claims to return without calling the LLM."
                        ),
                        "minimum": 0,
                        "maximum": 1000,
                    },
                },
                "required": ["url"],
            },
        ),
        types.Tool(
            name="verify_text",
            description=(
                "Extracts falsifiable claims from raw text and fact-checks them using "
                "Veritier's real-time verification engine. Returns structured verdicts with "
                "explanations and source URIs. Consumes claimsPerMonth quota. "
                "grounding_mode='both' costs 2x quota per claim. "
                "Pass mock_verdict (bool) with a test key (vt_test_...) for zero-quota testing."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Raw text containing claims to be fact-checked. Up to 32,000 characters.",
                    },
                    "grounding_mode": {
                        "type": "string",
                        "enum": ["web", "references", "both"],
                        "description": "Grounding strategy. 'web' uses live internet search (default). 'references' uses provided sources only. 'both' uses both (2x quota cost per claim).",
                    },
                    "grounding_references": {
                        "type": "array",
                        "description": "Up to 10 private references to ground claims against. Required when grounding_mode is 'references' or 'both'.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "enum": ["text", "url"]},
                                "content": {"type": "string"}
                            },
                            "required": ["type", "content"]
                        }
                    },
                    "mock_verdict": {
                        "type": "boolean",
                        "description": (
                            "Test mode only (requires a vt_test_... API key). "
                            "true = all mock verdicts true (happy-path). "
                            "false = all mock verdicts false (error-handling). "
                            "No quota consumed. Omit for normal operation."
                        ),
                    },
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="verify_document",
            description=(
                "Fetches a publicly accessible URL document and fact-checks its claims. "
                "Consumes claimsPerMonth quota. "
                "Pass mock_verdict (bool) with a test key (vt_test_...) for zero-quota testing."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Publicly accessible URL to fetch and verify.",
                    },
                    "grounding_mode": {
                        "type": "string",
                        "enum": ["web", "references", "both"],
                        "description": "Grounding strategy. Defaults to 'web'.",
                    },
                    "grounding_references": {
                        "type": "array",
                        "description": "Up to 10 private references. Required when grounding_mode is 'references' or 'both'.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string", "enum": ["text", "url"]},
                                "content": {"type": "string"}
                            },
                            "required": ["type", "content"]
                        }
                    },
                    "mock_verdict": {
                        "type": "boolean",
                        "description": (
                            "Test mode only (requires a vt_test_... API key). "
                            "true = all mock verdicts true. false = all false. No quota consumed."
                        ),
                    },
                },
                "required": ["url"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    args = arguments or {}

    try:
        async with httpx.AsyncClient() as client:

            if name == "extract_text":
                if "text" not in args:
                    raise ValueError("Missing 'text' argument")
                payload: dict = {"text": args["text"]}
                if "mock_claims" in args:
                    payload["mock_claims"] = args["mock_claims"]
                resp = await client.post(
                    f"{API_URL}/v1/extract",
                    json=payload,
                    headers=_auth_headers(),
                    timeout=60.0,
                )
                resp.raise_for_status()
                data = resp.json()
                claims = data.get("claims", [])
                text = "\n".join(f"- {c}" for c in claims) if claims else "No claims found."
                if data.get("warnings"):
                    text += "\n\nWarnings: " + "; ".join(data["warnings"])
                if data.get("is_test"):
                    text += "\n\n[TEST MODE] is_test=true - mock response, no quota consumed."
                return [types.TextContent(type="text", text=text)]

            elif name == "extract_document":
                if "url" not in args:
                    raise ValueError("Missing 'url' argument")
                payload = {"document": {"type": "url", "content": args["url"]}}
                if "mock_claims" in args:
                    payload["mock_claims"] = args["mock_claims"]
                resp = await client.post(
                    f"{API_URL}/v1/extract",
                    json=payload,
                    headers=_auth_headers(),
                    timeout=60.0,
                )
                resp.raise_for_status()
                data = resp.json()
                claims = data.get("claims", [])
                text = "\n".join(f"- {c}" for c in claims) if claims else "No claims found."
                if data.get("warnings"):
                    text += "\n\nWarnings: " + "; ".join(data["warnings"])
                if data.get("is_test"):
                    text += "\n\n[TEST MODE] is_test=true - mock response, no quota consumed."
                return [types.TextContent(type="text", text=text)]

            elif name == "verify_text":
                if "text" not in args:
                    raise ValueError("Missing 'text' argument")
                payload = {"text": args["text"]}
                if "grounding_mode" in args:
                    payload["grounding_mode"] = args["grounding_mode"]
                if "grounding_references" in args:
                    payload["grounding_references"] = args["grounding_references"]
                if "mock_verdict" in args:
                    payload["mock_verdict"] = args["mock_verdict"]
                resp = await client.post(
                    f"{API_URL}/v1/verify",
                    json=payload,
                    headers=_auth_headers(),
                    timeout=120.0,
                )
                resp.raise_for_status()
                return [types.TextContent(type="text", text=_format_results(resp.json()))]

            elif name == "verify_document":
                if "url" not in args:
                    raise ValueError("Missing 'url' argument")
                payload = {"document": {"type": "url", "content": args["url"]}}
                if "grounding_mode" in args:
                    payload["grounding_mode"] = args["grounding_mode"]
                if "grounding_references" in args:
                    payload["grounding_references"] = args["grounding_references"]
                if "mock_verdict" in args:
                    payload["mock_verdict"] = args["mock_verdict"]
                resp = await client.post(
                    f"{API_URL}/v1/verify",
                    json=payload,
                    headers=_auth_headers(),
                    timeout=120.0,
                )
                resp.raise_for_status()
                return [types.TextContent(type="text", text=_format_results(resp.json()))]

            else:
                raise ValueError(f"Unknown tool: {name}")

    except httpx.HTTPStatusError as e:
        return [
            types.TextContent(
                type="text",
                text=f"Veritier API error ({e.response.status_code}): {e.response.text}",
            )
        ]
    except Exception as e:
        return [
            types.TextContent(type="text", text=f"Proxy error: {e}")
        ]


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="veritier-proxy",
                server_version="2.1.1",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    anyio.run(main)
