#!/usr/bin/env python3
"""
Automatically enhance SKILL.md with missing content.

Usage:
    python3 enhance_skill.py /path/to/skill-directory [options]

Options:
    --dry-run: Preview changes without writing
    --sections SECTIONS: Comma-separated list of sections to enhance
                         Available: examples, scripts, best-practices, use-cases
                         Default: all sections
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path


def extract_script_info(script_path: Path) -> dict:
    """Extract information from a script file."""
    info = {
        "name": script_path.name,
        "purpose": "",
        "usage": "",
        "examples": []
    }
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring_match:
            docstring = docstring_match.group(1).strip()
            lines = docstring.split('\n')
            
            # First non-empty line is purpose
            for line in lines:
                line = line.strip()
                if line and not line.startswith('Usage:') and not line.startswith('Example'):
                    info["purpose"] = line
                    break
            
            # Look for usage in docstring
            for line in lines:
                if 'usage:' in line.lower() or 'python3' in line.lower():
                    info["usage"] = line.strip()
                    break
        
        # If no usage found in docstring, generate from filename
        if not info["usage"]:
            info["usage"] = f"python3 scripts/{script_path.name} [arguments]"
        
        # Generate examples based on script name
        info["examples"] = [
            f"# Basic usage\npython3 scripts/{script_path.name} input.txt",
            f"# With options\npython3 scripts/{script_path.name} input.txt --output result.txt"
        ]
        
    except Exception as e:
        info["purpose"] = f"Script for {script_path.stem.replace('_', ' ')}"
        info["usage"] = f"python3 scripts/{script_path.name} [arguments]"
    
    return info


def generate_scripts_section(skill_dir: Path) -> str:
    """Generate scripts documentation section."""
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return ""
    
    scripts = [f for f in scripts_dir.iterdir() if f.is_file()]
    if not scripts:
        return ""
    
    sections = []
    sections.append("## Scripts Reference\n")
    sections.append("The following scripts are available in this skill:\n")
    
    for script in sorted(scripts):
        info = extract_script_info(script)
        sections.append(f"### {info['name']}\n")
        sections.append(f"**Purpose**: {info['purpose']}\n")
        sections.append(f"**Usage**:\n")
        sections.append(f"```bash\n{info['usage']}\n```\n")
        
        if info['examples']:
            sections.append(f"**Examples**:\n")
            for example in info['examples']:
                sections.append(f"```bash\n{example}\n```\n")
        sections.append("")
    
    return '\n'.join(sections)


def generate_examples_section(skill_name: str) -> str:
    """Generate usage examples section."""
    sections = []
    sections.append("## Usage Examples\n")
    sections.append("Here are common usage patterns for this skill:\n")
    
    sections.append("### Example 1: Basic Usage\n")
    sections.append("**Scenario**: Describe a common use case\n")
    sections.append("**Command**:\n")
    sections.append("```bash\n# Command to execute the skill\n```\n")
    sections.append("**Expected Output**:\n")
    sections.append("```\nExpected result here\n```\n")
    
    sections.append("### Example 2: Advanced Usage\n")
    sections.append("**Scenario**: Describe a more complex use case\n")
    sections.append("**Command**:\n")
    sections.append("```bash\n# Advanced command with options\n```\n")
    sections.append("**Expected Output**:\n")
    sections.append("```\nExpected result here\n```\n")
    
    return '\n'.join(sections)


def generate_best_practices_section(skill_name: str) -> str:
    """Generate best practices section."""
    sections = []
    sections.append("## Best Practices\n")
    sections.append("Follow these recommendations for optimal results:\n")
    
    sections.append("### Do's\n")
    sections.append("- Start with clear requirements\n")
    sections.append("- Test with sample data first\n")
    sections.append("- Review outputs before finalizing\n")
    sections.append("\n")
    
    sections.append("### Don'ts\n")
    sections.append("- Skip validation steps\n")
    sections.append("- Use on production data without testing\n")
    sections.append("- Ignore error messages\n")
    sections.append("\n")
    
    sections.append("### Tips\n")
    sections.append("- Keep backups of important files\n")
    sections.append("- Use descriptive names for outputs\n")
    sections.append("- Document your workflow for reproducibility\n")
    
    return '\n'.join(sections)


def generate_use_cases_section(skill_name: str) -> str:
    """Generate common use cases section."""
    sections = []
    sections.append("## Common Use Cases\n")
    sections.append("This skill is commonly used for:\n")
    
    sections.append("1. **[Use Case 1]**: Brief description of scenario\n")
    sections.append("   - **When to use**: Context for when this applies\n")
    sections.append("   - **Expected outcome**: What you should get\n")
    sections.append("\n")
    
    sections.append("2. **[Use Case 2]**: Brief description of scenario\n")
    sections.append("   - **When to use**: Context for when this applies\n")
    sections.append("   - **Expected outcome**: What you should get\n")
    sections.append("\n")
    
    sections.append("3. **[Use Case 3]**: Brief description of scenario\n")
    sections.append("   - **When to use**: Context for when this applies\n")
    sections.append("   - **Expected outcome**: What you should get\n")
    
    return '\n'.join(sections)


def enhance_skill(skill_path: str, sections_to_enhance: list, dry_run: bool = False) -> dict:
    """Enhance a skill's SKILL.md with missing content."""
    skill_dir = Path(skill_path)
    skill_name = skill_dir.name
    
    if not skill_dir.exists():
        return {"error": f"Skill directory not found: {skill_path}"}
    
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.exists():
        return {"error": f"SKILL.md not found in {skill_path}"}
    
    # Read current content
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    content = original_content
    enhancements = []
    
    # Check and enhance each section
    if 'scripts' in sections_to_enhance:
        scripts_dir = skill_dir / "scripts"
        if scripts_dir.exists() and not re.search(r'##.*[Ss]cript', content):
            scripts_section = generate_scripts_section(skill_dir)
            if scripts_section:
                content = content.rstrip() + '\n\n' + scripts_section
                enhancements.append("Added scripts documentation")
    
    if 'examples' in sections_to_enhance:
        if not re.search(r'##.*[Ee]xample', content):
            examples_section = generate_examples_section(skill_name)
            content = content.rstrip() + '\n\n' + examples_section
            enhancements.append("Added usage examples")
    
    if 'best-practices' in sections_to_enhance:
        if not re.search(r'##.*[Bb]est [Pp]ractice', content):
            best_practices_section = generate_best_practices_section(skill_name)
            content = content.rstrip() + '\n\n' + best_practices_section
            enhancements.append("Added best practices")
    
    if 'use-cases' in sections_to_enhance:
        if not re.search(r'##.*[Uu]se [Cc]ase', content):
            use_cases_section = generate_use_cases_section(skill_name)
            content = content.rstrip() + '\n\n' + use_cases_section
            enhancements.append("Added common use cases")
    
    # Write or preview changes
    if dry_run:
        return {
            "skill_name": skill_name,
            "dry_run": True,
            "enhancements": enhancements,
            "preview": content if enhancements else "No changes needed",
            "original_length": len(original_content),
            "new_length": len(content)
        }
    else:
        if enhancements:
            with open(skill_md_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return {
            "skill_name": skill_name,
            "enhancements": enhancements,
            "original_length": len(original_content),
            "new_length": len(content),
            "char_increase": len(content) - len(original_content)
        }


def main():
    parser = argparse.ArgumentParser(
        description="Enhance SKILL.md with missing content"
    )
    parser.add_argument(
        "skill_path",
        help="Path to the skill directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without writing"
    )
    parser.add_argument(
        "--sections",
        default="examples,scripts,best-practices,use-cases",
        help="Comma-separated list of sections to enhance"
    )
    
    args = parser.parse_args()
    
    sections_to_enhance = [s.strip() for s in args.sections.split(',')]
    
    result = enhance_skill(args.skill_path, sections_to_enhance, args.dry_run)
    
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result.get("enhancements"):
        print(f"\n✅ Enhanced {result['skill_name']} with {len(result['enhancements'])} improvements")
        print(f"   Character count: {result['original_length']} → {result['new_length']}")
    else:
        print(f"\nℹ️ No enhancements needed for {result['skill_name']}")


if __name__ == "__main__":
    main()