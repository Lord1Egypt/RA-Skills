"""Baseline diff check."""

from __future__ import annotations

from .base import AuditContext, finish_check, make_finding, new_check
from ..report.model import Provenance, Severity, Status


def check_baseline_diff(ctx: AuditContext):
    check = new_check("PRJ002", "Baseline diff")
    if ctx.baseline is None or ctx.diff is None:
        check.status = Status.UNKNOWN
        check.summary = "No baseline manifest was provided."
        check.details = {"reason": "no_baseline"}
        check.add(
            make_finding(
                "PRJ002",
                Severity.INFO,
                Status.UNKNOWN,
                "No baseline available",
                "Only the current project snapshot can be reported; no change history is available.",
                recommendation="Create a baseline with --save-baseline before the next change, then audit against it.",
            )
        )
        return finish_check(check)

    diff = ctx.diff
    check.details = {
        "baseline_manifest_sha256": ctx.baseline.manifest_sha256,
        "current_manifest_sha256": ctx.manifest.manifest_sha256,
        "added_count": diff["added_count"],
        "removed_count": diff["removed_count"],
        "changed_count": diff["changed_count"],
        "unknown_count": diff["unknown_count"],
        "metadata_changed_count": diff["metadata_changed_count"],
        "added": diff["added"][:200],
        "removed": diff["removed"][:200],
        "changed": diff["changed"][:200],
        "unknown": diff["unknown"][:200],
        "metadata_changed": diff["metadata_changed"][:200],
        "truncated": any(
            len(diff[key]) > 200 for key in ("added", "removed", "changed", "unknown", "metadata_changed")
        ),
    }

    if diff["added_count"] or diff["removed_count"] or diff["changed_count"]:
        check.add(
            make_finding(
                "PRJ002",
                Severity.WARNING,
                Status.WARN,
                "Project differs from baseline",
                f"added={diff['added_count']}, removed={diff['removed_count']}, changed={diff['changed_count']}",
                recommendation="Review the changed files; this audit does not decide whether the change is acceptable.",
            )
        )

    for item in diff["added"][:100]:
        check.add(
            make_finding(
                "PRJ002",
                Severity.INFO,
                Status.PASS,
                "File added since baseline",
                item["path"],
                asset=item["path"],
                provenance=Provenance.UNKNOWN,
            )
        )
    for item in diff["removed"][:100]:
        check.add(
            make_finding(
                "PRJ002",
                Severity.INFO,
                Status.PASS,
                "File removed since baseline",
                item["path"],
                asset=item["path"],
                provenance=Provenance.UNKNOWN,
            )
        )
    for item in diff["changed"][:100]:
        check.add(
            make_finding(
                "PRJ002",
                Severity.INFO,
                Status.PASS,
                "File changed since baseline",
                item["path"],
                asset=item["path"],
                provenance=Provenance.UNKNOWN,
            )
        )
    for item in diff["unknown"][:100]:
        check.add(
            make_finding(
                "PRJ002",
                Severity.WARNING,
                Status.UNKNOWN,
                "File change cannot be verified by hash",
                f"{item['path']}: {item.get('reason', 'hash unavailable')}",
                asset=item["path"],
                recommendation="Raise --max-hash-mb or inspect the file manually.",
            )
        )
    if diff["metadata_changed_count"]:
        check.add(
            make_finding(
                "PRJ002",
                Severity.INFO,
                Status.PASS,
                "File metadata changed without content change",
                f"{diff['metadata_changed_count']} file(s) changed size/mtime but kept the same hash.",
                recommendation="This may be a touch or re-save; review if unexpected.",
            )
        )

    if diff["unknown_count"]:
        check.status = Status.UNKNOWN
    check.summary = (
        f"added={diff['added_count']}, removed={diff['removed_count']}, "
        f"changed={diff['changed_count']}, unknown={diff['unknown_count']}, "
        f"metadata={diff['metadata_changed_count']}"
    )
    return finish_check(check)
