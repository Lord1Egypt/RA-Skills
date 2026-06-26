#!/usr/bin/env python3
"""Append a directive, child output, or external message entry to an existing subagent context file.

Content sources (mutually exclusive, checked in order):
  1. --content "inline text"
  2. --content-file /path/to/file
  3. stdin (pipe or heredoc)
"""
import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


def now_iso() -> str:
    return datetime.now().astimezone().isoformat()


ROLE_LABELS = {
    "directive": "Directive",
    "child-output": "Child Output",
    "external-message": "External Message",
}


def detect_next_round(text: str, role: str) -> int:
    """Scan existing content for the highest round number of the given role, return next."""
    label = ROLE_LABELS[role]
    pattern = rf"^## {re.escape(label)} — Round (\d+)"
    rounds = [int(m.group(1)) for m in re.finditer(pattern, text, re.MULTILINE)]
    if rounds:
        return max(rounds) + 1
    # If no prior entry of this role exists, check the other role to stay in sync.
    other_label = "Child Output" if role == "directive" else "Directive"
    other_pattern = rf"^## {re.escape(other_label)} — Round (\d+)"
    other_rounds = [int(m.group(1)) for m in re.finditer(other_pattern, text, re.MULTILINE)]
    if other_rounds:
        max_other = max(other_rounds)
        # Directive for round N comes before child output for round N.
        # If appending a directive and the latest child output is round N, next directive is N+1.
        # If appending child output and the latest directive is round N, this child output is also N.
        if role == "directive":
            return max_other + 1
        else:
            return max_other
    return 1


def _find_rounds(text: str, label: str) -> set[int]:
    pattern = rf"^## {re.escape(label)} — Round (\d+)"
    return {int(m.group(1)) for m in re.finditer(pattern, text, re.MULTILINE)}


def detect_last_entry_role(text: str) -> str | None:
    """Return the role of the last entry in the context file, or None if empty."""
    pattern = r"^## (Directive|Child Output|External Message)(?:$| — )"
    matches = list(re.finditer(pattern, text, re.MULTILINE))
    if not matches:
        return None
    last_label = matches[-1].group(1)
    for role, label in ROLE_LABELS.items():
        if label == last_label:
            return role
    return None


def validate_sequence(text: str, role: str, round_num: int) -> None:
    """Enforce strict sequential ordering (Hard Rule 7).

    - Appending child-output for round N requires Directive round N to exist.
    - Appending directive for round N (N>1) requires Child Output round N-1 to exist.
    - Appending external-message requires the last entry to be child-output or external-message.
    """
    if role == "external-message":
        last_role = detect_last_entry_role(text)
        if last_role not in (None, "child-output", "external-message"):
            print(
                "Error: External Message can only appear after Background (before any directive), "
                "after Child Output, or after another External Message.",
                file=sys.stderr,
            )
            sys.exit(1)
    elif role == "child-output":
        directives = _find_rounds(text, "Directive")
        if round_num not in directives:
            print(
                f"Error: cannot append Child Output Round {round_num} — "
                f"Directive Round {round_num} not found. Strict sequential ordering violated.",
                file=sys.stderr,
            )
            sys.exit(1)
    elif role == "directive" and round_num > 1:
        child_outputs = _find_rounds(text, "Child Output")
        if (round_num - 1) not in child_outputs:
            print(
                f"Error: cannot append Directive Round {round_num} — "
                f"Child Output Round {round_num - 1} not found. Strict sequential ordering violated.",
                file=sys.stderr,
            )
            sys.exit(1)


def extract_last_entry_content(text: str, role: str) -> str | None:
    """Extract the body of the last entry matching the given role. Returns None if no entry found."""
    label = ROLE_LABELS[role]
    # Match section header and capture everything until the next --- separator or end of file
    if role == "external-message":
        pattern = rf"^## {re.escape(label)}\n\n(.*?)(?=\n---\n|\Z)"
    else:
        pattern = rf"^## {re.escape(label)} — Round \d+ — .+?\n\n(.*?)(?=\n---\n|\Z)"
    matches = list(re.finditer(pattern, text, re.MULTILINE | re.DOTALL))
    if not matches:
        return None
    return matches[-1].group(1).strip()


def main():
    ap = argparse.ArgumentParser(description="Append entry to subagent context file.")
    ap.add_argument("--context-file", required=True, help="Path to the context file")
    ap.add_argument("--role", required=True, choices=list(ROLE_LABELS.keys()),
                    help="Type of entry: 'directive', 'child-output', or 'external-message'")
    ap.add_argument("--content", default=None, help="Inline content string")
    ap.add_argument("--content-file", default=None, help="Path to file containing content")
    args = ap.parse_args()

    context_path = Path(args.context_file).expanduser().resolve()
    if not context_path.is_file():
        print(f"Error: context file not found: {context_path}", file=sys.stderr)
        sys.exit(1)

    # Resolve content
    if args.content is not None:
        body = args.content
    elif args.content_file is not None:
        content_file = Path(args.content_file).expanduser().resolve()
        if not content_file.is_file():
            print(f"Error: content file not found: {content_file}", file=sys.stderr)
            sys.exit(1)
        body = content_file.read_text(encoding="utf-8")
    elif not sys.stdin.isatty():
        body = sys.stdin.read()
    else:
        print("Error: no content provided. Use --content, --content-file, or pipe via stdin.",
              file=sys.stderr)
        sys.exit(1)

    existing = context_path.read_text(encoding="utf-8")

    # Dedup: if the latest entry of the same role has identical content, skip
    last_content = extract_last_entry_content(existing, args.role)
    if last_content is not None and last_content == body.strip():
        label = ROLE_LABELS[args.role]
        print(f"Duplicate: {label} content identical to latest existing entry. Skipped.")
        sys.exit(0)

    label = ROLE_LABELS[args.role]
    ts = now_iso()

    if args.role == "external-message":
        validate_sequence(existing, args.role, 0)
        last_role = detect_last_entry_role(existing)
        if last_role == "external-message":
            # Append to existing External Message section (no new header)
            entry = f"\n{body.strip()}\n"
        else:
            # Create new External Message section
            entry = f"\n---\n\n## {label}\n\n{body.strip()}\n"
        desc = label
    else:
        round_num = detect_next_round(existing, args.role)
        validate_sequence(existing, args.role, round_num)
        entry = f"\n---\n\n## {label} — Round {round_num} — {ts}\n\n{body.strip()}\n"
        desc = f"{label} Round {round_num}"

    with open(context_path, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"Appended {desc} to {context_path}")


if __name__ == "__main__":
    main()
