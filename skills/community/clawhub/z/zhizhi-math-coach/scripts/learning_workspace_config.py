#!/usr/bin/env python3
"""Shared config helpers for zhizhi-math-coach personal learning workspaces."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


CONFIG_REL_PATH = Path(".zhizhi-math-coach") / "config.json"
DEFAULT_SYNC_SCOPE = [
    ".zhizhi-math-coach/config.json",
    ".github/workflows/pages.yml",
    "README.md",
    "curriculum",
    "knowledge-points",
    "memory",
    "mistakes",
    "records",
    "weak-points",
    "worksheets",
    "site",
]
SENSITIVE_SYNC_SCOPE = {
    "curriculum",
    "knowledge-points",
    "memory",
    "mistakes",
    "records",
    "weak-points",
    "worksheets",
}
DEFAULT_AUTOMATION_TASKS = [
    {
        "name": "Zhizhi daily math review reminder",
        "kind": "daily_review",
        "enabled": True,
        "cron": "30 20 * * *",
        "session": "isolated",
    },
    {
        "name": "Zhizhi weekly math review",
        "kind": "weekly_review",
        "enabled": True,
        "cron": "0 20 * * 0",
        "session": "isolated",
    },
]


def run_git(args: list[str], workspace: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(workspace),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def parse_remote_url(url: str) -> tuple[str, str] | None:
    patterns = [
        r"^git@github\.com:([^/]+)/(.+?)(?:\.git)?$",
        r"^git@([^:]+):([^/]+)/(.+?)(?:\.git)?$",
        r"^https://github\.com/([^/]+)/(.+?)(?:\.git)?$",
    ]
    for pattern in patterns:
        match = re.match(pattern, url.strip())
        if not match:
            continue
        groups = match.groups()
        if len(groups) == 2:
            return groups[0], groups[1]
        return groups[1], groups[2]
    return None


def current_branch(workspace: Path, fallback: str = "main") -> str:
    if not workspace.exists():
        return fallback
    result = run_git(["branch", "--show-current"], workspace)
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return fallback


def infer_owner_repo(workspace: Path, remote: str = "origin") -> tuple[str, str] | None:
    if not workspace.exists():
        return None
    result = run_git(["remote", "get-url", remote], workspace)
    if result.returncode != 0:
        return None
    return parse_remote_url(result.stdout.strip())


def default_base_url(owner: str | None, repo: str | None) -> str:
    if not owner or not repo:
        return ""
    return f"https://{owner}.github.io/{repo}"


def config_path(workspace: Path) -> Path:
    return workspace.resolve() / CONFIG_REL_PATH


def default_config(
    workspace: Path,
    *,
    student_name: str = "孩子",
    remote: str = "origin",
    branch: str | None = None,
    owner: str | None = None,
    repo: str | None = None,
    timezone: str = "Asia/Shanghai",
) -> dict[str, Any]:
    inferred = infer_owner_repo(workspace, remote)
    owner = owner or (inferred[0] if inferred else "")
    repo = repo or (inferred[1] if inferred else workspace.resolve().name)
    branch = branch or current_branch(workspace)
    return {
        "version": 1,
        "workspace_role": "personal-learning-data",
        "student": {
            "display_name": student_name,
        },
        "github": {
            "owner": owner,
            "repo": repo,
        },
        "git_sync": {
            "enabled": False,
            "remote": remote,
            "branch": branch,
            "auto_pull_before_task": False,
            "auto_commit_after_task": False,
            "auto_push_after_task": False,
            "defer_push_after_grading": False,
            "sync_full_learning_data": False,
            "public_repository_accepted": False,
            "commit_scope": DEFAULT_SYNC_SCOPE,
        },
        "pages": {
            "enabled": False,
            "source": "github-actions",
            "auto_publish_worksheets": False,
            "base_url": default_base_url(owner, repo),
        },
        "automation": {
            "enabled": False,
            "scheduler": "openclaw-cron",
            "auto_register_when_supported": False,
            "timezone": timezone,
            "allow_record_writes": False,
            "allow_auto_worksheet_generation": False,
            "tasks": DEFAULT_AUTOMATION_TASKS,
            "registered_jobs": [],
        },
    }


def load_config(workspace: Path) -> dict[str, Any] | None:
    path = config_path(workspace)
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_config(workspace: Path, config: dict[str, Any]) -> Path:
    path = config_path(workspace)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def deep_update(target: dict[str, Any], patch: dict[str, Any]) -> dict[str, Any]:
    for key, value in patch.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            deep_update(target[key], value)
        else:
            target[key] = value
    return target


def ensure_config(workspace: Path, **kwargs: Any) -> dict[str, Any]:
    config = load_config(workspace)
    if config is None:
        config = default_config(workspace, **kwargs)
        write_config(workspace, config)
    return config


def update_config(workspace: Path, patch: dict[str, Any], **default_kwargs: Any) -> dict[str, Any]:
    config = load_config(workspace) or default_config(workspace, **default_kwargs)
    deep_update(config, patch)
    write_config(workspace, config)
    return config


def config_enabled(config: dict[str, Any] | None, section: str, key: str = "enabled") -> bool:
    if not config:
        return False
    value = config.get(section, {})
    return isinstance(value, dict) and bool(value.get(key))


def pages_base_url(config: dict[str, Any] | None) -> str:
    if not config:
        return ""
    pages = config.get("pages", {})
    if not isinstance(pages, dict):
        return ""
    return str(pages.get("base_url") or "").rstrip("/")


def configured_remote(config: dict[str, Any] | None, fallback: str = "origin") -> str:
    if not config:
        return fallback
    git_sync = config.get("git_sync", {})
    if not isinstance(git_sync, dict):
        return fallback
    return str(git_sync.get("remote") or fallback)


def configured_branch(config: dict[str, Any] | None, workspace: Path) -> str:
    if config:
        git_sync = config.get("git_sync", {})
        if isinstance(git_sync, dict) and git_sync.get("branch"):
            return str(git_sync["branch"])
    return current_branch(workspace)


def scope_has_sensitive_paths(scope: list[str]) -> bool:
    return any(path.split("/", 1)[0] in SENSITIVE_SYNC_SCOPE for path in scope)
