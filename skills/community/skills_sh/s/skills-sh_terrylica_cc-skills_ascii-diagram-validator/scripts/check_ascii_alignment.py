#!/usr/bin/env python3
# /// script
# dependencies = []
# ///
"""
ASCII Diagram Alignment Validator

Validates alignment of box-drawing characters in enclosed box diagrams.
Skips file tree structures (├── patterns) and handles arrow characters.
Outputs issues in compiler-like format: file:line:column: severity: message

Usage:
    uv run check_ascii_alignment.py <file_or_directory> [--warn-only] [--verbose]

Examples:
    uv run check_ascii_alignment.py docs/ARCHITECTURE.md
    uv run check_ascii_alignment.py docs/*.md
    uv run check_ascii_alignment.py docs/ --verbose
"""
import argparse
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# Box-drawing character sets
# Light (single) lines
SINGLE_HORIZONTAL = set('─')
SINGLE_VERTICAL = set('│')
# Double lines
DOUBLE_HORIZONTAL = set('═')
DOUBLE_VERTICAL = set('║')
# Heavy (bold) lines - used by graph-easy boxart
HEAVY_HORIZONTAL = set('━')
HEAVY_VERTICAL = set('┃')

HORIZONTAL = SINGLE_HORIZONTAL | DOUBLE_HORIZONTAL | HEAVY_HORIZONTAL
VERTICAL = SINGLE_VERTICAL | DOUBLE_VERTICAL | HEAVY_VERTICAL

# Corners - Light
CORNER_TL_LIGHT = set('┌')
CORNER_TR_LIGHT = set('┐')
CORNER_BL_LIGHT = set('└')
CORNER_BR_LIGHT = set('┘')
# Corners - Double
CORNER_TL_DOUBLE = set('╔')
CORNER_TR_DOUBLE = set('╗')
CORNER_BL_DOUBLE = set('╚')
CORNER_BR_DOUBLE = set('╝')
# Corners - Heavy (bold) - used by graph-easy boxart
CORNER_TL_HEAVY = set('┏')
CORNER_TR_HEAVY = set('┓')
CORNER_BL_HEAVY = set('┗')
CORNER_BR_HEAVY = set('┛')
# Corners - Rounded (arc) - used by graph-easy shape: rounded
CORNER_TL_ROUNDED = set('╭')
CORNER_TR_ROUNDED = set('╮')
CORNER_BL_ROUNDED = set('╰')
CORNER_BR_ROUNDED = set('╯')

CORNER_TL = CORNER_TL_LIGHT | CORNER_TL_DOUBLE | CORNER_TL_HEAVY | CORNER_TL_ROUNDED
CORNER_TR = CORNER_TR_LIGHT | CORNER_TR_DOUBLE | CORNER_TR_HEAVY | CORNER_TR_ROUNDED
CORNER_BL = CORNER_BL_LIGHT | CORNER_BL_DOUBLE | CORNER_BL_HEAVY | CORNER_BL_ROUNDED
CORNER_BR = CORNER_BR_LIGHT | CORNER_BR_DOUBLE | CORNER_BR_HEAVY | CORNER_BR_ROUNDED
CORNERS = CORNER_TL | CORNER_TR | CORNER_BL | CORNER_BR

# T-junctions - Light
T_LEFT_LIGHT = set('├')
T_RIGHT_LIGHT = set('┤')
T_TOP_LIGHT = set('┬')
T_BOTTOM_LIGHT = set('┴')
# T-junctions - Double
T_LEFT_DOUBLE = set('╠╞╟')
T_RIGHT_DOUBLE = set('╣╡╢')
T_TOP_DOUBLE = set('╦╤╥')
T_BOTTOM_DOUBLE = set('╩╧╨')
# T-junctions - Heavy (bold) - used by graph-easy boxart
T_LEFT_HEAVY = set('┣┡┢┝┞┟┠')
T_RIGHT_HEAVY = set('┫┥┦┧┨┩┪')
T_TOP_HEAVY = set('┳┭┮┯┰┱┲')
T_BOTTOM_HEAVY = set('┻┵┶┷┸┹┺')

