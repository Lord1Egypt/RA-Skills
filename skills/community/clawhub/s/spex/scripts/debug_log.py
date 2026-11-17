"""Script execution tracing for spex CLI subcommands."""

from __future__ import annotations

import json
import re
import sys
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Iterator

from common import find_matching_specs, local_iso_timestamp, logger
from config import get_project_context

MAX_STREAM_BYTES = 256 * 1024
PROMPT_STDOUT_LOG_BYTES = 2 * 1024
DEBUG_LOG_NAME = "debug.log"
SESSIONS_DIR_NAME = "sessions"
ACTIVE_SESSION_FILENAME = "active"
_SESSION_ID_RE = re.compile(r"^[A-Za-z0-9._-]+$")
_PROMPT_SUMMARY_KEYS = (
    "task_id",
    "commit_sha",
    "review_round",
    "all_done",
    "step_id",
    "resume_phase",
    "commit_title",
)


def validate_session_id(session_id: str) -> str:
    """Return a safe session id or raise ``ValueError``.

    Rejects empty values, ``.`` / ``..``, path separators, the reserved
    active-pointer name (case-insensitive), and any id that is not in the
    ``[A-Za-z0-9._-]+`` allowlist.
    """
    cleaned = (session_id or "").strip()
    if not cleaned:
        raise ValueError("session_id must be non-empty")
    if cleaned in {".", ".."}:
        raise ValueError(f"invalid session_id: {session_id!r}")
    if "/" in cleaned or "\\" in cleaned or "\0" in cleaned:
        raise ValueError(f"invalid session_id: {session_id!r}")
    if not _SESSION_ID_RE.fullmatch(cleaned):
        raise ValueError(f"invalid session_id: {session_id!r}")
    if cleaned.casefold() == ACTIVE_SESSION_FILENAME.casefold():
        raise ValueError(
            f"session_id is reserved for the active pointer: {session_id!r}"
        )
    return cleaned


def debug_enabled(argv: list[str]) -> bool:
    """Return True if CLI debug flag or config.debug is enabled."""
    if "-d" in argv or "--debug" in argv:
        return True
    ctx = get_project_context()
    return bool(ctx.config.get("debug"))


def append_debug_anchor(log_path: Path, line: str) -> None:
    """Append a timeline anchor best-effort (APPLY/tee); swallow OSError.

    CREATE prepare/post-action anchors use a raising writer in
    ``create_helper`` instead — do not route those through this helper.
    """
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        text = line if line.endswith("\n") else f"{line}\n"
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(text)
    except OSError as exc:
        logger.debug("Failed to write debug anchor to %s: %s", log_path, exc)


def emit_apply_anchor(
    spec_dir: str | Path,
    line: str,
    argv: list[str] | None = None,
) -> None:
    """Append an APPLY timeline anchor when debug is enabled."""
    if not debug_enabled(argv if argv is not None else sys.argv):
        return
    append_debug_anchor(Path(spec_dir) / DEBUG_LOG_NAME, line)


def parse_name_from_argv(argv: list[str]) -> str | None:
    """Parse --name or --name= from argv."""
    return parse_flag_from_argv(argv, "--name")


def parse_flag_from_argv(argv: list[str], flag: str) -> str | None:
    """Parse ``--flag value`` or ``--flag=value`` from argv."""
    equals_prefix = f"{flag}="
    for index, arg in enumerate(argv):
        if arg == flag and index + 1 < len(argv):
            return argv[index + 1]
        if arg.startswith(equals_prefix):
            return arg.split("=", 1)[1]
    return None


def is_prompt_argv(argv: list[str]) -> bool:
    """Return True if argv is a ``spex prompt ...`` invocation."""
    for arg in argv:
        if arg in {"-d", "--debug", "-V", "--version", "-h", "--help"}:
            continue
        if arg == "spex" or arg.endswith("/spex"):
            continue
        return arg == "prompt"
    return False


def sessions_dir(spex_root: str | Path) -> Path:
    """Return ``<spex_root>/sessions``."""
    return Path(spex_root) / SESSIONS_DIR_NAME


def active_session_path(spex_root: str | Path) -> Path:
    """Return the active-session pointer file path."""
    return sessions_dir(spex_root) / ACTIVE_SESSION_FILENAME


