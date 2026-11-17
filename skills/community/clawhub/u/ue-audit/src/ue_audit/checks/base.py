"""Shared context and helpers for audit checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..bridge import BridgeError
from ..manifest import FileEntry, Manifest
from ..project import ProjectInfo
from ..readonly import ReadOnlyBridge
from ..report.model import CheckResult, Finding, Severity, Status
from ..util import utc_now


@dataclass
class AuditOptions:
    live: bool = False
    blueprints: list[str] = field(default_factory=list)
    datatables: list[str] = field(default_factory=list)
    widgets: list[str] = field(default_factory=list)
    materials: list[str] = field(default_factory=list)
    animbps: list[str] = field(default_factory=list)
    max_file_mb: float = 100.0
    max_logs: int = 3
    log_since_hours: int = 0
    include_git: bool = True
    git_large_mb: float = 50.0
    watch_files: bool = True
    pie: bool = False
    pie_seconds: float = 3.0
    pie_mode: str = "pie"
    max_hash_bytes: int = 512 * 1024 * 1024


@dataclass
class AuditContext:
    project: ProjectInfo
    engine: dict[str, Any]
    manifest: Manifest
    baseline: Manifest | None
    diff: dict[str, Any] | None
    options: AuditOptions
    output_dir: Path
    evidence_dir: Path
    bridge: ReadOnlyBridge | None = None
    bridge_error: str = ""

    def evidence_ref(self, name: str) -> str:
        return f"evidence/{name}"

    def write_evidence_json(self, name: str, payload: Any) -> str:
        from ..report.render_json import write_json

        path = self.evidence_dir / name
        write_json(payload, path)
        return self.evidence_ref(name)


def finish_check(check: CheckResult) -> CheckResult:
    """Derive a check status/severity from its findings unless it is already skip/error/unknown."""
    severities = {item.severity for item in check.findings}
    if Severity.BLOCKER in severities:
        check.severity = Severity.BLOCKER
    elif Severity.ERROR in severities:
        check.severity = Severity.ERROR
    elif Severity.WARNING in severities:
        check.severity = Severity.WARNING
    else:
        check.severity = Severity.INFO

    if check.status in (Status.SKIP, Status.ERROR, Status.UNKNOWN):
        return check
    if check.severity in (Severity.BLOCKER, Severity.ERROR):
        check.status = Status.FAIL
    elif any(item.status == Status.UNKNOWN for item in check.findings):
        # An incomplete read is not a pass, and it should not be hidden by a
        # lower-severity warning. The warning findings remain visible.
        check.status = Status.UNKNOWN
    elif check.severity == Severity.WARNING:
        check.status = Status.WARN
    else:
        check.status = Status.PASS
    return check


def new_check(check_id: str, title: str) -> CheckResult:
    return CheckResult(
        check_id=check_id,
        title=title,
        status=Status.PASS,
        started_at=utc_now(),
    )


def make_finding(
    check_id: str,
    severity: Severity,
    status: Status,
    title: str,
    message: str,
    **kwargs: Any,
) -> Finding:
    return Finding(
        check_id=check_id,
        severity=severity,
        status=status,
        title=title,
        message=message,
        **kwargs,
    )


def normalize_game_path(value: str) -> str:
    """Extract a /Game/... path from values mangled by shells or copied logs."""
    raw = str(value or "").strip().replace("\\", "/")
    index = raw.find("/Game/")
    if index >= 0:
        return raw[index:]
    return raw


def engine_family(version: str) -> str:
    """Return major.minor for values like 5.1.1-23901901+++UE5+Release-5.1."""
    import re

    match = re.search(r"(\d+)\.(\d+)", str(version or ""))
    if not match:
        return ""
    return f"{match.group(1)}.{match.group(2)}"


def game_path_to_content_rel(game_path: str) -> list[str]:
    """Return candidate Content-relative paths for a /Game/ object path."""
    raw = normalize_game_path(game_path)
    if not raw.startswith("/Game/"):
        return []
    relative = raw[len("/Game/") :].split(".")[0].strip("/")
    if not relative:
        return []
    base = f"Content/{relative}"
    return [base + ".uasset", base + ".umap"]


def find_manifest_entry(manifest: Manifest, game_path: str) -> FileEntry | None:
    for candidate in game_path_to_content_rel(game_path):
        entry = manifest.files.get(candidate)
        if entry is not None:
            return entry
    lowered = {path.casefold(): entry for path, entry in manifest.files.items()}
    for candidate in game_path_to_content_rel(game_path):
        entry = lowered.get(candidate.casefold())
        if entry is not None:
            return entry
    return None


def bridge_error_message(exc: Exception) -> str:
    if isinstance(exc, BridgeError):
        hint = f" ({exc.hint})" if exc.hint else ""
        return f"{exc.message}{hint}"
    return str(exc)
