#!/usr/bin/env python3
"""
Self-Evolution Engine
Analyzes patterns, extracts learnings, and proposes behavioral evolution.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


# Default paths
WORKSPACE = Path.home() / ".openclaw" / "workspace"
LEARNINGS_DIR = WORKSPACE / ".learnings"
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"
EVOLUTION_LOG = WORKSPACE / ".evolution" / "evolution-log.md"


def ensure_evolution_dir():
    """Ensure evolution directory exists."""
    evol_dir = WORKSPACE / ".evolution"
    evol_dir.mkdir(parents=True, exist_ok=True)
    return evol_dir


def parse_date(date_str: str) -> Optional[datetime]:
    """Parse various date formats."""
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%d %b %Y",
        "%b %d, %Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


def extract_learnings(days: int = 30) -> list:
    """Extract learning entries from .learnings/ directory."""
    learnings = []
    cutoff = datetime.now() - timedelta(days=days)

    if not LEARNINGS_DIR.exists():
        return learnings

    for file_path in LEARNINGS_DIR.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")

        # Split into entries
        entries = re.split(r'^##\s+\[', content, flags=re.MULTILINE)[1:]  # Skip header

        for entry in entries:
            # Extract date
            date_match = re.search(r'\*\*Logged\*\*:\s*(.+?)(?:\n|$)', entry)
            if date_match:
                entry_date = parse_date(date_match.group(1))
                if entry_date and entry_date >= cutoff:
                    # Extract category
                    category_match = re.match(r'([A-Z]+-\d+-\d+)\]\s+(\w+)', entry)
                    if category_match:
                        entry_id = category_match.group(1)
                        category = category_match.group(2)

                        # Extract summary
                        summary_match = re.search(r'### Summary\n(.+?)(?:\n###|\n---|\Z)', entry, re.DOTALL)
                        summary = summary_match.group(1).strip() if summary_match else ""

                        learnings.append({
                            "id": entry_id,
                            "category": category,
                            "summary": summary,
                            "date": entry_date.isoformat(),
                            "source_file": str(file_path.name),
                            "content": entry,
                        })

    return learnings


def extract_memory_entries(days: int = 30) -> list:
    """Extract entries from memory/YYYY-MM-DD.md files."""
    entries = []
    cutoff = datetime.now() - timedelta(days=days)

    if not MEMORY_DIR.exists():
        return entries

    for file_path in sorted(MEMORY_DIR.glob("*.md"), reverse=True):
        # Parse date from filename
        try:
            file_date = datetime.strptime(file_path.stem, "%Y-%m-%d")
            if file_date < cutoff:
                break

            content = file_path.read_text(encoding="utf-8")
            if content.strip():
                entries.append({
                    "date": file_date.isoformat(),
                    "file": str(file_path.name),
                    "content": content,
                    "size": len(content),
                })
        except ValueError:
            continue

    return entries


def detect_error_patterns(learnings: list, threshold: int = 3) -> list:
    """Detect recurring error patterns."""
    patterns = []
    error_counter = Counter()

    for learning in learnings:
        if learning["category"] in ["error", "ERR"]:
            # Extract error type from summary
            error_type = learning["summary"].lower()
            # Normalize
            for keyword in ["failed", "error", "not found", "timeout", "invalid"]:
                if keyword in error_type:
                    error_counter[keyword] += 1
                    break
            else:
                error_counter["other"] += 1

    for error_type, count in error_counter.items():
        if count >= threshold:
            patterns.append({
                "type": "error",
                "pattern": error_type,
                "count": count,
                "suggested_action": f"Create prevention rule for {error_type} errors",
            })

    return patterns


def detect_success_patterns(learnings: list, min_occurrences: int = 3) -> list:
    """Detect successful workflow patterns."""
    patterns = []
    success_keywords = Counter()

    for learning in learnings:
        if learning["category"] in ["success", "best_practice", "LRN"]:
            summary = learning["summary"].lower()
            # Extract action verbs
            for verb in ["completed", "fixed", "solved", "optimized", "improved"]:
                if verb in summary:
                    success_keywords[verb] += 1

    for keyword, count in success_keywords.items():
        if count >= min_occurrences:
            patterns.append({
                "type": "success",
                "pattern": keyword,
                "count": count,
                "suggested_action": f"Document {keyword} workflow as reusable pattern",
            })

    return patterns


def detect_preference_patterns(learnings: list) -> list:
    """Detect user preference patterns from corrections."""
    preferences = []

    for learning in learnings:
        if learning["category"] == "correction":
            summary = learning["summary"].lower()
            preferences.append({
                "type": "preference",
                "summary": learning["summary"],
                "date": learning["date"],
            })

    return preferences


def analyze_patterns(days: int = 7, threshold: int = 3) -> dict:
    """Analyze all patterns from recent interactions."""
    learnings = extract_learnings(days=days)

    result = {
        "period": f"Last {days} days",
        "learnings_count": len(learnings),
        "patterns": {
            "errors": detect_error_patterns(learnings, threshold),
            "successes": detect_success_patterns(learnings),
            "preferences": detect_preference_patterns(learnings),
        },
        "recommendations": [],
    }

    # Generate recommendations
    for pattern in result["patterns"]["errors"]:
        result["recommendations"].append({
            "priority": "high",
            "action": pattern["suggested_action"],
            "target": "AGENTS.md",
        })

    for pattern in result["patterns"]["successes"]:
        result["recommendations"].append({
            "priority": "medium",
            "action": pattern["suggested_action"],
            "target": "AGENTS.md",
        })

    return result


def extract_rules(learnings: list) -> list:
    """Extract candidate rules from learnings."""
    rules = []

    for learning in learnings:
        if learning["category"] in ["best_practice", "correction"]:
            # Try to extract actionable rule
            summary = learning["summary"]
            if len(summary) < 200:  # Keep rules concise
                rules.append({
                    "source": learning["id"],
                    "rule": summary,
                    "date": learning["date"],
                    "type": learning["category"],
                })

    return rules


def self_assess(auto_evolve: bool = False) -> dict:
    """Perform self-assessment and optionally auto-evolve."""
    assessment = {
        "timestamp": datetime.now().isoformat(),
        "analysis": analyze_patterns(days=7),
        "memory_health": assess_memory_health(),
        "behavioral_health": assess_behavioral_health(),
        "recommendations": [],
    }

    # Generate recommendations based on assessment
    if assessment["memory_health"]["status"] != "healthy":
        assessment["recommendations"].append({
            "area": "memory",
            "action": "Run memory consolidation",
            "command": "python3 scripts/memory_manager.py --consolidate",
        })

    if assessment["behavioral_health"]["inconsistencies"]:
        assessment["recommendations"].append({
            "area": "behavior",
            "action": "Resolve behavioral inconsistencies",
            "details": assessment["behavioral_health"]["inconsistencies"],
        })

    return assessment


def assess_memory_health() -> dict:
    """Assess health of memory system."""
    health = {
        "status": "healthy",
        "issues": [],
    }

    # Check if memory files exist
    if not MEMORY_FILE.exists():
        health["issues"].append("MEMORY.md does not exist")
        health["status"] = "warning"

    if not MEMORY_DIR.exists():
        health["issues"].append("memory/ directory does not exist")
        health["status"] = "warning"
    else:
        # Check for stale daily memories
        memory_files = list(MEMORY_DIR.glob("*.md"))
        if len(memory_files) > 30:
            health["issues"].append(f"Too many daily memory files ({len(memory_files)})")
            health["status"] = "warning"

    # Check .learnings directory
    if not LEARNINGS_DIR.exists():
        health["issues"].append(".learnings/ directory does not exist")
        health["status"] = "warning"

    return health


def assess_behavioral_health() -> dict:
    """Assess health of behavioral files."""
    health = {
        "status": "healthy",
        "inconsistencies": [],
    }

    # Check SOUL.md exists
    soul_file = WORKSPACE / "SOUL.md"
    if not soul_file.exists():
        health["inconsistencies"].append("SOUL.md missing")
        health["status"] = "warning"

    # Check AGENTS.md exists
    agents_file = WORKSPACE / "AGENTS.md"
    if not agents_file.exists():
        health["inconsistencies"].append("AGENTS.md missing")
        health["status"] = "warning"

    return health


def generate_report(output_file: Optional[str] = None, full: bool = False) -> str:
    """Generate evolution report."""
    report_lines = [
        f"# Evolution Report: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Analysis Summary",
        "",
    ]

    analysis = analyze_patterns(days=30)

    report_lines.append(f"- Learnings analyzed: {analysis['learnings_count']}")
    report_lines.append(f"- Error patterns: {len(analysis['patterns']['errors'])}")
    report_lines.append(f"- Success patterns: {len(analysis['patterns']['successes'])}")
    report_lines.append(f"- Preference patterns: {len(analysis['patterns']['preferences'])}")
    report_lines.append("")

    if analysis["patterns"]["errors"]:
        report_lines.append("### Error Patterns Detected")
        report_lines.append("")
        for p in analysis["patterns"]["errors"]:
            report_lines.append(f"- **{p['pattern']}**: {p['count']} occurrences")
        report_lines.append("")

    if analysis["patterns"]["successes"]:
        report_lines.append("### Success Patterns Detected")
        report_lines.append("")
        for p in analysis["patterns"]["successes"]:
            report_lines.append(f"- **{p['pattern']}**: {p['count']} occurrences")
        report_lines.append("")

    if analysis["recommendations"]:
        report_lines.append("## Recommendations")
        report_lines.append("")
        for r in analysis["recommendations"]:
            report_lines.append(f"- [{r['priority']}] {r['action']} → {r['target']}")
        report_lines.append("")

    if full:
        # Add self-assessment
        assessment = self_assess()
        report_lines.append("## Self-Assessment")
        report_lines.append("")
        report_lines.append(f"- Memory health: {assessment['memory_health']['status']}")
        report_lines.append(f"- Behavioral health: {assessment['behavioral_health']['status']}")
        report_lines.append("")

        if assessment["recommendations"]:
            report_lines.append("### Recommended Actions")
            report_lines.append("")
            for r in assessment["recommendations"]:
                report_lines.append(f"- {r['action']}")
            report_lines.append("")

    report = "\n".join(report_lines)

    if output_file:
        Path(output_file).write_text(report, encoding="utf-8")
        print(f"Report written to {output_file}")

    return report


def log_evolution(action: str, details: str):
    """Log an evolution action."""
    ensure_evolution_dir()
    timestamp = datetime.now().isoformat()

    entry = f"""
