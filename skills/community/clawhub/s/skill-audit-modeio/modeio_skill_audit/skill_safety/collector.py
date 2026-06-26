from __future__ import annotations

import os
from pathlib import Path

from .common import is_probably_binary, is_test_or_fixture_path, safe_rel, sha256_text
from .constants import (
    EXECUTABLE_EXTENSIONS,
    HIGH_PRIORITY_FILES,
    MAX_FILE_BYTES,
    PROMPT_SURFACE_FILENAMES,
    PROMPT_SURFACE_HINTS,
    SKIP_DIR_NAMES,
    TEXT_EXTENSIONS,
)
from .models import FileRecord, ScanStats


def is_prompt_surface(rel_path: Path) -> bool:
    rel = str(rel_path).replace("\\", "/")
    rel_lower = rel.lower()
    name = rel_path.name
    suffix = rel_path.suffix.lower()

    if name in PROMPT_SURFACE_FILENAMES:
        return True
    if "/prompts/" in f"/{rel_lower}" or "/docs/" in f"/{rel_lower}":
        return suffix in {".md", ".txt", ".yaml", ".yml", ".json", ".html", ".htm"}
    if suffix in {".html", ".htm"}:
        return True
    if suffix in {".md", ".txt", ".html", ".htm"} and any(hint in rel_lower for hint in PROMPT_SURFACE_HINTS):
        return True
    if suffix in {".html", ".htm"} and any(token in rel_lower for token in ("injection", "prompt", "attack", "malicious", "exfil")):
        return True
    return False


def is_executable_surface(rel_path: Path) -> bool:
    suffix = rel_path.suffix.lower()
    if suffix in EXECUTABLE_EXTENSIONS:
        return True
    if rel_path.name in {"Makefile", "Dockerfile", "package.json", "pyproject.toml", "requirements.txt"}:
        return True
    rel = str(rel_path).replace("\\", "/")
    if rel.startswith(".github/workflows/"):
        return True
    return False


def should_scan_file(rel_path: Path) -> bool:
    rel = str(rel_path).replace("\\", "/")
    if is_test_or_fixture_path(rel_path) and not rel.startswith(".github/workflows/"):
        return False
    if rel_path.name in HIGH_PRIORITY_FILES:
        return True
    if rel_path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    if rel.startswith(".github/workflows/"):
        return True
    return False


def collect_file_records(target_repo: Path) -> tuple[list[FileRecord], ScanStats, list[str]]:
    records: list[FileRecord] = []
    file_hash_tokens: list[str] = []

    stats: ScanStats = {
        "total_files_seen": 0,
        "candidate_files": 0,
        "files_scanned": 0,
        "skipped_large_files": 0,
        "skipped_unreadable_files": 0,
        "skipped_large_executable_files": 0,
        "skipped_unreadable_executable_files": 0,
    }

    for dirpath, dirnames, filenames in os.walk(target_repo):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIR_NAMES]
        root = Path(dirpath)

        for filename in filenames:
            stats["total_files_seen"] += 1
            abs_path = root / filename
            rel_path = abs_path.relative_to(target_repo)

            if not should_scan_file(rel_path):
                continue
            stats["candidate_files"] += 1

            is_exec = is_executable_surface(rel_path)
            try:
                file_size = abs_path.stat().st_size
            except OSError:
                stats["skipped_unreadable_files"] += 1
                if is_exec:
                    stats["skipped_unreadable_executable_files"] += 1
                continue

            if file_size > MAX_FILE_BYTES:
                stats["skipped_large_files"] += 1
                if is_exec:
                    stats["skipped_large_executable_files"] += 1
                continue

            try:
                text = abs_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                try:
                    text = abs_path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    stats["skipped_unreadable_files"] += 1
                    if is_exec:
                        stats["skipped_unreadable_executable_files"] += 1
                    continue
            except OSError:
                stats["skipped_unreadable_files"] += 1
                if is_exec:
                    stats["skipped_unreadable_executable_files"] += 1
                continue

            if is_probably_binary(text):
                stats["skipped_unreadable_files"] += 1
                if is_exec:
                    stats["skipped_unreadable_executable_files"] += 1
                continue

            stats["files_scanned"] += 1
            rel = safe_rel(abs_path, target_repo)
            lines = text.splitlines()
            content_hash = sha256_text(text)
            file_hash_tokens.append(f"{rel}:{content_hash}")

            records.append(
                {
                    "path_obj": rel_path,
                    "rel_path": rel,
                    "text": text,
                    "lines": lines,
                    "is_prompt_surface": is_prompt_surface(rel_path),
                    "is_executable_surface": is_exec,
                }
            )

    return records, stats, file_hash_tokens
