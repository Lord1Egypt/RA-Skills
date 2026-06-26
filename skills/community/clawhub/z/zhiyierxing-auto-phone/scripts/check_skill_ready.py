#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from python_runtime import venv_python

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from device_memory import find_preferred_connected_device


def venv_has_runtime_deps(repo_dir: Path) -> bool:
    py = venv_python(repo_dir)
    if not py.exists():
        return False
    try:
        out = subprocess.run([str(py), '-c', 'import openai, requests; print("OK")'], capture_output=True, text=True, timeout=20)
        return out.returncode == 0
    except Exception:
        return False


def main() -> int:
    repo_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / 'Open-AutoGLM'
    device_type = sys.argv[2] if len(sys.argv) > 2 else 'android'

    missing = False
    missing_repo = False
    missing_venv = False
    missing_env = False
    missing_device_tool = False
    missing_deps = False

    print('[step] checking whether the skill can run your phone task now')

    print('[check] repo')
    if (repo_dir / '.git').exists():
        print(f'[ok] code is already deployed: {repo_dir}')
    else:
        print(f'[missing] code is not deployed yet: {repo_dir}')
        print('[next] the repo needs to be cloned or updated first')
        missing = True
        missing_repo = True

    print('[check] python virtual environment')
    if (repo_dir / '.venv').exists():
        print(f'[ok] repo-local .venv already exists: {repo_dir / ".venv"}')
        if venv_has_runtime_deps(repo_dir):
            print('[ok] critical runtime dependencies are importable from .venv')
        else:
            print('[missing] .venv exists but critical runtime dependencies are not installed correctly')
            print('[next] reinstall dependencies into the repo-local .venv before running the phone task')
            missing = True
            missing_deps = True
    else:
        print(f'[missing] repo-local .venv is not ready yet: {repo_dir / ".venv"}')
        print('[next] create .venv and install dependencies into it before running the phone task')
        missing = True
        missing_venv = True

    print('[check] model environment variables')
    for var in ('MODEL_BASE_URL', 'MODEL_NAME', 'MODEL_API_KEY'):
        if os.environ.get(var):
            print(f'[ok] {var} is set')
        else:
            print(f'[missing] {var} is not set')
            missing = True
            missing_env = True

    if missing_env:
        print('[next] configure the missing model env vars before execution')
        print('[hint] required vars: MODEL_BASE_URL, MODEL_NAME, MODEL_API_KEY')

    print('[check] device connection tool')
    if device_type == 'android':
        if shutil.which('adb'):
            print('[ok] adb is available for Android')
            preferred = find_preferred_connected_device()
            if preferred:
                print(f'[ok] preferred remembered device is currently reachable: {preferred}')
        else:
            print('[missing] adb is not installed or not on PATH')
            print('[next] install Android platform-tools first')
            missing = True
            missing_device_tool = True
    elif device_type == 'harmonyos':
        if shutil.which('hdc'):
            print('[ok] hdc is available for HarmonyOS')
        else:
            print('[missing] hdc is not installed or not on PATH')
            print('[next] install HarmonyOS SDK tools first')
            missing = True
            missing_device_tool = True
    elif device_type == 'iphone':
        print("[info] iPhone readiness must be confirmed through the repo's iOS setup guide")
    else:
        print(f'[error] unknown device type: {device_type}')
        return 1

    print(f'[info] host OS detected: {platform.system()}')

    if not missing:
        print('[ready] everything needed for task execution looks present')
        return 0

    print('[not-ready] the phone task cannot run yet')
    if missing_repo:
        print('[summary] first blocker: code has not been deployed')
    if missing_venv:
        print('[summary] python environment is not prepared yet')
    if missing_deps:
        print('[summary] python dependencies are incomplete inside .venv')
    if missing_env:
        print('[summary] model configuration is incomplete')
    if missing_device_tool:
        print('[summary] required device tooling is missing on this computer')
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