## [{timestamp}] {action}

{details}

---
"""
    with open(EVOLUTION_LOG, "a", encoding="utf-8") as f:
        f.write(entry)


def main():
    parser = argparse.ArgumentParser(description="Self-Evolution Engine")
    parser.add_argument("--analyze", action="store_true", help="Analyze patterns")
    parser.add_argument("--extract-patterns", action="store_true", help="Extract patterns")
    parser.add_argument("--self-assess", action="store_true", help="Run self-assessment")
    parser.add_argument("--report", action="store_true", help="Generate evolution report")
    parser.add_argument("--days", type=int, default=7, help="Days to analyze (default: 7)")
    parser.add_argument("--threshold", type=int, default=3, help="Pattern detection threshold")
    parser.add_argument("--output", help="Output file for report")
    parser.add_argument("--full", action="store_true", help="Full report")
    parser.add_argument("--auto-evolve", action="store_true", help="Auto-evolve after assessment")

    args = parser.parse_args()

    if args.analyze:
        result = analyze_patterns(days=args.days, threshold=args.threshold)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.extract_patterns:
        learnings = extract_learnings(days=args.days)
        rules = extract_rules(learnings)
        print(json.dumps(rules, indent=2, ensure_ascii=False))

    elif args.self_assess:
        result = self_assess(auto_evolve=args.auto_evolve)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.report:
        report = generate_report(output_file=args.output, full=args.full)
        if not args.output:
            print(report)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
