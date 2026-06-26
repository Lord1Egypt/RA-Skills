#!/usr/bin/env python3
"""
Text Diff - Show line-by-line differences between two text files.

Usage:
    python text_diff.py unified <file1> <file2> [-c context] [-o output]
    python text_diff.py context <file1> <file2> [-c context] [-o output]
    python text_diff.py side-by-side <file1> <file2> [-o output] [--no-color]
"""

import argparse
import difflib
import sys
from pathlib import Path


# ANSI color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def read_file(filepath):
    """Read a file and return list of lines."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()


def write_output(content, destination=None):
    """Write output to file or stdout."""
    if destination:
        Path(destination).write_text(content, encoding='utf-8')
        print(f"Diff written to: {destination}")
    else:
        print(content, end='')


def colorize_line(line, color, use_color=True):
    """Add color to a line if color is enabled."""
    if not use_color:
        return line
    return f"{color}{line}{Colors.RESET}"


def unified_diff(file1, file2, context=3, use_color=True):
    """Generate unified diff between two files."""
    lines1 = read_file(file1)
    lines2 = read_file(file2)

    diff = list(difflib.unified_diff(
        lines1, lines2,
        fromfile=file1,
        tofile=file2,
        n=context
    ))

    if not diff:
        return "", False

    result = []
    for line in diff:
        if line.startswith('---'):
            result.append(colorize_line(line, Colors.CYAN, use_color))
        elif line.startswith('+++'):
            result.append(colorize_line(line, Colors.CYAN, use_color))
        elif line.startswith('@@'):
            result.append(colorize_line(line, Colors.YELLOW, use_color))
        elif line.startswith('-'):
            result.append(colorize_line(line, Colors.RED, use_color))
        elif line.startswith('+'):
            result.append(colorize_line(line, Colors.GREEN, use_color))
        else:
            result.append(line)

    return ''.join(result), True


def context_diff(file1, file2, context=3, use_color=True):
    """Generate context diff between two files."""
    lines1 = read_file(file1)
    lines2 = read_file(file2)

    diff = list(difflib.context_diff(
        lines1, lines2,
        fromfile=file1,
        tofile=file2,
        n=context
    ))

    if not diff:
        return "", False

    result = []
    for line in diff:
        if line.startswith('***'):
            result.append(colorize_line(line, Colors.CYAN, use_color))
        elif line.startswith('---'):
            result.append(colorize_line(line, Colors.CYAN, use_color))
        elif line.startswith('***************'):
            result.append(colorize_line(line, Colors.YELLOW, use_color))
        elif line.startswith('---'):
            result.append(colorize_line(line, Colors.YELLOW, use_color))
        elif line.startswith('- '):
            result.append(colorize_line(line, Colors.RED, use_color))
        elif line.startswith('+ '):
            result.append(colorize_line(line, Colors.GREEN, use_color))
        elif line.startswith('! '):
            result.append(colorize_line(line, Colors.YELLOW, use_color))
        else:
            result.append(line)

    return ''.join(result), True


def side_by_side_diff(file1, file2, use_color=True):
    """Generate side-by-side comparison of two files."""
    lines1 = read_file(file1)
    lines2 = read_file(file2)

    # Normalize line endings
    lines1 = [line.rstrip('\n') for line in lines1]
    lines2 = [line.rstrip('\n') for line in lines2]

    # Calculate column width
    max_len1 = max(len(line) for line in lines1) if lines1 else 0
    max_len2 = max(len(line) for line in lines2) if lines2 else 0
    col_width = max(max_len1, max_len2, 40)

    differ = difflib.Differ()
    diff = list(differ.compare(lines1, lines2))

    result = []
    header = f"{'OLD':{col_width}} | {'NEW':{col_width}}\n"
    separator = f"{'-' * col_width}-+-{'-' * col_width}\n"

    result.append(colorize_line(header, Colors.BOLD + Colors.CYAN, use_color))
    result.append(separator)

    has_differences = False

    for line in diff:
        if line.startswith('  '):
            # Unchanged line
            content = line[2:]
            result.append(f"{content:{col_width}} | {content:{col_width}}\n")
        elif line.startswith('- '):
            # Removed line
            has_differences = True
            content = line[2:]
            left = colorize_line(f"{content:{col_width}}", Colors.RED, use_color)
            right = " " * col_width
            result.append(f"{left} | {right}\n")
        elif line.startswith('+ '):
            # Added line
            has_differences = True
            content = line[2:]
            left = " " * col_width
            right = colorize_line(f"{content:{col_width}}", Colors.GREEN, use_color)
            result.append(f"{left} | {right}\n")
        elif line.startswith('? '):
            # Difference indicator (skip, already shown above)
            continue

    return ''.join(result), has_differences


def cmd_unified(args):
    """Handle unified diff command."""
    try:
        diff_output, has_diff = unified_diff(
            args.file1, args.file2,
            context=args.context,
            use_color=not args.no_color
        )
        write_output(diff_output, args.output)
        return 1 if has_diff else 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3


def cmd_context(args):
    """Handle context diff command."""
    try:
        diff_output, has_diff = context_diff(
            args.file1, args.file2,
            context=args.context,
            use_color=not args.no_color
        )
        write_output(diff_output, args.output)
        return 1 if has_diff else 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3


def cmd_side_by_side(args):
    """Handle side-by-side diff command."""
    try:
        diff_output, has_diff = side_by_side_diff(
            args.file1, args.file2,
            use_color=not args.no_color
        )
        write_output(diff_output, args.output)
        return 1 if has_diff else 0
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3


def main():
    parser = argparse.ArgumentParser(
        description="Show line-by-line differences between text files",
        prog="text_diff.py"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Unified diff command
    unified_parser = subparsers.add_parser("unified", help="Show unified diff")
    unified_parser.add_argument("file1", help="First file to compare")
    unified_parser.add_argument("file2", help="Second file to compare")
    unified_parser.add_argument("-c", "--context", type=int, default=3,
                                help="Number of context lines (default: 3)")
    unified_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    unified_parser.add_argument("--no-color", action="store_true",
                                help="Disable colored output")

    # Context diff command
    context_parser = subparsers.add_parser("context", help="Show context diff")
    context_parser.add_argument("file1", help="First file to compare")
    context_parser.add_argument("file2", help="Second file to compare")
    context_parser.add_argument("-c", "--context", type=int, default=3,
                                help="Number of context lines (default: 3)")
    context_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    context_parser.add_argument("--no-color", action="store_true",
                                help="Disable colored output")

    # Side-by-side diff command
    side_parser = subparsers.add_parser("side-by-side", help="Show side-by-side comparison")
    side_parser.add_argument("file1", help="First file to compare")
    side_parser.add_argument("file2", help="Second file to compare")
    side_parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    side_parser.add_argument("--no-color", action="store_true",
                             help="Disable colored output")

    args = parser.parse_args()

    if args.command == "unified":
        return cmd_unified(args)
    elif args.command == "context":
        return cmd_context(args)
    elif args.command == "side-by-side":
        return cmd_side_by_side(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
