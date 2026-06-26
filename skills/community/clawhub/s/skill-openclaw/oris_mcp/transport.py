"""Abstract transport layer and stdio implementation.

Defines the Transport protocol for pluggable MCP message delivery.
StdioTransport implements the standard MCP stdio transport using
asyncio StreamReader/Writer for non-blocking I/O.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
from abc import ABC, abstractmethod
from typing import Any, Protocol

logger = logging.getLogger("oris.mcp.transport")


class MessageHandler(Protocol):
    """Protocol for handling incoming JSON-RPC messages."""

    async def handle(self, method: str, params: dict, req_id: Any) -> dict | None:
        """Process a message and return the response, or None for notifications."""
        ...


class Transport(ABC):
    """Abstract base for MCP transports."""

    @abstractmethod
    async def start(self, handler: MessageHandler) -> None:
        """Start the transport and begin processing messages."""
        ...

    @abstractmethod
    async def send(self, message: dict) -> None:
        """Send a JSON-RPC message to the client."""
        ...

    @abstractmethod
    async def close(self) -> None:
        """Shut down the transport cleanly."""
        ...


class StdioTransport(Transport):
    """MCP stdio transport: reads JSON-RPC from stdin, writes to stdout.

    Uses asyncio StreamReader/Writer for non-blocking I/O. Each line
    is a complete JSON-RPC 2.0 message. Compatible with Claude Desktop,
    LangChain, and other MCP clients.
    """

    def __init__(self) -> None:
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._running = False

    async def start(self, handler: MessageHandler) -> None:
        """Start reading from stdin and dispatching to the handler."""
        logger.info("stdio transport starting")

        loop = asyncio.get_event_loop()

        # Create async readers for stdin/stdout.
        self._reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(self._reader)
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)

        transport_w, protocol_w = await loop.connect_write_pipe(
            asyncio.streams.FlowControlMixin, sys.stdout
        )
        self._writer = asyncio.StreamWriter(
            transport_w, protocol_w, None, loop
        )

        self._running = True

        while self._running:
            try:
                line = await self._reader.readline()
                if not line:
                    break

                line_str = line.decode("utf-8").strip()
                if not line_str:
                    continue

                try:
                    message = json.loads(line_str)
                except json.JSONDecodeError as exc:
                    error = _make_error(None, -32700, f"Parse error: {exc}")
                    await self.send(error)
                    continue

                method = message.get("method", "")
                req_id = message.get("id")
                params = message.get("params", {})

                response = await handler.handle(method, params, req_id)

                if response is not None:
                    await self.send(response)

            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.error("stdio transport error: %s", exc)
                break

        logger.info("stdio transport stopped")

    async def send(self, message: dict) -> None:
        """Write a JSON-RPC response to stdout."""
        if self._writer is None:
            return

        data = json.dumps(message) + "\n"
        self._writer.write(data.encode("utf-8"))
        await self._writer.drain()

    async def close(self) -> None:
        """Stop the transport."""
        self._running = False
        if self._writer:
            self._writer.close()


def _make_response(req_id: Any, result: Any) -> dict:
    """Build a JSON-RPC 2.0 response."""
    return {"jsonrpc": "2.0", "id": req_id, "result": result}


def _make_error(req_id: Any, code: int, message: str) -> dict:
    """Build a JSON-RPC 2.0 error response."""
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": code, "message": message},
    }
