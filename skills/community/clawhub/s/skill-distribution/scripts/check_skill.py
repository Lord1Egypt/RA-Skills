#!/usr/bin/env python3
"""Check a skill folder against the rules skill registries share.

Usage: python check_skill.py <skill-folder>
Exit code 1 if any error is found; warnings do not fail the run.
"""
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
SECRET_RE = re.compile(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
RISKY_RE = re.compile(r"(curl|wget)[^\n|]*\|\s*(sudo\s+)?(ba|z)?sh\b")
MAX_BUNDLE = 50 * 1024 * 1024


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Top-level scalar keys only; nested maps are returned under 'parent.child'."""
    if not text.startswith("---"):
        raise ValueError("SKILL.md does not start with '---' YAML frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("SKILL.md frontmatter is not closed with '---'")
    fields: dict[str, str] = {}
    parent = ""
    for line in text[3:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indented = line.startswith((" ", "\t"))
        key, sep, value = line.strip().partition(":")
        if not sep:
            continue
        value = value.strip().strip("\"'")
        if not indented:
            parent = key if not value else ""
            fields[key] = value
        elif parent:
            fields[f"{parent}.{key}"] = value
    return fields, text[end + 4:]


def check(folder: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    skill_md = folder / "SKILL.md"
    if not skill_md.is_file():
        return [f"no SKILL.md in {folder}"], warnings

    text = skill_md.read_text(encoding="utf-8")
    try:
        fm, body = parse_frontmatter(text)
    except ValueError as exc:
        return [str(exc)], warnings

    name = fm.get("name", "")
    if not name:
        errors.append("frontmatter is missing 'name'")
    else:
        if len(name) > 64:
            errors.append(f"name is {len(name)} characters; the limit is 64")
        if not NAME_RE.match(name):
            errors.append(f"name '{name}' must be lowercase letters, digits and single hyphens, not starting or ending with a hyphen")
        if name != folder.resolve().name:
            errors.append(f"name '{name}' does not match the folder name '{folder.resolve().name}'")

    desc = fm.get("description", "")
    if not desc:
        errors.append("frontmatter is missing 'description'")
    elif len(desc) > 1024:
        errors.append(f"description is {len(desc)} characters; the limit is 1024")
    elif len(desc) < 60:
        warnings.append(f"description is only {len(desc)} characters; say what the skill does and when to use it")

    if len(fm.get("compatibility", "")) > 500:
        errors.append("compatibility is longer than 500 characters")

    lines = text.count("\n") + 1
    if lines > 500:
        warnings.append(f"SKILL.md is {lines} lines; keep it under 500 and move detail into references/")

    version = fm.get("version") or fm.get("metadata.version", "")
    if not version:
        warnings.append("no version found; ClawHub requires semver (use 1.0.0 for a first release)")
    elif not SEMVER_RE.match(version):
        warnings.append(f"version '{version}' is not semver (1.2.3); ClawHub will reject it")

    licence = fm.get("license", "")
    if not licence and not any((folder / n).is_file() for n in ("LICENSE", "LICENSE.txt", "LICENSE.md")):
        warnings.append("no license field or LICENSE file")
    if licence and licence.upper() != "MIT-0":
        warnings.append(f"license is '{licence}'; ClawHub relicenses everything as MIT-0, so skip ClawHub or accept that")

    for ref in re.findall(r"`((?:references|scripts|assets)/[^`\s]+)`", body):
        if not (folder / ref).exists():
            errors.append(f"SKILL.md points at '{ref}', which does not exist")

    total = 0
    for path in folder.rglob("*"):
        if not path.is_file() or any(part.startswith(".") for part in path.relative_to(folder).parts):
            continue
        total += path.stat().st_size
        if path.suffix.lower() in {".md", ".txt", ".py", ".sh", ".js", ".ts", ".json", ".yaml", ".yml", ".env"}:
            content = path.read_text(encoding="utf-8", errors="replace")
            rel = path.relative_to(folder)
            if SECRET_RE.search(content):
                errors.append(f"{rel} looks like it contains a secret or private key")
            if RISKY_RE.search(content):
                warnings.append(f"{rel} pipes a download into a shell; security scans flag this")
    if total > MAX_BUNDLE:
        errors.append(f"bundle is {total / 1048576:.1f} MB; ClawHub and claude.ai cap at 50 MB")

    return errors, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    folder = Path(sys.argv[1])
    if not folder.is_dir():
        print(f"error: {folder} is not a folder")
        return 2
    errors, warnings = check(folder)
    for e in errors:
        print(f"ERROR   {e}")
    for w in warnings:
        print(f"warning {w}")
    if not errors:
        print(f"ok      {folder.resolve().name}: {len(warnings)} warning(s), no errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
