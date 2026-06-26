"""Single-instance lock for monitor process (fcntl on Unix)."""

from __future__ import annotations

import os
from pathlib import Path

_LOCK_FD = None


def acquire_monitor_lock(project_root: Path, lock_name: str = "tg_monitor.lock") -> None:
    global _LOCK_FD
    try:
        import fcntl
    except ImportError:
        return
    lock_path = project_root / lock_name
    _LOCK_FD = open(lock_path, "w")
    try:
        fcntl.flock(_LOCK_FD.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        _LOCK_FD.close()
        _LOCK_FD = None
        print(
            "❌ 已有监控进程在运行，或锁文件仍被占用。\n"
            "   请先结束旧进程，或关闭其他使用同一 session 的 Python 脚本后再启动。"
        )
        raise SystemExit(1) from None
    _LOCK_FD.write(str(os.getpid()))
    _LOCK_FD.flush()
