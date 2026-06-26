#!/usr/bin/env python3
"""
Syntax validator for Odoo modules.
Validates Python (AST), XML (ElementTree), JavaScript (bracket balance), and SCSS files.
"""

import ast
import re
import sys
import os
from pathlib import Path
from typing import List, Tuple
from collections import defaultdict
import xml.etree.ElementTree as ET

from .utils import iter_project_files, read_file_safe


class SyntaxValidator:
    """Multi-format syntax validator for Odoo modules."""

    def __init__(self, project_path: str | Path, verbose: bool = False):
        self.project_path = Path(project_path)
        self.verbose = verbose
        self.errors: dict[str, list[str]] = defaultdict(list)
        self.warnings: dict[str, list[str]] = defaultdict(list)

    def validate_python(self, file_path: Path) -> Tuple[bool, List[str]]:
        errors = []
        content = read_file_safe(file_path)
        if content is None:
            return False, ["Failed to read file"]
        try:
            ast.parse(content, filename=str(file_path))
        except SyntaxError as e:
            errors.append(f"Line {e.lineno}: {e.msg}")
        return len(errors) == 0, errors

    def validate_xml(self, file_path: Path) -> Tuple[bool, List[str]]:
        errors = []
        content = read_file_safe(file_path)
        if content is None:
            return False, ["Failed to read file"]
        # Clean for parsing
        clean = content
        def fix_hyphens(m):
            inner = m.group(0)[4:-3]
            inner = re.sub(r'--+', '- -', inner)
            return f'<!--{inner}-->'
        clean = re.sub(r'<!--.*?-->', fix_hyphens, clean, flags=re.DOTALL)
        if not clean.strip().startswith('<odoo'):
            clean = f'<odoo>{clean}</odoo>'
        try:
            ET.fromstring(clean)
        except ET.ParseError as e:
            errors.append(f"XML parsing error: {e}")
        return len(errors) == 0, errors

    def validate_javascript(self, file_path: Path) -> Tuple[bool, List[str]]:
        errors = []
        content = read_file_safe(file_path)
        if content is None:
            return False, ["Failed to read file"]
        # Check bracket balance (strip strings/comments)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'"[^"]*"', '""', cleaned)
        cleaned = re.sub(r"'[^']*'", "''", cleaned)
        cleaned = re.sub(r'`[^`]*`', '``', cleaned)
        brackets = {'(': ')', '[': ']', '{': '}'}
        stack = []
        for ch in cleaned:
            if ch in brackets:
                stack.append(ch)
            elif ch in brackets.values():
                if not stack:
                    errors.append(f"Unmatched closing bracket '{ch}'")
                    break
                opening = stack.pop()
                if brackets[opening] != ch:
                    errors.append(f"Mismatched brackets: '{opening}' and '{ch}'")
                    break
        if stack:
            errors.append(f"Unclosed brackets: {stack}")
        return len(errors) == 0, errors

    def validate_scss(self, file_path: Path) -> Tuple[bool, List[str]]:
        errors = []
        content = read_file_safe(file_path)
        if content is None:
            return False, ["Failed to read file"]
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
        opens = cleaned.count('{')
        closes = cleaned.count('}')
        if opens != closes:
            errors.append(f"Unbalanced braces: {opens} opening, {closes} closing")
        return len(errors) == 0, errors

    def validate_all(self) -> dict:
        """Validate all files. Returns summary dict."""
        stats = {'errors': 0, 'warnings': 0, 'files': 0}

        for py in iter_project_files(self.project_path, ('.py',)):
            stats['files'] += 1
            ok, errs = self.validate_python(py)
            if not ok:
                rel = py.relative_to(self.project_path)
                for e in errs:
                    self.errors['python'].append(f"{rel}: {e}")
                stats['errors'] += 1

        for xml in iter_project_files(self.project_path, ('.xml',)):
            stats['files'] += 1
            ok, errs = self.validate_xml(xml)
            if not ok:
                rel = xml.relative_to(self.project_path)
                for e in errs:
                    self.errors['xml'].append(f"{rel}: {e}")
                stats['errors'] += 1

        for js in iter_project_files(self.project_path, ('.js',)):
            stats['files'] += 1
            ok, errs = self.validate_javascript(js)
            if not ok:
                rel = js.relative_to(self.project_path)
                for e in errs:
                    self.errors['js'].append(f"{rel}: {e}")
                stats['errors'] += 1

        for scss in iter_project_files(self.project_path, ('.scss',)):
            stats['files'] += 1
            ok, errs = self.validate_scss(scss)
            if not ok:
                rel = scss.relative_to(self.project_path)
                for e in errs:
                    self.errors['scss'].append(f"{rel}: {e}")
                stats['errors'] += 1

        return {
            'valid': stats['errors'] == 0,
            'errors': dict(self.errors),
            'stats': stats,
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.validate <project_path> [--verbose]")
        sys.exit(1)
    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist")
        sys.exit(1)
    v = SyntaxValidator(path, verbose='--verbose' in sys.argv)
    results = v.validate_all()
    if results['valid']:
        print("Validation passed - no syntax errors")
    else:
        print(f"Validation failed - {results['stats']['errors']} file(s) with errors")
        for ftype, errs in results['errors'].items():
            for e in errs:
                print(f"  [{ftype}] {e}")
    sys.exit(0 if results['valid'] else 1)


if __name__ == '__main__':
    main()
