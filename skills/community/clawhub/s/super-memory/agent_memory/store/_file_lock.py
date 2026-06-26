"""Cross-platform file locking for SQLite databases."""

from __future__ import annotations

import os
import sys
import time
import threading
import logging

logger = logging.getLogger(__name__)

if sys.platform != "win32":
    import fcntl
    _HAS_FCNTL = True
    _HAS_MSVCRT = False
else:
    _HAS_FCNTL = False
    try:
        import msvcrt
        _HAS_MSVCRT = True
    except ImportError:
        _HAS_MSVCRT = False


class _FileLock:
    """跨进程文件锁 — 仅用于注册表等非 SQLite 资源。

    SQLite 写入不再使用文件锁（依赖 WAL 模式 + busy_timeout），
    避免全局串行化导致的多 Agent 卡死问题。

    Unix: fcntl.flock
    Windows: msvcrt.locking + threading.Lock fallback
    """

    def __init__(self, lock_path: str, timeout: float = 3.0):
        self._lock_path = lock_path
        self._timeout = timeout
        self._fd = None
        self._thread_lock = threading.Lock()
        self._acquired = False

    def acquire(self):
        if _HAS_MSVCRT:
            self._fd = open(self._lock_path, "w")
            deadline = time.time() + self._timeout
            while True:
                try:
                    msvcrt.locking(self._fd.fileno(), msvcrt.LK_NBLCK, 1)
                    self._acquired = True
                    return
                except (IOError, OSError):
                    if time.time() >= deadline:
                        self._fd.close()
                        raise TimeoutError(f"获取文件锁超时: {self._lock_path}")
                    time.sleep(0.05)
        if not _HAS_FCNTL:
            self._thread_lock.acquire()
            self._acquired = True
            return
        self._fd = open(self._lock_path, "w")
        deadline = time.time() + self._timeout
        retry_delay = 0.05
        while True:
            try:
                fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return
            except (IOError, OSError):
                if time.time() >= deadline:
                    self._fd.close()
                    self._cleanup_stale_lock()
                    self._fd = open(self._lock_path, "w")
                    try:
                        fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        return
                    except (IOError, OSError):
                        self._fd.close()
                        raise TimeoutError(f"获取文件锁超时: {self._lock_path}")
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 1.5, 1.0)

    def _cleanup_stale_lock(self):
        try:
            if os.path.exists(self._lock_path):
                mtime = os.path.getmtime(self._lock_path)
                if time.time() - mtime > self._timeout * 2:
                    os.unlink(self._lock_path)
                    logger.debug(f"清理 stale lock: {self._lock_path}")
        except Exception as e:
            logger.warning("store: %s", e)

    def release(self):
        if _HAS_MSVCRT:
            if self._acquired and self._fd:
                try:
                    msvcrt.locking(self._fd.fileno(), msvcrt.LK_UNLCK, 1)
                except Exception as e:
                    logger.warning("store: %s", e)
                try:
                    self._fd.close()
                except Exception:
                    pass
                self._acquired = False
            return
        if not _HAS_FCNTL:
            try:
                self._thread_lock.release()
            except Exception as e:
                logger.warning("store: %s", e)
            self._acquired = False
            return
        if self._fd:
            try:
                fcntl.flock(self._fd, fcntl.LOCK_UN)
                self._fd.close()
            except Exception as e:
                logger.warning("store: %s", e)
            self._fd = None

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, *args):
        self.release()
