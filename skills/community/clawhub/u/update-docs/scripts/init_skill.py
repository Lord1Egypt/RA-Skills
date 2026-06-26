#!/usr/bin/env python3
"""
Initialize the update-docs skill structure.
"""

import os
import sys
import argparse
from pathlib import Path

def create_skill_structure(base_path):
    """Create the complete skill directory structure."""
    directories = [
        "scripts",
        "references", 
        "assets"
    ]
    
    for dir_name in directories:
        dir_path = base_path / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"Created directory: {dir_path}")
    
    # Create placeholder files if they don't exist
    placeholder_files = {
        "scripts/__init__.py": "# Skill scripts\n",
        "references/__init__.md": "# Reference documentation\n",
        "assets/__init__.md": "# Asset templates\n"
    }
    
    for file_path, content in placeholder_files.items():
        full_path = base_path / file_path
        if not full_path.exists():
            with open(full_path, 'w') as f:
                f.write(content)
            print(f"Created placeholder: {full_path}")

def main():
    parser = argparse.ArgumentParser(description="Initialize update-docs skill structure")
    parser.add_argument("skill_path", help="Path to the skill directory")
    
    args = parser.parse_args()
    
    skill_path = Path(args.skill_path)
    skill_path.mkdir(exist_ok=True)
    
    create_skill_structure(skill_path)
    print(f"Skill structure initialized at: {skill_path}")

if __name__ == "__main__":
    main()