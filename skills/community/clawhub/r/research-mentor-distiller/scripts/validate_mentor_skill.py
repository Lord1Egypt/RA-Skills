#!/usr/bin/env python3
"""Validate a MentorForge-generated scholar mentor skill package.

This validator intentionally does not install skills. It checks package
completeness, manifest consistency, version gates, and portability issues.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "distillation-manifest.json",
    "references/evidence-snapshot.md",
    "references/publication-index.md",
    "references/research-taste-profile.md",
    "references/fulltext-distillation.md",
    "references/validation.md",
]

VERSION_ORDER = {"v0": 0, "v1": 1, "v1.5": 1.5, "v2": 2, "v3": 3}


def fail(messages: list[str], text: str) -> None:
    messages.append(f"FAIL: {text}")


def warn(messages: list[str], text: str) -> None:
    messages.append(f"WARN: {text}")


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(skill_md: Path) -> tuple[dict[str, str], str | None]:
    text = load_text(skill_md)
    match = re.match(r"^---\n(.*?)\n---\n?", text, re.DOTALL)
    if not match:
        return {}, "SKILL.md is missing YAML frontmatter"
    raw = match.group(1)
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            return data, f"Invalid frontmatter line: {line!r}"
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, None


def is_ascii(text: str) -> bool:
    try:
        text.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def read_manifest(path: Path, messages: list[str]) -> dict[str, Any]:
    try:
        return json.loads(load_text(path))
    except FileNotFoundError:
        fail(messages, "distillation-manifest.json is missing")
    except json.JSONDecodeError as exc:
        fail(messages, f"distillation-manifest.json is invalid JSON: {exc}")
    return {}


def version_value(version: str | None) -> float:
    if not version:
        return -1
    return VERSION_ORDER.get(version.lower(), -1)


def validate_openai_yaml(skill_dir: Path, skill_name: str | None, messages: list[str]) -> None:
    path = skill_dir / "agents" / "openai.yaml"
    if not path.exists():
        return
    text = load_text(path)
    for needle in ["interface:", "display_name:", "short_description:", "default_prompt:"]:
        if needle not in text:
            fail(messages, f"agents/openai.yaml missing `{needle}`")
    if skill_name and f"${skill_name}" not in text:
        warn(messages, "agents/openai.yaml default_prompt should mention the skill as `$skill-name`")


def validate_manifest(
    skill_dir: Path,
    manifest: dict[str, Any],
    frontmatter: dict[str, str],
    args: argparse.Namespace,
    messages: list[str],
) -> None:
    skill_name = frontmatter.get("name")
    claimed = str(manifest.get("version_claimed", "")).lower()
    target = (args.target_version or claimed).lower()
    evidence = manifest.get("evidence", {}) if isinstance(manifest.get("evidence"), dict) else {}
    validation = manifest.get("validation", {}) if isinstance(manifest.get("validation"), dict) else {}
    fallback = manifest.get("fallback", {}) if isinstance(manifest.get("fallback"), dict) else {}

    for key in ["schema_version", "target", "skill_name", "version_claimed", "evidence", "validation"]:
        if key not in manifest:
            fail(messages, f"distillation-manifest.json missing `{key}`")

    if skill_name and manifest.get("skill_name") and manifest.get("skill_name") != skill_name:
        fail(messages, "manifest `skill_name` does not match SKILL.md frontmatter name")

    if skill_name and skill_dir.name != skill_name:
        fail(messages, "skill folder basename does not match SKILL.md frontmatter name")

    if target and version_value(claimed) < version_value(target):
        fail(messages, f"manifest claims `{claimed}` but target validation requested `{target}`")

    publication_count = int(evidence.get("publication_count") or 0)
    abstracts_count = int(evidence.get("abstracts_count") or 0)
    pdf_downloaded = int(evidence.get("pdf_downloaded") or 0)
    fulltext_extracted = int(evidence.get("fulltext_extracted") or 0)
    directions = evidence.get("directions_covered") or []
    forward_tests = int(validation.get("forward_tests") or 0)

    target_value = version_value(target)
    if target_value >= 1 and publication_count < args.min_publications:
        fail(messages, f"v1+ requires at least {args.min_publications} publication records; found {publication_count}")

    if target_value >= 1 and abstracts_count <= 0 and fulltext_extracted <= 0:
        warn(messages, "v1+ has no abstracts_count and no fulltext_extracted recorded")

    if target_value >= 2:
        if fulltext_extracted < args.min_fulltext:
            fail(messages, f"v2 requires at least {args.min_fulltext} extracted full-text papers; found {fulltext_extracted}")
        if pdf_downloaded and fulltext_extracted > pdf_downloaded:
            fail(messages, "fulltext_extracted cannot exceed pdf_downloaded")
        if len(directions) < args.min_directions:
            fail(messages, f"v2 requires at least {args.min_directions} covered direction(s); found {len(directions)}")

    if target_value >= 3 and forward_tests < args.min_forward_tests:
        fail(messages, f"v3 requires at least {args.min_forward_tests} forward tests; found {forward_tests}")

    if fallback.get("used") and not fallback.get("attempts"):
        warn(messages, "fallback.used is true but fallback.attempts is empty")


def validate_skill_dir(skill_dir: Path, args: argparse.Namespace) -> tuple[bool, list[str]]:
    messages: list[str] = []
    if not skill_dir.exists():
        return False, [f"FAIL: skill directory does not exist: {skill_dir}"]
    if not skill_dir.is_dir():
        return False, [f"FAIL: path is not a directory: {skill_dir}"]

    for rel in REQUIRED_FILES:
        path = skill_dir / rel
        if not path.exists():
            fail(messages, f"missing required file `{rel}`")
        elif path.is_file() and path.stat().st_size == 0:
            fail(messages, f"required file `{rel}` is empty")

    skill_md = skill_dir / "SKILL.md"
    frontmatter: dict[str, str] = {}
    if skill_md.exists():
        frontmatter, error = parse_frontmatter(skill_md)
        if error:
            fail(messages, error)
        else:
            for key in ["name", "description"]:
                if not frontmatter.get(key):
                    fail(messages, f"SKILL.md frontmatter missing `{key}`")
            raw_frontmatter = re.match(r"^---\n(.*?)\n---", load_text(skill_md), re.DOTALL)
            if raw_frontmatter and not is_ascii(raw_frontmatter.group(1)):
                fail(messages, "SKILL.md frontmatter must be ASCII-only for portability")
            name = frontmatter.get("name", "")
            if name and not re.fullmatch(r"[a-z0-9-]{1,63}", name):
                fail(messages, "SKILL.md frontmatter name must use lowercase letters, digits, and hyphens only")
            body = load_text(skill_md)
            for phrase in ["private opinion", "admissions", "review"]:
                if phrase not in body.lower():
                    warn(messages, f"SKILL.md may be missing boundary language for `{phrase}`")

    validate_openai_yaml(skill_dir, frontmatter.get("name"), messages)
    manifest = read_manifest(skill_dir / "distillation-manifest.json", messages)
    if manifest:
        validate_manifest(skill_dir, manifest, frontmatter, args, messages)

    for rel in [
        "references/evidence-snapshot.md",
        "references/research-taste-profile.md",
        "references/fulltext-distillation.md",
        "references/validation.md",
    ]:
        path = skill_dir / rel
        if path.exists():
            text = load_text(path)
            if len(text.strip()) < 200:
                warn(messages, f"`{rel}` looks too thin for a durable mentor skill")

    failed = any(message.startswith("FAIL:") for message in messages)
    if args.strict and any(message.startswith("WARN:") for message in messages):
        failed = True
    return not failed, messages


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a MentorForge mentor skill package without installing it.")
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--target-version", choices=["v0", "v1", "v1.5", "v2", "v3"], help="Minimum version to validate against.")
    parser.add_argument("--min-publications", type=int, default=20)
    parser.add_argument("--min-fulltext", type=int, default=10)
    parser.add_argument("--min-directions", type=int, default=1)
    parser.add_argument("--min-forward-tests", type=int, default=3)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    args = parser.parse_args()

    ok, messages = validate_skill_dir(args.skill_dir, args)
    status = "PASS" if ok else "FAIL"
    print(f"Mentor skill compliance: {status}")
    if messages:
        for message in messages:
            print(f"- {message}")
    else:
        print("- no issues found")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
