#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill file of a skill folder

Usage:
    python utils/package_skill.py <path/to/skill-folder> [output-directory]

Example:
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./dist
"""

import fnmatch
import json
import re
import sys
import zipfile
from pathlib import Path

from quick_validate import validate_skill


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _load_ignore_patterns(skill_root: Path) -> list[str]:
    ignore_file = skill_root / ".clawhubignore"
    if not ignore_file.exists():
        return []

    patterns: list[str] = []
    for raw_line in ignore_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def _should_ignore(path: Path, skill_root: Path, ignore_patterns: list[str]) -> bool:
    relative_path = path.relative_to(skill_root)
    relative_posix = relative_path.as_posix()
    path_parts = relative_path.parts

    for pattern in ignore_patterns:
        normalized = pattern.rstrip("/")
        if not normalized:
            continue

        if fnmatch.fnmatch(relative_posix, normalized):
            return True
        if fnmatch.fnmatch(relative_path.name, normalized):
            return True
        if any(fnmatch.fnmatch(part, normalized) for part in path_parts):
            return True
        if pattern.endswith("/") and any(part == normalized for part in path_parts):
            return True
    return False


def _parse_semver(version: str) -> tuple[tuple[int, int, int], tuple[tuple[int, object], ...]]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?", version.strip())
    if not match:
        raise ValueError(f"Invalid semver version: {version}")

    core = tuple(int(match.group(i)) for i in range(1, 4))
    prerelease_raw = match.group(4)
    if not prerelease_raw:
        return core, tuple()

    prerelease_parts: list[tuple[int, object]] = []
    for part in prerelease_raw.split("."):
        if part.isdigit():
            prerelease_parts.append((0, int(part)))
        else:
            prerelease_parts.append((1, part))
    return core, tuple(prerelease_parts)


def _compare_semver(left: str, right: str) -> int:
    left_core, left_pre = _parse_semver(left)
    right_core, right_pre = _parse_semver(right)

    if left_core != right_core:
        return -1 if left_core < right_core else 1

    if left_pre == right_pre:
        return 0
    if not left_pre:
        return 1
    if not right_pre:
        return -1

    for left_part, right_part in zip(left_pre, right_pre):
        if left_part == right_part:
            continue
        left_kind, left_value = left_part
        right_kind, right_value = right_part
        if left_kind != right_kind:
            return -1 if left_kind < right_kind else 1
        return -1 if left_value < right_value else 1

    if len(left_pre) == len(right_pre):
        return 0
    return -1 if len(left_pre) < len(right_pre) else 1


def _check_version_freshness(skill_root: Path) -> tuple[bool, str]:
    meta_path = skill_root / "_meta.json"
    if not meta_path.exists():
        return False, "_meta.json not found"

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    current_version = meta.get("version")
    if not isinstance(current_version, str) or not current_version.strip():
        return False, "_meta.json version is missing or invalid"

    origin_path = skill_root / ".clawhub" / "origin.json"
    if not origin_path.exists():
        _parse_semver(current_version)
        return True, "No installed origin metadata; version freshness check skipped."

    origin = json.loads(origin_path.read_text(encoding="utf-8"))
    installed_version = origin.get("installedVersion")
    if not isinstance(installed_version, str) or not installed_version.strip():
        _parse_semver(current_version)
        return True, "Installed origin version missing; version freshness check skipped."

    if _compare_semver(current_version, installed_version) <= 0:
        return (
            False,
            f"Version in _meta.json ({current_version}) must be greater than installed version ({installed_version}).",
        )
    return True, f"Version freshness OK: {current_version} > {installed_version}."


def package_skill(skill_path, output_dir=None):
    """
    Package a skill folder into a .skill file.

    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory for the .skill file (defaults to current directory)

    Returns:
        Path to the created .skill file, or None if error
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"[ERROR] Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"[ERROR] Path is not a directory: {skill_path}")
        return None

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"[ERROR] SKILL.md not found in {skill_path}")
        return None

    # Run validation before packaging
    print("Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"[ERROR] Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"[OK] {message}\n")

    version_ok, version_message = _check_version_freshness(skill_path)
    if not version_ok:
        print(f"[ERROR] {version_message}")
        return None
    print(f"[OK] {version_message}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    ignore_patterns = _load_ignore_patterns(skill_path)

    # Create the .skill file (zip format)
    try:
        with zipfile.ZipFile(skill_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the skill directory
            for file_path in skill_path.rglob("*"):
                # Security: never follow or package symlinks.
                if file_path.is_symlink():
                    print(f"[WARN] Skipping symlink: {file_path}")
                    continue

                if _should_ignore(file_path, skill_path, ignore_patterns):
                    continue

                if file_path.is_file():
                    resolved_file = file_path.resolve()
                    if not _is_within(resolved_file, skill_path):
                        print(f"[ERROR] File escapes skill root: {file_path}")
                        return None
                    # If output lives under skill_path, avoid writing archive into itself.
                    if resolved_file == skill_filename.resolve():
                        print(f"[WARN] Skipping output archive: {file_path}")
                        continue

                    # Calculate the relative path within the zip.
                    arcname = Path(skill_name) / file_path.relative_to(skill_path)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\n[OK] Successfully packaged skill to: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"[ERROR] Error creating .skill file: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python utils/package_skill.py <path/to/skill-folder> [output-directory]")
        print("\nExample:")
        print("  python utils/package_skill.py skills/public/my-skill")
        print("  python utils/package_skill.py skills/public/my-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"Packaging skill: {skill_path}")
    if output_dir:
        print(f"   Output directory: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
