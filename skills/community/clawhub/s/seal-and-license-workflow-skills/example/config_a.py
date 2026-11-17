"""A · config_a.py

A shared config script. Provides a `DEFAULT_USER` constant, a `get_greeting()`
function, and an argparse entry point so it can be invoked standalone (used by
`script_c` via subprocess). It is also importable as a plain module (used by
`script_b` via `import` and `from-import`).

Demonstrates: it can be either a Python module (import / from-import) or an
executable script (subprocess invocation) — MGC's ext08 recognizes both.
"""

import argparse
import sys
from pathlib import Path


DEFAULT_USER = "MirginCipher Demo User"


def get_greeting(user: str, greeting: str) -> str:
    """Format a single greeting line: '<greeting> (target: <user>)'."""
    return f"{greeting} (target: {user})"


def _resolve_desktop() -> Path:
    """Return the Desktop path on macOS / Windows, or fall back to home on Linux."""
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        desktop = Path.home()
    return desktop


def main() -> int:
    parser = argparse.ArgumentParser(
        description="config_a — write greeting to txt2_via_a.txt (shared by B and C)"
    )
    parser.add_argument(
        "--user", default="MirginCipher Demo User",
        help="target user name (default for argparse auto-extraction / ext02)"
    )
    parser.add_argument(
        "--greeting", default="Hello, written by config_a.py",
        help="greeting text (default for argparse auto-extraction / ext02)"
    )
    parser.add_argument(
        "--print", action="store_true",
        help="also print the greeting to stdout"
    )
    args = parser.parse_args()

    line = get_greeting(args.user, args.greeting)
    out = _resolve_desktop() / "txt2_via_a.txt"
    out.write_text(line + "\n", encoding="utf-8")

    if args.print:
        print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())