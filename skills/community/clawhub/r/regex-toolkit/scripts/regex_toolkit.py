#!/usr/bin/env python3
"""Regex toolkit — test, match, extract, replace, and explain regular expressions.

Features:
- Test a regex against input text (match/no-match)
- Find all matches with groups and positions
- Extract captured groups
- Search-and-replace with backreferences
- Explain regex patterns in plain English
- Common regex patterns library (email, URL, IP, phone, etc.)
- Validate regex syntax
- Multi-line and file input support

No external dependencies (Python stdlib only).
"""

import argparse
import json
import re
import sys


# --- Common patterns library ---
COMMON_PATTERNS = {
    "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "url": r"https?://[^\s<>\"']+",
    "ipv4": r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b",
    "ipv6": r"(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}",
    "phone-us": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "phone-intl": r"\+?\d{1,4}[-.\s]?\(?\d{1,5}\)?[-.\s]?\d{1,5}[-.\s]?\d{1,5}",
    "date-iso": r"\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])",
    "date-us": r"(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/\d{4}",
    "time-24h": r"(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?",
    "hex-color": r"#(?:[0-9a-fA-F]{3}){1,2}\b",
    "mac-address": r"(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}",
    "uuid": r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "zip-us": r"\b\d{5}(?:-\d{4})?\b",
    "credit-card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "slug": r"[a-z0-9]+(?:-[a-z0-9]+)*",
    "semver": r"\bv?(\d+)\.(\d+)\.(\d+)(?:-([\w.]+))?(?:\+([\w.]+))?\b",
    "domain": r"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b",
    "hashtag": r"#[a-zA-Z_]\w*",
    "mention": r"@[a-zA-Z0-9_]+",
    "markdown-link": r"\[([^\]]+)\]\(([^)]+)\)",
    "html-tag": r"<\/?([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>",
    "json-key": r'"([^"]+)"\s*:',
    "filepath-unix": r"(?:/[^\s/]+)+",
    "filepath-win": r"[A-Z]:\\(?:[^\\\s]+\\)*[^\\\s]+",
}

# --- Regex explainer ---

ESCAPE_MAP = {
    "d": "any digit (0-9)",
    "D": "any non-digit",
    "w": "any word character (letter, digit, underscore)",
    "W": "any non-word character",
    "s": "any whitespace",
    "S": "any non-whitespace",
    "b": "word boundary",
    "B": "non-word boundary",
    "n": "newline",
    "t": "tab",
    ".": "literal dot",
    "\\": "literal backslash",
}

SPECIAL_CHARS = {
    ".": "any character",
    "^": "start of string/line",
    "$": "end of string/line",
    "*": "zero or more of the preceding",
    "+": "one or more of the preceding",
    "?": "zero or one of the preceding (optional)",
}


