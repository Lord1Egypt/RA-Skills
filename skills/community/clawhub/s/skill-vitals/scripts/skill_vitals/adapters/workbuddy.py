"""WorkBuddy manifest/cache and welcome-mode discovery."""

import json
import os
import re
from pathlib import Path

from ..util import norm


WORKBUDDY_ORPHANED = []


def _safe_segment(value):
    """Return whether untrusted manifest data is one ordinary path segment."""
    if not isinstance(value, str) or not value or value in (".", ".."):
        return False
    return "/" not in value and "\\" not in value and "\0" not in value


def read_workbuddy_builtin_roots(home=None, orphaned=None):
    """Resolve WorkBuddy's top-level installed Skill packages from its cache."""
    base_home = Path(home) if home is not None else Path(os.path.expanduser("~"))
    marketplace = base_home / ".workbuddy" / "plugins" / "marketplaces" / "workbuddy-builtin"
    manifest = marketplace / ".codebuddy-plugin" / "marketplace.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    roots = []
    base = marketplace.resolve()
    cache = base_home / ".workbuddy" / "plugins" / "cache" / "workbuddy-builtin"
    seen_packages = set()
    orphaned_packages = WORKBUDDY_ORPHANED if orphaned is None else orphaned
    for plugin in data.get("plugins", []):
        category = plugin.get("category")
        if category not in ("skill", "builtin-plugin"):
            continue
        source = plugin.get("source")
        if not isinstance(source, str):
            continue
        manifest_source = (marketplace / source).resolve()
        try:
            manifest_source.relative_to(base)
        except ValueError:
            continue
        package = plugin.get("name")
        version = plugin.get("version")
        if not (_safe_segment(package) and _safe_segment(version)):
            continue
        if package in seen_packages:
            continue
        seen_packages.add(package)
        cached = cache / str(package) / str(version)
        try:
            cached.resolve().relative_to(cache.resolve())
        except (ValueError, OSError):
            continue
        candidate = cached if (cached / "SKILL.md").is_file() else manifest_source
        metadata = {
            "workbuddy_package": package,
            "workbuddy_version": version,
            "workbuddy_legacy_name": manifest_source.name,
            "workbuddy_orphan_marker": (cached / ".orphaned_at").is_file(),
        }
        if (metadata["workbuddy_orphan_marker"] and
                package not in orphaned_packages):
            orphaned_packages.append(package)

        if category == "skill":
            if candidate.is_dir():
                roots.append((str(candidate), dict(
                    metadata, root_kind=("builtin-skill-cache" if candidate == cached
                                         else "builtin-skill-marketplace-fallback"))))
            continue

        cache_usable = cached.is_dir() and (
            (cached / "SKILL.md").is_file() or (cached / "skills").is_dir())
        package_root = cached if cache_usable else manifest_source
        if not package_root.is_dir():
            continue
        if (package_root / "SKILL.md").is_file():
            roots.append((str(package_root), dict(
                metadata, root_kind="builtin-plugin-package", only_direct=True)))
        skills_dir = package_root / "skills"
        if skills_dir.is_dir():
            for child in sorted(skills_dir.iterdir(), key=norm):
                if (child / "SKILL.md").is_file():
                    roots.append((str(child), dict(
                        metadata, root_kind="builtin-plugin-skill")))
    return roots


def read_workbuddy_welcome_mode(home=None):
    """Read the latest session's welcomeMode from local WorkBuddy logs."""
    base_home = Path(home) if home is not None else Path(os.path.expanduser("~"))
    logs = base_home / ".workbuddy" / "logs"
    try:
        files = sorted(logs.rglob("*.log"), key=lambda path: path.stat().st_mtime,
                       reverse=True)
    except OSError:
        return None
    pattern = re.compile(r'(?:welcomeMode[=:]|X-WorkBuddy-Welcome-Mode[\\"]*[:=][\\"]*)'
                         r'(work|design|code)', re.I)
    for path in files[:20]:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        matches = pattern.findall(text)
        if matches:
            return matches[-1].lower()
    return None


def workbuddy_skill_active(legacy_name, welcome_mode):
    """Ardot packages are injected only into WorkBuddy's design welcome mode."""
    return not (str(legacy_name).startswith("ardot-") and
                welcome_mode and welcome_mode != "design")
