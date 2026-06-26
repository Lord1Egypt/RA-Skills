#!/usr/bin/env python3
"""SQL Formatter — format, lint, and minify SQL queries.

No external dependencies required. Uses standard library only.

Usage:
  python3 sql_format.py format --input query.sql [--output formatted.sql] [--indent 2] [--uppercase]
  python3 sql_format.py format --sql "SELECT * FROM users WHERE id = 1"
  python3 sql_format.py minify --input query.sql
  python3 sql_format.py lint --input query.sql
  echo "SELECT * FROM t" | python3 sql_format.py format --input -
"""

import argparse
import re
import sys
import json


# SQL keywords for formatting
MAJOR_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN",
    "OUTER JOIN", "FULL JOIN", "FULL OUTER JOIN", "LEFT OUTER JOIN",
    "RIGHT OUTER JOIN", "CROSS JOIN", "NATURAL JOIN",
    "ON", "AND", "OR", "ORDER BY", "GROUP BY", "HAVING", "LIMIT", "OFFSET",
    "UNION", "UNION ALL", "INTERSECT", "EXCEPT", "INSERT INTO", "VALUES",
    "UPDATE", "SET", "DELETE FROM", "CREATE TABLE", "ALTER TABLE",
    "DROP TABLE", "CREATE INDEX", "DROP INDEX", "WITH", "AS", "CASE",
    "WHEN", "THEN", "ELSE", "END", "RETURNING", "INTO", "DISTINCT",
    "EXISTS", "NOT EXISTS", "IN", "NOT IN", "BETWEEN", "LIKE", "IS NULL",
    "IS NOT NULL", "ASC", "DESC", "CASCADE", "RESTRICT", "IF EXISTS",
    "IF NOT EXISTS",
]

NEWLINE_BEFORE = {
    "SELECT", "FROM", "WHERE", "JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN",
    "OUTER JOIN", "FULL JOIN", "FULL OUTER JOIN", "LEFT OUTER JOIN",
    "RIGHT OUTER JOIN", "CROSS JOIN", "NATURAL JOIN",
    "ORDER BY", "GROUP BY", "HAVING", "LIMIT", "OFFSET",
    "UNION", "UNION ALL", "INTERSECT", "EXCEPT",
    "INSERT INTO", "UPDATE", "SET", "DELETE FROM",
    "CREATE TABLE", "ALTER TABLE", "DROP TABLE",
    "WITH", "RETURNING", "VALUES",
}

INDENT_AFTER = {
    "SELECT", "SET", "VALUES", "WITH",
}

INDENT_ON = {
    "AND", "OR", "ON",
}

LINT_RULES = [
    ("SELECT *", "Avoid SELECT * — specify columns explicitly for clarity and performance."),
    ("SELECT  ", "Multiple spaces detected — use single spaces."),
    ("\t", "Tab characters found — prefer spaces for consistent formatting."),
    ("!= ", "Use <> instead of != for SQL standard compliance (optional)."),
    (",,", "Double comma detected — likely a typo."),
    ("WHERE 1=1", "WHERE 1=1 detected — likely leftover debug clause."),
    ("WHERE 1 = 1", "WHERE 1 = 1 detected — likely leftover debug clause."),
]


def tokenize_sql(sql):
    """Tokenize SQL into words, strings, comments, and symbols."""
    tokens = []
    i = 0
    length = len(sql)

    while i < length:
        # Skip whitespace (but track it)
        if sql[i] in (" ", "\t", "\n", "\r"):
            i += 1
            continue

        # Single-line comment
        if sql[i:i+2] == "--":
            end = sql.find("\n", i)
            if end == -1:
                end = length
            tokens.append(("COMMENT", sql[i:end]))
            i = end
            continue

        # Multi-line comment
        if sql[i:i+2] == "/*":
            end = sql.find("*/", i + 2)
            if end == -1:
                end = length
            else:
                end += 2
            tokens.append(("COMMENT", sql[i:end]))
            i = end
            continue

        # String literal (single quotes)
        if sql[i] == "'":
            j = i + 1
            while j < length:
                if sql[j] == "'" and (j + 1 >= length or sql[j + 1] != "'"):
                    j += 1
                    break
                if sql[j] == "'" and j + 1 < length and sql[j + 1] == "'":
                    j += 2
                    continue
                j += 1
            tokens.append(("STRING", sql[i:j]))
            i = j
            continue

        # Double-quoted identifier
        if sql[i] == '"':
            j = i + 1
            while j < length and sql[j] != '"':
                j += 1
            j += 1  # include closing quote
            tokens.append(("IDENT", sql[i:j]))
            i = j
            continue

        # Parentheses
        if sql[i] == "(":
            tokens.append(("LPAREN", "("))
            i += 1
            continue
        if sql[i] == ")":
            tokens.append(("RPAREN", ")"))
            i += 1
            continue

        # Semicolon
        if sql[i] == ";":
            tokens.append(("SEMI", ";"))
            i += 1
            continue

        # Comma
        if sql[i] == ",":
            tokens.append(("COMMA", ","))
            i += 1
            continue

        # Operators
        if sql[i:i+2] in ("<=", ">=", "<>", "!=", "||", "::"):
            tokens.append(("OP", sql[i:i+2]))
            i += 2
            continue
        if sql[i] in ("<", ">", "=", "+", "-", "*", "/", "%", ".", "~"):
            tokens.append(("OP", sql[i]))
            i += 1
            continue

        # Words (keywords, identifiers, numbers)
        if sql[i].isalnum() or sql[i] == "_" or sql[i] == "@":
            j = i
            while j < length and (sql[j].isalnum() or sql[j] in ("_", ".", "@", "$")):
                j += 1
            tokens.append(("WORD", sql[i:j]))
            i = j
            continue

        # Anything else
        tokens.append(("OTHER", sql[i]))
        i += 1

    return tokens


