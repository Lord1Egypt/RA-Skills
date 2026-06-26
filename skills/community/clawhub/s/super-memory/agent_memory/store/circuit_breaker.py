"""Circuit breaker for SQLite store operations.

Protects the system from cascading failures when SQLite is slow or unresponsive.
States: CLOSED (normal) -> OPEN (failing) -> HALF_OPEN (testing recovery)
"""

import time
import threading
import logging

logger = logging.getLogger(__name__)


class StoreCircuitBreaker:
    """Circuit breaker for database operations.

    CLOSED: Operations execute normally. Failures increment failure count.
    OPEN: Operations are rejected immediately. After cooldown, transitions to HALF_OPEN.
    HALF_OPEN: One test operation is allowed. If it succeeds, transitions to CLOSED.
               If it fails, transitions back to OPEN.
    """

    def __init__(self, failure_threshold=5, recovery_timeout=30.0, half_open_max=1, name="store"):
        self.name = name
        self._failure_threshold = failure_threshold
        self._recovery_timeout = recovery_timeout
        self._half_open_max = half_open_max

        self._state = "closed"  # closed / open / half_open
        self._failure_count = 0
        self._last_failure_time = 0.0
        self._half_open_count = 0
        self._lock = threading.Lock()

        # Stats
        self._total_calls = 0
        self._total_rejected = 0
        self._total_failures = 0

    @property
    def state(self):
        """Current circuit breaker state."""
        with self._lock:
            if self._state == "open":
                # Check if cooldown has elapsed
                if time.time() - self._last_failure_time >= self._recovery_timeout:
                    self._state = "half_open"
                    self._half_open_count = 0
            return self._state

    def allow_request(self):
        """Check if a request should be allowed.

        Returns:
            True if request should proceed, False if it should be rejected
        """
        with self._lock:
            self._total_calls += 1
            state = self.state

            if state == "closed":
                return True
            elif state == "open":
                self._total_rejected += 1
                return False
            elif state == "half_open":
                if self._half_open_count < self._half_open_max:
                    self._half_open_count += 1
                    return True
                self._total_rejected += 1
                return False
            return True

    def record_success(self):
        """Record a successful operation."""
        with self._lock:
            if self._state == "half_open":
                self._state = "closed"
            self._failure_count = 0

    def record_failure(self):
        """Record a failed operation."""
        with self._lock:
            self._failure_count += 1
            self._total_failures += 1
            self._last_failure_time = time.time()

            if self._failure_count >= self._failure_threshold:
                self._state = "open"
                logger.warning(
                    "Store circuit breaker OPENED after %d failures",
                    self._failure_count,
                )
                try:
                    from agent_memory.observability.alerting import get_alert_manager
                    get_alert_manager().alert_circuit_breaker_open(self.name)
                except Exception:
                    pass

    @property
    def stats(self):
        """Return circuit breaker statistics."""
        return {
            "state": self.state,
            "failure_count": self._failure_count,
            "total_calls": self._total_calls,
            "total_rejected": self._total_rejected,
            "total_failures": self._total_failures,
        }


def retry_with_backoff(fn, max_retries=3, base_delay=0.1, circuit_breaker=None):
    """Execute a function with retry and optional circuit breaker.

    Args:
        fn: Callable to execute
        max_retries: Maximum number of retries
        base_delay: Base delay for exponential backoff (seconds)
        circuit_breaker: Optional StoreCircuitBreaker instance

    Returns:
        Result of fn()

    Raises:
        Exception: If all retries exhausted or circuit breaker is open
    """
    import sqlite3

    # Check circuit breaker
    if circuit_breaker and not circuit_breaker.allow_request():
        raise RuntimeError("熔断器已开启 — 数据库操作被拒绝")

    last_error = None
    for attempt in range(max_retries + 1):
        try:
            result = fn()
            if circuit_breaker:
                circuit_breaker.record_success()
            return result
        except sqlite3.OperationalError as e:
            last_error = e
            error_msg = str(e).lower()

            # Only retry on lock/busy errors, not on schema errors
            is_retryable = any(kw in error_msg for kw in ["locked", "busy", "timeout"])
            if not is_retryable:
                if circuit_breaker:
                    circuit_breaker.record_failure()
                raise

            if attempt < max_retries:
                delay = base_delay * (2 ** attempt)
                logger.debug("SQLite busy/locked, retrying in %.1fs (attempt %d/%d)",
                           delay, attempt + 1, max_retries)
                time.sleep(delay)
            else:
                if circuit_breaker:
                    circuit_breaker.record_failure()
                logger.error("SQLite operation failed after %d retries: %s", max_retries, e)
                raise
        except Exception as e:
            if circuit_breaker:
                circuit_breaker.record_failure()
            raise

    raise last_error
