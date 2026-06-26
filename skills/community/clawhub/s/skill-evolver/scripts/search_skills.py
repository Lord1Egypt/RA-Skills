#!/usr/bin/env python3
"""
Search skills based on intent analysis.
Outputs a markdown document with matching candidates.
"""
import argparse
import re
from pathlib import Path
from typing import Dict, List


def parse_intent(md_path: str) -> Dict:
    """Extract capabilities from intent markdown."""
    content = Path(md_path).read_text(encoding="utf-8")

    capabilities = []
    constraints = []

    # Extract capabilities
    cap_section = re.search(r"## Capabilities Required\s*(.+?)(?=##|$)", content, re.DOTALL)
    if cap_section:
        for line in cap_section.group(1).strip().split("\n"):
            match = re.match(r"-\s*(\w+)", line.strip())
            if match:
                capabilities.append(match.group(1))

    # Extract constraints
    const_section = re.search(r"## Constraints\s*(.+?)(?=##|$)", content, re.DOTALL)
    if const_section:
        for line in const_section.group(1).strip().split("\n"):
            match = re.match(r"-\s*(.+)", line.strip())
            if match:
                constraints.append(match.group(1))

    return {"capabilities": capabilities, "constraints": constraints}


def discover_skills(skills_dirs: List[Path]) -> List[Dict]:
    """Discover all skills from directories."""
    skills = []

    for skills_dir in skills_dirs:
        if not skills_dir.exists():
            continue

        for skill_path in skills_dir.iterdir():
            if not skill_path.is_dir():
                continue

            skill_md = skill_path / "SKILL.md"
            if not skill_md.exists():
                continue

            try:
                content = skill_md.read_text(encoding="utf-8")
                frontmatter = parse_frontmatter(content)

                skills.append({
                    "name": skill_path.name,
                    "path": str(skill_path),
                    "description": frontmatter.get("description", ""),
                    "source": str(skills_dir)
                })
            except Exception:
                continue

    return skills


def parse_frontmatter(content: str) -> Dict:
    """Parse YAML frontmatter from SKILL.md."""
    match = re.match(r"^---\s*\n(.+?)\n---", content, re.DOTALL)
    if not match:
        return {}

    fm_text = match.group(1)
    result = {}

    # Simple YAML parsing for name and description
    name_match = re.search(r"^name:\s*(.+)$", fm_text, re.MULTILINE)
    if name_match:
        result["name"] = name_match.group(1).strip()

    desc_match = re.search(r"^description:\s*\|?\s*(.+?)(?=^\w+:|$)", fm_text, re.MULTILINE | re.DOTALL)
    if desc_match:
        desc = desc_match.group(1).strip()
        # Clean up multi-line description
        desc = re.sub(r"\s+", " ", desc)
        result["description"] = desc

    return result


def extract_capabilities_from_description(description: str) -> List[str]:
    """Infer capabilities from skill description."""
    keywords = [
        "pdf", "excel", "docx", "pptx", "image", "video", "audio",
        "translate", "summarize", "analyze", "extract", "convert",
        "code", "deploy", "test", "search", "web", "api",
        "chart", "graph", "table", "data", "text"
    ]

    found = []
    desc_lower = description.lower()
    for kw in keywords:
        if kw in desc_lower:
            found.append(kw)

    return found


def match_skills(skills: List[Dict], required_caps: List[str]) -> List[Dict]:
    """Match skills against required capabilities."""
    matched = []

    for skill in skills:
        desc = skill.get("description", "").lower()
        skill_caps = extract_capabilities_from_description(desc)

        # Calculate overlap
        required_lower = [c.lower().replace("_", "") for c in required_caps]
        skill_caps_lower = [c.lower() for c in skill_caps]

        overlap = []
        for req in required_lower:
            for cap in skill_caps_lower:
                if req in cap or cap in req:
                    overlap.append(req)
                    break

        score = len(overlap) / max(1, len(required_lower)) if required_lower else 0

        if score > 0:
            matched.append({
                **skill,
                "matched_capabilities": overlap,
                "score": round(score, 2)
            })

    # Sort by score
    matched.sort(key=lambda x: x["score"], reverse=True)
    return matched


def generate_output(skills: List[Dict], required_caps: List[str], output_path: Path) -> None:
    """Generate markdown output."""
    lines = [
        "# Skill Candidates",
        "",
        "## Required Capabilities",
    ]

    for cap in required_caps:
        lines.append(f"- {cap}")

    lines.extend(["", "## Results", ""])

    if not skills:
        lines.append("No matching skills found.")
        lines.append("")
        lines.append("Consider:")
        lines.append("- Using native Claude abilities")
        lines.append("- Searching with different keywords")
        lines.append("- Creating a new skill")
    else:
        for i, skill in enumerate(skills[:10], 1):
            lines.append(f"### {i}. {skill['name']}")
            lines.append(f"- **Path**: `{skill['path']}`")
            lines.append(f"- **Score**: {skill['score']}")
            lines.append(f"- **Matched**: {', '.join(skill['matched_capabilities']) or 'keyword match'}")
            lines.append(f"- **Description**: {skill['description'][:200]}..." if len(skill['description']) > 200 else f"- **Description**: {skill['description']}")
            lines.append("")

        # Gap analysis
        all_matched = set()
        for skill in skills:
            all_matched.update(skill['matched_capabilities'])

        missing = [c for c in required_caps if c.lower().replace("_", "") not in all_matched]

        lines.extend(["## Gap Analysis", ""])
        if missing:
            lines.append("### Missing Capabilities")
            for m in missing:
                lines.append(f"- {m}")
            lines.append("")
            lines.append("Consider: native handling or creating a new skill")
        else:
            lines.append("All required capabilities are covered by candidates.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Search skills based on intent")
    parser.add_argument("--intent", required=True, help="Path to 01-intent.md")
    parser.add_argument("--output", required=True, help="Output path for 02-candidates.md")
    parser.add_argument("--skills-dir", action="append", default=[],
                        help="Skills directory (can specify multiple)")
    args = parser.parse_args()

    # Parse intent
    intent = parse_intent(args.intent)

    # Default skills directories
    skills_dirs = []
    if args.skills_dir:
        skills_dirs.extend([Path(d) for d in args.skills_dir])
    else:
        skills_dirs = [
            Path.home() / ".claude" / "skills",
            Path.cwd() / "skills",
        ]

    # Discover and match
    all_skills = discover_skills(skills_dirs)
    matched = match_skills(all_skills, intent["capabilities"])

    # Generate output
    generate_output(matched, intent["capabilities"], Path(args.output))
    print(f"Found {len(matched)} candidates. Output: {args.output}")


if __name__ == "__main__":
    main()
