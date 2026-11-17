#!/usr/bin/env python3
"""Parse unified git diff into structured JSON.

Reads `git diff` output from stdin, a file argument, or `--collect`
(auto-collect tracked + untracked changes from the git repo) and
outputs a JSON object with per-file diffs including parsed hunks,
line types, and change statistics.

Works from any CWD inside a git repo — detects the repo root
automatically so it behaves the same on cmd, PowerShell, Linux, and
macOS.

Inspired by open-code-review's internal/diff/parser.go + hunk.go.
"""

import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from difflib import unified_diff
from enum import Enum
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Regex patterns — mirrors OCR's parser.go
# ---------------------------------------------------------------------------
DIFF_HEADER_RE = re.compile(r"^diff --git a/(.+?) b/(.+)$")
OLD_FILE_RE = re.compile(r"^--- (?:(?:a/(.+))|(/dev/null))$")
NEW_FILE_RE = re.compile(r"^\+\+\+ (?:(?:b/(.+))|(/dev/null))$")
BINARY_RE = re.compile(r"^Binary files ")
HUNK_HEADER_RE = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@")
REVIEW_META_RE = re.compile(
    r"^review-workflow-meta: size_bytes=(\d+) is_large=(true|false)"
    r"(?: skipped_reason=([^\s]+))?$"
)

# ---------------------------------------------------------------------------
# Data model — mirrors OCR's model/diff.go + diff/hunk.go
# ---------------------------------------------------------------------------


class LineType(str, Enum):
    CONTEXT = "context"
    ADDED = "added"
    DELETED = "deleted"


@dataclass
class HunkLine:
    type: LineType
    content: str  # content WITHOUT the leading +/-/space marker


@dataclass
class Hunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list[HunkLine] = field(default_factory=list)


@dataclass
class FileDiff:
    old_path: str
    new_path: str
    diff_raw: str = ""
    hunks: list[Hunk] = field(default_factory=list)
    insertions: int = 0
    deletions: int = 0
    is_binary: bool = False
    is_new: bool = False
    is_deleted: bool = False
    is_large: bool = False
    size_bytes: Optional[int] = None
    skipped_reason: Optional[str] = None

    @property
    def effective_path(self) -> str:
        """Return the path that matters for review (new_path, or old_path for deleted)."""
        if self.new_path == "/dev/null":
            return self.old_path
        return self.new_path

    @property
    def status(self) -> str:
        if self.is_binary:
            return "binary"
        if self.is_new:
            return "added"
        if self.is_deleted:
            return "deleted"
        if self.old_path != self.new_path and self.old_path != "" and self.old_path != "/dev/null":
            return "renamed"
        return "modified"


@dataclass
class DiffResult:
    files: list[FileDiff] = field(default_factory=list)
    total_files: int = 0
    total_insertions: int = 0
    total_deletions: int = 0


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def _parse_hunk_header(line: str) -> tuple[int, int, int, int]:
    """Parse `@@ -old_start,old_count +new_start,new_count @@` into ints."""
    m = HUNK_HEADER_RE.match(line)
    if not m:
        raise ValueError(f"Invalid hunk header: {line}")
    old_start = int(m.group(1))
    old_count = int(m.group(2)) if m.group(2) else 1
    new_start = int(m.group(3))
    new_count = int(m.group(4)) if m.group(4) else 1
    return old_start, old_count, new_start, new_count


def _parse_hunks(raw_diff: str) -> list[Hunk]:
    """Parse the hunks from a single file's raw diff text.

    Lines before the first `@@` header (file-level metadata like
    `diff --git`, `---`, `+++`) are ignored.
    """
    hunks: list[Hunk] = []
    current: Optional[Hunk] = None

    for line in raw_diff.split("\n"):
        m = HUNK_HEADER_RE.match(line)
        if m:
            if current is not None:
                hunks.append(current)
            old_start, old_count, new_start, new_count = _parse_hunk_header(line)
            current = Hunk(
                old_start=old_start,
                old_count=old_count,
                new_start=new_start,
                new_count=new_count,
            )
            continue

        if current is None:
            continue  # skip file-level headers

        # Skip `\ No newline at end of file` and inter-file diff boundaries
        if line.startswith("\\ No newline at end of file"):
            continue
        if line.startswith("diff --git "):
            break

        if line.startswith("+") and not line.startswith("+++"):
            current.lines.append(HunkLine(type=LineType.ADDED, content=line[1:]))
        elif line.startswith("-") and not line.startswith("---"):
            current.lines.append(HunkLine(type=LineType.DELETED, content=line[1:]))
        else:
            # Context line: leading ' ' stripped
            content = line[1:] if line.startswith(" ") else line
            current.lines.append(HunkLine(type=LineType.CONTEXT, content=content))

    if current is not None:
        hunks.append(current)

    return hunks


