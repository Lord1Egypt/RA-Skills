#!/usr/bin/env python3
"""JavaScript transformation functions for Odoo version upgrades."""

import re
from pathlib import Path

from ..utils import (
    iter_project_files, read_file_safe, write_file_safe,
    JSONRPC_HELPER_METHOD, JSONRPC_STANDALONE_FUNCTION,
)


class JsTransforms:
    """Consolidated JavaScript transformations for Odoo upgrades."""

    def __init__(self, project_path: str | Path, target_version: int = 19):
        self.project_path = Path(project_path)
        self.target_version = target_version
        self.files_modified: list[Path] = []

    def _apply_to_js_files(self, transform_fn, description: str) -> int:
        count = 0
        for js_file in iter_project_files(self.project_path, ('.js',)):
            content = read_file_safe(js_file)
            if content is None:
                continue
            try:
                new_content = transform_fn(content)
                if new_content != content:
                    if write_file_safe(js_file, new_content):
                        self.files_modified.append(js_file)
                        count += 1
            except Exception as e:
                print(f"  Error in {description} for {js_file.name}: {e}")
        return count

    def fix_rpc_service(self) -> int:
        """Replace useService("rpc") with fetch-based _jsonRpc helper."""
        def transform(content: str) -> str:
            # Remove import of jsonrpc from rpc_service module
            content = re.sub(
                r'import\s*\{\s*jsonrpc\s*\}\s*from\s*["\']@web/core/network/rpc_service["\'];?\s*\n?',
                '', content
            )

            # Remove useService("rpc") declaration
            content = re.sub(
                r'(\s*)this\.rpc\s*=\s*useService\(["\']rpc["\']\);?\s*\n?',
                r'\1// RPC service removed in Odoo 19 - using _jsonRpc helper\n',
                content
            )

            # Replace this.rpc() calls with this._jsonRpc()
            if 'this.rpc(' in content:
                content = content.replace('this.rpc(', 'this._jsonRpc(')

                # Add _jsonRpc method if not already present
                if '_jsonRpc(endpoint, params' not in content:
                    # Try to insert after setup() method
                    setup_match = re.search(r'setup\(\)\s*\{[^}]*\}', content)
                    if setup_match:
                        pos = setup_match.end()
                        content = content[:pos] + '\n' + JSONRPC_HELPER_METHOD + '\n' + content[pos:]
                    else:
                        # Try after class opening
                        class_match = re.search(r'export\s+class\s+\w+\s+extends\s+\w+\s*\{', content)
                        if class_match:
                            pos = class_match.end()
                            content = content[:pos] + '\n' + JSONRPC_HELPER_METHOD + '\n' + content[pos:]

            # Handle standalone jsonrpc import replacement
            if 'import {jsonrpc}' in content and JSONRPC_STANDALONE_FUNCTION not in content:
                import_end = max(content.rfind('import '), 0)
                if import_end > 0:
                    line_end = content.find('\n', import_end)
                    if line_end > 0:
                        content = content[:line_end + 1] + '\n' + JSONRPC_STANDALONE_FUNCTION + '\n' + content[line_end + 1:]

            return content
        return self._apply_to_js_files(transform, "rpc-service")

    def fix_module_declaration(self) -> int:
        """Add missing /** @odoo-module **/ annotation."""
        def transform(content: str) -> str:
            if content.strip() and not content.strip().startswith('/** @odoo-module'):
                content = '/** @odoo-module **/\n\n' + content
            return content
        return self._apply_to_js_files(transform, "module-declaration")

    def fix_owl_lifecycle_hooks(self) -> int:
        """Rename OWL 1.x lifecycle methods to OWL 2.0 equivalents."""
        renames = [
            (r'\bmounted\s*\(\s*\)\s*\{', 'onMounted() {'),
            (r'\bwillStart\s*\(\s*\)\s*\{', 'onWillStart() {'),
            (r'\bpatched\s*\(\s*\)\s*\{', 'onPatched() {'),
            (r'\bwillUnmount\s*\(\s*\)\s*\{', 'onWillUnmount() {'),
            (r'\bwillUpdateProps\s*\(\s*\)\s*\{', 'onWillUpdateProps() {'),
            (r'\bconstructor\s*\(\s*parent\s*,\s*props\s*\)\s*\{', 'setup() {'),
        ]

        def transform(content: str) -> str:
            if 'Component' not in content:
                return content
            for pattern, replacement in renames:
                content = re.sub(pattern, replacement, content)
            return content
        return self._apply_to_js_files(transform, "owl-lifecycle")

    def apply_all(self) -> dict[str, int]:
        """Apply all applicable JavaScript transformations based on target version."""
        results = {}

        # Always safe
        results['module_declaration'] = self.fix_module_declaration()

        # Odoo 18+ transforms
        if self.target_version >= 18:
            results['owl_lifecycle'] = self.fix_owl_lifecycle_hooks()

        # Odoo 19+ transforms
        if self.target_version >= 19:
            results['rpc_service'] = self.fix_rpc_service()

        return results

    def apply_all_odoo19(self) -> dict[str, int]:
        """Deprecated: use apply_all() instead."""
        return self.apply_all()
