#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


GENERIC_TRIGGER_WORDS = {
    "workflow", "support", "helper", "guidance", "task", "tasks", "output",
    "notes", "reusable", "structure", "process", "repeatable",
}

ALLOWED_FRONTMATTER = {"name", "description", "version", "license", "author"}


EXTRANEOUS_DOCS = {
    "readme.md",
    "readme.rst",
    "readme.txt",
    "install.md",
    "installation.md",
    "installation_guide.md",
    "setup.md",
    "usage.md",
    "quick_reference.md",
    "quickstart.md",
    "changelog.md",
    "changes.md",
    "history.md",
    "contributing.md",
}

PROFILE_KEYWORDS = {
    "academic": {
        "citation", "bibliography", "reference", "apa", "mla", "harvard",
        "chicago", "essay", "paper", "assignment", "source metadata",
    },
    "product": {
        "prd", "mvp", "roadmap", "acceptance criteria", "user story",
        "requirements", "dev handoff", "competitive",
    },
    "integration": {
        "api", "oauth", "webhook", "token", "credential", "telegram",
        "notion", "connector", "health check",
    },
    "script": {
        "script", "cli", "batch", "parse", "validate", "export",
        "convert", "exit code", "dry-run",
    },
}


def parse_frontmatter(content: str) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
    return result


def count_numbered_steps(content: str) -> int:
    return len(re.findall(r"(?m)^\d+\.\s+\S+", content))


def section_text(content: str, title: str) -> str:
    match = re.search(
        rf"(?ms)^##\s+{re.escape(title)}\s*\n(.*?)(?=^##\s+|\Z)",
        content,
    )
    return match.group(1).strip() if match else ""


def extract_trigger_cues(content: str) -> list[str]:
    section = section_text(content, "Trigger Cues")
    triggers = []
    for line in section.splitlines():
        match = re.match(r"\s*-\s+`?([^`\n]+?)`?\s*$", line)
        if match:
            triggers.append(match.group(1).strip())
    return triggers


def is_specific_trigger(trigger: str) -> bool:
    normalized = trigger.strip().lower()
    if not normalized or normalized in GENERIC_TRIGGER_WORDS:
        return False
    if len(normalized) >= 12:
        return True
    if " " in normalized or "-" in normalized:
        return True
    return normalized not in GENERIC_TRIGGER_WORDS and len(normalized) >= 4


def infer_profile(content: str, references: list[Path]) -> str:
    reference_text = " ".join(path.name for path in references)
    text = f"{content} {reference_text}".lower()
    scores = {
        profile: sum(1 for keyword in keywords if keyword in text)
        for profile, keywords in PROFILE_KEYWORDS.items()
    }
    profile, score = max(scores.items(), key=lambda item: item[1])
    return profile if score >= 2 else "workflow"


def has_any(text: str, terms: list[str]) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def contains_unresolved_placeholder(text: str) -> bool:
    lowered = text.lower()
    patterns = [
        r"\btodo\b",
        r"replace this placeholder",
        r"implement skill-specific logic",
        r"\blorem ipsum\b",
        r"\byour value here\b",
        r"\btbd\b",
    ]
    return any(re.search(pattern, lowered) for pattern in patterns)