def session_debug_log_path(spex_root: str | Path, session_id: str) -> Path:
    """Return ``<spex_root>/sessions/<session_id>/debug.log``.

    Validates ``session_id`` and asserts the resolved path stays under
    ``sessions_dir(spex_root)``.
    """
    safe_id = validate_session_id(session_id)
    base = sessions_dir(spex_root).resolve()
    path = (base / safe_id / DEBUG_LOG_NAME).resolve()
    try:
        path.relative_to(base)
    except ValueError as exc:
        raise ValueError(
            f"session path escapes sessions dir: {session_id!r}"
        ) from exc
    return path


def get_active_session_id(spex_root: str | Path) -> str | None:
    """Read the active create-session id from the pointer file."""
    pointer = active_session_path(spex_root)
    if not pointer.is_file():
        return None
    try:
        session_id = pointer.read_text(encoding="utf-8").strip()
    except OSError as exc:
        logger.debug("Failed to read active session pointer %s: %s", pointer, exc)
        return None
    if not session_id:
        return None
    try:
        return validate_session_id(session_id)
    except ValueError:
        logger.debug("Ignoring invalid active session id %r", session_id)
        return None


def set_active_session(spex_root: str | Path, session_id: str) -> None:
    """Write ``session_id`` as the active create-session pointer."""
    safe_id = validate_session_id(session_id)
    pointer = active_session_path(spex_root)
    pointer.parent.mkdir(parents=True, exist_ok=True)
    pointer.write_text(f"{safe_id}\n", encoding="utf-8")


def clear_active_session(spex_root: str | Path) -> None:
    """Remove the active create-session pointer if present."""
    pointer = active_session_path(spex_root)
    try:
        pointer.unlink(missing_ok=True)
    except OSError as exc:
        logger.debug("Failed to clear active session pointer %s: %s", pointer, exc)


def merge_session_log_into_spec(
    spex_root: str | Path,
    session_id: str,
    spec_dir: str | Path,
) -> Path | None:
    """Append session log into ``spec_dir/debug.log``, then delete session log.

    Also relocates the session ``.prev_end`` sidecar onto the target log when
    content was merged (so post-merge ``gap_ms`` continues), and always removes
    the session sidecar so the empty session directory can be cleaned up.

    Returns the merged target path when a session log file existed (even if
    empty). Returns ``None`` when there was no session log to merge.
    Does not clear the active-session pointer.
    """
    if not session_id:
        return None

    try:
        session_log = session_debug_log_path(spex_root, session_id)
    except ValueError:
        logger.debug("Ignoring invalid session_id for merge: %r", session_id)
        return None
    session_dir = session_log.parent

    def _rmdir_if_empty() -> None:
        try:
            if session_dir.is_dir() and not any(session_dir.iterdir()):
                session_dir.rmdir()
        except OSError as exc:
            logger.debug("Failed to remove empty session dir %s: %s", session_dir, exc)

    if not session_log.is_file():
        # begin-session creates the dir even when debug is off and no log
        # is written; still best-effort clean the empty session dir.
        _rmdir_if_empty()
        return None

    target = Path(spec_dir) / DEBUG_LOG_NAME
    try:
        content = session_log.read_text(encoding="utf-8")
        if content:
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("a", encoding="utf-8") as handle:
                handle.write(content)
        session_log.unlink(missing_ok=True)

        # gap_ms sidecar lives beside the log; move it with merged content so
        # the session dir is empty enough for _rmdir_if_empty, and the first
        # post-merge trace on the spec log can still emit gap_ms.
        session_sidecar = _prev_end_state_path(session_log)
        if session_sidecar.is_file():
            try:
                if content:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    session_sidecar.replace(_prev_end_state_path(target))
                else:
                    session_sidecar.unlink(missing_ok=True)
            except OSError as exc:
                logger.debug(
                    "Failed to relocate/remove session prev_end %s: %s",
                    session_sidecar,
                    exc,
                )
                try:
                    session_sidecar.unlink(missing_ok=True)
                except OSError:
                    pass

        _rmdir_if_empty()
    except OSError as exc:
        logger.debug(
            "Failed to merge session log %s into %s: %s",
            session_log,
            target,
            exc,
        )
        return None

    return target


