"""Per-document exclusive lock (pure Python, POSIX and Windows).

Requests read a document, modify it and replace it. Without a lock, two
concurrent requests both succeed and the second silently discards the
first one's changes. The lock file sits next to the document
(``.<name>.lock``) and is held for the whole request, including snap
staging copies. It is never deleted: removing a lock file that another
process is waiting on would break mutual exclusion.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any, Optional

from . import errors

if os.name == "nt":
    import msvcrt
else:
    import fcntl


def lock_path(doc: Path) -> Path:
    return doc.with_name(f".{doc.name}.lock")


class DocumentLock:
    def __init__(self, doc: Path, timeout: float) -> None:
        self.path = lock_path(doc)
        self.timeout = timeout
        self.fh: Optional[Any] = None

    def _try(self) -> bool:
        assert self.fh is not None
        try:
            if os.name == "nt":
                self.fh.seek(0)
                msvcrt.locking(self.fh.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                fcntl.flock(self.fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            return False

    def __enter__(self) -> "DocumentLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fh = open(self.path, "a+")
        deadline = time.monotonic() + self.timeout
        delay = 0.05
        while not self._try():
            if time.monotonic() >= deadline:
                self.fh.close()
                self.fh = None
                raise errors.SkillError(
                    errors.DOCUMENT_BUSY,
                    f"'{self.path.name[1:-5]}' is being modified by another request",
                    hint="Requests on the same document run one at a time. Send your steps in one request, or retry when the other request has finished.",
                )
            time.sleep(delay)
            delay = min(delay * 1.5, 0.5)
        return self

    def __exit__(self, *exc: Any) -> None:
        if self.fh is None:
            return
        try:
            if os.name == "nt":
                self.fh.seek(0)
                msvcrt.locking(self.fh.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(self.fh.fileno(), fcntl.LOCK_UN)
        finally:
            self.fh.close()
            self.fh = None
