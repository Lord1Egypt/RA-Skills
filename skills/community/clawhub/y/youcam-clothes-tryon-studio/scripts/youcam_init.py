"""Python Environment bootstrap: virtual environment setup and dependency checks for youcam agent skill."""

import importlib.util
import json
import os
import subprocess
import sys
from typing import Any, NoReturn

from constants import REQUIREMENTS_FILE, VENV_DIR

# Third-party packages the CLI needs, as {import name: pip package name}.
_REQUIRED_PACKAGES = {"requests": "requests", "yaml": "PyYAML"}


def _venv_python(venv_dir: str) -> str:
    """Return the path to the python executable inside a virtual environment.

    Returns:
        str: Path to the venv's python executable, OS-appropriate.
    """
    if os.name == "nt":
        return os.path.join(venv_dir, "Scripts", "python.exe")
    return os.path.join(venv_dir, "bin", "python")


def exit_with_error(error: str, hint: str, details: Any = None, code: int = 1, **extra: Any) -> NoReturn:
    """Print a structured {error, hint, details} JSON message to stderr and exit.

    Args:
        error: Short error message.
        hint: Hints for debugging.
        details: The underlying error or raw payload, if any.
        code: The process exit code.
        **extra: Additional fields to include, e.g. per-item results.
    """

    payload: dict[str, Any] = {"error": error, "hint": hint}
    if details is not None:
        payload["details"] = details
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(code)


def _run_setup_step(cmd: list[str]) -> None:
    """Run one setup command, exiting with a structured error if it fails."""
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as exc:
        exit_with_error(
            "setup_failed",
            hint="Re-run `python youcam_core.py setup`, or run the failing command manually to see its full output.",
            details=f"command={exc.cmd!r} returncode={exc.returncode}",
        )


def setup_env() -> None:
    """
    Set up a skill's Python environment by creating a local virtual environment and installing dependencies.
    - Create a local virtual environment named .venv and install requirements.txt into it.
    - If the virtual environment already exists, it will not be recreated, but requirements.txt will still be installed.
    """
    print(f"[setup] current interpreter: {sys.executable}, Python {sys.version.split()[0]}")
    in_venv = sys.prefix != sys.base_prefix
    print(f"[setup] running inside a virtual environment: {in_venv}")

    if os.path.isdir(VENV_DIR):
        print(f"[setup] virtual environment already exists at {VENV_DIR}")
    else:
        print(f"[setup] creating virtual environment at {VENV_DIR} ...")
        _run_setup_step([sys.executable, "-m", "venv", VENV_DIR])

    venv_python = _venv_python(VENV_DIR)
    print(f"[setup] installing dependencies from {REQUIREMENTS_FILE} ...")
    _run_setup_step([venv_python, "-m", "pip", "install", "--upgrade", "pip"])
    _run_setup_step([venv_python, "-m", "pip", "install", "-r", REQUIREMENTS_FILE])

    activate_hint = rf"{VENV_DIR}\Scripts\activate" if os.name == "nt" else f"source {VENV_DIR}/bin/activate"
    print(
        "\nINFO: these dependencies were installed into a project local virtual environment, "
        "not your system or global Python.\n"
        f'Call "{venv_python}" youcam_core.py <command> to use it directly.\n'
        f"Or activate it first by running: {activate_hint}\n"
        "Invoking `python youcam_core.py ...` with a different interpreter will not see "
        "these installed packages.",
        file=sys.stderr,
    )


def check_dependencies() -> None:
    """
    Called by every command to ensure the required dependencies are installed.
    Exit with code 3 and a structured error if any required dependency is missing.
    """
    missing = [pkg for mod, pkg in _REQUIRED_PACKAGES.items() if importlib.util.find_spec(mod) is None]
    if missing:
        exit_with_error(
            "Missing required dependencies for youcam agent skill.",
            hint="Run `python youcam_core.py setup` to create a virtual environment and install requirements.txt, "
            "or `pip install -r requirements.txt` in the skill's scripts folder.",
            details=f"{missing}",
            code=3,
        )
