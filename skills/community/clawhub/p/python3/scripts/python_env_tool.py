#!/usr/bin/env python3
"""Practical Python environment helper for skill workflows."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def _venv_python(venv: Path) -> Path:
    if os.name == "nt":
        return venv / "Scripts" / "python.exe"
    return venv / "bin" / "python"


def _run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def cmd_doctor(_: argparse.Namespace) -> int:
    print(f"python_version={sys.version.split()[0]}")
    print(f"python_executable={sys.executable}")
    print(f"venv_active={'yes' if os.environ.get('VIRTUAL_ENV') else 'no'}")
    print(f"pip_module_available={'yes' if shutil.which('python3') else 'unknown'}")
    for filename in ("pyproject.toml", "requirements.txt", "requirements-dev.txt"):
        print(f"has_{filename.replace('.', '_')}={'yes' if Path(filename).exists() else 'no'}")
    return 0


def cmd_bootstrap(args: argparse.Namespace) -> int:
    venv = Path(args.venv)
    if args.recreate and venv.exists():
        shutil.rmtree(venv)
    if not venv.exists():
        _run([sys.executable, "-m", "venv", str(venv)])

    py = _venv_python(venv)
    _run([str(py), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"])

    if args.requirements:
        req = Path(args.requirements)
        if not req.exists():
            raise FileNotFoundError(f"requirements file not found: {req}")
        _run([str(py), "-m", "pip", "install", "-r", str(req)])

    print(f"venv_ready={venv}")
    return 0


def cmd_install(args: argparse.Namespace) -> int:
    venv = Path(args.venv)
    py = _venv_python(venv)
    if not py.exists():
        raise FileNotFoundError(
            f"venv python not found at {py}. Run bootstrap first."
        )

    if args.requirements:
        req = Path(args.requirements)
        if not req.exists():
            raise FileNotFoundError(f"requirements file not found: {req}")
        _run([str(py), "-m", "pip", "install", "-r", str(req)])

    if args.packages:
        _run([str(py), "-m", "pip", "install", *args.packages])

    if args.editable:
        _run([str(py), "-m", "pip", "install", "-e", "."])

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Python environment workflow helper")
    sub = parser.add_subparsers(dest="command", required=True)

    doctor = sub.add_parser("doctor", help="print environment checks")
    doctor.set_defaults(func=cmd_doctor)

    bootstrap = sub.add_parser("bootstrap", help="create/refresh venv and bootstrap pip")
    bootstrap.add_argument("--venv", default=".venv", help="venv path (default: .venv)")
    bootstrap.add_argument("--recreate", action="store_true", help="delete and recreate venv")
    bootstrap.add_argument(
        "--requirements",
        default="",
        help="optional requirements file to install after bootstrap",
    )
    bootstrap.set_defaults(func=cmd_bootstrap)

    install = sub.add_parser("install", help="install packages into an existing venv")
    install.add_argument("--venv", default=".venv", help="venv path (default: .venv)")
    install.add_argument(
        "--requirements",
        default="",
        help="optional requirements file to install",
    )
    install.add_argument(
        "--package",
        dest="packages",
        action="append",
        default=[],
        help="package to install (repeatable)",
    )
    install.add_argument(
        "--editable",
        action="store_true",
        help="install current project with pip install -e .",
    )
    install.set_defaults(func=cmd_install)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except subprocess.CalledProcessError as exc:
        print(f"error: command failed with exit code {exc.returncode}", file=sys.stderr)
        return exc.returncode
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
