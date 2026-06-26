#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from device_memory import find_preferred_connected_device


def venv_python(repo_dir: Path) -> Path:
    if os.name == 'nt':
        return repo_dir / '.venv' / 'Scripts' / 'python.exe'
    return repo_dir / '.venv' / 'bin' / 'python'


def main() -> int:
    repo_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / 'Open-AutoGLM'
    task = sys.argv[2] if len(sys.argv) > 2 else ''

    if not task:
        print('[error] missing task string')
        print('Usage: run_phone_task.py <repo_dir> <task>')
        return 1

    if not (repo_dir / '.venv').exists():
        print(f'[error] missing .venv: {repo_dir / ".venv"}')
        print('Create and install the repo-local virtual environment first.')
        return 1

    base_url = os.environ.get('MODEL_BASE_URL', '')
    model_name = os.environ.get('MODEL_NAME', '')
    api_key = os.environ.get('MODEL_API_KEY', '')
    if not base_url or not model_name or not api_key:
        print('[error] missing required model environment variables')
        print('Required: MODEL_BASE_URL, MODEL_NAME, MODEL_API_KEY')
        return 1

    main_py = repo_dir / 'main.py'
    if not main_py.exists():
        print(f'[error] main.py not found in repo dir: {repo_dir}')
        return 1

    py = venv_python(repo_dir)
    if not py.exists():
        print(f'[error] venv python not found: {py}')
        return 1

    preferred_device = os.environ.get('PHONE_DEVICE_ID') or find_preferred_connected_device()

    print('[run] executing phone task from repo-local .venv')
    if preferred_device:
        print(f'[device-select] using preferred device: {preferred_device}')

    cmd = [str(py), str(main_py), '--base-url', base_url, '--model', model_name, '--apikey', api_key]
    if preferred_device:
        cmd.extend(['--device-id', preferred_device])
    cmd.append(task)
    return subprocess.call(cmd, cwd=str(repo_dir), env=os.environ.copy())


if __name__ == '__main__':
    raise SystemExit(main())
