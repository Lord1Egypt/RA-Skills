#!/usr/bin/env python3
"""Manifest file upgrade utilities for Odoo version migrations."""

import ast
import os
import re
from pathlib import Path
from typing import Optional

from ..utils import read_file_safe, write_file_safe


# Supported Odoo version prefixes
VERSION_MAP = {
    '14': '14.0', '15': '15.0', '16': '16.0',
    '17': '17.0', '18': '18.0', '19': '19.0',
}

# Common external Python dependencies found in Odoo modules
KNOWN_EXTERNAL_DEPS = {
    'geopy', 'spacy', 'hachoir', 'PIL', 'numpy', 'pandas',
    'matplotlib', 'seaborn', 'requests', 'xlsxwriter', 'xlrd',
}

# Preferred key ordering for manifest output
MANIFEST_KEY_ORDER = [
    'name', 'version', 'summary', 'category', 'author',
    'website', 'support', 'license', 'contributors', 'depends',
    'data', 'assets', 'external_dependencies',
    'installable', 'auto_install', 'application',
]


class ManifestUpgrader:
    """Upgrade __manifest__.py files for a target Odoo version."""

    def __init__(self, target_version: int | str):
        self.target_version = str(target_version)

    def get_version_string(self, current_version: Optional[str] = None) -> str:
        base = VERSION_MAP.get(self.target_version, f'{self.target_version}.0')
        if current_version and '.' in str(current_version):
            parts = str(current_version).split('.')
            if len(parts) >= 3:
                return f"{base}.{parts[-3]}.{parts[-2]}.{parts[-1]}"
        return f"{base}.1.0.0"

    def read_manifest(self, file_path: str | Path) -> tuple[dict, str]:
        """Parse a manifest file. Returns (dict, raw_content)."""
        content = read_file_safe(file_path) or ''
        try:
            manifest = ast.literal_eval(content)
            return manifest, content
        except Exception:
            # Fallback: extract key fields with regex
            manifest = {}
            for key in ('name', 'version', 'license', 'category', 'author'):
                m = re.search(rf"['\"]({key})['\"]\s*:\s*['\"]([^'\"]+)['\"]", content)
                if m:
                    manifest[m.group(1)] = m.group(2)
            return manifest, content

    def update_manifest(self, manifest: dict, module_path: Path) -> tuple[dict, list[str]]:
        """Apply required updates to the manifest dict. Returns (updated_manifest, changes)."""
        changes = []

        old_version = manifest.get('version', '1.0')
        new_version = self.get_version_string(old_version)
        if old_version != new_version:
            manifest['version'] = new_version
            changes.append(f"Version: {old_version} -> {new_version}")

        if 'license' not in manifest:
            manifest['license'] = 'LGPL-3'
            changes.append("Added license: LGPL-3")

        if 'installable' not in manifest:
            manifest['installable'] = True
            changes.append("Added installable: True")

        if 'auto_install' not in manifest:
            manifest['auto_install'] = False
            changes.append("Added auto_install: False")

        # Detect external deps
        ext_deps = self._scan_external_deps(module_path)
        if ext_deps and 'external_dependencies' not in manifest:
            manifest['external_dependencies'] = {'python': ext_deps}
            changes.append(f"Added external dependencies: {ext_deps}")

        return manifest, changes

    def _scan_external_deps(self, module_path: Path) -> list[str]:
        found = set()
        for py_file in module_path.rglob('*.py'):
            if '__pycache__' in str(py_file):
                continue
            content = read_file_safe(py_file)
            if not content:
                continue
            for dep in KNOWN_EXTERNAL_DEPS:
                if f'import {dep}' in content or f'from {dep}' in content:
                    found.add(dep)
        return sorted(found)

    def _format_value(self, value, indent: int = 4) -> str:
        pad = ' ' * indent
        inner_pad = ' ' * (indent + 4)
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, bool):
            return 'True' if value else 'False'
        elif isinstance(value, list):
            items = [self._format_value(item, indent + 4) for item in value]
            return '[\n' + inner_pad + (',\n' + inner_pad).join(items) + ',\n' + pad + ']'
        elif isinstance(value, dict):
            items = [f"'{k}': {self._format_value(v, indent + 4)}" for k, v in value.items()]
            return '{\n' + inner_pad + (',\n' + inner_pad).join(items) + ',\n' + pad + '}'
        return str(value)

    def write_manifest(self, manifest: dict, file_path: str | Path) -> None:
        lines = ["# -*- coding: utf-8 -*-", "{"]
        for key in MANIFEST_KEY_ORDER:
            if key in manifest:
                lines.append(f"    '{key}': {self._format_value(manifest[key])},")
        for key, value in manifest.items():
            if key not in MANIFEST_KEY_ORDER:
                lines.append(f"    '{key}': {self._format_value(value)},")
        lines.append("}\n")
        write_file_safe(file_path, '\n'.join(lines))

    def process_module(self, module_path: str | Path) -> bool:
        """Upgrade a single module's manifest. Returns True if processed."""
        module_path = Path(module_path)
        manifest_path = module_path / '__manifest__.py'
        if not manifest_path.exists():
            return False

        manifest, original = self.read_manifest(manifest_path)
        updated, changes = self.update_manifest(manifest, module_path)

        if changes:
            # Backup
            backup_path = str(manifest_path) + '.backup'
            write_file_safe(backup_path, original)
            self.write_manifest(updated, manifest_path)
            print(f"  Updated {module_path.name}: {', '.join(changes)}")

        return True

    def process_project(self, project_path: str | Path) -> int:
        """Upgrade all module manifests in a project directory. Returns count."""
        count = 0
        for root, dirs, files in os.walk(project_path):
            if '__manifest__.py' in files:
                if self.process_module(root):
                    count += 1
        return count
