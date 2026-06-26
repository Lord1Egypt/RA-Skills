"""File-lock mutex for serializing skill execution across concurrent cron jobs.

Primary: fcntl.flock (kernel-level advisory lock). Falls back to PID-based
stagger if fcntl is unavailable (e.g. stripped Python build, container).

Usage:
    from mutex import acquire_lock
    with acquire_lock():
        do_work()
"""

import os
import time
from contextlib import contextmanager

LOCK_FILE = os.environ.get("SKILL_MUTEX_LOCK", "/tmp/openclaw-skill.lock")
LOCK_TIMEOUT = int(os.environ.get("SKILL_MUTEX_TIMEOUT", "300"))
STAGGER_SECONDS = 30


@contextmanager
def acquire_lock(timeout: int = LOCK_TIMEOUT):
    """Block until the global skill lock is acquired, or raise on timeout.

    Falls back to PID-based stagger (up to 30 s) if fcntl.flock is
    unavailable on the current platform or filesystem.
    """
    try:
        import fcntl

        deadline = time.monotonic() + timeout
        lock_fd = os.open(LOCK_FILE, os.O_CREAT | os.O_WRONLY, 0o644)
        try:
            while True:
                try:
                    fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise TimeoutError(
                            f"Could not acquire skill lock within {timeout}s — "
                            "another job may be stuck"
                        )
                    time.sleep(1)
            yield
        finally:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)

    except (ImportError, OSError):
        # Fallback: fcntl unavailable — stagger by PID to reduce contention
        stagger = os.getpid() % STAGGER_SECONDS
        if stagger:
            time.sleep(stagger)
        yield
