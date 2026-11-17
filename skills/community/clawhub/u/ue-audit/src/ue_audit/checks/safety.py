"""Read-only proof check for the audit itself."""

from __future__ import annotations

from .base import AuditContext, finish_check, make_finding, new_check
from ..report.model import Severity, Status


def check_readonly_proof(ctx: AuditContext, proof: dict):
    check = new_check("SAFE001", "Audit read-only evidence")
    check.details = proof

    if not proof.get("content_equal"):
        check.status = Status.FAIL
        check.add(
            make_finding(
                "SAFE001",
                Severity.BLOCKER,
                Status.FAIL,
                "Project content changed during the audit",
                proof.get("statement", ""),
                evidence=["evidence/manifest-before.json", "evidence/manifest-after.json"],
                recommendation="Stop and inspect the diff before trusting this report.",
            )
        )
        check.summary = proof.get("statement", "")
        return finish_check(check)

    if proof.get("unknown_count"):
        check.status = Status.UNKNOWN
        check.add(
            make_finding(
                "SAFE001",
                Severity.WARNING,
                Status.UNKNOWN,
                "Read-only completeness is unknown",
                proof.get("statement", ""),
                recommendation="Some files could not be hashed; inspect the unknown entries.",
            )
        )
        check.summary = proof.get("statement", "")
        return finish_check(check)

    if not proof.get("metadata_equal"):
        check.status = Status.WARN
        check.add(
            make_finding(
                "SAFE001",
                Severity.WARNING,
                Status.WARN,
                "File metadata changed during the audit",
                proof.get("statement", ""),
                recommendation="A save or touch may have occurred; review metadata_changed entries.",
            )
        )
        check.summary = proof.get("statement", "")
        return finish_check(check)

    check.status = Status.PASS
    check.summary = proof.get("statement", "")
    return finish_check(check)


def check_write_monitor(ctx: AuditContext, proof: dict):
    check = new_check("SAFE002", "During-write monitor")
    monitor = proof.get("during_write_monitor")
    events = proof.get("during_write_events") or []
    event_count = int(proof.get("during_write_event_count") or len(events))
    overflow = bool(proof.get("during_write_overflow"))
    check.details = {
        "monitor": monitor,
        "event_count": event_count,
        "overflow": overflow,
        "reason": proof.get("during_write_reason", ""),
        "limitation": proof.get("during_write_limitation", ""),
        "events": events[:100],
    }

    if monitor != "available":
        check.status = Status.UNKNOWN
        check.summary = (
            "During-write monitor unavailable"
            + (f": {proof.get('during_write_reason')}" if proof.get("during_write_reason") else ".")
        )
        check.add(
            make_finding(
                "SAFE002",
                Severity.INFO,
                Status.UNKNOWN,
                "During-write monitor is unavailable",
                proof.get("during_write_limitation", "Only before/after manifests were compared."),
                recommendation="Run on Windows with the default watcher enabled for stronger read-only evidence.",
            )
        )
        return finish_check(check)

    if event_count or overflow:
        preview = "; ".join(
            f"{item.get('action')}: {item.get('path')}" for item in events[:5]
        )
        check.status = Status.WARN
        check.summary = f"events={event_count}" + (", overflow" if overflow else "")
        check.add(
            make_finding(
                "SAFE002",
                Severity.WARNING,
                Status.WARN,
                "File-system events were observed during the audit",
                f"{event_count} event(s). {preview}" if preview else f"{event_count} event(s).",
                evidence=["evidence/write-events.json"],
                recommendation="Inspect the events; the editor or another process may have written during the audit.",
            )
        )
        return finish_check(check)

    check.status = Status.PASS
    check.summary = "No directory write events observed during the audit."
    return finish_check(check)
