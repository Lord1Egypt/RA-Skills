"""
Tool Call Timeout Wrapper — P0 Security

Wraps every tool call in a configurable timeout.
Default 30s, per-tool overrides available.
Prevents hanging calls from blocking subagents indefinitely.

Built for tool execution supervision

"""

import asyncio
import time
import json
import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)

# Default timeouts per tool (seconds)
DEFAULT_TIMEOUTS: Dict[str, float] = {
    "exec": 120.0,
    "web_fetch": 60.0,
    "web_search": 30.0,
    "image": 30.0,
    "image_generate": 120.0,
    "read": 10.0,
    "write": 10.0,
    "edit": 10.0,
    "memory_get": 5.0,
    "memory_search": 10.0,
    "sessions_spawn": 30.0,
    "sessions_send": 10.0,
    "process": 30.0,
}

GLOBAL_DEFAULT_TIMEOUT = 30.0


@dataclass
class TimeoutResult:
    """Result of a supervised tool call with timeout."""
    tool: str
    succeeded: bool
    output: Any = None
    error: Optional[str] = None
    duration_ms: float = 0.0
    timed_out: bool = False


class TimeoutWrapper:
    """
    Wraps tool calls with configurable timeouts.
    
    Usage:
        wrapper = TimeoutWrapper()
        result = await wrapper.call("web_fetch", web_fetch_fn, url="...")
        if result.timed_out:
            logger.warning(f"Tool {result.tool} timed out after {result.duration_ms}ms")
    """
    
    def __init__(self, custom_timeouts: Optional[Dict[str, float]] = None):
        self.timeouts = {**DEFAULT_TIMEOUTS, **(custom_timeouts or {})}
        self.stats: Dict[str, Dict] = {}  # tool -> {calls, timeouts, avg_duration}
    
    def get_timeout(self, tool: str) -> float:
        """Get timeout for a tool, falling back to global default."""
        return self.timeouts.get(tool, GLOBAL_DEFAULT_TIMEOUT)
    
    def set_timeout(self, tool: str, timeout: float) -> None:
        """Override timeout for a specific tool."""
        if timeout <= 0:
            raise ValueError(f"Timeout must be positive, got {timeout}")
        self.timeouts[tool] = timeout
        logger.info(f"Timeout override: {tool} = {timeout}s")
    
    async def call(
        self,
        tool: str,
        fn: Callable,
        timeout: Optional[float] = None,
        **kwargs
    ) -> TimeoutResult:
        """
        Execute a tool call with timeout protection.
        
        Args:
            tool: Tool name for timeout lookup
            fn: Async callable to execute
            timeout: Override timeout (seconds). None = use default for tool.
            **kwargs: Arguments to pass to fn
        
        Returns:
            TimeoutResult with success/failure status and duration
        """
        effective_timeout = timeout or self.get_timeout(tool)
        start = time.monotonic()
        
        try:
            result = await asyncio.wait_for(fn(**kwargs), timeout=effective_timeout)
            duration_ms = (time.monotonic() - start) * 1000
            self._record_stats(tool, duration_ms, timed_out=False)
            return TimeoutResult(
                tool=tool,
                succeeded=True,
                output=result,
                duration_ms=duration_ms,
            )
        except asyncio.TimeoutError:
            duration_ms = (time.monotonic() - start) * 1000
            self._record_stats(tool, duration_ms, timed_out=True)
            logger.warning(f"Tool {tool} timed out after {duration_ms:.0f}ms (limit: {effective_timeout}s)")
            return TimeoutResult(
                tool=tool,
                succeeded=False,
                error=f"Timeout after {effective_timeout}s",
                duration_ms=duration_ms,
                timed_out=True,
            )
        except Exception as e:
            duration_ms = (time.monotonic() - start) * 1000
            self._record_stats(tool, duration_ms, timed_out=False)
            return TimeoutResult(
                tool=tool,
                succeeded=False,
                error=str(e),
                duration_ms=duration_ms,
            )
    
    def _record_stats(self, tool: str, duration_ms: float, timed_out: bool) -> None:
        """Record call statistics for monitoring."""
        if tool not in self.stats:
            self.stats[tool] = {"calls": 0, "timeouts": 0, "total_ms": 0.0}
        self.stats[tool]["calls"] += 1
        if timed_out:
            self.stats[tool]["timeouts"] += 1
        self.stats[tool]["total_ms"] += duration_ms
    
    def get_stats(self) -> Dict[str, Dict]:
        """Get timeout statistics for all tools."""
        result = {}
        for tool, s in self.stats.items():
            avg = s["total_ms"] / s["calls"] if s["calls"] > 0 else 0
            result[tool] = {
                "calls": s["calls"],
                "timeouts": s["timeouts"],
                "timeout_rate": s["timeouts"] / s["calls"] if s["calls"] > 0 else 0,
                "avg_duration_ms": round(avg, 1),
                "configured_timeout": self.get_timeout(tool),
            }
        return result
    
    def get_config(self) -> Dict[str, float]:
        """Get current timeout configuration."""
        return dict(self.timeouts)


# Global singleton
_timeout_wrapper: Optional[TimeoutWrapper] = None

def get_timeout_wrapper() -> TimeoutWrapper:
    """Get or create the global timeout wrapper."""
    global _timeout_wrapper
    if _timeout_wrapper is None:
        _timeout_wrapper = TimeoutWrapper()
    return _timeout_wrapper