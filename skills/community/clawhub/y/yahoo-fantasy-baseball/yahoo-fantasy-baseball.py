"""Entry-point script for running yahoo-fantasy-baseball.

Dependencies must be installed explicitly via --setup before first use.
This avoids silent network/install activity during normal execution.
"""

import os
import subprocess
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_VENV_DIR = os.path.join(_SCRIPT_DIR, ".deps")
_REQUIREMENTS = os.path.join(_SCRIPT_DIR, "requirements.txt")

# Determine venv python path (Windows uses Scripts/, Unix uses bin/)
if sys.platform == "win32":
    _VENV_PYTHON = os.path.join(_VENV_DIR, "Scripts", "python.exe")
else:
    _VENV_PYTHON = os.path.join(_VENV_DIR, "bin", "python3")


def _bootstrap_venv():
    """Create a local venv and install requirements."""
    print("Installing dependencies...", file=sys.stderr)

    # Create venv
    subprocess.check_call(
        [sys.executable, "-m", "venv", _VENV_DIR],
        stdout=sys.stderr,
        stderr=sys.stderr,
    )

    # Install requirements into the venv
    pip_cmd = [_VENV_PYTHON, "-m", "pip", "install", "-q", "-r", _REQUIREMENTS]
    subprocess.check_call(pip_cmd, stdout=sys.stderr, stderr=sys.stderr)

    print("Dependencies installed.", file=sys.stderr)


def _reexec_in_venv():
    """Re-execute this script using the venv's Python."""
    if sys.platform == "win32":
        # On Windows, os.execv spawns a new process and exits the current one,
        # which causes the shell to print its prompt while the child is still
        # running. Use subprocess instead so stdin/stdout are properly inherited.
        sys.exit(subprocess.call([_VENV_PYTHON, __file__] + sys.argv[1:]))
    else:
        os.execv(_VENV_PYTHON, [_VENV_PYTHON, __file__] + sys.argv[1:])


# Handle --setup: explicitly install dependencies
if "--setup" in sys.argv:
    _bootstrap_venv()
    print("Setup complete. You can now run commands normally.", file=sys.stderr)
    sys.exit(0)

# Fail fast if dependencies are not installed
if not os.path.isfile(_VENV_PYTHON):
    print(
        "Error: Dependencies not installed.\n"
        "Run with --setup first:\n"
        f"  python {os.path.basename(__file__)} --setup",
        file=sys.stderr,
    )
    sys.exit(1)

# If we're not already running inside the venv, switch to it.
if os.path.abspath(sys.executable) != os.path.abspath(_VENV_PYTHON):
    _reexec_in_venv()

# At this point we're running inside the venv.
sys.path.insert(0, os.path.join(_SCRIPT_DIR, "scripts"))

from fantasy import main

main()
