#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path


def venv_python(repo_dir: Path) -> Path:
    if os.name == 'nt':
        return repo_dir / '.venv' / 'Scripts' / 'python.exe'
    return repo_dir / '.venv' / 'bin' / 'python'


def run(cmd, cwd=None, check=False, capture=False):
    if capture:
        return subprocess.run(cmd, cwd=cwd, env=os.environ.copy(), check=check, capture_output=True, text=True)
    return subprocess.run(cmd, cwd=cwd, env=os.environ.copy(), check=check)


def classify_recheck(repo_dir: Path, device_type: str) -> str:
    missing_env = [var for var in ('MODEL_BASE_URL', 'MODEL_NAME', 'MODEL_API_KEY') if not os.environ.get(var)]
    if missing_env:
        print(f'[config-needed] missing model env vars: {", ".join(missing_env)}')
        print('[safe-to-retry] set the missing env vars, then rerun the workflow')
        return 'config'

    if device_type == 'android':
        adb = subprocess.run(['adb', 'devices'], capture_output=True, text=True, env=os.environ.copy())
        lines = [line.strip() for line in adb.stdout.splitlines()[1:] if line.strip()]
        authorized = [line.split()[0] for line in lines if len(line.split()) >= 2 and line.split()[1] == 'device']
        if not authorized:
            print('[phone-action-needed] no authorized Android device is currently available')
            print('[safe-to-retry] reconnect the phone, accept USB debugging authorization, then rerun the workflow')
            return 'phone'

    if not (repo_dir / '.git').exists() or not (repo_dir / '.venv').exists():
        print('[runtime-failed] local deployment is still incomplete after repair')
        print('[safe-to-retry] inspect the logs above, fix the remaining local issue, then rerun the workflow')
        return 'runtime'

    print('[runtime-failed] setup is still incomplete after repair, but the blocker could not be classified precisely')
    print('[safe-to-retry] inspect the logs above and rerun after fixing the proven blocker')
    return 'runtime'


def diagnose_task_result(output: str, exit_code: int) -> str:
    text = output or ''
    if exit_code == 0:
        print('[diagnosis] success')
        return 'success'
    if '[phone-action-needed]' in text or '[takeover-paused]' in text:
        print('[diagnosis] blocked on phone-side manual takeover')
        return 'phone-action-needed'
    if '[decision-needed]' in text:
        print('[diagnosis] blocked on missing user choice or intent detail')
        return 'decision-needed'
    if 'ADB Keyboard is not installed' in text or 'ADB Keyboard not found' in text:
        print('[diagnosis] text input path is blocked by missing ADB Keyboard')
        return 'adb-keyboard'
    if 'no authorized Android device found' in text or 'no authorized Android device is currently available' in text:
        print('[diagnosis] blocked on Android device authorization / connection')
        return 'device-auth'
    if 'HTTP 200' not in text and 'model verification failed' in text:
        print('[diagnosis] blocked on model verification or endpoint health')
        return 'model-verification'
    print('[diagnosis] runtime failure with no narrower classification')
    return 'runtime-failed'


