#!/usr/bin/env python3
# run-spss-internal.py — Run SPSS syntax via SPSS built-in Python (no GUI)
# Usage: "C:\Program Files\IBM\SPSS\Statistics\XX\Python3\python.exe" run-spss-internal.py <sps_file>
# Note: dynamically scan for the SPSS install directory across any drive
#
# TRUSTED-INPUT-ONLY: This helper submits the given .sps syntax to the SPSS
# processor via spss.Submit(). The syntax file is executed as code — supply
# ONLY files you authored/trust. validate_syntax() below is a best-effort
# tripwire that blocks a LIMITED, hardcoded set of obviously dangerous line
# patterns (e.g. HOST COMMAND). It is NOT a comprehensive sandbox and does
# NOT guarantee safety against obfuscated/alternate syntax. Do not rely on it
# to sanitize untrusted input.

import sys
import os
import re

# EXECUTION GATE (default-deny, SDI-1/SDI-4): running SPSS syntax launches the
# third-party SPSS engine to execute user-supplied .sps code. Require the
# execution opt-in STATSOFT_VERIFY=1 — NOT the disclosure gate STATSOFT_REVEAL,
# which only governs install-path/version disclosure. The caller
# (statsoft-spss.ps1) enforces the same gate; this is defense-in-depth at the
# helper boundary so an authorized run is never wrongly blocked by a missing
# REVEAL, and an unauthorized run can never slip through.
if os.environ.get("STATSOFT_VERIFY") != "1":
    print("Execution denied (default-deny): set STATSOFT_VERIFY=1 to run SPSS syntax via the third-party SPSS engine.")
    sys.exit(1)

# Output helper (English-only; the Chinese argument is kept for call-site parity
# but is no longer printed).
def log(msg_cn, msg_en=None):
    if msg_en is None:
        msg_en = msg_cn
    print(msg_en)


def validate_syntax(syntax):
    """
    Best-effort tripwire, NOT a security guarantee.

    Blocks a LIMITED, hardcoded set of obviously dangerous line patterns
    (HOST / INSERT FILE / PRESERVE / RESTORE / COMPUTE...EXECUTE). This is a
    coarse denylist that can be bypassed by obfuscated or alternate syntax
    forms; it does not validate SPSS syntax at the statement level and must
    not be treated as a sanitizer for untrusted input. Callers must only pass
    trusted, user-authored .sps files.
    """
    dangerous_patterns = [
        r'^\s*HOST\s+COMMAND\s*=\s*',
        r'^\s*HOST\s+',
        r'^\s*INSERT\s+.*FILE\s*=\s*',
        r'^\s*PRESERVE\s*\.',
        r'^\s*RESTORE\s*\.',
        r'^\s*COMPUTE\s+.*EXECUTE\s*\.',
    ]
    lines = syntax.splitlines()
    for i, line in enumerate(lines, 1):
        if not line.strip() or line.strip().startswith('*'):
            continue
        for pattern in dangerous_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return False, "Line {}: blocked pattern '{}' in '{}'".format(i, pattern.strip(), line.strip()[:60])
    return True, "OK"


def _find_spss_home():
    """
    Auto-detect SPSS installation directory dynamically.
    Dynamically detect the SPSS install dir: iterate all drives and known patterns.
    """
    # Collect all available drive letters
    drives = ["C", "D", "E"]
    if sys.platform == "win32":
        try:
            import string
            import ctypes
            bitmask = ctypes.windll.kernel32.GetLogicalDrives()
            drives = [d for i, d in enumerate(string.ascii_uppercase) if bitmask & (1 << i)]
        except:
            pass  # fallback to default drives

    versions = ["26", "27", "28", "29", "30", "31"]
    patterns = [
        "{0}:\\Program Files\\IBM\\SPSS\\Statistics\\{1}",
        "{0}:\\Program Files (x86)\\IBM\\SPSS\\Statistics\\{1}",
        "{0}:\\SPSS\\Statistics\\{1}",
        "{0}:\\IBM\\SPSS\\Statistics\\{1}",
    ]

    for d in drives:
        for v in versions:
            for pat in patterns:
                dirpath = pat.format(d, v)
                if os.path.isdir(dirpath):
                    python_exe = os.path.join(dirpath, "Python3", "python.exe")
                    if os.path.isfile(python_exe):
                        return dirpath, python_exe
    return None, None


# Auto-detect SPSS home
spss_home, stats_python_path = _find_spss_home()
if spss_home is None:
    log("SPSS Statistics installation not detected", "SPSS Statistics installation not detected")
    log("Please verify SPSS is correctly installed with path SPSS\\Statistics\\<version>", "Please verify SPSS is correctly installed with path SPSS\\Statistics\\<version>")
    sys.exit(1)

# Validate path security (pattern-based, not hardcoded)
lowered = spss_home.lower()
if not ("spss" in lowered and "statistics" in lowered):
    log("SPSS path is not within the expected installation directory", "SPSS path is not within the expected installation directory")
    sys.exit(1)

# Add SPSS Python package path
spss_pkg = os.path.join(spss_home, "Python3", "Lib", "site-packages")
if spss_pkg not in sys.path:
    sys.path.insert(0, spss_pkg)

# Add SPSS bin path (DLL dependencies)
os.environ["PATH"] = spss_home + ";" + os.environ.get("PATH", "")

log("SPSS install dir: " + spss_home, "SPSS install dir: " + spss_home)
log("Built-in Python: " + stats_python_path, "Built-in Python: " + stats_python_path)

try:
    import spss
    log("SPSS Python module loaded successfully", "SPSS Python module loaded successfully")
except Exception as e:
    log("Failed to load SPSS module: " + str(e), "Failed to load SPSS module: " + str(e))
    sys.exit(1)


def run_syntax(sps_file):
    """Run syntax file via spss.Submit() (no GUI)"""
    if not os.path.exists(sps_file):
        log("Syntax file not found: " + sps_file, "Syntax file not found: " + sps_file)
        return 1

    with open(sps_file, "r", encoding="utf-8", errors="replace") as f:
        syntax = f.read()

    log("Running syntax file: " + sps_file, "Running syntax file: " + sps_file)
    log("Syntax lines: " + str(len(syntax.splitlines())), "Syntax lines: " + str(len(syntax.splitlines())))

    # Validate syntax for safety
    valid, reason = validate_syntax(syntax)
    if not valid:
        log("Syntax security check failed: " + reason, "Syntax security check failed: " + reason)
        log("Execution rejected. Please check the syntax file.", "Execution rejected. Please check the syntax file.")
        return 1

    log("Syntax security check passed", "Syntax security check passed")

    try:
        spss.StartSPSS()
        log("SPSS processor started (no GUI, no splash)", "SPSS processor started (no GUI, no splash)")

        spss.Submit(syntax)
        log("Syntax execution complete", "Syntax execution complete")

        spss.StopSPSS()
        log("SPSS processor stopped", "SPSS processor stopped")
        return 0

    except Exception as e:
        log("Syntax execution failed: " + str(e), "Syntax execution failed: " + str(e))
        import traceback
        traceback.print_exc()
        try:
            spss.StopSPSS()
        except:
            pass
        return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        log("Usage: python.exe run-spss-internal.py <sps_file>", "Usage: python.exe run-spss-internal.py <sps_file>")
        sys.exit(1)

    sps_file = sys.argv[1]
    rc = run_syntax(sps_file)
    sys.exit(rc)
