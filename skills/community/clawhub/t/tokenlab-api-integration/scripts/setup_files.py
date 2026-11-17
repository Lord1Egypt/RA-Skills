"""File safety shared by the Codex and Claude Code setup helpers."""

import argparse
from contextlib import contextmanager
import os
from pathlib import Path
import stat
import tempfile

MAX_CONFIG_BYTES = 1_048_576


class SetupError(Exception):
    """A safe-to-display error that never includes existing configuration values."""


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse normally echoes unknown arguments, which could contain a key.
        self.exit(2, "Invalid arguments. Use --help; never pass API keys as arguments.\n")


def read_file(path: Path, *, allow_links: bool = False) -> bytes | None:
    try:
        info = path.stat() if allow_links else path.lstat()
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode) or (not allow_links and info.st_nlink != 1):
        raise SetupError(f"Refusing a linked or non-regular {path.name} file.")
    if info.st_size > MAX_CONFIG_BYTES:
        raise SetupError(f"{path.name} exceeds the supported configuration size.")
    with path.open("rb") as handle:
        opened = os.fstat(handle.fileno())
        if (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
            raise SetupError("Configuration changed while reading; retry after checking it.")
        content = handle.read(MAX_CONFIG_BYTES + 1)
    if len(content) > MAX_CONFIG_BYTES:
        raise SetupError("Configuration grew while reading; no changes written.")
    return content


def require_same(path: Path, expected: bytes | None, *, allow_links: bool = False) -> None:
    if read_file(path, allow_links=allow_links) != expected:
        raise SetupError("Configuration changed after inspection; nothing further was overwritten.")


def atomic_write(path: Path, content: bytes, expected: bytes | None) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            if expected is not None and os.name != "nt":
                os.fchmod(handle.fileno(), stat.S_IMODE(path.stat().st_mode))
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        require_same(path, expected)
        if expected is None:
            # Publish a complete file without clobbering a concurrent creation.
            if os.name == "nt":
                os.rename(temporary, path)  # Windows rename refuses an existing target.
            else:
                os.link(temporary, path)
                os.unlink(temporary)
        else:
            os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def setup_lock(root: Path, profile: str):
    lock = root / f".{profile}.tokenlab-setup.lock"
    try:
        descriptor = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise SetupError("A setup lock exists. Check for another running helper before removing the lock.") from None
    os.close(descriptor)
    try:
        yield
    finally:
        lock.unlink()
