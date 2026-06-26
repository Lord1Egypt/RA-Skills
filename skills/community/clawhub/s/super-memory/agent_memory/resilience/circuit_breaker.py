"""Circuit breaker pattern for external service calls.

States:
- CLOSED: Normal operation, requests pass through
- OPEN: Failure threshold exceeded, requests are rejected immediately
- HALF_OPEN: Testing if service recovered, allows limited requests

Usage:
    breaker = CircuitBreaker("llm_api", failure_threshold=3, recovery_timeout=30)

    result = breaker.call(llm_function, prompt="hello")
    # or as decorator:
    @circuit("llm_api")
    def call_llm(prompt):
        return openai.ChatCompletion.create(...)
"""

import threading
import time
import logging
from enum import Enum
from functools import wraps
from typing import Callable, Any, Optional

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitOpenError(Exception):
    """Raised when circuit is open and request is rejected."""
    def __init__(self, circuit_name: str, recovery_after: float):
        self.circuit_name = circuit_name
        self.recovery_after = recovery_after
        super().__init__(
            f"断路器 [{circuit_name}] 已打开，服务暂时不可用。"
            f"预计 {recovery_after:.0f} 秒后恢复"
        )


class CircuitBreaker:
    """Thread-safe circuit breaker implementation."""

    def __init__(
        self,
        name: str,
        failure_threshold: int = 3,
        recovery_timeout: float = 30.0,
        half_open_max_calls: int = 1,
        success_threshold: int = 2,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.success_threshold = success_threshold

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = 0.0
        self._half_open_calls = 0
        self._call_count = 0
        self._last_call_time = 0.0
        self._lock = threading.Lock()

    @property
    def state(self) -> CircuitState:
        with self._lock:
            if self._state == CircuitState.OPEN:
                # Check if recovery timeout has elapsed
                if time.time() - self._last_failure_time >= self.recovery_timeout:
                    self._state = CircuitState.HALF_OPEN
                    self._half_open_calls = 0
                    self._success_count = 0
                    logger.info("断路器 [%s] 进入半开状态，开始探测恢复", self.name)
            return self._state

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Call func through the circuit breaker."""
        state = self.state

        if state == CircuitState.OPEN:
            remaining = self.recovery_timeout - (time.time() - self._last_failure_time)
            raise CircuitOpenError(self.name, max(0, remaining))

        if state == CircuitState.HALF_OPEN:
            with self._lock:
                if self._half_open_calls >= self.half_open_max_calls:
                    remaining = self.recovery_timeout - (time.time() - self._last_failure_time)
                    raise CircuitOpenError(self.name, max(0, remaining))
                self._half_open_calls += 1

        try:
            self._call_count += 1
            self._last_call_time = time.time()
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._success_count += 1
                if self._success_count >= self.success_threshold:
                    self._state = CircuitState.CLOSED
                    self._failure_count = 0
                    logger.info("断路器 [%s] 恢复正常（CLOSED）", self.name)
            elif self._state == CircuitState.CLOSED:
                self._failure_count = 0

    def _on_failure(self):
        with self._lock:
            self._failure_count += 1
            self._last_failure_time = time.time()
            if self._state == CircuitState.HALF_OPEN:
                self._state = CircuitState.OPEN
                logger.warning("断路器 [%s] 探测失败，重新打开（OPEN）", self.name)
            elif self._failure_count >= self.failure_threshold:
                self._state = CircuitState.OPEN
                logger.warning(
                    "断路器 [%s] 连续失败 %d 次，已打开（OPEN），%d 秒后重试",
                    self.name, self._failure_count, int(self.recovery_timeout)
                )

    def get_status(self) -> dict:
        """Get current circuit breaker status."""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self._failure_count,
            "call_count": self._call_count,
            "last_call_time": self._last_call_time,
            "last_failure_time": self._last_failure_time,
        }

    def reset(self):
        """Manually reset the circuit breaker."""
        with self._lock:
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._success_count = 0
            self._half_open_calls = 0
            logger.info("断路器 [%s] 已手动重置", self.name)


# Global registry of circuit breakers
_breakers: dict[str, CircuitBreaker] = {}
_breakers_lock = threading.Lock()


def get_breaker(name: str, **kwargs) -> CircuitBreaker:
    """Get or create a named circuit breaker."""
    with _breakers_lock:
        if name not in _breakers:
            _breakers[name] = CircuitBreaker(name, **kwargs)
        return _breakers[name]


def circuit(name: str, **kwargs):
    """Decorator to wrap a function with a circuit breaker."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            breaker = get_breaker(name, **kwargs)
            return breaker.call(func, *args, **kw)
        return wrapper
    return decorator


def get_all_breaker_status() -> dict[str, dict]:
    """Get status of all registered circuit breakers."""
    with _breakers_lock:
        return {name: b.get_status() for name, b in _breakers.items()}


def get_daily_llm_cost(
    breaker_name: str = "llm_api",
    avg_tokens_per_call: int = 700,
    cost_per_1k_tokens: float = 0.03,
) -> dict:
    """从断路器统计估算每日 LLM 调用成本。

    适用于成本监控和告警。

    参数:
        breaker_name: 断路器名称
        avg_tokens_per_call: 每次调用平均 token 数
        cost_per_1k_tokens: 每 1k token 的成本（美元）

    返回:
        {"breaker": str, "total_calls": int, "estimated_tokens": int, "estimated_cost_usd": float}
    """
    with _breakers_lock:
        if breaker_name not in _breakers:
            return {"error": f"Breaker {breaker_name} not found"}
        breaker = _breakers[breaker_name]

    call_count = breaker._call_count
    estimated_tokens = call_count * avg_tokens_per_call
    estimated_cost = estimated_tokens / 1000 * cost_per_1k_tokens

    return {
        "breaker": breaker_name,
        "total_calls": call_count,
        "estimated_tokens": estimated_tokens,
        "estimated_cost_usd": round(estimated_cost, 4),
    }
