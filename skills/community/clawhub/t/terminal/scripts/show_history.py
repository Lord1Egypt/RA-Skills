#!/usr/bin/env python3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_history

def main():
    history = load_history()
    runs = history.get("runs", [])

    if not runs:
        print("No command history yet.")
        return

    for run in runs[-15:]:
        print(f"{run['timestamp']} | status={run.get('status', 'executed')} | rc={run['returncode']} | risk={run['risk']}")
        print(f"  cwd: {run['cwd']}")
        print(f"  cmd: {run['command']}")
        print()

if __name__ == "__main__":
    main()
