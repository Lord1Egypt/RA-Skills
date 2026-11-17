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
import hashlib
import json
import os
import re
import secrets
import shutil
import subprocess
import sys
import tarfile
import zipfile
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

# ── 安全网排除（硬编码，叠加在用户 exclude.json 之上，用户配置不可放行）──────
# 目标：密钥/凭证/私钥类文件绝不进入发布包。用户 exclude.json 只能"额外排除"，
# 无法把安全网内的文件加回包里。命中安全网的文件会在打包结果中如实报告，
# 告知用户哪些内容未随包发布。
_SAFETY_NET = {
    "files": {
        "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519",
        ".netrc", ".npmrc", ".pypirc",
        ".git-credentials", ".gitcredentials",
        "credentials.json", "secrets.json",
        "service-account.json", "htpasswd", ".htpasswd", ".pgpass",
    },
    "exts": {
        ".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".ppk",
    },
    "patterns": [
        "id_rsa*", "id_dsa*", "id_ecdsa*", "id_ed25519*",
        "service-account*.json",
        ".env.*",           # .env.staging / .env.production 等（.env/.env.local 在用户层）
        "*credentials*.json",
        "*secret*.json",
    ],
}


def _matches_safety_net(rel_path: str) -> bool:
    """是否命中安全网排除（与用户 exclude 规则独立叠加）。"""
    parts = rel_path.replace("\\", "/").split("/")
    for part in parts:
        if part in _SAFETY_NET["files"]:
            return True
    ext = os.path.splitext(rel_path)[1].lower()
    if ext in _SAFETY_NET["exts"]:
        return True
    fname = os.path.basename(rel_path)
    for pat in _SAFETY_NET["patterns"]:
        if fnmatch.fnmatch(fname, pat) or fnmatch.fnmatch(rel_path.replace("\\", "/"), pat):
            return True
    return False


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
        sensitive_excluded = []   # 安全网拦截（未随包发布的敏感内容，如实报告）
        symlinks_skipped = []     # 符号链接（不跟随，防链接目标内容混入包）

        for root, dirs, files in os.walk(skill_dir):
            dirs[:] = sorted(
                d for d in dirs
                if d not in EXCLUDE_DIRS and not d.startswith("._")
            )
            for fname in sorted(files):
                abs_path = os.path.join(root, fname)
                rel_from_skill = os.path.relpath(abs_path, skill_dir)
                if fname == _SIGN_KEY_FILENAME:
                    # v1.1.1: sign.key 不再随包发布（文件名含 .key 易被 hub 侧
                    # 扫描器误判为私钥泄漏），记录到报告让用户知情
                    sensitive_excluded.append(
                        rel_from_skill.replace("\\", "/") + "  (签名件，v1.1.1 起不随包发布)"
                    )
                    continue
                if os.path.islink(abs_path):
                    symlinks_skipped.append(rel_from_skill.replace("\\", "/"))
                    continue
                if _should_exclude(rel_from_skill, EXCLUDE_DIRS,
                                   EXCLUDE_FILES, EXCLUDE_EXTS, EXCLUDE_PATTERNS):
                    continue
                if _matches_safety_net(rel_from_skill):
                    sensitive_excluded.append(rel_from_skill.replace("\\", "/"))
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
            "sensitive_excluded": sensitive_excluded,
            "symlinks_skipped": symlinks_skipped,
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


# ── Sign mode detection & clean staging (ported from internal v1.3.0+) ─────

_SIGN_KEY_FILENAME = "sign.key"   # per-skill signature artifact (ships in package)
_PRIVATE_KEY_FILE = ".sign-key"   # signer identity key (workspace root, never packaged)


def find_sign_workspace() -> str:
    """Locate the workspace that holds the signing private key.

    Same rule as skill-sign's find_workspace: OPENCLAW_WORKSPACE env var wins,
    else ~/.openclaw/workspace.
    """
    ws = os.environ.get("OPENCLAW_WORKSPACE")
    if ws and os.path.isdir(ws):
        return ws
    return os.path.expanduser("~/.openclaw/workspace")


def detect_private_key() -> tuple:
    """Detect whether the user already has a signing private key.

    Returns (status, key_path):
      "ok"      — key exists with a non-empty "key" field (→ auto-sign, old users unchanged)
      "missing" — no key file (→ auto-unsigned, zero setup for new users)
      "corrupt" — file exists but unparseable (→ hard error, never silent downgrade)
    """
    key_path = os.path.join(find_sign_workspace(), _PRIVATE_KEY_FILE)
    if not os.path.isfile(key_path):
        return "missing", key_path
    try:
        with open(key_path, encoding="utf-8") as f:
            data = json.load(f)
        if (isinstance(data, dict)
                and isinstance(data.get("key"), str)
                and data["key"].strip()):
            return "ok", key_path
    except Exception:
        pass
    return "corrupt", key_path