def resolve_debug_log_path(argv: list[str]) -> Path | None:
    """Resolve debug.log with mutual-exclusive routing.

    Priority (runtime never dual-writes); exact-before-fuzzy across both trees:
    1. Exact ``--name`` in ``specs/`` → ``<spec_dir>/debug.log``
    2. Exact ``--name`` in ``archives/`` → ``<archived_dir>/debug.log``
    3. Unique fuzzy ``--name`` in ``specs/`` → ``<spec_dir>/debug.log``
    4. Unique fuzzy ``--name`` in ``archives/`` → ``<archived_dir>/debug.log``
    5. Active create session → ``sessions/<id>/debug.log``
    6. Fallback → ``<spex_root>/debug.log``
    """
    ctx = get_project_context()
    if not ctx.spex_root:
        return None

    name = parse_name_from_argv(argv)
    if name:
        spex_root = Path(ctx.spex_root)
        specs_dir = spex_root / "specs"
        archives_dir = spex_root / "archives"

        exact_specs = specs_dir / name
        if exact_specs.is_dir():
            return exact_specs / DEBUG_LOG_NAME

        exact_archives = archives_dir / name
        if exact_archives.is_dir():
            return exact_archives / DEBUG_LOG_NAME

        if specs_dir.is_dir():
            matches = find_matching_specs(name, specs_dir)
            if len(matches) == 1:
                return matches[0] / DEBUG_LOG_NAME

        if archives_dir.is_dir():
            matches = find_matching_specs(name, archives_dir)
            if len(matches) == 1:
                return matches[0] / DEBUG_LOG_NAME

    session_id = get_active_session_id(ctx.spex_root)
    if session_id:
        return session_debug_log_path(ctx.spex_root, session_id)

    return Path(ctx.spex_root) / DEBUG_LOG_NAME


def safe_flush_debug_log_path(
    argv: list[str],
    pre_resolved: Path | None,
) -> Path | None:
    """Choose a post-command flush path that never recreates specs stubs.

    Selection:
    1. Post-command ``resolve_debug_log_path`` when available
    2. ``pre_resolved`` only if its parent directory still exists
    3. ``<spex_root>/debug.log`` when spex_root is configured
    4. ``None`` to skip the flush
    """
    resolved = resolve_debug_log_path(argv)
    if resolved is not None:
        return resolved

    if pre_resolved is not None and pre_resolved.parent.is_dir():
        return pre_resolved

    ctx = get_project_context()
    if ctx.spex_root:
        return Path(ctx.spex_root) / DEBUG_LOG_NAME
    return None


def _is_under_specs_tree(path: Path) -> bool:
    """Return True if ``path`` lies under ``<spex_root>/specs`` (may be missing).

    Uses path structure relative to configured ``spex_root``, so the check
    still holds when the entire ``specs/`` directory has vanished.
    """
    ctx = get_project_context()
    if ctx.spex_root:
        specs_root = Path(ctx.spex_root) / "specs"
        try:
            path.resolve(strict=False).relative_to(specs_root.resolve(strict=False))
            return True
        except ValueError:
            return False
    # No spex_root: refuse classic ``.../specs/<name>/`` parents.
    return path.parent.name == "specs"


def _prepare_debug_log_parent(log_path: Path) -> bool:
    """Ensure ``log_path`` parent exists; never recreate vanished specs dirs.

    Returns False when the write should be skipped.
    """
    parent = log_path.parent
    if parent.is_dir():
        return True

    # Refuse mkdir for any missing parent under specs/, even if specs/ itself
    # is absent. Never mkdir(parents=True) for a missing parent under specs/.
    if _is_under_specs_tree(parent):
        logger.debug(
            "Refusing to recreate vanished specs debug log parent: %s",
            parent,
        )
        return False

    try:
        parent.mkdir(parents=True, exist_ok=True)
        return True
    except OSError as exc:
        logger.debug("Failed to create debug log parent %s: %s", parent, exc)
        return False


