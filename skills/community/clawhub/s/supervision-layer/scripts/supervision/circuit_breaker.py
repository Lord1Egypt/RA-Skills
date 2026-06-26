"""
Circuit Breaker — P0 Security

Per-tool circuit breaker with 3-state machine: CLOSED → OPEN → HALF_OPEN.
Prevents cascading failures from burning through budgets.

Built for tool execution supervision

"""

import asyncio
import time
import logging
from dataclasses import dataclass, field
from typing import Dict, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitStats:
    """Statistics for a single circuit breaker."""
    tool: str
    state: CircuitState = CircuitState.CLOSED
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    total_calls: int = 0
    total_failures: int = 0
    total_rejections: int = 0
    last_failure_time: Optional[float] = None
    last_success_time: Optional[float] = None
    opened_at: Optional[float] = None


class CircuitBreaker:
    """
    Per-tool circuit breaker.
    
    CLOSED: Normal operation. Track consecutive failures.
        → If failures >= threshold → OPEN
    OPEN: All calls blocked. Wait for reset_after timeout.
        → If reset_after elapsed → HALF_OPEN (one test call allowed)
    HALF_OPEN: Allow one test call.
        → If success → CLOSED (reset counters)
        → If failure → OPEN (restart timer)
    
    Thread-safe via asyncio.Lock for async usage.
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        reset_after: float = 60.0,
        half_open_max_calls: int = 1,
    ):
        self.failure_threshold = failure_threshold
        self.reset_after = reset_after
        self.half_open_max_calls = half_open_max_calls
        self.circuits: Dict[str, CircuitStats] = {}
        self._locks: Dict[str, asyncio.Lock] = {}
        self._global_lock = asyncio.Lock()
    
    async def _get_lock(self, tool: str) -> asyncio.Lock:
        """Get or create a lock for a specific tool."""
        async with self._global_lock:
            if tool not in self._locks:
                self._locks[tool] = asyncio.Lock()
            return self._locks[tool]
    
    def _get_circuit(self, tool: str) -> CircuitStats:
        """Get or create circuit stats for a tool."""
        if tool not in self.circuits:
            self.circuits[tool] = CircuitStats(tool=tool)
        return self.circuits[tool]
    
    async def can_call(self, tool: str) -> bool:
        """
        Check if a call is allowed through the circuit breaker.
        
        Returns:
            True if call is allowed, False if circuit is OPEN.
        """
        lock = await self._get_lock(tool)
        async with lock:
            circuit = self._get_circuit(tool)
            now = time.monotonic()
            
            if circuit.state == CircuitState.CLOSED:
                return True
            
            elif circuit.state == CircuitState.OPEN:
                # Check if reset_after has elapsed
                if circuit.opened_at and (now - circuit.opened_at) >= self.reset_after:
                    circuit.state = CircuitState.HALF_OPEN
                    logger.info(f"Circuit {tool}: OPEN → HALF_OPEN (testing)")
                    return True
                circuit.total_rejections += 1
                return False
            
            elif circuit.state == CircuitState.HALF_OPEN:
                # Allow one test call
                return True
            
            return True
    
    async def record_success(self, tool: str) -> None:
        """Record a successful call."""
        lock = await self._get_lock(tool)
        async with lock:
            circuit = self._get_circuit(tool)
            now = time.monotonic()
            
            circuit.consecutive_failures = 0
            circuit.consecutive_successes += 1
            circuit.total_calls += 1
            circuit.last_success_time = now
            
            if circuit.state == CircuitState.HALF_OPEN:
                circuit.state = CircuitState.CLOSED
                logger.info(f"Circuit {tool}: HALF_OPEN → CLOSED (recovered)")
    
    async def record_failure(self, tool: str) -> None:
        """Record a failed call."""
        lock = await self._get_lock(tool)
        async with lock:
            circuit = self._get_circuit(tool)
            now = time.monotonic()
            
            circuit.consecutive_failures += 1
            circuit.consecutive_successes = 0
            circuit.total_calls += 1
            circuit.total_failures += 1
            circuit.last_failure_time = now
            
            if circuit.state == CircuitState.HALF_OPEN:
                # Test call failed — back to OPEN
                circuit.state = CircuitState.OPEN
                circuit.opened_at = now
                logger.warning(f"Circuit {tool}: HALF_OPEN → OPEN (test call failed)")
            
            elif circuit.state == CircuitState.CLOSED:
                # Check if threshold reached
                if circuit.consecutive_failures >= self.failure_threshold:
                    circuit.state = CircuitState.OPEN
                    circuit.opened_at = now
                    logger.warning(
                        f"Circuit {tool}: CLOSED → OPEN "
                        f"({circuit.consecutive_failures} consecutive failures)"
                    )
    
    async def record_rejection(self, tool: str) -> None:
        """Record a rejected call (circuit was OPEN)."""
        lock = await self._get_lock(tool)
        async with lock:
            circuit = self._get_circuit(tool)
            circuit.total_rejections += 1
    
    async def reset(self, tool: str) -> None:
        """Manually reset a circuit to CLOSED state."""
        lock = await self._get_lock(tool)
        async with lock:
            circuit = self._get_circuit(tool)
            circuit.state = CircuitState.CLOSED
            circuit.consecutive_failures = 0
            circuit.consecutive_successes = 0
            circuit.opened_at = None
            logger.info(f"Circuit {tool}: manually reset to CLOSED")
    
    def get_status(self) -> Dict[str, Dict]:
        """Get status of all circuit breakers."""
        result = {}
        for tool, circuit in self.circuits.items():
            result[tool] = {
                "state": circuit.state.value,
                "consecutive_failures": circuit.consecutive_failures,
                "consecutive_successes": circuit.consecutive_successes,
                "total_calls": circuit.total_calls,
                "total_failures": circuit.total_failures,
                "total_rejections": circuit.total_rejections,
                "failure_rate": (
                    circuit.total_failures / circuit.total_calls
                    if circuit.total_calls > 0 else 0
                ),
                "last_failure": circuit.last_failure_time,
                "last_success": circuit.last_success_time,
                "opened_at": circuit.opened_at,
            }
        return result
    
    def get_config(self) -> Dict:
        """Get current configuration."""
        return {
            "failure_threshold": self.failure_threshold,
            "reset_after": self.reset_after,
            "half_open_max_calls": self.half_open_max_calls,
        }


# Global singleton
_circuit_breaker: Optional[CircuitBreaker] = None

def get_circuit_breaker() -> CircuitBreaker:
    """Get or create the global circuit breaker."""
    global _circuit_breaker
    if _circuit_breaker is None:
        _circuit_breaker = CircuitBreaker()
    return _circuit_breaker