#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys

from runtime_common import candidate_python_commands, pip_available, python_exists, run_python, runtime_complete, venv_python


def _python_version(command: list[str]) -> str:
    result = run_python(command, ["--version"], check=False)
    return (result.stdout or result.stderr).strip() or "unknown"


def _binary_version(binary: str, args: list[str]) -> str:
    if not shutil.which(binary):
        return "missing"
    result = subprocess.run([binary] + args, capture_output=True, text=True, check=False)
    return (result.stdout or result.stderr).splitlines()[0].strip() if result.returncode == 0 else "present"


def _print_status(label: str, status: str, detail: str = "") -> None:
    suffix = f"  {detail}" if detail else ""
    print(f"{label:<18} {status}{suffix}")


def main() -> int:
    print("template-sds-generator runtime doctor")
    print()
    python_entries: list[tuple[str, list[str]]] = [("project .venv", venv_python())]
    seen: set[tuple[str, ...]] = {tuple(venv_python())}
    for candidate in candidate_python_commands():
        key = tuple(candidate)
        if key in seen:
            continue
        seen.add(key)
        label = "current python" if candidate[0] == sys.executable else candidate[0]
        python_entries.append((label, candidate))

    for label, command in python_entries:
        if not python_exists(command):
            _print_status(label, "missing")
            continue
        version = _python_version(command)
        status = "ok" if runtime_complete(command) else "incomplete"
        _print_status(label, status, version)
        _print_status(f"{label} pip", "ok" if pip_available(command) else "missing")
    print()
    for binary, args, label in (
        ("tesseract", ["--version"], "OCR backend"),
        ("soffice", ["--version"], "PDF engine"),
        ("libreoffice", ["--version"], "PDF engine alt"),
    ):
        version = _binary_version(binary, args)
        if version == "missing":
            _print_status(label, "missing")
        else:
            _print_status(label, "ok", f"{shutil.which(binary)} ({version})")
    print()
    print("Notes:")
    print("- Install Python 3.11+ with venv and pip support if no usable launcher is found.")
    print("- OCR is optional, but scanned PDFs need tesseract.")
    print("- PDF export needs soffice or libreoffice.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
