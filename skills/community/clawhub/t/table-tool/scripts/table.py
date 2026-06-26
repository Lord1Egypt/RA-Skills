#!/usr/bin/env python3
"""Table Tool - Generate ASCII tables."""

import argparse
import csv
import io
import json
import sys
from typing import List, Dict, Any


STYLES = {
    'simple': {
        'hline': True,
        'sep': '|',
    },
    'grid': {
        'hline': True,
        'sep': '|',
    },
    'double': {
        'hline': True,
        'sep': '║',
    },
    'rounded': {
        'hline': True,
        'sep': '│',
    },
    'markdown': {
        'hline': False,
        'sep': '|',
    }
}


def parse_data(data: str, delimiter: str = '|') -> List[List[str]]:
    """Parse input data into rows."""
    lines = data.strip().split('\n')
    
    # Try to detect delimiter
    if delimiter == 'auto':
        first_line = lines[0]
        for d in ['|', '\t', ',', ';']:
            if d in first_line:
                delimiter = d
                break
    
    rows = []
    for line in lines:
        if delimiter == 'auto':
            row = [line]
        else:
            row = line.split(delimiter)
        rows.append([cell.strip() for cell in row])
    
    return rows


def parse_csv(data: str) -> List[List[str]]:
    """Parse CSV data."""
    reader = csv.reader(io.StringIO(data))
    return list(reader)


def parse_json(data: str) -> List[Dict[str, Any]]:
    """Parse JSON data."""
    obj = json.loads(data)
    
    if isinstance(obj, list):
        return obj
    elif isinstance(obj, dict):
        return [obj]
    else:
        return []


def json_to_rows(data: List[Dict[str, Any]]) -> List[List[str]]:
    """Convert JSON array to rows."""
    if not data:
        return []
    
    # Get all keys
    keys = set()
    for item in data:
        keys.update(item.keys())
    keys = list(keys)
    
    # Header
    rows = [keys]
    
    # Data rows
    for item in data:
        row = [str(item.get(k, '')) for k in keys]
        rows.append(row)
    
    return rows


def calculate_widths(rows: List[List[str]]) -> List[int]:
    """Calculate column widths."""
    widths = []
    for row in rows:
        for i, cell in enumerate(row):
            if i >= len(widths):
                widths.append(len(cell))
            else:
                widths[i] = max(widths[i], len(cell))
    return widths


def format_cell(text: str, width: int, align: str = 'l') -> str:
    """Format a cell with alignment."""
    if align == 'l':
        return text.ljust(width)
    elif align == 'r':
        return text.rjust(width)
    elif align == 'c':
        return text.center(width)
    return text


def create_table(
    rows: List[List[str]],
    style: str = 'simple',
    alignments: List[str] = None
) -> str:
    """Create an ASCII table."""
    if not rows:
        return ""
    
    # Calculate widths
    widths = calculate_widths(rows)
    
    # Get style
    style_def = STYLES.get(style, STYLES['simple'])
    
    # Build table
    lines = []
    
    # Border characters based on style
    if style == 'simple' or style == 'grid':
        horiz, vert, corner = '-', '|', '+'
    elif style == 'double':
        horiz, vert, corner = '═', '║', '╬'
    elif style == 'rounded':
        horiz, vert, corner = '─', '│', '┼'
    else:  # markdown
        horiz, vert, corner = '-', '|', '|'
    
    # Top border
    if style != 'markdown':
        border = corner + horiz * (sum(widths) + len(widths) * 3 - 1) + corner
        lines.append(border)
    
    # Header and data
    for i, row in enumerate(rows):
        # Pad row
        padded_row = row + [''] * (len(widths) - len(row))
        
        # Format cells
        cells = []
        for j, cell in enumerate(padded_row):
            align = alignments[j] if alignments and j < len(alignments) else 'l'
            cells.append(format_cell(cell, widths[j], align))
        
        # Row line
        if style == 'markdown':
            line = vert + vert.join(cells) + vert
            lines.append(line)
            if i == 0:
                # Separator
                sep = vert + vert.join(['-' * w for w in widths]) + vert
                lines.append(sep)
        else:
            line = vert + ' ' + (' {} '.format(vert) if style in ['double', 'rounded'] else vert).join(cells) + ' ' + vert
            lines.append(line)
        
        # Mid border after header
        if i == 0 and style != 'markdown':
            border = corner + horiz * (sum(widths) + len(widths) * 3 - 1) + corner
            lines.append(border)
    
    # Bottom border
    if style != 'markdown':
        border = corner + horiz * (sum(widths) + len(widths) * 3 - 1) + corner
        lines.append(border)
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='ASCII table generator')
    
    parser.add_argument('--data', '-d', help='Pipe-separated data')
    parser.add_argument('--json', '-j', help='JSON array of objects')
    parser.add_argument('--csv', '-c', help='CSV data or file')
    parser.add_argument('--delimiter', default='|', help='Column delimiter')
    parser.add_argument('--style', default='simple', 
                       choices=['simple', 'grid', 'double', 'rounded', 'markdown'],
                       help='Table style')
    parser.add_argument('--align', '-a', help='Alignment (l, c, r per column)')
    
    args = parser.parse_args()
    
    # Parse input
    if args.json:
        data = parse_json(args.json)
        rows = json_to_rows(data)
    elif args.csv:
        if args.csv.startswith('{') or args.csv.startswith('['):
            # JSON in csv field
            data = parse_json(args.csv)
            rows = json_to_rows(data)
        elif '\n' in args.csv:
            # CSV data
            rows = parse_csv(args.csv)
        else:
            # File
            try:
                with open(args.csv, 'r') as f:
                    rows = parse_csv(f.read())
            except FileNotFoundError:
                print(f"Error: File not found: {args.csv}", file=sys.stderr)
                sys.exit(1)
    elif args.data:
        rows = parse_data(args.data, args.delimiter)
    else:
        # Read from stdin
        data = sys.stdin.read()
        if data.strip().startswith('[') or data.strip().startswith('{'):
            jdata = parse_json(data)
            rows = json_to_rows(jdata)
        else:
            rows = parse_data(data, args.delimiter)
    
    if not rows:
        print("Error: No data provided", file=sys.stderr)
        sys.exit(1)
    
    # Parse alignments
    alignments = None
    if args.align:
        alignments = list(args.align)
    
    # Generate table
    table = create_table(rows, args.style, alignments)
    print(table)


if __name__ == '__main__':
    main()
