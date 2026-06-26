#!/usr/bin/env python3
import platform
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

MIN_MAJOR = 3
MIN_MINOR = 10


def version_tuple(text: str) -> Optional[Tuple[int, int, int]]:
    parts = text.strip().split()
    for token in parts:
        if token and token[0].isdigit():
            nums = token.split('.')
            try:
                major = int(nums[0])
                minor = int(nums[1]) if len(nums) > 1 else 0
                patch = int(nums[2]) if len(nums) > 2 else 0
                return major, minor, patch
            except Exception:
                return None
    return None


def is_supported(ver: Tuple[int, int, int]) -> bool:
    return ver >= (MIN_MAJOR, MIN_MINOR, 0)


def candidate_commands() -> List[str]:
    system = platform.system()
    if system == 'Windows':
        return ['python3.12', 'python3.11', 'python3.10', 'python', 'py', 'python3']
    return ['python3.12', 'python3.11', 'python3.10', 'python3', 'python']


def probe(cmd: str) -> Optional[Tuple[str, Tuple[int, int, int]]]:
    path = shutil.which(cmd)
    if not path:
        return None
    try:
        out = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=10)
        text = (out.stdout or out.stderr or '').strip()
        ver = version_tuple(text)
        if ver is None:
            return None
        return path, ver
    except Exception:
        return None


def select_python() -> Optional[Tuple[str, Tuple[int, int, int], str]]:
    for cmd in candidate_commands():
        probed = probe(cmd)
        if not probed:
            continue
        path, ver = probed
        if is_supported(ver):
            return path, ver, cmd
    return None


def install_python_if_possible() -> bool:
    system = platform.system()
    if system == 'Darwin' and shutil.which('brew'):
        for formula in ['python@3.12', 'python@3.11', 'python@3.10']:
            rc = subprocess.run(['brew', 'install', formula]).returncode
            if rc == 0 and select_python():
                return True
        return False
    if system == 'Windows' and shutil.which('winget'):
        for pkg in ['Python.Python.3.12', 'Python.Python.3.11', 'Python.Python.3.10']:
            rc = subprocess.run(['winget', 'install', '--id', pkg, '--accept-package-agreements', '--accept-source-agreements']).returncode
            if rc == 0 and select_python():
                return True
        return False
    return False


def venv_python(repo_dir: Path) -> Path:
    if platform.system() == 'Windows':
        return repo_dir / '.venv' / 'Scripts' / 'python.exe'
    return repo_dir / '.venv' / 'bin' / 'python'
