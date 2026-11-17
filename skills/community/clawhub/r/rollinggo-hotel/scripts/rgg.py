#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import subprocess
from pathlib import Path

# 1. Prefer existing CLIENT_ID, fallback to overseas skill default Client ID
os.environ["CLIENT_ID"] = os.environ.get("CLIENT_ID", "rollinggoglobal")

is_win = sys.platform == "win32"
script_dir = Path(__file__).parent.resolve()
skill_bin_dir = script_dir.parent / "bin"

# 2. Cross-platform executable resolution (Windows / macOS / Linux)
def resolve_executable():
    if skill_bin_dir.exists():
        local_exe_name = "rgg.exe" if is_win else "rgg"
        local_path = skill_bin_dir / local_exe_name
        if local_path.exists():
            return str(local_path)

    if is_win:
        rgg_cmd = shutil.which("rgg.cmd")
        if rgg_cmd:
            return rgg_cmd
        rgg_exe = shutil.which("rgg.exe")
        if rgg_exe:
            return rgg_exe
        return "rgg"
    else:
        rgg_bin = shutil.which("rgg")
        if rgg_bin:
            return rgg_bin
        return "rgg"

target_cmd = resolve_executable()

def main():
    args = [target_cmd] + sys.argv[1:]
    try:
        use_shell = is_win and target_cmd.endswith(".cmd")
        res = subprocess.run(args, shell=use_shell)
        sys.exit(res.returncode)
    except KeyboardInterrupt:
        sys.exit(130)
    except FileNotFoundError:
        print(f"[rgg wrapper] Failed to find or execute rgg command (OS: {sys.platform})", file=sys.stderr)
        print("Please make sure @rollinggo/hotel-global is installed via 'npm install -g @rollinggo/hotel-global@latest' or 'python scripts/install.py'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[rgg wrapper] Exception occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
