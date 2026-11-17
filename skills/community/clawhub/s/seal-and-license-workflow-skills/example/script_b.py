"""B · script_b.py

Reads values from `config_a` via two import styles and writes a greeting to
`~/Desktop/txt1.txt`.

Demonstrates two ext08-recognized patterns:
  - `import config_a`                         (plain import)
  - `from config_a import get_greeting, DEFAULT_USER`  (from-import)
"""

import argparse
import sys
from pathlib import Path

# --- Same-package import: MGC ext08 auto-recognition ---
import config_a                                  # pattern: import
from config_a import get_greeting, DEFAULT_USER  # pattern: from-import


def _resolve_desktop() -> Path:
    """Return the Desktop path on macOS / Windows, or fall back to home on Linux."""
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        desktop = Path.home()
    return desktop


def run(user: str = "MirginCipher Demo User",
        greeting: str = "Hello, written by script_b.py via import") -> int:
    """Write a two-line txt1.txt using values imported from config_a."""
    out = _resolve_desktop() / "txt1.txt"
    lines = [
        f"[script_b] {get_greeting(user, greeting)}",
        f"[script_b] DEFAULT_USER (via from-import) = {DEFAULT_USER}",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[script_b] wrote: {out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="script_b — write txt1.txt")
    # Literal defaults so MGC's argparse extractor fills ext02 cleanly
    parser.add_argument("--user", default="MirginCipher Demo User")
    parser.add_argument("--greeting", default="Hello, written by script_b.py via import")
    args = parser.parse_args()
    return run(args.user, args.greeting)


if __name__ == "__main__":
    sys.exit(main())