"""
crash_reporting.py — Sigrid's Crash Reporter & Runtime Diagnostics
===================================================================

Adopted from NorseSagaEngine crash_reporting.py with no structural changes.
This is the foundation layer — every other module depends on it for
fail-safe error recording and runtime breadcrumb tracing.

Norse framing: Huginn (thought) and Muninn (memory) capture all that
goes wrong in the nine worlds so nothing is lost to the void.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import platform
import shutil
import sys
import threading
import traceback
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any, Callable, Deque, Dict, List, Optional


logger = logging.getLogger(__name__)

SnapshotProvider = Callable[[], Dict[str, Any]]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_serialize(value: Any, max_depth: int = 4, max_items: int = 25) -> Any:
    """Convert runtime objects into JSON-safe snapshots without crashing.

    Muninn remembers everything — even things that resist being spoken aloud.
    """
    try:
        if max_depth <= 0:
            return f"<max_depth:{type(value).__name__}>"

        if value is None or isinstance(value, (bool, int, float, str)):
            return value

        if isinstance(value, dict):
            out: Dict[str, Any] = {}
            for idx, (k, v) in enumerate(value.items()):
                if idx >= max_items:
                    out["__truncated__"] = f"{len(value) - max_items} more keys"
                    break
                out[str(k)] = _safe_serialize(v, max_depth=max_depth - 1, max_items=max_items)
            return out

        if isinstance(value, (list, tuple, set)):
            seq = list(value)
            out_list = [
                _safe_serialize(item, max_depth=max_depth - 1, max_items=max_items)
                for item in seq[:max_items]
            ]
            if len(seq) > max_items:
                out_list.append(f"<truncated:{len(seq) - max_items} more items>")
            return out_list

        if hasattr(value, "__dict__"):
            return {
                "__class__": type(value).__name__,
                "fields": _safe_serialize(vars(value), max_depth=max_depth - 1, max_items=max_items),
            }

        return str(value)
    except Exception as exc:
        return f"<serialization_error:{exc}>"


@dataclass
class CrashEvent:
    """A single runtime crash or exception event recorded in the Vargr Ledger."""

    event_id: str
    timestamp: str
    source: str
    error_type: str
    message: str
    traceback: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    runtime_snapshot: Dict[str, Any] = field(default_factory=dict)
    fingerprint: str = ""
    occurrence_count: int = 1


@dataclass
class TraceEvent:
    """Low-cost breadcrumb for deep post-mortem tracing — Huginn's flight path."""

    timestamp: str
    category: str
    message: str
    severity: str
    details: Dict[str, Any] = field(default_factory=dict)