def init_private_key() -> dict:
    """One-shot generation of the signing private key.

    Returns {ok, path, existed, error}. Refuses to overwrite an existing key:
    resetting it would break identity checks of historical signatures.
    """
    status, key_path = detect_private_key()
    if status == "ok":
        return {"ok": True, "path": key_path, "existed": True, "error": ""}
    if status == "corrupt":
        return {"ok": False, "path": key_path, "existed": True,
                "error": "private key file exists but is unreadable"}
    try:
        priv = secrets.token_hex(32)
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        with open(key_path, "w", encoding="utf-8") as f:
            json.dump({"key": priv}, f)
        os.chmod(key_path, 0o600)
        return {"ok": True, "path": key_path, "existed": False, "error": ""}
    except Exception as e:
        return {"ok": False, "path": key_path, "existed": False, "error": str(e)}


def build_clean_stage(slug: str, skill_dir: str, stage_root: str,
                      keep_sign_key: bool = True,
                      skill_root_for_config: Optional[Path] = None) -> str:
    """Copy skill_dir into a clean staging dir under stage_root, exclude rules applied.

    Signing runs against this exact copy so sign.key's content_hash matches the
    shipped file set. Keeping two independent exclude rule sets (one for
    signing, one for packing) would eventually drift and make verify() report
    "Tampering detected" on the install side.

    keep_sign_key=False (unsigned mode) drops any legacy sign.key from the
    source dir: an old signature covers old content and would only trigger
    false tampering reports downstream. keep_sign_key=True (sign mode) keeps
    it so sign.py's "cannot overwrite someone else's signature" guard stays
    armed.
    """
    stage_skill = os.path.join(stage_root, slug)
    if os.path.exists(stage_skill):
        shutil.rmtree(stage_skill)

    cfg_root = Path(skill_root_for_config) if skill_root_for_config else Path(skill_dir)
    EXCLUDE_DIRS, EXCLUDE_FILES, EXCLUDE_EXTS, EXCLUDE_PATTERNS = \
        load_exclude_config(cfg_root)

    for root, dirs, files in os.walk(skill_dir):
        dirs[:] = sorted(
            d for d in dirs
            if d not in EXCLUDE_DIRS and not d.startswith("._")
        )
        for fname in sorted(files):
            if not keep_sign_key and fname == _SIGN_KEY_FILENAME:
                continue
            abs_path = os.path.join(root, fname)
            rel = os.path.relpath(abs_path, skill_dir)
            if _should_exclude(rel, EXCLUDE_DIRS, EXCLUDE_FILES,
                                EXCLUDE_EXTS, EXCLUDE_PATTERNS):
                continue
            if os.path.islink(abs_path):
                # 不跟随符号链接，防止把链接目标（可能在工作区外）的内容拷入 stage
                continue
            dst = os.path.join(stage_skill, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(abs_path, dst)
    return stage_skill


# ── Strict SKILL.md frontmatter version (for --package-only) ──────────────

_FM_VERSION_RE = re.compile(r"^(version:\s*)(\S+)\s*$", re.MULTILINE)


def _split_frontmatter(text: str) -> tuple:
    """Split frontmatter block from the rest. ("", text) when absent."""
    if not text.startswith("---"):
        return "", text
    end = text.find("\n---", 3)
    if end == -1:
        return "", text
    cut = text.find("\n", end + 1)
    if cut == -1:
        cut = len(text)
    else:
        cut += 1
    return text[:cut], text[cut:]


def read_skill_md_version(skill_dir: str) -> str:
    """Strictly read `version` from SKILL.md frontmatter. '' when undeclared.

    Only matches inside the frontmatter block so body text like "version: x"
    in prose never matches.
    """
    path = os.path.join(skill_dir, "SKILL.md")
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return ""
    fm, _ = _split_frontmatter(text)
    if not fm:
        return ""
    m = _FM_VERSION_RE.search(fm)
    return m.group(2).strip().strip("\"'") if m else ""


# ── Deterministic package-only ZIP (ported from internal v1.4.x) ───────────


def do_package_only(slug: str, skill_dir: str, out_dir: str,
                    expected_version: str,
                    skill_root_for_config: Optional[Path] = None,
                    tool_version: str = "") -> dict:
    """Build a deterministic unsigned ZIP: no credentials, no network, no source mutation.

    The caller owns version resolution; this only accepts an exact target
    version and refuses to package when SKILL.md does not declare it.
    Determinism: fixed timestamps (1980-01-01), fixed permission bits
    (755 for executables, else 644), entries sorted by path — so the same
    tree always yields the same sha256.
    """
    version_pattern = r"^\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?$"
    if not re.fullmatch(version_pattern, expected_version or ""):
        return {"ok": False, "code": "INVALID_EXPECTED_VERSION",
                "error": "--expected-version must be a valid semver string"}
    actual_version = read_skill_md_version(skill_dir)
    if actual_version != expected_version:
        return {"ok": False, "code": "VERSION_MISMATCH",
                "error": (f"SKILL.md version mismatch: expected={expected_version}, "
                          f"actual={actual_version or '<missing>'}"),
                "expectedVersion": expected_version,
                "actualVersion": actual_version}

    cfg_root = Path(skill_root_for_config) if skill_root_for_config else Path(skill_dir)
    EXCLUDE_DIRS, EXCLUDE_FILES, EXCLUDE_EXTS, EXCLUDE_PATTERNS = \
        load_exclude_config(cfg_root)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.abspath(os.path.join(out_dir, f"{slug}-{expected_version}.zip"))
    pending = []
    sensitive_excluded = []   # 安全网拦截报告（与 package_skill 同口径）
    try:
        for root, dirs, files in os.walk(skill_dir):
            for dirname in dirs:
                abs_dir = os.path.join(root, dirname)
                if os.path.islink(abs_dir):
                    return {"ok": False, "code": "UNSAFE_SYMLINK",
                            "error": "candidate skill must not contain symlinks: "
                                     + os.path.relpath(abs_dir, skill_dir)}
            dirs[:] = sorted(d for d in dirs
                             if d not in EXCLUDE_DIRS and not d.startswith("._"))
            for fname in sorted(files):
                abs_path = os.path.join(root, fname)
                rel_path = os.path.relpath(abs_path, skill_dir).replace("\\", "/")
                if os.path.islink(abs_path):
                    return {"ok": False, "code": "UNSAFE_SYMLINK",
                            "error": "candidate skill must not contain symlinks: "
                                     + rel_path}
                if fname == _SIGN_KEY_FILENAME:
                    sensitive_excluded.append(
                        rel_path + "  (签名件，v1.1.1 起不随包发布)")
                    continue
                if _should_exclude(rel_path, EXCLUDE_DIRS, EXCLUDE_FILES,
                                   EXCLUDE_EXTS, EXCLUDE_PATTERNS):
                    continue
                if _matches_safety_net(rel_path):
                    sensitive_excluded.append(rel_path)
                    continue
                size = os.path.getsize(abs_path)
                if size > MAX_PACKAGE_SIZE_BYTES:
                    return {"ok": False, "skipped": True, "code": "FILE_TOO_LARGE",
                            "error": (f"file {rel_path} exceeds single-file limit "
                                      f"{MAX_PACKAGE_SIZE_BYTES // 1024 // 1024} MB")}
                with open(abs_path, "rb") as stream:
                    body = stream.read()
                pending.append((rel_path, body, os.access(abs_path, os.X_OK)))
        if not pending or not any(path == "SKILL.md" for path, _, _ in pending):
            return {"ok": False, "code": "SKILL_MD_MISSING",
                    "error": "clean package is missing SKILL.md"}

        manifest = []
        with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for rel_path, body, executable in sorted(pending):
                info = zipfile.ZipInfo(rel_path, (1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (0o100755 if executable else 0o100644) << 16
                archive.writestr(info, body)
                manifest.append({"path": rel_path,
                                 "sha256": hashlib.sha256(body).hexdigest()})
        with open(out_path, "rb") as stream:
            package_sha256 = hashlib.sha256(stream.read()).hexdigest()
        return {"ok": True, "mode": "package-only", "slug": slug,
                "version": expected_version,
                "toolVersion": tool_version,
                "packagePath": out_path, "packageSha256": package_sha256,
                "fileCount": len(manifest), "files": manifest,
                "sensitive_excluded": sensitive_excluded}
    except Exception as exc:
        return {"ok": False, "code": "PACKAGE_FAILED", "error": str(exc)}


__all__ = [
    "MAX_PACKAGE_SIZE_BYTES",
    "load_exclude_config",
    "package_skill",
    "build_multipart_from_tarball",
    "try_sign_skill",
    "find_sign_workspace",
    "detect_private_key",
    "init_private_key",
    "build_clean_stage",
    "read_skill_md_version",
    "do_package_only",
]
