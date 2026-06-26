#!/usr/bin/env python3
"""
Validate Claude skill structure and YAML frontmatter
Checks for:
  - Correct folder naming (kebab-case)
  - SKILL.md exists
  - Valid YAML frontmatter
  - Required fields
  - No XML angle brackets
"""

import os
import sys
import re
import yaml

def check_folder_name(folder_path):
    """Check folder name is kebab-case"""
    folder_name = os.path.basename(folder_path)
    if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', folder_name):
        return False, f"Invalid folder name: '{folder_name}' (use kebab-case)"
    return True, "Folder name valid"

def check_skill_md_exists(folder_path):
    """Check SKILL.md exists"""
    skill_file = os.path.join(folder_path, 'SKILL.md')
    if not os.path.exists(skill_file):
        return False, "SKILL.md not found"
    return True, "SKILL.md exists"

def extract_frontmatter(content):
    """Extract and validate YAML frontmatter"""
    if not content.startswith('---'):
        return False, None, "Frontmatter must start with ---"
    
    try:
        end_idx = content.find('---', 3)
        if end_idx == -1:
            return False, None, "Frontmatter must end with ---"
        
        yaml_content = content[3:end_idx].strip()
        data = yaml.safe_load(yaml_content)
        return True, data, "Frontmatter valid"
    except yaml.YAMLError as e:
        return False, None, f"YAML error: {str(e)}"

def validate_frontmatter(metadata):
    """Check required fields"""
    errors = []
    
    if 'name' not in metadata:
        errors.append("Missing 'name' field")
    elif not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', metadata['name']):
        errors.append(f"Invalid 'name': {metadata['name']} (use kebab-case)")
    
    if 'description' not in metadata:
        errors.append("Missing 'description' field")
    elif len(metadata['description']) > 1024:
        errors.append(f"Description too long: {len(metadata['description'])} > 1024")
    
    return errors

def check_no_xml_brackets(content):
    """Check no XML in frontmatter"""
    frontmatter_end = content.find('---', 3)
    if frontmatter_end != -1:
        frontmatter = content[:frontmatter_end + 3]
        if '<' in frontmatter or '>' in frontmatter:
            return False, "XML brackets < > found in frontmatter"
    return True, "No XML brackets"

def validate_skill(folder_path):
    """Run all validation checks"""
    print(f"\n{'='*60}")
    print(f"Validating skill: {folder_path}")
    print(f"{'='*60}\n")
    
    all_passed = True
    
    # Check 1: Folder name
    passed, msg = check_folder_name(folder_path)
    status = "✓" if passed else "✗"
    print(f"{status} Folder name: {msg}")
    all_passed = all_passed and passed
    
    # Check 2: SKILL.md exists
    passed, msg = check_skill_md_exists(folder_path)
    status = "✓" if passed else "✗"
    print(f"{status} SKILL.md: {msg}")
    all_passed = all_passed and passed
    
    if not passed:
        print(f"\n✗ Validation failed: SKILL.md not found")
        return False
    
    # Read SKILL.md
    skill_file = os.path.join(folder_path, 'SKILL.md')
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"✗ Cannot read SKILL.md: {e}")
        return False
    
    # Check 3: Frontmatter
    passed, metadata, msg = extract_frontmatter(content)
    status = "✓" if passed else "✗"
    print(f"{status} YAML Frontmatter: {msg}")
    all_passed = all_passed and passed
    
    if not passed:
        print(f"\n✗ Validation failed: {msg}")
        return False
    
    # Check 4: Required fields
    errors = validate_frontmatter(metadata)
    if errors:
        print("✗ Frontmatter fields:")
        for error in errors:
            print(f"    - {error}")
        all_passed = False
    else:
        print("✓ Frontmatter fields: Valid")
    
    # Check 5: XML brackets
    passed, msg = check_no_xml_brackets(content)
    status = "✓" if passed else "✗"
    print(f"{status} No XML brackets: {msg}")
    all_passed = all_passed and passed
    
    # Summary
    print(f"\n{'='*60}")
    if all_passed:
        print("✅ Validation PASSED - Ready to upload!")
    else:
        print("❌ Validation FAILED - Fix issues above")
    print(f"{'='*60}\n")
    
    return all_passed

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_skill.py <skill_folder>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a directory")
        sys.exit(1)
    
    success = validate_skill(folder_path)
    sys.exit(0 if success else 1)
