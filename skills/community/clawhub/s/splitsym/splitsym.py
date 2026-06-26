#!/usr/bin/env python3
"""
splitsym - Extract split symbols (line or pair) from files
Usage: splitsym <file> [--lines M-N] [--config FILE]
"""

import json
import re
import sys
import os
from pathlib import Path

DEFAULT_CONFIG = Path.home() / ".config/splitsym/symbols.json"

def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_rules(filepath, config):
    """Return (rule_type, pattern_dict) for given file."""
    ext = Path(filepath).suffix.lower()
    name = Path(filepath).name

    # 先匹配 pair 规则
    for rule in config.get("symbols", {}).get("pair", []):
        if re.search(rule["file_pattern"], name, re.IGNORECASE) or \
           re.search(rule["file_pattern"], ext, re.IGNORECASE):
            return "pair", rule

    # 再匹配 line 规则
    for rule in config.get("symbols", {}).get("line", []):
        if re.search(rule["file_pattern"], name, re.IGNORECASE) or \
           re.search(rule["file_pattern"], ext, re.IGNORECASE):
            return "line", rule

    # fallback
    fb = config.get("fallback")
    if fb:
        return fb.get("type", "line"), fb
    raise ValueError(f"No split rule for {filepath}")

def process_pair(filepath, rule, line_range):
    start_re = re.compile(rule["start"])
    end_re = re.compile(rule["end"])
    include_content = rule.get("include_content", True)

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    if line_range:
        s, e = map(int, line_range.split('-'))
        lines = lines[s-1:e]
        base = s
    else:
        base = 1

    in_pair = False
    start_line = None
    start_indent = 0
    content_lines = []

    for i, line in enumerate(lines, start=base):
        if not in_pair:
            if start_re.search(line):
                in_pair = True
                start_line = i
                start_indent = len(line) - len(line.lstrip())
                content_lines = [line.rstrip('\n')]
        else:
            content_lines.append(line.rstrip('\n'))
            if end_re.search(line):
                # 输出
                if include_content:
                    snippet = ' '.join(content_lines)[:80]
                else:
                    snippet = f"{rule['name']} block"
                print(f"{start_line:6d} {' ' * start_indent}PAIR: {snippet}")
                in_pair = False
                content_lines = []

def process_line(filepath, rule, line_range):
    start_re = re.compile(rule["start"])
    group = rule.get("group", 1)

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    if line_range:
        s, e = map(int, line_range.split('-'))
        lines = lines[s-1:e]
        base = s
    else:
        base = 1

    for i, line in enumerate(lines, start=base):
        m = start_re.search(line)
        if m:
            content = m.group(group).strip()
            if content:
                indent = len(line) - len(line.lstrip())
                print(f"{i:6d} {' ' * indent}{content}")

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--lines", help="line range like 100-200")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(args.config):
        print(f"Config not found: {args.config}", file=sys.stderr)
        sys.exit(1)

    config = load_config(args.config)
    try:
        typ, rule = get_rules(args.file, config)
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if typ == "pair":
        process_pair(args.file, rule, args.lines)
    else:
        process_line(args.file, rule, args.lines)

if __name__ == "__main__":
    main()