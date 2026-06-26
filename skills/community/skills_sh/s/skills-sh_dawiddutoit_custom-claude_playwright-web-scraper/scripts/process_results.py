#!/usr/bin/env python3
"""Process scraped data into structured formats (CSV, JSON, or Markdown)."""

import argparse
import json
import csv
import sys
from pathlib import Path
from typing import Any, Dict, List
from datetime import datetime


def load_results(input_file: Path) -> List[Dict[str, Any]]:
    """Load results from JSON file."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Handle both list of objects and {"results": [...]} format
    if isinstance(data, dict) and 'results' in data:
        return data['results']
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Input must be a JSON array or object with 'results' key")


def to_csv(results: List[Dict[str, Any]], output_file: Path) -> None:
    """Convert results to CSV format."""
    if not results:
        print("Warning: No results to convert", file=sys.stderr)
        return

    # Get all unique keys from all results
    fieldnames = set()
    for item in results:
        fieldnames.update(item.keys())
    fieldnames = sorted(fieldnames)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"✅ Wrote {len(results)} records to {output_file}")


def to_json(results: List[Dict[str, Any]], output_file: Path, pretty: bool = True) -> None:
    """Convert results to JSON format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        if pretty:
            json.dump(results, f, indent=2, ensure_ascii=False)
        else:
            json.dump(results, f, ensure_ascii=False)

    print(f"✅ Wrote {len(results)} records to {output_file}")


def to_markdown(results: List[Dict[str, Any]], output_file: Path) -> None:
    """Convert results to Markdown table format."""
    if not results:
        print("Warning: No results to convert", file=sys.stderr)
        return

    # Get all unique keys
    fieldnames = set()
    for item in results:
        fieldnames.update(item.keys())
    fieldnames = sorted(fieldnames)

    with open(output_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write('| ' + ' | '.join(fieldnames) + ' |\n')
        f.write('| ' + ' | '.join(['---'] * len(fieldnames)) + ' |\n')

        # Write rows
        for item in results:
            row = [str(item.get(key, '')).replace('|', '\\|') for key in fieldnames]
            f.write('| ' + ' | '.join(row) + ' |\n')

    print(f"✅ Wrote {len(results)} records to {output_file}")


def generate_stats(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate statistics about the scraped data."""
    if not results:
        return {"total": 0}

    stats = {
        "total": len(results),
        "fields": sorted(set().union(*[set(r.keys()) for r in results])),
        "field_count": len(set().union(*[set(r.keys()) for r in results])),
        "sample": results[0] if results else None
    }

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Process scraped data into structured formats"
    )
    parser.add_argument(
        'input_file',
        type=Path,
        help='Input JSON file containing scraped results'
    )
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file path (extension determines format: .csv, .json, .md)'
    )
    parser.add_argument(
        '--format',
        choices=['csv', 'json', 'markdown'],
        help='Output format (overrides file extension)'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Print statistics about the data'
    )
    parser.add_argument(
        '--compact',
        action='store_true',
        help='Use compact JSON output (no pretty printing)'
    )

    args = parser.parse_args()

    # Load results
    try:
        results = load_results(args.input_file)
    except Exception as e:
        print(f"❌ Error loading input file: {e}", file=sys.stderr)
        sys.exit(1)

    # Print stats if requested
    if args.stats:
        stats = generate_stats(results)
        print("\n📊 Statistics:")
        print(f"  Total records: {stats['total']}")
        print(f"  Fields ({stats['field_count']}): {', '.join(stats['fields'])}")
        if stats.get('sample'):
            print(f"  Sample record: {json.dumps(stats['sample'], indent=2)}")
        print()

    # Determine output format
    if args.output:
        if args.format:
            output_format = args.format
        else:
            # Infer from extension
            ext = args.output.suffix.lower()
            if ext == '.csv':
                output_format = 'csv'
            elif ext == '.json':
                output_format = 'json'
            elif ext == '.md':
                output_format = 'markdown'
            else:
                print(f"❌ Unknown file extension: {ext}", file=sys.stderr)
                print("Use --format to specify csv, json, or markdown", file=sys.stderr)
                sys.exit(1)

        # Convert and write
        try:
            if output_format == 'csv':
                to_csv(results, args.output)
            elif output_format == 'json':
                to_json(results, args.output, pretty=not args.compact)
            elif output_format == 'markdown':
                to_markdown(results, args.output)
        except Exception as e:
            print(f"❌ Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Just print stats
        if not args.stats:
            print("No output file specified. Use -o to save results or --stats to view statistics")
            sys.exit(1)


if __name__ == '__main__':
    main()
