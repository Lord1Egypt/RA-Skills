#!/usr/bin/env python3
"""scar_code_review.py — Code review that learns from failures.

Combines systematic checklist review with scar/reflex arc memory.
When a review misses a bug, record a scar. Next time, the reflex arc
flags similar patterns before the LLM even looks at the code.

Standalone module. Zero external dependencies (stdlib only). Python 3.9+.
Part of Tetra Genesis (B Button Corp).

License: MIT-0
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ============================================================================
# Configuration
# ============================================================================

DEFAULT_SCAR_FILE = Path.cwd() / "review_scars.jsonl"

SEVERITY_ORDER = {"critical": 0, "high": 1, "warning": 2, "info": 3}


def _scar_path(scar_file: Optional[str] = None) -> Path:
    """Resolve scar file path."""
    return Path(scar_file) if scar_file else DEFAULT_SCAR_FILE


def _read_jsonl(filepath: Path) -> list[dict]:
    """Read a JSONL file, skipping malformed lines."""
    if not filepath.exists():
        return []
    entries: list[dict] = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


# ============================================================================
# Scar Storage — review_scars.jsonl
# ============================================================================

def load_review_scars(scar_file: Optional[str] = None) -> list[dict]:
    """Load all review scars from JSONL file.

    Returns list of dicts with keys:
        id, what_missed, pattern, severity, created_at
    """
    return _read_jsonl(_scar_path(scar_file))


def record_miss(
    what_missed: str,
    pattern: str,
    severity: str = "warning",
    scar_file: Optional[str] = None,
) -> dict:
    """Record a scar when a review missed something.

    Args:
        what_missed: Description of what the review failed to catch.
        pattern: Regex pattern that would have caught it.
        severity: One of critical, high, warning, info.

    Returns:
        The recorded scar entry dict.
    """
    if severity not in SEVERITY_ORDER:
        raise ValueError(f"Invalid severity: {severity}. Use: {list(SEVERITY_ORDER)}")

    path = _scar_path(scar_file)
    entry = {
        "id": f"rscar_{int(time.time() * 1000)}",
        "what_missed": what_missed,
        "pattern": pattern,
        "severity": severity,
        "created_at": datetime.now().isoformat(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry


# ============================================================================
# Reflex Arc — Pattern-match diff against past scars. No LLM.
# ============================================================================

def _extract_keywords(text: str) -> list[str]:
    """Extract keywords from text (English 3+ chars, Japanese 2+ chars)."""
    en_words = re.findall(r"[a-zA-Z_]{3,}", text)
    ja_words = re.findall(r"[\u4e00-\u9fff\u30a0-\u30ff]{2,}", text)
    return en_words + ja_words


def reflex_check(
    diff_text: str,
    scars: list[dict],
    threshold_ratio: float = 0.4,
    min_matches: int = 2,
) -> list[str]:
    """Check diff against past review scars. Spinal reflex — no LLM.

    Two-pass check per scar:
      1. Regex match: if scar has a 'pattern' field, try it as regex against diff
      2. Keyword overlap: extract keywords from 'what_missed', check overlap

    Args:
        diff_text: The diff or code text to check.
        scars: List of scar dicts from load_review_scars().
        threshold_ratio: Keyword overlap ratio to trigger (default 0.4).
        min_matches: Minimum keyword matches required (default 2).

    Returns:
        List of block reason strings. Empty list if no collision.
    """
    if not diff_text or not scars:
        return []

    blocks: list[str] = []
    diff_lower = diff_text.lower()

    for scar in scars:
        scar_id = scar.get("id", "unknown")

        # Pass 1: regex pattern match
        pattern = scar.get("pattern", "")
        if pattern:
            try:
                if re.search(pattern, diff_text, re.IGNORECASE | re.MULTILINE):
                    blocks.append(
                        f"scar {scar_id}: pattern matched '{pattern}' "
                        f"— {scar.get('what_missed', '')[:60]}"
                    )
                    continue  # no need for keyword check if regex hit
            except re.error:
                pass  # invalid regex, fall through to keyword check

        # Pass 2: keyword overlap (same algorithm as tetra_scar.py)
        what_missed = scar.get("what_missed", "")
        if not what_missed:
            continue

        keywords = _extract_keywords(what_missed)
        if len(keywords) < 2:
            continue

        matches = [kw for kw in keywords if kw.lower() in diff_lower]
        threshold = max(min_matches, len(keywords) * threshold_ratio)
        if len(matches) >= threshold:
            blocks.append(
                f"scar {scar_id}: keyword collision '{what_missed[:60]}' "
                f"(matched: {', '.join(matches[:5])})"
            )

    return blocks


# ============================================================================
# Checklist Review — Regex/heuristic checks, no LLM
# ============================================================================

def _make_finding(
    dimension: str,
    severity: str,
    message: str,
    line: int,
    code: str = "",
) -> dict:
    """Create a finding dict."""
    return {
        "dimension": dimension,
        "severity": severity,
        "message": message,
        "line": line,
        "code": code.strip()[:120] if code else "",
    }


# --- Security checks ---

_SQL_INJECTION_PATTERNS = [
    # f-string in SQL execute
    re.compile(
        r"""(?:execute|cursor\.execute|query|raw)\s*\(\s*f['"]""",
        re.IGNORECASE,
    ),
    # .format() in SQL execute
    re.compile(
        r"""(?:execute|cursor\.execute|query|raw)\s*\(\s*['"].*\.format\s*\(""",
        re.IGNORECASE,
    ),
    # % formatting with variables (not %s placeholders followed by tuple arg)
    re.compile(
        r"""(?:execute|cursor\.execute|query|raw)\s*\(\s*['"].*%s.*['"]\s*%\s*""",
        re.IGNORECASE,
    ),
    # String concatenation in SQL
    re.compile(
        r"""(?:SELECT|INSERT|UPDATE|DELETE|DROP)\s+.*\+\s*(?:request|user|input|param|args)""",
        re.IGNORECASE,
    ),
]

