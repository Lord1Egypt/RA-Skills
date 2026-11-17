"""Best-effort Windows directory write monitor for the audit window.

This is not a kernel ETW/USN audit. It uses ReadDirectoryChangesW on the
project roots, records events while the audit runs, and reports them as
supporting evidence. If the watcher is unavailable, the report says so.
"""

from __future__ import annotations

import ctypes
import os
import struct
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .util import utc_now


FILE_LIST_DIRECTORY = 0x0001
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
FILE_SHARE_DELETE = 0x00000004
OPEN_EXISTING = 3
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_OVERLAPPED = 0x40000000
FILE_NOTIFY_CHANGE_FILE_NAME = 0x00000001
FILE_NOTIFY_CHANGE_DIR_NAME = 0x00000002
FILE_NOTIFY_CHANGE_ATTRIBUTES = 0x00000004
FILE_NOTIFY_CHANGE_SIZE = 0x00000008
FILE_NOTIFY_CHANGE_LAST_WRITE = 0x00000010
FILE_NOTIFY_CHANGE_CREATION = 0x00000040
FILE_NOTIFY_CHANGE_SECURITY = 0x00000100
ERROR_IO_PENDING = 997
ERROR_OPERATION_ABORTED = 995
WAIT_OBJECT_0 = 0
WAIT_TIMEOUT = 258
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

ACTION_NAMES = {
    1: "added",
    2: "removed",
    3: "modified",
    4: "renamed_from",
    5: "renamed_to",
}


@dataclass
class WriteEvent:
    root: str
    path: str
    action: str
    timestamp: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, str]:
        return {
            "root": self.root,
            "path": self.path,
            "action": self.action,
            "timestamp": self.timestamp,
        }


class _Overlapped(ctypes.Structure):
    _fields_ = [
        ("Internal", ctypes.c_void_p),
        ("InternalHigh", ctypes.c_void_p),
        ("Offset", ctypes.c_ulong),
        ("OffsetHigh", ctypes.c_ulong),
        ("hEvent", ctypes.c_void_p),
    ]


