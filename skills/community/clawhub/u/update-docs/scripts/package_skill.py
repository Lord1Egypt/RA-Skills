#!/usr/bin/env python3
"""
Package the update-docs skill into a distributable .skill file.

This script validates the skill structure and creates a compressed .skill file
that can be shared and installed by other OpenClaw instances.
"""

import os
import sys
import json
import zipfile
import argparse
from pathlib import Path

def validate_skill_structure(skill_path):
    """Validate that the skill has the required structure."""
    skill_path = Path(skill_path)
    
    # Check required files
    required_files = ["SKILL.md"]
    for file in required_files:
        if not (skill_path / file).exists():
            print(f"Error: Missing required file: {file}", file=sys.stderr)
            return False
    
    # Check SKILL.md frontmatter
    try:
        with open(skill_path / "SKILL.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Simple frontmatter validation
        if not content.startswith("---"):
            print("Error: SKILL.md missing frontmatter", file=sys.stderr)
            return False
        
        # Extract frontmatter
        end_marker = content.find("\n---", 3)
        if end_marker == -1:
            print("Error: SKILL.md frontmatter not properly closed", file=sys.stderr)
            return False
        
        frontmatter = content[3:end_marker]
        if "name:" not in frontmatter or "description:" not in frontmatter:
            print("Error: SKILL.md frontmatter missing name or description", file=sys.stderr)
            return False
            
    except Exception as e:
        print(f"Error reading SKILL.md: {e}", file=sys.stderr)
        return False
    
    # Check directory structure
    allowed_dirs = {"scripts", "references", "assets"}
    for item in skill_path.iterdir():
        if item.is_dir() and item.name not in allowed_dirs:
            print(f"Warning: Unexpected directory: {item.name}", file=sys.stderr)
    
    print("✓ Skill structure validation passed")
    return True

def get_skill_name(skill_path):
    """Extract skill name from SKILL.md frontmatter."""
    with open(Path(skill_path) / "SKILL.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    start = content.find("---") + 3
    end = content.find("\n---", start)
    frontmatter = content[start:end]
    
    for line in frontmatter.split("\n"):
        if line.strip().startswith("name:"):
            return line.strip().split(":", 1)[1].strip().strip('"\'')
    
    return None

def package_skill(skill_path, output_dir=None):
    """Package the skill into a .skill file."""
    skill_path = Path(skill_path)
    
    if not validate_skill_structure(skill_path):
        return False
    
    skill_name = get_skill_name(skill_path)
    if not skill_name:
        print("Error: Could not extract skill name from SKILL.md", file=sys.stderr)
        return False
    
    # Determine output path
    if output_dir:
        output_path = Path(output_dir) / f"{skill_name}.skill"
    else:
        output_path = skill_path.parent / f"{skill_name}.skill"
    
    # Create zip file
    print(f"Creating {output_path}...")
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                if file.endswith(".pyc") or file == "__pycache__":
                    continue
                
                file_path = Path(root) / file
                arcname = file_path.relative_to(skill_path.parent)
                zf.write(file_path, arcname)
                print(f"  Added: {arcname}")
    
    print(f"✓ Successfully created {output_path}")
    print(f"Skill '{skill_name}' is ready for distribution!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Package update-docs skill")
    parser.add_argument("skill_path", help="Path to the skill directory")
    parser.add_argument("output_dir", nargs="?", help="Output directory for .skill file")
    
    args = parser.parse_args()
    
    success = package_skill(args.skill_path, args.output_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()