class TeeIO:
    """Write-through stream wrapper that captures output up to a byte cap."""

    def __init__(self, stream, parts: list[str], meta: dict) -> None:
        self._stream = stream
        self._parts = parts
        self._meta = meta

    def write(self, data: str) -> int:
        if not data:
            return 0
        self._stream.write(data)
        byte_len = len(data.encode("utf-8", errors="replace"))
        self._meta["total_bytes"] += byte_len
        if self._meta["truncated"]:
            return len(data)

        buffered = self._meta["buffered_bytes"]
        remaining = MAX_STREAM_BYTES - buffered
        if byte_len <= remaining:
            self._parts.append(data)
            self._meta["buffered_bytes"] = buffered + byte_len
        else:
            if remaining > 0:
                encoded = data.encode("utf-8", errors="replace")
                self._parts.append(
                    encoded[:remaining].decode("utf-8", errors="ignore")
                )
                self._meta["buffered_bytes"] = MAX_STREAM_BYTES
            self._meta["truncated"] = True
        return len(data)

    def flush(self) -> None:
        self._stream.flush()

    def fileno(self) -> int:
        return self._stream.fileno()

    def isatty(self) -> bool:
        return self._stream.isatty()

    def __getattr__(self, name: str):
        return getattr(self._stream, name)


def _format_stream_block(label: str, parts: list[str], meta: dict) -> str:
    content = "".join(parts)
    if meta["truncated"]:
        content += f"\n... [truncated, total {meta['total_bytes']} bytes]"
    return f"----- {label} -----\n{content}\n"


def _summarize_prompt_stdout(content: str, total_bytes: int) -> str:
    """Return a skim-friendly prompt stdout for debug.log (not caller stdout)."""
    stripped = content.strip()
    if stripped:
        try:
            data = json.loads(stripped)
        except (json.JSONDecodeError, TypeError, ValueError):
            data = None
        if isinstance(data, dict):
            bits = [f"total={total_bytes}B"]
            keys = sorted(str(k) for k in data.keys())
            bits.append(f"keys={','.join(keys)}")
            for key in _PROMPT_SUMMARY_KEYS:
                if key not in data:
                    continue
                bits.append(f"{key}={data[key]!s}")
            prompt_val = data.get("prompt")
            if isinstance(prompt_val, str):
                prompt_len = len(prompt_val.encode("utf-8", errors="replace"))
                bits.append(f"prompt_len={prompt_len}")
            return (
                f"[truncated prompt stdout, {'; '.join(bits)}]\n"
            )

    encoded = content.encode("utf-8", errors="replace")
    if len(encoded) <= PROMPT_STDOUT_LOG_BYTES:
        if total_bytes > len(encoded):
            return (
                f"{content}"
                f"\n... [truncated prompt stdout, total={total_bytes}B]\n"
            )
        return content
    head = encoded[:PROMPT_STDOUT_LOG_BYTES].decode("utf-8", errors="ignore")
    return f"{head}\n... [truncated prompt stdout, total={total_bytes}B]\n"


def _format_stdout_for_log(
    argv: list[str], parts: list[str], meta: dict
) -> str:
    """Format stdout for the log; summarize/truncate prompt commands only."""
    if is_prompt_argv(argv):
        content = "".join(parts)
        summarized = _summarize_prompt_stdout(content, meta["total_bytes"])
        return f"----- stdout -----\n{summarized}\n"
    return _format_stream_block("stdout", parts, meta)


def _parse_iso_timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _prev_end_state_path(log_path: Path) -> Path:
    """Sidecar path for the last flushed block's end timestamp."""
    return Path(str(log_path) + ".prev_end")


def _previous_end_instant(log_path: Path) -> datetime | None:
    """Return previous END wall time for gap_ms.

    BEGIN is stamped at flush time (command end), so that stamp is the END.
    Read it from a sidecar written on each successful flush — never by
    regex-scanning the log body, which can be poisoned by BEGIN/END lines
    embedded in stdout/stderr payloads.
    """
    if not log_path.is_file():
        return None
    state_path = _prev_end_state_path(log_path)
    if not state_path.is_file():
        return None
    try:
        raw = state_path.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return _parse_iso_timestamp(raw)


