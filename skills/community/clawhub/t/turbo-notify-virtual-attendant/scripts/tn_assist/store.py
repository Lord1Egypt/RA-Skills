"""Atomic, private file storage and the workspace lock."""

from __future__ import annotations

import contextlib
import json
import os
import socket
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

_DIR_MODE = 0o700
_FILE_MODE = 0o600


def ensure_private_dir(path: Path) -> None:
    path.mkdir(mode=_DIR_MODE, parents=True, exist_ok=True)


def write_json_atomic(path: Path, data: object) -> None:
    ensure_private_dir(path.parent)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, _FILE_MODE)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def read_json(path: Path, default: Any) -> Any:
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        return default


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    ensure_private_dir(path.parent)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
    fd = os.open(str(path), os.O_RDWR | os.O_APPEND | os.O_CREAT, _FILE_MODE)
    try:
        size = os.fstat(fd).st_size
        if size and os.pread(fd, 1, size - 1) != b"\n":
            line = "\n" + line  # a crash left half a line: the new record starts on its own line
        os.write(fd, line.encode("utf-8"))
        os.fsync(fd)
    finally:
        os.close(fd)


def append_jsonl_once(
    path: Path, record: dict[str, Any], *, key: str = "id", tail: int = 200
) -> bool:
    """Append unless a recent line already carries the same ``key`` value. Returns True if written.

    Replays happen right after a crash, so only the tail of the file needs checking.
    """
    value = record.get(key)
    if value is not None and any(row.get(key) == value for row in read_jsonl(path)[-tail:]):
        return False
    append_jsonl(path, record)
    return True


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read a JSON-lines file; a line torn by a crash is skipped, never fatal for the rest."""
    try:
        with open(path, encoding="utf-8") as handle:
            lines = handle.read().split("\n")
    except FileNotFoundError:
        return []
    records: list[dict[str, Any]] = []
    for line in lines:
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class WorkspaceLock:
    """One runner per workspace. Stale means: holder gone, or heartbeat older than ``ttl_s``.

    A clock that moves backwards makes a heartbeat look newer, never older, so a fresh
    lock is not stolen; a dead holder on this host is always taken over.
    """

    def __init__(
        self,
        path: Path,
        *,
        clock: Callable[[], float] = time.time,
        pid: int | None = None,
        pid_alive: Callable[[int], bool] = _pid_alive,
    ) -> None:
        self._path = path
        self._clock = clock
        self._pid = os.getpid() if pid is None else pid
        self._pid_alive = pid_alive
        self._host = socket.gethostname()
        self._ttl_s = 90

    def _record(self) -> dict[str, Any]:
        return {"pid": self._pid, "host": self._host, "heartbeat": self._clock()}

    def _stale(self, held: dict[str, Any]) -> bool:
        same_host = held.get("host") == self._host
        if same_host and not self._pid_alive(int(held.get("pid", -1))):
            return True
        age = self._clock() - float(held.get("heartbeat", 0))
        return age > self._ttl_s

    def acquire(self, ttl_s: int = 90) -> bool:
        self._ttl_s = ttl_s
        ensure_private_dir(self._path.parent)
        for _ in range(2):
            try:
                fd = os.open(str(self._path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, _FILE_MODE)
            except FileExistsError:
                try:
                    held = read_json(self._path, None)
                except ValueError:
                    held = None  # a lock file the dead holder left half written
                if isinstance(held, dict) and not self._stale(held):
                    return False
                with contextlib.suppress(FileNotFoundError):
                    os.unlink(self._path)
                continue
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(self._record(), handle)
            return True
        return False

    def heartbeat(self) -> None:
        write_json_atomic(self._path, self._record())

    def release(self) -> None:
        held = read_json(self._path, None)
        if (
            isinstance(held, dict)
            and held.get("pid") == self._pid
            and held.get("host") == self._host
        ):
            with contextlib.suppress(FileNotFoundError):
                os.unlink(self._path)
