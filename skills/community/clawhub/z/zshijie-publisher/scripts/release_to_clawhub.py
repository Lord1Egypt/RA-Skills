#!/usr/bin/env python3

import argparse
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]+$")


def parse_frontmatter_value(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{key}:\s*(.+)$", frontmatter, re.MULTILINE)
    if not match:
        raise SystemExit(f"[ERROR] SKILL.md frontmatter is missing '{key}'.")
    return match.group(1).strip().strip("\"'")


def validate_skill_dir(skill_dir: Path) -> None:
    skill_md = skill_dir / "SKILL.md"
    agents_yaml = skill_dir / "agents" / "openai.yaml"

    if not skill_dir.exists() or not skill_dir.is_dir():
        raise SystemExit(f"[ERROR] Skill directory not found: {skill_dir}")
    if not skill_md.exists():
        raise SystemExit(f"[ERROR] Missing SKILL.md: {skill_md}")
    if not agents_yaml.exists():
        raise SystemExit(f"[ERROR] Missing agents/openai.yaml: {agents_yaml}")

    content = skill_md.read_text()
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        raise SystemExit("[ERROR] SKILL.md must start with YAML frontmatter.")
    frontmatter = match.group(1)
    name = parse_frontmatter_value(frontmatter, "name")
    description = parse_frontmatter_value(frontmatter, "description")

    if not NAME_RE.match(name) or name.startswith("-") or name.endswith("-") or "--" in name:
        raise SystemExit(f"[ERROR] Invalid skill name in frontmatter: {name}")
    if not description or len(description) > 1024:
        raise SystemExit("[ERROR] Skill description must be present and under 1024 characters.")


def build_publish_command(skill_dir: Path) -> list[str]:
    return ["clawhub", "publish", str(skill_dir.resolve())]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a skill folder and print or run the ClawHub publish command.",
    )
    parser.add_argument(
        "skill_dir",
        nargs="?",
        default=".",
        help="Path to the skill directory. Defaults to the current directory.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run the publish command instead of only printing it.",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).resolve()
    validate_skill_dir(skill_dir)
    command = build_publish_command(skill_dir)

    print(f"[OK] Skill directory looks publishable: {skill_dir}")
    print("[INFO] Next command:")
    print(shlex.join(command))
    if shutil.which("clawhub") is None:
        print("[INFO] 'clawhub' is not on PATH in this environment. Install or expose it before using --execute.")

    if not args.execute:
        return 0

    if shutil.which("clawhub") is None:
        raise SystemExit("[ERROR] 'clawhub' is not installed or not on PATH.")

    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
