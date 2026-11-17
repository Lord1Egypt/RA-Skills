import sys
from pathlib import Path

def _is_wheel_installed() -> bool:
    path_str = str(Path(__file__).resolve())
    return "site-packages" in path_str

def get_skill_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path.cwd()
    if _is_wheel_installed():
        return Path.cwd()
    return Path(__file__).resolve().parent.parent

def get_data_dir() -> Path:
    return get_skill_root()
