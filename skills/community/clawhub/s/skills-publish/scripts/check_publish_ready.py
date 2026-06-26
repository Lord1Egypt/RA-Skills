#!/usr/bin/env python3
"""Check local readiness for publishing a skill to ClawHub."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


SEMVER_RE = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:[-+][0-9A-Za-z.-]+)?$")
SLUG_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
PERSONAL_PATH_RE = re.compile(r"(/Users/[^/\s]+|C:\\Users\\[^\\\s]+)", re.IGNORECASE)
TODO_RE = re.compile(r"\bTODO\b", re.IGNORECASE)
TAGS_RE = re.compile(r"^[a-z0-9-]+(?:,[a-z0-9-]+)*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check a skill folder before publishing to ClawHub."
    )
    parser.add_argument("skill_path", help="Path to the skill folder")
    parser.add_argument("--slug", help="Target ClawHub slug")
    parser.add_argument("--display-name", help="Display name for ClawHub")
    parser.add_argument("--version", help="Semver version to publish")
    parser.add_argument(
        "--change-type",
        choices=["first-release", "patch", "minor", "major"],
        help="Suggest a default version when --version is omitted",
    )
    parser.add_argument("--changelog", default="", help="Optional changelog text")
    parser.add_argument("--tags", default="latest", help="Comma-separated tags")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    return parser.parse_args()


def strip_wrapping_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def fold_block_lines(lines: list[str], style: str) -> str:
    if style == "|":
        return "\n".join(lines).rstrip()
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if line.strip():
            current.append(line.strip())
            continue
        if current:
            paragraphs.append(" ".join(current))
            current = []
        paragraphs.append("")
    if current:
        paragraphs.append(" ".join(current))
    return "\n".join(paragraphs).rstrip()


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md is missing valid YAML frontmatter delimited by ---")
    raw = match.group(1)
    body = match.group(2)
    data: dict[str, Any] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            i += 1
            continue
        if line.startswith((" ", "\t")):
            raise ValueError(f"Unsupported frontmatter indentation at top level: {line}")
        key, sep, remainder = line.partition(":")
        if not sep:
            raise ValueError(f"Unsupported frontmatter line: {line}")
        key = key.strip()
        remainder = remainder.strip()
        if remainder in {"|", ">"}:
            style = remainder
            i += 1
            block_indent = None
            block_lines: list[str] = []
            while i < len(lines):
                current = lines[i]
                if not current.strip():
                    block_lines.append("")
                    i += 1
                    continue
                indent = len(current) - len(current.lstrip(" "))
                if block_indent is None:
                    if indent == 0:
                        break
                    block_indent = indent
                if indent < block_indent:
                    break
                block_lines.append(current[block_indent:])
                i += 1
            data[key] = fold_block_lines(block_lines, style)
            continue
        data[key] = strip_wrapping_quotes(remainder)
        i += 1
    return data, body


def internal_links(body: str) -> list[str]:
    links = re.findall(r"\[.*?\]\(((?!https?://).*?)\)", body)
    return [link.split("#")[0].strip() for link in links if link.split("#")[0].strip()]


def build_publish_command(
    skill_path: Path,
    slug: str,
    display_name: str,
    version: str,
    changelog: str,
    tags: str,
) -> str:
    parts = [
        "clawhub",
        "publish",
        str(skill_path),
        "--slug",
        slug,
        "--name",
        display_name,
        "--version",
        version,
        "--tags",
        tags,
    ]
    if changelog:
        parts.extend(["--changelog", changelog])
    return " ".join(shlex.quote(part) for part in parts)


def suggest_version(change_type: str | None) -> str | None:
    if change_type == "first-release":
        return "1.0.0"
    if change_type == "patch":
        return "1.0.1"
    if change_type == "minor":
        return "1.1.0"
    if change_type == "major":
        return "2.0.0"
    return None


def detect_personal_paths(text: str) -> list[str]:
    matches = PERSONAL_PATH_RE.findall(text)
    unique: list[str] = []
    for item in matches:
        if item not in unique:
            unique.append(item)
    return unique[:5]


def main() -> int:
    args = parse_args()
    skill_path = Path(args.skill_path).expanduser().resolve()
    skill_file = skill_path / "SKILL.md"

    findings: list[dict[str, str]] = []
    frontmatter: dict[str, Any] = {}
    body = ""
    next_steps: list[str] = []

    if not skill_file.exists():
        findings.append({"severity": "critical", "message": f"Missing file: {skill_file}"})
    else:
        text = skill_file.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(text)

        name = str(frontmatter.get("name", "")).strip()
        description = str(frontmatter.get("description", "")).strip()

        if not name:
            findings.append({"severity": "critical", "message": "Frontmatter name is missing."})
        elif name != skill_path.name:
            findings.append({"severity": "high", "message": f"Frontmatter name '{name}' does not match directory '{skill_path.name}'."})

        if not description:
            findings.append({"severity": "critical", "message": "Frontmatter description is missing."})
        elif "use when" not in description.lower():
            findings.append({"severity": "high", "message": "Frontmatter description should include explicit 'Use when ...' trigger phrasing."})

        metadata = str(frontmatter.get("metadata", ""))
        if "openclaw" not in metadata.lower():
            findings.append({"severity": "medium", "message": "metadata.openclaw is missing or not obvious in frontmatter."})

        missing_links = [link for link in internal_links(body) if not (skill_path / link).exists()]
        if missing_links:
            findings.append({"severity": "high", "message": f"Broken internal links: {', '.join(missing_links)}"})

        todo_hits = TODO_RE.findall(text)
        if todo_hits:
            findings.append({"severity": "medium", "message": "TODO placeholders remain in the skill package."})

        path_hits = detect_personal_paths(text)
        if path_hits:
            findings.append({"severity": "high", "message": f"Personal path(s) found in public files: {', '.join(path_hits)}"})

    slug = args.slug or skill_path.name
    if not SLUG_RE.match(slug):
        findings.append({"severity": "high", "message": f"Slug '{slug}' is not lowercase-hyphen format."})

    version = args.version or suggest_version(args.change_type)
    if version and not SEMVER_RE.match(version):
        findings.append({"severity": "high", "message": f"Version '{version}' is not valid semver."})
    if not args.version and version:
        next_steps.append(f"Suggested version from change type: {version}")

    if args.tags and not TAGS_RE.match(args.tags):
        findings.append({"severity": "medium", "message": f"Tags '{args.tags}' should be lowercase, hyphenated, and comma-separated."})

    if not shutil.which("clawhub"):
        findings.append({"severity": "medium", "message": "clawhub CLI is not installed or not on PATH."})
    else:
        try:
            whoami = subprocess.run(
                ["clawhub", "whoami"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            if whoami.returncode != 0:
                findings.append({"severity": "medium", "message": "clawhub CLI is installed, but login state could not be confirmed with `clawhub whoami`. Run `clawhub login` or `clawhub login --token <token>`. "})
            elif whoami.stdout.strip():
                next_steps.append(f"Authenticated as: {whoami.stdout.strip()}")
        except Exception:
            findings.append({"severity": "low", "message": "Could not verify `clawhub whoami`; confirm CLI login state manually before publish."})

    publish_command = None
    if args.display_name and version and SLUG_RE.match(slug) and SEMVER_RE.match(version):
        publish_command = build_publish_command(
            skill_path=skill_path,
            slug=slug,
            display_name=args.display_name,
            version=version,
            changelog=args.changelog,
            tags=args.tags,
        )
    else:
        if not args.display_name:
            next_steps.append("Provide --display-name to generate the final publish command.")
        if not version:
            next_steps.append("Provide --version or --change-type to generate the final publish command.")

    ready = not any(item["severity"] == "critical" for item in findings)
    report = {
        "skill_path": str(skill_path),
        "slug": slug,
        "display_name": args.display_name or "",
        "version": version or "",
        "tags": args.tags,
        "ready_for_review": ready,
        "findings": findings,
        "publish_command": publish_command,
        "next_steps": next_steps,
    }

    if args.json:
        json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
        print("")
        return 0

    print(f"ClawHub Publish Check: {skill_path.name}")
    print(f"Path: {skill_path}")
    print(f"Ready for review: {'yes' if ready else 'no'}")
    print("")
    print("Findings:")
    if findings:
        for item in findings:
            print(f"- [{item['severity']}] {item['message']}")
    else:
        print("- No blocking local issues found.")
    print("")
    print("Publish command:")
    if publish_command:
        print(publish_command)
    else:
        print("- Provide --display-name and --version to generate the exact publish command.")
    print("")
    print("Next steps:")
    if next_steps:
        for item in next_steps:
            print(f"- {item}")
    else:
        print("- No additional local steps suggested.")

    return 0 if ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
