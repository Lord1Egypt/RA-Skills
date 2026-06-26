#!/usr/bin/env python3
"""sn-work-record 运行时引导：优先切换到依赖完整的 Python 解释器。"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from typing import Iterable

ENV_GUARD = "SN_WORK_RECORD_RUNTIME_BOOTSTRAPPED"
ENV_PREFERRED = "SN_WORK_RECORD_PYTHON"
DEFAULT_VENV_NAMES = ["sn_work_record_env", "oa_worktime_env", "ddddocr_env", ".venv", "venv"]


def _unique_existing(paths: Iterable[str | None]) -> list[str]:
    result: list[str] = []
    seen = set()
    for path in paths:
        if not path:
            continue
        real = os.path.realpath(os.path.expanduser(path))
        if real in seen or not os.path.exists(real):
            continue
        seen.add(real)
        result.append(real)
    return result


def _build_candidates(preferred_python: str | None = None) -> list[str]:
    workspace = os.path.expanduser("~/.openclaw/workspace")
    env_python = os.environ.get(ENV_PREFERRED)
    named_venvs = [os.path.join(workspace, name, "bin", "python") for name in DEFAULT_VENV_NAMES]
    fallback_candidates = [env_python, preferred_python, sys.executable, shutil.which("python3"), shutil.which("python")]
    return _unique_existing([env_python, preferred_python, *named_venvs, *fallback_candidates])


def _has_modules(python_executable: str, modules: list[str]) -> bool:
    code = (
        "import importlib.util, sys; "
        "mods = sys.argv[1:]; "
        "missing = [m for m in mods if importlib.util.find_spec(m) is None]; "
        "raise SystemExit(0 if not missing else 1)"
    )
    try:
        proc = subprocess.run(
            [python_executable, "-c", code, *modules],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=5,
            check=False,
        )
        return proc.returncode == 0
    except Exception:
        return False


def ensure_runtime(required_modules: list[str], preferred_python: str | None = None) -> None:
    """确保当前脚本运行在依赖完整的解释器中。"""
    if os.environ.get(ENV_GUARD) == "1":
        return

    current = os.path.realpath(sys.executable)
    candidates = _build_candidates(preferred_python)

    if _has_modules(current, required_modules):
        return

    for candidate in candidates:
        if os.path.realpath(candidate) == current:
            continue
        if _has_modules(candidate, required_modules):
            new_env = os.environ.copy()
            new_env[ENV_GUARD] = "1"
            os.execve(candidate, [candidate, *sys.argv], new_env)

    missing = ", ".join(required_modules)
    raise RuntimeError(
        "找不到可用的 Python 解释器来运行 sn-work-record；"
        f"需要依赖: {missing}；已检查: {', '.join(candidates) or '无'}；"
        f"可通过环境变量 {ENV_PREFERRED} 指定解释器路径"
    )
