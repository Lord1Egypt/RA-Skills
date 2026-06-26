#!/usr/bin/env python3
"""
Skill Packager
Packages a skill folder into a Clawhub-ready zip archive.
"""

import os
import sys
import json
import zipfile
from pathlib import Path
from datetime import datetime

def validate_skill(skill_path: str) -> tuple:
    """
    Validate skill structure
    Returns (is_valid, errors)
    """
    errors = []
    path = Path(skill_path)
    
    # Check SKILL.md exists
    skill_md = path / "SKILL.md"
    if not skill_md.exists():
        errors.append("Missing SKILL.md")
    else:
        content = skill_md.read_text(encoding='utf-8')
        # Check YAML frontmatter
        if not content.startswith('---'):
            errors.append("SKILL.md missing YAML frontmatter")
        elif 'name:' not in content or 'description:' not in content:
            errors.append("SKILL.md missing required fields (name, description)")
    
    # Check manifest.json
    manifest_path = path / "manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            required = ['name', 'version', 'description']
            for field in required:
                if field not in manifest:
                    errors.append(f"manifest.json missing field: {field}")
        except json.JSONDecodeError:
            errors.append("manifest.json is not valid JSON")
    
    # Check for forbidden files
    forbidden = ['.git', '__pycache__', '.DS_Store', 'node_modules']
    for f in forbidden:
        if (path / f).exists():
            errors.append(f"Forbidden file/folder found: {f}")
    
    return (len(errors) == 0, errors)

def package_skill(skill_path: str, output_dir: str = None, version: str = None) -> str:
    """
    Package skill into zip file
    
    Returns path to generated zip file
    """
    path = Path(skill_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Skill path not found: {skill_path}")
    
    # Get skill name from manifest or folder name
    manifest_path = path / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        skill_name = manifest.get('name', path.name)
        skill_version = version or manifest.get('version', '1.0.0')
    else:
        skill_name = path.name
        skill_version = version or '1.0.0'
    
    # Output path
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = path.parent
    
    zip_filename = f"{skill_name}-v{skill_version}.zip"
    zip_path = output_path / zip_filename
    
    # Create zip
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in path.rglob('*'):
            if file_path.is_file():
                # Skip forbidden files
                if any(f in str(file_path) for f in ['.git', '__pycache__', '.DS_Store', 'node_modules']):
                    continue
                
                arcname = file_path.relative_to(path)
                zf.write(file_path, arcname)
    
    return str(zip_path)

def generate_upload_guide(skill_name: str, zip_path: str) -> str:
    """Generate Clawhub upload instructions"""
    return f"""
🎉 Skill Package Ready: {skill_name}

📦 File: {zip_path}

📋 Pre-Upload Checklist:
   ☐ Test the skill locally
   ☐ Review SKILL.md for accuracy
   ☐ Update manifest.json version
   ☐ Add any missing documentation

🚀 Upload to Clawhub:
   1. Visit: https://clawhub.com/upload
   2. Click "Upload Skill"
   3. Select: {zip_path}
   4. Fill in details:
      - Name: {skill_name}
      - Category: [选择合适分类]
      - Description: [复制SKILL.md里的description]
   5. Submit for review

📖 Local Testing:
   ```bash
   openclaw skill install ./{skill_name}
   ```

✨ Your skill will be available to the community after approval!
"""

def main():
    if len(sys.argv) < 2:
        print("Usage: package_skill.py <skill-folder> [output-dir] [version]")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    version = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"📦 Packaging skill: {skill_path}")
    
    # Validate
    is_valid, errors = validate_skill(skill_path)
    if not is_valid:
        print("❌ Validation failed:")
        for error in errors:
            print(f"   - {error}")
        sys.exit(1)
    
    print("✅ Validation passed")
    
    # Package
    try:
        zip_path = package_skill(skill_path, output_dir, version)
        print(f"✅ Created: {zip_path}")
        
        # Get skill name
        path = Path(skill_path)
        manifest_path = path / "manifest.json"
        skill_name = path.name
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text())
            skill_name = manifest.get('name', path.name)
        
        print(generate_upload_guide(skill_name, zip_path))
        
    except Exception as e:
        print(f"❌ Packaging failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
