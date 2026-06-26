#!/usr/bin/env python3
import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = 'https://github.com/zai-org/Open-AutoGLM.git'


def run(cmd):
    return subprocess.run(cmd)


def repo_usable(target_dir: Path) -> bool:
    return (target_dir / 'requirements.txt').exists() and (target_dir / 'main.py').exists()


def main() -> int:
    target_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / 'Open-AutoGLM'

    if not shutil.which('git'):
        print('[error] git not found. Please install git first.')
        return 1

    if (target_dir / '.git').exists():
        print(f'[info] repo already exists, updating: {target_dir}')
        pull = run(['git', '-C', str(target_dir), '-c', 'http.version=HTTP/1.1', 'pull', '--ff-only'])
        if pull.returncode == 0:
            return 0
        print('[warn] git pull failed, trying git fetch --all --prune as fallback')
        fetch = run(['git', '-C', str(target_dir), '-c', 'http.version=HTTP/1.1', 'fetch', '--all', '--prune'])
        if fetch.returncode == 0:
            return run(['git', '-C', str(target_dir), 'status', '--short']).returncode
        if repo_usable(target_dir):
            print('[warn] repo update failed, but local repo appears usable; continuing with local files')
            return 0
        return fetch.returncode

    print(f'[info] cloning repo to: {target_dir}')
    clone = run(['git', '-c', 'http.version=HTTP/1.1', 'clone', REPO_URL, str(target_dir)])
    if clone.returncode == 0:
        return 0
    if repo_usable(target_dir):
        print('[warn] repo clone failed, but local repo appears usable; continuing with local files')
        return 0
    return clone.returncode


if __name__ == '__main__':
    raise SystemExit(main())
