#!/usr/bin/env python3
"""Check ClawHub publish readiness: CLI, auth, and skill format."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Optional


def run_cmd(cmd: list[str], timeout: int = 10) -> tuple[int, str, str]:
    """Run a shell command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return 1, "", f"Command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"


def check_cli() -> tuple[bool, str]:
    """Check if clawhub CLI is installed."""
    rc, stdout, stderr = run_cmd(["clawhub", "-V"])
    if rc == 0:
        version = stdout.strip() or "installed"
        return True, f"clawhub CLI: {version}"
    return False, "clawhub CLI not found. Install: npm i -g clawhub"


def check_auth() -> tuple[bool, str]:
    """Check if user is logged in to clawhub."""
    rc, stdout, stderr = run_cmd(["clawhub", "whoami"])
    if rc == 0:
        # whoami output: "- Checking token\n✔ casperkwok" (stdout may have spinner text)
        combined = (stdout + stderr).strip()
        # Extract last non-empty line after any spinner/progress text
        lines = [l.strip() for l in combined.split("\n") if l.strip() and not l.startswith("-")]
        user = lines[-1].lstrip("✔ ").strip() if lines else "unknown"
        return True, f"Logged in as: {user}"
    return False, "Not logged in. Run: clawhub login"


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
    # Simple YAML parsing: extract top-level keys (name, description, version, metadata)
    data = {}
    for line in frontmatter_text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Only capture top-level keys (no leading spaces)
        if not line.startswith(" ") and not line.startswith("\t"):
            top_match = re.match(r"^(\w+):\s*(.*)$", stripped)
            if top_match:
                key, value = top_match.groups()
                value = value.strip()
                if value and value not in ("{}", ""):
                    # Remove quotes
                    if (value.startswith('"') and value.endswith('"')) or \
                       (value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]
                    data[key] = value
                else:
                    data[key] = ""
    return data


def check_skill_format(skill_path: Path) -> tuple[bool, list[str]]:
    """Check if skill directory meets ClawHub requirements."""
    errors = []
    warnings = []

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md not found")
        return False, errors + warnings

    # Parse frontmatter
    frontmatter = parse_frontmatter(skill_path)
    if not frontmatter:
        errors.append("SKILL.md missing YAML frontmatter")
        return False, errors + warnings

    # Check required fields
    required_fields = ["name", "description", "version"]
    for field in required_fields:
        if field not in frontmatter or not frontmatter[field]:
            errors.append(f"SKILL.md frontmatter missing: {field}")

    # Check description quality
    desc = frontmatter.get("description", "")
    if len(desc) < 20:
        warnings.append(f"description is short ({len(desc)} chars), should be > 20")

    # Check version format
    version = frontmatter.get("version", "")
    if version and not re.match(r"^\d+\.\d+\.\d+$", version):
        warnings.append(f"version '{version}' should follow semver (x.y.z)")

    # Check metadata (recommended)
    if "metadata" not in frontmatter:
        warnings.append("metadata.openclaw.requires recommended for declaring runtime deps")

    return len(errors) == 0, errors + warnings


def check_slug_available(slug: str) -> tuple[bool, str]:
    """Check if a skill slug is already published."""
    rc, stdout, stderr = run_cmd(["clawhub", "inspect", slug])
    if rc == 0:
        return False, f"Slug '{slug}' already published. Use update instead."
    return True, f"Slug '{slug}' is available"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check ClawHub publish readiness")
    parser.add_argument("--path", "-p", type=str, default=".", help="Skill directory path")
    parser.add_argument("--slug", "-s", type=str, help="Check if slug is available")
    args = parser.parse_args()

    skill_path = Path(args.path)
    all_ok = True

    print("=" * 50)
    print("ClawHub Publish Readiness Check")
    print("=" * 50)

    # 1. CLI
    print("\n[1/4] Checking clawhub CLI...")
    ok, msg = check_cli()
    print(f"  {'✓' if ok else '✗'} {msg}")
    all_ok = all_ok and ok

    # 2. Auth
    print("\n[2/4] Checking authentication...")
    ok, msg = check_auth()
    print(f"  {'✓' if ok else '✗'} {msg}")
    all_ok = all_ok and ok

    # 3. Skill format
    print("\n[3/4] Checking skill format...")
    ok, issues = check_skill_format(skill_path)
    for issue in issues:
        is_error = "not found" in issue.lower() or "missing" in issue.lower()
        prefix = "  ✗" if is_error else "  !"
        print(f"{prefix} {issue}")
    if not issues:
        print("  ✓ SKILL.md format valid")
    all_ok = all_ok and ok

    # 4. Slug availability
    if args.slug:
        print(f"\n[4/4] Checking slug '{args.slug}'...")
        ok, msg = check_slug_available(args.slug)
        print(f"  {'✓' if ok else '✗'} {msg}")
        all_ok = all_ok and ok

    print("\n" + "=" * 50)
    if all_ok:
        print("✓ All checks passed! Ready to publish.")
    else:
        print("✗ Some checks failed. Fix the issues above before publishing.")
    print("=" * 50)

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
