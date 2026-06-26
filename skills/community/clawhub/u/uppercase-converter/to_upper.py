#!/usr/bin/env python3
"""Convert English lowercase letters to uppercase.

Reads text from command-line arguments (joined with spaces) or, if none are
given, from standard input. Writes the uppercased text to standard output.

Only ASCII letters a-z are uppercased; everything else passes through unchanged.
"""

import sys


def to_upper(text: str) -> str:
    """Uppercase ASCII a-z, leaving all other characters untouched."""
    return "".join(
        chr(ord(ch) - 32) if "a" <= ch <= "z" else ch
        for ch in text
    )


def main() -> int:
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        sys.stdout.write(to_upper(text))
        sys.stdout.write("\n")
    else:
        # No args: stream stdin so large/multiline input works.
        data = sys.stdin.read()
        sys.stdout.write(to_upper(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