def _remember_end_instant(log_path: Path, end: datetime) -> None:
    """Persist last END stamp next to the log for the next gap_ms calculation."""
    state_path = _prev_end_state_path(log_path)
    try:
        state_path.write_text(end.isoformat() + "\n", encoding="utf-8")
    except OSError as exc:
        logger.debug("Failed to write gap prev_end to %s: %s", state_path, exc)


def _build_meta_line(
    argv: list[str], log_path: Path, now: datetime
) -> str:
    """Build ``meta:`` line with argv fields and gap_ms since previous END."""
    step = parse_flag_from_argv(argv, "--step")
    if step is None:
        step = parse_flag_from_argv(argv, "--id")
    commit = parse_flag_from_argv(argv, "--commit")

    parts: list[str] = []
    if step is not None:
        parts.append(f"step={step}")
    if commit is not None:
        parts.append(f"commit={commit}")

    prev_end = _previous_end_instant(log_path)
    if prev_end is not None:
        gap_ms = max(0, int((now - prev_end).total_seconds() * 1000))
        parts.append(f"gap_ms={gap_ms}")

    if not parts:
        return "meta:\n"
    return f"meta: {' '.join(parts)}\n"


def _append_trace(
    log_path: Path,
    argv: list[str],
    stdout_parts: list[str],
    stdout_meta: dict,
    stderr_parts: list[str],
    stderr_meta: dict,
    exit_code: int,
    duration_ms: int,
) -> None:
    timestamp = local_iso_timestamp()
    now = _parse_iso_timestamp(timestamp) or datetime.now().astimezone()
    argv_text = " ".join(argv)
    meta_line = _build_meta_line(argv, log_path, now)
    block = (
        f"===== BEGIN {timestamp} =====\n"
        f"argv: {argv_text}\n"
        f"{meta_line}"
        f"{_format_stdout_for_log(argv, stdout_parts, stdout_meta)}"
        f"{_format_stream_block('stderr', stderr_parts, stderr_meta)}"
        f"===== END exit={exit_code} duration_ms={duration_ms} =====\n"
    )
    if not _prepare_debug_log_parent(log_path):
        return
    try:
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(block)
        _remember_end_instant(log_path, now)
    except OSError as exc:
        logger.debug("Failed to write debug log to %s: %s", log_path, exc)


def _normalize_exit_code(code) -> int:
    if code is None:
        return 0
    if isinstance(code, int):
        return code
    try:
        return int(code)
    except (TypeError, ValueError):
        return 1


@contextmanager
def trace_command(log_path: Path, argv: list[str]) -> Iterator[None]:
    """Context manager that tees stdout/stderr and appends a trace block.

    The flush path is chosen via ``safe_flush_debug_log_path`` after the
    command body returns. This matters for ``prepare-spec``: the pre-command
    path may be the active session log (new ``--name`` does not exist yet),
    but handoff merges/deletes that file and clears the active pointer, after
    which ``--name`` uniquely matches the new spec. Flushing the pre-resolved
    session path would recreate an orphan session log; re-resolving appends
    the tee block to ``<spec_dir>/debug.log`` instead.

    After ``archive`` moves a spec to ``archives/``, re-resolve follows the
    archived directory so tee appends there instead of recreating a vanished
    ``specs/<name>/`` stub via ``mkdir``.
    """
    start = time.monotonic()
    exit_code = 0
    stdout_parts: list[str] = []
    stderr_parts: list[str] = []
    stdout_meta = {"buffered_bytes": 0, "total_bytes": 0, "truncated": False}
    stderr_meta = {"buffered_bytes": 0, "total_bytes": 0, "truncated": False}

    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = TeeIO(old_stdout, stdout_parts, stdout_meta)
    sys.stderr = TeeIO(old_stderr, stderr_parts, stderr_meta)

    try:
        yield
    except SystemExit as exc:
        exit_code = _normalize_exit_code(exc.code)
        raise
    except BaseException:
        exit_code = 1
        raise
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        duration_ms = int((time.monotonic() - start) * 1000)
        flush_path = safe_flush_debug_log_path(argv, log_path)
        if flush_path is None:
            return
        _append_trace(
            flush_path,
            argv,
            stdout_parts,
            stdout_meta,
            stderr_parts,
            stderr_meta,
            exit_code,
            duration_ms,
        )
