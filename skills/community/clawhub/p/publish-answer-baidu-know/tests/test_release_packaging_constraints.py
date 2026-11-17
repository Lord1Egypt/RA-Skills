# -*- coding: utf-8 -*-
"""发布打包守护：PyArmor 单文件行数与 UTF-8 without BOM。"""
from __future__ import annotations

import os
import unittest

from _support import get_skill_root

SCRIPTS_MAX_LINES = 1000
SCRIPTS_RECOMMENDED_MAX_LINES = 900

TEXT_EXTENSIONS = frozenset(
    {
        ".py",
        ".md",
        ".yml",
        ".yaml",
        ".json",
        ".toml",
        ".ini",
        ".txt",
        ".ps1",
        ".sh",
    }
)

SPECIAL_TEXT_FILES = frozenset({".env.example", ".gitignore"})

SKIP_DIR_NAMES = frozenset(
    {
        ".git",
        "__pycache__",
        ".pytest_cache",
        "rpa-artifacts",
        "videos",
    }
)

BINARY_EXTENSIONS = frozenset(
    {
        ".db",
        ".sqlite",
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".mp4",
        ".zip",
        ".tar",
        ".gz",
    }
)


def _is_text_candidate(path: str) -> bool:
    basename = os.path.basename(path)
    if basename in SPECIAL_TEXT_FILES:
        return True
    ext = os.path.splitext(basename)[1].lower()
    if ext in BINARY_EXTENSIONS:
        return False
    return ext in TEXT_EXTENSIONS


def _iter_text_files(skill_root: str) -> list[str]:
    found: list[str] = []
    for root, dirnames, filenames in os.walk(skill_root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for name in filenames:
            full = os.path.join(root, name)
            if _is_text_candidate(full):
                found.append(full)
    return sorted(found)


def _iter_scripts_py_files(skill_root: str) -> list[str]:
    scripts_dir = os.path.join(skill_root, "scripts")
    found: list[str] = []
    if not os.path.isdir(scripts_dir):
        return found
    for root, dirnames, filenames in os.walk(scripts_dir):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES]
        for name in filenames:
            if name.endswith(".py"):
                found.append(os.path.join(root, name))
    return sorted(found)


class TestReleasePackagingConstraints(unittest.TestCase):
    def test_scripts_py_files_under_pyarmor_line_limit(self) -> None:
        skill_root = get_skill_root()
        offenders: list[str] = []
        for path in _iter_scripts_py_files(skill_root):
            with open(path, encoding="utf-8") as f:
                line_count = sum(1 for _ in f)
            if line_count >= SCRIPTS_MAX_LINES:
                rel = os.path.relpath(path, skill_root).replace("\\", "/")
                offenders.append(
                    f"{rel}: {line_count} lines (limit < {SCRIPTS_MAX_LINES})"
                )
        self.assertEqual(
            offenders,
            [],
            msg=(
                "PyArmor trial/free mode may fail when a single Python file reaches "
                f"{SCRIPTS_MAX_LINES} lines; split this file into smaller modules. "
                f"Recommended keep each file < {SCRIPTS_RECOMMENDED_MAX_LINES} lines. "
                f"Offenders: {offenders}"
            ),
        )

    def test_text_files_are_utf8_without_bom(self) -> None:
        skill_root = get_skill_root()
        bom_failures: list[str] = []
        decode_failures: list[str] = []
        feff_failures: list[str] = []

        for path in _iter_text_files(skill_root):
            rel = os.path.relpath(path, skill_root).replace("\\", "/")
            with open(path, "rb") as f:
                raw = f.read()

            if raw.startswith(b"\xef\xbb\xbf"):
                bom_failures.append(rel)
                continue

            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                decode_failures.append(f"{rel}: {exc}")
                continue

            if "\ufeff" in text:
                feff_failures.append(rel)

        self.assertEqual(
            bom_failures,
            [],
            msg=(
                "Files must be saved as UTF-8 without BOM (remove UTF-8 BOM prefix). "
                f"Offenders: {bom_failures}"
            ),
        )
        self.assertEqual(
            decode_failures,
            [],
            msg=(
                "Files must be valid UTF-8 without BOM. "
                f"Offenders: {decode_failures}"
            ),
        )
        self.assertEqual(
            feff_failures,
            [],
            msg=(
                "Files must not contain U+FEFF; save as UTF-8 without BOM. "
                f"Offenders: {feff_failures}"
            ),
        )


if __name__ == "__main__":
    unittest.main()
