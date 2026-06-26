from __future__ import annotations

import difflib
import hashlib
import tarfile
import tempfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
from typing import Any

from pypi_package_changelog_generator.diff_text import format_git_diff_patch, omit_diff_body
from pypi_package_changelog_generator.pypi_client import PypiClient, PypiClientError


class ArchiveDiffError(RuntimeError):
    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


@dataclass(slots=True)
class ExtractedArchive:
    root: Path
    temp_dir: tempfile.TemporaryDirectory[str]

    def cleanup(self) -> None:
        self.temp_dir.cleanup()


@dataclass(slots=True)
class ArchiveComparison:
    from_archive: ExtractedArchive
    to_archive: ExtractedArchive
    file_changes: list[dict[str, Any]]

    def cleanup(self) -> None:
        self.from_archive.cleanup()
        self.to_archive.cleanup()


def compare_release_archives(
    client: PypiClient,
    from_release: dict[str, Any],
    to_release: dict[str, Any],
) -> ArchiveComparison:
    from_url = client.find_sdist_url(from_release)
    to_url = client.find_sdist_url(to_release)
    if not from_url or not to_url:
        raise ArchiveDiffError(
            code="sdist_missing",
            message="A source distribution is required for archive fallback.",
        )

    try:
        from_archive = extract_archive(client.download_bytes(from_url))
        to_archive = extract_archive(client.download_bytes(to_url))
    except PypiClientError as exc:
        raise ArchiveDiffError(
            code=exc.code, message=exc.message, retryable=exc.retryable
        ) from exc

    file_changes = build_file_changes(from_archive.root, to_archive.root)
    return ArchiveComparison(
        from_archive=from_archive, to_archive=to_archive, file_changes=file_changes
    )


def _is_safe_tar_member(root: Path, member: tarfile.TarInfo) -> bool:
    member_name = member.name.replace("\\", "/")
    member_posix_path = PurePosixPath(member_name)
    member_windows_path = PureWindowsPath(member_name)
    if member_posix_path.is_absolute() or member_windows_path.is_absolute():
        return False
    if member_windows_path.drive:
        return False
    if ".." in member_posix_path.parts:
        return False
    destination = root.joinpath(*member_posix_path.parts).resolve(strict=False)
    if not destination.is_relative_to(root):
        return False
    return member.isdir() or member.isreg()


def extract_archive(content: bytes) -> ExtractedArchive:
    temp_dir = tempfile.TemporaryDirectory(prefix="pypi-changelog-")
    root = Path(temp_dir.name)
    root_resolved = root.resolve()
    try:
        with tarfile.open(fileobj=BytesIO(content), mode="r:gz") as archive:
            members = archive.getmembers()
            for member in members:
                if not _is_safe_tar_member(root_resolved, member):
                    raise ArchiveDiffError(
                        code="unsafe_archive_entry",
                        message=f"Archive contains unsafe entry: {member.name}",
                    )
            archive.extractall(root, members=members, filter="data")
        children = [path for path in root.iterdir()]
        if len(children) == 1 and children[0].is_dir():
            extracted_root = children[0]
        else:
            extracted_root = root
        return ExtractedArchive(root=extracted_root, temp_dir=temp_dir)
    except Exception:
        temp_dir.cleanup()
        raise


def build_file_changes(from_root: Path, to_root: Path) -> list[dict[str, Any]]:
    before = _collect_files(from_root)
    after = _collect_files(to_root)

    added = set(after) - set(before)
    removed = set(before) - set(after)
    common = set(before) & set(after)

    renames = _detect_renames(before, after, added, removed)
    file_changes: list[dict[str, Any]] = []

    renamed_targets = {new for _, new in renames}
    renamed_sources = {old for old, _ in renames}
    for old_path, new_path in sorted(renames):
        file_changes.append(
            {
                "path": new_path,
                "previous_path": old_path,
                "status": "renamed",
                "additions": 0,
                "deletions": 0,
                "changes": 0,
                "patch": format_git_diff_patch(
                    path=new_path,
                    previous_path=old_path,
                    status="renamed",
                ),
            }
        )

    for path in sorted(added - renamed_targets):
        file_changes.append(_create_change(path, None, after[path], status="added"))
    for path in sorted(removed - renamed_sources):
        file_changes.append(_create_change(path, before[path], None, status="removed"))
    for path in sorted(common):
        if before[path]["hash"] == after[path]["hash"]:
            continue
        file_changes.append(
            _create_change(path, before[path], after[path], status="modified")
        )
    return file_changes


