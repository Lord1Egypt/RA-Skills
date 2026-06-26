#!/usr/bin/env python3
"""
Code Review - Main Entry Point

Commands:
  review file <path>      - Review a single file
  review diff <file>      - Review a diff/patch file
  review staged           - Review staged changes
  review commit <sha>     - Review a commit
  report                  - Generate formatted report
"""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent


def run_review_file(args):
    """Review one or more files"""
    sys.path.insert(0, str(SCRIPT_DIR))
    from analyzer import ReviewEngine

    engine = ReviewEngine({
        'max_complexity': args.max_complexity,
        'max_function_lines': args.max_function_lines,
        'max_file_lines': args.max_file_lines,
    })

    filepaths = [Path(f) for f in args.files]
    report = engine.review_files(filepaths)

    output = engine.format_report(report, args.format)

    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"Report saved to: {args.output}")
    else:
        print(output)

    # Exit with error code if there are errors
    if report.summary.get('errors', 0) > 0 and args.fail_on_error:
        sys.exit(1)


def run_review_staged(args):
    """Review staged git changes"""
    # Get list of staged files
    result = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Error: Not a git repository or git error")
        sys.exit(1)

    files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]

    if not files:
        print("No staged files to review")
        return

    print(f"Reviewing {len(files)} staged file(s)...")

    # Run review on staged files
    sys.path.insert(0, str(SCRIPT_DIR))
    from analyzer import ReviewEngine

    engine = ReviewEngine({
        'max_complexity': args.max_complexity,
        'max_function_lines': args.max_function_lines,
        'max_file_lines': args.max_file_lines,
    })

    filepaths = [Path(f) for f in files if Path(f).exists()]
    report = engine.review_files(filepaths)

    output = engine.format_report(report, args.format)

    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"\nReport saved to: {args.output}")
    else:
        print(output)

    # Exit with error code if there are errors
    if report.summary.get('errors', 0) > 0 and args.fail_on_error:
        sys.exit(1)


def run_review_commit(args):
    """Review a specific commit"""
    # Get files changed in commit
    result = subprocess.run(
        ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', args.commit],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Error: Could not get commit {args.commit}")
        sys.exit(1)

    files = [f.strip() for f in result.stdout.strip().split('\n') if f.strip()]

    if not files:
        print(f"No files in commit {args.commit}")
        return

    print(f"Reviewing commit {args.commit}: {len(files)} file(s)")

    # Run review
    sys.path.insert(0, str(SCRIPT_DIR))
    from analyzer import ReviewEngine

    engine = ReviewEngine({
        'max_complexity': args.max_complexity,
        'max_function_lines': args.max_function_lines,
        'max_file_lines': args.max_file_lines,
    })

    filepaths = [Path(f) for f in files if Path(f).exists()]
    report = engine.review_files(filepaths)

    output = engine.format_report(report, args.format)

    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f"\nReport saved to: {args.output}")
    else:
        print(output)


def run_review_diff(args):
    """Review a diff/patch file"""
    # For now, just review the file as-is
    # Future: parse diff to only review changed lines
    print("Reviewing diff file (reviewing entire files in diff)...")
    run_review_file(args)


def main():
    parser = argparse.ArgumentParser(
        description='Code Review - Automated code quality checks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py review file src/main.py
  python3 main.py review file src/*.py --format json
  python3 main.py review staged
  python3 main.py review commit abc123
  python3 main.py review file src/ --fail-on-error
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # review subcommand
    review_parser = subparsers.add_parser('review', help='Review code')
    review_subparsers = review_parser.add_subparsers(dest='review_type', help='Review type')

    # review file
    file_parser = review_subparsers.add_parser('file', help='Review files')
    file_parser.add_argument('files', nargs='+', help='Files to review')
    file_parser.add_argument('--format', '-f', choices=['md', 'json'], default='md')
    file_parser.add_argument('--output', '-o', help='Output file')
    file_parser.add_argument('--max-complexity', type=int, default=10)
    file_parser.add_argument('--max-function-lines', type=int, default=50)
    file_parser.add_argument('--max-file-lines', type=int, default=500)
    file_parser.add_argument('--fail-on-error', action='store_true',
                            help='Exit with error code if issues found')
    file_parser.set_defaults(func=run_review_file)

    # review staged
    staged_parser = review_subparsers.add_parser('staged', help='Review staged changes')
    staged_parser.add_argument('--format', '-f', choices=['md', 'json'], default='md')
    staged_parser.add_argument('--output', '-o', help='Output file')
    staged_parser.add_argument('--max-complexity', type=int, default=10)
    staged_parser.add_argument('--max-function-lines', type=int, default=50)
    staged_parser.add_argument('--max-file-lines', type=int, default=500)
    staged_parser.add_argument('--fail-on-error', action='store_true')
    staged_parser.set_defaults(func=run_review_staged)

    # review commit
    commit_parser = review_subparsers.add_parser('commit', help='Review a commit')
    commit_parser.add_argument('commit', help='Commit SHA')
    commit_parser.add_argument('--format', '-f', choices=['md', 'json'], default='md')
    commit_parser.add_argument('--output', '-o', help='Output file')
    commit_parser.add_argument('--max-complexity', type=int, default=10)
    commit_parser.add_argument('--max-function-lines', type=int, default=50)
    commit_parser.add_argument('--max-file-lines', type=int, default=500)
    commit_parser.add_argument('--fail-on-error', action='store_true')
    commit_parser.set_defaults(func=run_review_commit)

    # review diff
    diff_parser = review_subparsers.add_parser('diff', help='Review a diff file')
    diff_parser.add_argument('files', nargs='+', help='Diff files to review')
    diff_parser.add_argument('--format', '-f', choices=['md', 'json'], default='md')
    diff_parser.add_argument('--output', '-o', help='Output file')
    diff_parser.add_argument('--max-complexity', type=int, default=10)
    diff_parser.add_argument('--max-function-lines', type=int, default=50)
    diff_parser.add_argument('--max-file-lines', type=int, default=500)
    diff_parser.add_argument('--fail-on-error', action='store_true')
    diff_parser.set_defaults(func=run_review_diff)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == 'review' and args.review_type is None:
        review_parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()