_SECRET_PATTERNS = [
    re.compile(
        r"""(?:password|passwd|secret|api_key|apikey|token|private_key)\s*=\s*['"][^'"]{4,}['"]""",
        re.IGNORECASE,
    ),
    re.compile(
        r"""(?:AWS_SECRET|GITHUB_TOKEN|SLACK_TOKEN)\s*=\s*['"][^'"]+['"]""",
        re.IGNORECASE,
    ),
]

_XSS_PATTERNS = [
    re.compile(r"""\.innerHTML\s*=""", re.IGNORECASE),
    re.compile(r"""document\.write\s*\(""", re.IGNORECASE),
    re.compile(r"""v-html\s*=""", re.IGNORECASE),
    re.compile(r"""dangerouslySetInnerHTML""", re.IGNORECASE),
]

_EVAL_PATTERNS = [
    re.compile(r"""\beval\s*\("""),
    re.compile(r"""\bexec\s*\("""),
    re.compile(r"""subprocess\..*shell\s*=\s*True""", re.IGNORECASE),
    re.compile(r"""\bos\.system\s*\("""),
]


def _check_security(lines: list[str]) -> list[dict]:
    findings: list[dict] = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//"):
            continue

        for pat in _SQL_INJECTION_PATTERNS:
            if pat.search(line):
                findings.append(_make_finding(
                    "security", "critical",
                    "Possible SQL injection via string formatting",
                    i, line,
                ))
                break

        for pat in _SECRET_PATTERNS:
            if pat.search(line):
                findings.append(_make_finding(
                    "security", "critical",
                    "Possible hardcoded secret or credential",
                    i, line,
                ))
                break

        for pat in _XSS_PATTERNS:
            if pat.search(line):
                findings.append(_make_finding(
                    "security", "high",
                    "Possible XSS via unsafe HTML insertion",
                    i, line,
                ))
                break

        for pat in _EVAL_PATTERNS:
            if pat.search(line):
                findings.append(_make_finding(
                    "security", "high",
                    "Dangerous eval/exec/shell usage",
                    i, line,
                ))
                break

    return findings


# --- Performance checks ---

_N_PLUS_ONE_LOOP_START = re.compile(r"""^\s*(?:for|while)\b""")
_QUERY_IN_BODY = re.compile(
    r"""(?:\.query|\.execute|\.find|\.filter|\.get|\.fetch|\.select|\.objects\.)""",
    re.IGNORECASE,
)
_UNBOUNDED_SELECT = re.compile(
    r"""SELECT\s+(?:\*|[\w,\s]+)\s+FROM\s+\w+\s*(?:;|$|['"])""",
    re.IGNORECASE,
)
_MISSING_PAGINATION = re.compile(
    r"""\.(?:all|find|filter|objects\.filter)\s*\(\s*\)""",
    re.IGNORECASE,
)