T_LEFT = T_LEFT_LIGHT | T_LEFT_DOUBLE | T_LEFT_HEAVY
T_RIGHT = T_RIGHT_LIGHT | T_RIGHT_DOUBLE | T_RIGHT_HEAVY
T_TOP = T_TOP_LIGHT | T_TOP_DOUBLE | T_TOP_HEAVY
T_BOTTOM = T_BOTTOM_LIGHT | T_BOTTOM_DOUBLE | T_BOTTOM_HEAVY
T_JUNCTIONS = T_LEFT | T_RIGHT | T_TOP | T_BOTTOM

# Crosses - Light, Double, Heavy
CROSSES = set('┼╬╪╫╋')

# Arrow characters (valid terminators for lines)
# Includes graph-easy arrows: ∨∧ (mathematical symbols used as arrows)
ARROWS = set('▶▷►▻▸▹→⟶⟹▼▽▾▿↓⇓◀◁◄◅◂◃←⟵⟸▲△▴▵↑⇑∨∧<>')

# Block elements - used by graph-easy as decorative borders (valid terminators)
# ▐ (right half block), ▌ (left half block), ▀ (upper half), ▄ (lower half)
BLOCK_ELEMENTS = set('▐▌▀▄█░▒▓')

# Ellipsis characters - used by graph-easy for truncation (valid terminators)
# ⋮ (vertical ellipsis), ⋯ (horizontal ellipsis), … (horizontal ellipsis)
ELLIPSIS_CHARS = set('⋮⋯…')

# Valid line terminators (arrows + block elements + ellipsis)
VALID_TERMINATORS = ARROWS | BLOCK_ELEMENTS | ELLIPSIS_CHARS

# All box-drawing characters
ALL_BOX_CHARS = HORIZONTAL | VERTICAL | CORNERS | T_JUNCTIONS | CROSSES

# Characters that connect upward
CONNECTS_UP = VERTICAL | CORNER_BL | CORNER_BR | T_LEFT | T_RIGHT | T_BOTTOM | CROSSES
# Characters that connect downward
CONNECTS_DOWN = VERTICAL | CORNER_TL | CORNER_TR | T_LEFT | T_RIGHT | T_TOP | CROSSES
# Characters that connect left
CONNECTS_LEFT = HORIZONTAL | CORNER_TR | CORNER_BR | T_TOP | T_BOTTOM | T_RIGHT | CROSSES
# Characters that connect right
CONNECTS_RIGHT = HORIZONTAL | CORNER_TL | CORNER_BL | T_TOP | T_BOTTOM | T_LEFT | CROSSES

# File tree patterns to skip (require space after dashes for actual tree patterns)
FILE_TREE_PATTERN = re.compile(r'[├└]── ')


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    file: str
    line: int
    column: int
    severity: Severity
    message: str
    suggestion: str | None = None

    def __str__(self) -> str:
        base = f"{self.file}:{self.line}:{self.column}: {self.severity.value}: {self.message}"
        if self.suggestion:
            base += f"\n  → Suggestion: {self.suggestion}"
        return base


def is_file_tree_block(lines: list[str]) -> bool:
    """Detect if a code block is a file tree structure."""
    tree_line_count = 0
    for line in lines:
        if FILE_TREE_PATTERN.search(line):
            tree_line_count += 1
    # If more than 20% of lines have tree patterns, it's a file tree
    return tree_line_count > len(lines) * 0.2


def is_enclosed_box_diagram(lines: list[str]) -> bool:
    """Detect if a code block contains an enclosed box diagram (with corner characters)."""
    has_tl = any(any(c in CORNER_TL for c in line) for line in lines)
    has_tr = any(any(c in CORNER_TR for c in line) for line in lines)
    has_bl = any(any(c in CORNER_BL for c in line) for line in lines)
    has_br = any(any(c in CORNER_BR for c in line) for line in lines)

    # For a proper enclosed box, we need at least top-left + bottom-right or top-right + bottom-left
    return (has_tl and has_br) or (has_tr and has_bl) or (has_tl and has_tr and has_bl and has_br)