def format_sql(sql, indent_size=2, uppercase_keywords=True):
    """Format SQL query with proper indentation and line breaks."""
    tokens = tokenize_sql(sql)
    lines = []
    current_line = []
    indent_level = 0
    pad = " " * indent_size
    paren_depth = 0

    i = 0
    while i < len(tokens):
        ttype, tval = tokens[i]

        if ttype == "COMMENT":
            if current_line:
                lines.append(pad * indent_level + " ".join(current_line))
                current_line = []
            lines.append(pad * indent_level + tval)
            i += 1
            continue

        if ttype == "STRING" or ttype == "IDENT":
            current_line.append(tval)
            i += 1
            continue

        if ttype == "LPAREN":
            current_line.append("(")
            paren_depth += 1
            i += 1
            continue

        if ttype == "RPAREN":
            current_line.append(")")
            paren_depth -= 1
            if paren_depth < 0:
                paren_depth = 0
            i += 1
            continue

        if ttype == "SEMI":
            current_line.append(";")
            lines.append(pad * indent_level + " ".join(current_line))
            current_line = []
            lines.append("")
            indent_level = 0
            i += 1
            continue

        if ttype == "COMMA":
            current_line.append(",")
            i += 1
            continue

        if ttype == "WORD":
            upper_val = tval.upper()

            # Check for multi-word keywords
            compound = None
            if i + 1 < len(tokens) and tokens[i + 1][0] == "WORD":
                two_word = upper_val + " " + tokens[i + 1][1].upper()
                if two_word in NEWLINE_BEFORE or two_word in INDENT_AFTER:
                    compound = two_word
                    # Check three-word
                    if i + 2 < len(tokens) and tokens[i + 2][0] == "WORD":
                        three_word = two_word + " " + tokens[i + 2][1].upper()
                        if three_word in NEWLINE_BEFORE:
                            compound = three_word

            if compound:
                word_count = len(compound.split())
                kw = compound if uppercase_keywords else compound.lower()

                if compound in NEWLINE_BEFORE and paren_depth == 0:
                    if current_line:
                        lines.append(pad * indent_level + " ".join(current_line))
                        current_line = []
                    # Decrease indent for major keywords
                    if compound in ("FROM", "WHERE", "ORDER BY", "GROUP BY", "HAVING",
                                    "LIMIT", "OFFSET", "SET", "VALUES", "RETURNING",
                                    "UNION", "UNION ALL", "INTERSECT", "EXCEPT"):
                        pass  # same level as SELECT
                    current_line.append(kw)
                else:
                    current_line.append(kw)

                i += word_count
                continue

            # Single keyword handling
            if upper_val in NEWLINE_BEFORE and paren_depth == 0:
                if current_line:
                    lines.append(pad * indent_level + " ".join(current_line))
                    current_line = []
                kw = upper_val if uppercase_keywords else upper_val.lower()
                current_line.append(kw)
            elif upper_val in INDENT_ON and paren_depth == 0:
                if current_line:
                    lines.append(pad * indent_level + " ".join(current_line))
                    current_line = []
                kw = upper_val if uppercase_keywords else upper_val.lower()
                current_line.append(pad + kw)
            elif uppercase_keywords and upper_val in [kw.split()[0] for kw in MAJOR_KEYWORDS]:
                current_line.append(upper_val)
            else:
                current_line.append(tval)

            i += 1
            continue

        # Default: operators, etc.
        current_line.append(tval)
        i += 1

    if current_line:
        lines.append(pad * indent_level + " ".join(current_line))

    # Clean up extra blank lines
    result = "\n".join(lines)
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip()


def minify_sql(sql):
    """Minify SQL by removing unnecessary whitespace and comments."""
    tokens = tokenize_sql(sql)
    parts = []
    for ttype, tval in tokens:
        if ttype == "COMMENT":
            continue
        parts.append(tval)
    # Join with single spaces, collapse multiple spaces
    result = " ".join(parts)
    result = re.sub(r"\s+", " ", result)
    # Remove spaces around certain operators
    result = re.sub(r"\s*([(),;])\s*", r"\1", result)
    result = re.sub(r"\(\s+", "(", result)
    result = re.sub(r"\s+\)", ")", result)
    return result.strip()