def _check_performance(lines: list[str]) -> list[dict]:
    findings: list[dict] = []
    in_loop = False
    loop_depth = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track loop context for N+1 detection
        if _N_PLUS_ONE_LOOP_START.match(stripped):
            in_loop = True
            loop_depth += 1

        if in_loop and _QUERY_IN_BODY.search(stripped):
            findings.append(_make_finding(
                "performance", "warning",
                "Possible N+1 query pattern: query inside loop",
                i, line,
            ))

        # Simple heuristic: closing brace/dedent ends loop
        if in_loop and stripped in ("}", "") and loop_depth > 0:
            loop_depth -= 1
            if loop_depth == 0:
                in_loop = False

        if _UNBOUNDED_SELECT.search(stripped):
            if not re.search(r"\b(?:LIMIT|WHERE|TOP)\b", stripped, re.IGNORECASE):
                findings.append(_make_finding(
                    "performance", "info",
                    "Unbounded SELECT without LIMIT or WHERE",
                    i, line,
                ))

        if _MISSING_PAGINATION.search(stripped):
            findings.append(_make_finding(
                "performance", "info",
                "Collection query without pagination/limit",
                i, line,
            ))

    return findings


# --- Correctness checks ---

_UNCHECKED_NULL = re.compile(
    r"""(?:None|null|nil|undefined)\b.*(?:\.|->)\w+|(?:\.|->)\w+.*(?:None|null|nil|undefined)""",
)
_OFF_BY_ONE = re.compile(
    r"""(?:<=\s*len\s*\(|<=\s*\.(?:length|size|count)\b|range\s*\(\s*1\s*,\s*\w+\s*\))""",
)
_UNHANDLED_PROMISE = re.compile(
    r"""(?:^|\s)(?!await\s)(?:fetch|axios|\.get|\.post|\.put|\.delete|\.patch)\s*\(""",
)


def _check_correctness(lines: list[str]) -> list[dict]:
    findings: list[dict] = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//"):
            continue

        if _OFF_BY_ONE.search(stripped):
            findings.append(_make_finding(
                "correctness", "warning",
                "Possible off-by-one: check boundary condition",
                i, line,
            ))

        if _UNHANDLED_PROMISE.search(stripped):
            # Skip lines that have .then or .catch or await on same line
            if not re.search(r"(?:\.then|\.catch|await)\b", stripped):
                findings.append(_make_finding(
                    "correctness", "warning",
                    "Possible unhandled async call (no await/then/catch)",
                    i, line,
                ))

    return findings


# --- Maintainability checks ---

def _check_maintainability(lines: list[str]) -> list[dict]:
    findings: list[dict] = []

    # Long function detection
    func_start_re = re.compile(
        r"""^\s*(?:def |function |(?:async\s+)?(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\()"""
    )
    func_starts: list[tuple[int, int]] = []  # (line_num, indent_level)

    for i, line in enumerate(lines, 1):
        if func_start_re.match(line):
            indent = len(line) - len(line.lstrip())
            func_starts.append((i, indent))

    # Check function lengths
    for idx, (start, indent) in enumerate(func_starts):
        # Function ends at next function at same/lower indent, or EOF
        if idx + 1 < len(func_starts):
            end = func_starts[idx + 1][0]
        else:
            end = len(lines) + 1
        length = end - start
        if length > 50:
            findings.append(_make_finding(
                "maintainability", "warning",
                f"Function exceeds 50 lines ({length} lines)",
                start, lines[start - 1] if start <= len(lines) else "",
            ))

    # Deep nesting detection (>4 levels)
    for i, line in enumerate(lines, 1):
        if not line.strip():
            continue
        # Count indent level
        stripped = line.lstrip()
        indent_chars = len(line) - len(stripped)
        # Estimate indent level (assume 2 or 4 space indent, or tabs)
        if "\t" in line[:indent_chars]:
            level = line[:indent_chars].count("\t")
        else:
            level = indent_chars // 4 if indent_chars >= 4 else indent_chars // 2
        if level > 4 and stripped and not stripped.startswith(("#", "//", "*")):
            findings.append(_make_finding(
                "maintainability", "info",
                f"Deep nesting (level {level}): consider extracting a function",
                i, line,
            ))

    # Magic number detection
    magic_re = re.compile(
        r"""(?<!=)\s(?<!\w)(\d{2,})(?!\w)(?!\s*[;:,\]\})\n])"""
    )
    # Exclude common non-magic numbers
    _NON_MAGIC = frozenset({"10", "16", "32", "64", "100", "200", "256", "404", "500", "1000"})
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith(("#", "//", "*", "import", "from")):
            continue
        for m in magic_re.finditer(line):
            num = m.group(1)
            if num not in _NON_MAGIC and not num.startswith("0x"):
                findings.append(_make_finding(
                    "maintainability", "info",
                    f"Magic number {num}: consider naming as a constant",
                    i, line,
                ))
                break  # one per line

    return findings


# ============================================================================
# Main Review Function
# ============================================================================

