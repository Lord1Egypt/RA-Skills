"""
Helper for running LibreOffice (soffice) on Windows.
Simplified version — Linux AF_UNIX shim removed (not needed on Windows).

Usage:
    from office.soffice import run_soffice, get_soffice_env

    # Option 1 – run soffice directly
    result = run_soffice(["--headless", "--convert-to", "pdf", "input.docx"])

    # Option 2 – get env dict for your own subprocess calls
    env = get_soffice_env()
    subprocess.run(["soffice", ...], env=env)
"""

import os
import subprocess
import shutil


_SOFFICE_NAMES = [
    "soffice",
    "soffice.exe",
    "libreoffice",
    "libreoffice.exe",
]

# Common install paths on Windows
_WINDOWS_SEARCH_PATHS = [
    r"C:\Program Files\LibreOffice\program\soffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    r"C:\Program Files\LibreOffice\program\libreoffice.exe",
    r"C:\Program Files (x86)\LibreOffice\program\libreoffice.exe",
    # Portable installs
    os.path.expanduser(r"~\AppData\Local\LibreOffice\program\soffice.exe"),
]


def _find_soffice() -> str:
    """Find soffice executable on the system PATH or known locations."""
    # Check SOFFICE_PATH env var first
    soffice_path = os.environ.get("SOFFICE_PATH")
    if soffice_path and os.path.isfile(soffice_path):
        return soffice_path

    # Check known Windows paths
    for p in _WINDOWS_SEARCH_PATHS:
        if os.path.isfile(p):
            return p

    # Check PATH
    for name in _SOFFICE_NAMES:
        found = shutil.which(name)
        if found:
            return found

    raise FileNotFoundError(
        "LibreOffice (soffice) not found. Install LibreOffice or set SOFFICE_PATH env var.\n"
        "Download: https://www.libreoffice.org/download/download-libreoffice/"
    )


def get_soffice_env() -> dict:
    """Return environment dict for running soffice headlessly."""
    env = os.environ.copy()
    env["SAL_USE_VCLPLUGIN"] = "svp"
    return env


def run_soffice(args: list, **kwargs) -> subprocess.CompletedProcess:
    """Run soffice with the given arguments."""
    soffice = _find_soffice()
    env = get_soffice_env()
    return subprocess.run([soffice] + args, env=env, **kwargs)


if __name__ == "__main__":
    import sys
    result = run_soffice(sys.argv[1:])
    sys.exit(result.returncode)
