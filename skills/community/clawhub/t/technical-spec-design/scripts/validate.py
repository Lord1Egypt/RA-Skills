#!/usr/bin/env python3
"""
Skill Validator - Validate skill file integrity

Usage:
  python validate.py
  python validate.py --verbose
"""

import os
import sys
import re
from pathlib import Path
from typing import List


class ValidationResult:
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []


class SkillValidator:
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.result = ValidationResult()

    def validate_all(self) -> bool:
        print(f'Validating skill: {self.skill_path}')
        print('=' * 60)

        self._validate_structure()
        self._validate_skill_md()
        self._validate_frontmatter()
        self._validate_resources()
        self._validate_scripts()

        return self._report()

    def _validate_structure(self):
        self.result.info.append('Checking directory structure...')

        required_files = ['skill.md']
        optional_dirs = ['scripts', 'resources', 'examples']

        for file in required_files:
            file_path = self.skill_path / file
            if not file_path.exists():
                self.result.errors.append(f'Missing required file: {file}')

        for dir_name in optional_dirs:
            dir_path = self.skill_path / dir_name
            if dir_path.exists() and not dir_path.is_dir():
                self.result.errors.append(f'{dir_name} should be a directory')

    def _validate_skill_md(self):
        skill_md = self.skill_path / 'skill.md'
        if not skill_md.exists():
            return

        content = skill_md.read_text(encoding='utf-8')

        # Check for recommended sections (English)
        recommended_sections = [
            '# Overview',
            '## Usage',
            '## Common Mistakes',
        ]

        for section in recommended_sections:
            if section not in content:
                self.result.warnings.append(f'Consider adding section: {section}')

        # Check word count
        word_count = len(content.split())
        if word_count > 2000:
            self.result.warnings.append(
                f'skill.md has high word count ({word_count} words), consider splitting to resources/'
            )
        elif word_count < 100:
            self.result.warnings.append(
                f'skill.md has low word count ({word_count} words), may need more content'
            )

    def _validate_frontmatter(self):
        skill_md = self.skill_path / 'skill.md'
        if not skill_md.exists():
            return

        content = skill_md.read_text(encoding='utf-8')

        if not content.startswith('---'):
            self.result.errors.append(
                'skill.md missing YAML Frontmatter (must start with ---)'
            )
            return

        # Extract frontmatter
        fm_end = content.find('---', 4)
        if fm_end == -1:
            self.result.errors.append('YAML Frontmatter not properly closed')
            return

        frontmatter = content[4:fm_end]
        self._parse_yaml_frontmatter(frontmatter)

    def _parse_yaml_frontmatter(self, frontmatter: str):
        data = {}
        for line in frontmatter.split('\n'):
            match = re.match(r'^(\w+):\s*(.+)$', line)
            if match:
                data[match.group(1)] = match.group(2).strip()

        # Validate required fields
        if 'name' not in data:
            self.result.errors.append('Missing required field: name')
        elif not self._is_valid_skill_name(data['name']):
            self.result.errors.append(
                'Invalid name field format: only letters, numbers, and hyphens allowed'
            )

        if 'description' not in data:
            self.result.errors.append('Missing required field: description')
        else:
            desc = data['description']
            # Handle multi-line description
            desc_length = len(re.sub(r'\s+', ' ', desc).strip())

            if desc_length > 500:
                self.result.warnings.append(
                    f'description is long ({desc_length} chars), recommend keeping under 500'
                )

            # Check if starts with "Use when" or ">"
            first_line = desc.split('\n')[0].strip()
            if not first_line.startswith('Use when') and not first_line.startswith('>'):
                self.result.warnings.append(
                    "description should start with 'Use when'"
                )

    def _is_valid_skill_name(self, name: str) -> bool:
        return bool(re.match(r'^[a-z0-9-]+$', name))

    def _validate_resources(self):
        resources_dir = self.skill_path / 'resources'
        if not resources_dir.exists():
            return

        # Check for orphaned files
        referenced_files = set()
        skill_md = self.skill_path / 'skill.md'

        if skill_md.exists():
            content = skill_md.read_text(encoding='utf-8')
            # Simple link detection
            link_regex = r'\[([^\]]+)\]\(([^)]+)\)'
            for match in re.finditer(link_regex, content):
                url = match.group(2)
                filename = Path(url).name
                if url.startswith('resources/'):
                    referenced_files.add(filename)

        actual_files = set()
        for entry in resources_dir.iterdir():
            if entry.is_file():
                actual_files.add(entry.name)

        # Find unreferenced files
        unreferenced = actual_files - referenced_files
        if unreferenced:
            self.result.info.append(
                f'Files in resources/ not referenced by skill.md: {", ".join(unreferenced)}'
            )

    def _validate_scripts(self):
        scripts_dir = self.skill_path / 'scripts'
        if not scripts_dir.exists():
            return

        for entry in scripts_dir.iterdir():
            if entry.is_file() and entry.suffix in ('.py', '.sh'):
                content = entry.read_text(encoding='utf-8')
                if '__main__' in content or 'def main(' in content:
                    self.result.info.append(f'Executable script: {entry.name}')

    def _report(self) -> bool:
        print()

        if self.result.errors:
            print('❌ Errors:')
            for error in self.result.errors:
                print(f'  - {error}')
            print()

        if self.result.warnings:
            print('⚠️  Warnings:')
            for warning in self.result.warnings:
                print(f'  - {warning}')
            print()

        if self.result.info:
            print('ℹ️  Info:')
            for info in self.result.info:
                print(f'  - {info}')
            print()

        # Return validation result
        if self.result.errors:
            print('❌ Validation failed')
            return False
        else:
            print('✅ Validation passed')
            return True


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Skill Validator',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    # Default to parent directory of scripts
    skill_path = Path(__file__).parent.parent

    validator = SkillValidator(skill_path)
    success = validator.validate_all()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
