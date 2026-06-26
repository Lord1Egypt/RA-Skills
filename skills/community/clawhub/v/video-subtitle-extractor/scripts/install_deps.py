#!/usr/bin/env python3
"""Video Subtitle Extractor - Dependency Installer

Auto-detects and installs all required dependencies:
- ffmpeg (system package manager)
- yt-dlp (pip)
- openai-whisper (pip) or faster-whisper
Supports Windows (winget), macOS (brew), Linux (apt).
"""

import subprocess
import sys
import shutil
import platform
import os


def run(cmd, check=True, shell=False):
    """Run a shell command and return success."""
    try:
        if isinstance(cmd, list):
            subprocess.run(cmd, check=check, capture_output=False)
        else:
            subprocess.run(cmd, shell=True, check=check, capture_output=False)
        return True
    except subprocess.CalledProcessError:
        return False


def get_platform():
    """Detect OS platform."""
    system = platform.system()
    if system == 'Windows':
        return 'windows'
    elif system == 'Darwin':
        return 'macos'
    else:
        return 'linux'


# Common ffmpeg install paths on Windows (not always in PATH)
FFMPEG_WIN_PATHS = [
    os.path.join(os.environ.get('ProgramFiles', r'C:\Program Files'), 'TRCCCAP', 'ffmpeg.exe'),
    os.path.join(os.environ.get('ProgramFiles', r'C:\Program Files'), 'FFmpeg', 'bin', 'ffmpeg.exe'),
    os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'ffmpeg', 'bin', 'ffmpeg.exe'),
]


def check_binary(name):
    """Check if a binary exists in PATH or known install locations."""
    if shutil.which(name) is not None:
        return True
    # On Windows, check common install paths for ffmpeg
    if name == 'ffmpeg' and get_platform() == 'windows':
        for p in FFMPEG_WIN_PATHS:
            if os.path.isfile(p):
                print(f'  Found at: {p} (not in PATH)')
                return True
    return False


def install_ffmpeg():
    """Install ffmpeg via system package manager."""
    if check_binary('ffmpeg'):
        print('[OK] ffmpeg already installed')
        return True

    print('[INSTALL] ffmpeg...')
    plat = get_platform()

    if plat == 'windows':
        if check_binary('winget'):
            ok = run('winget install Gyan.FFmpeg --accept-package-agreements --silent', shell=True)
            if ok:
                print('  FFmpeg installed. Add to PATH: C:\\Program Files\\TRCCCAP\\')
                return True
        print('[WARN] Cannot auto-install ffmpeg. Install manually from https://ffmpeg.org/')
        return False

    elif plat == 'macos':
        if check_binary('brew'):
            return run(['brew', 'install', 'ffmpeg'])

    elif plat == 'linux':
        if check_binary('apt'):
            return run(['sudo', 'apt', 'install', '-y', 'ffmpeg'])

    print('[WARN] Could not auto-install ffmpeg on this platform')
    return False


def install_yt_dlp():
    """Install yt-dlp via pip."""
    try:
        import yt_dlp
        print('[OK] yt-dlp already installed')
        return True
    except ImportError:
        pass

    print('[INSTALL] yt-dlp...')
    return run([sys.executable, '-m', 'pip', 'install', 'yt-dlp', '--user'], check=False)


def install_whisper(mode='openai'):
    """Install speech-to-text engine (openai-whisper or faster-whisper)."""
    if mode == 'faster':
        try:
            import faster_whisper
            print('[OK] faster-whisper already installed')
            return True
        except ImportError:
            pass
        print('[INSTALL] faster-whisper...')
        return run([sys.executable, '-m', 'pip', 'install', 'faster-whisper', '--user'], check=False)
    else:
        try:
            import whisper
            print('[OK] openai-whisper already installed')
            return True
        except ImportError:
            pass
        print('[INSTALL] openai-whisper...')
        return run([sys.executable, '-m', 'pip', 'install', 'openai-whisper', '--user'], check=False)


def install_all(mode='openai'):
    """Install all dependencies and return summary."""
    print('=== Video Subtitle Extractor - Dependency Installer ===')
    print(f'Platform: {get_platform()}')
    print()

    results = {
        'ffmpeg': install_ffmpeg(),
        'yt-dlp': install_yt_dlp(),
        'whisper': install_whisper(mode),
    }

    print()
    print('=== Installation Summary ===')
    all_ok = True
    for name, ok in results.items():
        status = 'OK' if ok else 'FAILED'
        print(f'  [{status}] {name}')
        if not ok:
            all_ok = False

    if all_ok:
        print()
        print('All dependencies installed successfully!')
    else:
        print()
        print('Some dependencies failed. Check warnings above.')

    return all_ok


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'openai'
    install_all(mode)