class CrashReporter:
    """Crash reporter that writes per-event files and rolling summary reports.

    Thor's stability circuits: catches every troll before it brings down the hall.
    """

    def __init__(self, logs_root: str = "logs") -> None:
        self.logs_root = Path(logs_root)
        self.crash_dir = self.logs_root / "crash_reports"
        self.diagnostics_dir = self.crash_dir / "diagnostics"
        self.backup_dir = self.crash_dir / "backup"

        # Yggdrasil grows its root structure before anything else can proceed
        for directory in (self.crash_dir, self.diagnostics_dir, self.backup_dir):
            try:
                directory.mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                logger.error("Could not create crash dir %s: %s", directory, exc)

        self._lock = threading.RLock()
        self._counter = 0
        self._snapshot_providers: Dict[str, SnapshotProvider] = {}
        self._index_file = self.crash_dir / "index.json"
        self._trace_file = self.diagnostics_dir / "runtime_trace.jsonl"
        self._fingerprints_file = self.diagnostics_dir / "fingerprints.json"
        self._breadcrumbs: Deque[TraceEvent] = deque(maxlen=250)
        self._fingerprint_counts: Dict[str, int] = self._load_json_recovering(
            self._fingerprints_file, {}
        )

    def register_snapshot_provider(self, name: str, provider: SnapshotProvider) -> None:
        """Register a callable that captures state snapshots at crash time."""
        with self._lock:
            self._snapshot_providers[name] = provider

    def trace_event(
        self,
        category: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
        severity: str = "info",
    ) -> None:
        """Record runtime breadcrumbs — Huginn scouts for relevant threads."""
        event = TraceEvent(
            timestamp=_utc_now_iso(),
            category=category,
            message=message,
            severity=severity,
            details=_safe_serialize(details or {}),
        )
        with self._lock:
            self._breadcrumbs.append(event)

        payload = json.dumps(_safe_serialize(event.__dict__), ensure_ascii=False, default=str)
        self._safe_append_line(self._trace_file, payload)

    def _safe_append_line(self, path: Path, line: str) -> None:
        try:
            with open(path, "a", encoding="utf-8") as handle:
                handle.write(line + "\n")
        except Exception as exc:
            logger.error("Failed appending trace line to %s: %s", path, exc)

    def capture_runtime_snapshot(self) -> Dict[str, Any]:
        """Snapshot the nine worlds — platform, threads, memory, env flags."""
        resources: Dict[str, Any] = {}
        try:
            # resource module is Linux-only; fails gracefully on Windows
            import resource
            usage = resource.getrusage(resource.RUSAGE_SELF)
            resources = {
                "max_rss_kb": getattr(usage, "ru_maxrss", 0),
                "voluntary_context_switches": getattr(usage, "ru_nvcsw", 0),
                "involuntary_context_switches": getattr(usage, "ru_nivcsw", 0),
            }
        except Exception:
            resources = {"resource_info": "unavailable_on_this_platform"}

        snapshot: Dict[str, Any] = {
            "pid": os.getpid(),
            "cwd": os.getcwd(),
            "python": sys.version,
            "python_executable": sys.executable,
            "argv": list(sys.argv),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "thread_count": threading.active_count(),
            "threads": [t.name for t in threading.enumerate()][:40],
            "loaded_modules": len(sys.modules),
            "resource_usage": resources,
            "env_flags": {
                "DEBUG": os.environ.get("DEBUG", ""),
                "PYTHONUNBUFFERED": os.environ.get("PYTHONUNBUFFERED", ""),
            },
        }

        with self._lock:
            providers = dict(self._snapshot_providers)

        for name, provider in providers.items():
            try:
                snapshot[name] = _safe_serialize(provider())
            except Exception as exc:
                snapshot[name] = {"provider_error": str(exc)}

        return snapshot

    def report_exception(
        self,
        error: BaseException,
        source: str,
        metadata: Optional[Dict[str, Any]] = None,
        tb_text: Optional[str] = None,
    ) -> str:
        """Record an exception to the Vargr Ledger. Returns the event_id."""
        metadata = metadata or {}
        with self._lock:
            self._counter += 1
            event_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{self._counter:05d}"

        fingerprint = self._fingerprint_for(error, source)
        with self._lock:
            self._fingerprint_counts[fingerprint] = (
                self._fingerprint_counts.get(fingerprint, 0) + 1
            )
            occurrence_count = self._fingerprint_counts[fingerprint]
            breadcrumbs = [entry.__dict__ for entry in list(self._breadcrumbs)[-25:]]

        enriched_metadata = dict(metadata)
        enriched_metadata["breadcrumbs"] = breadcrumbs
        enriched_metadata["fingerprint"] = fingerprint
        enriched_metadata["occurrence_count"] = occurrence_count

        event = CrashEvent(
            event_id=event_id,
            timestamp=_utc_now_iso(),
            source=source,
            error_type=type(error).__name__,
            message=str(error),
            traceback=tb_text or traceback.format_exc(),
            metadata=_safe_serialize(enriched_metadata),
            runtime_snapshot=self.capture_runtime_snapshot(),
            fingerprint=fingerprint,
            occurrence_count=occurrence_count,
        )

        self._persist_event(event)
        return event_id

    def report_incident(
        self, source: str, message: str, metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Record a non-exception incident (logic error, invalid state, etc.)."""
        incident = RuntimeError(message)
        return self.report_exception(
            incident, source=source, metadata=metadata, tb_text="<no traceback>"
        )

    def _fingerprint_for(self, error: BaseException, source: str) -> str:
        payload = f"{source}|{type(error).__name__}|{str(error)[:120]}"
        return hashlib.sha256(payload.encode("utf-8", errors="replace")).hexdigest()[:16]

    def _persist_event(self, event: CrashEvent) -> None:
        event_file = self.crash_dir / f"crash_{event.event_id}.json"
        payload = {
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "source": event.source,
            "error_type": event.error_type,
            "message": event.message,
            "traceback": event.traceback,
            "metadata": event.metadata,
            "runtime_snapshot": event.runtime_snapshot,
            "fingerprint": event.fingerprint,
            "occurrence_count": event.occurrence_count,
        }
        if not self._safe_write_json(event_file, payload):
            logger.error("Could not persist crash event %s", event.event_id)
            return

        self._safe_write_json(self._fingerprints_file, self._fingerprint_counts)
        self._append_index(event)
        self._write_summary_report()

    def _safe_write_json(self, path: Path, payload: Any) -> bool:
        """Atomic write with fallback — the mead hall always has a backup barrel."""
        for attempt in range(3):
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                with NamedTemporaryFile(
                    "w", delete=False, encoding="utf-8", dir=path.parent
                ) as handle:
                    json.dump(payload, handle, indent=2, ensure_ascii=False, default=str)
                    temp_path = Path(handle.name)
                temp_path.replace(path)
                return True
            except Exception as exc:
                logger.error("JSON write failed (%s) for %s attempt %s", exc, path, attempt + 1)

        try:
            fallback = self.backup_dir / f"{path.name}.fallback"
            with open(fallback, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, ensure_ascii=False, default=str)
            return True
        except Exception as exc:
            logger.error("Backup JSON write failed for %s: %s", path, exc)
            return False

    def _load_json_recovering(self, path: Path, default: Any) -> Any:
        """Load JSON with quarantine of corrupt files — no troll gets in twice."""
        if not path.exists():
            return default
        try:
            with open(path, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except Exception as exc:
            logger.error("Corrupt JSON at %s: %s", path, exc)
            try:
                damaged = path.with_suffix(path.suffix + ".corrupt")
                shutil.move(str(path), str(damaged))
            except Exception as move_exc:
                logger.error("Cannot quarantine %s: %s", path, move_exc)
            return default

    def _append_index(self, event: CrashEvent) -> None:
        try:
            entries: List[Dict[str, Any]] = (
                self._load_json_recovering(self._index_file, []) or []
            )
            entries.append({
                "event_id": event.event_id,
                "timestamp": event.timestamp,
                "source": event.source,
                "error_type": event.error_type,
                "message": event.message,
                "fingerprint": event.fingerprint,
                "occurrence_count": event.occurrence_count,
            })
            self._safe_write_json(self._index_file, entries[-500:])
        except Exception as exc:
            logger.error("Failed to update crash index: %s", exc)

    def _write_summary_report(self) -> None:
        try:
            entries: List[Dict[str, Any]] = (
                self._load_json_recovering(self._index_file, []) or []
            )
            by_type: Dict[str, int] = {}
            by_source: Dict[str, int] = {}
            for event in entries:
                t = str(event.get("error_type", "Unknown"))
                s = str(event.get("source", "unknown"))
                by_type[t] = by_type.get(t, 0) + 1
                by_source[s] = by_source.get(s, 0) + 1

            lines = [
                "# Sigrid — Crash Summary",
                "",
                f"Generated: {_utc_now_iso()}",
                f"Total recorded crashes: {len(entries)}",
                "",
                "## Top Error Types",
            ]
            for err, count in sorted(by_type.items(), key=lambda kv: kv[1], reverse=True)[:20]:
                lines.append(f"- {err}: {count}")
            lines.extend(["", "## Top Sources"])
            for src, count in sorted(by_source.items(), key=lambda kv: kv[1], reverse=True)[:20]:
                lines.append(f"- {src}: {count}")
            lines.extend(["", "## Recent Crashes"])
            for event in entries[-30:]:
                lines.append(
                    "- {timestamp} | {source} | {error_type} | {message}".format(**event)
                )

            report_file = self.crash_dir / "crash_summary.md"
            with open(report_file, "w", encoding="utf-8") as handle:
                handle.write("\n".join(lines) + "\n")
        except Exception as exc:
            logger.error("Failed to write crash summary: %s", exc)


# ─── Singleton accessor ────────────────────────────────────────────────────────

_GLOBAL_REPORTER: Optional[CrashReporter] = None


def get_crash_reporter(logs_root: str = "logs") -> CrashReporter:
    """Return the global CrashReporter, initialising it on first call."""
    global _GLOBAL_REPORTER
    if _GLOBAL_REPORTER is None:
        _GLOBAL_REPORTER = CrashReporter(logs_root=logs_root)
    return _GLOBAL_REPORTER
