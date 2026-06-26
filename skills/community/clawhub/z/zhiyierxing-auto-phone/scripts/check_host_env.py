#!/usr/bin/env python3
import shutil
import subprocess
import sys
from python_runtime import MIN_MAJOR, MIN_MINOR, select_python


def find(cmd: str):
    return shutil.which(cmd)


def run_version(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        text = (out.stdout or out.stderr or '').strip()
        return out.returncode, text
    except Exception as e:
        return 1, str(e)


def main():
    wants = sys.argv[1:] or ['git', 'python3', 'adb']
    failed = False
    print('[host-check] checking:', ', '.join(wants))
    selected_python = select_python()

    for item in wants:
        if item == 'python3':
            if not selected_python:
                failed = True
                print(f'[missing] {item} (need Python {MIN_MAJOR}.{MIN_MINOR}+ )')
                continue
            path, ver, cmd = selected_python
            print(f'[ok] {item}: {path} (resolved via {cmd})')
            print(f'  Python {ver[0]}.{ver[1]}.{ver[2]}')
            continue

        path = find(item)
        if not path:
            failed = True
            print(f'[missing] {item}')
            continue
        print(f'[ok] {item}: {path}')
        code, text = run_version([item, 'version'])
        if code != 0:
            code, text = run_version([item, '--version'])
        if text:
            print(f'  {text.splitlines()[0]}')

    if failed:
        print(f'\n[summary] missing required tools or Python {MIN_MAJOR}.{MIN_MINOR}+ . install/fix them before continuing.')
        sys.exit(1)
    print('\n[summary] host prerequisites look present.')


if __name__ == '__main__':
    main()
