from __future__ import annotations

from pathlib import PurePosixPath

FULL_DIFF_SUFFIXES = {".py", ".md"}


def keeps_full_patch(path: str | None) -> bool:
    return PurePosixPath(path or "").suffix.lower() in FULL_DIFF_SUFFIXES


def omit_diff_body(path: str | None, status: str | None) -> bool:
    return not keeps_full_patch(path) and status in {"added", "removed"}


def truncate_patch(patch: str, max_chars: int) -> str:
    return patch[:max_chars].rstrip() + "\n...<truncated>...\n"


def format_git_diff_patch(
    *,
    path: str | None,
    status: str | None,
    previous_path: str | None = None,
    patch: str | None = None,
    binary: bool = False,
) -> str | None:
    if not path:
        return patch

    old_path = previous_path or path
    header = [f"diff --git a/{old_path} b/{path}"]
    if status == "added":
        header.append("new file mode 100644")
    elif status == "removed":
        header.append("deleted file mode 100644")
    elif status == "renamed" and previous_path:
        header.append(f"rename from {previous_path}")
        header.append(f"rename to {path}")

    if binary:
        header.append(_binary_note(path=path, status=status, previous_path=previous_path))
        return "\n".join(header) + "\n"
    if omit_diff_body(path, status):
        return "\n".join(header) + "\n"

    normalized_patch = _normalize_patch(patch)
    if not normalized_patch:
        if len(header) > 1:
            return "\n".join(header) + "\n"
        return None
    if not normalized_patch.startswith("--- "):
        normalized_patch = _file_labels(
            path=path,
            status=status,
            previous_path=previous_path,
        ) + normalized_patch
    return "\n".join(header) + "\n" + normalized_patch


def _normalize_patch(patch: str | None) -> str:
    if not patch:
        return ""
    normalized = patch.replace("\r\n", "\n")
    if not normalized.endswith("\n"):
        normalized += "\n"
    return normalized


def _file_labels(*, path: str, status: str | None, previous_path: str | None) -> str:
    old_path = previous_path or path
    old_label = "/dev/null" if status == "added" else f"a/{old_path}"
    new_label = "/dev/null" if status == "removed" else f"b/{path}"
    return f"--- {old_label}\n+++ {new_label}\n"


def _binary_note(*, path: str, status: str | None, previous_path: str | None) -> str:
    old_path = previous_path or path
    old_label = "/dev/null" if status == "added" else f"a/{old_path}"
    new_label = "/dev/null" if status == "removed" else f"b/{path}"
    return f"Binary files {old_label} and {new_label} differ"
