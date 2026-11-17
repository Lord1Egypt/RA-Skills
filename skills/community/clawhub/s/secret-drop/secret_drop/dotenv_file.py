"""Atomic dotenv updates that never print values."""

from __future__ import annotations

import os
import re
import stat
import tempfile
from pathlib import Path

from secret_drop.errors import SecretDropError

_NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]{0,127}$")
_EXPORT_RE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=")


def validate_name(name: str) -> str:
    if not _NAME_RE.match(name or ""):
        raise SecretDropError(
            "Name must match ^[A-Z][A-Z0-9_]{0,127}$ (OpenClaw store / env grammar)."
        )
    return name


def default_openclaw_env_path() -> Path:
    state_dir = os.environ.get("OPENCLAW_STATE_DIR") or str(Path.home() / ".openclaw")
    return Path(state_dir).expanduser() / ".env"


def format_assignment(name: str, value: str) -> str:
    if value == "":
        return f"{name}=\n"
    if (
        any(ch in value for ch in ' \t\n\r"\'#$&*?[]{}();`\\|')
        or value.startswith(" ")
        or value.endswith(" ")
    ):
        escaped = (
            value.replace("\\", "\\\\")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace('"', '\\"')
        )
        return f'{name}="{escaped}"\n'
    return f"{name}={value}\n"


def _assert_safe_replace_target(path: Path, *, destination: str) -> None:
    """Reject a symlink or non-file target immediately before os.replace."""
    try:
        target_stat = os.lstat(path)
    except FileNotFoundError:
        return
    if stat.S_ISLNK(target_stat.st_mode):
        raise SecretDropError("Refusing to write through a symlink.")
    if not stat.S_ISREG(target_stat.st_mode):
        raise SecretDropError(f"{destination} exists and is not a regular file.")


def upsert_env_file(path: Path, name: str, value: str) -> dict[str, str | int | bool]:
    validate_name(name)
    path = path.expanduser()
    created = not path.exists()
    if path.exists() and path.is_symlink():
        raise SecretDropError("Refusing to write through a symlink.")
    if path.exists() and not path.is_file():
        raise SecretDropError("Env destination exists and is not a regular file.")
    parent = path.parent
    parent_was_missing = not parent.exists()
    parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    if parent_was_missing:
        os.chmod(parent, 0o700)

    original = path.read_text(encoding="utf-8") if path.exists() else ""
    lines = original.splitlines(keepends=True)
    replaced = False
    out: list[str] = []
    assignment = format_assignment(name, value)
    for line in lines:
        match = _EXPORT_RE.match(line)
        if match and match.group(1) == name:
            if not replaced:
                prefix = "export " if line.lstrip().startswith("export ") else ""
                out.append(prefix + assignment)
                replaced = True
        else:
            out.append(line)
    if not replaced:
        if out and not out[-1].endswith("\n"):
            out.append("\n")
        out.append(assignment)

    data = "".join(out).encode("utf-8")
    fd, tmp_name = tempfile.mkstemp(prefix=".secret-drop-", suffix=".tmp", dir=str(parent))
    tmp_path = Path(tmp_name)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        _assert_safe_replace_target(path, destination="Env destination")
        os.replace(tmp_path, path)
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise

    return {
        "path": str(path),
        "created": created,
        "replaced": replaced,
        "bytes": len(value.encode("utf-8")),
    }


def write_secret_file(
    path: Path, value: str, *, replace: bool = False
) -> dict[str, str | int | bool]:
    path = path.expanduser()
    existed = path.exists()
    if path.exists() and path.is_symlink():
        raise SecretDropError("Refusing to write through a symlink.")
    if existed and not replace:
        raise SecretDropError("File already exists; pass --replace to overwrite it.")
    if existed and not path.is_file():
        raise SecretDropError("File destination exists and is not a regular file.")
    parent = path.parent
    parent_was_missing = not parent.exists()
    parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    if parent_was_missing:
        os.chmod(parent, 0o700)
    data = value.encode("utf-8")
    fd, tmp_name = tempfile.mkstemp(prefix=".secret-drop-", suffix=".tmp", dir=str(parent))
    tmp_path = Path(tmp_name)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        _assert_safe_replace_target(path, destination="File destination")
        os.replace(tmp_path, path)
        os.chmod(path, 0o600)
    except Exception:
        try:
            tmp_path.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    return {"path": str(path), "created": not existed, "replaced": existed, "bytes": len(data)}