def _file_marker_path(match: re.Match[str]) -> str:
    """Return the path from a ---/+++ file marker, including /dev/null."""
    for group in match.groups():
        if group is not None:
            return group
    return ""


def parse_diff_text(diff_text: str) -> DiffResult:
    """Parse full unified diff text and return structured DiffResult."""
    lines = diff_text.split("\n")
    result = DiffResult()
    current: Optional[FileDiff] = None
    buf: list[str] = []

    for line in lines:
        if m := DIFF_HEADER_RE.match(line):
            # Flush previous diff
            if current is not None:
                current.diff_raw = "\n".join(buf).rstrip("\n")
                current.hunks = _parse_hunks(current.diff_raw)
                result.files.append(current)
                buf = []
            current = FileDiff(old_path=m.group(1), new_path=m.group(2))

        if current is None:
            continue

        # Detect file-level flags
        if BINARY_RE.match(line):
            current.is_binary = True
        elif m := REVIEW_META_RE.match(line):
            current.size_bytes = int(m.group(1))
            current.is_large = m.group(2) == "true"
            current.skipped_reason = m.group(3)
        elif m := OLD_FILE_RE.match(line):
            if _file_marker_path(m) == "/dev/null":
                current.is_new = True
        elif m := NEW_FILE_RE.match(line):
            if _file_marker_path(m) == "/dev/null":
                current.is_deleted = True
        elif line.startswith("+") and not line.startswith("+++"):
            current.insertions += 1
        elif line.startswith("-") and not line.startswith("---"):
            current.deletions += 1

        buf.append(line)

    # Flush last diff
    if current is not None:
        current.diff_raw = "\n".join(buf).rstrip("\n")
        current.hunks = _parse_hunks(current.diff_raw)
        result.files.append(current)

    # Aggregate totals
    result.total_files = len(result.files)
    result.total_insertions = sum(f.insertions for f in result.files)
    result.total_deletions = sum(f.deletions for f in result.files)

    return result


# ---------------------------------------------------------------------------
# Git collection helpers — tracked diff + untracked file diffs
# ---------------------------------------------------------------------------


def _find_repo_root() -> str:
    """Return the absolute path to the git repository root.

    Uses `git rev-parse --show-toplevel` so this works from any
    subdirectory of the repo, on any platform (Windows/cmd/PowerShell,
    Linux, macOS).
    """
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        print(
            "fatal: not a git repository (or any of the parent directories): .git",
            file=sys.stderr,
        )
        sys.exit(1)
    return proc.stdout.strip()


