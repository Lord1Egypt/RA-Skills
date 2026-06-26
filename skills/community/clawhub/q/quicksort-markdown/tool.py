#!/usr/bin/env python3
"""
Sorts markdown headings and their nested content alphabetically.
"""

import argparse
import sys
import re
from typing import List, Tuple, Iterator

def parse_markdown_lines(lines: List[str]) -> Iterator[Tuple[int, str, List[str]]]:
    """Yield (level, heading, content) for each top-level heading and its nested content."""
    current_heading = None
    current_level = 0
    current_content: List[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if match:
            level = len(match.group(1))
            heading = match.group(2).strip()
            if current_heading is not None and level <= current_level:
                yield (current_level, current_heading, current_content)
                current_heading = heading
                current_level = level
                current_content = []
            else:
                if current_heading is None:
                    current_heading = heading
                    current_level = level
                    current_content = []
                else:
                    current_content.append(line)
        else:
            if current_heading is not None:
                current_content.append(line)
            else:
                # Content before first heading — leave as-is
                yield (0, "", [line])
        i += 1

    if current_heading is not None:
        yield (current_level, current_heading, current_content)
    elif current_heading is None and current_content:
        yield (0, "", current_content)

def sort_sections(sections: List[Tuple[int, str, List[str]]]) -> List[str]:
    """Sort sections by heading name, recursively sorting subsections."""
    result: List[str] = []
    # Separate top-level from deeper-level sections
    top_level: List[Tuple[int, str, List[str]]] = [s for s in sections if s[0] == max(s[0], 1)]
    top_level.sort(key=lambda x: x[1].lower())

    for level, heading, content in top_level:
        result.append(f"{'#' * level} {heading}")
        # Parse content for nested sections
        sub_sections = list(parse_markdown_lines(content))
        if sub_sections and any(s[0] > level for s in sub_sections if s[0] > 0):
            sorted_content = sort_sections(sub_sections)
            result.extend(sorted_content)
        else:
            result.extend(content)

    return result

def main():
    parser = argparse.ArgumentParser(
        description="Sort markdown headings and their content alphabetically."
    )
    parser.add_argument(
        "input", 
        nargs="?", 
        type=argparse.FileType("r"), 
        default=sys.stdin, 
        help="Input .md file (stdin if not specified)"
    )
    parser.add_argument(
        "-o", 
        "--output", 
        type=argparse.FileType("w"), 
        default=sys.stdout, 
        help="Output file (stdout if not specified)"
    )

    args = parser.parse_args()

    try:
        lines = [line.rstrip("\n") for line in args.input.readlines()]
        sections = list(parse_markdown_lines(lines))
        sorted_lines = sort_sections(sections)
        for line in sorted_lines:
            print(line, file=args.output)
    except Exception as e:
        print(f"Error processing markdown: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
