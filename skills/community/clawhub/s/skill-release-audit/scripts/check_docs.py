#!/usr/bin/env python3
"""
Module 6: SKILL.md Documentation Completeness
- Must have meaningful description in frontmatter
- Should have a Dependencies / Requirements section if any deps found
- Should mention all scripts and references
- Frontmatter should not have undocumented fields
"""

import re
from pathlib import Path

from _common import split_frontmatter
from i18n import t


ALLOWED_FRONTMATTER_KEYS = {
    # Cross-platform SKILL.md base spec (Anthropic standard)
    "name", "description", "license", "compatibility", "metadata", "allowed-tools",
    "version",
    # ClawHub / OpenClaw recognised top-level extensions (see references/hub-specs.md)
    "homepage", "emoji", "os", "always", "skillKey",
    "user-invocable", "disable-model-invocation", "command-dispatch",
    "command-tool", "command-arg-mode",
    # Dependency-declaration fields recognised by module 5 (check_deps.py)
    "python", "python_optional", "bins", "depends_on_skills",
}


def _fm_str(fm: dict, key: str) -> str:
    """Read a frontmatter value as a stripped string (tolerates list/dict/None)."""
    val = fm.get(key, "")
    if val is None:
        return ""
    return str(val).strip()


def _read_skill_md(skill_dir: Path) -> tuple[str, dict, str]:
    """Returns (raw_content, frontmatter_dict, body_text)."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return "", {}, ""

    content = skill_md.read_text(encoding="utf-8")
    fm, _fm_raw, body = split_frontmatter(content)
    return content, fm, body


def check_description_quality(fm: dict) -> list[dict]:
    issues = []
    desc = _fm_str(fm, "description")

    if not desc:
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": t("docs.no_description"),
            "severity": "ERROR",
        })
        return issues

    if len(desc) < 30:
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": t("docs.desc_too_short", n=len(desc)),
            "severity": "WARN",
        })

    # Good description should mention when to use
    trigger_words = ["when", "use when", "触发", "当用户", "支持", "Use when", "适用"]
    if not any(t.lower() in desc.lower() for t in trigger_words):
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": t("docs.desc_no_scenario"),
            "severity": "WARN",
        })

    return issues


def check_deps_section(skill_dir: Path, fm: dict, body: str) -> list[dict]:
    """If scripts exist with third-party imports, SKILL.md should have a deps section."""
    issues = []
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return issues

    has_py_scripts = any(s.suffix == ".py" for s in scripts_dir.iterdir() if s.is_file())
    if not has_py_scripts:
        return issues

    has_deps_section = bool(re.search(
        r'^#+\s*(依赖|Dependencies|Requirements|安装|Install)',
        body, re.MULTILINE | re.IGNORECASE
    ))

    # Also check frontmatter requires field
    has_requires_fm = any(k in fm for k in ["requires", "dependencies"])

    if not has_deps_section and not has_requires_fm:
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": (
t("docs.no_deps_section")
            ),
            "severity": "WARN",
        })

    return issues


def check_name_matches_dir(skill_dir: Path, fm: dict) -> list[dict]:
    issues = []
    declared_name = _fm_str(fm, "name")
    dir_name = skill_dir.name

    if declared_name and declared_name != dir_name:
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": (
t("docs.name_mismatch", name=declared_name, dir=dir_name)
            ),
            "severity": "WARN",
        })

    return issues


def check_version_field(fm: dict, version_severity: str = "INFO") -> list[dict]:
    """Validate the optional `version` frontmatter field.

    Most registries treat `version` as optional (ClawHub/GitHub). Some private
    SkillHub deployments require it. The target profile decides the severity of a
    *missing* version via `version_severity` (INFO / WARN / ERROR). A present but
    malformed version is always WARN.
    """
    issues = []
    version = _fm_str(fm, "version")

    if not version:
        if version_severity and version_severity.upper() != "OFF":
            issues.append({
                "file": "SKILL.md",
                "line": None,
                "message": (
t("docs.no_version")
                ),
                "severity": version_severity.upper(),
            })
    else:
        # 简单格式校验：应符合 semver x.y.z 或 x.y 格式
        if not re.match(r'^\d+\.\d+(\.\d+)?$', version):
            issues.append({
                "file": "SKILL.md",
                "line": None,
                "message": (
t("docs.bad_version", version=version)
                ),
                "severity": "WARN",
            })

    return issues


def check_unexpected_frontmatter_keys(fm: dict) -> list[dict]:
    issues = []
    unexpected = set(fm.keys()) - ALLOWED_FRONTMATTER_KEYS
    if unexpected:
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": (
t("docs.unexpected_keys", keys=', '.join(sorted(unexpected)), allowed=', '.join(sorted(ALLOWED_FRONTMATTER_KEYS)))
            ),
            "severity": "WARN",
        })
    return issues


def check_required_frontmatter(fm: dict, required: list) -> list[dict]:
    """Ensure all profile-required frontmatter fields are present and non-empty.
    `name`/`description` emptiness are already covered elsewhere; this catches any
    extra fields a target profile marks as required.
    """
    issues = []
    for key in required or []:
        if not _fm_str(fm, key):
            issues.append({
                "file": "SKILL.md",
                "line": None,
                "message": t("docs.required_field", key=key),
                "severity": "ERROR",
            })
    return issues


def check_slug(skill_dir: Path, fm: dict, profile: dict) -> list[dict]:
    """Validate skill name/dir against the target's slug rules."""
    issues = []
    pattern = profile.get("slug_regex")
    max_len = profile.get("slug_max_len")
    slug = _fm_str(fm, "name") or skill_dir.name

    if pattern and not re.match(pattern, slug):
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": (
t("docs.slug_pattern", slug=slug, pattern=pattern)
            ),
            "severity": "WARN",
        })
    if max_len and len(slug) > max_len:
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": t("docs.slug_too_long", slug=slug, n=len(slug), max=max_len),
            "severity": "WARN",
        })
    return issues


