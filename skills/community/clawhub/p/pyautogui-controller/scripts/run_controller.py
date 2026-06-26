#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(r"C:\Users\dev\Desktop\昱昱\skills\pyautogui-controller")
ENTRY = PROJECT_DIR / "main.py"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python run_controller.py \"<command>\"")
        return 1
    cmd = [sys.executable, str(ENTRY), sys.argv[1]]
    completed = subprocess.run(cmd, cwd=str(PROJECT_DIR))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
