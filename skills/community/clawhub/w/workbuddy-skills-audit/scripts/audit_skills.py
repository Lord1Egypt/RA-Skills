#!/usr/bin/env python3
"""skills-audit: Scan installed skills, compare against golden list, generate report.

Usage:
    python scripts/audit_skills.py [--dir SKILLS_DIR] [--golden GOLDEN_PATH]

Options:
    --dir SKILLS_DIR      Path to skills directory (default: ~/.workbuddy/skills/)
    --golden GOLDEN_PATH  Path to golden list reference (default: references/golden-list.md)
    --output OUTPUT_PATH  Report output path (default: skills-audit-YYYY-MM.md)
"""

import os
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path

PLATFORM_PATTERNS = {
    "Clawdbot": r"clawdbot(?:\.json)?|clawdhub",
    "Moltbot": r"moltbot(?:\.json)?",
    "OpenClaw": r"openclaw|opencli|clawhub",
    "CodeConductor": r"CodeConductor\.ai|codeconductor\.ai",
}


def parse_frontmatter(text):
    """Parse YAML frontmatter from SKILL.md content."""
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        m = re.match(r"^(\w+):\s*(.*)", line)
        if m:
            key = m.group(1).strip()
            value = m.group(2).strip().strip('"').strip("'")
            fm[key] = value
    return fm


def read_golden_list(path):
    """Parse golden-list.md and return set of approved skill directory names."""
    text = Path(path).read_text(encoding="utf-8")
    approved = set()
    # Parse inline-code entries: `name`
    for m in re.finditer(r"`([a-z][a-z0-9_-]+)`", text):
        approved.add(m.group(1).lower())
    # Parse code blocks (the ``` section listing names)
    for m in re.finditer(r"```\s*\n(.*?)\n```", text, re.DOTALL):
        for line in m.group(1).strip().split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                approved.add(line.lower())
    return approved


def scan_skills(skills_dir):
    """Scan the skills directory and parse all SKILL.md files."""
    skills = []
    skill_dirs = sorted(Path(skills_dir).iterdir())
    for d in skill_dirs:
        if not d.is_dir():
            continue
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            continue
        content = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        name = fm.get("name", d.name)
        desc = fm.get("description", "")
        skills.append({
            "name": name,
            "dir": d.name,
            "path": str(skill_md),
            "description": desc,
        })
    return skills


def classify_skill(skill, approved):
    """Classify a skill as approved, platform-specific, or unknown."""
    name_lower = skill["name"].lower()
    dir_lower = skill["dir"].lower()

    if name_lower in approved or dir_lower in approved:
        return "approved"

    content = skill["path"]
    try:
        text = Path(content).read_text(encoding="utf-8")
    except Exception:
        text = ""

    for platform, pattern in PLATFORM_PATTERNS.items():
        if re.search(pattern, text, re.IGNORECASE):
            return f"platform:{platform}"

    return "unknown"


def generate_report(skills, approved, output_path):
    """Generate a Markdown audit report."""
    lines = []
    lines.append(f"# Skills Audit Report — {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("")
    lines.append(f"**Total installed skills:** {len(skills)}")
    lines.append("")

    approved_count = 0
    unknown_skills = []
    platform_skills = []
    duplicate_groups = []

    for s in skills:
        classification = classify_skill(s, approved)
        if classification == "approved":
            approved_count += 1
        elif classification.startswith("platform:"):
            platform_skills.append((s, classification.split(":", 1)[1]))
        else:
            unknown_skills.append(s)

    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Category | Count |")
    lines.append(f"|----------|-------|")
    lines.append(f"| Approved | {approved_count} |")
    lines.append(f"| Unknown (review needed) | {len(unknown_skills)} |")
    lines.append(f"| Platform-specific (removable) | {len(platform_skills)} |")
    lines.append(f"| **Total** | **{len(skills)}** |")
    lines.append("")

    if platform_skills:
        lines.append("## Platform-Specific Skills (Candidates for Removal)")
        lines.append("")
        lines.append("| Skill | Directory | Platform |")
        lines.append("|-------|-----------|----------|")
        for s, platform in platform_skills:
            lines.append(f"| {s['name']} | `{s['dir']}` | {platform} |")
        lines.append("")

    if unknown_skills:
        lines.append("## Unknown Skills (Requires Manual Review)")
        lines.append("")
        lines.append("| Skill | Directory | Description |")
        lines.append("|-------|-----------|-------------|")
        for s in unknown_skills:
            desc_short = s["description"][:80] if s["description"] else "*no description*"
            lines.append(f"| {s['name']} | `{s['dir']}` | {desc_short} |")
        lines.append("")

    lines.append("## Full Skill List")
    lines.append("")
    lines.append("| # | Skill | Directory | Status |")
    lines.append("|---|-------|-----------|--------|")
    for i, s in enumerate(skills, 1):
        classification = classify_skill(s, approved)
        status_map = {
            "approved": "✅ Approved",
            "unknown": "⚠️  Review",
        }
        if classification.startswith("platform:"):
            status_map[classification] = f"❌ Platform: {classification.split(':', 1)[1]}"
        status = status_map.get(classification, classification)
        status = status.replace("\u2705", "[OK]").replace("\u26a0\ufe0f", "[!]").replace("\u274c", "[X]")
        lines.append(f"| {i} | {s['name']} | `{s['dir']}` | {status} |")
    lines.append("")

    lines.append("---")
    lines.append(f"*Generated by skills-audit on {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append("")

    output = "\n".join(lines)
    output_path.write_text(output, encoding="utf-8")
    return output


def main():
    parser = argparse.ArgumentParser(description="Audit installed skills against golden list")
    parser.add_argument("--dir", default=str(Path.home() / ".workbuddy" / "skills"),
                        help="Path to skills directory")
    parser.add_argument("--golden", default=None,
                        help="Path to golden list reference file")
    parser.add_argument("--output", default=None,
                        help="Report output path")
    args = parser.parse_args()

    skills_dir = Path(args.dir)
    if not skills_dir.exists():
        print(f"Error: Skills directory not found: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    # Resolve golden list path
    if args.golden:
        golden_path = Path(args.golden)
    else:
        golden_path = Path(__file__).parent.parent / "references" / "golden-list.md"

    if not golden_path.exists():
        print(f"Warning: Golden list not found at {golden_path}, using empty list", file=sys.stderr)
        approved = set()
    else:
        approved = read_golden_list(golden_path)

    # Resolve output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path.cwd() / f"skills-audit-{datetime.now().strftime('%Y-%m')}.md"

    skills = scan_skills(skills_dir)
    report = generate_report(skills, approved, output_path)
    print(report)


if __name__ == "__main__":
    main()
