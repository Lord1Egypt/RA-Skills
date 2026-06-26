#!/usr/bin/env python3
"""
Analyze a SKILL.md and return structured insights.

Usage:
    python analyze_skill.py <SKILL.md_path>

Outputs:
    - Section completeness score
    - Trigger clarity analysis
    - Safety coverage report
    - Improvement suggestions
"""

import json
import re
import sys
from pathlib import Path


def analyze_skill(content: str) -> dict:
    """Analyze skill content deeply."""
    
    report = {
        "structure": {},
        "safety": {},
        "triggers": {},
        "quality": {},
        "suggestions": []
    }
    
    # Structure analysis
    sections = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
    report["structure"]["sections_found"] = sections
    report["structure"]["section_count"] = len(sections)
    report["structure"]["depth"] = max(
        (len(line) - len(line.lstrip('#')) for line in content.split('\n') if line.startswith('#')),
        default=0
    )
    
    # Check for required sections
    required = ["when to use", "workflow", "examples", "safety", "boundaries"]
    content_lower = content.lower()
    missing = [r for r in required if r not in content_lower]
    report["structure"]["missing_required"] = missing
    
    if missing:
        report["suggestions"].append(f"Add missing sections: {', '.join(missing)}")
    
    # Safety analysis
    safety_patterns = {
        "explicit_never_rules": len(re.findall(r'(?i)never\s*[:\-]', content)),
        "explicit_always_rules": len(re.findall(r'(?i)always\s*[:\-]', content)),
        "confirmation_required": bool(re.search(r'(?i)confirm|bestätigung|approve', content)),
        "boundaries_documented": bool(re.search(r'(?i)boundar|grenzen|einschränkung', content))
    }
    report["safety"] = safety_patterns
    
    if not safety_patterns["confirmation_required"]:
        report["suggestions"].append("Add explicit confirmation requirements before destructive actions")
    
    if not safety_patterns["boundaries_documented"]:
        report["suggestions"].append("Document clear boundaries (what NOT to do)")
    
    # Trigger analysis
    trigger_section = re.search(
        r'(?i)#+\s*when\s+to\s+use.*?(?=#+\s|$)',
        content,
        re.DOTALL
    )
    if trigger_section:
        triggers = re.findall(r'^(?:\s*[-*•]|\d+\.)\s+(.+)$', trigger_section.group(), re.MULTILINE)
        report["triggers"]["count"] = len(triggers)
        report["triggers"]["examples"] = triggers[:5]  # First 5
        
        if len(triggers) < 2:
            report["suggestions"].append("Add more trigger conditions (at least 3 recommended)")
    else:
        report["triggers"]["count"] = 0
        report["suggestions"].append("Add 'When to Use' section with clear trigger conditions")
    
    # Quality metrics
    report["quality"]["word_count"] = len(content.split())
    report["quality"]["example_count"] = len(re.findall(r'(?i)^#{1,4}\s*example', content, re.MULTILINE))
    report["quality"]["code_blocks"] = len(re.findall(r'```', content)) // 2  # Paired
    
    if report["quality"]["example_count"] == 0:
        report["suggestions"].append("Add concrete usage examples (at least 2)")
    
    # Overall score calculation
    score = 100
    score -= len(missing) * 15  # -15 per missing required section
    if not safety_patterns["confirmation_required"]: score -= 10
    if not safety_patterns["boundaries_documented"]: score -= 10
    if report["triggers"]["count"] < 2: score -= 10
    if report["quality"]["example_count"] == 0: score -= 15
    if report["quality"]["example_count"] == 1: score -= 5
    
    report["overall_score"] = max(0, score)
    
    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_skill.py <SKILL.md_path>")
        sys.exit(1)
    
    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: File not found: {path}")
        sys.exit(1)
    
    content = path.read_text(encoding="utf-8")
    report = analyze_skill(content)
    
    # Output
    print(f"\nSkill Analysis: {path}")
    print(f"Overall Score: {report['overall_score']}/100\n")
    
    print(f"Structure: {report['structure']['section_count']} sections, depth {report['structure']['depth']}")
    if report['structure']['missing_required']:
        print(f"  Missing: {', '.join(report['structure']['missing_required'])}")
    
    print(f"\nTriggers: {report['triggers'].get('count', 0)} found")
    for t in report['triggers'].get('examples', []):
        print(f"  - {t[:80]}...")
    
    print(f"\nSafety Coverage:")
    for k, v in report['safety'].items():
        print(f"  {k}: {v}")
    
    print(f"\nQuality Metrics:")
    print(f"  Words: {report['quality']['word_count']}")
    print(f"  Examples: {report['quality']['example_count']}")
    print(f"  Code blocks: {report['quality']['code_blocks']}")
    
    if report['suggestions']:
        print(f"\nSuggestions ({len(report['suggestions'])}):")
        for i, s in enumerate(report['suggestions'], 1):
            print(f"  {i}. {s}")
    
    print(f"\n[JSON]\n{json.dumps(report, indent=2, ensure_ascii=False)}")
