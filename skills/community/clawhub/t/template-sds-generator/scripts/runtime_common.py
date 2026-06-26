from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_IMPORTS = (
    "fitz",
    "jsonschema",
    "lxml",
    "pdfplumber",
    "PIL",
    "pydantic",
    "rapidfuzz",
    "yaml",
    "docx",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VENV_DIR = PROJECT_ROOT / ".venv"
TEMPLATE_PATH = PROJECT_ROOT / "assets" / "templates" / "sds_base.docx"
REQUIREMENTS_LOCK = PROJECT_ROOT / "requirements.lock"


def candidate_python_commands() -> list[list[str]]:
    candidates: list[list[str]] = []
    for command in ("python3", "python", "py"):
        if shutil.which(command):
            candidates.append([command])
    if sys.executable:
        candidates.insert(0, [sys.executable])
    unique: list[list[str]] = []
    seen: set[tuple[str, ...]] = set()
    for candidate in candidates:
        key = tuple(candidate)
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
    return unique


def venv_python() -> list[str]:
    if sys.platform == "win32":
        return [str(VENV_DIR / "Scripts" / "python.exe")]
    return [str(VENV_DIR / "bin" / "python")]


def run_python(command: list[str], args: list[str], *, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command + args, cwd=PROJECT_ROOT, capture_output=True, text=True, check=check)


def python_exists(command: list[str]) -> bool:
    executable = command[0]
    return Path(executable).exists() if Path(executable).is_absolute() else shutil.which(executable) is not None


def runtime_complete(command: list[str]) -> bool:
    if not python_exists(command):
        return False
    probe = "import " + ", ".join(REQUIRED_IMPORTS)
    result = run_python(command, ["-c", probe], check=False)
    return result.returncode == 0


def pip_available(command: list[str]) -> bool:
    return run_python(command, ["-m", "pip", "--version"], check=False).returncode == 0


def create_or_repair_venv() -> None:
    if python_exists(venv_python()):
        return
    launcher = next((candidate for candidate in candidate_python_commands() if python_exists(candidate)), None)
    if launcher is None:
        raise RuntimeError("No Python launcher found. Install Python 3.11+ first.")
    result = run_python(launcher, ["-m", "venv", str(VENV_DIR)], check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Failed to create virtualenv.")


def ensure_pip(command: list[str]) -> None:
    if pip_available(command):
        return
    result = run_python(command, ["-m", "ensurepip", "--upgrade"], check=False)
    if result.returncode != 0 or not pip_available(command):
        raise RuntimeError("Unable to provision pip inside .venv. Install Python with venv/pip support first.")


def install_requirements(command: list[str]) -> None:
    upgrade = run_python(command, ["-m", "pip", "install", "--upgrade", "pip"], check=False)
    if upgrade.returncode != 0:
        raise RuntimeError(upgrade.stderr.strip() or upgrade.stdout.strip() or "Failed to upgrade pip.")
    install = run_python(command, ["-m", "pip", "install", "-r", str(REQUIREMENTS_LOCK)], check=False)
    if install.returncode != 0:
        raise RuntimeError(install.stderr.strip() or install.stdout.strip() or "Failed to install requirements.")


def ensure_base_template(command: list[str]) -> None:
    if TEMPLATE_PATH.exists():
        return
    result = run_python(command, [str(PROJECT_ROOT / "scripts" / "build_base_template.py")], check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Failed to build base template.")


def resolve_runtime() -> list[str] | None:
    for candidate in (venv_python(), *candidate_python_commands()):
        if runtime_complete(candidate):
            return candidate
    return None
