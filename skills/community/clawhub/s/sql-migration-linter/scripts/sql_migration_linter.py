#!/usr/bin/env python3
"""SQL Migration Linter — rule-based linter for .sql migration files.

Pure Python stdlib. No dependencies. Detects common SQL mistakes in migrations.
"""
import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2}

# SQL reserved words (subset — most commonly misused as identifiers)
RESERVED = {
    "user", "order", "group", "select", "from", "where", "table", "index",
    "primary", "foreign", "key", "column", "row", "count", "sum", "avg",
    "min", "max", "date", "time", "timestamp", "year", "month", "day",
    "natural", "join", "outer", "inner", "left", "right", "cross", "using",
    "default", "unique", "check", "references", "cascade", "restrict",
    "limit", "offset", "union", "intersect", "except", "all", "any", "some",
    "value", "values", "level", "type", "status", "name",
}

KEYWORDS = {
    "select", "from", "where", "insert", "update", "delete", "create", "drop",
    "alter", "table", "index", "view", "column", "constraint", "primary",
    "foreign", "key", "references", "unique", "not", "null", "default",
    "check", "cascade", "restrict", "join", "inner", "outer", "left", "right",
    "on", "group", "by", "order", "having", "limit", "offset", "with", "as",
    "and", "or", "in", "between", "like", "is", "exists", "case", "when",
    "then", "else", "end", "begin", "commit", "rollback", "transaction",
    "truncate", "concurrently", "if",
}


@dataclass
class Finding:
    file: str
    line: int
    rule: str
    severity: str
    message: str

    def to_dict(self):
        return asdict(self)


def strip_comments_and_strings(sql: str) -> str:
    """Remove -- line comments, /* block comments */, and string literals.

    Returns SQL with comments/strings replaced by spaces (preserving line numbers).
    """
    out = []
    i = 0
    n = len(sql)
    while i < n:
        c = sql[i]
        # Line comment
        if c == "-" and i + 1 < n and sql[i + 1] == "-":
            while i < n and sql[i] != "\n":
                out.append(" ")
                i += 1
            continue
        # Block comment
        if c == "/" and i + 1 < n and sql[i + 1] == "*":
            while i + 1 < n and not (sql[i] == "*" and sql[i + 1] == "/"):
                out.append("\n" if sql[i] == "\n" else " ")
                i += 1
            out.append(" ")
            out.append(" ")
            i += 2
            continue
        # String literal
        if c in ("'", '"'):
            quote = c
            out.append(" ")
            i += 1
            while i < n:
                if sql[i] == quote:
                    # Handle doubled quote escape
                    if i + 1 < n and sql[i + 1] == quote:
                        out.append("  ")
                        i += 2
                        continue
                    out.append(" ")
                    i += 1
                    break
                out.append("\n" if sql[i] == "\n" else " ")
                i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def split_statements(stripped: str):
    """Yield (statement_text, start_line) tuples, split by top-level semicolons."""
    buf = []
    start_line = 1
    cur_line = 1
    first_nonspace = False
    for ch in stripped:
        if ch == "\n":
            cur_line += 1
        if ch == ";":
            stmt = "".join(buf)
            if stmt.strip():
                yield stmt, start_line
            buf = []
            start_line = cur_line
            first_nonspace = False
            continue
        if not first_nonspace and not ch.isspace():
            start_line = cur_line
            first_nonspace = True
        buf.append(ch)
    stmt = "".join(buf)
    if stmt.strip():
        yield stmt, start_line


def words(stmt: str):
    return re.findall(r"[A-Za-z_][A-Za-z0-9_]*", stmt)


def first_word(stmt: str):
    m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)", stmt)
    return m.group(1).lower() if m else ""


def first_n_words(stmt: str, n: int):
    return [w.lower() for w in words(stmt)[:n]]


def find_line_of(text: str, offset: int, base_line: int = 1) -> int:
    return base_line + text.count("\n", 0, offset)


