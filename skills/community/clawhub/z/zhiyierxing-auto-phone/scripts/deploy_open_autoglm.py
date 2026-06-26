#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from python_runtime import MIN_MAJOR, MIN_MINOR, install_python_if_possible, select_python, venv_python


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, env=os.environ.copy())


def venv_matches_selected(repo_dir: Path, selected_path: str) -> bool:
    py = venv_python(repo_dir)
    if not py.exists():
        return False
    try:
        out = subprocess.run([str(py), '-c', 'import sys; print(sys.executable)'], capture_output=True, text=True, timeout=10)
        existing = (out.stdout or '').strip()
        return existing == str(py) and py.exists()
    except Exception:
        return False


def main() -> int:
    device_type = sys.argv[1] if len(sys.argv) > 1 else 'android'
    model_mode = sys.argv[2] if len(sys.argv) > 2 else 'bigmodel'
    repo_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path.cwd() / 'Open-AutoGLM'
    root_dir = Path(__file__).resolve().parent.parent

    print('[1/6] host check')
    wants = ['git', 'python3']
    if device_type == 'android':
        wants.append('adb')
    elif device_type == 'harmonyos':
        wants.append('hdc')
    host_check = run([sys.executable, str(root_dir / 'scripts' / 'check_host_env.py'), *wants])
    if host_check.returncode != 0:
        print(f'[info] trying to self-install a suitable Python {MIN_MAJOR}.{MIN_MINOR}+ runtime when possible')
        if not install_python_if_possible():
            return host_check.returncode
        host_check = run([sys.executable, str(root_dir / 'scripts' / 'check_host_env.py'), *wants])
        if host_check.returncode != 0:
            return host_check.returncode

    print('\n[2/6] repo sync')
    clone_script = root_dir / 'scripts' / 'clone_or_update_open_autoglm.py'
    clone = run([sys.executable, str(clone_script), str(repo_dir)])
    if clone.returncode != 0:
        return clone.returncode

    print('\n[3/6] device readiness')
    if device_type == 'android':
        ready = run([sys.executable, str(root_dir / 'scripts' / 'check_android_ready.py')])
        if ready.returncode != 0:
            return ready.returncode
    elif device_type == 'harmonyos':
        ready = run([sys.executable, str(root_dir / 'scripts' / 'check_harmonyos_ready.py')])
        if ready.returncode != 0:
            return ready.returncode
    elif device_type == 'iphone':
        ready = run([sys.executable, str(root_dir / 'scripts' / 'check_iphone_ready.py')])
        if ready.returncode != 0:
            return ready.returncode
    else:
        print(f'[error] unknown device type: {device_type}')
        return 1

    print('\n[4/6] python venv + dependencies')
    repo_dir.mkdir(parents=True, exist_ok=True)
    selected_python = select_python()
    if not selected_python:
        print(f'[error] no suitable Python {MIN_MAJOR}.{MIN_MINOR}+ interpreter found even after install attempt')
        return 1
    selected_path, selected_ver, selected_cmd = selected_python
    print(f'[info] using Python {selected_ver[0]}.{selected_ver[1]}.{selected_ver[2]} via {selected_cmd} -> {selected_path}')
    venv_dir = repo_dir / '.venv'
    py = venv_python(repo_dir)
    recreate_venv = False
    if not venv_dir.exists():
        recreate_venv = True
    elif not venv_matches_selected(repo_dir, selected_path):
        print('[warn] existing .venv does not match the selected supported Python runtime; recreating it')
        recreate_venv = True

    if recreate_venv:
        if venv_dir.exists():
            shutil.rmtree(venv_dir)
        create_venv = run([selected_path, '-m', 'venv', str(venv_dir)], cwd=str(repo_dir))
        if create_venv.returncode != 0:
            return create_venv.returncode
        py = venv_python(repo_dir)
    upgrade_pip = run([str(py), '-m', 'pip', 'install', '--upgrade', 'pip'], cwd=str(repo_dir))
    if upgrade_pip.returncode != 0:
        return upgrade_pip.returncode
    install_req = run([str(py), '-m', 'pip', 'install', '-r', 'requirements.txt'], cwd=str(repo_dir))
    if install_req.returncode != 0:
        return install_req.returncode
    install_editable = run([str(py), '-m', 'pip', 'install', '-e', '.'], cwd=str(repo_dir))
    if install_editable.returncode != 0:
        return install_editable.returncode

    print('\n[5/6] model config')
    if model_mode == 'bigmodel':
        print('Use the configured env vars with model=autoglm-phone and base-url=https://open.bigmodel.cn/api/paas/v4')
    elif model_mode == 'third-party-openai-compatible':
        print('Use the configured env vars with your OpenAI-compatible base URL and model name')
    elif model_mode == 'self-hosted':
        print('Start your /v1 endpoint first, then run the task through the configured env vars')
    else:
        print(f'[error] unknown model mode: {model_mode}')
        return 1

    print('\n[6/6] next step')
    print(f'[info] host OS: {platform.system()}')
    print('[hint] after env vars are configured, run the end-to-end workflow with ensure_and_run_task.py')
    print(f'  {sys.executable} {root_dir / "scripts" / "ensure_and_run_task.py"} {device_type} {model_mode} {repo_dir} "<YOUR_NATURAL_LANGUAGE_TASK>"')

    print('[done] deployment path prepared')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
