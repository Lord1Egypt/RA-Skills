#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def workspace_root() -> Path:
    explicit = os.getenv("SHERPAMIND_WORKSPACE_ROOT")
    if explicit:
        return Path(explicit).resolve()
    repo = repo_root().resolve()
    if repo.parent.name == "skills":
        return repo.parent.parent.resolve()
    return Path.cwd().resolve()


def venv_python() -> Path:
    return workspace_root() / ".SherpaMind" / "private" / "runtime" / "venv" / "bin" / "python"


def ensure_bootstrap() -> Path:
    python = venv_python()
    if python.exists():
        return python
    bootstrap = repo_root() / "scripts" / "bootstrap.py"
    subprocess.run([sys.executable, str(bootstrap)], check=True)
    return python


def main() -> int:
    python = ensure_bootstrap()
    env = os.environ.copy()
    env.setdefault("SHERPAMIND_WORKSPACE_ROOT", str(workspace_root()))
    env["PYTHONPATH"] = str(repo_root() / "src") + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    cmd = [str(python), "-m", "sherpamind.cli", *sys.argv[1:]]
    return subprocess.call(cmd, env=env, cwd=str(repo_root()))


if __name__ == "__main__":
    raise SystemExit(main())
