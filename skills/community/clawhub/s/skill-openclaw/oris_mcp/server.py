"""Oris MCP Server: dual-transport (stdio + gRPC) with async worker pool.

Implements the Model Context Protocol (MCP) specification for exposing
Oris payment tools to AI agents (Claude, GPT, LangChain, CrewAI).

Transports:
    stdio  - Standard MCP transport (stdin/stdout JSON-RPC 2.0)
    gRPC   - High-frequency bidirectional streaming (port 50051)

Both transports share the same tool executor and worker pool.

Configuration via environment variables:
    ORIS_API_KEY       - Developer API key (oris_sk_live_...)
    ORIS_API_SECRET    - Developer API secret (oris_ss_live_...)
    ORIS_AGENT_ID      - Agent UUID
    ORIS_BASE_URL      - API base URL (default: https://api.useoris.finance)
    ORIS_GRPC_PORT     - gRPC listen port (default: 50051)
    ORIS_GRPC_ENABLED  - Enable gRPC transport (default: false)

Usage:
    export ORIS_API_KEY="oris_sk_live_..."
    export ORIS_API_SECRET="oris_ss_live_..."
    export ORIS_AGENT_ID="550e8400-e29b-41d4-a716-446655440000"
    python -m oris_mcp.server

Claude Desktop configuration (claude_desktop_config.json):
    {
        "mcpServers": {
            "oris": {
                "command": "python",
                "args": ["-m", "oris_mcp.server"],
                "cwd": "/path/to/oris-mcp-server",
                "env": {
                    "ORIS_API_KEY": "oris_sk_live_...",
                    "ORIS_API_SECRET": "oris_ss_live_...",
                    "ORIS_AGENT_ID": "..."
                }
            }
        }
    }
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from typing import Any

from oris_mcp.tools import TOOL_DEFINITIONS
from oris_mcp.executor import OrisToolExecutor
from oris_mcp.transport import Transport, StdioTransport, _make_response, _make_error
from oris_mcp.usage_gate import UsageGate
from oris_mcp.worker_pool import WorkerPool

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("oris.mcp")

PROTOCOL_VERSION = "2024-11-05"

SERVER_INFO = {
    "name": "oris-mcp-server",
    "version": "0.2.0",
}

SERVER_CAPABILITIES = {
    "tools": {},
}


class OrisMcpServer:
    """Dual-transport MCP server for Oris payment tools.

    Accepts connections over stdio (standard MCP) and gRPC (high-frequency).
    Both transports dispatch tool calls through the same async worker pool.
    """

    def __init__(self) -> None:
        api_key = os.environ.get("ORIS_API_KEY", "")
        api_secret = os.environ.get("ORIS_API_SECRET", "")
        agent_id = os.environ.get("ORIS_AGENT_ID", "")
        base_url = os.environ.get("ORIS_BASE_URL", "https://api.useoris.finance")

        # Fall back to OpenClaw config for credentials not provided via env.
        if not agent_id or not api_key or not api_secret:
            config = self._read_openclaw_config()
            if not api_key:
                api_key = config.get("apiKey", "")
            if not api_secret:
                api_secret = config.get("apiSecret", "")
            if not agent_id:
                agent_id = config.get("agentId", "")

        if not api_key or not api_secret or not agent_id:
            logger.error(
                "Oris credentials not found. Run 'openclaw run oris setup' first, "
                "or set ORIS_API_KEY, ORIS_API_SECRET, and ORIS_AGENT_ID."
            )

        self._pool = WorkerPool()
        self._executor = OrisToolExecutor(
            api_key=api_key,
            api_secret=api_secret,
            agent_id=agent_id,
            base_url=base_url,
            worker_pool=self._pool,
        )
        self._transports: list[Transport] = []

    @staticmethod
    def _read_openclaw_config() -> dict[str, Any]:
        """Read Oris credentials from OpenClaw's native config store."""
        config_path = os.path.join(
            os.environ.get("HOME", os.environ.get("USERPROFILE", "~")),
            ".openclaw",
            "config.json",
        )
        try:
            with open(config_path) as f:
                data = json.load(f)
                return data.get("oris", {})
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        self._initialized = False

        self._usage_gate = UsageGate(self._executor)

    def add_transport(self, transport: Transport) -> None:
        """Add a transport to the server."""
        self._transports.append(transport)

    async def handle(self, method: str, params: dict, req_id: Any) -> dict | None:
        """Transport-agnostic message handler.

        Processes JSON-RPC 2.0 messages from any transport.
        Returns the response dict, or None for notifications.
        """
        # Notifications (no id) do not expect a response.
        if req_id is None:
            if method == "notifications/initialized":
                self._initialized = True
                logger.info("client initialized")
            return None

        if method == "initialize":
            return self._handle_initialize(req_id, params)
        elif method == "tools/list":
            return self._handle_tools_list(req_id)
        elif method == "tools/call":
            return await self._handle_tools_call(req_id, params)
        else:
            return _make_error(req_id, -32601, f"Method not found: {method}")

    def _handle_initialize(self, req_id: Any, params: dict) -> dict:
        """Handle the initialize handshake."""
        client_info = params.get("clientInfo", {})
        logger.info(
            "initialize from %s %s",
            client_info.get("name", "unknown"),
            client_info.get("version", ""),
        )
        return _make_response(req_id, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": SERVER_CAPABILITIES,
            "serverInfo": SERVER_INFO,
        })

    def _handle_tools_list(self, req_id: Any) -> dict:
        """Return the list of available tools."""
        return _make_response(req_id, {"tools": TOOL_DEFINITIONS})

    async def _handle_tools_call(self, req_id: Any, params: dict) -> dict:
        """Execute a tool call through the worker pool."""
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        logger.info(
            "tool call: %s(%s)",
            tool_name,
            json.dumps(arguments, default=str)[:200],
        )

        valid_tools = {t["name"] for t in TOOL_DEFINITIONS}
        if tool_name not in valid_tools:
            return _make_error(req_id, -32602, f"Unknown tool: {tool_name}")

        # Pre-execution: fail-closed usage gate for OpenClaw billing.
        block_error, usage_snapshot = await self._usage_gate.check(tool_name)
        if block_error is not None:
            return _make_response(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({"error": block_error}, indent=2),
                    }
                ],
                "isError": True,
            })

        result = await self._executor.execute(tool_name, arguments)

        if "error" in result:
            return _make_response(req_id, {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps({"error": result["error"]}, indent=2),
                    }
                ],
                "isError": True,
            })

        # Post-execution: inject usage warning for free tier 80-99 TX range.
        warning = UsageGate.get_warning(usage_snapshot)
        if warning:
            result["_oris_usage"] = warning

        return _make_response(req_id, {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(result, indent=2, default=str),
                }
            ],
        })

    async def run(self) -> None:
        """Start all transports and run until shutdown."""
        logger.info(
            "Oris MCP server starting (%d transport(s))", len(self._transports)
        )

        tasks = [transport.start(self) for transport in self._transports]
        await asyncio.gather(*tasks)

        logger.info("Oris MCP server shutting down")
        await self._executor.close()

    async def shutdown(self) -> None:
        """Shut down all transports."""
        for transport in self._transports:
            await transport.close()
        await self._executor.close()


async def async_main():
    """Async entry point."""
    server = OrisMcpServer()
    server.add_transport(StdioTransport())
    await server.run()


def main():
    """Entry point for the MCP server."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