def lint_file(path: str, dialect: str = "generic") -> list[Finding]:
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except Exception as e:
        return [Finding(path, 1, "file-read", "error", f"cannot read: {e}")]

    findings: list[Finding] = []
    stripped = strip_comments_and_strings(raw)

    # Rule 1: missing trailing semicolon
    if stripped.strip() and not stripped.rstrip().endswith(";"):
        last_line = raw.rstrip().count("\n") + 1
        findings.append(Finding(
            path, last_line, "missing-trailing-semicolon", "error",
            "file does not end with a semicolon",
        ))

    # Rule 2: tab/space mixing on the same line
    for ln_no, line in enumerate(raw.splitlines(), start=1):
        indent = line[: len(line) - len(line.lstrip())]
        if "\t" in indent and " " in indent:
            findings.append(Finding(
                path, ln_no, "mixed-indentation", "warning",
                "mixed tabs and spaces in indentation",
            ))
            break

    # Rule 3: trailing whitespace
    for ln_no, line in enumerate(raw.splitlines(), start=1):
        if line != line.rstrip() and line.strip():
            findings.append(Finding(
                path, ln_no, "trailing-whitespace", "info",
                "trailing whitespace",
            ))

    # Transaction tracking
    has_begin = False
    has_commit = False
    ddl_count = 0

    for stmt, line in split_statements(stripped):
        fw = first_word(stmt)
        fw2 = first_n_words(stmt, 2)
        fw3 = first_n_words(stmt, 3)
        upper = stmt.upper()

        if fw in ("begin", "start"):
            has_begin = True
            continue
        if fw == "commit":
            has_commit = True
            continue
        if fw == "rollback":
            continue

        # Rule 4: keyword case consistency — check if keywords are mixed case
        _check_keyword_case(path, stmt, line, findings)

        # Rule 5: DROP without IF EXISTS
        if fw == "drop":
            if "if exists" not in stmt.lower() and len(fw2) >= 2 and fw2[1] in (
                "table", "index", "view", "sequence", "schema", "function",
                "trigger", "constraint", "column", "database",
            ):
                findings.append(Finding(
                    path, line, "drop-without-if-exists", "warning",
                    f"DROP {fw2[1].upper()} without IF EXISTS — migration will fail if already dropped",
                ))
            ddl_count += 1
            # Rule 5b: DROP TABLE is destructive
            if len(fw2) >= 2 and fw2[1] == "table":
                findings.append(Finding(
                    path, line, "destructive-drop-table", "warning",
                    "DROP TABLE is destructive — ensure backup exists",
                ))

        # Rule 6: CREATE without IF NOT EXISTS (DDL only)
        if fw == "create":
            is_idempotent = "if not exists" in stmt.lower()
            # skip CREATE OR REPLACE (views/functions)
            if not is_idempotent and "or replace" not in stmt.lower():
                obj = None
                for idx, w in enumerate(fw3):
                    if w in ("table", "index", "view", "sequence", "schema",
                             "trigger", "function"):
                        obj = w
                        break
                if obj and obj != "function" and obj != "view":
                    findings.append(Finding(
                        path, line, "create-without-if-not-exists", "warning",
                        f"CREATE {obj.upper()} without IF NOT EXISTS — migration fails on re-run",
                    ))
            ddl_count += 1

            # Rule 6b (Postgres): CREATE INDEX without CONCURRENTLY
            if dialect == "postgres" and len(fw3) >= 2 and fw3[1] == "index" \
                    and "concurrently" not in stmt.lower():
                findings.append(Finding(
                    path, line, "create-index-locks-table", "warning",
                    "CREATE INDEX without CONCURRENTLY locks the table (Postgres)",
                ))

        # Rule 7: ALTER tracked for DDL count
        if fw == "alter":
            ddl_count += 1
            # Rule 7b (Postgres): ADD COLUMN NOT NULL without DEFAULT
            if dialect == "postgres" and "add column" in stmt.lower() \
                    and re.search(r"\bnot\s+null\b", stmt, re.I) \
                    and not re.search(r"\bdefault\b", stmt, re.I):
                findings.append(Finding(
                    path, line, "add-column-not-null-no-default", "error",
                    "ADD COLUMN NOT NULL without DEFAULT fails on non-empty tables",
                ))

        # Rule 8: UPDATE without WHERE
        if fw == "update":
            if not re.search(r"\bwhere\b", stmt, re.I):
                findings.append(Finding(
                    path, line, "update-without-where", "error",
                    "UPDATE without WHERE clause affects every row",
                ))

        # Rule 9: DELETE without WHERE
        if fw == "delete":
            if not re.search(r"\bwhere\b", stmt, re.I):
                findings.append(Finding(
                    path, line, "delete-without-where", "error",
                    "DELETE without WHERE clause removes every row",
                ))

        # Rule 10: TRUNCATE warning
        if fw == "truncate":
            findings.append(Finding(
                path, line, "truncate-is-destructive", "warning",
                "TRUNCATE removes all rows and cannot be rolled back in some engines",
            ))

        # Rule 11: SELECT * in migrations
        if fw == "select" and re.search(r"select\s+\*", stmt, re.I):
            findings.append(Finding(
                path, line, "select-star", "info",
                "SELECT * in migrations is brittle to schema changes",
            ))

        # Rule 12: INSERT without ON CONFLICT (in migrations)
        if fw == "insert" and "on conflict" not in stmt.lower() \
                and "on duplicate key" not in stmt.lower():
            findings.append(Finding(
                path, line, "insert-without-conflict-handling", "info",
                "INSERT without ON CONFLICT fails on re-run if row exists",
            ))

        # Rule 13: reserved word as identifier
        _check_reserved_identifier(path, stmt, line, findings)

    # Rule 14: DDL count > 1 but no transaction
    if ddl_count >= 2 and not (has_begin and has_commit):
        findings.append(Finding(
            path, 1, "missing-transaction", "warning",
            f"{ddl_count} DDL statements without explicit BEGIN/COMMIT — all-or-nothing not guaranteed",
        ))

    # Rule 15: BEGIN without COMMIT
    if has_begin and not has_commit:
        findings.append(Finding(
            path, 1, "begin-without-commit", "error",
            "BEGIN without matching COMMIT",
        ))

    return findings


