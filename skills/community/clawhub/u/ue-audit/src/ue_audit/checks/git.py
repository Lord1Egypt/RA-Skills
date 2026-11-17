"""Git working-tree hygiene check."""

from __future__ import annotations

from .base import AuditContext, finish_check, make_finding, new_check
from ..project import git_info, git_large_files
from ..report.model import Severity, Status


def check_git(ctx: AuditContext):
    check = new_check("GIT001", "Git working-tree hygiene")
    if not ctx.options.include_git:
        check.status = Status.SKIP
        check.summary = "Git check disabled."
        check.details = {"reason": "git_check_disabled"}
        return check

    info = git_info(ctx.project.root)
    if not info.get("available"):
        check.status = Status.SKIP
        check.summary = "Project is not a Git working tree."
        check.details = {"reason": info.get("reason", "not_a_git_repository")}
        return check

    threshold = int(ctx.options.git_large_mb * 1024 * 1024)
    large = git_large_files(ctx.project.root, threshold)
    check.details = {
        "head": info.get("head", ""),
        "branch": info.get("branch", ""),
        "dirty": info.get("dirty", False),
        "modified_count": info.get("modified_count", 0),
        "untracked_count": info.get("untracked_count", 0),
        "conflict_count": info.get("conflict_count", 0),
        "entries": info.get("entries", [])[:200],
        "entries_truncated": info.get("truncated", False),
        "large_threshold_bytes": threshold,
        "large_files": large,
    }

    if info.get("conflict_count", 0):
        check.add(
            make_finding(
                "GIT001",
                Severity.ERROR,
                Status.FAIL,
                "Unresolved Git conflicts",
                f"{info['conflict_count']} conflicted path(s) in the working tree.",
                recommendation="Resolve merge/rebase conflicts before treating the project as a stable baseline.",
            )
        )
    if info.get("modified_count", 0):
        check.add(
            make_finding(
                "GIT001",
                Severity.WARNING,
                Status.WARN,
                "Tracked files have uncommitted changes",
                f"{info['modified_count']} modified tracked path(s).",
                recommendation="Commit or stash intended changes so the audit baseline is reproducible.",
            )
        )
    if info.get("untracked_count", 0):
        check.add(
            make_finding(
                "GIT001",
                Severity.WARNING,
                Status.WARN,
                "Untracked files are present",
                f"{info['untracked_count']} untracked path(s).",
                recommendation="Confirm new assets are intentionally untracked or add them to version control.",
            )
        )
    for item in large[:20]:
        check.add(
            make_finding(
                "GIT001",
                Severity.INFO,
                Status.PASS,
                "Large tracked file",
                f"{item['path']} is {item['size']} bytes.",
                asset=item["path"],
                recommendation="Confirm whether this file belongs in Git; consider LFS for large binary assets.",
            )
        )
    if not any(
        [
            info.get("conflict_count", 0),
            info.get("modified_count", 0),
            info.get("untracked_count", 0),
            large,
        ]
    ):
        check.add(
            make_finding(
                "GIT001",
                Severity.INFO,
                Status.PASS,
                "Git working tree is clean",
                f"HEAD={info.get('head', '')[:12]} branch={info.get('branch', '')}",
            )
        )

    check.summary = (
        f"modified={info.get('modified_count', 0)}, "
        f"untracked={info.get('untracked_count', 0)}, "
        f"conflicts={info.get('conflict_count', 0)}, "
        f"large={len(large)}"
    )
    return finish_check(check)