def main() -> int:
    root_dir = Path(__file__).resolve().parent.parent
    device_type = sys.argv[1] if len(sys.argv) > 1 else 'android'
    model_mode = sys.argv[2] if len(sys.argv) > 2 else 'bigmodel'
    repo_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else Path.cwd() / 'Open-AutoGLM'
    task = sys.argv[4] if len(sys.argv) > 4 else ''

    if not task:
        print('[error] missing task string')
        print('Usage: ensure_and_run_task.py <device_type> <model_mode> <repo_dir> <task>')
        return 1

    print('[phase] direct end-to-end workflow')
    print('[info] first try to reuse the current local environment and auto-fix only what is locally repairable')

    if device_type == 'android':
        print('[phase] android connection preparation')
        prep = run([sys.executable, str(root_dir / 'scripts' / 'prepare_android_connection.py')])
        if prep.returncode == 0:
            print('[auto-fixed] android connection preparation completed')

    print('[phase] readiness check')
    ready = run([sys.executable, str(root_dir / 'scripts' / 'check_skill_ready.py'), str(repo_dir), device_type])
    if ready.returncode == 0:
        print('[ok] readiness check passed')
    elif ready.returncode == 2:
        print('[info] some prerequisites are still missing')
        print('[info] the workflow will auto-fix local installable blockers when possible')

        print('[phase] install host tools if needed')
        install_script = root_dir / 'scripts' / 'install_host_tools.py'
        if install_script.exists():
            install = subprocess.run([sys.executable, str(install_script), device_type], env=os.environ.copy())
            if install.returncode == 0:
                print('[auto-fixed] host tools step completed without fatal errors')
            else:
                print('[warn] host tool installation step reported a non-zero exit code; continuing to deployment / repair')

        print('[phase] deployment / repair')
        deploy_script = root_dir / 'scripts' / 'deploy_open_autoglm.py'
        deploy = subprocess.run([sys.executable, str(deploy_script), device_type, model_mode, str(repo_dir)], env=os.environ.copy())
        if deploy.returncode != 0:
            print('[runtime-failed] deployment / repair exited with a non-zero code')
            return deploy.returncode
        print('[auto-fixed] deployment / repair completed')

        print('[phase] readiness re-check')
        recheck = run([sys.executable, str(root_dir / 'scripts' / 'check_skill_ready.py'), str(repo_dir), device_type])
        if recheck.returncode != 0:
            classify_recheck(repo_dir, device_type)
            return 2
        print('[ok] readiness re-check passed')
    else:
        print('[error] readiness check failed unexpectedly')
        return ready.returncode

    print('[phase] model verification')
    py = venv_python(repo_dir)
    verify = subprocess.run([
        str(py), str(root_dir / 'scripts' / 'verify_open_autoglm.py'),
        '--base-url', os.environ.get('MODEL_BASE_URL', ''),
        '--model', os.environ.get('MODEL_NAME', ''),
        '--apikey', os.environ.get('MODEL_API_KEY', ''),
        '--task', '请输出一个最简单的 do(action="Wait", duration="1 seconds") 来验证动作格式'
    ], cwd=str(repo_dir), env=os.environ.copy())
    if verify.returncode != 0:
        print('[runtime-failed] model verification failed')
        print('[safe-to-retry] verify model endpoint settings or service health, then rerun the workflow')
        return verify.returncode

    print('[phase] real task execution')
    task_cmd = [sys.executable, str(root_dir / 'scripts' / 'run_phone_task.py'), str(repo_dir), task]
    task_run = run(task_cmd, capture=True)
    if task_run.stdout:
        print(task_run.stdout, end='' if task_run.stdout.endswith('\n') else '\n')
    if task_run.stderr:
        print(task_run.stderr, end='' if task_run.stderr.endswith('\n') else '\n', file=sys.stderr)

    diagnosis = diagnose_task_result((task_run.stdout or '') + '\n' + (task_run.stderr or ''), task_run.returncode)
    if task_run.returncode == 0:
        print('[ok] real task execution finished successfully')
    else:
        print('[runtime-failed] real task execution failed')
        if diagnosis == 'adb-keyboard':
            print('[phone-action-needed] install or enable ADB Keyboard, then rerun the workflow')
        elif diagnosis == 'device-auth':
            print('[phone-action-needed] reconnect and authorize the Android device, then rerun the workflow')
        elif diagnosis == 'phone-action-needed':
            print('[phone-action-needed] complete the takeover step on the phone, then rerun or resume the workflow')
        elif diagnosis == 'decision-needed':
            print('[decision-needed] provide the missing choice or intent detail, then rerun the workflow')
        elif diagnosis == 'model-verification':
            print('[config-needed] check model endpoint settings or service health, then rerun the workflow')
        print('[safe-to-retry] inspect the task logs above and retry after fixing the specific blocker')
    return task_run.returncode


if __name__ == '__main__':
    raise SystemExit(main())
