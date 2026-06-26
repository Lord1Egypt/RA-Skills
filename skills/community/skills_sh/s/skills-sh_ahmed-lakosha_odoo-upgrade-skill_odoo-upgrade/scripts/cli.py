#!/usr/bin/env python3
"""Unified CLI entry point for all Odoo upgrade operations."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog='odoo-upgrade',
        description='Odoo module upgrade toolkit (v5.1)',
    )
    sub = parser.add_subparsers(dest='command', help='Available commands')

    # precheck
    pc = sub.add_parser('precheck', help='Scan for compatibility issues (read-only)')
    pc.add_argument('path', help='Path to module or project')
    pc.add_argument('--target', type=int, default=19, choices=[14, 15, 16, 17, 18, 19])

    # validate
    vl = sub.add_parser('validate', help='Validate syntax of all files')
    vl.add_argument('path', help='Path to module or project')
    vl.add_argument('--verbose', action='store_true')

    # upgrade
    up = sub.add_parser('upgrade', help='Run full upgrade pipeline')
    up.add_argument('path', help='Path to module or project')
    up.add_argument('--target', type=int, default=19, choices=[14, 15, 16, 17, 18, 19])
    up.add_argument('--no-validation', action='store_true')

    # manifest
    mn = sub.add_parser('manifest', help='Update manifest files only')
    mn.add_argument('path', help='Path to module or project')
    mn.add_argument('--target', type=int, default=19, choices=[14, 15, 16, 17, 18, 19])

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == 'precheck':
        from .precheck import OdooPreChecker
        checker = OdooPreChecker(args.path, target_version=args.target)
        results = checker.run()
        sys.exit(1 if results['critical'] > 0 else 0)

    elif args.command == 'validate':
        from .validate import SyntaxValidator
        v = SyntaxValidator(args.path, verbose=args.verbose)
        results = v.validate_all()
        sys.exit(0 if results['valid'] else 1)

    elif args.command == 'upgrade':
        from .upgrade import OdooUpgrader
        upgrader = OdooUpgrader(
            args.path,
            target_version=args.target,
            validate=not args.no_validation,
        )
        upgrader.run()

    elif args.command == 'manifest':
        from .transforms.manifest import ManifestUpgrader
        upgrader = ManifestUpgrader(args.target)
        count = upgrader.process_project(args.path)
        print(f"Updated {count} manifests")


if __name__ == '__main__':
    main()
