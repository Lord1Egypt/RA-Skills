# !/usr/bin/env python3
"""
Bootstrap path setup and rwlib imports for voice-setup scripts.

Gracefully handles the case where `rabbit-writes` is missing as a sibling skill.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# scripts -> voice-setup -> skills.
SKILLS_DIR = os.path.dirname(os.path.dirname(HERE))
ENGINE_DIR = os.path.join(SKILLS_DIR, "rabbit-writes")
SCAN_PATH = os.path.join(ENGINE_DIR, "scripts", "scan.py")
RWLIB_PARENT = os.path.dirname(SCAN_PATH)

for path in (HERE, RWLIB_PARENT):
    if os.path.exists(os.path.join(path, "rwlib")) and path not in sys.path:
        sys.path.insert(0, path)

try:
    from rwlib import cli_error, inflect, voice_check, voices as voices_mod
    from rwlib.voices import load_scan
except (ImportError, ModuleNotFoundError) as exc:
    script_name = os.path.basename(sys.argv[0]) if sys.argv and sys.argv[0] else "script"
    out = [
        "=" * 70,
        "FILE / I/O ERROR: Sibling engine skill `rabbit-writes` is missing.",
        "=" * 70,
        f"Script: {script_name}",
        "Parameter: 'rabbit-writes sibling skill' (expected type: directory path)",
        f"Provided Path: {ENGINE_DIR!r}",
        f"Details: {exc}",
        "\nVALID USAGE REQUIREMENT:",
        f"  Install `rabbit-writes` as a sibling directory under: {SKILLS_DIR}",
        f"  Expected structure: {SKILLS_DIR}/rabbit-writes/scripts/rwlib/",
        "=" * 70
    ]
    print("\n".join(out), file=sys.stderr)
    sys.exit(2)

NAME_RX = re.compile(r"^[A-Za-z0-9_-]+$")

__all__ = [
    "HERE", "SKILLS_DIR", "ENGINE_DIR", "SCAN_PATH", "RWLIB_PARENT",
    "cli_error", "inflect", "voice_check", "voices_mod", "load_scan",
    "NAME_RX"
]
