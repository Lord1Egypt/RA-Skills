#!/usr/bin/env python3
"""filelock.py — reentrant inter-process file lock (fcntl.flock).

Guards read-modify-write of state.json / trades.json against cron overlap:
the lock file is <path>.lock, held for the whole critical section (load ->
mutate -> save), not just the write.

Reentrant within one process: scripts invoked inside autonomous_runner's
already-locked cycle re-enter as a no-op instead of deadlocking on their
own flock (flock is per open-file-description).

Module:  import filelock -> with filelock.held(path): ...
"""

import fcntl
import os

_held = {}


class held:
    """Context manager: exclusive flock on <path>.lock for the block."""

    def __init__(self, path):
        self._lock_path = os.path.abspath(path) + ".lock"
        self._fd = None

    def __enter__(self):
        if self._lock_path in _held:  # already ours: reentrant no-op
            _held[self._lock_path] += 1
            return self
        fd = os.open(self._lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        fcntl.flock(fd, fcntl.LOCK_EX)
        _held[self._lock_path] = 1
        self._fd = fd
        return self

    def __exit__(self, *exc):
        if self._fd is None:
            _held[self._lock_path] -= 1
            return False
        del _held[self._lock_path]
        fcntl.flock(self._fd, fcntl.LOCK_UN)
        os.close(self._fd)
        return False
