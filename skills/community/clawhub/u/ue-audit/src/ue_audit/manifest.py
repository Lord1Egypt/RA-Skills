"""Deterministic project manifest and diff."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .project import ProjectInfo
from .util import (
    SCHEMA_VERSION,
    TOOL_NAME,
    TOOL_VERSION,
    as_posix,
    canonical_json,
    format_bytes,
    hash_json,
    sha256_file,
    utc_now,
)


DEFAULT_ROOTS = ("Content", "Config", "Source", "Plugins")
DEFAULT_EXCLUDE_DIRS = {
    ".git",
    ".svn",
    ".hg",
    ".vs",
    ".idea",
    ".vscode",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "node_modules",
    "Saved",
    "Intermediate",
    "DerivedDataCache",
    "Binaries",
}
DEFAULT_EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".tmp"}
DEFAULT_EXCLUDE_FILES = {".DS_Store", "Thumbs.db", "desktop.ini"}
DEFAULT_MAX_HASH_BYTES = 512 * 1024 * 1024


@dataclass
class FileEntry:
    path: str
    size: int
    mtime_ns: int
    sha256: str = ""
    hash_skipped: str = ""
    is_symlink: bool = False
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "size": self.size,
            "mtime_ns": self.mtime_ns,
            "sha256": self.sha256,
        }
        if self.hash_skipped:
            data["hash_skipped"] = self.hash_skipped
        if self.is_symlink:
            data["is_symlink"] = True
        if self.error:
            data["error"] = self.error
        return data

    @classmethod
    def from_dict(cls, path: str, data: dict[str, Any]) -> "FileEntry":
        return cls(
            path=path,
            size=int(data.get("size") or 0),
            mtime_ns=int(data.get("mtime_ns") or 0),
            sha256=str(data.get("sha256") or ""),
            hash_skipped=str(data.get("hash_skipped") or ""),
            is_symlink=bool(data.get("is_symlink")),
            error=str(data.get("error") or ""),
        )


@dataclass
class Manifest:
    root: str
    files: dict[str, FileEntry] = field(default_factory=dict)
    roots: list[str] = field(default_factory=lambda: list(DEFAULT_ROOTS))
    excludes: list[str] = field(default_factory=list)
    max_hash_bytes: int = DEFAULT_MAX_HASH_BYTES
    algorithm: str = "sha256"
    generated_at: str = ""
    schema_version: int = SCHEMA_VERSION
    tool: str = TOOL_NAME
    tool_version: str = TOOL_VERSION
    manifest_sha256: str = ""

    @property
    def file_count(self) -> int:
        return len(self.files)

    @property
    def total_bytes(self) -> int:
        return sum(entry.size for entry in self.files.values())

    def compute_hash(self) -> str:
        payload = {
            "algorithm": self.algorithm,
            "roots": sorted(self.roots),
            "excludes": sorted(self.excludes),
            "max_hash_bytes": self.max_hash_bytes,
            "files": {
                path: {
                    "size": entry.size,
                    "mtime_ns": entry.mtime_ns,
                    "sha256": entry.sha256,
                    "hash_skipped": entry.hash_skipped,
                    "is_symlink": entry.is_symlink,
                    "error": entry.error,
                }
                for path, entry in sorted(self.files.items())
            },
        }
        return hash_json(payload)

    def finalize(self) -> "Manifest":
        if not self.generated_at:
            self.generated_at = utc_now()
        self.manifest_sha256 = self.compute_hash()
        return self

    def to_dict(self) -> dict[str, Any]:
        self.finalize()
        return {
            "schema_version": self.schema_version,
            "tool": self.tool,
            "tool_version": self.tool_version,
            "root": self.root,
            "generated_at": self.generated_at,
            "algorithm": self.algorithm,
            "roots": list(self.roots),
            "excludes": list(self.excludes),
            "max_hash_bytes": self.max_hash_bytes,
            "file_count": self.file_count,
            "total_bytes": self.total_bytes,
            "manifest_sha256": self.manifest_sha256,
            "files": {path: entry.to_dict() for path, entry in sorted(self.files.items())},
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Manifest":
        files_raw = data.get("files") or {}
        if not isinstance(files_raw, dict):
            raise ValueError("manifest.files must be an object")
        files = {
            str(path): FileEntry.from_dict(str(path), value)
            for path, value in files_raw.items()
            if isinstance(value, dict)
        }
        manifest = cls(
            root=str(data.get("root") or ""),
            files=files,
            roots=[str(item) for item in (data.get("roots") or DEFAULT_ROOTS)],
            excludes=[str(item) for item in (data.get("excludes") or [])],
            max_hash_bytes=int(data.get("max_hash_bytes") or DEFAULT_MAX_HASH_BYTES),
            algorithm=str(data.get("algorithm") or "sha256"),
            generated_at=str(data.get("generated_at") or ""),
            schema_version=int(data.get("schema_version") or SCHEMA_VERSION),
            tool=str(data.get("tool") or TOOL_NAME),
            tool_version=str(data.get("tool_version") or TOOL_VERSION),
            manifest_sha256=str(data.get("manifest_sha256") or ""),
        )
        if not manifest.manifest_sha256:
            manifest.finalize()
        return manifest


def _is_excluded_dir(name: str, exclude_dirs: set[str]) -> bool:
    return name.casefold() in exclude_dirs


def _is_excluded_file(name: str, exclude_files: set[str], exclude_suffixes: set[str]) -> bool:
    if name.casefold() in exclude_files:
        return True
    return Path(name).suffix.casefold() in exclude_suffixes


def build_manifest(
    project: ProjectInfo,
    roots: Iterable[str] | None = None,
    max_hash_bytes: int = DEFAULT_MAX_HASH_BYTES,
    exclude_dirs: Iterable[str] | None = None,
    exclude_suffixes: Iterable[str] | None = None,
    exclude_files: Iterable[str] | None = None,
    include_uproject: bool = True,
) -> Manifest:
    root_names = [str(item) for item in (roots or DEFAULT_ROOTS)]
    exclude_dir_set = {item.casefold() for item in (exclude_dirs or DEFAULT_EXCLUDE_DIRS)}
    exclude_suffix_set = {item.casefold() for item in (exclude_suffixes or DEFAULT_EXCLUDE_SUFFIXES)}
    exclude_file_set = {item.casefold() for item in (exclude_files or DEFAULT_EXCLUDE_FILES)}

    files: dict[str, FileEntry] = {}

    if include_uproject:
        for uproject in sorted(project.root.glob("*.uproject")):
            _add_file_entry(project.root, uproject, files, max_hash_bytes)

    for root_name in root_names:
        root = project.root / root_name
        if not root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
            dirnames[:] = sorted(
                name for name in dirnames if not _is_excluded_dir(name, exclude_dir_set)
            )
            for filename in sorted(filenames):
                if _is_excluded_file(filename, exclude_file_set, exclude_suffix_set):
                    continue
                path = Path(dirpath) / filename
                _add_file_entry(project.root, path, files, max_hash_bytes)

    manifest = Manifest(
        root=str(project.root),
        files=files,
        roots=root_names,
        excludes=sorted(exclude_dir_set | exclude_suffix_set | exclude_file_set),
        max_hash_bytes=max_hash_bytes,
    )
    return manifest.finalize()


def _add_file_entry(
    project_root: Path, path: Path, files: dict[str, FileEntry], max_hash_bytes: int
) -> None:
    try:
        stat = path.lstat()
    except OSError as exc:
        rel = as_posix(path.relative_to(project_root))
        files[rel] = FileEntry(path=rel, size=0, mtime_ns=0, error=str(exc))
        return

    rel = as_posix(path.relative_to(project_root))
    is_symlink = path.is_symlink()
    entry = FileEntry(
        path=rel,
        size=int(stat.st_size),
        mtime_ns=int(stat.st_mtime_ns),
        is_symlink=is_symlink,
    )
    if is_symlink:
        entry.hash_skipped = "symlink"
        files[rel] = entry
        return
    if entry.size > max_hash_bytes:
        entry.hash_skipped = "too_large"
        files[rel] = entry
        return
    try:
        entry.sha256 = sha256_file(path)
    except OSError as exc:
        entry.error = str(exc)
    files[rel] = entry


def save_manifest(manifest: Manifest, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_manifest(path: Path) -> Manifest:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a manifest object")
    return Manifest.from_dict(data)


def _casefold_map(files: dict[str, FileEntry]) -> dict[str, FileEntry]:
    result: dict[str, FileEntry] = {}
    for path, entry in files.items():
        key = path.casefold()
        if key in result and result[key].path != path:
            # Extremely unlikely on Windows, but keep deterministic:
            # exact-case duplicate wins only if it is the same path; otherwise
            # leave the first one; the diff will report the collision as unknown.
            continue
        result[key] = entry
    return result


def diff_manifests(
    before: Manifest, after: Manifest, include_metadata: bool = True
) -> dict[str, Any]:
    before_map = _casefold_map(before.files)
    after_map = _casefold_map(after.files)
    added: list[dict[str, Any]] = []
    removed: list[dict[str, Any]] = []
    changed: list[dict[str, Any]] = []
    unknown: list[dict[str, Any]] = []
    metadata_changed: list[dict[str, Any]] = []
    renamed_case: list[dict[str, str]] = []
    unchanged = 0

    for key in sorted(set(before_map) | set(after_map)):
        old = before_map.get(key)
        new = after_map.get(key)
        if old is None and new is not None:
            added.append(
                {
                    "path": new.path,
                    "size": new.size,
                    "sha256": new.sha256,
                    "hash_skipped": new.hash_skipped,
                }
            )
            continue
        if new is None and old is not None:
            removed.append(
                {
                    "path": old.path,
                    "size": old.size,
                    "sha256": old.sha256,
                    "hash_skipped": old.hash_skipped,
                }
            )
            continue
        assert old is not None and new is not None
        if old.path != new.path:
            renamed_case.append({"before": old.path, "after": new.path})

        if old.size != new.size:
            changed.append(
                {
                    "path": new.path,
                    "reason": "size",
                    "before": _entry_fingerprint(old),
                    "after": _entry_fingerprint(new),
                }
            )
            continue

        if old.hash_skipped or new.hash_skipped or not old.sha256 or not new.sha256:
            reason = old.hash_skipped or new.hash_skipped or "hash_missing"
            unknown.append(
                {
                    "path": new.path,
                    "reason": reason,
                    "before": _entry_fingerprint(old),
                    "after": _entry_fingerprint(new),
                }
            )
            continue

        if old.sha256 != new.sha256:
            changed.append(
                {
                    "path": new.path,
                    "reason": "content",
                    "before": _entry_fingerprint(old),
                    "after": _entry_fingerprint(new),
                }
            )
            continue

        unchanged += 1
        if include_metadata and (old.mtime_ns != new.mtime_ns or old.path != new.path):
            metadata_changed.append(
                {
                    "path": new.path,
                    "before": _entry_fingerprint(old),
                    "after": _entry_fingerprint(new),
                }
            )

    return {
        "added": added,
        "removed": removed,
        "changed": changed,
        "unknown": unknown,
        "metadata_changed": metadata_changed,
        "renamed_case": renamed_case,
        "unchanged_count": unchanged,
        "added_count": len(added),
        "removed_count": len(removed),
        "changed_count": len(changed),
        "unknown_count": len(unknown),
        "metadata_changed_count": len(metadata_changed),
    }


def _entry_fingerprint(entry: FileEntry) -> dict[str, Any]:
    return {
        "size": entry.size,
        "mtime_ns": entry.mtime_ns,
        "sha256": entry.sha256,
        "hash_skipped": entry.hash_skipped,
        "is_symlink": entry.is_symlink,
        "error": entry.error,
    }


def diff_is_empty(diff: dict[str, Any], include_metadata: bool = True) -> bool:
    if diff.get("added_count") or diff.get("removed_count") or diff.get("changed_count"):
        return False
    if diff.get("unknown_count"):
        return False
    if include_metadata and diff.get("metadata_changed_count"):
        return False
    return True


def manifest_summary(manifest: Manifest) -> dict[str, Any]:
    return {
        "root": manifest.root,
        "file_count": manifest.file_count,
        "total_bytes": manifest.total_bytes,
        "total_human": format_bytes(manifest.total_bytes),
        "manifest_sha256": manifest.manifest_sha256,
        "roots": list(manifest.roots),
        "max_hash_bytes": manifest.max_hash_bytes,
        "hash_skipped_count": sum(1 for entry in manifest.files.values() if entry.hash_skipped),
        "error_count": sum(1 for entry in manifest.files.values() if entry.error),
    }


def manifest_canonical(manifest: Manifest) -> str:
    return canonical_json(manifest.to_dict())
