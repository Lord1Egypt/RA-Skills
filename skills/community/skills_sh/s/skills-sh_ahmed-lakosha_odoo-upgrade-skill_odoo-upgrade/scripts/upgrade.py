#!/usr/bin/env python3
"""
Main Odoo upgrade orchestrator.
Coordinates backup, transforms, and validation for version migrations.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

from .utils import create_backup
from .transforms import XmlTransforms, JsTransforms, PyTransforms, ManifestUpgrader
from .validate import SyntaxValidator
from .precheck import OdooPreChecker


class OdooUpgrader:
    """Orchestrates the full upgrade workflow."""

    def __init__(self, project_path: str | Path, target_version: int = 19,
                 validate: bool = True):
        self.project_path = Path(project_path)
        self.target_version = target_version
        self.validate = validate
        self.report: list[str] = []
        self.backup_path = None

    def run(self) -> dict:
        """Execute the full upgrade pipeline."""
        print(f"\nOdoo Upgrade: {self.project_path.name} -> v{self.target_version}")
        print("=" * 60)

        # Step 1: Backup
        print("\n[1/6] Creating backup...")
        self.backup_path = create_backup(self.project_path)
        self.report.append(f"Backup: {self.backup_path}")

        # Step 2: Pre-check
        print("\n[2/6] Pre-upgrade scan...")
        checker = OdooPreChecker(self.project_path, target_version=self.target_version)
        pre_results = checker.run()
        self.report.append(f"Pre-check: {pre_results['total']} issues ({pre_results['critical']} critical)")

        # Step 3: Manifests
        print("\n[3/6] Updating manifests...")
        manifest_upgrader = ManifestUpgrader(self.target_version)
        manifest_count = manifest_upgrader.process_project(self.project_path)
        self.report.append(f"Manifests updated: {manifest_count}")

        # Step 4: XML transforms
        print("\n[4/6] Applying XML transforms...")
        xml = XmlTransforms(self.project_path, target_version=self.target_version)
        xml_results = xml.apply_all()
        xml_total = sum(xml_results.values())
        self.report.append(f"XML files modified: {xml_total}")

        # Step 5: Python + JS transforms
        print("\n[5/6] Applying Python & JS transforms...")
        py = PyTransforms(self.project_path, target_version=self.target_version)
        py_results = py.apply_all()
        py_total = sum(py_results.values())

        js = JsTransforms(self.project_path, target_version=self.target_version)
        js_results = js.apply_all()
        js_total = sum(js_results.values())

        self.report.append(f"Python files modified: {py_total}")
        self.report.append(f"JavaScript files modified: {js_total}")

        # Step 6: Post-validation
        post_results = None
        if self.validate:
            print("\n[6/6] Post-upgrade validation...")
            validator = SyntaxValidator(self.project_path)
            post_results = validator.validate_all()
            if post_results['valid']:
                print("  Validation PASSED")
                self.report.append("Post-validation: PASSED")
            else:
                err_count = post_results['stats']['errors']
                print(f"  Validation found {err_count} file(s) with errors")
                self.report.append(f"Post-validation: {err_count} error(s)")
        else:
            print("\n[6/6] Skipping validation")

        # Generate report
        self._write_report()

        total_modified = xml_total + py_total + js_total + manifest_count
        print(f"\nUpgrade complete: {total_modified} files modified")
        print(f"Backup at: {self.backup_path}")

        return {
            'manifests': manifest_count,
            'xml': xml_results,
            'python': py_results,
            'javascript': js_results,
            'validation': post_results,
            'total_modified': total_modified,
        }

    def _write_report(self):
        report_path = self.project_path / "MIGRATION_REPORT.md"
        lines = [
            f"# Odoo {self.target_version} Migration Report",
            f"\n**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**Project**: {self.project_path.name}",
            "\n## Summary",
        ]
        for item in self.report:
            lines.append(f"- {item}")
        lines.append("\n## Next Steps")
        lines.append("1. Review all modified files")
        lines.append("2. Test module installation")
        lines.append("3. Verify all views load correctly")
        lines.append("4. Test JavaScript components")

        report_path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"\nReport: {report_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.upgrade <project_path> [--no-validation] [--target VERSION]")
        sys.exit(1)

    project_path = sys.argv[1]
    if not os.path.exists(project_path):
        print(f"Error: Path '{project_path}' does not exist")
        sys.exit(1)

    validate = '--no-validation' not in sys.argv
    target = 19
    if '--target' in sys.argv:
        idx = sys.argv.index('--target')
        if idx + 1 < len(sys.argv):
            target = int(sys.argv[idx + 1])

    upgrader = OdooUpgrader(project_path, target_version=target, validate=validate)
    upgrader.run()


if __name__ == '__main__':
    main()
