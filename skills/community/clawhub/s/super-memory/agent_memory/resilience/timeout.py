"""Timeout utility for wrapping synchronous calls with a deadline."""

import threading
import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)

_MAX_TIMEOUT_THREADS = 20
_active_timeout_threads = 0
_timeout_threads_lock = threading.Lock()


class TimeoutError(Exception):
    """Raised when a call exceeds its deadline."""
    def __init__(self, timeout: float, func_name: str = ""):
        self.timeout = timeout
        self.func_name = func_name
        super().__init__(
            f"操作超时（{timeout:.1f}秒）" + (f": {func_name}" if func_name else "")
        )


def timeout_call(
    func: Callable,
    *args,
    timeout: float = 10.0,
    default: Any = None,
    func_name: str = "",
    on_timeout: Callable = None,
    **kwargs,
) -> Any:
    """Call func with a timeout. Returns default if timeout exceeded.

    Uses a daemon thread to execute the function. If the thread doesn't
    complete within timeout seconds, returns default value.

    WARNING: This uses thread-based timeout. The function may continue
    running in the background after timeout. For truly cancellable operations,
    use async with asyncio.wait_for() instead.

    Args:
        func: Function to call
        timeout: Maximum seconds to wait
        default: Value to return on timeout
        func_name: Name for error messages
        on_timeout: Optional callback invoked on timeout (e.g., to cancel the operation)
        *args, **kwargs: Arguments to pass to func

    Returns:
        Result of func(*args, **kwargs), or default on timeout
    """
    global _active_timeout_threads
    with _timeout_threads_lock:
        if _active_timeout_threads >= _MAX_TIMEOUT_THREADS:
            logger.warning(
                "超时线程数已达上限(%d)，直接返回默认值: %s",
                _MAX_TIMEOUT_THREADS, func_name
            )
            return default
        _active_timeout_threads += 1

    result = [default]
    exception = [None]
    completed = [False]

    def _worker():
        global _active_timeout_threads
        try:
            result[0] = func(*args, **kwargs)
            completed[0] = True
        except Exception as e:
            exception[0] = e
        finally:
            with _timeout_threads_lock:
                _active_timeout_threads -= 1

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
    thread.join(timeout=timeout)

    if thread.is_alive():
        # Thread is still running — it timed out
        logger.warning(
            "操作超时（%.1fs）: %s，返回默认值",
            timeout, func_name or func.__name__
        )
        # Call on_timeout callback if provided (e.g., to cancel API request)
        if on_timeout:
            try:
                on_timeout()
            except Exception:
                pass
        return default

    if exception[0] is not None:
        raise exception[0]

    return result[0]


def llm_call_with_timeout(llm_fn, prompt, timeout=10.0, **kwargs):
    """Specialized timeout wrapper for LLM API calls.

    Uses the LLM provider's native timeout when available,
    falling back to thread-based timeout.
    """
    # Try to use native timeout if the function supports it
    if hasattr(llm_fn, '__self__') and hasattr(llm_fn.__self__, 'timeout'):
        # OpenAI client has a timeout parameter
        original_timeout = llm_fn.__self__.timeout
        try:
            llm_fn.__self__.timeout = timeout
            return llm_fn(prompt, **kwargs)
        finally:
            llm_fn.__self__.timeout = original_timeout

    # Fallback to thread-based timeout
    return timeout_call(
        llm_fn, prompt,
        timeout=timeout,
        default=None,
        func_name="llm_api_call",
        **kwargs,
    )
