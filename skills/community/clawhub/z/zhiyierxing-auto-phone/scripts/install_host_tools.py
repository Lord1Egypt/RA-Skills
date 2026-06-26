#!/usr/bin/env python3
import platform
import shutil
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, env=None)


def install_adb() -> int:
    if shutil.which('adb'):
        print('[ok] adb is already installed')
        return 0

    system = platform.system()
    if system == 'Darwin':
        if shutil.which('brew'):
            print('[step] installing Android platform tools via Homebrew')
            return run(['brew', 'install', 'android-platform-tools']).returncode
        print('[error] Homebrew is not installed or not on PATH')
        print('[next] install Homebrew first, or install Android platform-tools manually')
        return 1

    if system == 'Linux':
        print('[error] automatic adb installation for Linux is not implemented yet')
        print('[next] install adb using your distro package manager, then continue')
        return 1

    if system == 'Windows':
        if shutil.which('winget'):
            print('[step] installing Android platform tools via winget')
            return run(['winget', 'install', '--id', 'Google.PlatformTools', '--accept-package-agreements', '--accept-source-agreements']).returncode
        print('[error] winget is not available')
        print('[next] install Android SDK Platform-Tools manually or install winget, then continue')
        return 1

    print(f'[error] unsupported or unknown host OS: {system}')
    print('[next] install Android platform-tools manually, then continue')
    return 1


def main() -> int:
    device_type = sys.argv[1] if len(sys.argv) > 1 else 'android'

    if device_type == 'android':
        rc = install_adb()
        if rc != 0:
            return rc
    elif device_type == 'harmonyos':
        if shutil.which('hdc'):
            print('[ok] hdc is already installed')
        else:
            print('[error] automatic hdc installation is not implemented yet')
            print('[next] install HarmonyOS SDK tools manually, then continue')
            return 1
    elif device_type == 'iphone':
        print('[info] iPhone path does not use adb/hdc auto-install here')
    else:
        print(f'[error] unknown device type: {device_type}')
        return 1

    print('[done] host tool install step finished')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
