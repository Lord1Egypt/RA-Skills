#!/usr/bin/env python3
"""
requirements-checker — Validate, lint, sort, and compare Python requirements.txt files.
Pure stdlib, no external dependencies.
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Dict


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class Issue:
    severity: str          # "error", "warning", "info"
    rule: str              # rule/check identifier
    line_no: Optional[int] # 1-based line number, or None for file-level
    line: Optional[str]    # original line text
    message: str

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "rule": self.rule,
            "line_no": self.line_no,
            "line": self.line,
            "message": self.message,
        }


@dataclass
class ParsedRequirement:
    line_no: int
    raw: str                    # original text
    name: str                   # normalised package name
    original_name: str          # as written
    extras: List[str]
    specifier: str              # full specifier string, e.g. ">=1.0,<2.0"
    url: Optional[str]          # for URL-style deps
    is_comment: bool
    is_blank: bool
    is_option: bool             # -r, --index-url, etc.
    is_editable: bool           # -e
    is_vcs: bool                # git+, hg+, svn+, bzr+


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

# PEP 508 package name pattern
_NAME_RE = re.compile(
    r'^([A-Za-z0-9]([A-Za-z0-9._-]*[A-Za-z0-9])?)'   # package name
    r'(\[([^\]]*)\])?'                                  # optional extras
    r'\s*'
    r'((?:[><=!~^][=<>]?[^\s,;#]+(?:\s*,\s*[><=!~^][=<>]?[^\s,;#]+)*)?)'  # version spec
    r'\s*'
    r'(;[^#]*)?'                                        # environment marker
    r'(\s*#.*)?$'                                       # inline comment
)

_VALID_OPS = {'==', '>=', '<=', '!=', '~=', '>', '<'}

_VCS_PREFIXES = ('git+', 'hg+', 'svn+', 'bzr+')

_OPTION_RE = re.compile(r'^-[re]|^--(?:requirement|extra-index-url|index-url|no-index|'
                        r'find-links|trusted-host|constraint|pre|editable)\b')

_VERSION_PART_RE = re.compile(
    r'([><=!~^]{1,3})\s*([A-Za-z0-9.*+!_-]+)'
)


def normalise_name(name: str) -> str:
    """PEP 503 normalisation."""
    return re.sub(r'[-_.]+', '-', name).lower()


def parse_line(line_no: int, raw: str) -> ParsedRequirement:
    """Parse a single requirements.txt line into a ParsedRequirement."""
    stripped = raw.strip()

    # blank
    if not stripped:
        return ParsedRequirement(
            line_no=line_no, raw=raw, name='', original_name='',
            extras=[], specifier='', url=None,
            is_comment=False, is_blank=True, is_option=False,
            is_editable=False, is_vcs=False,
        )

    # pure comment
    if stripped.startswith('#'):
        return ParsedRequirement(
            line_no=line_no, raw=raw, name='', original_name='',
            extras=[], specifier='', url=None,
            is_comment=True, is_blank=False, is_option=False,
            is_editable=False, is_vcs=False,
        )

    # options / flags
    if _OPTION_RE.match(stripped):
        is_editable = stripped.startswith('-e') or stripped.startswith('--editable')
        return ParsedRequirement(
            line_no=line_no, raw=raw, name='', original_name='',
            extras=[], specifier='', url=None,
            is_comment=False, is_blank=False, is_option=True,
            is_editable=is_editable, is_vcs=False,
        )

    # VCS / URL deps (git+https://... etc.)
    is_vcs = any(stripped.lower().startswith(p) for p in _VCS_PREFIXES)
    if is_vcs or re.match(r'https?://', stripped, re.I):
        # Try to extract egg name
        egg_match = re.search(r'#egg=([A-Za-z0-9._-]+)', stripped)
        name = egg_match.group(1) if egg_match else ''
        return ParsedRequirement(
            line_no=line_no, raw=raw, name=normalise_name(name),
            original_name=name, extras=[], specifier='', url=stripped,
            is_comment=False, is_blank=False, is_option=False,
            is_editable=False, is_vcs=is_vcs,
        )

    # Strip inline comment for parsing
    no_comment = re.sub(r'\s#.*$', '', stripped)

    m = _NAME_RE.match(no_comment)
    if m:
        original_name = m.group(1)
        extras_str = m.group(4) or ''
        extras = [e.strip() for e in extras_str.split(',') if e.strip()] if extras_str else []
        specifier = (m.group(5) or '').strip()
        return ParsedRequirement(
            line_no=line_no, raw=raw,
            name=normalise_name(original_name),
            original_name=original_name,
            extras=extras,
            specifier=specifier,
            url=None,
            is_comment=False, is_blank=False, is_option=False,
            is_editable=False, is_vcs=False,
        )

    # Fallback: unrecognised
    return ParsedRequirement(
        line_no=line_no, raw=raw, name='', original_name='',
        extras=[], specifier='', url=None,
        is_comment=False, is_blank=False, is_option=False,
        is_editable=False, is_vcs=False,
    )


def read_requirements(path: str) -> Tuple[List[str], List[ParsedRequirement]]:
    """Read a file and return (raw_lines, parsed_reqs)."""
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            raw_lines = fh.readlines()
    except FileNotFoundError:
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(2)
    except PermissionError:
        print(f"error: permission denied: {path}", file=sys.stderr)
        sys.exit(2)

    parsed = [parse_line(i + 1, line) for i, line in enumerate(raw_lines)]
    return raw_lines, parsed


def validate_specifier(specifier: str) -> List[str]:
    """Return list of error strings for invalid version specifier parts."""
    errors = []
    if not specifier:
        return errors
    parts = [p.strip() for p in specifier.split(',') if p.strip()]
    for part in parts:
        m = re.match(r'^([><=!~^]{1,3})\s*(.+)$', part)
        if not m:
            errors.append(f"unparseable specifier part '{part}'")
            continue
        op = m.group(1)
        if op not in _VALID_OPS:
            errors.append(f"invalid operator '{op}'")
    return errors


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_validate(path: str, ignored_rules: List[str]) -> List[Issue]:
    issues: List[Issue] = []
    raw_lines, parsed = read_requirements(path)

    # Track seen names for duplicate detection
    seen: Dict[str, int] = {}  # normalised name -> first line_no

    for req in parsed:
        line = req.raw.rstrip('\n')

        # Trailing whitespace (info)
        if not req.is_blank and req.raw != req.raw.rstrip() + '\n' and req.raw != req.raw.rstrip():
            if req.raw.endswith('  ') or req.raw.rstrip('\n').endswith(' ') or req.raw.rstrip('\n').endswith('\t'):
                issues.append(Issue('info', 'trailing-whitespace', req.line_no, line,
                                    "Trailing whitespace"))

        if req.is_blank:
            # Blank/whitespace-only lines are fine but note them
            if req.raw.strip() == '' and req.raw != '\n' and req.raw != '':
                issues.append(Issue('info', 'whitespace-only-line', req.line_no, line,
                                    "Whitespace-only line (not truly blank)"))
            continue

        if req.is_comment:
            continue

        if req.is_option:
            if req.is_editable:
                issues.append(Issue('warning', 'editable-install', req.line_no, line,
                                    f"Editable install (-e) — not suitable for production pinning"))
            elif re.match(r'--extra-index-url|--index-url', line.strip()):
                issues.append(Issue('warning', 'custom-index-url', req.line_no, line,
                                    "Custom index URL — ensure it is trusted"))
            elif re.match(r'-r|--requirement', line.strip()):
                issues.append(Issue('info', 'requirement-include', req.line_no, line,
                                    "Nested -r include — validate the referenced file separately"))
            continue

        if req.is_vcs:
            issues.append(Issue('warning', 'vcs-dependency', req.line_no, line,
                                f"VCS dependency — not reproducible without a pinned commit ref"))
            continue

        if req.url:
            issues.append(Issue('info', 'url-dependency', req.line_no, line,
                                "URL dependency — ensure URL is stable and versioned"))
            continue

        # Unrecognised / invalid format
        if not req.name:
            issues.append(Issue('error', 'invalid-format', req.line_no, line,
                                f"Line does not match PEP 508 format"))
            continue

        # Invalid specifier operators
        spec_errors = validate_specifier(req.specifier)
        for err in spec_errors:
            issues.append(Issue('error', 'invalid-specifier', req.line_no, line, err))

        # Duplicate packages
        if req.name in seen:
            issues.append(Issue('error', 'duplicate-package', req.line_no, line,
                                f"Duplicate package '{req.original_name}' "
                                f"(first seen on line {seen[req.name]})"))
        else:
            seen[req.name] = req.line_no

    # Check for missing final newline
    if raw_lines and not raw_lines[-1].endswith('\n'):
        issues.append(Issue('info', 'missing-final-newline', len(raw_lines), raw_lines[-1].rstrip(),
                            "File does not end with a newline"))

    return [i for i in issues if i.rule not in ignored_rules]


def cmd_lint(path: str, ignored_rules: List[str]) -> List[Issue]:
    """Lint for best practices on top of validation issues."""
    issues = cmd_validate(path, ignored_rules)

    _, parsed = read_requirements(path)

    active = [r for r in parsed if not r.is_blank and not r.is_comment
              and not r.is_option and not r.is_vcs and not r.url and r.name]

    # Alphabetical order check
    names = [r.original_name.lower() for r in active]
    sorted_names = sorted(names)
    if names != sorted_names:
        # Find first out-of-order
        for i in range(1, len(names)):
            if names[i] < names[i - 1]:
                req = active[i]
                issues.append(Issue('warning', 'non-alphabetical', req.line_no, req.raw.rstrip('\n'),
                                    f"'{req.original_name}' is out of alphabetical order"))
                break

    # Per-package lint
    operator_set = set()
    for req in active:
        line = req.raw.rstrip('\n')

        # Unpinned (no specifier at all)
        if not req.specifier:
            issues.append(Issue('warning', 'unpinned', req.line_no, line,
                                f"'{req.original_name}' has no version specifier — unpinned dependency"))

        else:
            parts = [p.strip() for p in req.specifier.split(',') if p.strip()]
            ops = set()
            has_exact = False
            has_gte = False
            has_upper = False
            for part in parts:
                m = re.match(r'^([><=!~^]{1,3})', part)
                if m:
                    op = m.group(1)
                    ops.add(op)
                    operator_set.add(op)
                    if op == '==':
                        has_exact = True
                    if op in ('>=', '>'):
                        has_gte = True
                    if op in ('<=', '<'):
                        has_upper = True

            # >= without upper bound
            if has_gte and not has_upper and not has_exact:
                issues.append(Issue('warning', 'no-upper-bound', req.line_no, line,
                                    f"'{req.original_name}' uses >= without an upper bound — "
                                    f"may break on major version bumps"))

        # Trailing whitespace
        if req.raw.rstrip('\n') != req.raw.rstrip('\n').rstrip():
            issues.append(Issue('info', 'trailing-whitespace', req.line_no, line,
                                "Trailing whitespace"))

    # Mixed operators (some ==, some >=) — file-level warning
    if '==' in operator_set and '>=' in operator_set:
        if 'mixed-operators' not in ignored_rules:
            issues.append(Issue('info', 'mixed-operators', None, None,
                                "File mixes == (exact pins) and >= (range) operators — "
                                "consider a consistent pinning strategy"))

    # Deduplicate issues by (rule, line_no)
    seen_keys = set()
    deduped = []
    for iss in issues:
        key = (iss.rule, iss.line_no)
        if key not in seen_keys:
            seen_keys.add(key)
            deduped.append(iss)

    return [i for i in deduped if i.rule not in ignored_rules]


def cmd_duplicates(path: str, ignored_rules: List[str]) -> List[Issue]:
    issues: List[Issue] = []
    _, parsed = read_requirements(path)

    seen: Dict[str, List[Tuple[int, str]]] = {}
    for req in parsed:
        if req.is_blank or req.is_comment or req.is_option or not req.name:
            continue
        seen.setdefault(req.name, []).append((req.line_no, req.raw.rstrip('\n')))

    for name, occurrences in seen.items():
        if len(occurrences) > 1:
            line_nums = ', '.join(str(ln) for ln, _ in occurrences)
            # Report each duplicate line as an error
            for i, (ln, raw) in enumerate(occurrences):
                if i == 0:
                    issues.append(Issue('error', 'duplicate-package', ln, raw,
                                        f"Package '{name}' appears {len(occurrences)} times "
                                        f"(lines {line_nums}) — keeping first occurrence"))
                else:
                    issues.append(Issue('error', 'duplicate-package', ln, raw,
                                        f"Duplicate of '{name}' first seen on line {occurrences[0][0]}"))

    return issues


def cmd_sort(path: str, write: bool) -> str:
    """Return sorted requirements as a string. Optionally write back."""
    raw_lines, parsed = read_requirements(path)

    # Separate header comments/options from actual requirements
    header_lines: List[str] = []
    req_lines: List[Tuple[str, str]] = []  # (sort_key, raw_line)
    trailer: List[str] = []

    # Strategy: sort only non-blank, non-comment, non-option requirement lines
    # Keep comments that appear before the first package with their group
    # Simple approach: stable-sort all package lines by normalised name,
    # preserve comments and options in place (prepended to following package)

    groups: List[Tuple[str, List[str]]] = []  # (sort_key, lines_in_group)
    current_prefix: List[str] = []

    for req in parsed:
        if req.is_blank or req.is_comment or req.is_option:
            current_prefix.append(req.raw)
        elif req.name or req.url or req.is_vcs:
            sort_key = req.name or (req.url or '').lower()
            group_lines = current_prefix + [req.raw]
            groups.append((sort_key, group_lines))
            current_prefix = []
        else:
            # Unrecognised — keep as-is with prefix
            sort_key = ''
            group_lines = current_prefix + [req.raw]
            groups.append((sort_key, group_lines))
            current_prefix = []

    # Remaining prefix (trailing comments/blanks)
    trailing = current_prefix

    # Sort groups by sort_key (case-insensitive), stable for equal keys
    groups.sort(key=lambda g: g[0])

    result_lines: List[str] = []
    for _, grp_lines in groups:
        result_lines.extend(grp_lines)
    result_lines.extend(trailing)

    output = ''.join(result_lines)
    # Ensure final newline
    if output and not output.endswith('\n'):
        output += '\n'

    if write:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(output)
        print(f"Wrote sorted requirements to {path}", file=sys.stderr)

    return output


def cmd_compare(path1: str, path2: str) -> List[Issue]:
    """Compare two requirements files, returning issues describing differences."""
    issues: List[Issue] = []

    def load_map(path: str) -> Dict[str, ParsedRequirement]:
        _, parsed = read_requirements(path)
        m: Dict[str, ParsedRequirement] = {}
        for r in parsed:
            if not r.is_blank and not r.is_comment and not r.is_option and r.name:
                m[r.name] = r
        return m

    map1 = load_map(path1)
    map2 = load_map(path2)

    all_names = sorted(set(map1) | set(map2))

    for name in all_names:
        if name in map1 and name not in map2:
            r = map1[name]
            issues.append(Issue('warning', 'removed', r.line_no, r.raw.rstrip('\n'),
                                f"REMOVED: {r.original_name}{r.specifier}  (was in {path1})"))
        elif name in map2 and name not in map1:
            r = map2[name]
            issues.append(Issue('info', 'added', r.line_no, r.raw.rstrip('\n'),
                                f"ADDED:   {r.original_name}{r.specifier}  (new in {path2})"))
        else:
            r1, r2 = map1[name], map2[name]
            if r1.specifier != r2.specifier:
                issues.append(Issue('info', 'changed', r2.line_no, r2.raw.rstrip('\n'),
                                    f"CHANGED: {r1.original_name}  "
                                    f"{r1.specifier or '(unpinned)'} → {r2.specifier or '(unpinned)'}"))

    return issues


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def _severity_order(s: str) -> int:
    return {'error': 0, 'warning': 1, 'info': 2}.get(s, 3)


def format_output(issues: List[Issue], fmt: str, source: str = '', extra: str = '') -> str:
    errors = [i for i in issues if i.severity == 'error']
    warnings = [i for i in issues if i.severity == 'warning']
    infos = [i for i in issues if i.severity == 'info']

    if fmt == 'json':
        data = {
            "source": source,
            "summary": {
                "total": len(issues),
                "errors": len(errors),
                "warnings": len(warnings),
                "info": len(infos),
            },
            "issues": [i.to_dict() for i in issues],
        }
        if extra:
            data["extra"] = extra
        return json.dumps(data, indent=2)

    elif fmt == 'markdown':
        lines = []
        if source:
            lines.append(f"## requirements-checker: `{source}`\n")
        lines.append(f"**{len(issues)} issue(s):** "
                     f"{len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info(s)\n")
        if issues:
            lines.append("| Line | Severity | Rule | Message |")
            lines.append("|------|----------|------|---------|")
            for i in sorted(issues, key=lambda x: (_severity_order(x.severity), x.line_no or 0)):
                ln = str(i.line_no) if i.line_no else '—'
                lines.append(f"| {ln} | {i.severity} | `{i.rule}` | {i.message} |")
        else:
            lines.append("No issues found.")
        if extra:
            lines.append(f"\n{extra}")
        return '\n'.join(lines)

    else:  # text (default)
        lines = []
        if source:
            lines.append(f"File: {source}")
        if issues:
            for i in sorted(issues, key=lambda x: (_severity_order(x.severity), x.line_no or 0)):
                ln = f"line {i.line_no}" if i.line_no else "file"
                sev = i.severity.upper()
                lines.append(f"  [{sev}] {ln}  ({i.rule})  {i.message}")
                if i.line and i.line_no:
                    lines.append(f"         {i.line}")
        else:
            lines.append("  No issues found.")
        lines.append("")
        lines.append(f"Summary: {len(issues)} issue(s) — "
                     f"{len(errors)} error(s), {len(warnings)} warning(s), {len(infos)} info(s)")
        if extra:
            lines.append(extra)
        return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='requirements-checker',
        description='Validate, lint, sort, and compare Python requirements.txt files.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  requirements-checker validate requirements.txt
  requirements-checker lint requirements.txt --strict
  requirements-checker duplicates requirements.txt --format json
  requirements-checker sort requirements.txt --write
  requirements-checker compare requirements.txt requirements-dev.txt
        """,
    )
    parser.add_argument('--format', '-f', choices=['text', 'json', 'markdown'],
                        default='text', help='Output format (default: text)')
    parser.add_argument('--strict', action='store_true',
                        help='Exit 1 on any issue (CI mode)')
    parser.add_argument('--ignore', metavar='RULE', action='append', default=[],
                        help='Ignore a specific lint/validation rule (repeatable)')

    sub = parser.add_subparsers(dest='command', required=True)

    # validate
    p_val = sub.add_parser('validate', help='Validate requirements.txt format')
    p_val.add_argument('file', help='Path to requirements.txt')

    # lint
    p_lint = sub.add_parser('lint', help='Lint for best practices')
    p_lint.add_argument('file', help='Path to requirements.txt')

    # duplicates
    p_dup = sub.add_parser('duplicates', help='Find duplicate packages')
    p_dup.add_argument('file', help='Path to requirements.txt')

    # sort
    p_sort = sub.add_parser('sort', help='Sort requirements alphabetically')
    p_sort.add_argument('file', help='Path to requirements.txt')
    p_sort.add_argument('--write', action='store_true',
                        help='Write sorted output in-place')

    # compare
    p_cmp = sub.add_parser('compare', help='Compare two requirements files')
    p_cmp.add_argument('file1', help='Base requirements file')
    p_cmp.add_argument('file2', help='Target requirements file')

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    fmt = args.format
    strict = args.strict
    ignored = list(args.ignore)

    if args.command == 'validate':
        issues = cmd_validate(args.file, ignored)
        print(format_output(issues, fmt, source=args.file))
        if strict and issues:
            return 1
        errors = [i for i in issues if i.severity == 'error']
        return 1 if errors else 0

    elif args.command == 'lint':
        issues = cmd_lint(args.file, ignored)
        print(format_output(issues, fmt, source=args.file))
        if strict and issues:
            return 1
        errors = [i for i in issues if i.severity == 'error']
        return 1 if errors else 0

    elif args.command == 'duplicates':
        issues = cmd_duplicates(args.file, ignored)
        print(format_output(issues, fmt, source=args.file))
        if strict and issues:
            return 1
        return 1 if issues else 0

    elif args.command == 'sort':
        sorted_output = cmd_sort(args.file, write=args.write)
        if not args.write:
            print(sorted_output, end='')
        return 0

    elif args.command == 'compare':
        issues = cmd_compare(args.file1, args.file2)
        extra_note = f"Comparing:\n  A: {args.file1}\n  B: {args.file2}"
        print(format_output(issues, fmt, source=f"{args.file1} vs {args.file2}",
                            extra=extra_note))
        if strict and issues:
            return 1
        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