def _check_keyword_case(path: str, stmt: str, base_line: int, findings: list):
    """Detect mixed case keywords (e.g. Select vs SELECT vs select)."""
    # Collect instances of each keyword
    seen_case = {}
    for m in re.finditer(r"\b([A-Za-z_]+)\b", stmt):
        w = m.group(1)
        lw = w.lower()
        if lw not in KEYWORDS:
            continue
        # Only flag if we see BOTH "all upper" AND "all lower" or "mixed"
        case_type = (
            "upper" if w.isupper() else
            "lower" if w.islower() else
            "mixed"
        )
        seen_case.setdefault(lw, set()).add(case_type)
    # Emit at most one finding per statement
    for lw, cases in seen_case.items():
        if len(cases) > 1 or "mixed" in cases:
            findings.append(Finding(
                path, base_line, "keyword-case-inconsistent", "info",
                f"keyword '{lw}' appears in inconsistent case",
            ))
            return


def _check_reserved_identifier(path: str, stmt: str, base_line: int, findings: list):
    """Flag unquoted identifiers that are reserved words in common contexts.

    Contexts: CREATE TABLE <name>, CREATE INDEX ON <name>, INSERT INTO <name>,
    REFERENCES <name>, column definitions.
    """
    text = stmt
    # CREATE TABLE foo
    for m in re.finditer(r"\bcreate\s+table\s+(?:if\s+not\s+exists\s+)?([A-Za-z_][A-Za-z0-9_]*)", text, re.I):
        name = m.group(1)
        if name.lower() in RESERVED:
            findings.append(Finding(
                path, base_line + text.count("\n", 0, m.start()),
                "reserved-word-identifier", "warning",
                f"table name '{name}' is a reserved word in SQL",
            ))
    # INSERT INTO foo
    for m in re.finditer(r"\binsert\s+into\s+([A-Za-z_][A-Za-z0-9_]*)", text, re.I):
        name = m.group(1)
        if name.lower() in RESERVED:
            findings.append(Finding(
                path, base_line + text.count("\n", 0, m.start()),
                "reserved-word-identifier", "warning",
                f"table name '{name}' is a reserved word in SQL",
            ))


def collect_files(inputs: list[str]) -> list[str]:
    out = []
    for inp in inputs:
        p = Path(inp)
        if p.is_dir():
            out.extend(str(f) for f in p.rglob("*.sql"))
        elif p.is_file():
            out.append(str(p))
        else:
            print(f"warning: {inp} not found", file=sys.stderr)
    return sorted(out)


