#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

SUCCESS_PATTERNS = [
    r"successfully",
    r"published\s+.+@\d+\.\d+\.\d+",
    r"\[ok\]",
    r"exited with code 0",
    r"latest:\s*\d+\.\d+\.\d+",
]
FAIL_PATTERNS = [
    r"validation failed",
    r"error:",
    r"uncaught",
    r"401",
    r"unauthorized",
    r"skill not found",
    r"path must be a folder",
    r"command exited with code [1-9]",
]
PARTIAL_PATTERNS = [
    r"preparing",
    r"fetching",
    r"pending",
    r"still running",
    r"waiting",
    r"processing",
    r"command still running",
]
WARNING_PATTERNS = [
    r"warnings?:\s*yes",
    r"warn",
    r"cooldown",
    r"fallback",
    r"retry",
]


def classify(text: str):
    lower = text.lower()
    success = any(re.search(p, lower) for p in SUCCESS_PATTERNS)
    failure = any(re.search(p, lower) for p in FAIL_PATTERNS)
    partial = any(re.search(p, lower) for p in PARTIAL_PATTERNS)
    warning = any(re.search(p, lower) for p in WARNING_PATTERNS)
    if failure:
        return "failure"
    if success and warning:
        return "partial"
    if success and not partial:
        return "success"
    if partial and not success:
        return "partial"
    if success and partial:
        return "ambiguous"
    return "ambiguous"


def decisive_lines(text: str):
    out = []
    for line in text.splitlines():
        low = line.lower()
        if any(re.search(p, low) for p in SUCCESS_PATTERNS + FAIL_PATTERNS + PARTIAL_PATTERNS + WARNING_PATTERNS):
            out.append(line)
    return out[:12]


def detect_context(text: str):
    lower = text.lower()
    if 'publish' in lower or 'clawhub' in lower:
        return 'publish'
    if 'package' in lower or '.skill' in lower:
        return 'package'
    if '401' in lower or 'authentication' in lower or 'invalid api key' in lower:
        return 'auth'
    if 'still running' in lower or 'session ' in lower:
        return 'process'
    return 'generic'


def recommendation(verdict: str, context: str):
    base = {
        "success": "Evidence supports moving to the next step.",
        "failure": "Stop and fix the reported error before proceeding.",
        "partial": "Do not claim success yet; inspect warnings or incomplete state first.",
        "ambiguous": "Read the full output manually before deciding the next step.",
    }[verdict]
    extra = {
        'publish': {
            'success': ' Verify latest/version before announcing success.',
            'failure': ' Do not say the skill was published.',
            'partial': ' Wait for the final publish result before claiming it worked.',
            'ambiguous': ' Check latest/version and the page scan state.',
        },
        'package': {
            'success': ' Confirm the archive path exists.',
            'failure': ' Fix validation/path issues before retrying packaging.',
            'partial': ' Packaging has not produced proof of an artifact yet.',
            'ambiguous': ' Look for an explicit "Successfully packaged" line.',
        },
        'auth': {
            'success': ' Confirm the authenticated action actually completed.',
            'failure': ' Treat credentials as invalid until re-verified.',
            'partial': ' Auth state is unresolved; do not continue dependent steps.',
            'ambiguous': ' Check provider, profile, and exact credential mode.',
        },
        'process': {
            'success': ' Confirm the process ended and produced the expected outcome.',
            'failure': ' Inspect logs before retrying or killing related work.',
            'partial': ' Poll or read more logs instead of narrating completion.',
            'ambiguous': ' Get more process output before deciding.',
        },
        'generic': {k: '' for k in ['success','failure','partial','ambiguous']},
    }
    return base + extra[context][verdict]


def main():
    ap = argparse.ArgumentParser(description='Audit tool/command output before taking the next step')
    ap.add_argument('path', nargs='?')
    args = ap.parse_args()

    if args.path:
        text = Path(args.path).read_text(encoding='utf-8')
    else:
        text = sys.stdin.read()

    verdict = classify(text)
    context = detect_context(text)
    print(f'Context: {context}')
    print(f'Verdict: {verdict}')
    print(f'Recommendation: {recommendation(verdict, context)}')
    print('Decisive lines:')
    lines = decisive_lines(text)
    if lines:
        for line in lines:
            print(f'- {line}')
    else:
        print('- No decisive lines found; inspect the full output manually.')


if __name__ == '__main__':
    main()
