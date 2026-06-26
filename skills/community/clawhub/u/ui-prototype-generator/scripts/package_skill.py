#!/usr/bin/env python3
"""
Package the ui-prototype-generator skill into a distributable .skill file.

Usage:
    python3 package_skill.py
    python3 package_skill.py ./dist
"""

import os
import sys
import zipfile
from pathlib import Path

def package_skill(skill_dir, output_dir=None):
    """Package the skill into a .skill file."""
    skill_dir = Path(skill_dir)
    
    # Determine output directory
    if output_dir is None:
        output_dir = skill_dir.parent
    else:
        output_dir = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get skill name from directory
    skill_name = skill_dir.name
    
    # Create output filename
    output_file = output_dir / f"{skill_name}.skill"
    
    # Create zip file
    try:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files in skill directory
            for root, dirs, files in os.walk(skill_dir):
                # Skip hidden files and directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                files = [f for f in files if not f.startswith('.')]
                
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(skill_dir.parent)
                    zipf.write(file_path, arcname)
        
        print(f"✓ Skill packaged successfully: {output_file}")
        print(f"  File size: {output_file.stat().st_size / 1024:.1f} KB")
        
        # List contents
        print("\nPackage contents:")
        with zipfile.ZipFile(output_file, 'r') as zipf:
            for name in zipf.namelist():
                print(f"  - {name}")
        
        return True
        
    except Exception as e:
        print(f"Error creating package: {e}")
        return False

def main():
    # Get skill directory (parent of scripts directory)
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    
    # Check if we're in the right place
    if not (skill_dir / "SKILL.md").exists():
        print("Error: This script should be run from within a skill directory")
        print(f"SKILL.md not found in {skill_dir}")
        sys.exit(1)
    
    # Parse command line arguments
    output_dir = None
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    
    print(f"Packaging skill: {skill_dir.name}")
    print("=" * 50)
    
    # Package skill
    if package_skill(skill_dir, output_dir):
        print("\n✓ Packaging complete!")
        
        # Installation instructions
        print("\nTo install this skill:")
        print(f"1. Copy {skill_dir.name}.skill to your OpenClaw skills directory")
        print(f"2. Run: openclaw skills install <path-to-skill-file>")
        print(f"3. Restart OpenClaw or reload skills")
        
        print(f"\nTo publish to ClawHub:")
        print(f"1. Create account at https://clawhub.com")
        print(f"2. Upload {skill_dir.name}.skill")
        print(f"3. Add description, tags, and documentation")
        
    else:
        print("\n✗ Packaging failed.")
        sys.exit(1)

if __name__ == '__main__':
    main()