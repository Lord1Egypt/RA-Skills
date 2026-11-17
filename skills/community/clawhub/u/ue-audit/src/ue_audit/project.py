"""Unreal project discovery and metadata."""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class ProjectError(RuntimeError):
    """Raised when a path is not a usable Unreal project."""


@dataclass
class ProjectInfo:
    root: Path
    uproject: Path
    name: str
    data: dict[str, Any] = field(default_factory=dict)
    engine_association: str = ""
    content_dir: Path = field(init=False)
    config_dir: Path = field(init=False)
    source_dir: Path = field(init=False)
    plugins_dir: Path = field(init=False)

    def __post_init__(self) -> None:
        self.content_dir = self.root / "Content"
        self.config_dir = self.root / "Config"
        self.source_dir = self.root / "Source"
        self.plugins_dir = self.root / "Plugins"

    @property
    def plugins(self) -> list[dict[str, Any]]:
        raw = self.data.get("Plugins") or []
        if not isinstance(raw, list):
            return []
        result: list[dict[str, Any]] = []
        for item in raw:
            if isinstance(item, dict):
                result.append(item)
        return result

    def local_plugin_path(self, name: str) -> Path:
        return self.plugins_dir / name / f"{name}.uplugin"

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "root": str(self.root),
            "uproject": str(self.uproject),
            "engine_association": self.engine_association,
            "content_dir": str(self.content_dir),
            "config_dir": str(self.config_dir),
            "source_dir": str(self.source_dir),
            "has_source": self.source_dir.is_dir(),
            "plugins": self.plugins,
        }


def find_project(path: str | Path) -> ProjectInfo:
    candidate = Path(path).expanduser().resolve()
    if candidate.is_file():
        if candidate.suffix.lower() != ".uproject":
            raise ProjectError(f"not a .uproject file: {candidate}")
        uproject = candidate
        root = candidate.parent
    elif candidate.is_dir():
        matches = sorted(candidate.glob("*.uproject"))
        if not matches:
            raise ProjectError(f"no .uproject found in {candidate}")
        if len(matches) > 1:
            names = ", ".join(item.name for item in matches)
            raise ProjectError(f"multiple .uproject files found in {candidate}: {names}")
        uproject = matches[0]
        root = candidate
    else:
        raise ProjectError(f"path does not exist: {candidate}")

    try:
        data = json.loads(uproject.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        raise ProjectError(f"cannot read {uproject}: {exc}") from exc
    if not isinstance(data, dict):
        raise ProjectError(f"{uproject} is not a JSON object")

    return ProjectInfo(
        root=root,
        uproject=uproject,
        name=uproject.stem,
        data=data,
        engine_association=str(data.get("EngineAssociation") or ""),
    )


def resolve_engine_version(
    project: ProjectInfo, engine_path: str | Path | None = None
) -> dict[str, Any]:
    if engine_path:
        engine_root = Path(engine_path).expanduser().resolve()
        if engine_root.name.lower() == "engine":
            build_version = engine_root / "Build" / "Build.version"
        else:
            build_version = engine_root / "Engine" / "Build" / "Build.version"
        if build_version.is_file():
            try:
                data = json.loads(build_version.read_text(encoding="utf-8-sig"))
            except (OSError, ValueError):
                data = {}
            major = data.get("MajorVersion")
            minor = data.get("MinorVersion")
            patch = data.get("PatchVersion")
            if major is not None and minor is not None:
                display = f"{major}.{minor}"
                if patch is not None:
                    display += f".{patch}"
                return {
                    "source": "explicit_engine_path",
                    "engine_root": str(engine_root),
                    "engine_version": display,
                    "major": major,
                    "minor": minor,
                    "patch": patch,
                    "build_id": data.get("BuildId", ""),
                    "build_version_file": str(build_version),
                }
        return {
            "source": "explicit_engine_path",
            "engine_root": str(engine_root),
            "engine_version": "",
            "error": f"Build.version not found under {engine_root}",
        }

    association = project.engine_association
    match = re.match(r"^(\d+)\.(\d+)", association or "")
    if match:
        return {
            "source": "uproject_engine_association",
            "engine_root": "",
            "engine_version": f"{match.group(1)}.{match.group(2)}",
            "major": int(match.group(1)),
            "minor": int(match.group(2)),
            "patch": None,
            "build_id": "",
        }
    return {
        "source": "uproject_engine_association",
        "engine_root": "",
        "engine_version": "",
        "engine_association": association,
        "warning": "EngineAssociation is empty or not a version string",
    }


def _run_git(root: Path, args: list[str], timeout: float = 8.0) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None


def git_info(root: Path) -> dict[str, Any]:
    """Return basic Git metadata without failing when Git is unavailable."""
    if not (root / ".git").exists():
        return {"available": False, "reason": "not_a_git_repository"}

    top = _run_git(root, ["rev-parse", "--show-toplevel"])
    if top is None or top.returncode != 0:
        return {"available": False, "reason": "git_not_available_or_not_a_repository"}

    head = _run_git(root, ["rev-parse", "HEAD"])
    branch = _run_git(root, ["rev-parse", "--abbrev-ref", "HEAD"])
    status = _run_git(root, ["status", "--porcelain=v1", "-z"])
    entries: list[dict[str, str]] = []
    if status is not None and status.returncode == 0:
        raw = status.stdout or ""
        parts = raw.split("\0")
        index = 0
        while index < len(parts):
            item = parts[index]
            index += 1
            if not item:
                continue
            code = item[:2]
            path = item[3:] if len(item) > 3 else ""
            entries.append({"code": code, "path": path, "kind": _git_kind(code)})
            if "R" in code or "C" in code:
                index += 1

    conflicts = [item for item in entries if item["kind"] == "conflict"]
    untracked = [item for item in entries if item["kind"] == "untracked"]
    modified = [item for item in entries if item["kind"] == "modified"]

    return {
        "available": True,
        "root": (top.stdout or "").strip(),
        "head": (head.stdout or "").strip() if head and head.returncode == 0 else "",
        "branch": (branch.stdout or "").strip() if branch and branch.returncode == 0 else "",
        "dirty": len(modified) > 0,
        "entry_count": len(entries),
        "modified_count": len(modified),
        "untracked_count": len(untracked),
        "conflict_count": len(conflicts),
        "entries": entries[:200],
        "truncated": len(entries) > 200,
    }


def _git_kind(code: str) -> str:
    if code in {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}:
        return "conflict"
    if code == "??":
        return "untracked"
    return "modified"


def git_large_files(root: Path, threshold_bytes: int, limit: int = 200) -> list[dict[str, Any]]:
    """Return tracked files larger than threshold_bytes."""
    tracked = _run_git(root, ["ls-files", "-z"])
    if tracked is None or tracked.returncode != 0:
        return []
    results: list[dict[str, Any]] = []
    for relative in (tracked.stdout or "").split("\0"):
        if not relative:
            continue
        path = root / relative
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > threshold_bytes:
            results.append({"path": relative.replace("\\", "/"), "size": size})
            if len(results) >= limit:
                break
    results.sort(key=lambda item: item["size"], reverse=True)
    return results
