#!/usr/bin/env python3
"""
quickcsv - Convert JSON, YAML, or TSV to CSV
"""
import argparse
import csv
import json
import sys
import yaml

def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def read_tsv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

def write_csv(data, output_path):
    if not data:
        return

    # Handle list of dicts or single-depth JSON arrays
    if isinstance(data, dict):
        data = [data]

    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())
    fieldnames = sorted(fieldnames)

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def main():
    parser = argparse.ArgumentParser(description="Convert JSON, YAML, or TSV to CSV")
    parser.add_argument('input', help='Input file (json, yaml, yml, tsv)')
    parser.add_argument('-o', '--output', help='Output CSV file (default: stdout)', default=None)
    parser.add_argument('--no-output-header', action='store_true', help='Skip CSV header row')

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output

    # Detect file type
    if input_path.endswith('.json'):
        data = read_json(input_path)
    elif input_path.endswith('.yaml') or input_path.endswith('.yml'):
        data = read_yaml(input_path)
    elif input_path.endswith('.tsv'):
        data = read_tsv(input_path)
    else:
        print("Error: Input file must be .json, .yaml, .yml, or .tsv", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        if isinstance(data, dict):
            data = [data]
        else:
            print("Error: Data format not supported (must be object or array)", file=sys.stderr)
            sys.exit(1)

    if output_path:
        write_csv(data, output_path)
    else:
        # Write to stdout
        if not data:
            sys.exit(0)
        fieldnames = sorted(set(k for d in data for k in d.keys()))
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        if not args.no_output_header:
            writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == '__main__':
    main()