class DirectoryWatcher:
    """Watch a set of directories for write-like events during an audit."""

    def __init__(
        self,
        roots: list[Path],
        max_events: int = 500,
        ignore_suffixes: set[str] | None = None,
    ) -> None:
        self.roots = [Path(root).resolve() for root in roots if Path(root).is_dir()]
        self.max_events = max_events
        self.ignore_suffixes = {
            item.casefold() for item in (ignore_suffixes or {".pyc", ".pyo", ".tmp"})
        }
        self.events: list[WriteEvent] = []
        self.errors: list[str] = []
        self.overflow = False
        self.available = False
        self.reason = ""
        self._threads: list[threading.Thread] = []
        self._handles: list[int] = []
        self._stop = threading.Event()
        self._lock = threading.Lock()

    def start(self) -> "DirectoryWatcher":
        if os.name != "nt":
            self.reason = "not_windows"
            return self
        if not self.roots:
            self.reason = "no_watch_roots"
            return self
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.CreateFileW.restype = ctypes.c_void_p
            kernel32.CreateFileW.argtypes = [
                ctypes.c_wchar_p,
                ctypes.c_ulong,
                ctypes.c_ulong,
                ctypes.c_void_p,
                ctypes.c_ulong,
                ctypes.c_ulong,
                ctypes.c_void_p,
            ]
            kernel32.ReadDirectoryChangesW.restype = ctypes.c_int
            kernel32.ReadDirectoryChangesW.argtypes = [
                ctypes.c_void_p,
                ctypes.c_void_p,
                ctypes.c_ulong,
                ctypes.c_int,
                ctypes.c_ulong,
                ctypes.POINTER(ctypes.c_ulong),
                ctypes.POINTER(_Overlapped),
                ctypes.c_void_p,
            ]
            kernel32.CancelIoEx.restype = ctypes.c_int
            kernel32.CancelIoEx.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
            kernel32.GetOverlappedResult.restype = ctypes.c_int
            kernel32.GetOverlappedResult.argtypes = [
                ctypes.c_void_p,
                ctypes.POINTER(_Overlapped),
                ctypes.POINTER(ctypes.c_ulong),
                ctypes.c_int,
            ]
            kernel32.CreateEventW.restype = ctypes.c_void_p
            kernel32.CreateEventW.argtypes = [
                ctypes.c_void_p,
                ctypes.c_int,
                ctypes.c_int,
                ctypes.c_wchar_p,
            ]
            kernel32.WaitForSingleObject.restype = ctypes.c_ulong
            kernel32.WaitForSingleObject.argtypes = [ctypes.c_void_p, ctypes.c_ulong]
            kernel32.CloseHandle.restype = ctypes.c_int
            kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
            self.available = True
        except Exception as exc:  # noqa: BLE001
            self.reason = f"ctypes_error: {exc}"
            return self

        for root in self.roots:
            thread = threading.Thread(
                target=self._watch_root, args=(root,), name=f"ue-audit-watch-{root.name}", daemon=True
            )
            self._threads.append(thread)
            thread.start()
        return self

    def stop(self) -> None:
        self._stop.set()
        if os.name == "nt":
            try:
                kernel32 = ctypes.windll.kernel32
                with self._lock:
                    handles = list(self._handles)
                for handle in handles:
                    try:
                        kernel32.CancelIoEx(ctypes.c_void_p(handle), None)
                    except Exception:
                        pass
            except Exception:
                pass
        for thread in self._threads:
            thread.join(timeout=2.0)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            events = [event.to_dict() for event in self.events]
            errors = list(self.errors)
            overflow = self.overflow
        return {
            "available": self.available,
            "reason": self.reason,
            "roots": [str(root) for root in self.roots],
            "event_count": len(events),
            "events": events[:500],
            "overflow": overflow,
            "errors": errors[:20],
            "limitation": (
                "Best-effort ReadDirectoryChangesW monitor over the configured roots; "
                "not kernel ETW/USN. Events outside the roots or writes restored before "
                "the next event may not be observed."
            ),
        }

    def _record(self, root: Path, relative: str, action: str) -> None:
        if not relative:
            return
        if any(relative.casefold().endswith(suffix) for suffix in self.ignore_suffixes):
            return
        with self._lock:
            if len(self.events) >= self.max_events:
                self.overflow = True
                return
            self.events.append(
                WriteEvent(
                    root=str(root),
                    path=relative.replace("\\", "/"),
                    action=action,
                )
            )

    def _watch_root(self, root: Path) -> None:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.CreateFileW(
            str(root),
            FILE_LIST_DIRECTORY,
            FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
            None,
            OPEN_EXISTING,
            FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OVERLAPPED,
            None,
        )
        if not handle or handle == INVALID_HANDLE_VALUE:
            with self._lock:
                self.errors.append(f"CreateFileW failed for {root} (error {kernel32.GetLastError()})")
            return

        event = kernel32.CreateEventW(None, 1, 0, None)
        if not event:
            with self._lock:
                self.errors.append(f"CreateEventW failed for {root}")
            kernel32.CloseHandle(ctypes.c_void_p(handle))
            return

        with self._lock:
            self._handles.append(handle)

        buffer = ctypes.create_string_buffer(64 * 1024)
        bytes_returned = ctypes.c_ulong(0)
        overlapped = _Overlapped()
        overlapped.hEvent = event
        filter_flags = (
            FILE_NOTIFY_CHANGE_FILE_NAME
            | FILE_NOTIFY_CHANGE_DIR_NAME
            | FILE_NOTIFY_CHANGE_ATTRIBUTES
            | FILE_NOTIFY_CHANGE_SIZE
            | FILE_NOTIFY_CHANGE_LAST_WRITE
            | FILE_NOTIFY_CHANGE_CREATION
            | FILE_NOTIFY_CHANGE_SECURITY
        )

        try:
            while not self._stop.is_set():
                ctypes.memset(ctypes.byref(overlapped), 0, ctypes.sizeof(overlapped))
                overlapped.hEvent = event
                ok = kernel32.ReadDirectoryChangesW(
                    ctypes.c_void_p(handle),
                    buffer,
                    len(buffer),
                    1,
                    filter_flags,
                    ctypes.byref(bytes_returned),
                    ctypes.byref(overlapped),
                    None,
                )
                if not ok:
                    error = kernel32.GetLastError()
                    if error != ERROR_IO_PENDING:
                        with self._lock:
                            self.errors.append(f"ReadDirectoryChangesW failed for {root} (error {error})")
                        break
                wait = kernel32.WaitForSingleObject(ctypes.c_void_p(event), 500)
                if wait == WAIT_TIMEOUT:
                    continue
                if wait != WAIT_OBJECT_0:
                    break
                if self._stop.is_set():
                    kernel32.CancelIoEx(ctypes.c_void_p(handle), ctypes.byref(overlapped))
                    break
                got = kernel32.GetOverlappedResult(
                    ctypes.c_void_p(handle),
                    ctypes.byref(overlapped),
                    ctypes.byref(bytes_returned),
                    0,
                )
                if not got:
                    error = kernel32.GetLastError()
                    if error == ERROR_OPERATION_ABORTED:
                        break
                    with self._lock:
                        self.errors.append(f"GetOverlappedResult failed for {root} (error {error})")
                    break
                if bytes_returned.value == 0:
                    with self._lock:
                        self.overflow = True
                else:
                    self._parse_buffer(root, buffer.raw[: bytes_returned.value])
        finally:
            try:
                kernel32.CancelIoEx(ctypes.c_void_p(handle), None)
            except Exception:
                pass
            with self._lock:
                try:
                    self._handles.remove(handle)
                except ValueError:
                    pass
            kernel32.CloseHandle(ctypes.c_void_p(handle))
            kernel32.CloseHandle(ctypes.c_void_p(event))

    def _parse_buffer(self, root: Path, data: bytes) -> None:
        offset = 0
        while offset + 12 <= len(data):
            next_offset, action, name_length = struct.unpack_from("<III", data, offset)
            name_bytes = data[offset + 12 : offset + 12 + name_length]
            try:
                name = name_bytes.decode("utf-16-le", errors="replace")
            except Exception:
                name = ""
            action_name = ACTION_NAMES.get(action, f"action_{action}")
            if name:
                self._record(root, name, action_name)
            if next_offset == 0:
                break
            offset += next_offset
