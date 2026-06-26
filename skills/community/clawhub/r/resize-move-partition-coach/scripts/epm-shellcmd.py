#!/usr/bin/env python3
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def usage(name: str) -> int:
    print("Usage:")
    print(f'  {name} "Resize Partition" C:\\')
    print(f'  {name} "Split Partition" D:\\')
    print()
    print("Notes:")
    print("  - The first argument is mapped to shellcmd.")
    print("  - Remaining arguments are written into a temp file and passed as shellparam.")
    return 0


def usage_error(name: str) -> int:
    print("[ERROR] Missing shell parameters.")
    print()
    return usage(name) or 1


def main() -> int:
    argv = sys.argv[1:]
    script_name = Path(sys.argv[0]).name
    if not argv or argv[0] in ("-h", "--help"):
        return usage(script_name)

    shellcmd = argv[0]
    shellparam_values = argv[1:]
    if not shellparam_values:
        return usage_error(script_name)

    shellparam_content = " ".join(shellparam_values)
    fd, tmp_name = tempfile.mkstemp(prefix="epm-shellparam-", suffix=".tmp")
    os.close(fd)
    tmp_file = Path(tmp_name)
    tmp_file.write_text(shellparam_content, encoding="utf-8", newline="")

    epmui_path = Path(r"C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe")

    print(f"[INFO] shellcmd={shellcmd}")
    print(f"[INFO] shellparam file={tmp_file}")
    print(f"[INFO] shellparam raw={shellparam_content}")

    if not epmui_path.exists():
        print("[ERROR] EPMUI.exe not found.")
        print("Expected at:")
        print(r"  C:\Program Files\EaseUS\EaseUS Partition Master\bin\EPMUI.exe")
        return 2

    proc = subprocess.Popen(
        [
            str(epmui_path),
            "startByEpm0",
            f"shellcmd={shellcmd}",
            f"shellparam={tmp_file}",
        ]
    )
    if proc.pid <= 0:
        print("[ERROR] Failed to launch EPMUI.exe.")
        return 1

    print("[OK] Launch request sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
