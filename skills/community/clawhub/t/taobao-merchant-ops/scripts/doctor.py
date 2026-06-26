#!/usr/bin/env python3
from __future__ import annotations

import importlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from app_config import load_runtime_config
from license_gate import load_license_status


def _check(condition: bool, name: str, detail: str, *, level: str = "error") -> dict[str, str]:
    return {
        "name": name,
        "ok": "true" if condition else "false",
        "level": level,
        "detail": detail,
    }


def run_doctor(config_path: str | Path | None = None, python_exe: str | Path | None = None) -> list[dict[str, str]]:
    config = load_runtime_config(config_path)
    py = Path(python_exe or sys.executable)
    results: list[dict[str, str]] = []

    results.append(
        _check(
            sys.version_info >= (3, 9),
            "python_version",
            f"Current: {sys.version.split()[0]}",
        )
    )
    results.append(_check(py.exists(), "python_executable", str(py)))

    for key in ("capture_script", "inspection_script", "parse_script", "mapping_path"):
        path = Path(config[key])
        results.append(_check(path.exists(), key, str(path)))

    for key in ("downloads_dir", "output_dir", "run_log_dir"):
        path = Path(config[key])
        try:
            path.mkdir(parents=True, exist_ok=True)
            test_file = path / ".write_test"
            test_file.write_text("ok", encoding="utf-8")
            test_file.unlink()
            results.append(_check(True, f"{key}_writable", str(path)))
        except Exception as exc:
            results.append(_check(False, f"{key}_writable", f"{path}: {exc}"))

    for module in ("openpyxl", "yaml", "playwright"):
        try:
            importlib.import_module(module)
            results.append(_check(True, f"module_{module}", "installed"))
        except Exception as exc:
            results.append(_check(False, f"module_{module}", f"missing: {exc}"))

    playwright_cli = shutil.which("playwright")
    browser_install = subprocess.run(
        [str(py), "-m", "playwright", "install", "--dry-run", "chromium"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    results.append(
        _check(
            browser_install.returncode == 0,
            "playwright_chromium",
            browser_install.stdout.strip() or f"cli={playwright_cli}",
            level="warning" if browser_install.returncode != 0 else "error",
        )
    )

    lic = load_license_status(Path(config["license_file"]))
    level = "warning" if lic["status"] != "valid" else "error"
    results.append(_check(lic["status"] == "valid", "license_status", json.dumps(lic, ensure_ascii=False), level=level))
    return results


def print_doctor_report(results: list[dict[str, str]]) -> int:
    exit_code = 0
    for item in results:
        ok = item["ok"] == "true"
        icon = "OK" if ok else item["level"].upper()
        print(f"[{icon}] {item['name']}: {item['detail']}")
        if not ok and item["level"] == "error":
            exit_code = 1
    if exit_code:
        print("\nFix errors above, then rerun with: python scripts/run_taobao_merchant_ops.py --doctor")
    return exit_code
