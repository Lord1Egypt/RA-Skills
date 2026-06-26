"""Resource management and limits for TrinityGuard."""

from __future__ import annotations

import contextlib
import functools
import logging
import os
import resource
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Generator, Optional

from exceptions import ResourceLimitError, MemoryLimitError, TimeoutError

logger = logging.getLogger(__name__)

# Default resource limits
DEFAULT_MAX_MEMORY_MB = 1024  # 1GB
DEFAULT_MAX_CPU_TIME = 30  # 30 seconds
DEFAULT_MAX_FILE_SIZE_MB = 100  # 100MB
DEFAULT_MAX_TEXT_LENGTH = 1_000_000  # 1M characters
DEFAULT_MAX_ARRAY_SIZE = 10000  # Maximum array length


class ResourceLimits:
    """Manage resource limits for TrinityGuard operations."""

    def __init__(
        self,
        max_memory_mb: Optional[int] = None,
        max_cpu_time: Optional[int] = None,
        max_file_size_mb: Optional[int] = None,
    ):
        """Initialize resource limits.

        Args:
            max_memory_mb: Maximum memory in MB
            max_cpu_time: Maximum CPU time in seconds
            max_file_size_mb: Maximum file size in MB
        """
        self.max_memory_mb = max_memory_mb or DEFAULT_MAX_MEMORY_MB
        self.max_cpu_time = max_cpu_time or DEFAULT_MAX_CPU_TIME
        self.max_file_size_mb = max_file_size_mb or DEFAULT_MAX_FILE_SIZE_MB

        # Original limits (for restoration)
        self._original_limits = {}

    def set_limits(self) -> None:
        """Set resource limits for the current process."""
        try:
            # Memory limit
            if self.max_memory_mb:
                memory_bytes = self.max_memory_mb * 1024 * 1024
                soft, hard = resource.getrlimit(resource.RLIMIT_AS)
                self._original_limits['RLIMIT_AS'] = (soft, hard)
                resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, hard))
                logger.debug(f"Set memory limit to {self.max_memory_mb}MB")

            # CPU time limit
            if self.max_cpu_time:
                soft, hard = resource.getrlimit(resource.RLIMIT_CPU)
                self._original_limits['RLIMIT_CPU'] = (soft, hard)
                resource.setrlimit(resource.RLIMIT_CPU, (self.max_cpu_time, hard))
                logger.debug(f"Set CPU time limit to {self.max_cpu_time}s")

        except (ValueError, OSError) as e:
            logger.warning(f"Failed to set resource limits: {e}")

    def restore_limits(self) -> None:
        """Restore original resource limits."""
        try:
            for limit_type, (soft, hard) in self._original_limits.items():
                if limit_type == 'RLIMIT_AS':
                    resource.setrlimit(resource.RLIMIT_AS, (soft, hard))
                elif limit_type == 'RLIMIT_CPU':
                    resource.setrlimit(resource.RLIMIT_CPU, (soft, hard))
                logger.debug(f"Restored {limit_type}")
        except (ValueError, OSError) as e:
            logger.warning(f"Failed to restore resource limits: {e}")

    def check_memory_usage(self) -> int:
        """Check current memory usage.

        Returns:
            Memory usage in MB
        """
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except ImportError:
            # Fallback: estimate using /proc (Linux only)
            try:
                with open('/proc/self/status') as f:
                    for line in f:
                        if line.startswith('VmRSS:'):
                            kb = int(line.split()[1])
                            return kb // 1024
            except Exception:
                pass
        except Exception:
            pass

        return 0


class ResourceMonitor:
    """Monitor resource usage during operations."""

    def __init__(
        self,
        max_memory_mb: int = DEFAULT_MAX_MEMORY_MB,
        check_interval: float = 1.0,
    ):
        """Initialize resource monitor.

        Args:
            max_memory_mb: Maximum allowed memory in MB
            check_interval: How often to check resources (seconds)
        """
        self.max_memory_mb = max_memory_mb
        self.check_interval = check_interval
        self._monitoring = False
        self._start_time = None
        self._peak_memory = 0

    def start(self) -> None:
        """Start monitoring resources."""
        self._monitoring = True
        self._start_time = time.time()
        self._peak_memory = 0
        logger.debug("Started resource monitoring")

    def stop(self) -> Dict[str, Any]:
        """Stop monitoring and return statistics.

        Returns:
            Resource usage statistics
        """
        self._monitoring = False
        elapsed = time.time() - self._start_time if self._start_time else 0

        stats = {
            "elapsed_seconds": elapsed,
            "peak_memory_mb": self._peak_memory,
            "max_memory_mb": self.max_memory_mb,
        }

        logger.debug(f"Stopped resource monitoring: {stats}")
        return stats

    def check(self) -> None:
        """Check resource usage and raise exception if limits exceeded."""
        if not self._monitoring:
            return

        # Check memory
        memory_mb = self._get_memory_usage()
        self._peak_memory = max(self._peak_memory, memory_mb)

        if memory_mb > self.max_memory_mb:
            raise MemoryLimitError(
                f"Memory limit exceeded: {memory_mb:.2f}MB / {self.max_memory_mb}MB",
                details={
                    "used_mb": memory_mb,
                    "limit_mb": self.max_memory_mb
                }
            )

        # Check elapsed time (soft limit)
        if self._start_time and self.max_cpu_time:
            elapsed = time.time() - self._start_time
            if elapsed > self.max_cpu_time * 0.9:  # Warning at 90%
                logger.warning(f"Approaching CPU time limit: {elapsed:.2f}s / {self.max_cpu_time}s")

    def _get_memory_usage(self) -> int:
        """Get current memory usage in MB."""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / (1024 * 1024)
        except Exception:
            return 0