def _collect_files(root: Path) -> dict[str, dict[str, Any]]:
    files: dict[str, dict[str, Any]] = {}
    for path in root.rglob("*"):
        if not path.is_file() or _should_skip(path.relative_to(root)):
            continue
        content = path.read_bytes()
        files[_relative_posix_path(path, root)] = {
            "hash": hashlib.sha1(content).hexdigest(),
            "size": len(content),
            "binary": b"\0" in content[:4096],
            "content": content,
        }
    return files


def _detect_renames(
    before: dict[str, dict[str, Any]],
    after: dict[str, dict[str, Any]],
    added: set[str],
    removed: set[str],
) -> list[tuple[str, str]]:
    removed_by_hash: dict[str, list[str]] = {}
    for path in removed:
        removed_by_hash.setdefault(before[path]["hash"], []).append(path)

    renames: list[tuple[str, str]] = []
    for path in added:
        matches = removed_by_hash.get(after[path]["hash"], [])
        if not matches:
            continue
        old_path = matches.pop(0)
        renames.append((old_path, path))
    return renames


def _create_change(
    path: str,
    before: dict[str, Any] | None,
    after: dict[str, Any] | None,
    *,
    status: str,
) -> dict[str, Any]:
    before_lines = _decode_lines(before["content"]) if before else []
    after_lines = _decode_lines(after["content"]) if after else []
    patch = None
    additions = 0
    deletions = 0
    if before and after and not before["binary"] and not after["binary"]:
        raw_patch = "".join(
            difflib.unified_diff(
                before_lines,
                after_lines,
                fromfile=f"a/{path}",
                tofile=f"b/{path}",
                n=3,
            )
        )
        patch = format_git_diff_patch(path=path, status=status, patch=raw_patch)
        additions = sum(
            1
            for line in raw_patch.splitlines()
            if line.startswith("+") and not line.startswith("+++")
        )
        deletions = sum(
            1
            for line in raw_patch.splitlines()
            if line.startswith("-") and not line.startswith("---")
        )
    elif after and not after["binary"]:
        additions = len(after_lines)
        raw_patch = _build_single_sided_patch(
            path=path,
            status=status,
            before_lines=[],
            after_lines=after_lines,
        )
        patch = format_git_diff_patch(path=path, status=status, patch=raw_patch)
    elif before and not before["binary"]:
        deletions = len(before_lines)
        raw_patch = _build_single_sided_patch(
            path=path,
            status=status,
            before_lines=before_lines,
            after_lines=[],
        )
        patch = format_git_diff_patch(path=path, status=status, patch=raw_patch)
    elif before or after:
        patch = format_git_diff_patch(
            path=path,
            status=status,
            binary=True,
        )

    return {
        "path": path,
        "previous_path": None,
        "status": status,
        "additions": additions,
        "deletions": deletions,
        "changes": additions + deletions,
        "patch": patch,
    }


def _decode_lines(content: bytes) -> list[str]:
    return content.decode("utf-8", errors="replace").splitlines(keepends=True)


def _build_single_sided_patch(
    *,
    path: str,
    status: str,
    before_lines: list[str],
    after_lines: list[str],
) -> str | None:
    """Build a unified diff for added or removed text files when body output is needed."""
    if omit_diff_body(path, status):
        return None
    return "".join(
        difflib.unified_diff(
            before_lines,
            after_lines,
            fromfile="/dev/null" if status == "added" else f"a/{path}",
            tofile="/dev/null" if status == "removed" else f"b/{path}",
            n=3,
        )
    )


def _relative_posix_path(path: PurePath, root: PurePath) -> str:
    """Return a root-relative path with POSIX separators for git-style diff labels."""
    return path.relative_to(root).as_posix()


def _should_skip(path: Path) -> bool:
    skip_parts = {".git", ".hg", "__pycache__", ".tox", ".mypy_cache", ".ruff_cache"}
    if any(part in skip_parts for part in path.parts):
        return True
    if path.suffix in {".pyc", ".pyo"}:
        return True
    return False
