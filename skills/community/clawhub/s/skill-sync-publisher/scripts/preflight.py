from __future__ import annotations

import hashlib
import os
import re
import subprocess
from pathlib import Path
from typing import Any


SECRET_NAME = re.compile(r"(^|/)(\.env($|\.)|.*(secret|credential|private[-_]?key).*)", re.I)
SECRET_CONTENT = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----|\b[A-Z0-9_]*(TOKEN|API[_-]?KEY|SECRET|PASSWORD)\s*=\s*['\"]?[A-Za-z0-9_\-]{12,}",
    re.I,
)


def _git(cwd: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        return ""
    return result.stdout.strip()


def source_key(skill_dir: Path, repo_root: Path) -> str:
    remote = _git(repo_root, "remote", "get-url", "origin") or str(repo_root)
    remote = re.sub(r"^git@github\.com:", "github.com/", remote)
    remote = re.sub(r"^https?://github\.com/", "github.com/", remote)
    remote = re.sub(r"\.git$", "", remote)
    return f"{remote}#{skill_dir.relative_to(repo_root).as_posix()}"


def _frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]
    end = text.find("\n---", 4)
    if end < 0:
        return {}, ["SKILL.md frontmatter is not closed"]
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"invalid frontmatter line: {line}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"\'')
    if not fields.get("name"):
        errors.append("frontmatter requires name")
    elif not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", fields["name"]):
        errors.append("frontmatter name must be lowercase hyphen-case")
    if not fields.get("description"):
        errors.append("frontmatter requires description")
    return fields, errors


def inspect(skill_dir: Path) -> dict[str, Any]:
    skill_dir = skill_dir.resolve()
    repo_root_text = _git(skill_dir, "rev-parse", "--show-toplevel")
    repo_root = Path(repo_root_text).resolve() if repo_root_text else skill_dir
    skill_file = skill_dir / "SKILL.md"
    errors: list[str] = []
    warnings: list[str] = []
    if not skill_file.is_file():
        errors.append("SKILL.md is missing")
        return {"skillDir": str(skill_dir), "repoRoot": str(repo_root), "errors": errors, "warnings": warnings}
    text = skill_file.read_text(encoding="utf-8")
    fields, errors = _frontmatter(text)
    files: list[str] = []
    blocked: list[str] = []
    digest = hashlib.sha256()
    for path in sorted(p for p in skill_dir.rglob("*") if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts and p.suffix != ".pyc"):
        rel = path.relative_to(skill_dir).as_posix()
        files.append(rel)
        digest.update(rel.encode() + b"\0")
        data = path.read_bytes()
        digest.update(data)
        if SECRET_NAME.search(rel):
            blocked.append(f"sensitive filename: {rel}")
        content_scan = data.decode("utf-8", errors="ignore")
        if path.suffix.lower() not in {".md", ".py", ".txt", ".yaml", ".yml"} and len(data) <= 2_000_000 and SECRET_CONTENT.search(content_scan):
            blocked.append(f"possible credential content: {rel}")
        if path.is_file() and os.access(path, os.X_OK) and not rel.startswith("scripts/"):
            warnings.append(f"executable outside scripts/: {rel}")
        if path.suffix.lower() not in {".md", ".py", ".txt", ".yaml", ".yml"} and (b"/Users/" in data or b"/home/" in data):
            warnings.append(f"absolute home path reference: {rel}")
    errors.extend(blocked)
    status = "blocked" if errors else "ready"
    status_lines = _git(repo_root, "status", "--short").splitlines()
    target_relative = skill_dir.relative_to(repo_root).as_posix()
    unrelated = []
    if target_relative != ".":
        target_prefix = target_relative.rstrip("/") + "/"
        for line in status_lines:
            changed = line[3:].strip() if len(line) >= 3 else line.strip()
            if changed and not (changed == target_relative or changed.startswith(target_prefix)):
                unrelated.append(changed)
    return {
        "skillDir": str(skill_dir),
        "repoRoot": str(repo_root),
        "sourceKey": source_key(skill_dir, repo_root),
        "name": fields.get("name"),
        "description": fields.get("description"),
        "files": files,
        "sourceHash": f"sha256:{digest.hexdigest()}",
        "gitBranch": _git(repo_root, "branch", "--show-current"),
        "gitRemote": _git(repo_root, "remote", "get-url", "origin"),
        "gitStatus": _git(repo_root, "status", "--short"),
        "unrelatedGitChanges": unrelated,
        "pluginManifest": (skill_dir / ".codex-plugin" / "plugin.json").is_file() or (repo_root / ".codex-plugin" / "plugin.json").is_file(),
        "status": status,
        "errors": errors,
        "warnings": warnings,
    }
