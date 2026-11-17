#!/usr/bin/env python3
"""Classify files by extension → language → review rule.

Consumes the JSON output of diff_parse.py (or a plain file list) and
outputs a JSON object mapping each file to its language, review-rule
reference path, and eligibility for review.

Inspired by open-code-review's internal/config/rules/system_rules.go +
internal/config/allowlist/allowed_ext.go.
"""

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Extension → language mapping
# ---------------------------------------------------------------------------

EXT_LANG_MAP: dict[str, str] = {
    # Rust
    ".rs": "rust",
    # Go
    ".go": "go",
    # Python
    ".py": "python",
    ".pyi": "python",
    # TypeScript / JavaScript
    ".ts": "typescript",
    ".tsx": "typescript+react",
    ".js": "javascript",
    ".jsx": "javascript+react",
    ".mjs": "javascript",
    ".cjs": "javascript",
    # Java
    ".java": "java",
    ".kt": "kotlin",
    ".scala": "scala",
    # Frontend frameworks
    ".vue": "vue",
    ".svelte": "svelte",
    # HTML / CSS
    ".html": "html",
    ".css": "css",
    ".scss": "css",
    ".less": "css",
    # Config / Data
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".xml": "xml",
    # Markdown / Docs
    ".md": "markdown",
    ".mdx": "markdown",
    ".rst": "markdown",
    # Shell
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".ps1": "shell",
    # SQL
    ".sql": "sql",
    # Docker
    "Dockerfile": "dockerfile",
}

# Special filename patterns (no extension)
SPECIAL_NAMES: dict[str, str] = {
    "Dockerfile": "dockerfile",
    "Makefile": "makefile",
    "BUILD": "bazel",
    "WORKSPACE": "bazel",
}

# ---------------------------------------------------------------------------
# Language → review rule file (relative to code-reviewer/references/)
# ---------------------------------------------------------------------------

LANG_RULE_MAP: dict[str, Optional[str]] = {
    "rust": "rust.md",
    "go": "go.md",
    "python": "python.md",
    "typescript": "typescript.md",
    "typescript+react": "typescript.md",
    "javascript": "typescript.md",
    "javascript+react": "typescript.md",
    "java": "java.md",
    "kotlin": "java.md",
    "scala": "java.md",
    "vue": "vue.md",
    "svelte": "svelte.md",
    "nestjs": "nestjs.md",
    "html": None,
    "css": None,
    "json": None,
    "yaml": None,
    "toml": None,
    "xml": None,
    "markdown": None,
    "shell": None,
    "sql": None,
    "dockerfile": None,
    "makefile": None,
    "bazel": None,
}

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class FileClassifyEntry:
    path: str
    language: Optional[str] = None
    rule_file: Optional[str] = None
    reviewable: bool = True
    exclude_reason: Optional[str] = None


@dataclass
class ClassifyResult:
    files: list[FileClassifyEntry] = field(default_factory=list)
    total: int = 0
    reviewable: int = 0
    excluded: int = 0
    language_groups: dict[str, list[str]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Classify logic
# ---------------------------------------------------------------------------


def classify_path(path: str) -> FileClassifyEntry:
    """Classify a single file path."""
    entry = FileClassifyEntry(path=path)
    name = Path(path).name
    suffix = Path(path).suffix.lower()

    # 1. Detect language
    lang: Optional[str] = None

    if name in SPECIAL_NAMES:
        lang = SPECIAL_NAMES[name]
    elif name.startswith("Dockerfile"):
        lang = "dockerfile"
    else:
        lang = EXT_LANG_MAP.get(suffix)

    entry.language = lang

    # 2. NestJS detection: *.ts files with specific markers
    if lang == "typescript":
        if _looks_like_nestjs(path):
            entry.language = "nestjs"
            lang = "nestjs"

    # 3. Map to rule file
    if lang:
        rule = LANG_RULE_MAP.get(lang)
        entry.rule_file = rule

    return entry


def _looks_like_nestjs(path: str) -> bool:
    """Heuristic: file paths that suggest NestJS project structure."""
    nest_markers = (
        ".module.ts",
        ".controller.ts",
        ".service.ts",
        ".guard.ts",
        ".interceptor.ts",
        ".pipe.ts",
        ".filter.ts",
        ".decorator.ts",
        ".dto.ts",
        "main.ts",
        "app.module.ts",
    )
    for marker in nest_markers:
        if marker in path:
            return True
    return False


def classify_all(diff_json) -> ClassifyResult:
    """Classify all files from diff_parse.DiffResult or its dict representation.

    Accepts: DiffResult dataclass, its __dict__, or a plain list of path strings.
    """
    result = ClassifyResult()

    paths = _extract_file_paths(diff_json)

    for p in paths:
        entry = classify_path(p)
        result.files.append(entry)
        result.total += 1
        if entry.reviewable:
            result.reviewable += 1
            lang = entry.language or "unknown"
            result.language_groups.setdefault(lang, []).append(p)
        else:
            result.excluded += 1

    return result


def _extract_file_paths(diff_json) -> list[str]:
    """Extract file paths from DiffResult dataclass, its __dict__, or a plain list."""
    if isinstance(diff_json, list):
        return [str(p) for p in diff_json]
    if isinstance(diff_json, dict) and "files" in diff_json:
        return [_extract_path(f) for f in diff_json["files"]]
    if hasattr(diff_json, "files"):
        return [_extract_path(f) for f in diff_json.files]
    raise ValueError("Expected list of paths or diff_parse.py output with 'files' key")


def _extract_path(f) -> str:
    """Extract the file path from a FileDiff dataclass or dict."""
    if hasattr(f, "effective_path"):
        return f.effective_path
    if hasattr(f, "new_path"):
        is_deleted = getattr(f, "is_deleted", False)
        is_binary = getattr(f, "is_binary", False)
        if is_deleted or is_binary:
            return getattr(f, "effective_path", getattr(f, "new_path", str(f)))
        return f.new_path
    if isinstance(f, dict):
        if f.get("is_deleted") or f.get("is_binary"):
            return f.get("effective_path", f.get("new_path", ""))
        return f.get("new_path", str(f))
    return str(f)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def _encode(obj):
    """Custom JSON encoder for dataclasses."""
    if hasattr(obj, "__dataclass_fields__"):
        return {k: v for k, v in obj.__dict__.items()}
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    if len(sys.argv) > 1:
        raw = Path(sys.argv[1]).read_text(encoding="utf-8")
    else:
        raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    data = json.loads(raw)
    result = classify_all(data)
    json.dump(result, sys.stdout, default=_encode, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
