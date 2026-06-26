#!/usr/bin/env python3
"""
Analyze a skill directory and report enhancement opportunities.

Usage:
    python3 analyze_skill.py /path/to/skill-directory

Output: JSON report with enhancement recommendations.
"""

import json
import os
import re
import sys
from pathlib import Path


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from SKILL.md content."""
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            frontmatter = content[3:end].strip()
            # Simple parsing for name and description
            result = {}
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    result[key.strip()] = value.strip()
            return result
    return {}


def get_body_content(content: str) -> str:
    """Get body content excluding frontmatter."""
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            return content[end + 3:].strip()
    return content


def analyze_skill(skill_path: str) -> dict:
    """Analyze a skill directory and return enhancement report."""
    skill_dir = Path(skill_path)
    skill_name = skill_dir.name
    
    if not skill_dir.exists():
        return {"error": f"Skill directory not found: {skill_path}"}
    
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        return {"error": f"SKILL.md not found in {skill_path}"}
    
    # Read SKILL.md
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract frontmatter and body
    frontmatter = extract_frontmatter(content)
    body = get_body_content(content)
    
    # Calculate metrics
    char_count = len(content)
    body_char_count = len(body)
    
    # Check for sections
    has_examples = bool(re.search(r'##.*[Ee]xample', body))
    has_best_practices = bool(re.search(r'##.*[Bb]est [Pp]ractice', body))
    has_use_cases = bool(re.search(r'##.*[Uu]se [Cc]ase', body))
    has_scripts_section = bool(re.search(r'##.*[Ss]cript', body))
    
    # Check for TODO/XXX placeholders
    has_todo = bool(re.search(r'TODO|XXX|FIXME', content))
    
    # Analyze scripts directory
    scripts_dir = skill_dir / "scripts"
    scripts = []
    scripts_documented = True
    if scripts_dir.exists():
        scripts = [f.name for f in scripts_dir.iterdir() if f.is_file()]
        # Check if scripts are mentioned in SKILL.md
        for script in scripts:
            if script not in content:
                scripts_documented = False
                break
    
    # Analyze references directory
    references_dir = skill_dir / "references"
    references = []
    if references_dir.exists():
        references = [f.name for f in references_dir.iterdir() if f.is_file()]
    
    # Analyze assets directory
    assets_dir = skill_dir / "assets"
    assets = []
    if assets_dir.exists():
        assets = [f.name for f in assets_dir.iterdir() if f.is_file() or f.is_dir()]
    
    # Generate recommendations
    recommendations = []
    
    if char_count < 3000:
        recommendations.append(f"Content is short ({char_count} chars). Consider adding more examples and documentation.")
    
    if scripts and not scripts_documented:
        recommendations.append(f"Scripts exist but not documented: {', '.join(scripts)}")
    
    if not has_examples:
        recommendations.append("Add usage examples section with concrete examples")
    
    if not has_best_practices:
        recommendations.append("Add best practices section")
    
    if not has_use_cases:
        recommendations.append("Add common use cases section")
    
    if has_todo:
        recommendations.append("Remove TODO/XXX placeholders from documentation")
    
    # Build report
    report = {
        "skill_name": skill_name,
        "skill_path": str(skill_dir.absolute()),
        "metrics": {
            "total_chars": char_count,
            "body_chars": body_char_count,
            "is_short": char_count < 3000
        },
        "sections": {
            "has_examples": has_examples,
            "has_best_practices": has_best_practices,
            "has_use_cases": has_use_cases,
            "has_scripts_section": has_scripts_section
        },
        "resources": {
            "scripts_count": len(scripts),
            "scripts": scripts,
            "scripts_documented": scripts_documented,
            "references_count": len(references),
            "references": references,
            "assets_count": len(assets),
            "assets": assets
        },
        "quality": {
            "has_todo_placeholders": has_todo
        },
        "recommendations": recommendations,
        "frontmatter": {
            "name": frontmatter.get('name', 'Not found'),
            "description": frontmatter.get('description', 'Not found')
        }
    }
    
    return report


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_skill.py /path/to/skill-directory")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    report = analyze_skill(skill_path)
    
    # Output as formatted JSON
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # Exit with error code if there are recommendations
    if report.get("recommendations"):
        sys.exit(0)  # Still success, but with recommendations


if __name__ == "__main__":
    main()
