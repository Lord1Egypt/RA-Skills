"""Performance optimization module for TrinityGuard.

Provides parallel detection, caching, and early exit optimizations.
"""

from __future__ import annotations

import asyncio
import functools
import hashlib
import logging
import re
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional, Tuple

from cachetools import TTLCache

logger = logging.getLogger(__name__)

# =============================================================================
# Detection Result Cache
# =============================================================================

# Cache: detection result -> (detected, timestamp)
# TTL: 5 minutes (300 seconds)
detection_cache = TTLCache(maxsize=10000, ttl=300)


def get_cache_key(text: str, fn_name: str) -> str:
    """Generate cache key for detection result.

    Args:
        text: Input text to hash
        fn_name: Detection function name

    Returns:
        Cache key string
    """
    text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    return f"{fn_name}:{text_hash}"


def cached_detect(fn: Callable) -> Callable:
    """Decorator to cache detection results.

    Args:
        fn: Detection function to cache

    Returns:
        Wrapped function with caching
    """
    @functools.wraps(fn)
    def wrapper(text: str, *args, **kwargs) -> Any:
        # Generate cache key
        cache_key = get_cache_key(text, fn.__name__)

        # Check cache
        if cache_key in detection_cache:
            logger.debug(f"Cache hit for {fn.__name__}")
            return detection_cache[cache_key]

        # Cache miss - run detection
        result = fn(text, *args, **kwargs)

        # Store in cache
        detection_cache[cache_key] = result

        return result

    return wrapper