def lint_sql(sql):
    """Lint SQL for common issues."""
    issues = []
    lines = sql.split("\n")

    # Check global patterns
    upper_sql = sql.upper()
    for pattern, message in LINT_RULES:
        if pattern.upper() in upper_sql:
            issues.append({"severity": "warning", "message": message})

    # Line-specific checks
    for i, line in enumerate(lines, 1):
        stripped = line.rstrip()
        if len(stripped) > 120:
            issues.append({
                "severity": "warning",
                "line": i,
                "message": f"Line exceeds 120 characters ({len(stripped)} chars)."
            })
        if line != line.rstrip():
            issues.append({
                "severity": "info",
                "line": i,
                "message": "Trailing whitespace."
            })

    # Check for missing semicolons
    stripped_sql = sql.strip()
    if stripped_sql and not stripped_sql.endswith(";"):
        issues.append({
            "severity": "info",
            "message": "Query does not end with a semicolon."
        })

    # Check for inconsistent keyword casing
    tokens = tokenize_sql(sql)
    keyword_set = set()
    for kw in MAJOR_KEYWORDS:
        for part in kw.split():
            keyword_set.add(part)

    found_upper = False
    found_lower = False
    for ttype, tval in tokens:
        if ttype == "WORD" and tval.upper() in keyword_set:
            if tval == tval.upper():
                found_upper = True
            elif tval == tval.lower():
                found_lower = True
    if found_upper and found_lower:
        issues.append({
            "severity": "warning",
            "message": "Inconsistent keyword casing — mix of UPPER and lower case keywords detected."
        })

    return issues


def load_sql(path):
    """Load SQL from a file path or stdin (-)."""
    if path == "-":
        return sys.stdin.read()
    with open(path, "r") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(
        description="SQL Formatter — format, minify, and lint SQL queries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s format --input query.sql
  %(prog)s format --sql "SELECT id, name FROM users WHERE active = true"
  %(prog)s format --input query.sql --uppercase --indent 4
  %(prog)s minify --input query.sql
  %(prog)s lint --input query.sql
  %(prog)s lint --input query.sql --json
  echo "SELECT * FROM t" | %(prog)s format --input -
"""
    )
    sub = parser.add_subparsers(dest="command", help="Command to run")

    # format
    fmt_p = sub.add_parser("format", help="Format SQL with proper indentation")
    fmt_g = fmt_p.add_mutually_exclusive_group(required=True)
    fmt_g.add_argument("--input", help="Path to SQL file (or - for stdin)")
    fmt_g.add_argument("--sql", help="SQL string to format")
    fmt_p.add_argument("--output", help="Output file path (default: stdout)")
    fmt_p.add_argument("--indent", type=int, default=2, help="Indent size (default: 2)")
    fmt_p.add_argument("--uppercase", action="store_true", default=True,
                        help="Uppercase keywords (default: true)")
    fmt_p.add_argument("--lowercase", action="store_true",
                        help="Lowercase keywords")

    # minify
    min_p = sub.add_parser("minify", help="Minify SQL (remove whitespace/comments)")
    min_g = min_p.add_mutually_exclusive_group(required=True)
    min_g.add_argument("--input", help="Path to SQL file (or - for stdin)")
    min_g.add_argument("--sql", help="SQL string to minify")
    min_p.add_argument("--output", help="Output file path (default: stdout)")

    # lint
    lint_p = sub.add_parser("lint", help="Lint SQL for common issues")
    lint_g = lint_p.add_mutually_exclusive_group(required=True)
    lint_g.add_argument("--input", help="Path to SQL file (or - for stdin)")
    lint_g.add_argument("--sql", help="SQL string to lint")
    lint_p.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Load SQL
    sql = None
    if hasattr(args, "sql") and args.sql:
        sql = args.sql
    elif hasattr(args, "input") and args.input:
        try:
            sql = load_sql(args.input)
        except FileNotFoundError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    if not sql or not sql.strip():
        print("Error: no SQL input provided", file=sys.stderr)
        sys.exit(1)

    if args.command == "format":
        uc = not args.lowercase
        result = format_sql(sql, indent_size=args.indent, uppercase_keywords=uc)
        if args.output:
            with open(args.output, "w") as f:
                f.write(result + "\n")
            print(f"✅ Formatted SQL written to {args.output}")
        else:
            print(result)

    elif args.command == "minify":
        result = minify_sql(sql)
        if hasattr(args, "output") and args.output:
            with open(args.output, "w") as f:
                f.write(result + "\n")
            print(f"✅ Minified SQL written to {args.output}")
        else:
            print(result)

    elif args.command == "lint":
        issues = lint_sql(sql)
        if args.json:
            print(json.dumps({"issues": issues, "count": len(issues)}, indent=2))
        else:
            if not issues:
                print("✅ No issues found.")
            else:
                print(f"⚠️  Found {len(issues)} issue(s):")
                for issue in issues:
                    sev = issue.get("severity", "info").upper()
                    line = f" (line {issue['line']})" if "line" in issue else ""
                    print(f"  [{sev}]{line} {issue['message']}")


if __name__ == "__main__":
    main()