def check_field_lengths(fm: dict, profile: dict) -> list[dict]:
    """Enforce name/description max length when the profile declares them."""
    issues = []
    fmc = profile.get("frontmatter", {})
    name_max = fmc.get("name_max_len")
    desc_max = fmc.get("description_max_len")

    name = _fm_str(fm, "name")
    desc = _fm_str(fm, "description")
    if name_max and len(name) > name_max:
        issues.append({
            "file": "SKILL.md", "line": None,
            "message": t("docs.name_too_long", n=len(name), max=name_max),
            "severity": "WARN",
        })
    if desc_max and len(desc) > desc_max:
        issues.append({
            "file": "SKILL.md", "line": None,
            "message": t("docs.desc_too_long", n=len(desc), max=desc_max),
            "severity": "WARN",
        })
    return issues


def check_required_files(skill_dir: Path, profile: dict) -> list[dict]:
    """Check for README / LICENSE when the target profile requires them
    (e.g. GitHub). Registries like ClawHub do not require these.
    """
    issues = []
    files_cfg = profile.get("files", {})

    if files_cfg.get("require_readme"):
        if not any((skill_dir / n).exists() for n in ("README.md", "README.rst", "README.txt", "README")):
            issues.append({
                "file": ".", "line": None,
                "message": t("docs.no_readme"),
                "severity": "WARN",
            })
    if files_cfg.get("require_license"):
        if not any((skill_dir / n).exists() for n in ("LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING")):
            issues.append({
                "file": ".", "line": None,
                "message": t("docs.no_license"),
                "severity": "WARN",
            })
    return issues


def run(skill_dir: Path, profile: dict | None = None) -> dict:
    issues = []
    profile = profile or {}
    fm_cfg = profile.get("frontmatter", {})
    content, fm, body = _read_skill_md(skill_dir)

    if not content:
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": t("docs.no_skill_md"),
            "severity": "ERROR",
        })
        return {
            "module": t("module.docs"),
            "status": "FAIL",
            "issues": issues,
        }

    issues.extend(check_description_quality(fm))
    issues.extend(check_version_field(fm, fm_cfg.get("version_severity", "INFO")))
    issues.extend(check_required_frontmatter(fm, fm_cfg.get("required", [])))
    issues.extend(check_field_lengths(fm, profile))
    issues.extend(check_slug(skill_dir, fm, profile))
    issues.extend(check_required_files(skill_dir, profile))
    issues.extend(check_deps_section(skill_dir, fm, body))
    issues.extend(check_name_matches_dir(skill_dir, fm))
    issues.extend(check_unexpected_frontmatter_keys(fm))

    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]

    return {
        "module": t("module.docs"),
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "issues": issues,
    }
