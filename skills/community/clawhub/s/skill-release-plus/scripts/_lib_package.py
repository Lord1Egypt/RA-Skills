#!/usr/bin/env python3
"""
_lib_package.py — Shared packaging logic for skill-release-plus.

Provides:
  - load_exclude_config(skill_root: Path) -> (dirs, files, exts, patterns)
  - package_skill(slug, skill_dir, out_dir) -> dict {ok, path, file_count, files}
  - build_multipart_from_tarball(fields, tar_path, slug) -> (body, content_type, count)
  - try_sign_skill(skill_dir) -> dict {ok, hash, signed_at, signed_by, skipped}

Maintains the original release.py exclusion semantics:
  - dirs: exact directory name match (e.g. __pycache__, node_modules)
  - files: exact filename match (e.g. .DS_Store)
  - exts: extension match including dot (e.g. .pyc)
  - patterns: fnmatch wildcards against basename AND relative path

Design notes (preserved from upstream):
  - sign.key is included in the package (used for content verification on hub side)
  - tar member names use parent-dir prefix (e.g. "skill-release-plus/SKILL.md")
"""
from __future__ import annotations

import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from typing import Optional


MAX_PACKAGE_SIZE_BYTES = 2 * 1024 * 1024  # 2 MB single-file warn threshold


_DEFAULT_EXCLUDE = {
    "_comment": "Edit to customize. dirs/files = exact match. exts = with dot. patterns = fnmatch.",
    "dirs": [
        ".git", ".github",
        "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
        ".tox", ".hypothesis", "htmlcov", "dist", "build",
        "node_modules", ".cache", ".next", ".nuxt", ".vite", ".turbo",
        ".idea", ".vscode",
        "archived", "tests",
        ".tmp", "tmp", ".secrets",
    ],
    "files": [
        ".DS_Store", "._.DS_Store", "Thumbs.db",
        ".coverage", "coverage.xml",
        ".env", ".env.local",
        "__skill_meta__.json",
    ],
    "exts": [
        ".pyc", ".pyo", ".bak",
    ],
    "patterns": [
        "cloned_*.html",
        "AUDIT-*.md",
        "TEST-*.md",
        "*.json.md",
        "*.yaml.md",
        "*.yml.md",
        "__skill_meta__.*",
        ".tmp_backup_*",
        "*_backup_*",
    ],
}


