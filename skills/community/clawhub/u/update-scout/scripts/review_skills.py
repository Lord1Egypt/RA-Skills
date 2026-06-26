#!/usr/bin/env python3
"""
scout - review_skills.py
Reviews installed OpenClaw skills against structural best practices and suggests improvements.

Usage:
  python3 review_skills.py [--skills-dir /path/to/skills] [--json]

What it does:
  1. Finds all skills in the skills directory (any folder with a SKILL.md)
  2. Optionally fetches the latest OpenClaw skill-creator guidelines for context
  3. Runs each skill through a set of structural checks
  4. Outputs a health report with specific, actionable suggestions

Note: This script performs static structural checks (frontmatter, body length, script
references, etc.). It does not use AI to evaluate skill quality — the agent reviewing
the output is responsible for that judgment.

Set GITHUB_TOKEN env var for higher API rate limits (your own token, never stored).
"""

import json
import os
import re
import sys
import argparse
from pathlib import Path
from typing import Optional

from scout_config import github_request

# Optional: fetch latest skill-creator SKILL.md for context when presenting findings
SKILL_CREATOR_RAW_URL = (
    "https://raw.githubusercontent.com/openclaw/openclaw/main/"
    "skills/skill-creator/SKILL.md"
)


def fetch_best_practices() -> Optional[str]:
    """Fetch the OpenClaw skill-creator best practices doc for agent context.
    Returns the content string or None if unavailable. Not used for checks —
    the agent can reference it when explaining suggestions."""
    try:
        import urllib.request
        headers = {"User-Agent": "scout-skill/1.0"}
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        req = urllib.request.Request(SKILL_CREATOR_RAW_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode("utf-8")
    except Exception:
        return None


def find_skills(skills_dir: str) -> list:
    """Find all skill directories (folders containing SKILL.md)."""
    base = Path(skills_dir)
    if not base.exists():
        return []
    return sorted(
        p for p in base.iterdir()
        if p.is_dir() and not p.is_symlink() and (p / "SKILL.md").exists()
    )


def parse_frontmatter(content: str) -> dict:
    """Extract key/value pairs from YAML frontmatter. Handles simple string values only."""
    result = {}
    if not content.startswith("---"):
        return result
    end = content.find("\n---", 3)
    if end == -1:
        return result
    for line in content[3:end].strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            result[key.strip()] = val.strip().strip('"').strip("'")
    return result


def extract_body(content: str) -> str:
    """Extract everything after the frontmatter block."""
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            return content[end + 4:].strip()
    return content.strip()


def filename_referenced(filename: str, body: str) -> bool:
    """Check if a script filename appears in the body (as a standalone token or path component)."""
    # Match filename as a complete token — allows leading path separators like scripts/
    # but not as a substring of another filename (e.g. 'config.py' != 'scout_config.py')
    pattern = re.compile(r'(?:^|[\s/`\'"])' + re.escape(filename) + r'(?:$|[\s`\'"\)])', re.MULTILINE)
    return bool(pattern.search(body))


def check_skill(skill_path: Path) -> dict:
    """Run structural health checks on a single skill directory."""
    skill_md_path = skill_path / "SKILL.md"

    try:
        content = skill_md_path.read_text(encoding="utf-8")
    except Exception as e:
        return {
            "name": skill_path.name,
            "path": str(skill_path),
            "issues": [f"Could not read SKILL.md: {e}"],
            "suggestions": [],
            "healthy": False,
        }

    fm = parse_frontmatter(content)
    body = extract_body(content)
    name = fm.get("name", "")
    description = fm.get("description", "")

    issues = []
    suggestions = []

    # Frontmatter checks
    if not name:
        issues.append("Missing `name` in frontmatter")

    if not description:
        issues.append("Missing `description` in frontmatter")
    else:
        if len(description) < 80:
            suggestions.append("Description is short — expand to clearly describe when to use this skill")
        if len(description) > 600:
            suggestions.append("Description may be too long for skill card display — aim for under 400 chars for the lead sentence")
        # Check if description clearly states when to use the skill
        has_when = any(kw in description.lower() for kw in ("use when", "when to use", "when:"))
        if not has_when:
            suggestions.append("Description doesn't state when to use this skill — add 'Use when...' guidance")
        # Check if it leads with user value vs. agent-trigger boilerplate
        tech_starts = ["this skill", "provides", "handles", "manages", "wraps"]
        if any(description.lower().startswith(s) for s in tech_starts):
            suggestions.append("Description leads with technical framing — consider leading with user value (what problem it solves)")

    # Body checks
    if not body or len(body) < 100:
        issues.append("SKILL.md body is empty or very short — add workflow instructions")
    if len(body.splitlines()) > 500:
        suggestions.append("SKILL.md body exceeds 500 lines — consider moving detail to references/ files")

    # Script reference checks — only check scripts meant to be run directly
    scripts_dir = skill_path / "scripts"
    if scripts_dir.exists():
        # Glob without following symlinks
        all_scripts = [
            f for f in scripts_dir.iterdir()
            if f.is_file() and not f.is_symlink()
            and f.suffix in (".py", ".sh", ".bash")
        ]
        # Filter known internal modules (named *_config.py or starting with _)
        runnable = [
            f for f in all_scripts
            if not f.name.startswith("_")
            and not f.name.endswith("_config.py")
            and not f.name.startswith("test_")
        ]
        if runnable:
            unreferenced = [f.name for f in runnable if not filename_referenced(f.name, body)]
            if len(unreferenced) == len(runnable):
                suggestions.append("Scripts exist in scripts/ but none are referenced in SKILL.md — add usage examples")
            elif unreferenced:
                suggestions.append(f"Some scripts not referenced in SKILL.md: {', '.join(unreferenced)}")

    # Extraneous file check
    bad = [
        str(f.relative_to(skill_path)) for f in skill_path.rglob("*")
        if f.is_file() and not f.is_symlink()
        and f.name.lower() in ("readme.md", "changelog.md", "installation.md", "quick_reference.md")
    ]
    if bad:
        issues.append(f"Extraneous documentation files found (per skill spec, remove these): {', '.join(bad)}")

    return {
        "name": name or skill_path.name,
        "path": str(skill_path),
        "issues": issues,
        "suggestions": suggestions,
        "healthy": len(issues) == 0,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Review OpenClaw skills against structural best practices"
    )
    parser.add_argument(
        "--skills-dir",
        default=os.path.expanduser("~/.openclaw/workspace/skills"),
        help="Path to skills directory"
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Fetch best practices doc for agent context — not used for automated checks
    best_practices = fetch_best_practices()
    bp_status = "✅ Available" if best_practices else "⚠️  Unavailable (check GITHUB_TOKEN or network)"

    skills = find_skills(args.skills_dir)
    if not skills:
        if args.json:
            print(json.dumps({"error": f"No skills found in {args.skills_dir}"}))
        else:
            print(f"No skills found in {args.skills_dir}")
        sys.exit(1)

    results = [check_skill(p) for p in skills]

    if args.json:
        out = {
            "skills_dir": args.skills_dir,
            "best_practices_source": SKILL_CREATOR_RAW_URL,
            "best_practices_status": bp_status,
            # Include fetched content so agent can reference it when explaining suggestions
            "best_practices_content": best_practices,
            "skill_count": len(results),
            "results": results,
        }
        print(json.dumps(out, indent=2))
        return

    healthy = [r for r in results if r["healthy"] and not r["suggestions"]]
    needs_attention = [r for r in results if r["issues"] or r["suggestions"]]

    print("=== Scout Skill Health Report ===\n")
    print(f"Best practices reference: {SKILL_CREATOR_RAW_URL}")
    print(f"Status: {bp_status}")
    print(f"Skills checked: {len(results)}")
    print("Note: Checks are structural only. Agent review required for quality assessment.\n")

    if needs_attention:
        for r in needs_attention:
            marker = "❌" if r["issues"] else "💡"
            print(f"{marker} {r['name']}  ({r['path']})")
            for issue in r["issues"]:
                print(f"   ❌ {issue}")
            for suggestion in r["suggestions"]:
                print(f"   💡 {suggestion}")
            print()

    if healthy:
        print(f"✅ Healthy: {', '.join(r['name'] for r in healthy)}")

    print("\nReview complete. All changes require explicit approval before applying.")


if __name__ == "__main__":
    main()