@contextlib.contextmanager
def resource_context(
    max_memory_mb: Optional[int] = None,
    max_cpu_time: Optional[int] = None,
) -> Generator[ResourceMonitor, None, None]:
    """Context manager for resource-limited operations.

    Args:
        max_memory_mb: Maximum memory in MB
        max_cpu_time: Maximum CPU time in seconds

    Yields:
        ResourceMonitor instance
    """
    monitor = ResourceMonitor(max_memory_mb=max_memory_mb)
    limits = ResourceLimits(max_memory_mb=max_memory_mb, max_cpu_time=max_cpu_time)

    limits.set_limits()
    monitor.start()

    try:
        yield monitor
    finally:
        monitor.stop()
        limits.restore_limits()


@contextlib.contextmanager
def temp_file(
    suffix: str = "",
    prefix: str = "trinityguard_",
    delete_on_exit: bool = True,
) -> Generator[Path, None, None]:
    """Context manager for temporary file creation.

    Args:
        suffix: File suffix (e.g., ".json")
        prefix: File prefix
        delete_on_exit: Whether to delete file on exit

    Yields:
        Path to temporary file
    """
    fd = None
    path = None

    try:
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
        yield Path(path)
    finally:
        # Close file descriptor
        if fd is not None:
            try:
                os.close(fd)
            except Exception:
                pass

        # Delete file
        if delete_on_exit and path and Path(path).exists():
            try:
                Path(path).unlink()
            except Exception as e:
                logger.warning(f"Failed to delete temp file {path}: {e}")


def limit_text_length(text: str, max_length: int = DEFAULT_MAX_TEXT_LENGTH) -> str:
    """Limit text length to prevent memory issues.

    Args:
        text: Text to limit
        max_length: Maximum length

    Returns:
        Truncated text if needed
    """
    if not isinstance(text, str):
        text = str(text)

    if len(text) > max_length:
        logger.warning(f"Text truncated from {len(text)} to {max_length} characters")
        # Truncate to max_length - len(suffix) to ensure result doesn't exceed max_length
        suffix = "... [truncated]"
        truncated_max = max_length - len(suffix)
        return text[:max(0, truncated_max)] + suffix

    return text


def limit_array_size(arr: list, max_size: int = DEFAULT_MAX_ARRAY_SIZE) -> list:
    """Limit array size to prevent memory issues.

    Args:
        arr: Array to limit
        max_size: Maximum size

    Returns:
        Truncated array if needed
    """
    if not isinstance(arr, list):
        return arr

    if len(arr) > max_size:
        logger.warning(f"Array truncated from {len(arr)} to {max_size} items")
        return arr[:max_size]

    return arr


def check_disk_space(path: Path, min_space_mb: int = 100) -> None:
    """Check available disk space.

    Args:
        path: Path to check
        min_space_mb: Minimum required space in MB

    Raises:
        ResourceLimitError: If insufficient disk space
    """
    try:
        stat = os.statvfs(path)
        available_mb = stat.f_bavail * stat.f_frsize / (1024 * 1024)

        if available_mb < min_space_mb:
            raise ResourceLimitError(
                f"Insufficient disk space: {available_mb:.2f}MB available, {min_space_mb}MB required",
                details={
                    "available_mb": available_mb,
                    "required_mb": min_space_mb,
                    "path": str(path)
                }
            )
    except Exception as e:
        if isinstance(e, ResourceLimitError):
            raise
        logger.warning(f"Could not check disk space: {e}")


# Decorator for resource-limited operations

def with_resource_limits(
    max_memory_mb: Optional[int] = None,
    max_cpu_time: Optional[int] = None,
):
    """Decorator to apply resource limits to a function.

    Args:
        max_memory_mb: Maximum memory in MB
        max_cpu_time: Maximum CPU time in seconds
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with resource_context(max_memory_mb=max_memory_mb, max_cpu_time=max_cpu_time) as monitor:
                # Call function periodically checking resources
                result = func(*args, **kwargs)
                monitor.check()
                return result
        return wrapper
    return decorator
