#!/usr/bin/env python3
"""
Script to validate Odoo module structure against OCA conventions.
Usage: python validate_module.py <module_path>
"""
import argparse
import sys
from pathlib import Path


def validate_manifest(module_path):
    """Validate __manifest__.py file"""
    manifest_path = module_path / '__manifest__.py'
    
    if not manifest_path.exists():
        return ["❌ __manifest__.py not found"]
    
    errors = []
    
    try:
        with open(manifest_path, 'r') as f:
            content = f.read()
            manifest = eval(content)
        
        # Check required keys
        required_keys = ['name', 'version', 'license', 'author', 'depends']
        for key in required_keys:
            if key not in manifest:
                errors.append(f"❌ Missing required key in __manifest__.py: {key}")
        
        # Check author includes OCA
        if 'author' in manifest:
            if 'Odoo Community Association (OCA)' not in manifest['author']:
                errors.append("⚠️  Author should include 'Odoo Community Association (OCA)'")
        
        # Check license
        if 'license' in manifest:
            if manifest['license'] not in ['AGPL-3', 'LGPL-3']:
                errors.append(f"⚠️  License '{manifest['license']}' is not standard for OCA (use AGPL-3 or LGPL-3)")
        
        # Check version format
        if 'version' in manifest:
            version_parts = manifest['version'].split('.')
            if len(version_parts) != 5:
                errors.append(f"⚠️  Version format should be x.y.z.w.v (e.g., 17.0.1.0.0), got: {manifest['version']}")
        
        if not errors:
            errors.append("✅ __manifest__.py is valid")
    
    except Exception as e:
        errors.append(f"❌ Error reading __manifest__.py: {e}")
    
    return errors


def validate_structure(module_path):
    """Validate module directory structure"""
    errors = []
    
    # Check required files
    required_files = ['__init__.py', '__manifest__.py']
    for file_name in required_files:
        if not (module_path / file_name).exists():
            errors.append(f"❌ Missing required file: {file_name}")
    
    # Check if README.rst exists (should be auto-generated)
    if (module_path / 'README.rst').exists():
        errors.append("✅ README.rst found")
    else:
        errors.append("⚠️  README.rst not found (should be auto-generated from readme/ folder)")
    
    # Check readme/ folder
    readme_dir = module_path / 'readme'
    if readme_dir.exists():
        if (readme_dir / 'DESCRIPTION.rst').exists():
            errors.append("✅ readme/DESCRIPTION.rst found")
        else:
            errors.append("⚠️  readme/DESCRIPTION.rst not found")
    else:
        errors.append("⚠️  readme/ folder not found")
    
    # Check common directories
    common_dirs = ['models', 'views', 'security']
    existing_dirs = [d for d in common_dirs if (module_path / d).exists()]
    if existing_dirs:
        errors.append(f"✅ Found directories: {', '.join(existing_dirs)}")
    
    return errors


def validate_naming(module_path):
    """Validate file naming conventions"""
    errors = []
    
    # Check models directory
    models_dir = module_path / 'models'
    if models_dir.exists():
        for py_file in models_dir.glob('*.py'):
            if py_file.name != '__init__.py':
                if not py_file.name.islower():
                    errors.append(f"⚠️  Model file should be lowercase: {py_file.name}")
                if '-' in py_file.name:
                    errors.append(f"⚠️  Use underscores instead of hyphens: {py_file.name}")
    
    # Check views directory
    views_dir = module_path / 'views'
    if views_dir.exists():
        for xml_file in views_dir.glob('*.xml'):
            if not xml_file.name.endswith('_views.xml'):
                errors.append(f"⚠️  View files should end with '_views.xml': {xml_file.name}")
    
    if not errors:
        errors.append("✅ File naming conventions are correct")
    
    return errors


def validate_module(module_path):
    """Validate entire module"""
    module_path = Path(module_path)
    
    if not module_path.exists():
        print(f"❌ Module path does not exist: {module_path}")
        return False
    
    if not module_path.is_dir():
        print(f"❌ Module path is not a directory: {module_path}")
        return False
    
    print(f"Validating module: {module_path.name}")
    print("=" * 60)
    
    all_valid = True
    
    # Validate manifest
    print("\n📄 Manifest Validation")
    print("-" * 60)
    for msg in validate_manifest(module_path):
        print(msg)
        if msg.startswith("❌"):
            all_valid = False
    
    # Validate structure
    print("\n📁 Structure Validation")
    print("-" * 60)
    for msg in validate_structure(module_path):
        print(msg)
        if msg.startswith("❌"):
            all_valid = False
    
    # Validate naming
    print("\n📝 Naming Convention Validation")
    print("-" * 60)
    for msg in validate_naming(module_path):
        print(msg)
        if msg.startswith("❌"):
            all_valid = False
    
    print("\n" + "=" * 60)
    if all_valid:
        print("✅ Module validation passed!")
    else:
        print("❌ Module validation found errors")
    
    return all_valid


def main():
    parser = argparse.ArgumentParser(
        description='Validate Odoo module against OCA conventions'
    )
    parser.add_argument(
        'module_path',
        help='Path to the module to validate'
    )
    
    args = parser.parse_args()
    
    success = validate_module(args.module_path)
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
