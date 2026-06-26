from __future__ import annotations

from pypi_package_changelog_generator.diff_text import keeps_full_patch, truncate_patch
from pypi_package_changelog_generator.models import ChangelogResult


def apply_budget(
    result: ChangelogResult,
    *,
    max_commits: int = 80,
    max_reviews: int = 40,
    max_files: int = 120,
    max_patch_chars: int = 2000,
) -> None:
    original_commit_count = len(result.commits)
    original_review_count = len(result.reviews)
    original_file_count = len(result.file_changes)

    result.file_changes = _prioritize_files(result.file_changes)[:max_files]
    result.commits = result.commits[:max_commits]
    result.reviews = result.reviews[:max_reviews]

    for change in result.file_changes:
        patch = change.get("patch")
        if (
            not patch
            or keeps_full_patch(change.get("path"))
            or len(patch) <= max_patch_chars
        ):
            continue
        change["patch"] = truncate_patch(patch, max_patch_chars)
        result.truncation.truncated = True
        result.truncation.reason = (
            "patch excerpts were shortened to fit the evidence budget"
        )

    if original_commit_count > len(result.commits):
        result.truncation.truncated = True
        result.truncation.omitted_commits = original_commit_count - len(result.commits)
        result.truncation.reason = (
            result.truncation.reason or "commit list exceeded the evidence budget"
        )
    if original_file_count > len(result.file_changes):
        result.truncation.truncated = True
        result.truncation.omitted_files = original_file_count - len(result.file_changes)
        result.truncation.reason = (
            result.truncation.reason or "file list exceeded the evidence budget"
        )
    if original_review_count > len(result.reviews) and not result.truncation.reason:
        result.truncation.truncated = True
        result.truncation.reason = "review list exceeded the evidence budget"


def _prioritize_files(file_changes: list[dict]) -> list[dict]:
    def score(change: dict) -> tuple[int, int, str]:
        path = (change.get("path") or "").lower()
        importance = 0
        if path.endswith(("pyproject.toml", "setup.py", "setup.cfg", "pkg-info")):
            importance += 1000
        if path.endswith(".py"):
            importance += 100
        if change.get("status") in {"removed", "renamed"}:
            importance += 50
        return (-importance, -(change.get("changes") or 0), path)

    return sorted(file_changes, key=score)