def quality_report(skill_dir: Path) -> dict:
    errors = []
    warnings = []
    milestone_caps = []
    score = 0

    skill_md = skill_dir / "SKILL.md"
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    references = sorted((skill_dir / "references").glob("*")) if (skill_dir / "references").exists() else []
    scripts = sorted((skill_dir / "scripts").rglob("*.py")) if (skill_dir / "scripts").exists() else []
    extraneous_docs = sorted(path.name for path in skill_dir.iterdir() if path.is_file() and path.name.lower() in EXTRANEOUS_DOCS) if skill_dir.exists() else []

    if not skill_md.exists():
        return {
            "valid": False,
            "score": 0,
            "grade": "invalid",
            "errors": ["SKILL.md not found"],
            "warnings": warnings,
        }

    content = skill_md.read_text(encoding="utf-8", errors="ignore")
    frontmatter = parse_frontmatter(content)
    triggers = extract_trigger_cues(content)
    specific_triggers = [trigger for trigger in triggers if is_specific_trigger(trigger)]
    reference_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore") for path in references
    )
    combined_text = f"{content}\n{reference_text}"
    inferred_profile = infer_profile(content, references)
    line_count = len(content.splitlines())

    if extraneous_docs:
        errors.append(
            "skill package contains user-facing project docs that bloat agent context: "
            + ", ".join(extraneous_docs)
        )

    unexpected_frontmatter = sorted(set(frontmatter) - ALLOWED_FRONTMATTER)
    if unexpected_frontmatter:
        warnings.append(
            "frontmatter should only contain name, description, version, license, or author for reliable triggering: "
            + ", ".join(unexpected_frontmatter)
        )
        milestone_caps.append(89)

    if line_count <= 500:
        score += 5
    else:
        warnings.append("SKILL.md should stay under 500 lines; move details into references")
        milestone_caps.append(84)

    if frontmatter.get("name") and re.match(r"^[a-z0-9-]+$", frontmatter["name"]):
        score += 10
    else:
        errors.append("frontmatter name is missing or not hyphen-case")

    description = frontmatter.get("description", "")
    if 80 <= len(description) <= 1024 and "Use when" in description:
        score += 15
    else:
        warnings.append("description should be specific, include trigger conditions, and be 80-1024 chars")
    if any(generic in description.lower() for generic in ["workflow guidance", "use the skill workflow"]):
        warnings.append("description is too generic for reliable triggering")
        milestone_caps.append(84)

    required_sections = ["Trigger Cues", "Output Contract", "Quality Gates", "Resources"]
    present_sections = [section for section in required_sections if f"## {section}" in content]
    score += len(present_sections) * 6
    missing_sections = sorted(set(required_sections) - set(present_sections))
    if missing_sections:
        warnings.append(f"missing recommended sections: {', '.join(missing_sections)}")

    workflow_section_text = section_text(content, "Core Workflow") or section_text(content, "Default Workflow")
    if workflow_section_text:
        score += 6
    else:
        warnings.append("missing recommended section: Core Workflow or Default Workflow")
        milestone_caps.append(89)

    if "## Resource Loading" in content:
        score += 6
    else:
        warnings.append("missing Resource Loading guidance for progressive disclosure")
        milestone_caps.append(89)

    if "## Execution Mode" in content:
        score += 6
    else:
        warnings.append("missing Execution Mode guidance for the skill's degree of freedom")
        milestone_caps.append(89)

    if count_numbered_steps(workflow_section_text) >= 4:
        score += 10
    else:
        warnings.append("workflow section should include at least 4 numbered steps")

    if len(triggers) >= 5 and len(specific_triggers) >= 4:
        score += 10
    else:
        warnings.append("trigger cues should include at least 5 mostly specific phrases")
        milestone_caps.append(84)

    if references:
        score += min(15, 5 + len(references) * 5)
        missing_reference_links = [
            path.name for path in references if f"references/{path.name}" not in content
        ]
        if missing_reference_links:
            warnings.append(
                "references exist but are not linked from SKILL.md: "
                + ", ".join(missing_reference_links)
            )
            milestone_caps.append(84)
        if contains_unresolved_placeholder(reference_text):
            warnings.append("references still contain TODO or placeholder language")
            milestone_caps.append(84)
    else:
        warnings.append("no references generated; mature skills usually need stable reference material")

    if openai_yaml.exists():
        yaml_text = openai_yaml.read_text(encoding="utf-8", errors="ignore")
        if "display_name:" in yaml_text and "short_description:" in yaml_text:
            score += 10
        else:
            warnings.append("agents/openai.yaml is missing useful interface metadata")
        if any(generic in yaml_text.lower() for generic in ["workflow guidance", "use the skill workflow"]):
            warnings.append("agents/openai.yaml interface text is generic")
            milestone_caps.append(89)
    else:
        warnings.append("agents/openai.yaml not found")

    if not contains_unresolved_placeholder(content):
        score += 10
    else:
        warnings.append("candidate still contains TODO or placeholder language")

    if scripts:
        score += 5

    if inferred_profile == "academic":
        if not has_any(combined_text, ["apa", "mla", "chicago", "harvard", "in-text citation", "reference list"]):
            warnings.append("academic skills should cover common citation styles and citation surfaces")
            milestone_caps.append(84)
        if not has_any(combined_text, ["metadata", "missing field", "missing-fields", "source lead"]):
            warnings.append("academic citation skills should include source metadata intake behavior")
            milestone_caps.append(84)
        if not has_any(combined_text, ["never invent", "do not invent", "fake reference", "fake citation"]):
            warnings.append("academic citation skills should explicitly forbid invented citations")
            milestone_caps.append(84)
    elif inferred_profile == "product":
        if not has_any(combined_text, ["acceptance criteria", "mvp", "non-goal", "dev handoff"]):
            warnings.append("product skills should include MVP, acceptance criteria, non-goals, and handoff behavior")
            milestone_caps.append(84)
    elif inferred_profile == "integration":
        if not has_any(combined_text, ["credential", "secret", "health check", "failure"]):
            warnings.append("integration skills should include credential, health-check, and failure behavior")
            milestone_caps.append(84)
    elif inferred_profile == "script":
        if scripts and not has_any(combined_text, ["input", "output", "exit code", "dry-run", "validation"]):
            warnings.append("script skills should define input/output and failure contracts")
            milestone_caps.append(84)

    score = min(score, 100)
    if milestone_caps:
        score = min(score, min(milestone_caps))
    valid = not errors and score >= 70
    grade = "milestone" if score >= 85 and not errors else "draft" if valid else "needs-work"

    return {
        "valid": valid,
        "score": score,
        "grade": grade,
        "errors": errors,
        "warnings": warnings,
        "inferred_profile": inferred_profile,
        "references": [str(path.name) for path in references],
        "scripts": [str(path.relative_to(skill_dir / "scripts")) for path in scripts],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and score a generated skill candidate.")
    parser.add_argument("skill_dir", help="Path to the generated skill directory.")
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    report = quality_report(Path(args.skill_dir).expanduser().resolve())
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("VALID" if report["valid"] else "INVALID")
        print(f"score={report['score']} grade={report['grade']}")
        for error in report["errors"]:
            print(f"error: {error}")
        for warning in report["warnings"]:
            print(f"warning: {warning}")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
