#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Environment diagnostics for WeChat Article Assistant."""

from __future__ import annotations

import ast
import importlib
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from config import get_paths
from utils import success

REQUIRED_PYTHON_PACKAGES = [
    {"import_name": "bs4", "package_name": "beautifulsoup4"},
    {"import_name": "requests", "package_name": "requests"},
    {"import_name": "markdownify", "package_name": "markdownify"},
]

REQUIRED_SCRIPT_FILES = [
    "wechat_article_assistant.py",
    "cli.py",
    "login_service.py",
    "article_service.py",
    "sync_service.py",
    "openclaw_messaging.py",
    "run_sync_all.sh",
]


def _check_python_commands() -> dict[str, Any]:
    results: dict[str, Any] = {}
    for cmd in ["python", "python3"]:
        path = shutil.which(cmd)
        entry: dict[str, Any] = {
            "found": bool(path),
            "path": path or "",
        }
        if path:
            proc = subprocess.run([cmd, "--version"], capture_output=True, text=True, check=False)
            entry["ok"] = proc.returncode == 0
            entry["version"] = (proc.stdout or proc.stderr).strip()
        else:
            entry["ok"] = False
            entry["version"] = ""
        results[cmd] = entry
    return results


def _pip_show_version(package_name: str) -> str:
    proc = subprocess.run(
        [sys.executable, "-m", "pip", "show", package_name],
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        return ""
    for line in proc.stdout.splitlines():
        if line.lower().startswith("version:"):
            return line.split(":", 1)[1].strip()
    return ""


def _scan_imported_third_party_modules() -> list[str]:
    base = Path(__file__).resolve().parent
    stdlib = set(sys.stdlib_module_names)
    local = {p.stem for p in base.glob('*.py')}
    third: set[str] = set()
    for path in base.glob('*.py'):
        tree = ast.parse(path.read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for item in node.names:
                    root = item.name.split('.')[0]
                    if root not in stdlib and root not in local and root != '__future__':
                        third.add(root)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root = node.module.split('.')[0]
                    if root not in stdlib and root not in local and root != '__future__':
                        third.add(root)
    return sorted(third)


def _check_python_packages() -> list[dict[str, Any]]:
    declared = {item["import_name"]: item["package_name"] for item in REQUIRED_PYTHON_PACKAGES}
    scanned = _scan_imported_third_party_modules()
    merged_imports = sorted(set(declared.keys()) | set(scanned))
    rows: list[dict[str, Any]] = []
    for import_name in merged_imports:
        package_name = declared.get(import_name, import_name)
        try:
            module = importlib.import_module(import_name)
            version = getattr(module, "__version__", "") or _pip_show_version(package_name)
            rows.append(
                {
                    "import_name": import_name,
                    "package_name": package_name,
                    "installed": True,
                    "version": version,
                }
            )
        except Exception as exc:
            rows.append(
                {
                    "import_name": import_name,
                    "package_name": package_name,
                    "installed": False,
                    "version": "",
                    "error": str(exc),
                }
            )
    return rows


def _check_script_files() -> list[dict[str, Any]]:
    base = Path(__file__).resolve().parent
    rows: list[dict[str, Any]] = []
    for name in REQUIRED_SCRIPT_FILES:
        path = base / name
        rows.append(
            {
                "name": name,
                "path": str(path),
                "exists": path.exists(),
            }
        )
    return rows


def _check_openclaw() -> dict[str, Any]:
    path = shutil.which("openclaw")
    data: dict[str, Any] = {
        "found": bool(path),
        "path": path or "",
    }
    if path:
        proc = subprocess.run(["openclaw", "--help"], capture_output=True, text=True, check=False)
        data["ok"] = proc.returncode == 0
    else:
        data["ok"] = False
    return data


def _check_paths() -> dict[str, Any]:
    paths = get_paths()
    checks = {}

    ensure_targets = ["root", "data_dir", "downloads_dir", "images_dir", "articles_dir", "qrcodes_dir", "logs_dir"]
    for key in ensure_targets:
        path = getattr(paths, key)
        created = False
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            created = True
        checks[key] = {
            "path": str(path),
            "exists": path.exists(),
            "created": created,
            "writable_parent": path.parent.exists() and path.parent.is_dir(),
        }

    db_parent_created = False
    if not paths.db_path.parent.exists():
        paths.db_path.parent.mkdir(parents=True, exist_ok=True)
        db_parent_created = True

    db_created = False
    if not paths.db_path.exists():
        paths.db_path.touch()
        db_created = True

    checks["db_path"] = {
        "path": str(paths.db_path),
        "exists": paths.db_path.exists(),
        "created": db_created,
        "parent_created": db_parent_created,
        "writable_parent": paths.db_path.parent.exists() and paths.db_path.parent.is_dir(),
    }
    return checks


def env_check() -> dict[str, Any]:
    python_commands = _check_python_commands()
    packages = _check_python_packages()
    scripts = _check_script_files()
    openclaw_cmd = _check_openclaw()
    paths = _check_paths()

    issues: list[str] = []
    if not any(item.get("ok") for item in python_commands.values()):
        issues.append("python/python3 均不可用")
    missing_packages = [item["name"] for item in packages if not item.get("installed")]
    if missing_packages:
        issues.append(f"缺少 Python 依赖: {', '.join(missing_packages)}")
    missing_scripts = [item["name"] for item in scripts if not item.get("exists")]
    if missing_scripts:
        issues.append(f"缺少脚本文件: {', '.join(missing_scripts)}")
    if not openclaw_cmd.get("found"):
        issues.append("openclaw 命令不可用")

    return success(
        {
            "ok": len(issues) == 0,
            "issues": issues,
            "python_commands": python_commands,
            "python_packages": packages,
            "script_files": scripts,
            "openclaw": openclaw_cmd,
            "paths": paths,
            "platform": sys.platform,
            "python_runtime": sys.version,
        },
        "Skill 环境检查完成",
    )
