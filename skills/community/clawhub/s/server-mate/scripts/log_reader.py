#!/usr/bin/env python3
"""Log reader abstraction layer for Server-Mate.

The agent's main run_cycle should not care whether a log lives on the local
disk or behind a BT panel. It always asks a LogReader for "give me the lines
since the cursor you last handed me". Concrete subclasses encapsulate:

    LocalLogReader   - file system, inode tracking, truncate/rotate recovery.
                       Delegates to server_agent.read_incremental_lines so the
                       battle-tested local logic is not duplicated.

    BTRemoteLogReader - BT panel ExecShell-based incremental byte reads. Tracks
                        remote_offset + last known size. Detects rotation by
                        checking if the remote file shrank below remote_offset.

State persistence: each cursor returned by read_incremental() is a plain dict
that the agent stores under site_state['cursors']['access_log' | 'error_log'].
The dict shape is intentionally compatible with build_log_cursor() so existing
state files keep loading after the upgrade.
"""

from __future__ import annotations

import datetime as dt
import logging
from pathlib import Path
from typing import Any, Protocol

from bt_client import BTPanelClient, BTPanelError


LOG = logging.getLogger("server_mate.log_reader")


def _utcnow_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


class LogReader(Protocol):
    """Minimal contract every reader must satisfy."""

    source: str  # "local" | "bt_remote"
    path: str

    def read_incremental(
        self, cursor: dict[str, Any] | None
    ) -> tuple[list[str], dict[str, Any]]:
        """Return (new_lines, updated_cursor).

        Implementations MUST NOT raise on transient failures — they should
        return ([], cursor_with_status) so the main agent loop never crashes
        because one site is unreachable.
        """
        ...


class LocalLogReader:
    """Local file reader. Thin adapter over server_agent.read_incremental_lines.

    Imported lazily inside __init__ to avoid a circular import (server_agent
    imports this module).
    """

    source = "local"

    def __init__(
        self,
        log_path: str,
        startup_mode: str,
        bootstrap_tail_lines: int,
    ) -> None:
        self.path = str(log_path or "")
        self.startup_mode = startup_mode
        self.bootstrap_tail_lines = bootstrap_tail_lines
        from server_agent import read_incremental_lines

        self._read_fn = read_incremental_lines

    def read_incremental(
        self, cursor: dict[str, Any] | None
    ) -> tuple[list[str], dict[str, Any]]:
        if not self.path:
            return [], dict(cursor or {})
        return self._read_fn(
            Path(self.path),
            cursor,
            self.startup_mode,
            self.bootstrap_tail_lines,
        )


