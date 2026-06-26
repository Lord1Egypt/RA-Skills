#!/usr/bin/env python3
"""
create_skill.py - Skill factory for programmatic skill creation

Usage:
    python create_skill.py --config <config.json>
    python create_skill.py --name <name> --description <desc> --instructions <markdown>
    
The script creates a complete skill directory with SKILL.md and optional resources,
then validates and packages it.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


DEFAULT_OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "skills"
SKILL_CREATOR_DIR = Path("/app/skills/skill-creator")


def validate_skill_name(name: str) -> bool:
    """Validate skill name format: lowercase, digits, hyphens only, <64 chars."""
    if not name or len(name) >= 64:
        return False
    return all(c.islower() or c.isdigit() or c == '-' for c in name) and name[0].isalpha()


def create_skill_md(skill_name: str, description: str, instructions: str) -> str:
    """Generate SKILL.md content."""
    # Handle escaped newlines from command line
    instructions = instructions.replace('\\n', '\n')
    return f"""---
name: {skill_name}
description: {description}
---

{instructions}
"""


def create_skill(
    skill_name: str,
    description: str,
    instructions: str,
    scripts: Optional[list] = None,
    references: Optional[list] = None,
    assets: Optional[list] = None,
    output_dir: Optional[Path] = None,
    validate: bool = True,
    package: bool = True,
) -> dict:
    """
    Create a complete skill package.
    
    Returns a result dict with success status and created files.
    """
    result = {
        "success": False,
        "skill_path": None,
        "skill_file": None,
        "files_created": [],
        "errors": []
    }
    
    # Validate skill name
    if not validate_skill_name(skill_name):
        result["errors"].append(f"Invalid skill name: '{skill_name}'. Must be lowercase, digits, hyphens only, <64 chars, start with letter.")
        return result
    
    # Set output directory
    output_dir = Path(output_dir) if output_dir else DEFAULT_OUTPUT_DIR
    skill_path = output_dir / skill_name
    
    # Check if skill already exists
    if skill_path.exists():
        result["errors"].append(f"Skill already exists: {skill_path}")
        return result
    
    try:
        # Create directory structure
        skill_path.mkdir(parents=True, exist_ok=True)
        result["skill_path"] = str(skill_path)
        
        # Create SKILL.md
        skill_md_content = create_skill_md(skill_name, description, instructions)
        skill_md_path = skill_path / "SKILL.md"
        skill_md_path.write_text(skill_md_content, encoding="utf-8")
        result["files_created"].append("SKILL.md")
        
        # Create scripts
        if scripts:
            scripts_dir = skill_path / "scripts"
            scripts_dir.mkdir(exist_ok=True)
            for script in scripts:
                script_name = script.get("name", "script.py")
                script_content = script.get("content", "")
                script_path = scripts_dir / script_name
                script_path.write_text(script_content, encoding="utf-8")
                # Make executable if Python/Shell
                if script_name.endswith(('.py', '.sh')):
                    script_path.chmod(0o755)
                result["files_created"].append(f"scripts/{script_name}")
        
        # Create references
        if references:
            refs_dir = skill_path / "references"
            refs_dir.mkdir(exist_ok=True)
            for ref in references:
                ref_name = ref.get("name", "reference.md")
                ref_content = ref.get("content", "")
                ref_path = refs_dir / ref_name
                ref_path.write_text(ref_content, encoding="utf-8")
                result["files_created"].append(f"references/{ref_name}")
        
        # Create assets
        if assets:
            assets_dir = skill_path / "assets"
            assets_dir.mkdir(exist_ok=True)
            for asset in assets:
                asset_name = asset.get("name", "asset")
                asset_content = asset.get("content", "")
                asset_path = assets_dir / asset_name
                # Handle binary content (base64)
                if asset.get("encoding") == "base64":
                    import base64
                    asset_path.write_bytes(base64.b64decode(asset_content))
                else:
                    asset_path.write_text(asset_content, encoding="utf-8")
                result["files_created"].append(f"assets/{asset_name}")
        
        # Validate
        if validate:
            validate_script = SKILL_CREATOR_DIR / "scripts" / "package_skill.py"
            if validate_script.exists():
                proc = subprocess.run(
                    ["python3", str(validate_script), str(skill_path), "--validate-only"],
                    capture_output=True,
                    text=True
                )
                if proc.returncode != 0:
                    result["errors"].append(f"Validation failed: {proc.stderr}")
                    return result
        
        # Package
        if package:
            package_script = SKILL_CREATOR_DIR / "scripts" / "package_skill.py"
            if package_script.exists():
                proc = subprocess.run(
                    ["python3", str(package_script), str(skill_path), str(output_dir)],
                    capture_output=True,
                    text=True
                )
                if proc.returncode == 0:
                    result["skill_file"] = str(output_dir / f"{skill_name}.skill")
                else:
                    result["errors"].append(f"Packaging failed: {proc.stderr}")
        
        result["success"] = len(result["errors"]) == 0
        
    except Exception as e:
        result["errors"].append(str(e))
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Create a new skill")
    parser.add_argument("--config", type=str, help="Path to JSON config file")
    parser.add_argument("--name", type=str, help="Skill name")
    parser.add_argument("--description", type=str, help="Skill description")
    parser.add_argument("--instructions", type=str, help="Skill instructions (markdown)")
    parser.add_argument("--output-dir", type=str, help="Output directory")
    parser.add_argument("--no-validate", action="store_true", help="Skip validation")
    parser.add_argument("--no-package", action="store_true", help="Skip packaging")
    
    args = parser.parse_args()
    
    # Load config from file if provided
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {
            "skill_name": args.name,
            "description": args.description,
            "instructions": args.instructions,
            "output_dir": args.output_dir,
            "validate": not args.no_validate,
            "package": not args.no_package
        }
    
    # Validate required fields
    if not config.get("skill_name"):
        print("Error: skill_name is required", file=sys.stderr)
        sys.exit(1)
    if not config.get("description"):
        print("Error: description is required", file=sys.stderr)
        sys.exit(1)
    if not config.get("instructions"):
        print("Error: instructions is required", file=sys.stderr)
        sys.exit(1)
    
    # Create skill
    result = create_skill(
        skill_name=config["skill_name"],
        description=config["description"],
        instructions=config["instructions"],
        scripts=config.get("scripts"),
        references=config.get("references"),
        assets=config.get("assets"),
        output_dir=config.get("output_dir"),
        validate=config.get("validate", True),
        package=config.get("package", True)
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["success"] else 1)


if __name__ == "__main__":
    main()
