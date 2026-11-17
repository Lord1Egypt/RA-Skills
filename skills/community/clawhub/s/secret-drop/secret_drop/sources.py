"""Read local secret sources without shell expansion or stdout output."""

from __future__ import annotations

import errno
import os
import re
import stat
from pathlib import Path

from secret_drop import MAX_SECRET_BYTES
from secret_drop.dotenv_file import default_openclaw_env_path, validate_name
from secret_drop.errors import SecretDropError

MAX_SOURCE_BYTES = 2_000_000
_ASSIGNMENT_RE = re.compile(
    r"^\s*(?:export\s+)?(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<value>.*)$"
)


def _read_regular_file(path: Path, *, max_bytes: int = MAX_SOURCE_BYTES) -> str:
    path = path.expanduser()
    flags = os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
    except FileNotFoundError as exc:
        raise SecretDropError("Secret source file does not exist.") from exc
    except OSError as exc:
        if exc.errno in {errno.ELOOP, errno.EMLINK}:
            raise SecretDropError("Refusing to read a secret through a symlink.") from exc
        raise SecretDropError("Could not open the secret source file.") from exc

    try:
        source_stat = os.fstat(fd)
        if not stat.S_ISREG(source_stat.st_mode):
            raise SecretDropError("Secret source is not a regular file.")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(fd, min(65_536, max_bytes + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
            if total > max_bytes:
                raise SecretDropError("Secret source file is too large.")
    finally:
        os.close(fd)

    try:
        return b"".join(chunks).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SecretDropError("Secret source must be UTF-8 text.") from exc


def _decode_dotenv_value(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1]
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        value = raw[1:-1]
        out: list[str] = []
        i = 0
        escapes = {"n": "\n", "r": "\r", "t": "\t", '"': '"', "\\": "\\"}
        while i < len(value):
            if value[i] == "\\" and i + 1 < len(value):
                nxt = value[i + 1]
                out.append(escapes.get(nxt, nxt))
                i += 2
                continue
            out.append(value[i])
            i += 1
        return "".join(out)
    return raw


def read_dotenv_value(path: Path, name: str) -> str:
    validate_name(name)
    text = _read_regular_file(path)
    found: str | None = None
    for line in text.splitlines():
        if not line or line.lstrip().startswith("#"):
            continue
        match = _ASSIGNMENT_RE.match(line)
        if match and match.group("name") == name:
            found = _decode_dotenv_value(match.group("value"))
    if found is None:
        raise SecretDropError("Secret name was not found in the dotenv source.")
    return _validate_secret(found)


def read_secret_source(*, source: str, path: str | None, name: str | None) -> str:
    if source == "openclaw-env":
        if not name:
            raise SecretDropError("--name is required for openclaw-env.")
        return read_dotenv_value(default_openclaw_env_path(), name)
    if source == "dotenv":
        if not path or not name:
            raise SecretDropError("--path and --name are required for dotenv.")
        return read_dotenv_value(Path(path), name)
    if source == "file":
        if not path:
            raise SecretDropError("--path is required for file.")
        return _validate_secret(_read_regular_file(Path(path), max_bytes=MAX_SECRET_BYTES))
    raise SecretDropError(f"Unsupported secret source: {source}")


def _validate_secret(secret: str) -> str:
    if not secret:
        raise SecretDropError("Secret source is empty.")
    if "\x00" in secret:
        raise SecretDropError("Secret source contains a NUL byte.")
    if len(secret.encode("utf-8")) > MAX_SECRET_BYTES:
        raise SecretDropError(f"Secret exceeds the {MAX_SECRET_BYTES}-byte limit.")
    return secret