def explain_regex(pattern):
    """Explain a regex pattern in plain English."""
    explanations = []
    i = 0
    while i < len(pattern):
        matched = False

        # Check for quantifiers with braces
        if pattern[i] == '{':
            end = pattern.find('}', i)
            if end != -1:
                quant = pattern[i:end+1]
                parts = quant[1:-1].split(',')
                if len(parts) == 1:
                    explanations.append(f"  exactly {parts[0]} times")
                elif parts[1] == '':
                    explanations.append(f"  {parts[0]} or more times")
                else:
                    explanations.append(f"  between {parts[0]} and {parts[1]} times")
                i = end + 1
                continue

        # Check for character classes
        if pattern[i] == '[':
            end = pattern.find(']', i)
            if end != -1:
                cls = pattern[i:end+1]
                neg = "not " if len(cls) > 1 and cls[1] == '^' else ""
                inner = cls[2:-1] if neg else cls[1:-1]
                explanations.append(f"  {neg}one of: {inner}")
                i = end + 1
                continue

        # Check for groups
        if pattern[i] == '(':
            if pattern[i:i+3] == '(?:':
                explanations.append("  non-capturing group start")
                i += 3
                continue
            elif pattern[i:i+4] == '(?P<':
                end = pattern.find('>', i)
                if end != -1:
                    name = pattern[i+4:end]
                    explanations.append(f"  named group '{name}' start")
                    i = end + 1
                    continue
            elif pattern[i:i+3] == '(?=':
                explanations.append("  lookahead start")
                i += 3
                continue
            elif pattern[i:i+3] == '(?!':
                explanations.append("  negative lookahead start")
                i += 3
                continue
            elif pattern[i:i+4] == '(?<=':
                explanations.append("  lookbehind start")
                i += 4
                continue
            elif pattern[i:i+4] == '(?<!':
                explanations.append("  negative lookbehind start")
                i += 4
                continue
            else:
                explanations.append("  capturing group start")
                i += 1
                continue

        if pattern[i] == ')':
            explanations.append("  group end")
            i += 1
            continue

        if pattern[i] == '|':
            explanations.append("  OR")
            i += 1
            continue

        # Escaped characters
        if pattern[i] == '\\' and i + 1 < len(pattern):
            next_char = pattern[i+1]
            two_char = pattern[i:i+2]
            if next_char in ESCAPE_MAP:
                explanations.append(f"  {two_char} → {ESCAPE_MAP[next_char]}")
            else:
                explanations.append(f"  {two_char} → literal '{next_char}'")
            i += 2
            continue

        # Special single chars
        if pattern[i] in SPECIAL_CHARS:
            explanations.append(f"  {pattern[i]} → {SPECIAL_CHARS[pattern[i]]}")
            i += 1
            continue

        explanations.append(f"  '{pattern[i]}' → literal character")
        i += 1

    return explanations


def get_flags(args):
    """Build regex flags from args."""
    flags = 0
    if hasattr(args, 'ignorecase') and args.ignorecase:
        flags |= re.IGNORECASE
    if hasattr(args, 'multiline') and args.multiline:
        flags |= re.MULTILINE
    if hasattr(args, 'dotall') and args.dotall:
        flags |= re.DOTALL
    return flags


def get_input(args):
    """Get input text from args or stdin."""
    if hasattr(args, 'text') and args.text:
        return args.text
    if hasattr(args, 'file') and args.file:
        with open(args.file, "r") as f:
            return f.read()
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return None


def resolve_pattern(pattern_str):
    """Resolve a pattern — either a named common pattern or a raw regex."""
    if pattern_str in COMMON_PATTERNS:
        return COMMON_PATTERNS[pattern_str]
    return pattern_str


