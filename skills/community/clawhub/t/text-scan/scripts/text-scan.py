#!/usr/bin/env python3
"""text-scan.py — Search for relevant information in text files.

Usage:
    python3 text-scan.py <file> [options]

Options:
    --query <text>        Search query (keywords to find)
    --lines <n>           Number of lines after match (default: 5)
    --before <n>          Number of lines before match (default: 2)
    --max-results <n>     Maximum results to return (default: 5)
    --fuzzy               Use fuzzy matching for approximate keywords
    --context             Show surrounding context for each match
    --output <file>       Write results to file (instead of stdout)

If no --query is given, reads from stdin for the query.

Examples:
    python3 text-scan.py STATE.md --query "runway"
    python3 text-scan.py MEMORY.md --query "project goals" --lines 10 --before 2
    cat LOG.md | python3 text-scan.py --query "weather" --fuzzy
"""

import sys
import os
import argparse
import re
import json


def normalize(text):
    """Normalize text for fuzzy matching: lowercase, strip extra whitespace."""
    return re.sub(r'\s+', ' ', text.lower().strip())


def tokens(text):
    """Split text into tokens (words), also extract n-grams."""
    normalized = normalize(text)
    words = normalized.split()
    # Include bigrams
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
    return words + bigrams


def match_query(line, query_tokens):
    """Score how well a line matches the query. Returns (score, matched_terms)."""
    line_norm = normalize(line)
    line_toks = set(tokens(line_norm))
    if not query_tokens:
        return 0, []

    matched = []
    score = 0
    for q in query_tokens:
        # Exact match
        if q in line_toks:
            score += 2
            matched.append(q)
        elif q in line_norm:
            # Partial/substring match
            score += 1
            matched.append(q)

    # Bonus: words close together in line (phrase match)
    for i in range(len(query_tokens) - 1):
        pair = f"{query_tokens[i]} {query_tokens[i+1]}"
        if pair in line_norm:
            score += 3

    return score, matched


def scan_file(filepath, query, lines_after=5, lines_before=2, max_results=5, fuzzy=False):
    """Scan a file for lines matching the query.

    Returns list of dicts: {line_num, content, score, matched_terms, context}
    """
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    if not query.strip():
        return []

    query_tokens = tokens(query)
    if not query_tokens:
        return []

    results = []
    for i, line in enumerate(lines):
        score, matched = match_query(line, query_tokens)
        if score > 0:
            start = max(0, i - lines_before)
            end = min(len(lines), i + lines_after)
            context_lines = lines[start:i] + [line] + lines[i+1:end]
            results.append({
                "line_num": i + 1,
                "content": line.rstrip('\n'),
                "score": score,
                "matched_terms": matched,
                "context": [l.rstrip('\n') for l in context_lines]
            })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:max_results]


def main():
    parser = argparse.ArgumentParser(description='Scan text files for relevant information')
    parser.add_argument('file', nargs='?', help='File to scan (stdin if omitted)')
    parser.add_argument('--query', '-q', required=True, help='Search query')
    parser.add_argument('--lines', '-a', type=int, default=5, help='Lines after match')
    parser.add_argument('--before', '-b', type=int, default=2, help='Lines before match')
    parser.add_argument('--max-results', '-n', type=int, default=5, help='Max results')
    parser.add_argument('--output', '-o', help='Output file')
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--brief', action='store_true', help='Brief format (line_num: content only)')
    parser.add_argument('--fuzzy', action='store_true', help='Enable fuzzy matching')

    args = parser.parse_args()

    # Read file
    if args.file:
        filepath = args.file
    else:
        filepath = '<stdin>'
        with open(0, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()

        query = args.query
        query_tokens = tokens(query)
        results = []
        for i, line in enumerate(lines):
            score, matched = match_query(line, query_tokens)
            if score > 0:
                start = max(0, i - args.before)
                end = min(len(lines), i + args.lines)
                results.append({
                    "line_num": i + 1,
                    "content": line.rstrip('\n'),
                    "score": score,
                    "matched_terms": matched,
                    "context": [l.rstrip('\n') for l in lines[start:end]]
                })
        results.sort(key=lambda x: x["score"], reverse=True)
        results = results[:args.max_results]

        if args.json:
            output = json.dumps(results, indent=2, ensure_ascii=False)
        elif args.brief:
            output = '\n'.join(f"{r['line_num']}: {r['content'][:120]}" for r in results)
        else:
            output = ""
            for r in results:
                output += f"\n{'─' * 40}\n"
                output += f"Line {r['line_num']} (score: {r['score']}, matched: {', '.join(r['matched_terms'])})\n"
                output += f"{'─' * 40}\n"
                output += '\n'.join(r['context'])
                output += '\n'
        sys.stdout.write(output)
        return

    if not os.path.exists(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    results = scan_file(filepath, args.query, args.lines, args.before, args.max_results, args.fuzzy)

    if not results:
        print(f"No matches for query: '{args.query}'")
        sys.exit(0)

    if args.json:
        output = json.dumps(results, indent=2, ensure_ascii=False)
    elif args.brief:
        output = '\n'.join(f"Line {r['line_num']}: {r['content'][:120]}" for r in results)
    else:
        output = ""
        for r in results:
            output += f"\n{'─' * 40}\n"
            output += f"Line {r['line_num']} (score: {r['score']}, matched: {', '.join(r['matched_terms'])})\n"
            output += f"{'─' * 40}\n"
            output += '\n'.join(r['context'])
            output += '\n'

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
    else:
        sys.stdout.write(output)

    print(f"\n✓ Found {len(results)} matches", file=sys.stderr)


if __name__ == '__main__':
    main()
