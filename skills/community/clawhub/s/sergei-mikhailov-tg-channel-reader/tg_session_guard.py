"""
tg-reader session guard — locking, backups, and last-known-good recovery.

Protects the Telegram session file (a SQLite database that grants full
account access) from the failure modes seen in production:

- concurrent tg-reader processes corrupting the file (exclusive flock);
- `auth` overwriting a working session (timestamped backups with rotation);
- a destroyed/emptied session file with no way back (last-known-good copy,
  saved only after a *verified* authorized run, restorable explicitly).

No heavy dependencies (no Pyrogram/Telethon) — shared by both backends and
by the offline diagnostic.
"""

import hashlib
import json
import os
import shutil
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

try:
    import fcntl
except ImportError:  # non-POSIX (Windows): locking degrades to a no-op
    fcntl = None

_BACKUP_KEEP = 3  # timestamped .bak-* files kept per session


class SessionLockTimeout(Exception):
    """Another process holds the session lock and did not release it in time."""


class NotAuthorizedError(Exception):
    """The session file holds no authorized user (empty, corrupted, or revoked)."""


class NetworkError(Exception):
    """Could not reach Telegram — says nothing about session validity."""


# ── Paths ────────────────────────────────────────────────────────────────────
# All guard files share the `.session.` prefix so .gitignore patterns and
# humans can recognize the whole family at a glance:
#   {name}.session            the live session (owned by Pyrogram/Telethon)
#   {name}.session.lock       flock target
#   {name}.session.last-good  verified-good copy
#   {name}.session.last-good.json   no-secrets manifest for the copy
#   {name}.session.bak-<ts>   timestamped backups (auth / restore)

def _session_path(session_name: str) -> Path:
    return Path(f"{session_name}.session")


def _lock_path(session_name: str) -> Path:
    return Path(f"{session_name}.session.lock")


def _last_good_path(session_name: str) -> Path:
    return Path(f"{session_name}.session.last-good")


def _manifest_path(session_name: str) -> Path:
    return Path(f"{session_name}.session.last-good.json")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _copy_600(src: Path, dst: Path) -> None:
    """Copy src to dst atomically with 0600 permissions.

    The temp file is created 0600 from the first byte — never a window where
    session content sits on disk with default-umask permissions.
    """
    tmp = dst.with_name(dst.name + ".tmp")
    tmp.unlink(missing_ok=True)
    fd = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    with os.fdopen(fd, "wb") as out, open(src, "rb") as inp:
        shutil.copyfileobj(inp, out)
    os.replace(tmp, dst)


# ── Locking ──────────────────────────────────────────────────────────────────

@contextmanager
def session_lock(session_name: str, timeout: float = 60):
    """Exclusive lock on the session — one tg-reader process at a time.

    Blocks up to `timeout` seconds waiting for the holder, then raises
    SessionLockTimeout. The lock file is never deleted (unlink+flock races).
    On platforms without fcntl the lock is a no-op.
    """
    lock_path = _lock_path(session_name)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(lock_path, os.O_CREAT | os.O_WRONLY, 0o600)
    f = os.fdopen(fd, "w")
    try:
        if fcntl is None:
            yield
            return
        waited = 0.0
        while True:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except (BlockingIOError, PermissionError):
                if waited >= timeout:
                    raise SessionLockTimeout(str(lock_path))
                time.sleep(1)
                waited += 1
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
    finally:
        f.close()


def is_lock_held(session_name: str) -> bool:
    """Non-blocking probe: is another process holding the session lock?"""
    if fcntl is None:
        return False
    lock_path = _lock_path(session_name)
    if not lock_path.exists():
        return False
    try:
        fd = os.open(lock_path, os.O_WRONLY)
    except OSError:
        return False
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    except (BlockingIOError, PermissionError):
        return True
    finally:
        os.close(fd)


# ── Timestamped backups (before auth / restore) ──────────────────────────────

def backup_session(session_name: str, keep: int = _BACKUP_KEEP):
    """Copy the current session file to a timestamped .bak-* (0600).

    Returns the backup path as str, or None when there is nothing to back up.
    Old backups beyond `keep` are removed (they grant full account access —
    the fewer copies exist, the better).
    """
    src = _session_path(session_name)
    if not src.exists():
        return None
    dst = Path(f"{session_name}.session.bak-{_timestamp()}")
    _copy_600(src, dst)
    _rotate_backups(session_name, keep)
    return str(dst)


def _rotate_backups(session_name: str, keep: int) -> None:
    base = _session_path(session_name)
    backups = sorted(
        base.parent.glob(base.name + ".bak-*"),
        key=lambda p: p.name,
        reverse=True,
    )
    for old in backups[keep:]:
        try:
            old.unlink()
        except OSError:
            pass


# ── Last-known-good ──────────────────────────────────────────────────────────

def save_last_good(session_name: str, user_id=None, username=None, backend=None):
    """Snapshot the session as last-known-good after a *verified* authorized run.

    Call only after the client has disconnected (file quiesced) and while the
    session lock is still held. Best-effort: a failed snapshot must never fail
    the fetch that just succeeded — errors go to stderr, not stdout (stdout is
    reserved for the command's JSON output).
    """
    src = _session_path(session_name)
    if not src.exists():
        return None
    try:
        dst = _last_good_path(session_name)
        _copy_600(src, dst)
        manifest = {
            "verified_at": _utc_now_iso(),
            "user_id": user_id,
            "username": username,
            "backend": backend,
            "source_path": str(src),
            "sha256": _sha256(dst),
        }
        mpath = _manifest_path(session_name)
        tmp = mpath.with_name(mpath.name + ".tmp")
        tmp.unlink(missing_ok=True)
        fd = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
            f.write("\n")
        os.replace(tmp, mpath)
        return str(dst)
    except OSError as e:
        print(f"warning: could not save last-good session backup: {e}", file=sys.stderr)
        return None


def load_last_good_info(session_name: str):
    """Read the last-good manifest (offline, no secrets). None when absent."""
    lkg = _last_good_path(session_name)
    mpath = _manifest_path(session_name)
    if not lkg.exists() or not mpath.exists():
        return None
    try:
        with open(mpath) as f:
            manifest = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    manifest["path"] = str(lkg)
    return manifest


def restore_last_good(session_name: str):
    """Put the last-good copy in place of the current session file.

    The current file (if any) is moved aside to a timestamped .bak-* first —
    nothing is destroyed. The last-good copy is integrity-checked against the
    manifest sha256 before it is installed. The caller is responsible for
    holding the session lock and for verifying authorization afterwards.

    Returns a dict describing what happened; raises ValueError when there is
    no usable backup.
    """
    info = load_last_good_info(session_name)
    if info is None:
        raise ValueError(
            "No last-good session backup found. One is saved automatically "
            "after each successful authorized run; none exists yet."
        )
    lkg = _last_good_path(session_name)
    actual_sha = _sha256(lkg)
    if actual_sha != info.get("sha256"):
        raise ValueError(
            f"Last-good backup {lkg} does not match its manifest checksum — "
            "refusing to restore a possibly corrupted copy."
        )

    target = _session_path(session_name)
    moved_to = None
    if target.exists():
        moved_to = Path(f"{session_name}.session.bak-{_timestamp()}")
        os.replace(target, moved_to)
        _rotate_backups(session_name, _BACKUP_KEEP)
    _copy_600(lkg, target)

    return {
        "restored_from": str(lkg),
        "verified_at": info.get("verified_at"),
        "user_id": info.get("user_id"),
        "username": info.get("username"),
        "previous_file_moved_to": str(moved_to) if moved_to else None,
    }
