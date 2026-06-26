#!/usr/bin/env python3
import argparse
import os
import sys

def chunk_text_file(input_file, lines_per_chunk, output_prefix):
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)

    if lines_per_chunk < 1:
        print("Error: Lines per chunk must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            chunk_num = 1
            lines = []
            for line in f:
                lines.append(line)
                if len(lines) >= lines_per_chunk:
                    write_chunk(lines, output_prefix, chunk_num)
                    chunk_num += 1
                    lines = []
            # Write remaining lines
            if lines:
                write_chunk(lines, output_prefix, chunk_num)
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)

def write_chunk(lines, prefix, number):
    output_filename = f"{prefix}_{number:03d}.txt"
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        out_file.writelines(lines)
    print(f"Wrote {len(lines)} lines to {output_filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Split a large text file into smaller chunks by line count."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input text file"
    )
    parser.add_argument(
        "-n", "--lines",
        type=int,
        default=1000,
        help="Number of lines per chunk (default: 1000)"
    )
    parser.add_argument(
        "-o", "--output",
        default="chunk",
        help="Output prefix for chunk files (default: 'chunk')"
    )

    args = parser.parse_args()

    chunk_text_file(args.input_file, args.lines, args.output)

if __name__ == "__main__":
    main()
