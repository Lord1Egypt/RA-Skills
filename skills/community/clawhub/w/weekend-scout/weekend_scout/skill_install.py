"""Helpers for installing Weekend Scout skills with a bound Python runtime."""

from __future__ import annotations

import shutil
from pathlib import Path

TEXT_RESOURCE_EXTENSIONS = {
    ".md",
    ".markdown",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".py",
    ".ps1",
    ".sh",
}


def bound_python_command(executable: str) -> str:
    """Return a shell-safe Python command bound to one concrete interpreter."""
    text = str(executable).strip()
    return f'"{text}"'


def bind_runtime_commands(text: str, executable: str) -> str:
    """Rewrite runtime CLI invocations to use one exact Python interpreter."""
    python_cmd = f"{bound_python_command(executable)} -m weekend_scout"
    return text.replace("python -m weekend_scout", python_cmd)


def copy_skill_tree(source_dir: Path, target_dir: Path, *, executable: str) -> None:
    """Copy one generated skill tree and bind runtime commands in text files."""
    target_dir.mkdir(parents=True, exist_ok=True)
    for item in source_dir.rglob("*"):
        rel = item.relative_to(source_dir)
        dest = target_dir / rel
        if item.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        if item.suffix.lower() in TEXT_RESOURCE_EXTENSIONS:
            content = item.read_text(encoding="utf-8")
            dest.write_text(bind_runtime_commands(content, executable), encoding="utf-8")
        else:
            shutil.copy2(item, dest)
