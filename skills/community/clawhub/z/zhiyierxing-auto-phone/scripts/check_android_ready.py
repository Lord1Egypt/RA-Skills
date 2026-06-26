#!/usr/bin/env python3
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from device_memory import remember_device


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def main() -> int:
    if not shutil.which('adb'):
        print('[error] adb not found. Install Android platform-tools first.')
        return 1

    print('[step] checking adb devices')
    subprocess.run(['adb', 'devices'])
    devices = run(['adb', 'devices'])
    lines = [line.strip() for line in devices.stdout.splitlines()[1:] if line.strip()]
    authorized = [line.split()[0] for line in lines if len(line.split()) >= 2 and line.split()[1] == 'device']
    if not authorized:
        print('[error] no authorized Android device found')
        print('Fixes:')
        print('  1. Use a data-capable USB cable')
        print('  2. Enable Developer Options and USB debugging')
        print('  3. Accept the USB debugging authorization popup on the phone')
        print('  4. Retry: adb kill-server && adb start-server && adb devices')
        return 1

    print('[ok] device(s):')
    for dev in authorized:
        print(dev)
        remember_device(dev, source='ready-check')

    print('[step] checking ADB Keyboard availability (non-blocking)')
    ime_list = run(['adb', 'shell', 'ime', 'list', '-a'])
    if 'com.android.adbkeyboard/.AdbIME' in (ime_list.stdout + ime_list.stderr):
        print('[ok] ADB Keyboard is installed or discoverable')
    else:
        print('[warn] ADB Keyboard not found in ime list')
        print('[warn] continue anyway; only ask the user to install/enable it if real text input later fails')
        print('[hint] if needed later, use:')
        print('  adb shell ime enable com.android.adbkeyboard/.AdbIME')
        print('  adb shell ime set com.android.adbkeyboard/.AdbIME')

    print('[done] android readiness check finished')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
