#!/usr/bin/env python3
"""Python transformation functions for Odoo version upgrades."""

import re
from pathlib import Path

from ..utils import iter_project_files, read_file_safe, write_file_safe


class PyTransforms:
    """Consolidated Python transformations for Odoo upgrades."""

    def __init__(self, project_path: str | Path, target_version: int = 19):
        self.project_path = Path(project_path)
        self.target_version = target_version
        self.files_modified: list[Path] = []

    def _apply_to_py_files(self, transform_fn, description: str) -> int:
        count = 0
        for py_file in iter_project_files(self.project_path, ('.py',)):
            content = read_file_safe(py_file)
            if content is None:
                continue
            try:
                new_content = transform_fn(content)
                if new_content != content:
                    if write_file_safe(py_file, new_content):
                        self.files_modified.append(py_file)
                        count += 1
            except Exception as e:
                print(f"  Error in {description} for {py_file.name}: {e}")
        return count

    def fix_imports(self) -> int:
        """Fix deprecated import paths (openerp -> odoo, slug/unslug, url_for)."""
        patterns = [
            (r'from openerp import', 'from odoo import'),
            (r'import openerp', 'import odoo'),
            (r'from odoo\.addons\.http_routing\.models\.ir_http import slug',
             'from odoo.http import request\n\ndef slug(value):\n    """Compatibility wrapper for slug function"""\n    return request.env[\'ir.http\']._slug(value)'),
            (r'from odoo\.addons\.http_routing\.models\.ir_http import url_for',
             '# url_for removed - use self.env["ir.http"]._url_for() instead'),
        ]

        def transform(content: str) -> str:
            for pattern, replacement in patterns:
                content = re.sub(pattern, replacement, content)
            return content
        return self._apply_to_py_files(transform, "python-imports")

    def fix_controller_type(self) -> int:
        """Convert type='json' to type='jsonrpc' in @http.route decorators (Odoo 19)."""
        route_pattern = re.compile(
            r"(@http\.route\([^)]*?)type\s*=\s*['\"]json['\"]([^)]*\))",
            re.DOTALL,
        )

        def transform(content: str) -> str:
            return route_pattern.sub(
                lambda m: m.group(1) + "type='jsonrpc'" + m.group(2),
                content,
            )
        return self._apply_to_py_files(transform, "controller-type")

    def fix_view_mode_tree(self) -> int:
        """Replace 'tree' with 'list' in view_mode values in Python code."""
        def transform(content: str) -> str:
            content = re.sub(r"(['\"]view_mode['\"]:\s*['\"])tree(['\"])", r"\1list\2", content)
            content = re.sub(r"(['\"]view_mode['\"]:\s*['\"])tree,", r"\1list,", content)
            content = re.sub(r",tree([,'\"])", r",list\1", content)
            content = re.sub(r"(['\"]view_type['\"]:\s*['\"])tree(['\"])", r"\1list\2", content)
            return content
        return self._apply_to_py_files(transform, "view-mode-tree")

    def fix_url_for_usage(self) -> int:
        """Replace url_for() calls with self.env['ir.http']._url_for()."""
        def transform(content: str) -> str:
            content = re.sub(
                r'from\s+odoo\.addons\.http_routing\.models\.ir_http\s+import\s+url_for',
                '', content
            )
            content = re.sub(r'\burl_for\(', r"self.env['ir.http']._url_for(", content)
            return content
        return self._apply_to_py_files(transform, "url-for")

    def apply_all(self) -> dict[str, int]:
        """Apply all applicable Python transformations based on target version."""
        results = {}

        # Always applicable (openerp -> odoo)
        results['imports'] = self.fix_imports()

        # Odoo 19+ transforms
        if self.target_version >= 19:
            results['controller_type'] = self.fix_controller_type()
            results['view_mode_tree'] = self.fix_view_mode_tree()
            results['url_for'] = self.fix_url_for_usage()

        return results

    def apply_all_odoo19(self) -> dict[str, int]:
        """Deprecated: use apply_all() instead."""
        return self.apply_all()