class BTRemoteLogReader:
    """Incremental reader for a log file on a remote BT-managed host.

    Cursor shape (extends the local cursor for forward compatibility):
        {
            "path":          "/www/wwwlogs/site.log",  # remote absolute path
            "offset":        12345,                     # remote_offset, bytes
            "remote_size":   12345,                     # last seen file size
            "panel_id":      "bt-prod-hk",
            "status":        "ready" | "rotated" | "missing" | "read_error" |
                             "auth_error" | "transport_error" | "backlog",
            "rotated_at":    iso8601 (optional),
            "missing_since": iso8601 (optional),
            "last_error":    str (optional),
            "backlog_bytes": int (optional, present when this cycle hit the
                              chunk_bytes cap and bytes still remain on the
                              remote file),
        }
    """

    source = "bt_remote"

    def __init__(
        self,
        client: BTPanelClient,
        remote_path: str,
        startup_mode: str,
        bootstrap_tail_bytes: int = 64 * 1024,
    ) -> None:
        self.client = client
        self.path = str(remote_path or "")
        self.startup_mode = startup_mode
        # Bootstrap is sized in BYTES for remote reads, not lines, since we
        # cannot count lines without first transferring data. 64KB is a
        # reasonable proxy for "last few thousand lines".
        self.bootstrap_tail_bytes = max(int(bootstrap_tail_bytes), 0)

    def _build_cursor(
        self,
        previous: dict[str, Any] | None,
        offset: int,
        remote_size: int | None,
        status: str,
        **extra: Any,
    ) -> dict[str, Any]:
        cursor = dict(previous or {})
        cursor.update(
            {
                "path": self.path,
                "offset": max(int(offset), 0),
                "remote_size": int(remote_size) if remote_size is not None else cursor.get("remote_size"),
                "panel_id": self.client.config.panel_id,
                "status": status,
            }
        )
        for key, value in extra.items():
            cursor[key] = value
        return cursor

    def read_incremental(
        self, cursor: dict[str, Any] | None
    ) -> tuple[list[str], dict[str, Any]]:
        if not self.path:
            return [], dict(cursor or {})

        previous = dict(cursor or {})
        # If we are switching the path we tracked, restart cleanly.
        path_changed = previous.get("path") and previous.get("path") != self.path
        previous_offset = 0 if path_changed else max(int(previous.get("offset", 0)), 0)

        try:
            remote_size = self.client.get_remote_file_size(self.path)
        except BTPanelError as exc:
            LOG.warning("BT remote stat failed for %s: %s", self.path, exc)
            return [], self._build_cursor(
                previous,
                previous_offset,
                previous.get("remote_size"),
                status="transport_error",
                last_error=str(exc),
            )

        if remote_size is None:
            missing_since = previous.get("missing_since") or _utcnow_iso()
            return [], self._build_cursor(
                previous,
                previous_offset,
                None,
                status="missing",
                missing_since=missing_since,
            )

        first_attach = path_changed or "offset" not in previous
        if first_attach:
            if self.startup_mode == "full":
                start_offset = 0
            else:
                start_offset = max(remote_size - self.bootstrap_tail_bytes, 0)
            lines, new_offset, backlog = self._fetch_range(start_offset, remote_size)
            return lines, self._build_cursor(
                previous,
                new_offset,
                remote_size,
                status="backlog" if backlog > 0 else "ready",
                missing_since=None,
                backlog_bytes=backlog,
            )

        # Truncation / rotation: remote shrunk below the offset we recorded.
        if remote_size < previous_offset:
            lines, new_offset, backlog = self._fetch_range(0, remote_size)
            return lines, self._build_cursor(
                previous,
                new_offset,
                remote_size,
                status="rotated",
                rotated_at=_utcnow_iso(),
                missing_since=None,
                backlog_bytes=backlog,
            )

        if remote_size == previous_offset:
            return [], self._build_cursor(
                previous,
                previous_offset,
                remote_size,
                status="ready",
                missing_since=None,
                backlog_bytes=0,
            )

        lines, new_offset, backlog = self._fetch_range(previous_offset, remote_size)
        return lines, self._build_cursor(
            previous,
            new_offset,
            remote_size,
            status="backlog" if backlog > 0 else "ready",
            missing_since=None,
            backlog_bytes=backlog,
        )

    def _fetch_range(self, start: int, end: int) -> tuple[list[str], int, int]:
        """Fetch up to chunk_bytes from [start, end) in a SINGLE ExecShell call.

        Returns ``(lines, new_offset, backlog_bytes)``.

        Bounding strategy (Stage-5 hardening):
            * Per cron tick we issue exactly ONE bounded read
              (``head -c <chunk_bytes>``, default 5 MB). If a remote error_log
              just exploded by 800 MB, we still only pull 5 MB this cycle and
              the remaining 795 MB rolls over to subsequent cron ticks. This
              caps memory, network, AND time per cycle simultaneously.
            * To avoid splitting a line across the cap boundary, we trim the
              trailing partial line and rewind ``new_offset`` to the start of
              that line so the next cycle re-reads it cleanly.
            * If we capped the read AND there are still bytes between
              ``new_offset`` and ``end``, we report ``backlog_bytes > 0`` so
              the caller can stamp the cursor with status="backlog" and emit
              a visible warning.
        """
        if end <= start:
            return [], start, 0

        # Single per-cycle cap. This is also enforced inside the shell pipe via
        # ``head -c {size}`` (see BTPanelClient.read_remote_file_chunk) so even a
        # panel-side bug cannot blow past it.
        cap = max(int(self.client.config.chunk_bytes), 1)
        want = min(cap, end - start)

        try:
            data = self.client.read_remote_file_chunk(self.path, start, want)
        except BTPanelError as exc:
            LOG.warning("BT remote read failed for %s: %s", self.path, exc)
            return [], start, max(end - start, 0)

        if not data:
            # Either the file vanished between stat and read, or the chunk
            # returned empty for some other transient reason. Don't advance.
            return [], start, max(end - start, 0)

        text = data.decode("utf-8", errors="replace")
        last_newline = text.rfind("\n")
        if last_newline == -1:
            # The cap-sized read didn't contain any newline. This usually means
            # one logical line is genuinely larger than chunk_bytes (rare but
            # possible for stack traces). Don't advance — surface as backlog so
            # an operator notices instead of looping silently.
            LOG.warning(
                "BT remote read of %s yielded %s bytes with no newline (single "
                "line > chunk_bytes=%s?); not advancing offset",
                self.path,
                len(data),
                cap,
            )
            return [], start, max(end - start, 0)

        complete = text[: last_newline + 1]
        consumed_bytes = len(complete.encode("utf-8", errors="replace"))
        lines = complete.splitlines(keepends=True)
        new_offset = start + consumed_bytes
        backlog = max(end - new_offset, 0)

        # If we both filled the cap AND there's more on the remote side, log a
        # visible backlog warning. This is the operator-facing signal that the
        # site is falling behind real-time.
        if backlog > 0 and len(data) >= cap:
            LOG.warning(
                "BT remote backlog for %s: %s bytes still pending after this "
                "cycle (cap=%s); will catch up on subsequent cron ticks.",
                self.path,
                backlog,
                cap,
            )

        return lines, new_offset, backlog


