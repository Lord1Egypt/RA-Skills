#!/usr/bin/env python3
"""
Universal fresh runner for shop_inspection.

Features:
1) Auto-detect project root (folder containing main.py + config.yaml)
2) Auto-pick Python executable (.venv/venv/python), fallback to current Python
3) Optional Playwright Chromium install
4) Bootstrap seller/buyer login states if missing
5) Run inspection modules

Usage examples:
  python shop_inspection_fresh_run_universal.py
  python shop_inspection_fresh_run_universal.py --project "D:\\shop_inspection"
  python shop_inspection_fresh_run_universal.py --modules evaluation,frontend,backend,shipping
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_MODULES = "evaluation,frontend,backend,shipping"


def run(cmd: list[str], *, interactive: bool = False) -> int:
    print("\n>>", " ".join(cmd))
    if interactive:
        return subprocess.call(cmd)
    return subprocess.run(cmd, text=True).returncode


def _candidate_project_roots(explicit: str | None) -> list[Path]:
    roots: list[Path] = []
    if explicit:
        roots.append(Path(explicit).resolve())

    script_dir = Path(__file__).resolve().parent
    roots.extend(
        [
            script_dir,
            script_dir / "shop_inspection",
            script_dir.parent / "shop_inspection",
            Path.cwd(),
            Path.cwd() / "shop_inspection",
        ]
    )
    return roots


def find_project_root(explicit: str | None) -> Path:
    for p in _candidate_project_roots(explicit):
        if (p / "main.py").exists() and (p / "config.yaml").exists():
            return p
    raise SystemExit(
        "Cannot find project root.\n"
        "Please pass --project \"<path-to-shop_inspection>\"."
    )


def pick_python(project_root: Path, explicit_python: str | None) -> Path:
    if explicit_python:
        p = Path(explicit_python).resolve()
        if p.exists():
            return p
        raise SystemExit(f"--python not found: {p}")

    candidates = [
        project_root / ".venv" / "Scripts" / "python.exe",
        project_root / "venv" / "Scripts" / "python.exe",
        project_root / ".venv" / "bin" / "python",
        project_root / "venv" / "bin" / "python",
    ]
    for c in candidates:
        if c.exists():
            return c

    # Fallback to current interpreter (works if dependencies installed here)
    return Path(sys.executable).resolve()


def ensure_exists(path: Path, name: str) -> None:
    if not path.exists():
        raise SystemExit(f"{name} not found: {path}")


def maybe_install_playwright(py: Path) -> None:
    ans = input("Install/repair Playwright Chromium now? [Y/n]: ").strip().lower()
    if ans in ("", "y", "yes"):
        code = run([str(py), "-m", "playwright", "install", "chromium"])
        if code != 0:
            raise SystemExit("Playwright install failed.")


def bootstrap_if_missing(py: Path, main_py: Path, config: Path, role: str, state_file: Path) -> None:
    if state_file.exists():
        print(f"{role} state exists: {state_file}")
        return

    print(f"\n{role} state missing: {state_file}")
    print("Browser will open. Login manually, then press Enter in terminal to save state.")
    code = run(
        [
            str(py),
            str(main_py),
            "--config",
            str(config),
            "--bootstrap-login",
            "--bootstrap-role",
            role,
        ],
        interactive=True,
    )
    if code != 0:
        raise SystemExit(f"bootstrap login failed for role={role}")
    if not state_file.exists():
        raise SystemExit(f"state file was not created: {state_file}")


def run_inspection(py: Path, main_py: Path, config: Path, modules: str) -> None:
    cmd = [str(py), str(main_py), "--config", str(config)]
    if modules.strip():
        cmd.extend(["--modules", modules.strip()])
    code = run(cmd)
    if code != 0:
        raise SystemExit("inspection run failed.")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Universal fresh runner for shop_inspection")
    p.add_argument("--project", default="", help="Path to shop_inspection project root")
    p.add_argument("--python", default="", help="Path to python executable to run main.py")
    p.add_argument(
        "--modules",
        default=DEFAULT_MODULES,
        help=f"Modules to run (default: {DEFAULT_MODULES})",
    )
    p.add_argument(
        "--skip-playwright-install",
        action="store_true",
        help="Skip prompt to install/repair Playwright Chromium",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    project_root = find_project_root(args.project or None)
    py = pick_python(project_root, args.python or None)

    main_py = project_root / "main.py"
    config = project_root / "config.yaml"
    state_dir = project_root / "state"
    seller_state = state_dir / "seller_storage.json"
    buyer_state = state_dir / "buyer_storage.json"

    ensure_exists(main_py, "main.py")
    ensure_exists(config, "config.yaml")
    ensure_exists(py, "python executable")
    state_dir.mkdir(parents=True, exist_ok=True)

    print(f"Project root: {project_root}")
    print(f"Python exe : {py}")
    print(f"Config     : {config}")
    print(f"Modules    : {args.modules or '(all default in main.py)'}")

    if not args.skip_playwright_install:
        maybe_install_playwright(py)

    # seller for evaluation/backend/shipping; buyer for frontend
    bootstrap_if_missing(py, main_py, config, "seller", seller_state)
    bootstrap_if_missing(py, main_py, config, "buyer", buyer_state)

    run_inspection(py, main_py, config, args.modules)

    reports_dir = project_root / "reports"
    print("\nDone. Check reports:")
    print(reports_dir)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nInterrupted.")
        raise SystemExit(130)