def get_char_at(lines: list[str], row: int, col: int) -> str | None:
    """Get character at position, handling bounds."""
    if row < 0 or row >= len(lines):
        return None
    line = lines[row]
    if col < 0 or col >= len(line):
        return None
    return line[col]


def find_box_chars_in_line(line: str) -> list[tuple[int, str]]:
    """Find all box-drawing characters in a line with their column positions."""
    results = []
    for col, char in enumerate(line):
        if char in ALL_BOX_CHARS:
            results.append((col, char))
    return results


def check_vertical_alignment(
    lines: list[str], row: int, col: int, char: str, file: str
) -> list[Issue]:
    """Check vertical alignment for a character that connects up or down."""
    issues = []

    # Check if character should connect upward
    if char in CONNECTS_UP:
        above = get_char_at(lines, row - 1, col)
        # Valid connections: box chars that connect down, arrows, terminators,
        # or horizontal lines (graph-easy arrow stem pattern: │ below ─)
        if above is not None and above not in CONNECTS_DOWN and above not in ' \t' and above not in VALID_TERMINATORS and above not in HORIZONTAL:
            issues.append(Issue(
                file=file,
                line=row + 1,  # 1-indexed
                column=col + 1,
                severity=Severity.ERROR,
                message=f"vertical connector '{char}' at column {col + 1} has no matching character above (found '{above}')",
                suggestion=f"Add '│', '├', '┤', '┬', or '┼' at line {row}, column {col + 1}, or check if '{char}' should be a different character"
            ))

    # Check if character should connect downward
    if char in CONNECTS_DOWN:
        below = get_char_at(lines, row + 1, col)
        # Valid connections: box chars that connect up, arrows, terminators,
        # or horizontal lines (graph-easy arrow stem pattern: │ above ─)
        if below is not None and below not in CONNECTS_UP and below not in ' \t' and below not in VALID_TERMINATORS and below not in HORIZONTAL:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"vertical connector '{char}' at column {col + 1} has no matching character below (found '{below}')",
                suggestion=f"Add '│', '├', '┤', '┴', or '┼' at line {row + 2}, column {col + 1}, or check if '{char}' should be a different character"
            ))

    return issues


def check_horizontal_alignment(
    lines: list[str], row: int, col: int, char: str, file: str
) -> list[Issue]:
    """Check horizontal alignment for a character that connects left or right."""
    issues = []
    line = lines[row]

    # Check if character should connect left
    if char in CONNECTS_LEFT:
        left = get_char_at(lines, row, col - 1)
        if col > 0 and left is not None and left not in CONNECTS_RIGHT and left not in ' \t' and left not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"horizontal connector '{char}' has no matching character to the left (found '{left}')",
                suggestion=f"Add '─', '┌', '└', '┬', '┴', or '┼' at column {col}"
            ))

    # Check if character should connect right
    if char in CONNECTS_RIGHT:
        right = get_char_at(lines, row, col + 1)
        if col < len(line) - 1 and right is not None and right not in CONNECTS_LEFT and right not in ' \t' and right not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"horizontal connector '{char}' has no matching character to the right (found '{right}')",
                suggestion=f"Add '─', '┐', '┘', '┬', '┴', or '┼' at column {col + 2}"
            ))

    return issues


