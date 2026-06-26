"""Prometheus metrics export for TrinityGuard.

This module provides Prometheus metrics for monitoring TrinityGuard performance
and decision-making patterns.
"""

from __future__ import annotations

import os
import time
from functools import wraps
from typing import Callable, Dict, Any, List

try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry, REGISTRY
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False
    # Create dummy classes for graceful degradation
    class Counter:
        def __init__(self, *args, **kwargs): pass
        def labels(self, *args, **kwargs): return self
        def inc(self, amount=1): pass
        def __call__(self, *args, **kwargs): return self

    class Histogram:
        def __init__(self, *args, **kwargs): pass
        def labels(self, *args, **kwargs): return self
        def observe(self, amount): pass
        def time(self): return self
        def __call__(self, *args, **kwargs): return self

    class Gauge:
        def __init__(self, *args, **kwargs): pass
        def labels(self, *args, **kwargs): return self
        def set(self, value): pass
        def inc(self, amount=1): pass
        def dec(self, amount=1): pass
        def __call__(self, *args, **kwargs): return self


if PROMETHEUS_AVAILABLE:
    # Counter metrics
    invocations_total = Counter(
        'trinityguard_invocations_total',
        'Total number of TrinityGuard invocations',
        ['environment', 'version']
    )

    detection_total = Counter(
        'trinityguard_detection_total',
        'Total number of detections',
        ['type', 'result']
    )

    decision_total = Counter(
        'trinityguard_decision_total',
        'Total number of decisions',
        ['stage', 'decision', 'reason']
    )

    early_exit_total = Counter(
        'trinityguard_early_exit_total',
        'Total number of early exit checks',
        ['triggered', 'reason']
    )

    cache_operations_total = Counter(
        'trinityguard_cache_operations_total',
        'Total number of cache operations',
        ['operation', 'cache_type']
    )

    # Histogram metrics
    latency_histogram = Histogram(
        'trinityguard_latency_seconds',
        'Request latency in seconds',
        ['stage'],
        buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
    )

    detection_duration = Histogram(
        'trinityguard_detection_duration_seconds',
        'Detection duration in seconds',
        ['type'],
        buckets=[0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
    )

    user_prompt_length = Histogram(
        'trinityguard_user_prompt_length_bytes',
        'User prompt length in bytes',
        buckets=[10, 50, 100, 500, 1000, 5000, 10000, 50000]
    )

    # Gauge metrics
    cache_size = Gauge(
        'trinityguard_cache_size',
        'Current cache size',
        ['cache_type']
    )

    active_sessions = Gauge(
        'trinityguard_active_sessions',
        'Number of active sessions'
    )

    last_error_timestamp = Gauge(
        'trinityguard_last_error_timestamp_seconds',
        'Timestamp of last error',
        ['error_type']
    )


def get_environment() -> str:
    """Get current environment from env var or default."""
    return os.environ.get('TRINITYGUARD_ENVIRONMENT', 'development')


def get_version() -> str:
    """Get version from env var or default."""
    return os.environ.get('TRINITYGUARD_VERSION', '3.2.0')


def record_invocation() -> None:
    """Record a new invocation."""
    if PROMETHEUS_AVAILABLE:
        invocations_total.labels(
            environment=get_environment(),
            version=get_version()
        ).inc()


def record_detection(detection_type: str, result: str) -> None:
    """Record a detection result.

    Args:
        detection_type: Type of detection (e.g., 'sql_injection', 'jwt_token')
        result: Result ('detected' or 'not_detected')
    """
    if PROMETHEUS_AVAILABLE:
        detection_total.labels(type=detection_type, result=result).inc()


def record_decision(stage: str, decision: str, reason: str = '') -> None:
    """Record a decision.

    Args:
        stage: Stage ('preflight', 'runtime', 'output')
        decision: Decision ('allow', 'downgrade', 'block', 'stop')
        reason: Optional reason for the decision
    """
    if PROMETHEUS_AVAILABLE:
        decision_total.labels(stage=stage, decision=decision, reason=reason).inc()


def record_early_exit(triggered: bool, reason: str = '') -> None:
    """Record an early exit check.

    Args:
        triggered: Whether early exit was triggered
        reason: Reason for early exit
    """
    if PROMETHEUS_AVAILABLE:
        triggered_str = 'true' if triggered else 'false'
        early_exit_total.labels(triggered=triggered_str, reason=reason).inc()


def record_cache_operation(operation: str, cache_type: str) -> None:
    """Record a cache operation.

    Args:
        operation: Operation ('hit', 'miss', 'set', 'delete')
        cache_type: Cache type ('detection', 'pattern')
    """
    if PROMETHEUS_AVAILABLE:
        cache_operations_total.labels(operation=operation, cache_type=cache_type).inc()


def observe_latency(stage: str, duration_seconds: float) -> None:
    """Record latency for a stage.

    Args:
        stage: Stage ('preflight', 'runtime', 'output', 'total')
        duration_seconds: Duration in seconds
    """
    if PROMETHEUS_AVAILABLE:
        latency_histogram.labels(stage=stage).observe(duration_seconds)


def observe_detection_duration(detection_type: str, duration_seconds: float) -> None:
    """Record detection duration.

    Args:
        detection_type: Type of detection
        duration_seconds: Duration in seconds
    """
    if PROMETHEUS_AVAILABLE:
        detection_duration.labels(type=detection_type).observe(duration_seconds)


def observe_user_prompt_length(length_bytes: int) -> None:
    """Record user prompt length.

    Args:
        length_bytes: Prompt length in bytes
    """
    if PROMETHEUS_AVAILABLE:
        user_prompt_length.observe(length_bytes)


def set_cache_size(cache_type: str, size: int) -> None:
    """Set current cache size.

    Args:
        cache_type: Cache type ('detection', 'pattern')
        size: Cache size
    """
    if PROMETHEUS_AVAILABLE:
        cache_size.labels(cache_type=cache_type).set(size)


def set_active_sessions(count: int) -> None:
    """Set number of active sessions.

    Args:
        count: Number of active sessions
    """
    if PROMETHEUS_AVAILABLE:
        active_sessions.set(count)


def set_last_error(error_type: str, timestamp_seconds: float) -> None:
    """Set timestamp of last error.

    Args:
        error_type: Type of error
        timestamp_seconds: Unix timestamp
    """
    if PROMETHEUS_AVAILABLE:
        last_error_timestamp.labels(error_type=error_type).set(timestamp_seconds)


def metrics_context(manager):
    """Context manager for timing operations.

    Args:
        manager: The metric to use (e.g., latency_histogram)

    Example:
        with metrics_context(latency_histogram.labels(stage='preflight')):
            # do work
            pass
    """
    if PROMETHEUS_AVAILABLE:
        return manager.time()
    else:
        return DummyContextManager()


class DummyContextManager:
    """Dummy context manager for when Prometheus is not available."""
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass


def get_metrics_text() -> bytes:
    """Get Prometheus metrics text.

    Returns:
        Metrics in Prometheus text format
    """
    if PROMETHEUS_AVAILABLE:
        return generate_latest(REGISTRY)
    else:
        return b'# Prometheus metrics not available\n'


def get_metrics_content_type() -> str:
    """Get Prometheus metrics content type.

    Returns:
        Content type string
    """
    if PROMETHEUS_AVAILABLE:
        return CONTENT_TYPE_LATEST
    else:
        return 'text/plain'


# Decorator for timing functions
def timed(stage: str, metric_histogram=None):
    """Decorator to time function execution.

    Args:
        stage: Stage name for the metric
        metric_histogram: Optional histogram to use (defaults to latency_histogram)

    Example:
        @timed('preflight')
        def preflight_decision(...):
            ...
    """
    if not PROMETHEUS_AVAILABLE:
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    if metric_histogram is None:
        metric_histogram = latency_histogram

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                duration = time.perf_counter() - start
                metric_histogram.labels(stage=stage).observe(duration)
        return wrapper
    return decorator


# Decorator for recording detections
def count_detections(detection_type: str):
    """Decorator to count detections in a function.

    Args:
        detection_type: Type of detection (e.g., 'sql_injection')

    Example:
        @count_detections('sql_injection')
        def detect_sql_injection(text):
            ...
    """
    if not PROMETHEUS_AVAILABLE:
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Handle both bool and dict return types
            if isinstance(result, bool):
                detected = result
            elif isinstance(result, dict):
                detected = result.get('detected', False)
            else:
                detected = False

            result_str = 'detected' if detected else 'not_detected'
            record_detection(detection_type, result_str)
            return result
        return wrapper
    return decorator


def is_available() -> bool:
    """Check if Prometheus metrics are available.

    Returns:
        True if prometheus_client is installed
    """
    return PROMETHEUS_AVAILABLE


__all__ = [
    # Metrics
    'invocations_total',
    'detection_total',
    'decision_total',
    'early_exit_total',
    'cache_operations_total',
    'latency_histogram',
    'detection_duration',
    'user_prompt_length',
    'cache_size',
    'active_sessions',
    'last_error_timestamp',
    # Functions
    'record_invocation',
    'record_detection',
    'record_decision',
    'record_early_exit',
    'record_cache_operation',
    'observe_latency',
    'observe_detection_duration',
    'observe_user_prompt_length',
    'set_cache_size',
    'set_active_sessions',
    'set_last_error',
    'get_metrics_text',
    'get_metrics_content_type',
    'metrics_context',
    'timed',
    'count_detections',
    'is_available',
]
