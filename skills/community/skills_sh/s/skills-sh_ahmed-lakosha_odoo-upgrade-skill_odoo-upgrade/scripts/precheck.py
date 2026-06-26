#!/usr/bin/env python3
"""
Pre-upgrade compatibility scanner for Odoo modules.
Read-only analysis that identifies version compatibility issues without modifying files.
"""

import re
import sys
import os
from pathlib import Path
from typing import List, Tuple
from collections import defaultdict

from .utils import iter_project_files, read_file_safe


# Issue severity levels
CRITICAL = 'CRITICAL'  # Installation will fail
HIGH = 'HIGH'          # Will likely cause errors
MEDIUM = 'MEDIUM'      # Should fix for compatibility
LOW = 'LOW'            # Minor, optional


class OdooPreChecker:
    """Non-destructive compatibility scanner for Odoo version upgrades."""

    def __init__(self, project_path: str | Path, target_version: int = 19):
        self.project_path = Path(project_path)
        self.target_version = target_version
        self.issues: list[tuple[str, str, str, str]] = []  # (severity, file, line, message)

    def _add_issue(self, severity: str, filepath: Path, line: int, message: str):
        rel = filepath.relative_to(self.project_path) if filepath.is_relative_to(self.project_path) else filepath
        self.issues.append((severity, str(rel), str(line), message))

    def check_xml_files(self) -> int:
        count = 0
        for xml_file in iter_project_files(self.project_path, ('.xml',)):
            content = read_file_safe(xml_file)
            if not content:
                continue
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                # Odoo 19+ checks
                if self.target_version >= 19:
                    if '<tree' in line and '<!--' not in line:
                        self._add_issue(CRITICAL, xml_file, i, '<tree> tag must be <list> in Odoo 19')
                        count += 1
                    if re.search(r'<group[^>]*expand', line):
                        self._add_issue(CRITICAL, xml_file, i, '<group expand> not allowed in search views (Odoo 19)')
                        count += 1
                    if 't-name="kanban-box"' in line:
                        self._add_issue(HIGH, xml_file, i, 'kanban-box must be renamed to card (Odoo 19)')
                        count += 1
                    if re.search(r'<field\s+name=["\']numbercall', line):
                        self._add_issue(HIGH, xml_file, i, 'numbercall field removed in Odoo 19')
                        count += 1
                    if 'active_id' in line and 'context=' in line:
                        self._add_issue(MEDIUM, xml_file, i, 'active_id should be replaced with id (Odoo 19)')
                        count += 1
                    if re.search(r'xpath[^>]*//tree', line):
                        self._add_issue(CRITICAL, xml_file, i, 'XPath //tree must be //list (Odoo 19)')
                        count += 1
                    if re.search(r'view_mode["\']?\s*[:>]\s*["\']?[^"\']*tree', line):
                        self._add_issue(CRITICAL, xml_file, i, 'view_mode tree must be list (Odoo 19)')
                        count += 1
                    if 'inherit_id="website.snippet_options"' in line:
                        self._add_issue(HIGH, xml_file, i, 'website.snippet_options removed in Odoo 19')
                        count += 1
                    if re.search(r'format_(datetime|date|amount)\(env,', line):
                        self._add_issue(CRITICAL, xml_file, i, 'format helper: remove env parameter (Odoo 19)')
                        count += 1

                # Odoo 18+ checks
                if self.target_version >= 18:
                    if re.search(r'attrs\s*=\s*["\']\{', line):
                        self._add_issue(HIGH, xml_file, i, 'attrs={} syntax deprecated, use inline expressions (Odoo 18+)')
                        count += 1

                # Odoo 15+ checks (Bootstrap 4 -> 5)
                if self.target_version >= 15:
                    for old_cls in ('class="ml-', 'class="mr-', 'class="pl-', 'class="pr-'):
                        if old_cls in line:
                            self._add_issue(MEDIUM, xml_file, i, f'Bootstrap 4 class detected, use ms-/me-/ps-/pe- (Odoo 15+)')
                            count += 1
                            break
        return count

    def check_python_files(self) -> int:
        count = 0
        for py_file in iter_project_files(self.project_path, ('.py',)):
            content = read_file_safe(py_file)
            if not content:
                continue
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                # All versions: ancient openerp imports
                if self.target_version >= 15:
                    if 'from openerp' in line:
                        self._add_issue(CRITICAL, py_file, i, "Deprecated 'openerp' import, use 'odoo'")
                        count += 1

                # Odoo 19+ checks
                if self.target_version >= 19:
                    if re.search(r"type\s*=\s*['\"]json['\"]", line) and '@http.route' in content[max(0, content.find(line)-200):content.find(line)+len(line)]:
                        self._add_issue(HIGH, py_file, i, "type='json' should be type='jsonrpc' (Odoo 19)")
                        count += 1
                    if re.search(r"view_mode.*tree", line) and 'view_mode' in line:
                        self._add_issue(MEDIUM, py_file, i, "view_mode 'tree' should be 'list' (Odoo 19)")
                        count += 1

                # Odoo 18+ checks
                if self.target_version >= 18:
                    if 'from odoo.addons.http_routing' in line and 'slug' in line:
                        self._add_issue(HIGH, py_file, i, 'slug import location changed (Odoo 18+)')
                        count += 1
        return count

    def check_javascript_files(self) -> int:
        count = 0
        for js_file in iter_project_files(self.project_path, ('.js',)):
            content = read_file_safe(js_file)
            if not content:
                continue
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                # Odoo 19+ checks
                if self.target_version >= 19:
                    if re.search(r'useService\(["\']rpc["\']\)', line):
                        self._add_issue(CRITICAL, js_file, i, 'RPC service not available in Odoo 19 frontend')
                        count += 1
                    if '@web/core/network/rpc_service' in line:
                        self._add_issue(CRITICAL, js_file, i, 'RPC service module removed in Odoo 19')
                        count += 1

                # Odoo 18+ checks (OWL lifecycle)
                if self.target_version >= 18:
                    if re.search(r'\bmounted\s*\(\s*\)', line) and 'Component' in content:
                        self._add_issue(HIGH, js_file, i, 'OWL 1.x lifecycle: mounted() -> onMounted() (Odoo 18+)')
                        count += 1
                    if re.search(r'\bwillStart\s*\(\s*\)', line) and 'Component' in content:
                        self._add_issue(HIGH, js_file, i, 'OWL 1.x lifecycle: willStart() -> onWillStart() (Odoo 18+)')
                        count += 1

            if content.strip() and not content.strip().startswith('/** @odoo-module'):
                self._add_issue(LOW, js_file, 1, 'Missing @odoo-module declaration')
                count += 1
        return count

    def check_scss_files(self) -> int:
        count = 0
        deprecated_vars = {
            '$headings-font-weight': '$o-theme-headings-font-weight',
            '$font-size-base': '$o-theme-font-size-base',
        }
        for scss_file in iter_project_files(self.project_path, ('.scss',)):
            content = read_file_safe(scss_file)
            if not content:
                continue
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if self.target_version >= 19:
                    for old, new in deprecated_vars.items():
                        if old in line:
                            self._add_issue(MEDIUM, scss_file, i, f"Deprecated '{old}', use '{new}' (Odoo 19)")
                            count += 1
        return count

    def run(self) -> dict:
        """Run all checks. Returns summary dict."""
        print(f"\nScanning: {self.project_path} (target: Odoo {self.target_version})\n")

        xml_issues = self.check_xml_files()
        py_issues = self.check_python_files()
        js_issues = self.check_javascript_files()
        scss_issues = self.check_scss_files()

        total = xml_issues + py_issues + js_issues + scss_issues

        # Group by severity
        by_severity = defaultdict(list)
        for sev, filepath, line, msg in self.issues:
            by_severity[sev].append((filepath, line, msg))

        # Print results
        for sev in (CRITICAL, HIGH, MEDIUM, LOW):
            items = by_severity.get(sev, [])
            if items:
                print(f"\n[{sev}] ({len(items)} issues)")
                for filepath, line, msg in items:
                    print(f"  {filepath}:{line} - {msg}")

        if total == 0:
            print("\nNo compatibility issues found.")
        else:
            critical = len(by_severity.get(CRITICAL, []))
            print(f"\nTotal: {total} issues ({critical} critical)")

        return {
            'total': total,
            'critical': len(by_severity.get(CRITICAL, [])),
            'high': len(by_severity.get(HIGH, [])),
            'medium': len(by_severity.get(MEDIUM, [])),
            'low': len(by_severity.get(LOW, [])),
            'issues': self.issues,
        }


# Backward compatibility alias
Odoo19PreChecker = OdooPreChecker


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.precheck <project_path> [--target VERSION]")
        sys.exit(1)

    project_path = sys.argv[1]
    if not os.path.exists(project_path):
        print(f"Error: Path '{project_path}' does not exist")
        sys.exit(1)

    target = 19
    if '--target' in sys.argv:
        idx = sys.argv.index('--target')
        if idx + 1 < len(sys.argv):
            target = int(sys.argv[idx + 1])

    checker = OdooPreChecker(project_path, target_version=target)
    results = checker.run()
    sys.exit(1 if results['critical'] > 0 else 0)


if __name__ == '__main__':
    main()
