#!/usr/bin/env python3
"""
Sync all memory sources and mine patterns.
"""

import subprocess
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent

def run_script(name):
    result = subprocess.run(
        ["python3", name],
        cwd=SKILL_DIR / "scripts",
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)

if __name__ == "__main__":
    print("=== Syncing Claude Code ===")
    run_script("sync-claude-code.py")

    print("\n=== Syncing Self-Improving ===")
    run_script("sync-self-improving.py")

    print("\n=== Mining Patterns ===")
    run_script("pattern-miner.py")

    print("\n=== All sync complete ===")
