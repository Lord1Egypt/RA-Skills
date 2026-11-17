"""C · script_c.py

Launches `config_a.py` as a subprocess (literal-list style recognized by MGC
ext08) and writes a summary to `~/Desktop/txt2.txt`.

Demonstrates one ext08-recognized pattern:
  - `subprocess.run([sys.executable, "config_a.py", ...])`  (subprocess, literal list)
"""

import argparse
import subprocess
import sys
from pathlib import Path


def _resolve_desktop() -> Path:
    """Return the Desktop path on macOS / Windows, or fall back to home on Linux."""
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        desktop = Path.home()
    return desktop


def run(user: str = "MirginCipher Demo User",
        greeting: str = "Hello, written by script_c.py via subprocess") -> int:
    """Spawn config_a.py as a subprocess and write a summary to txt2.txt."""
    here = Path(__file__).resolve().parent
    target = here / "config_a.py"

    # ── subprocess: literal list form (MGC ext08 recognizes this) ──
    proc = subprocess.run(
        [sys.executable, str(target), "--user", user, "--greeting", greeting, "--print"],
        capture_output=True, text=True,
    )

    out = _resolve_desktop() / "txt2.txt"
    lines = [
        "[script_c] call mode: subprocess (literal list)",
        "[script_c] caller:    script_c.py",
        "[script_c] callee:    config_a.py",
        f"[script_c] passed --user:     {user}",
        f"[script_c] passed --greeting: {greeting}",
        f"[script_c] stdout: {(proc.stdout or '').strip() or '(no stdout)'}",
    ]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[script_c] wrote: {out}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="script_c — write txt2.txt")
    # Literal defaults so MGC's argparse extractor fills ext02 cleanly
    parser.add_argument("--user", default="MirginCipher Demo User")
    parser.add_argument("--greeting", default="Hello, written by script_c.py via subprocess")
    args = parser.parse_args()
    return run(args.user, args.greeting)


if __name__ == "__main__":
    sys.exit(main())