#!/usr/bin/env python3
"""Publish or update a skill on ClawHub with version bumping and changelog."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


def run_cmd(cmd: list[str], timeout: int = 30) -> tuple[int, str, str]:
    """Run a shell command."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return 1, "", f"Command not found: {cmd[0]}"


def parse_frontmatter(skill_path: Path) -> Optional[dict]:
    """Parse YAML frontmatter from SKILL.md."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None

    frontmatter_text = match.group(1)
    data = {}
    for line in frontmatter_text.split("\n"):
        top_match = re.match(r"^(\w+):\s*(.*)$", line)
        if top_match:
            key, value = top_match.groups()
            value = value.strip()
            if value:
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                data[key] = value
            else:
                data[key] = {}
    return data


def update_version(skill_path: Path, new_version: str) -> bool:
    """Update version in SKILL.md frontmatter."""
    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8")

    # Replace version line
    new_content = re.sub(
        r"^(version:\s*)[\d\.]+",
        rf"\g<1>{new_version}",
        content,
        flags=re.MULTILINE
    )

    if new_content == content:
        return False

    skill_md.write_text(new_content, encoding="utf-8")
    return True


def bump_version(version: str, bump_type: str = "patch") -> str:
    """Bump semver version."""
    parts = version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        return f"{major + 1}.0.0"
    elif bump_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:
        return f"{major}.{minor}.{patch + 1}"


def get_git_changelog(skill_path: Path) -> str:
    """Generate changelog from recent git commits."""
    rc, stdout, _ = run_cmd(
        ["git", "-C", str(skill_path), "log", "--oneline", "-5"],
        timeout=5
    )
    if rc == 0 and stdout.strip():
        commits = [line.strip() for line in stdout.strip().split("\n") if line.strip()]
        if commits:
            # Extract just the message part (after hash)
            messages = []
            for c in commits:
                parts = c.split(" ", 1)
                if len(parts) > 1:
                    messages.append(parts[1])
            if messages:
                return "; ".join(messages[:3])
    return ""


def get_current_published_version(slug: str) -> Optional[str]:
    """Get currently published version from clawhub."""
    rc, stdout, _ = run_cmd(["clawhub", "inspect", "--json", slug], timeout=10)
    if rc == 0:
        try:
            data = json.loads(stdout)
            return data.get("latestVersion", {}).get("version")
        except json.JSONDecodeError:
            pass
    return None


def publish_skill(skill_path: Path, slug: str, version: str, changelog: str) -> bool:
    """Publish skill to ClawHub."""
    cmd = [
        "clawhub", "publish", str(skill_path),
        "--slug", slug,
        "--version", version,
        "--changelog", changelog,
    ]

    print(f"\nRunning: clawhub publish {slug}@{version}")
    rc, stdout, stderr = run_cmd(cmd, timeout=60)

    if rc == 0:
        print(f"✓ {stdout.strip()}")
        return True
    else:
        print(f"✗ Failed: {stderr.strip()}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Publish or update skill on ClawHub")
    parser.add_argument("--path", "-p", type=str, default=".", help="Skill directory path")
    parser.add_argument("--slug", "-s", type=str, help="Skill slug (default: read from SKILL.md)")
    parser.add_argument("--version", "-v", type=str, help="Version to publish (auto-bump if omitted)")
    parser.add_argument("--changelog", "-c", type=str, help="Changelog text")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], default="patch",
                        help="Version bump type when --version not specified")
    parser.add_argument("--dry-run", action="store_true", help="Preview without publishing")
    args = parser.parse_args()

    skill_path = Path(args.path)

    # Parse frontmatter
    frontmatter = parse_frontmatter(skill_path)
    if not frontmatter:
        print("✗ Could not parse SKILL.md frontmatter")
        return 1

    slug = args.slug or frontmatter.get("name")
    if not slug:
        print("✗ No slug provided and no 'name' in frontmatter")
        return 1

    current_version = frontmatter.get("version", "0.0.0")

    # Determine version
    if args.version:
        new_version = args.version
    else:
        # Check published version
        published_version = get_current_published_version(slug)
        if published_version:
            base_version = published_version
            print(f"Current published version: {base_version}")
        else:
            base_version = current_version
            print(f"Not yet published. Current version in SKILL.md: {base_version}")

        new_version = bump_version(base_version, args.bump)
        print(f"Suggested new version: {new_version}")

    # Generate changelog if not provided
    changelog = args.changelog
    if not changelog:
        git_log = get_git_changelog(skill_path)
        if git_log:
            changelog = git_log
        else:
            changelog = f"Update to version {new_version}"
        print(f"Auto-generated changelog: {changelog}")

    if args.dry_run:
        print(f"\n[DRY RUN] Would publish {slug}@{new_version}")
        print(f"  Path: {skill_path}")
        print(f"  Changelog: {changelog}")
        return 0

    # Update version in SKILL.md
    if update_version(skill_path, new_version):
        print(f"✓ Updated SKILL.md version to {new_version}")

    # Publish
    if publish_skill(skill_path, slug, new_version, changelog):
        print(f"\n✓ Published successfully!")
        print(f"  Link: https://clawhub.ai/skills/{slug}")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
