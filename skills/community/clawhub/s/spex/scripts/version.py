#!/usr/bin/env python3
"""Version management utility for spex.

Reads, checks, and bumps the version stored in pyproject.toml and SKILL.md.
The canonical pyproject.toml is in skills/spex/pyproject.toml (the
installable skill package). A dev-only pyproject.toml lives at the project
root; its version field is kept in sync but is not authoritative.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from common import logger

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_SKILL_DIR = _PROJECT_ROOT / "skills" / "spex"
_SKILL_PYPROJECT = _SKILL_DIR / "pyproject.toml"
_ROOT_PYPROJECT = _PROJECT_ROOT / "pyproject.toml"
_SKILL_MD = _SKILL_DIR / "SKILL.md"

_SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$")


def _read_pyproject_version(path: Path) -> str | None:
    """Extract version= from a pyproject.toml file."""
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r'^version\s*=\s*"([^"]+)"', line)
        if m:
            return m.group(1)
    return None


def _write_pyproject_version(path: Path, new_version: str) -> bool:
    """Update version= in a pyproject.toml file. Returns True if changed or already matches."""
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8")
    new_content = re.sub(
        r'^(version\s*=\s*")[^"]+"',
        rf'\g<1>{new_version}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )
    if new_content == content:
        # Either no version field found, or already at the target version.
        # Check if the current version already matches the target.
        current = _read_pyproject_version(path)
        return current == new_version
    path.write_text(new_content, encoding="utf-8")
    return True


def get_pyproject_version() -> str | None:
    """Return version from the skill's pyproject.toml (authoritative)."""
    return _read_pyproject_version(_SKILL_PYPROJECT)


def get_root_pyproject_version() -> str | None:
    """Return version from the root dev pyproject.toml (synced, not authoritative)."""
    return _read_pyproject_version(_ROOT_PYPROJECT)


def get_skill_version() -> str | None:
    if not _SKILL_MD.is_file():
        return None
    for line in _SKILL_MD.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^version:\s*(.+)", line)
        if m:
            return m.group(1).strip().strip("\"'")
    return None


def check_versions() -> bool:
    skill_pyproject_ver = get_pyproject_version()
    root_pyproject_ver = get_root_pyproject_version()
    skill_ver = get_skill_version()

    if skill_pyproject_ver is None:
        logger.error("Error: cannot read version from skills/spex/pyproject.toml")
        return False
    if skill_ver is None:
        logger.error("Error: cannot read version from SKILL.md")
        return False
    if skill_pyproject_ver != skill_ver:
        logger.error(
            "Error: version mismatch\n"
            "  skills/spex/pyproject.toml: %s\n"
            "  SKILL.md:                   %s",
            skill_pyproject_ver, skill_ver,
        )
        return False

    # Root pyproject.toml version is advisory (dev-only) but warn if out of sync.
    if root_pyproject_ver is not None and root_pyproject_ver != skill_pyproject_ver:
        logger.warning(
            "Warning: root pyproject.toml version out of sync\n"
            "  pyproject.toml:       %s\n"
            "  skills/spex/pyproject.toml: %s",
            root_pyproject_ver, skill_pyproject_ver,
        )

    return True


def bump_version(new_version: str) -> bool:
    if not _SEMVER_RE.match(new_version):
        logger.error("Error: invalid semver format: %s", new_version)
        return False

    # Update skill's pyproject.toml (authoritative)
    if not _write_pyproject_version(_SKILL_PYPROJECT, new_version):
        logger.error("Error: could not find version in skills/spex/pyproject.toml")
        return False

    # Update root pyproject.toml if it has a version field
    if _ROOT_PYPROJECT.is_file():
        _write_pyproject_version(_ROOT_PYPROJECT, new_version)

    # Update SKILL.md
    content = _SKILL_MD.read_text(encoding="utf-8")
    new_content = re.sub(
        r"^(version:\s*).+",
        rf"\g<1>{new_version}",
        content,
        count=1,
        flags=re.MULTILINE,
    )
    if new_content == content:
        # Version field already matches target.
        current = get_skill_version()
        if current == new_version:
            print(f"{new_version}")
            return True
        logger.error("Error: could not find version in SKILL.md")
        return False
    _SKILL_MD.write_text(new_content, encoding="utf-8")

    print(f"{new_version}")
    return True


def main(argv=None):
    from cli import ArgumentParser

    usage = """\
Usage: spex version [--check | --bump <version>]

Show, check, or bump the project version.

Options:
  --check         Exit 1 if version sources are inconsistent
  --bump <ver>    Update version in all files (semver format)
  -h, --help      Show this help message and exit
"""
    parser = ArgumentParser(prog="spex version", usage=usage)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--bump", metavar="VERSION")
    args = parser.parse(argv)

    if args.check:
        if not check_versions():
            sys.exit(1)
        ver = get_pyproject_version()
        logger.info("OK: %s", ver)
    elif args.bump:
        if not bump_version(args.bump):
            sys.exit(1)
    else:
        ver = get_pyproject_version()
        if ver is None:
            logger.error("Error: cannot read version")
            sys.exit(1)
        print(ver)


if __name__ == "__main__":
    from common import setup_logging
    setup_logging()
    main()
