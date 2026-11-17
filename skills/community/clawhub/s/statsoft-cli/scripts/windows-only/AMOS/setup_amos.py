#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""setup_amos.py — AMOS detection and configuration (Python, PowerShell-independent)
Usage:
  python setup_amos.py                  # Auto-detect
  python setup_amos.py <install_dir>    # Specify installation directory
"""
import os
import sys
import json


def find_amos_exe():
    """Locate amos.exe on the system dynamically"""
    roots = [
        r"C:\Program Files\IBM\SPSS\Amos",
        r"C:\Program Files (x86)\IBM\SPSS\Amos",
        r"C:\Program Files\IBM\SPSS Statistics\Amos",
        r"C:\Program Files (x86)\IBM\SPSS Statistics\Amos",
        r"D:\Program Files\IBM\SPSS\Amos",
        r"D:\Program Files (x86)\IBM\SPSS\Amos",
        r"C:\SPSS\Amos",
        r"D:\SPSS\Amos",
    ]
    # Also scan all drives
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        roots.extend([
            rf"{letter}:\Program Files\IBM\SPSS\Amos",
            rf"{letter}:\Program Files (x86)\IBM\SPSS\Amos",
            rf"{letter}:\SPSS\Amos",
            rf"{letter}:\IBM\SPSS\Amos",
        ])
    for root in roots:
        exe = os.path.join(root, "amos.exe")
        if os.path.isfile(exe):
            return root, exe
    return None, None


def get_file_version(exe_path):
    """Get version from exe file info"""
    try:
        import ctypes
        size = ctypes.windll.version.GetFileVersionInfoSizeW(exe_path, None)
        if size == 0:
            return "unknown"
        buffer = ctypes.create_string_buffer(size)
        ctypes.windll.version.GetFileVersionInfoW(exe_path, 0, size, buffer)
        lplpBuffer = ctypes.c_void_p()
        puLen = ctypes.c_uint()
        ctypes.windll.version.VerQueryValueW(buffer, "\\", ctypes.byref(lplpBuffer), ctypes.byref(puLen))
        if puLen.value == 0:
            return "unknown"
        class VS_FIXEDFILEINFO(ctypes.Structure):
            _fields_ = [
                ("dwSignature", ctypes.c_uint32),
                ("dwStrucVersion", ctypes.c_uint32),
                ("dwFileVersionMS", ctypes.c_uint32),
                ("dwFileVersionLS", ctypes.c_uint32),
                ("dwProductVersionMS", ctypes.c_uint32),
                ("dwProductVersionLS", ctypes.c_uint32),
                ("dwFileFlagsMask", ctypes.c_uint32),
                ("dwFileFlags", ctypes.c_uint32),
                ("dwFileOS", ctypes.c_uint32),
                ("dwFileType", ctypes.c_uint32),
                ("dwFileSubtype", ctypes.c_uint32),
                ("dwFileDateMS", ctypes.c_uint32),
                ("dwFileDateLS", ctypes.c_uint32),
            ]
        info = ctypes.cast(lplpBuffer, ctypes.POINTER(VS_FIXEDFILEINFO)).contents
        ms = info.dwFileVersionMS
        ls = info.dwFileVersionLS
        return f"{(ms >> 16) & 0xFFFF}.{ms & 0xFFFF}.{(ls >> 16) & 0xFFFF}.{ls & 0xFFFF}"
    except:
        return "unknown"


def main():
    print("[Python] === AMOS Detection ===\n")

    # Parse arguments: an optional positional <install_dir> plus explicit
    # persistence flags.
    #   --no-write -> detection-only, never persist config.json (default-safe).
    #   --consent  -> explicit opt-in; persist config.json via the gate.
    # When neither flag is given, fall back to the environment gate
    # (STATSOFT_AUTO_WRITE / STATSOFT_CONFIRM) — never self-grant authorization.
    manual_dir = None
    cli_consent = False
    cli_no_write = False
    for a in sys.argv[1:]:
        if a == "--consent":
            cli_consent = True
        elif a == "--no-write":
            cli_no_write = True
        elif a.startswith("--"):
            continue
        elif manual_dir is None:
            manual_dir = a

    # If command-line argument provided, use it directly
    if manual_dir is not None:
        exe = os.path.join(manual_dir, "amos.exe")
        if os.path.isfile(exe):
            root = manual_dir
            print(f"Using provided path: {root}")
        else:
            print(f"ERROR: amos.exe not found in {manual_dir}")
            sys.exit(1)
    else:
        root, exe = find_amos_exe()
        if not exe:
            print("AMOS not found in common locations.")
            print("Please run: setup_amos.py <install_dir>")
            sys.exit(1)

    version = get_file_version(exe)
    print(f"Found: {exe}")
    print(f"Version: {version}\n")

    # Write to config.json — delegate to the centralized fail-closed gate.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "config.json")

    config = {}
    if os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass

    config["AMOS"] = {
        "installed": True,
        "path": root,
        "exe": exe,
        "version": version,
        "platform": "win"
    }

    # Route persistence through the single auditable gate (write_config.py).
    # Fail-closed by default: persist ONLY on explicit opt-in. CLI flags take
    # precedence over the environment gate; --no-write always wins (detection-only).
    import subprocess
    gate = os.path.join(script_dir, "..", "..", "common", "write_config.py")
    payload = json.dumps(config, ensure_ascii=False)
    _persist = False
    if not cli_no_write:
        if cli_consent:
            _persist = True
        elif os.environ.get("STATSOFT_AUTO_WRITE") == "1":
            _persist = True
        elif os.environ.get("STATSOFT_CONFIRM") == "1" and sys.stdin.isatty():
            sys.stdout.write("Persist detected config to config.json? (y/N) ")
            sys.stdout.flush()
            _ans = sys.stdin.readline().strip().lower()
            _persist = _ans in ("y", "yes")
    if not _persist:
        print("Detection-only: config.json NOT modified. Set STATSOFT_AUTO_WRITE=1 to persist, pass --consent, or STATSOFT_CONFIRM=1 for an interactive prompt.")
    else:
        try:
            cmd = [sys.executable, gate, config_path]
            # Propagate the explicit opt-in to the centralized gate.
            if cli_consent or os.environ.get("STATSOFT_AUTO_WRITE") == "1":
                cmd.append("--consent")
            proc = subprocess.run(
                cmd,
                input=payload,
                capture_output=True,
                text=True,
            )
            if proc.stdout:
                print(proc.stdout.strip())
            if proc.stderr:
                print(proc.stderr.strip(), file=sys.stderr)
        except Exception as e:
            print("Failed to invoke config gate: " + str(e))

    print("Done.")


if __name__ == "__main__":
    main()