def review(
    file_path: str,
    scars: Optional[list[dict]] = None,
    scar_file: Optional[str] = None,
) -> list[dict]:
    """Run all checklist dimensions against a file.

    Args:
        file_path: Path to the source file to review.
        scars: Optional pre-loaded scars. If None and scar_file is set,
               loads from scar_file. If both None, skips scar check.

    Returns:
        List of finding dicts, sorted by severity.
        Each has: dimension, severity, message, line, code.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    content = path.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()

    findings: list[dict] = []

    # Run checklist dimensions
    findings.extend(_check_security(lines))
    findings.extend(_check_performance(lines))
    findings.extend(_check_correctness(lines))
    findings.extend(_check_maintainability(lines))

    # Run scar reflex against file content
    if scars is None and scar_file:
        scars = load_review_scars(scar_file)
    if scars:
        blocks = reflex_check(content, scars)
        for block in blocks:
            findings.append(_make_finding(
                "scar", "critical",
                f"Scar reflex: {block}",
                0, "",
            ))

    # Sort by severity
    findings.sort(key=lambda f: SEVERITY_ORDER.get(f["severity"], 99))
    return findings


# ============================================================================
# CLI Interface
# ============================================================================

def _cli_review(args: object) -> None:
    """CLI handler for 'review' subcommand."""
    scars = load_review_scars(args.scar_file) if args.scar_file else None
    try:
        findings = review(args.file, scars=scars, scar_file=args.scar_file)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    if not findings:
        print("No findings.")
        sys.exit(0)

    counts: dict[str, int] = {}
    for f in findings:
        sev = f["severity"]
        counts[sev] = counts.get(sev, 0) + 1
        line_info = f" (line {f['line']})" if f["line"] else ""
        print(f"[{sev}] [{f['dimension']}] {f['message']}{line_info}")
        if f["code"]:
            print(f"  > {f['code']}")

    parts = [f"{v} {k}" for k, v in sorted(counts.items(), key=lambda x: SEVERITY_ORDER.get(x[0], 99))]
    print(f"\n{len(findings)} findings ({', '.join(parts)})")

    if counts.get("critical", 0) > 0:
        sys.exit(1)


def _cli_check_diff(args: object) -> None:
    """CLI handler for 'check-diff' subcommand."""
    diff_path = Path(args.diff_file)
    if not diff_path.exists():
        print(f"ERROR: File not found: {args.diff_file}", file=sys.stderr)
        sys.exit(2)

    diff_text = diff_path.read_text(encoding="utf-8", errors="replace")
    scars = load_review_scars(args.scar_file)

    blocks = reflex_check(diff_text, scars)
    if not blocks:
        print("CLEAR — no scar collisions.")
        sys.exit(0)

    for b in blocks:
        print(f"BLOCKED: {b}")
    sys.exit(1)


def _cli_record_miss(args: object) -> None:
    """CLI handler for 'record-miss' subcommand."""
    try:
        entry = record_miss(
            what_missed=args.what_missed,
            pattern=args.pattern,
            severity=args.severity,
            scar_file=args.scar_file,
        )
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    print(f"SCAR RECORDED: {entry['id']}")
    print(f"  what_missed: {entry['what_missed']}")
    print(f"  pattern: {entry['pattern']}")
    print(f"  severity: {entry['severity']}")


def _cli_list_scars(args: object) -> None:
    """CLI handler for 'list-scars' subcommand."""
    scars = load_review_scars(args.scar_file)
    if not scars:
        print("No review scars recorded yet.")
        return
    for s in scars:
        print(f"[{s.get('created_at', '?')}] {s.get('id', '?')} ({s.get('severity', '?')})")
        print(f"  missed: {s.get('what_missed', '')[:80]}")
        print(f"  pattern: {s.get('pattern', '')[:80]}")
        print()


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="scar-code-review: Code review that learns from failures"
    )
    parser.add_argument(
        "--scar-file", default=None,
        help="Path to review_scars.jsonl (default: ./review_scars.jsonl)",
    )
    sub = parser.add_subparsers(dest="command")

    # review
    p_review = sub.add_parser("review", help="Review a source file")
    p_review.add_argument("file", help="Path to file to review")
    p_review.set_defaults(func=_cli_review)

    # check-diff
    p_diff = sub.add_parser("check-diff", help="Check diff against scars")
    p_diff.add_argument("diff_file", help="Path to diff file")
    p_diff.set_defaults(func=_cli_check_diff)

    # record-miss
    p_miss = sub.add_parser("record-miss", help="Record a missed finding")
    p_miss.add_argument("--what-missed", required=True, help="What the review missed")
    p_miss.add_argument("--pattern", required=True, help="Regex pattern to catch it")
    p_miss.add_argument(
        "--severity", default="warning",
        choices=["critical", "high", "warning", "info"],
    )
    p_miss.set_defaults(func=_cli_record_miss)

    # list-scars
    p_ls = sub.add_parser("list-scars", help="List recorded review scars")
    p_ls.set_defaults(func=_cli_list_scars)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