def _run_git(repo_root: str, args: list[str]) -> str:
    """Run a git command inside *repo_root* and return UTF-8 output."""
    proc = subprocess.run(
        ["git", "-C", repo_root, *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return proc.stdout.decode("utf-8", errors="replace")


def _to_git_path(path: str) -> str:
    """Normalize a repository path for git diff headers."""
    return Path(path).as_posix()


def _is_binary_content(content: bytes) -> bool:
    """Heuristic matching git's main binary signal well enough for review routing."""
    return b"\x00" in content


# ---------------------------------------------------------------------------
# Untracked-file filtering constants
# ---------------------------------------------------------------------------

# Files larger than this are recorded as metadata-only (no content expansion).
MAX_UNTRACKED_BYTES = 512 * 1024

# Directory names that should be skipped at any nesting level.
SKIP_DIRS = (
    ".git/",
    "node_modules/",
    "vendor/",
    "__pycache__/",
    ".venv/",
    "venv/",
    "dist/",
    "build/",
    ".next/",
    ".turbo/",
    "coverage/",
    ".pytest_cache/",
    "target/",
)
SKIP_DIR_NAMES = tuple(directory.strip("/") for directory in SKIP_DIRS)

# Suffixes that should be skipped regardless of directory.
SKIP_SUFFIXES = (
    ".lock",
    ".map",
    ".min.js",
    ".min.css",
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".webp",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".pyc",
    ".class",
    ".o",
    ".so",
    ".dylib",
    ".dll",
    ".exe",
    ".bin",
)


# ---------------------------------------------------------------------------
# Untracked-file diff helpers
# ---------------------------------------------------------------------------


def _should_skip_untracked(path: str) -> bool:
    """Return true when an untracked path should not be read into review input."""
    normalized = _to_git_path(path).lower()
    parts = [part for part in normalized.split("/") if part]
    if any(part in SKIP_DIR_NAMES for part in parts):
        return True
    return normalized.endswith(SKIP_SUFFIXES)


def _skipped_untracked_file_diff(
    path: str,
    size_bytes: int,
    reason: str,
    *,
    is_large: bool = False,
) -> str:
    """Create metadata-only diff for an untracked file that should not be expanded."""
    git_path = _to_git_path(path)
    return "\n".join(
        [
            f"diff --git a/{git_path} b/{git_path}",
            "new file mode 100644",
            f"review-workflow-meta: size_bytes={size_bytes} is_large={str(is_large).lower()} skipped_reason={reason}",
            "--- /dev/null",
            f"+++ b/{git_path}",
        ]
    )


def _untracked_file_diff(path: str, repo_root: str) -> str:
    """Create a unified diff for one untracked file.

    *path* is relative to *repo_root* (as returned by `git ls-files`).
    """
    abs_path = Path(repo_root) / path
    git_path = _to_git_path(path)

    if abs_path.is_symlink():
        return _skipped_untracked_file_diff(path, 0, "symlink")

    try:
        size_bytes = abs_path.stat().st_size
    except OSError:
        return _skipped_untracked_file_diff(path, 0, "stat_error")

    header = [f"diff --git a/{git_path} b/{git_path}", "new file mode 100644"]

    if size_bytes > MAX_UNTRACKED_BYTES:
        return _skipped_untracked_file_diff(path, size_bytes, "max_file_bytes", is_large=True)

    try:
        content = abs_path.read_bytes()
    except OSError:
        return _skipped_untracked_file_diff(path, size_bytes, "read_error")

    if _is_binary_content(content):
        return "\n".join(
            [
                *header,
                f"review-workflow-meta: size_bytes={size_bytes} is_large=false",
                f"Binary files /dev/null and b/{git_path} differ",
            ]
        )

    text = content.decode("utf-8", errors="replace")
    lines = text.splitlines()
    if not lines:
        return "\n".join([*header, "--- /dev/null", f"+++ b/{git_path}"])

    body = unified_diff(
        [],
        lines,
        fromfile="/dev/null",
        tofile=f"b/{git_path}",
        lineterm="",
    )
    return "\n".join([*header, f"review-workflow-meta: size_bytes={size_bytes} is_large=false", *body])


def collect_git_diff(repo_root: str, include_untracked: bool = True) -> str:
    """Collect tracked git diff and synthesize diffs for untracked files.

    *repo_root* must be an absolute path (use `_find_repo_root()`).
    """
    parts: list[str] = []
    tracked = _run_git(repo_root, ["diff", "HEAD", "--no-color", "--no-ext-diff", "-U3", "--"])
    if tracked.strip():
        parts.append(tracked.rstrip("\n"))

    if include_untracked:
        raw_paths = _run_git(repo_root, ["ls-files", "-z", "--others", "--exclude-standard"])
        for path in [p for p in raw_paths.split("\0") if p]:
            if _should_skip_untracked(path):
                continue
            parts.append(_untracked_file_diff(path, repo_root))

    return "\n".join(parts)


def _read_stdin_utf8() -> str:
    """Read stdin as UTF-8 regardless of the host shell code page."""
    return sys.stdin.buffer.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Main — read from stdin, file argument, or --collect
# ---------------------------------------------------------------------------


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # ---------- determine input source ----------
    if len(sys.argv) >= 2 and sys.argv[1] == "--collect":
        repo_root = _find_repo_root()
        diff_text = collect_git_diff(repo_root, include_untracked=True)
    elif len(sys.argv) > 1:
        diff_text = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        diff_text = _read_stdin_utf8()

    result = parse_diff_text(diff_text)

    # Custom encoder to handle dataclasses + enums
    def _encode(obj):
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, "__dataclass_fields__"):
            return asdict(obj)
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    json.dump(result, sys.stdout, default=_encode, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
