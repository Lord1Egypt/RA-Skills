"""D · script_d.py

Driver / orchestrator. Drives both B (via `import`) and C (via subprocess) in
one run, then writes a combined summary to `~/Desktop/combined.txt`.

Demonstrates two more ext08-recognized edges:
  - D → B: `import script_b; script_b.run(...)`               (import)
  - D → C: `subprocess.run([sys.executable, "script_c.py"])`  (subprocess, literal list)
"""

import argparse
import subprocess
import sys
from pathlib import Path

# --- D → B: import (MGC ext08 auto-recognizes) ---
import script_b  # pattern: import


def _resolve_desktop() -> Path:
    """Return the Desktop path on macOS / Windows, or fall back to home on Linux."""
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        desktop = Path.home()
    return desktop


def run(user: str = "MirginCipher Demo User",
        greeting: str = "Hello, written by script_d.py orchestrating B and C") -> int:
    """Run B and C, then write the combined summary."""
    here = Path(__file__).resolve().parent

    # 1. B (import) — runs in-process; ext08 routes via sealed execution
    script_b.run(user=user, greeting=greeting)
    txt1 = _resolve_desktop() / "txt1.txt"

    # 2. C (subprocess) — runs in a sealed subprocess
    c_target = here / "script_c.py"
    proc = subprocess.run(
        [sys.executable, str(c_target), "--user", user, "--greeting", greeting],
        capture_output=True, text=True,
    )
    txt2 = _resolve_desktop() / "txt2.txt"
    txt2_via_a = _resolve_desktop() / "txt2_via_a.txt"

    # 3. Summary
    combined = _resolve_desktop() / "combined.txt"
    lines = [
        "[script_d] ===== Combined summary =====",
        "[script_d] caller:    script_d.py",
        f"[script_d] B (import)         wrote: {txt1}",
        f"[script_d] C (subprocess)     stdout: {(proc.stdout or '').strip() or '(no stdout)'}",
        f"[script_d] txt2.txt and txt2_via_a.txt written to Desktop by C and A",
    ]
    combined.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[script_d] wrote: {combined}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="script_d — driver / orchestrator")
    # Literal defaults so MGC's argparse extractor fills ext02 cleanly
    parser.add_argument("--user", default="MirginCipher Demo User")
    parser.add_argument("--greeting", default="Hello, written by script_d.py orchestrating B and C")
    args = parser.parse_args()
    return run(args.user, args.greeting)


if __name__ == "__main__":
    sys.exit(main())