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

    # If command-line argument provided, use it directly
    if len(sys.argv) > 1:
        manual_dir = sys.argv[1]
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

    # Write to config.json
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "config.json")

    config = {}
    if os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except:
            pass

    config["AMOS"] = {
        "installed": True,
        "path": root,
        "exe": exe,
        "version": version,
        "platform": "win"
    }

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"Configuration saved to: {config_path}")
    print("Done.")


if __name__ == "__main__":
    main()
