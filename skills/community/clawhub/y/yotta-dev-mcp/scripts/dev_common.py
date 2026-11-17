#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared constants and filesystem helpers for yotta-dev-mcp."""

import os
import re
from pathlib import Path


IGNORE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", ".next", ".nuxt", ".cache", ".tmp", ".tmp2",
    ".workflow", ".codex", ".cursor", ".claude", ".agents",
    "scratch", "_scratch", "_probe", "probe", "probes",
    "sandbox", ".sandbox", "debug", "_debug",
    "temp", "tmp", ".yottameta", "vendor", "third_party",
}
IGNORE_DIR_PATTERNS = (
    re.compile(r"(?i)^_bak(?:[_-].*)?$"),
)
IGNORE_TEMP_FILE_RE = re.compile(
    r"(?i)^(?:probe[_-].*|_probe[_-].*|scratch[_-].*|_scratch[_-].*|tmp_.*|temp_.*|.*_tmp)"
    r"\.(?:py|js|jsx|mjs|cjs|ts|tsx|sh|ps1|go|rs|java|kt|kts|rb|php)$"
)
SOURCE_EXTS = {
    ".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".sh", ".ps1",
    ".go", ".rs", ".java", ".kt", ".kts", ".rb", ".php",
}
TEXT_EXTS = SOURCE_EXTS | {".json", ".md", ".txt", ".yml", ".yaml", ".toml", ".ini", ".cfg"}
MAX_FILE_BYTES = 2 * 1024 * 1024

JS_EXTS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs")
CONFIG_NAMES = {
    "package.json", "package-lock.json", "tsconfig.json", "pyproject.toml",
    "setup.cfg", "requirements.txt", "requirements-dev.txt", "Cargo.toml",
    "go.mod", "Makefile", "Dockerfile", "docker-compose.yml", "docker-compose.yaml",
    ".eslintrc.json", ".eslintrc.js", ".prettierrc", ".prettierrc.json",
}
CONFIG_SUFFIXES = (".toml", ".ini", ".cfg", ".yml", ".yaml")
STORAGE_SUFFIXES = {
    ".sqlite": "sqlite-file", ".sqlite3": "sqlite-file",
    ".db": "db-file", ".mdb": "db-file", ".dbf": "db-file",
}
TEST_NAME_RE = re.compile(
    r"(?i)^test_.*\.(py|js|ts|jsx|tsx)$|_test\.py$|\.(test|spec)\.[jt]sx?$"
)
UNKNOWN_LIMIT = 50
EVIDENCE_LIMIT = 100
RISK_ENUM_WEIGHTS = {"critical": 5, "high": 4, "medium": 2, "low": 1}
CONE_LIMIT = 500
SYMBOL_MATCH_LIMIT = 20
IMPORT_KINDS_DECISIVE = ("internal", "internal-file")
BLAST_LEVELS = ((9, "critical"), (6, "high"), (3, "medium"))
VERIFY_LEVELS = ("L0", "L1", "L2", "L3", "L4", "L5")
VERIFY_EXEC_LEVELS = ("L2", "L3", "L4")
VERIFY_DEFAULT_LEVELS = ("L0", "L1")
VERIFY_REQUIRED_SOURCE_FILES = (
    "SKILL.md", "package.json", "README.md", "README.zh-CN.md",
    "CHANGELOG.md", "LICENSE", "NOTICE", "server.json", "install.sh",
    "bin/yotta-dev-mcp.js", "bin/install.js",
    "scripts/dev_engine.py", "scripts/yotta_dev_mcp.py",
    "scripts/dev_adapters.py", "scripts/dev_common.py", "scripts/dev_model.py",
    "scripts/dev_architecture.py", "scripts/dev_impact.py", "scripts/dev_verify.py",
    "scripts/dev_selftest.py",
    "references/tools.md", "references/adapters.md",
    "references/architecture-contract.md", "assets/banner.png",
)
VERIFY_REQUIRED_INSTALLED_FILES = ("SKILL.md",)
VERIFY_REQUIRED_INSTALLED_ASSETS = ("assets/banner.png",)
LEAN_INSTALL_MARKERS = ("_icon.png",)
VERIFY_WRITE_GATES = (
    ("run_checks", "allow_execute"),
    ("scaffold_skill", "apply"),
    ("workflow_state", "apply"),
    ("verify_change", "allow_execute"),
    ("run_adapter", "allow_execute"),
)

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")
ERROR_RE = re.compile(
    r"(?i)(traceback|exception|\berror\b|\bfailed\b|\bfail\b|fatal|panic|"
    r"assertion|npm err!|\berr\b|\bwarn(?:ing)?\b)"
)


def source_exts():
    return set(SOURCE_EXTS)


def _is_ignored_dir(name):
    return name in IGNORE_DIRS or any(
        pattern.match(name) for pattern in IGNORE_DIR_PATTERNS
    )


def _json_safe(value):
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(v) for v in value]
    return value


def _read_text(path):
    path = Path(path)
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError("文件超过大小上限: %s" % path)
    data = path.read_bytes()
    if b"\x00" in data[:4096]:
        raise ValueError("二进制文件不参与文本扫描: %s" % path)
    return data.decode("utf-8-sig", errors="replace")


def _iter_files(root, extensions=None, max_files=5000, all_files=False, ignore_temp=True):
    root = Path(root)
    extensions = set(extensions or TEXT_EXTS)
    count = 0
    for current, dirs, files in os.walk(str(root)):
        dirs[:] = sorted(d for d in dirs if not _is_ignored_dir(d))
        for name in sorted(files):
            if ignore_temp and IGNORE_TEMP_FILE_RE.match(name):
                continue
            path = Path(current) / name
            if path.is_symlink():
                continue
            if not all_files and extensions and path.suffix.lower() not in extensions:
                continue
            if path.stat().st_size > MAX_FILE_BYTES:
                continue
            yield path
            count += 1
            if count >= max_files:
                return


def _rel(root, path):
    try:
        return str(Path(path).resolve().relative_to(Path(root).resolve())).replace("\\", "/")
    except ValueError:
        return str(Path(path)).replace("\\", "/")


def _language(path):
    ext = Path(path).suffix.lower()
    if ext == ".py":
        return "python"
    if ext in (".js", ".jsx", ".mjs", ".cjs"):
        return "javascript"
    if ext in (".ts", ".tsx"):
        return "typescript"
    if ext in (".sh", ".ps1"):
        return "shell"
    return ext.lstrip(".") or "text"


def _frontmatter_version(text):
    match = re.search(r"(?m)^version:\s*[\"']?([^\"'\r\n]+)", text)
    return match.group(1).strip() if match else None


def _frontmatter_name(text):
    match = re.search(r"(?m)^name:\s*[\"']?([^\"'\r\n]+)", text)
    return match.group(1).strip() if match else None