def format_text(findings: list[Finding]) -> str:
    if not findings:
        return "✓ no issues found"
    by_file = {}
    for f in findings:
        by_file.setdefault(f.file, []).append(f)
    lines = []
    for file, items in by_file.items():
        lines.append(f"\n{file}:")
        for f in sorted(items, key=lambda x: (x.line, x.rule)):
            sev = {"error": "E", "warning": "W", "info": "I"}.get(f.severity, "?")
            lines.append(f"  {f.line:4d}:{sev}: [{f.rule}] {f.message}")
    counts = {"error": 0, "warning": 0, "info": 0}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    lines.append(f"\n{counts['error']} errors, {counts['warning']} warnings, {counts['info']} info")
    return "\n".join(lines)


def format_json(findings: list[Finding]) -> str:
    return json.dumps([f.to_dict() for f in findings], indent=2)


def format_summary(findings: list[Finding]) -> str:
    counts = {"error": 0, "warning": 0, "info": 0}
    rule_counts = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
        rule_counts[f.rule] = rule_counts.get(f.rule, 0) + 1
    out = [f"errors={counts['error']} warnings={counts['warning']} info={counts['info']}"]
    out.append("\ntop rules:")
    for rule, n in sorted(rule_counts.items(), key=lambda x: -x[1])[:10]:
        out.append(f"  {n:4d}  {rule}")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Lint SQL migration files.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    lint = sub.add_parser("lint", help="Run all rules")
    lint.add_argument("paths", nargs="+", help="SQL file(s) or directory")
    lint.add_argument("--dialect", choices=["generic", "postgres", "mysql", "sqlite"],
                      default="generic")
    lint.add_argument("--format", choices=["text", "json", "summary"], default="text")
    lint.add_argument("--min-severity", choices=["info", "warning", "error"], default="info")

    rules = sub.add_parser("rules", help="List all rules")

    args = ap.parse_args(argv)

    if args.cmd == "rules":
        _print_rules()
        return 0

    files = collect_files(args.paths)
    if not files:
        print("no .sql files found", file=sys.stderr)
        return 2

    all_findings: list[Finding] = []
    for f in files:
        all_findings.extend(lint_file(f, dialect=args.dialect))

    min_sev = SEVERITY_ORDER[args.min_severity]
    filtered = [f for f in all_findings if SEVERITY_ORDER[f.severity] >= min_sev]

    if args.format == "text":
        print(format_text(filtered))
    elif args.format == "json":
        print(format_json(filtered))
    else:
        print(format_summary(filtered))

    # Exit code: 2 on error, 1 on warning, 0 otherwise
    if any(f.severity == "error" for f in filtered):
        return 2
    if any(f.severity == "warning" for f in filtered):
        return 1
    return 0


def _print_rules():
    rules = [
        ("missing-trailing-semicolon", "error", "File does not end with ;"),
        ("mixed-indentation", "warning", "Tabs and spaces mixed in indentation"),
        ("trailing-whitespace", "info", "Trailing whitespace"),
        ("drop-without-if-exists", "warning", "DROP without IF EXISTS"),
        ("destructive-drop-table", "warning", "DROP TABLE is destructive"),
        ("create-without-if-not-exists", "warning", "CREATE without IF NOT EXISTS"),
        ("create-index-locks-table", "warning", "CREATE INDEX without CONCURRENTLY (Postgres)"),
        ("add-column-not-null-no-default", "error", "ADD COLUMN NOT NULL without DEFAULT (Postgres)"),
        ("update-without-where", "error", "UPDATE without WHERE"),
        ("delete-without-where", "error", "DELETE without WHERE"),
        ("truncate-is-destructive", "warning", "TRUNCATE is destructive"),
        ("select-star", "info", "SELECT * in migrations"),
        ("insert-without-conflict-handling", "info", "INSERT without ON CONFLICT"),
        ("reserved-word-identifier", "warning", "Identifier is a SQL reserved word"),
        ("keyword-case-inconsistent", "info", "Mixed keyword case"),
        ("missing-transaction", "warning", "Multi-DDL migration without BEGIN/COMMIT"),
        ("begin-without-commit", "error", "BEGIN without COMMIT"),
    ]
    print(f"{'rule':42} {'severity':10} description")
    print("-" * 90)
    for name, sev, desc in rules:
        print(f"{name:42} {sev:10} {desc}")


if __name__ == "__main__":
    sys.exit(main())