def clear_detection_cache():
    """Clear all cached detection results."""
    detection_cache.clear()
    logger.debug("Detection cache cleared")


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics.

    Returns:
        Dictionary with cache stats
    """
    return {
        "size": len(detection_cache),
        "maxsize": detection_cache.maxsize,
        "ttl": detection_cache.ttl,
    }


# =============================================================================
# Parallel Detection
# =============================================================================

async def run_detection_async(
    fn: Callable,
    *args,
    **kwargs
) -> Tuple[str, Any]:
    """Run a single detection function asynchronously.

    Args:
        fn: Detection function to run
        *args: Positional arguments for fn
        **kwargs: Keyword arguments for fn

    Returns:
        Tuple of (function_name, result)
    """
    try:
        result = fn(*args, **kwargs)
        return (fn.__name__, result)
    except Exception as e:
        logger.error(f"Detection error in {fn.__name__}: {e}")
        return (fn.__name__, None)


async def parallel_detect_async(
    text: str,
    policy: Dict[str, Any],
    detectors: Optional[List[Callable]] = None,
) -> Dict[str, Any]:
    """Run multiple detection functions in parallel (async).

    Args:
        text: Text to analyze
        policy: Security policy configuration
        detectors: List of detection functions (optional)

    Returns:
        Dictionary mapping function names to results
    """
    # Default detectors if not provided
    if detectors is None:
        # Import here to avoid circular imports
        from self_guard_runtime_hook_template import (
            detect_jwt_token,
            detect_database_connection,
            detect_email_addresses,
            detect_ip_addresses,
            detect_credit_card,
            detect_environment_variables,
        )
        detectors = [
            detect_jwt_token,
            detect_database_connection,
            detect_email_addresses,
            detect_ip_addresses,
            detect_credit_card,
            detect_environment_variables,
        ]

    # Create tasks for all detectors
    tasks = [run_detection_async(detector, text) for detector in detectors]

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks)

    # Convert to dictionary
    return dict(results)


def parallel_detect(
    text: str,
    policy: Dict[str, Any],
    detectors: Optional[List[Callable]] = None,
    max_workers: int = 4,
) -> Dict[str, Any]:
    """Run multiple detection functions in parallel (sync wrapper).

    Args:
        text: Text to analyze
        policy: Security policy configuration
        detectors: List of detection functions (optional)
        max_workers: Maximum number of worker threads

    Returns:
        Dictionary mapping function names to results
    """
    # Run async function in new event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(
        parallel_detect_async(text, policy, detectors)
    )


def parallel_detect_threadpool(
    text: str,
    policy: Dict[str, Any],
    detectors: Optional[List[Callable]] = None,
    max_workers: int = 4,
) -> Dict[str, Any]:
    """Run multiple detection functions in parallel using ThreadPoolExecutor.

    Args:
        text: Text to analyze
        policy: Security policy configuration
        detectors: List of detection functions (optional)
        max_workers: Maximum number of worker threads

    Returns:
        Dictionary mapping function names to results
    """
    if detectors is None:
        # Import here to avoid circular imports
        from self_guard_runtime_hook_template import (
            detect_jwt_token,
            detect_database_connection,
            detect_email_addresses,
            detect_ip_addresses,
            detect_credit_card,
            detect_environment_variables,
        )
        detectors = [
            detect_jwt_token,
            detect_database_connection,
            detect_email_addresses,
            detect_ip_addresses,
            detect_credit_card,
            detect_environment_variables,
        ]

    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all detection jobs
        future_to_fn = {
            executor.submit(detector, text): detector
            for detector in detectors
        }

        # Collect results as they complete
        for future in future_to_fn:
            fn = future_to_fn[future]
            try:
                result = future.result()
                results[fn.__name__] = result
            except Exception as e:
                logger.error(f"Detection error in {fn.__name__}: {e}")
                results[fn.__name__] = None

    return results


# =============================================================================
# Early Exit Optimization
# =============================================================================

# High-risk patterns that justify immediate blocking
EARLY_EXIT_PATTERNS = [
    # Direct credential disclosure
    r"(?i)(直接|显示|输出|打印|列出|打印|dump|show|print|list|export).*(密码|password|token|密钥|key|secret|凭证)[\s，。]*",
    # Exfiltration patterns
    r"(?i)(提取|获取|export|exfil|dump|steal).*(password|token|key|secret|credential)",
    # Bypass security
    r"(?i)(绕过|bypass|ignore|skip).*(安全|security|check|验证|verify)",
]


def early_high_risk_check(text: str) -> Tuple[bool, str]:
    """Fast high-risk pattern detection for early exit.

    This should be called FIRST before any other detection.
    If returns True, can immediately block without further checks.

    Args:
        text: Input text to check

    Returns:
        Tuple of (should_block, reason)
    """
    text_low = text.lower()

    for pattern in EARLY_EXIT_PATTERNS:
        if re.search(pattern, text_low):
            match = re.search(pattern, text_low)
            reason = f"Early exit: High-risk pattern detected: {match.group(0)[:50]}"
            logger.warning(f"Early exit triggered: {reason}")
            return (True, reason)

    return (False, "")


def should_early_exit(
    user_prompt: str,
    planned_actions: List[str],
    policy: Dict[str, Any],
) -> Tuple[bool, str]:
    """Determine if request should be blocked early (skip runtime/output stages).

    Args:
        user_prompt: User's input prompt
        planned_actions: List of planned actions
        policy: Security policy configuration

    Returns:
        Tuple of (should_exit, reason)
    """
    # Check 1: High-risk action + sensitive context
    high_risk_actions = {str(x) for x in policy.get("high_risk_actions", [])}
    has_high_risk_action = any(a in high_risk_actions for a in planned_actions)

    if has_high_risk_action:
        # Check if prompt has disclosure intent
        explicit_phrases = [str(x).lower() for x in policy.get("explicit_disclosure_phrases", [])]
        prompt_low = user_prompt.lower()

        for phrase in explicit_phrases:
            if phrase in prompt_low:
                reason = f"Early exit: High-risk action '{has_high_risk_action}' with explicit disclosure phrase '{phrase}'"
                return (True, reason)

    # Check 2: Direct high-risk patterns
    should_block, reason = early_high_risk_check(user_prompt)
    if should_block:
        return (True, reason)

    # Check 3: Credential exfil intent
    from self_guard_runtime_hook_template import is_credential_exfil_request
    if is_credential_exfil_request(user_prompt.lower()):
        reason = "Early exit: Credential exfiltration intent detected"
        return (True, reason)

    return (False, "")


# =============================================================================
# Performance Monitoring
# =============================================================================

class PerformanceMonitor:
    """Monitor and track detection performance."""

    def __init__(self):
        self.detection_times: Dict[str, List[float]] = {}
        self.cache_hits: int = 0
        self.cache_misses: int = 0
        self.early_exits: int = 0

    def record_detection_time(self, fn_name: str, duration_ms: float):
        """Record detection execution time.

        Args:
            fn_name: Detection function name
            duration_ms: Execution time in milliseconds
        """
        if fn_name not in self.detection_times:
            self.detection_times[fn_name] = []

        self.detection_times[fn_name].append(duration_ms)

    def record_cache_hit(self):
        """Record a cache hit."""
        self.cache_hits += 1

    def record_cache_miss(self):
        """Record a cache miss."""
        self.cache_misses += 1

    def record_early_exit(self):
        """Record an early exit event."""
        self.early_exits += 1

    def get_stats(self) -> Dict[str, Any]:
        """Get performance statistics.

        Returns:
            Dictionary with performance stats
        """
        stats = {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate": (
                self.cache_hits / (self.cache_hits + self.cache_misses)
                if (self.cache_hits + self.cache_misses) > 0
                else 0
            ),
            "early_exits": self.early_exits,
        }

        # Add detection time stats
        if self.detection_times:
            stats["detection_times"] = {}
            for fn_name, times in self.detection_times.items():
                stats["detection_times"][fn_name] = {
                    "count": len(times),
                    "avg_ms": sum(times) / len(times),
                    "min_ms": min(times),
                    "max_ms": max(times),
                }

        return stats


# Global performance monitor
performance_monitor = PerformanceMonitor()


# =============================================================================
# Utility Functions
# =============================================================================

def timed_detect(fn: Callable) -> Callable:
    """Decorator to time detection execution.

    Args:
        fn: Detection function to time

    Returns:
        Wrapped function with timing
    """
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        import time

        start = time.perf_counter()
        result = fn(*args, **kwargs)
        end = time.perf_counter()

        duration_ms = (end - start) * 1000
        performance_monitor.record_detection_time(fn.__name__, duration_ms)

        return result

    return wrapper
