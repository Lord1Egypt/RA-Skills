#!/usr/bin/env python3
"""Package the skill folder as .zip and .skill archives after validation."""

from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
WORKSPACE_ROOT = SKILL_ROOT.parent

if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import validate_skill  # noqa: E402


EXCLUDED_DIR_NAMES = {"__pycache__", "__MACOSX", ".git"}
EXCLUDED_FILE_NAMES = {".DS_Store"}
EXCLUDED_SUFFIXES = {".pyc"}


def should_include(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDED_DIR_NAMES:
        return False
    if path.name in EXCLUDED_FILE_NAMES:
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return True


def read_version() -> str:
    version = (SKILL_ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        raise ValueError("VERSION file is empty.")
    return version


def build_archive(output_path: Path) -> None:
    if output_path.exists():
        output_path.unlink()

    with ZipFile(output_path, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(SKILL_ROOT.rglob("*")):
            if path.is_dir() or not should_include(path):
                continue
            arcname = Path(SKILL_ROOT.name) / path.relative_to(SKILL_ROOT)
            archive.write(path, arcname.as_posix())


def main() -> int:
    errors, warnings = validate_skill.validate_skill_root(SKILL_ROOT)
    print(f"Packaging skill from: {SKILL_ROOT}")
    if warnings:
        print("[WARN] Validation notes:")
        for item in warnings:
            print(f"  - {item}")
    if errors:
        print("[FAIL] Validation failed. Packaging aborted.")
        for item in errors:
            print(f"  - {item}")
        return 1

    version = read_version()
    version_tag = f"v{version}"

    versioned_zip_output = WORKSPACE_ROOT / f"{SKILL_ROOT.name}-{version_tag}.zip"
    versioned_skill_output = WORKSPACE_ROOT / f"{SKILL_ROOT.name}-{version_tag}.skill"
    latest_zip_output = WORKSPACE_ROOT / f"{SKILL_ROOT.name}.zip"
    latest_skill_output = WORKSPACE_ROOT / f"{SKILL_ROOT.name}.skill"

    build_archive(versioned_zip_output)
    build_archive(versioned_skill_output)
    build_archive(latest_zip_output)
    build_archive(latest_skill_output)

    print("[OK] Archives created:")
    print(f"  - {versioned_zip_output}")
    print(f"  - {versioned_skill_output}")
    print(f"  - {latest_zip_output}")
    print(f"  - {latest_skill_output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
