#!/usr/bin/env python3
"""
CLI wrapper for Constitutional Memory.

Usage:
    python cli.py context                                         # Print LLM context
    python cli.py scan --code strategy.py                         # Scan file for violations
    python cli.py add-lesson --strategy v1 --category drawdown \
        --description "High drawdown" --severity critical         # Add a lesson
    python cli.py add-ban --pattern "dangerous_function"          # Add a banned pattern
    python cli.py list-lessons                                    # List all lessons
    python cli.py list-bans                                       # List all bans
    python cli.py seed-examples                                   # Populate with example data
"""
import argparse
import json
import os
import sys

from memory_system import ConstitutionalMemory


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="constitutional-memory",
        description="Strategy Constitutional Memory — lesson & ban management CLI",
    )
    parser.add_argument(
        "--memory-dir",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "memory"),
        help="Path to the memory storage directory (default: ./memory)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # -- context ---------------------------------------------------------------
    ctx = sub.add_parser("context", help="Print the LLM context fragment")
    ctx.add_argument(
        "--max-lessons",
        type=int,
        default=30,
        help="Maximum number of lessons to include (default: 30)",
    )

    # -- scan ------------------------------------------------------------------
    scan = sub.add_parser("scan", help="Scan a source file for banned patterns")
    scan.add_argument(
        "--code",
        required=True,
        help="Path to the source file to scan",
    )

    # -- add-lesson ------------------------------------------------------------
    add = sub.add_parser("add-lesson", help="Add a lesson to the constitution")
    add.add_argument("--strategy", required=True, help="Strategy identifier")
    add.add_argument(
        "--category",
        required=True,
        help="Category (e.g. drawdown, selection, position_sizing, timing, ml_failure, success)",
    )
    add.add_argument("--description", required=True, help="Root-cause description")
    add.add_argument("--evidence", default="", help="Supporting data / evidence")
    add.add_argument(
        "--severity",
        default="high",
        choices=["critical", "high", "medium", "low"],
        help="Severity level (default: high)",
    )
    add.add_argument("--ban", default=None, help="Optional code pattern to ban")

    # -- add-ban ---------------------------------------------------------------
    ban_cmd = sub.add_parser("add-ban", help="Add a banned code pattern")
    ban_cmd.add_argument("--pattern", required=True, help="The code pattern to prohibit")

    # -- list-lessons ----------------------------------------------------------
    sub.add_parser("list-lessons", help="List all recorded lessons")

    # -- list-bans -------------------------------------------------------------
    sub.add_parser("list-bans", help="List all banned patterns")

    # -- seed-examples ---------------------------------------------------------
    sub.add_parser("seed-examples", help="Populate memory with generic example lessons")

    return parser


def main():
    parser = _build_parser()
    args = parser.parse_args()

    memory = ConstitutionalMemory(memory_dir=args.memory_dir)

    if args.command == "context":
        print(memory.get_context(max_lessons=args.max_lessons))

    elif args.command == "scan":
        code_path = args.code
        if not os.path.isfile(code_path):
            print(f"Error: file not found — {code_path}", file=sys.stderr)
            sys.exit(1)
        with open(code_path, encoding="utf-8") as f:
            code = f.read()
        violations = memory.scan_code(code)
        if violations:
            print(f"Found {len(violations)} violation(s):\n")
            for v in violations:
                print(f"  Line {v['line']}: banned pattern `{v['pattern']}`")
                print(f"    {v['content']}\n")
            sys.exit(1)
        else:
            print("No violations found.")

    elif args.command == "add-lesson":
        memory.add_lesson(
            strategy_name=args.strategy,
            category=args.category,
            description=args.description,
            evidence=args.evidence,
            severity=args.severity,
            new_ban=args.ban,
        )
        print(f"Lesson added (strategy={args.strategy}, severity={args.severity}).")
        if args.ban:
            print(f"Banned pattern added: `{args.ban}`")

    elif args.command == "add-ban":
        memory.add_ban(args.pattern)
        print(f"Banned pattern added: `{args.pattern}`")

    elif args.command == "list-lessons":
        if not memory.lessons:
            print("No lessons recorded yet.")
        else:
            print(f"{len(memory.lessons)} lesson(s):\n")
            for lesson in memory.lessons:
                sev = lesson.get("severity", "?").upper()
                print(
                    f"  #{lesson['id']} [{sev}] [{lesson['strategy']}] "
                    f"{lesson['category']}: {lesson['description']}"
                )
                if lesson.get("evidence"):
                    print(f"    Evidence: {lesson['evidence']}")
                print()

    elif args.command == "list-bans":
        if not memory.bans:
            print("No banned patterns configured.")
        else:
            print(f"{len(memory.bans)} banned pattern(s):\n")
            for ban in memory.bans:
                print(f"  X `{ban}`")

    elif args.command == "seed-examples":
        before = len(memory.lessons)
        memory.seed_from_examples()
        after = len(memory.lessons)
        if after > before:
            print(f"Seeded {after - before} example lesson(s).")
        else:
            print("Memory already contains lessons — examples not added.")


if __name__ == "__main__":
    main()