def make_log_reader(
    log_path: str,
    panel_id: str,
    panel_registry: dict[str, BTPanelClient],
    startup_mode: str,
    bootstrap_tail_lines: int,
    bootstrap_tail_bytes: int = 64 * 1024,
) -> LogReader:
    """Factory: pick a Local or Remote reader based on panel_id.

    If panel_id is set but the corresponding client is missing (auth/url
    invalid), we fall back to a no-op reader that always reports "missing" so
    the cycle keeps running and the operator sees the broken site clearly.
    """
    panel_id = (panel_id or "").strip()
    if not panel_id:
        return LocalLogReader(log_path, startup_mode, bootstrap_tail_lines)

    client = panel_registry.get(panel_id)
    if client is None:
        LOG.warning(
            "Site references panel_id=%s but no live client is registered; "
            "skipping remote log %s",
            panel_id,
            log_path,
        )
        return _UnconfiguredRemoteReader(panel_id, log_path)

    return BTRemoteLogReader(
        client,
        log_path,
        startup_mode,
        bootstrap_tail_bytes=bootstrap_tail_bytes,
    )


class _UnconfiguredRemoteReader:
    """No-op reader returned when panel_id points at a missing/auth-failed panel."""

    source = "bt_remote_unconfigured"

    def __init__(self, panel_id: str, path: str) -> None:
        self.panel_id = panel_id
        self.path = path

    def read_incremental(
        self, cursor: dict[str, Any] | None
    ) -> tuple[list[str], dict[str, Any]]:
        next_cursor = dict(cursor or {})
        next_cursor.update(
            {
                "path": self.path,
                "panel_id": self.panel_id,
                "status": "auth_error",
                "last_error": f"panel '{self.panel_id}' not configured / missing api_key",
            }
        )
        return [], next_cursor