def check_corner_connections(
    lines: list[str], row: int, col: int, char: str, file: str
) -> list[Issue]:
    """Validate corner characters have proper connections."""
    issues = []

    # Top-left corner: should connect right and down
    if char in CORNER_TL:
        right = get_char_at(lines, row, col + 1)
        below = get_char_at(lines, row + 1, col)

        if right is not None and right not in CONNECTS_LEFT and right not in ' \t\n' and right not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"top-left corner '{char}' not connected to the right",
                suggestion="Add horizontal line '─' or '═' after the corner"
            ))

        if below is not None and below not in CONNECTS_UP and below not in ' \t\n' and below not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"top-left corner '{char}' not connected below",
                suggestion=f"Add vertical line '│' or '║' at line {row + 2}, column {col + 1}"
            ))

    # Top-right corner: should connect left and down
    if char in CORNER_TR:
        left = get_char_at(lines, row, col - 1)
        below = get_char_at(lines, row + 1, col)

        if left is not None and left not in CONNECTS_RIGHT and left not in ' \t\n' and left not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"top-right corner '{char}' not connected to the left",
                suggestion="Add horizontal line '─' or '═' before the corner"
            ))

        if below is not None and below not in CONNECTS_UP and below not in ' \t\n' and below not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"top-right corner '{char}' not connected below",
                suggestion=f"Add vertical line '│' or '║' at line {row + 2}, column {col + 1}"
            ))

    # Bottom-left corner: should connect right and up
    if char in CORNER_BL:
        right = get_char_at(lines, row, col + 1)
        above = get_char_at(lines, row - 1, col)

        if right is not None and right not in CONNECTS_LEFT and right not in ' \t\n' and right not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"bottom-left corner '{char}' not connected to the right",
                suggestion="Add horizontal line '─' or '═' after the corner"
            ))

        if above is not None and above not in CONNECTS_DOWN and above not in ' \t\n' and above not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"bottom-left corner '{char}' not connected above",
                suggestion=f"Add vertical line '│' or '║' at line {row}, column {col + 1}"
            ))

    # Bottom-right corner: should connect left and up
    if char in CORNER_BR:
        left = get_char_at(lines, row, col - 1)
        above = get_char_at(lines, row - 1, col)

        if left is not None and left not in CONNECTS_RIGHT and left not in ' \t\n' and left not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"bottom-right corner '{char}' not connected to the left",
                suggestion="Add horizontal line '─' or '═' before the corner"
            ))

        if above is not None and above not in CONNECTS_DOWN and above not in ' \t\n' and above not in VALID_TERMINATORS:
            issues.append(Issue(
                file=file,
                line=row + 1,
                column=col + 1,
                severity=Severity.ERROR,
                message=f"bottom-right corner '{char}' not connected above",
                suggestion=f"Add vertical line '│' or '║' at line {row}, column {col + 1}"
            ))

    return issues


def extract_code_blocks(content: str) -> list[tuple[int, list[str]]]:
    """Extract code blocks from markdown, returning (start_line, lines) tuples."""
    blocks = []
    lines = content.split('\n')
    in_block = False
    block_start = 0
    block_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('```'):
            if in_block:
                # End of block
                blocks.append((block_start, block_lines))
                block_lines = []
                in_block = False
            else:
                # Start of block
                in_block = True
                block_start = i + 1  # Next line is start of content
        elif in_block:
            block_lines.append(line)

    return blocks


def validate_block(block_lines: list[str], block_start: int, file_path: str, verbose: bool) -> list[Issue]:
    """Validate a single code block for ASCII diagram alignment issues."""
    issues = []

    # Check if this block contains any box-drawing characters
    has_box_chars = any(
        any(c in ALL_BOX_CHARS for c in line)
        for line in block_lines
    )

    if not has_box_chars:
        return issues

    # Skip file tree structures
    if is_file_tree_block(block_lines):
        if verbose:
            print(f"    Skipping file tree structure at line {block_start + 1}")
        return issues

    # Only validate enclosed box diagrams
    if not is_enclosed_box_diagram(block_lines):
        if verbose:
            print(f"    Skipping non-enclosed diagram at line {block_start + 1}")
        return issues

    if verbose:
        print(f"    Checking enclosed box diagram at line {block_start + 1}")

    # Validate each line in the block
    for rel_row, line in enumerate(block_lines):
        box_chars = find_box_chars_in_line(line)

        for col, char in box_chars:
            # Check vertical alignment
            vert_issues = check_vertical_alignment(
                block_lines, rel_row, col, char, file_path
            )
            # Adjust line numbers to absolute file positions
            for issue in vert_issues:
                issues.append(Issue(
                    file=issue.file,
                    line=block_start + issue.line,
                    column=issue.column,
                    severity=issue.severity,
                    message=issue.message,
                    suggestion=issue.suggestion
                ))

            # Check horizontal alignment
            horiz_issues = check_horizontal_alignment(
                block_lines, rel_row, col, char, file_path
            )
            for issue in horiz_issues:
                issues.append(Issue(
                    file=issue.file,
                    line=block_start + issue.line,
                    column=issue.column,
                    severity=issue.severity,
                    message=issue.message,
                    suggestion=issue.suggestion
                ))

            # Check corner connections
            if char in CORNERS:
                corner_issues = check_corner_connections(
                    block_lines, rel_row, col, char, file_path
                )
                for issue in corner_issues:
                    issues.append(Issue(
                        file=issue.file,
                        line=block_start + issue.line,
                        column=issue.column,
                        severity=issue.severity,
                        message=issue.message,
                        suggestion=issue.suggestion
                    ))

    return issues


