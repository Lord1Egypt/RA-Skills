#!/usr/bin/env python3
"""Split Tool - Split files."""

import argparse
import os
import sys


def split_file(filepath: str, lines: int = None, bytes_val: str = None, prefix: str = 'x'):
    """Split file."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    
    file_size = os.path.getsize(filepath)
    
    # Calculate chunk size
    if bytes_val:
        if bytes_val.endswith('K'):
            chunk_size = int(bytes_val[:-1]) * 1024
        elif bytes_val.endswith('M'):
            chunk_size = int(bytes_val[:-1]) * 1024 * 1024
        elif bytes_val.endswith('G'):
            chunk_size = int(bytes_val[:-1]) * 1024 * 1024 * 1024
        else:
            chunk_size = int(bytes_val)
    elif lines:
        # Estimate based on average line length
        with open(filepath, 'r') as f:
            sample = f.read(8192)
        avg_line = len(sample) / max(sample.count('\n'), 1)
        chunk_size = int(lines * avg_line)
    else:
        chunk_size = 1000
    
    # Split
    with open(filepath, 'rb') as f:
        part_num = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            part_path = f"{prefix}{part_num:03d}"
            with open(part_path, 'wb') as out:
                out.write(chunk)
            
            print(f"Created: {part_path}")
            part_num += 1
    
    print(f"Split into {part_num} files")


def main():
    parser = argparse.ArgumentParser(description='Split files')
    parser.add_argument('file', help='File to split')
    parser.add_argument('-l', '--lines', type=int, help='Lines per chunk')
    parser.add_argument('-b', '--bytes', help='Bytes per chunk (K, M, G)')
    parser.add_argument('-p', '--prefix', default='x', help='Output prefix')
    
    args = parser.parse_args()
    
    split_file(args.file, args.lines, args.bytes, args.prefix)


if __name__ == '__main__':
    main()
