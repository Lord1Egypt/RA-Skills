#!/usr/bin/env python3
"""
Validate a skill directory against the Skill Evolver Quality Checklist.

Usage:
    python validate_skill.py <skill_directory>
    python validate_skill.py <path_to_SKILL.md>

Returns JSON with:
    - overall_score (0-100)
    - sections_check (completeness)
    - safety_check (rules present)
    - clarity_check (examples, triggers)
    - issues (list of problems found)
"""

import json
import sys
import re
from pathlib import Path


def analyze_skill_md(content: str) -> dict:
    """Analyze SKILL.md content and return structured report."""
    
    report = {
        "sections_found": [],
        "sections_missing": [],
        "required_sections": [
            "When to Use",
            "Core Principles",
            "Workflow",
            "Examples",
            "Safety"
        ],
        "safety_rules": {
            "never_auto_write": False,
            "never_auto_exec": False,
            "confirm_before_write": False,
            "confirm_before_exec": False,
            "explicit_boundaries": False
        },
        "examples_count": 0,
        "triggers_count": 0,
        "word_count": len(content.split()),
        "issues": []
    }
    
    # Check required sections
    content_lower = content.lower()
    for section in report["required_sections"]:
        section_lower = section.lower()
        # Check various heading styles
        patterns = [
            f"^#+\\s*{re.escape(section)}",
            f"^#+\\s*{re.escape(section_lower)}",
            f"## {re.escape(section)}",
            f"## {re.escape(section_lower)}"
        ]
        found = any(re.search(p, content, re.MULTILINE | re.IGNORECASE) for p in patterns)
        if found:
            report["sections_found"].append(section)
        else:
            report["sections_missing"].append(section)
            report["issues"].append(f"Missing section: {section}")
    
    # Check safety rules
    safety_keywords = {
        "never_auto_write": [r"never.*write.*without.*confirm", r"nicht.*schreiben.*ohne.*bestätigung"],
        "never_auto_exec": [r"never.*execut.*without.*confirm", r"never.*run.*without.*confirm", r"keine.*befehle.*ohne"],
        "confirm_before_write": [r"confirm.*before.*write", r"bestätigung.*vor.*schreiben"],
        "confirm_before_exec": [r"confirm.*before.*execut", r"bestätigung.*vor.*ausführen"],
        "explicit_boundaries": [r"boundar", r"grenzen", r"safety.*boundar"]
    }
    
    for rule, patterns in safety_keywords.items():
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                report["safety_rules"][rule] = True
                break
    
    # Count examples (look for "Example" headings)
    report["examples_count"] = len(re.findall(r'^#{1,4}\s*Example', content, re.MULTILINE | re.IGNORECASE))
    
    # Count trigger conditions
    trigger_section = re.search(r'when to use.*?(?=^#{1,3}\s)', content, re.IGNORECASE | re.DOTALL)
    if trigger_section:
        report["triggers_count"] = len(re.findall(r'[-*•]\s', trigger_section.group()))
    
    # Calculate score
    section_score = len(report["sections_found"]) / len(report["required_sections"]) * 40
    safety_score = sum(report["safety_rules"].values()) / len(report["safety_rules"]) * 30
    example_score = min(report["examples_count"] / 2, 1) * 20
    size_score = min(report["word_count"] / 500, 1) * 10
    
    report["overall_score"] = round(section_score + safety_score + example_score + size_score)
    
    # Flag low scores
    if report["overall_score"] < 50:
        report["issues"].append(f"Low overall score: {report['overall_score']}/100")
    if report["examples_count"] == 0:
        report["issues"].append("No examples found — add concrete usage examples")
    if sum(report["safety_rules"].values()) < 2:
        report["issues"].append("Insufficient safety rules — add explicit confirmation requirements")
    
    return report


def validate_skill_directory(skill_dir: Path) -> dict:
    """Validate a complete skill directory."""
    
    if skill_dir.is_file() and skill_dir.name.lower() == "skill.md":
        skill_dir = skill_dir.parent
    
    skill_md = skill_dir / "SKILL.md"
    
    if not skill_md.exists():
        return {
            "valid": False,
            "error": f"SKILL.md not found in {skill_dir}",
            "issues": ["Missing SKILL.md — this is required"]
        }
    
    content = skill_md.read_text(encoding="utf-8")
    report = analyze_skill_md(content)
    
    # Check for referenced but missing files
    scripts_dir = skill_dir / "scripts"
    templates_dir = skill_dir / "templates"
    
    # Look for script references
    script_refs = re.findall(r'`?scripts[\/\\]([\w\-]+\.\w+)`?', content)
    missing_scripts = []
    for script in script_refs:
        if not (scripts_dir / script).exists():
            missing_scripts.append(script)
    
    if missing_scripts:
        report["issues"].append(f"Referenced scripts not found: {', '.join(missing_scripts)}")
    
    # Look for template references
    template_refs = re.findall(r'`?templates[\/\\]([\w\-]+\.\w+)`?', content)
    missing_templates = []
    for template in template_refs:
        if not (templates_dir / template).exists():
            missing_templates.append(template)
    
    if missing_templates:
        report["issues"].append(f"Referenced templates not found: {', '.join(missing_templates)}")
    
    report["valid"] = report["overall_score"] >= 50 and len(report["issues"]) <= 2
    report["skill_directory"] = str(skill_dir)
    
    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_skill.py <skill_directory_or_SKILL.md>")
        sys.exit(1)
    
    target = Path(sys.argv[1])
    
    if not target.exists():
        print(f"Error: Path not found: {target}")
        sys.exit(1)
    
    result = validate_skill_directory(target)
    
    # Pretty print
    print(f"\n{'='*60}")
    print(f"Skill Validation Report: {result.get('skill_directory', target)}")
    print(f"{'='*60}\n")
    
    print(f"Overall Score: {result['overall_score']}/100")
    valid_str = "YES" if result['valid'] else "NO"
    print(f"Valid: {valid_str}\n")
    
    if 'sections_found' in result:
        print(f"Sections Found: {len(result['sections_found'])}/5")
        for s in result['sections_found']:
            print(f"  [OK] {s}")
        for s in result.get('sections_missing', []):
            print(f"  [MISSING] {s}")
    
    print(f"\nSafety Rules:")
    for rule, present in result.get('safety_rules', {}).items():
        status = "[OK]" if present else "[MISSING]"
        print(f"  {status} {rule}")
    
    print(f"\nExamples: {result.get('examples_count', 0)}")
    print(f"Word Count: {result.get('word_count', 0)}")
    
    if result.get('issues'):
        print(f"\n[!] Issues Found ({len(result['issues'])}):")
        for issue in result['issues']:
            print(f"  - {issue}")
    else:
        print(f"\n[OK] No issues found!")
    
    print(f"\n{'='*60}")
    
    # Also output JSON for programmatic use
    print(f"\n[JSON]\n{json.dumps(result, indent=2, ensure_ascii=False)}")