def load_exclude_config(skill_root: Path) -> tuple:
    """Load exclude config from <skill_root>/config/exclude.json.
    Auto-creates default if missing. Returns (dirs, files, exts, patterns)."""
    cfg_path = skill_root / "config" / "exclude.json"

    if not cfg_path.is_file():
        try:
            cfg_path.parent.mkdir(parents=True, exist_ok=True)
            cfg_path.write_text(
                json.dumps(_DEFAULT_EXCLUDE, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            print(f"  INFO: auto-created {cfg_path}", file=sys.stderr)
        except Exception as e:
            print(f"  ERROR: cannot create {cfg_path}: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  ERROR: invalid JSON in {cfg_path}: {e}", file=sys.stderr)
        sys.exit(1)

    for field in ("dirs", "files", "exts"):
        if not isinstance(cfg.get(field), list):
            print(f"  ERROR: {cfg_path}: field '{field}' must be a list",
                  file=sys.stderr)
            sys.exit(1)

    patterns = cfg.get("patterns", [])
    if not isinstance(patterns, list):
        patterns = []

    return set(cfg["dirs"]), set(cfg["files"]), set(cfg["exts"]), list(patterns)


def _should_exclude(rel_path: str, dirs, files, exts, patterns) -> bool:
    parts = rel_path.replace("\\", "/").split("/")
    for part in parts:
        if part in dirs:
            return True
        if part in files:
            return True
        if part.startswith("._"):
            return True
    ext = os.path.splitext(rel_path)[1].lower()
    if ext in exts:
        return True
    fname = os.path.basename(rel_path)
    for pat in patterns:
        if fnmatch.fnmatch(fname, pat) or fnmatch.fnmatch(rel_path.replace("\\", "/"), pat):
            return True
    return False


def package_skill(slug: str, skill_dir: str, out_dir: str,
                  skill_root_for_config: Optional[Path] = None) -> dict:
    """
    Pack skill_dir into <out_dir>/<slug>.tar.gz.
    Returns {ok, path, file_count, files} or {ok: False, skipped, oversize_files, error}.
    """
    skill_dir = os.path.abspath(skill_dir)
    out_dir = os.path.abspath(out_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{slug}.tar.gz")

    cfg_root = Path(skill_root_for_config) if skill_root_for_config else Path(skill_dir)
    EXCLUDE_DIRS, EXCLUDE_FILES, EXCLUDE_EXTS, EXCLUDE_PATTERNS = \
        load_exclude_config(cfg_root)

    try:
        oversize_files = []
        pending = []

        for root, dirs, files in os.walk(skill_dir):
            dirs[:] = sorted(
                d for d in dirs
                if d not in EXCLUDE_DIRS and not d.startswith("._")
            )
            for fname in sorted(files):
                abs_path = os.path.join(root, fname)
                rel_from_skill = os.path.relpath(abs_path, skill_dir)
                if _should_exclude(rel_from_skill, EXCLUDE_DIRS,
                                   EXCLUDE_FILES, EXCLUDE_EXTS, EXCLUDE_PATTERNS):
                    continue
                rel_from_parent = os.path.relpath(
                    abs_path, os.path.dirname(skill_dir)
                ).replace("\\", "/")
                file_size = os.path.getsize(abs_path)
                if file_size > MAX_PACKAGE_SIZE_BYTES:
                    oversize_files.append({
                        "path":      rel_from_skill.replace("\\", "/"),
                        "size_mb":   round(file_size / 1024 / 1024, 2),
                        "size_bytes": file_size,
                    })
                pending.append((abs_path, rel_from_parent))

        if oversize_files:
            return {
                "ok": False,
                "skipped": True,
                "error": (
                    f"{len(oversize_files)} file(s) exceed single-file size limit "
                    f"{MAX_PACKAGE_SIZE_BYTES // 1024 // 1024} MB"
                ),
                "oversize_files": oversize_files,
            }

        with tarfile.open(out_path, "w:gz") as tar:
            for abs_path, arcname in pending:
                tar.add(abs_path, arcname=arcname)

        with tarfile.open(out_path, "r:gz") as tar:
            file_names = [m.name for m in tar.getmembers() if m.isfile()]

        return {
            "ok": True,
            "path": out_path,
            "file_count": len(file_names),
            "files": file_names,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


def build_multipart_from_tarball(fields: dict, tar_path: str, slug: str) -> tuple:
    """
    Build a multipart/form-data body from a tarball. The tarball is expected to
    have entries prefixed with "<slug>/" (which we strip before sending).

    Returns (body_bytes, content_type, file_count)
    """
    boundary = "----WebKitFormBoundarySkillReleasePlus"
    parts = []

    for key, value in fields.items():
        parts.append((
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="{key}"\r\n\r\n'
            f'{value}\r\n'
        ).encode())

    prefix = slug + "/"
    file_count = 0
    with tarfile.open(tar_path, "r:gz") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            rel_path = member.name
            if rel_path.startswith(prefix):
                rel_path = rel_path[len(prefix):]
            if not rel_path:
                continue
            f = tar.extractfile(member)
            if f is None:
                continue
            file_data = f.read()
            header = (
                f'--{boundary}\r\n'
                f'Content-Disposition: form-data; name="files"; '
                f'filename="{rel_path.replace(os.sep, "/")}"\r\n'
                f'Content-Type: application/octet-stream\r\n\r\n'
            ).encode()
            parts.append(header + file_data + b"\r\n")
            file_count += 1

    body = b"".join(parts) + f"--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}", file_count


def try_sign_skill(skill_dir: str, sign_script: Optional[str] = None,
                   optional: bool = True) -> dict:
    """
    Try to sign the skill using skill-sign. Returns:
      {ok: True, hash, signed_at, signed_by, skipped: False} on success
      {ok: True, skipped: True, reason} when sign.py missing AND optional=True
      {ok: False, error} on real failure
    """
    if sign_script is None:
        # Try common locations (order matters; env var wins)
        env_workspace = os.environ.get("OPENCLAW_WORKSPACE", "")
        candidates = [
            os.environ.get("SRP_SIGN_SCRIPT", ""),  # explicit override
            (os.path.join(env_workspace, "skills", "skill-sign", "scripts", "sign.py")
             if env_workspace else ""),
            shutil.which("sign.py") or "",
            # OpenClaw default install location (fallback for OpenClaw users)
            os.path.expanduser("~/.openclaw/workspace/skills/skill-sign/scripts/sign.py"),
            os.path.expanduser("~/.config/openclaw/skills/skill-sign/scripts/sign.py"),
        ]
        for c in candidates:
            if c and os.path.isfile(c):
                sign_script = c
                break

    if not sign_script or not os.path.isfile(sign_script):
        if optional:
            return {
                "ok": True, "skipped": True,
                "reason": "skill-sign not installed; package will be unsigned",
            }
        return {"ok": False, "error": "skill-sign not installed"}

    try:
        proc = subprocess.run(
            [sys.executable, sign_script, skill_dir],
            capture_output=True, text=True, timeout=60,
        )
        if proc.returncode != 0:
            return {"ok": False, "error": proc.stderr.strip() or proc.stdout.strip()}

        key_path = os.path.join(skill_dir, "sign.key")
        if os.path.isfile(key_path):
            with open(key_path) as f:
                key_data = json.load(f)
            return {
                "ok": True, "skipped": False,
                "hash": key_data.get("content_hash", ""),
                "signed_at": key_data.get("signed_at", ""),
                "signed_by": key_data.get("signed_by", ""),
            }
        return {"ok": True, "skipped": False, "hash": "", "signed_at": ""}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": "skill-sign timeout (60s)"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


__all__ = [
    "MAX_PACKAGE_SIZE_BYTES",
    "load_exclude_config",
    "package_skill",
    "build_multipart_from_tarball",
    "try_sign_skill",
]
