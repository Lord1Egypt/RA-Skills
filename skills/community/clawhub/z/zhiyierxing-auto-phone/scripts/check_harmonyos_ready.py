#!/usr/bin/env python3
import shutil
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> int:
    if not shutil.which('hdc'):
        print('[error] hdc not found. Install HarmonyOS SDK tools first.')
        return 1

    print('[step] checking hdc targets')
    subprocess.run(['hdc', 'list', 'targets'])
    targets = run(['hdc', 'list', 'targets'])
    lines = [line.strip() for line in (targets.stdout + '\n' + targets.stderr).splitlines() if line.strip()]
    parsed = [line for line in lines if line.lower() != 'list of connected targets']
    if not parsed:
        print('[error] no authorized HarmonyOS target found')
        print('Fixes:')
        print('  1. Enable Developer Options')
        print('  2. Enable USB debugging')
        print('  3. Accept the authorization prompt')
        print('  4. If wireless, run hdc tconn <ip:port>')
        return 1

    print('[ok] target(s):')
    for target in parsed:
        print(target)

    print('[done] harmonyos readiness check finished')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