def validate_file(file_path: Path, verbose: bool = False) -> list[Issue]:
    """Validate a single file for ASCII diagram alignment issues."""
    issues = []

    try:
        content = file_path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError) as e:
        issues.append(Issue(
            file=str(file_path),
            line=0,
            column=0,
            severity=Severity.ERROR,
            message=f"Could not read file: {e}"
        ))
        return issues

    # Extract code blocks from markdown
    code_blocks = extract_code_blocks(content)

    if verbose:
        print(f"  Found {len(code_blocks)} code block(s) in {file_path}")

    for block_start, block_lines in code_blocks:
        block_issues = validate_block(block_lines, block_start, str(file_path), verbose)
        issues.extend(block_issues)

    return issues


def validate_path(path: Path, verbose: bool = False) -> list[Issue]:
    """Validate a file or directory."""
    issues = []

    if path.is_file():
        if verbose:
            print(f"Validating: {path}")
        issues.extend(validate_file(path, verbose))
    elif path.is_dir():
        # Find all markdown files
        for md_file in sorted(path.rglob('*.md')):
            if verbose:
                print(f"Validating: {md_file}")
            issues.extend(validate_file(md_file, verbose))
    else:
        issues.append(Issue(
            file=str(path),
            line=0,
            column=0,
            severity=Severity.ERROR,
            message=f"Path does not exist: {path}"
        ))

    return issues


def main():
    parser = argparse.ArgumentParser(
        description='Validate ASCII box-drawing diagram alignment in markdown files'
    )
    parser.add_argument(
        'paths',
        nargs='+',
        type=Path,
        help='Files or directories to validate'
    )
    parser.add_argument(
        '--warn-only',
        action='store_true',
        help='Exit 0 even if warnings found (still exit 1 on errors)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Print verbose progress information'
    )

    args = parser.parse_args()

    all_issues: list[Issue] = []

    for path in args.paths:
        all_issues.extend(validate_path(path, args.verbose))

    # Deduplicate issues (same file:line:column:message)
    seen = set()
    unique_issues = []
    for issue in all_issues:
        key = (issue.file, issue.line, issue.column, issue.message)
        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    # Sort by file, then line, then column
    unique_issues.sort(key=lambda i: (i.file, i.line, i.column))

    # Print issues
    for issue in unique_issues:
        print(issue)

    # Summary
    error_count = sum(1 for i in unique_issues if i.severity == Severity.ERROR)
    warning_count = sum(1 for i in unique_issues if i.severity == Severity.WARNING)
    info_count = sum(1 for i in unique_issues if i.severity == Severity.INFO)

    if unique_issues:
        print(f"\n{'─' * 60}")
        print(f"Summary: {error_count} error(s), {warning_count} warning(s), {info_count} info")

    # Exit code
    if error_count > 0:
        sys.exit(1)
    elif warning_count > 0 and not args.warn_only:
        sys.exit(2)
    else:
        if not unique_issues:
            print("✓ No alignment issues found")
        sys.exit(0)


if __name__ == '__main__':
    main()
