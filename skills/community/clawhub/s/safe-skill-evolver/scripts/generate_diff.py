#!/usr/bin/env python3
"""
Generate a readable diff between two SKILL.md versions or content blocks.

Usage:
    python generate_diff.py <old_file> <new_file>
    python generate_diff.py --inline "old content" "new content"

Output formats:
    - markdown: Human-readable with before/after blocks (default)
    - json: Structured diff for programmatic use
    - unified: Standard unified diff format
"""

import difflib
import json
import sys
from pathlib import Path


def parse_sections(content: str) -> dict:
    """Parse SKILL.md into sections for structured comparison."""
    sections = {}
    current_section = "header"
    current_lines = []
    
    for line in content.split('\n'):
        if line.startswith('#'):
            # Save previous section
            if current_lines:
                sections[current_section] = '\n'.join(current_lines).strip()
            # Start new section
            current_section = line.lstrip('#').strip()
            current_lines = [line]
        else:
            current_lines.append(line)
    
    # Save last section
    if current_lines:
        sections[current_section] = '\n'.join(current_lines).strip()
    
    return sections


def generate_markdown_diff(old_text: str, new_text: str) -> str:
    """Generate a human-readable markdown diff."""
    
    old_sections = parse_sections(old_text)
    new_sections = parse_sections(new_text)
    
    output = ["# Skill Diff", ""]
    output.append("## Summary")
    
    # Added sections
    added = [s for s in new_sections if s not in old_sections and s != "header"]
    removed = [s for s in old_sections if s not in new_sections and s != "header"]
    common = [s for s in old_sections if s in new_sections and s != "header"]
    
    output.append(f"- **Added sections:** {len(added)}")
    output.append(f"- **Removed sections:** {len(removed)}")
    output.append(f"- **Modified sections:** {len(common)}")
    output.append("")
    
    # Added
    if added:
        output.append("## New Sections")
        for section in added:
            output.append(f"### + {section}")
            output.append("```")
            output.append(new_sections[section][:500])
            if len(new_sections[section]) > 500:
                output.append("... (truncated)")
            output.append("```")
            output.append("")
    
    # Removed
    if removed:
        output.append("## Removed Sections")
        for section in removed:
            output.append(f"### - {section}")
            output.append("```")
            output.append(old_sections[section][:500])
            if len(old_sections[section]) > 500:
                output.append("... (truncated)")
            output.append("```")
            output.append("")
    
    # Modified
    modified = []
    for section in common:
        if old_sections[section] != new_sections[section]:
            modified.append(section)
    
    if modified:
        output.append("## Modified Sections")
        for section in modified:
            output.append(f"### ~ {section}")
            output.append("")
            output.append("**Before:**")
            output.append("```")
            output.append(old_sections[section][:300])
            if len(old_sections[section]) > 300:
                output.append("...")
            output.append("```")
            output.append("")
            output.append("**After:**")
            output.append("```")
            output.append(new_sections[section][:300])
            if len(new_sections[section]) > 300:
                output.append("...")
            output.append("```")
            output.append("")
            
            # Line-level diff
            old_lines = old_sections[section].split('\n')
            new_lines = new_sections[section].split('\n')
            diff = list(difflib.unified_diff(
                old_lines, new_lines, 
                fromfile=f"{section} (old)", 
                tofile=f"{section} (new)",
                lineterm=""
            ))
            
            if diff and len(diff) > 6:  # Skip header lines
                output.append("**Line changes:**")
                output.append("```diff")
                for line in diff[2:]:  # Skip ---/+++ headers
                    if line.startswith('+'):
                        output.append(f"+ {line[1:]}")
                    elif line.startswith('-'):
                        output.append(f"- {line[1:]}")
                    elif line.startswith('@@'):
                        output.append(line)
                output.append("```")
                output.append("")
    
    return '\n'.join(output)


def generate_unified_diff(old_text: str, new_text: str, old_name="SKILL.md", new_name="SKILL.md") -> str:
    """Generate standard unified diff."""
    old_lines = old_text.split('\n')
    new_lines = new_text.split('\n')
    
    diff = difflib.unified_diff(
        old_lines, new_lines,
        fromfile=old_name, tofile=new_name,
        lineterm=""
    )
    
    return '\n'.join(diff)


def generate_structured_diff(old_text: str, new_text: str) -> dict:
    """Generate structured diff for programmatic use."""
    
    old_sections = parse_sections(old_text)
    new_sections = parse_sections(new_text)
    
    result = {
        "added_sections": [],
        "removed_sections": [],
        "modified_sections": [],
        "unchanged_sections": []
    }
    
    all_sections = set(old_sections.keys()) | set(new_sections.keys())
    
    for section in all_sections:
        if section == "header":
            continue
        
        if section not in old_sections:
            result["added_sections"].append({
                "title": section,
                "content_preview": new_sections[section][:200]
            })
        elif section not in new_sections:
            result["removed_sections"].append({
                "title": section,
                "content_preview": old_sections[section][:200]
            })
        elif old_sections[section] != new_sections[section]:
            # Calculate word diff
            old_words = set(old_sections[section].split())
            new_words = set(new_sections[section].split())
            
            result["modified_sections"].append({
                "title": section,
                "word_changes": {
                    "added": len(new_words - old_words),
                    "removed": len(old_words - new_words)
                },
                "old_preview": old_sections[section][:200],
                "new_preview": new_sections[section][:200]
            })
        else:
            result["unchanged_sections"].append(section)
    
    return result


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_diff.py <old_file> <new_file> [--format markdown|json|unified]")
        sys.exit(1)
    
    format_type = "markdown"
    if "--format" in sys.argv:
        idx = sys.argv.index("--format")
        format_type = sys.argv[idx + 1]
        sys.argv = sys.argv[:idx] + sys.argv[idx+2:]
    
    old_path = Path(sys.argv[1])
    new_path = Path(sys.argv[2])
    
    if not old_path.exists() or not new_path.exists():
        print(f"Error: One or both files not found")
        sys.exit(1)
    
    old_text = old_path.read_text(encoding="utf-8")
    new_text = new_path.read_text(encoding="utf-8")
    
    if format_type == "markdown":
        print(generate_markdown_diff(old_text, new_text))
    elif format_type == "unified":
        print(generate_unified_diff(old_text, new_text, str(old_path), str(new_path)))
    elif format_type == "json":
        result = generate_structured_diff(old_text, new_text)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"Unknown format: {format_type}")
        sys.exit(1)