def cmd_test(args):
    """Test if a pattern matches input."""
    pattern = resolve_pattern(args.pattern)
    text = get_input(args)
    if text is None:
        print("Error: Provide text via --text, --file, or stdin.", file=sys.stderr)
        sys.exit(1)

    try:
        flags = get_flags(args)
        match = re.search(pattern, text, flags)
        if match:
            print(f"MATCH found at position {match.start()}-{match.end()}: '{match.group()}'")
            if match.groups():
                for i, g in enumerate(match.groups(), 1):
                    print(f"  Group {i}: '{g}'")
            return
        print("NO MATCH")
    except re.error as e:
        print(f"Regex error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_findall(args):
    """Find all matches."""
    pattern = resolve_pattern(args.pattern)
    text = get_input(args)
    if text is None:
        print("Error: Provide text via --text, --file, or stdin.", file=sys.stderr)
        sys.exit(1)

    try:
        flags = get_flags(args)
        matches = list(re.finditer(pattern, text, flags))
        if not matches:
            print("No matches found.")
            return

        results = []
        for m in matches:
            entry = {
                "match": m.group(),
                "start": m.start(),
                "end": m.end(),
            }
            if m.groups():
                entry["groups"] = list(m.groups())
            results.append(entry)

        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(f"Found {len(matches)} match(es):\n")
            for i, r in enumerate(results, 1):
                print(f"  {i}. '{r['match']}' (pos {r['start']}-{r['end']})")
                if "groups" in r:
                    for j, g in enumerate(r["groups"], 1):
                        print(f"     Group {j}: '{g}'")
    except re.error as e:
        print(f"Regex error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_replace(args):
    """Search and replace."""
    pattern = resolve_pattern(args.pattern)
    text = get_input(args)
    if text is None:
        print("Error: Provide text via --text, --file, or stdin.", file=sys.stderr)
        sys.exit(1)

    try:
        flags = get_flags(args)
        count = args.count if args.count else 0
        result = re.sub(pattern, args.replacement, text, count=count, flags=flags)
        print(result)
    except re.error as e:
        print(f"Regex error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_explain(args):
    """Explain a regex pattern."""
    pattern = args.pattern
    resolved = resolve_pattern(pattern)
    if pattern != resolved:
        print(f"Pattern '{pattern}' resolves to: {resolved}\n")
        pattern = resolved

    print(f"Pattern: {pattern}\n")
    print("Breakdown:")
    for line in explain_regex(pattern):
        print(line)


def cmd_validate(args):
    """Validate regex syntax."""
    try:
        re.compile(args.pattern)
        print(f"Valid regex: {args.pattern}")
    except re.error as e:
        print(f"Invalid regex: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_patterns(args):
    """List common patterns."""
    if args.name:
        name = args.name
        if name not in COMMON_PATTERNS:
            print(f"Unknown pattern '{name}'. Use --list to see available patterns.", file=sys.stderr)
            sys.exit(1)
        print(f"{name}: {COMMON_PATTERNS[name]}")
        return

    print("Available common patterns:\n")
    max_name = max(len(n) for n in COMMON_PATTERNS)
    for name, pattern in COMMON_PATTERNS.items():
        print(f"  {name:<{max_name}}  {pattern}")


def main():
    parser = argparse.ArgumentParser(
        description="Regex toolkit — test, find, replace, and explain regular expressions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s test '\\d+' --text 'abc 123 def'
  %(prog)s findall email --file emails.txt
  %(prog)s replace '\\bfoo\\b' --replacement bar --text 'foo bar foo'
  %(prog)s explain '(?P<year>\\d{4})-(?P<month>\\d{2})'
  %(prog)s patterns --list
  %(prog)s validate '[a-z'
"""
    )
    sub = parser.add_subparsers(dest="command", help="Command to run")

    # Common arguments
    def add_input_args(p):
        p.add_argument("--text", "-t", help="Input text string")
        p.add_argument("--file", "-f", help="Input file")
        p.add_argument("--ignorecase", "-i", action="store_true", help="Case-insensitive matching")
        p.add_argument("--multiline", "-m", action="store_true", help="Multi-line mode (^ and $ match line boundaries)")
        p.add_argument("--dotall", "-s", action="store_true", help="Dot matches newline")

    # test
    p_test = sub.add_parser("test", help="Test if pattern matches input")
    p_test.add_argument("pattern", help="Regex pattern or common pattern name")
    add_input_args(p_test)

    # findall
    p_find = sub.add_parser("findall", help="Find all matches with positions and groups")
    p_find.add_argument("pattern", help="Regex pattern or common pattern name")
    p_find.add_argument("--json", action="store_true", help="Output as JSON")
    add_input_args(p_find)

    # replace
    p_repl = sub.add_parser("replace", help="Search and replace")
    p_repl.add_argument("pattern", help="Regex pattern or common pattern name")
    p_repl.add_argument("--replacement", "-r", required=True, help="Replacement string (supports \\1 backreferences)")
    p_repl.add_argument("--count", "-c", type=int, default=0, help="Max replacements (0=all)")
    add_input_args(p_repl)

    # explain
    p_explain = sub.add_parser("explain", help="Explain a regex in plain English")
    p_explain.add_argument("pattern", help="Regex pattern or common pattern name")

    # validate
    p_val = sub.add_parser("validate", help="Check if regex syntax is valid")
    p_val.add_argument("pattern", help="Regex pattern to validate")

    # patterns
    p_patterns = sub.add_parser("patterns", help="List common regex patterns")
    p_patterns.add_argument("name", nargs="?", help="Show a specific pattern")
    p_patterns.add_argument("--list", action="store_true", help="List all patterns")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    cmd_map = {
        "test": cmd_test,
        "findall": cmd_findall,
        "replace": cmd_replace,
        "explain": cmd_explain,
        "validate": cmd_validate,
        "patterns": cmd_patterns,
    }

    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
