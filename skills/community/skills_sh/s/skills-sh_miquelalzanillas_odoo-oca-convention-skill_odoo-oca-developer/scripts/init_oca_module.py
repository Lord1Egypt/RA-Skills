#!/usr/bin/env python3
"""
Script to initialize a new Odoo module following OCA conventions.
Usage: python init_oca_module.py <module_name> [--path <target_directory>]
"""
import argparse
import os
import shutil
import sys
from pathlib import Path


def snake_case_to_title(snake_str):
    """Convert snake_case to Title Case"""
    return ' '.join(word.capitalize() for word in snake_str.split('_'))


def create_odoo_module(module_name, target_path, odoo_version="17.0"):
    """Create a new Odoo module structure following OCA conventions"""
    
    # Get the skill directory (parent of scripts/)
    skill_dir = Path(__file__).parent.parent
    template_dir = skill_dir / "assets" / "module_template"
    
    if not template_dir.exists():
        print(f"Error: Template directory not found at {template_dir}")
        return False
    
    # Create target directory
    module_path = Path(target_path) / module_name
    if module_path.exists():
        print(f"Error: Directory {module_path} already exists")
        return False
    
    print(f"Creating Odoo module: {module_name}")
    print(f"Target path: {module_path}")
    print(f"Odoo version: {odoo_version}")
    
    # Copy template
    shutil.copytree(template_dir, module_path)
    
    # Replace placeholders in files
    replacements = {
        '{MODULE_NAME}': module_name,
        '{MODULE_TITLE}': snake_case_to_title(module_name),
        '{ODOO_VERSION}': odoo_version,
    }
    
    # Files to process
    files_to_process = [
        '__manifest__.py',
        'README.rst',
        'readme/DESCRIPTION.rst',
    ]
    
    for file_name in files_to_process:
        file_path = module_path / file_name
        if file_path.exists():
            with open(file_path, 'r') as f:
                content = f.read()
            
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            with open(file_path, 'w') as f:
                f.write(content)
    
    print(f"\n✅ Module '{module_name}' created successfully!")
    print(f"\nNext steps:")
    print(f"1. Edit {module_name}/__manifest__.py to complete module information")
    print(f"2. Add your models in {module_name}/models/")
    print(f"3. Add your views in {module_name}/views/")
    print(f"4. Update readme/ files with module documentation")
    print(f"5. Run pre-commit to generate README.rst")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Initialize a new Odoo module following OCA conventions'
    )
    parser.add_argument(
        'module_name',
        help='Name of the module to create (snake_case)'
    )
    parser.add_argument(
        '--path',
        default='.',
        help='Target directory where the module will be created (default: current directory)'
    )
    parser.add_argument(
        '--version',
        default='17.0',
        help='Odoo version (default: 17.0)'
    )
    
    args = parser.parse_args()
    
    # Validate module name
    if not args.module_name.replace('_', '').replace('-', '').isalnum():
        print("Error: Module name must contain only letters, numbers, and underscores")
        return 1
    
    # Create module
    success = create_odoo_module(
        args.module_name,
        args.path,
        args.version
    )
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
