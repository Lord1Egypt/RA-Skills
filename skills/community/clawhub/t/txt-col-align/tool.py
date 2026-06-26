#!/usr/bin/env python3
"""
Align columns in delimiter-separated text files or stdin input.
"""
import argparse
import sys
import csv
from typing import List, Optional, TextIO

def detect_dialect(sample: str) -> csv.Dialect:
    """Detect delimiter and basic CSV dialect from sample text."""
    sniffer = csv.Sniffer()
    try:
        return sniffer.sniff(sample, delimiters=',\t;| ')
    except csv.Error:
        # Default to space if detection fails
        dialect = csv.Dialect()
        dialect.delimiter = ' '
        dialect.quotechar = '"'
        dialect.quoting = csv.QUOTE_MINIMAL
        return dialect

def read_rows(file_handle: TextIO, delimiter: Optional[str] = None) -> List[List[str]]:
    """Read rows from file and return as list of row lists."""
    sample = ''.join([file_handle.readline() for _ in range(5)])
    file_handle.seek(0)

    if delimiter:
        reader = csv.reader(file_handle, delimiter=delimiter)
    else:
        dialect = detect_dialect(sample)
        reader = csv.reader(file_handle, dialect=dialect)

    rows = []
    for line in reader:
        # Handle empty lines gracefully
        if line:
            rows.append(line)
        else:
            rows.append([''])

    return rows

def align_columns(rows: List[List[str]], padding: int = 1) -> str:
    """Align columns by computing max width and padding each cell."""
    if not rows:
        return ""

    # Handle uneven rows by filling with empty strings
    max_cols = max(len(row) for row in rows)
    normalized_rows = [row + [''] * (max_cols - len(row)) for row in rows]

    # Compute max width for each column
    col_widths = [
        max(len(str(normalized_rows[r][c])) for r in range(len(normalized_rows)))
        for c in range(max_cols)
    ]

    # Format each row with padding
    result_lines = []
    for row in normalized_rows:
        aligned = ''.join(
            f"{row[i]:{col_widths[i] + padding}}" for i in range(len(row))
        ).rstrip()
        result_lines.append(aligned)

    return '\n'.join(result_lines)

def main():
    parser = argparse.ArgumentParser(
        description="Align columns in text files or stdin input.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  colalign data.csv
  colalign --delimiter ';' logs.txt
  echo -e "a,b\\nc,de" | colalign
        """.strip()
    )
    parser.add_argument(
        'input_file',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='Input file (default: stdin)'
    )
    parser.add_argument(
        '-d', '--delimiter',
        type=str,
        help='Field delimiter (auto-detected by default: comma, tab, semicolon, etc.)'
    )
    parser.add_argument(
        '-p', '--padding',
        type=int,
        default=2,
        help='Number of spaces between columns (default: 2)'
    )

    args = parser.parse_args()

    try:
        rows = read_rows(args.input_file, delimiter=args.delimiter)
        aligned = align_columns(rows, padding=args.padding)
        print(aligned)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if args.input_file is not sys.stdin:
            args.input_file.close()

if __name__ == '__main__':
    main()
