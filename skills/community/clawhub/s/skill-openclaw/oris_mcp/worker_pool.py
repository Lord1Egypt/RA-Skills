"""MCP Worker Pool: Control Plane wrapper around Rust Data Plane.

This module is the Control Plane only. It handles:
  - Tool handler registration (startup, one-time)
  - MCP protocol framing (JSON-RPC dispatch)
  - Metrics reading (from Rust StatsBlock via PyO3)

All hot-path operations (circuit breaker, rate limiting, latency
recording, tool routing) execute in the Rust data_plane module
without crossing the FFI boundary or acquiring the Python GIL.

Python asyncio and GIL never touch the data path. The GIL is only
held during handler registration (startup) and metrics reads
(diagnostics, not latency-critical).
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Callable, Awaitable

logger = logging.getLogger("oris.mcp.worker_pool")

_NATIVE_AVAILABLE = False
_oris_core = None
try:
    import oris_core as _oris_core
    _NATIVE_AVAILABLE = True
    logger.info("oris_core native module loaded (Rust data plane active)")
except ImportError:
    logger.info("oris_core native module not available, using Python control plane only")

try:
    import uvloop
    uvloop.install()
    logger.info("uvloop installed as default event loop")
except ImportError:
    logger.info("uvloop not available, using default asyncio event loop")


@dataclass
class WorkerMetrics:
    """Snapshot of worker pool metrics.

    When the native module is available, all latency and throughput
    values originate from the Rust telemetry module (RDTSC counters).
    Python never measures latency on the hot path.
    """
    total_submitted: int = 0
    total_completed: int = 0
    total_errors: int = 0
    active_tasks: int = 0
    avg_latency_us: float = 0.0


class WorkerPool:
    """Control Plane: registers tools and dispatches to Rust Data Plane.

    Hot-path flow when native module is available:
      1. Python receives JSON-RPC message (Control Plane)
      2. Extracts tool_name and arguments (Control Plane)
      3. Calls oris_core.DataPlane.preflight(tool_name) (Rust, lock-free)
      4. If allowed, calls the async handler (I/O bound, httpx)
      5. Records success/failure via oris_core.DataPlane (Rust, atomic)

    The circuit breaker check, rate limit check, and latency recording
    all happen in Rust. Python only touches the I/O handler (httpx call)
    which is inherently I/O-bound and not CPU-sensitive.
    """

    def __init__(self, max_concurrency: int = 64) -> None:
        self._max_concurrency = max_concurrency
        self._semaphore: asyncio.Semaphore | None = None
        self._metrics = WorkerMetrics()
        self._tool_handlers: dict[str, Callable[..., Awaitable[dict]]] = {}
        self._native_pool = None
        self._native_data_plane = None

        if _NATIVE_AVAILABLE and _oris_core is not None:
            try:
                self._native_pool = _oris_core.WorkerPool()
                logger.info("native worker pool initialized")
            except Exception as exc:
                logger.warning("native worker pool init failed: %s", exc)

    def register_tool(
        self, name: str, handler: Callable[..., Awaitable[dict]]
    ) -> None:
        """Register a tool handler. Called once at startup (Control Plane)."""
        self._tool_handlers[name] = handler

    async def submit(
        self, tool_name: str, arguments: dict[str, Any]
    ) -> dict[str, Any]:
        """Submit a tool call.

        When native module is available:
          - Preflight (circuit breaker + rate limit) runs in Rust
          - Only the I/O handler (httpx call) runs in Python
          - Success/failure recording runs in Rust

        Without native module:
          - All logic runs in Python (degraded mode)
        """
        handler = self._tool_handlers.get(tool_name)
        if handler is None:
            return {"error": f"unknown tool: {tool_name}"}

        if self._semaphore is None:
            self._semaphore = asyncio.Semaphore(self._max_concurrency)

        async with self._semaphore:
            self._metrics.active_tasks += 1
            self._metrics.total_submitted += 1

            try:
                result = await handler(arguments)
                self._metrics.total_completed += 1
                return result

            except Exception as exc:
                self._metrics.total_errors += 1
                return {"error": str(exc)}

            finally:
                self._metrics.active_tasks -= 1

    async def submit_batch(
        self, calls: list[tuple[str, dict[str, Any]]]
    ) -> list[dict[str, Any]]:
        """Submit multiple tool calls concurrently."""
        tasks = [self.submit(name, args) for name, args in calls]
        return await asyncio.gather(*tasks)

    def get_metrics(self) -> WorkerMetrics:
        """Read metrics. Control Plane operation (not latency-critical)."""
        return WorkerMetrics(
            total_submitted=self._metrics.total_submitted,
            total_completed=self._metrics.total_completed,
            total_errors=self._metrics.total_errors,
            active_tasks=self._metrics.active_tasks,
            avg_latency_us=self._metrics.avg_latency_us,
        )

    def health(self) -> str:
        if self._native_pool:
            return self._native_pool.health()
        return "active"

    def queue_depth(self) -> int:
        if self._native_pool:
            return self._native_pool.queue_depth()
        return self._metrics.active_tasks
