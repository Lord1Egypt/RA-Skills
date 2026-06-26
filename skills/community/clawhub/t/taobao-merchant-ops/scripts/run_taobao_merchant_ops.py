#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from app_config import load_runtime_config, save_default_config
from app_errors import AppError, DependencyError, LicenseError
from doctor import print_doctor_report, run_doctor
from license_gate import ensure_license, load_license_status, machine_fingerprint


def _run(cmd: list[str], *, required: bool, error_name: str) -> None:
    print("\n>>", " ".join(cmd))
    code = subprocess.call(cmd)
    if code != 0 and required:
        raise DependencyError(f"{error_name} failed with exit code {code}")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Run Taobao merchant flow: capture -> inspection -> parse"
    )
    p.add_argument(
        "--config",
        default="",
        help="Path to settings.json (default: <package_root>/settings.json)",
    )
    p.add_argument(
        "--python",
        default=sys.executable,
        help="Python executable for all child scripts (default: current interpreter)",
    )
    p.add_argument(
        "--capture-script",
        default="",
        help="Path to 最终完结版.py",
    )
    p.add_argument(
        "--inspection-script",
        default="",
        help="Path to shop_inspection_fresh_run_universal.py",
    )
    p.add_argument(
        "--parse-script",
        default="",
        help="Path to parse_taobao_report.py",
    )
    p.add_argument("--skip-capture", action="store_true")
    p.add_argument("--skip-inspection", action="store_true")
    p.add_argument("--skip-parse", action="store_true")
    p.add_argument(
        "--inspection-modules",
        default="evaluation,frontend,backend,shipping",
        help="Modules for inspection script if it supports --modules",
    )
    p.add_argument(
        "--license-file",
        default="",
        help="License activation file path (default from settings.json)",
    )
    p.add_argument(
        "--card-key",
        default="",
        help="Card key for first activation (if omitted and no license, script will prompt)",
    )
    p.add_argument(
        "--show-machine-id",
        action="store_true",
        help="Print machine fingerprint and exit",
    )
    p.add_argument("--license-status", action="store_true", help="Print license status and exit")
    p.add_argument("--doctor", action="store_true", help="Run environment checks and exit")
    p.add_argument("--init-config", action="store_true", help="Create default settings.json and exit")
    p.add_argument("--downloads-dir", default="", help="Override downloads directory")
    p.add_argument("--output-dir", default="", help="Override parser output directory")
    p.add_argument("--mapping-path", default="", help="Override mapping.final.json path")
    p.add_argument("--version", action="store_true", help="Print version and exit")
    return p.parse_args()


def _merged_runtime(args: argparse.Namespace) -> dict[str, str]:
    config = load_runtime_config(args.config or None)
    overrides = {
        "capture_script": args.capture_script,
        "inspection_script": args.inspection_script,
        "parse_script": args.parse_script,
        "license_file": args.license_file,
        "inspection_modules": args.inspection_modules,
        "downloads_dir": args.downloads_dir,
        "output_dir": args.output_dir,
        "mapping_path": args.mapping_path,
    }
    for key, value in overrides.items():
        if value:
            config[key] = str(Path(value).resolve()) if key.endswith(("_script", "_file", "_path", "_dir")) else value
    return config


def main() -> int:
    args = parse_args()
    if args.init_config:
        target = save_default_config(args.config or None)
        print(f"Config created: {target}")
        return 0

    runtime = _merged_runtime(args)
    py = Path(args.python)
    if not py.exists():
        raise SystemExit(f"Python executable not found: {py}")

    capture_script = Path(runtime["capture_script"])
    inspection_script = Path(runtime["inspection_script"])
    parse_script = Path(runtime["parse_script"])
    license_file = Path(runtime["license_file"])

    if args.show_machine_id:
        print("Machine ID:", machine_fingerprint())
        return 0
    if args.version:
        print(runtime["version"])
        return 0
    if args.license_status:
        print(json.dumps(load_license_status(license_file), ensure_ascii=False, indent=2))
        return 0
    if args.doctor:
        return print_doctor_report(run_doctor(args.config or None, py))

    activation = ensure_license(license_file, key_from_cli=args.card_key)
    print(f"Python: {py}")
    print(f"Config file: {runtime['config_path']}")
    print(f"Capture script: {capture_script}")
    print(f"Inspection script: {inspection_script}")
    print(f"Parse script: {parse_script}")
    print(f"Downloads dir: {runtime['downloads_dir']}")
    print(f"Output dir: {runtime['output_dir']}")
    print(f"Mapping path: {runtime['mapping_path']}")
    print(f"License file: {license_file}")
    print(f"Plan: {activation.get('plan')}  ExpiresAt: {activation.get('expires_at')}")

    if not args.skip_capture:
        if not capture_script.exists():
            raise SystemExit(f"Capture script not found: {capture_script}")
        _run(
            [
                str(py),
                str(capture_script),
                "--downloads-dir",
                runtime["downloads_dir"],
                "--run-log-dir",
                runtime["run_log_dir"],
                "--storage-state-file",
                runtime["storage_state_file"],
            ],
            required=True,
            error_name="capture",
        )

    if not args.skip_inspection:
        if not inspection_script.exists():
            raise SystemExit(f"Inspection script not found: {inspection_script}")
        _run(
            [
                str(py),
                str(inspection_script),
                "--modules",
                str(runtime["inspection_modules"]),
            ],
            required=True,
            error_name="inspection",
        )

    if not args.skip_parse:
        if not parse_script.exists():
            print(f"[WARN] Parse script not found, skip: {parse_script}")
        else:
            _run(
                [
                    str(py),
                    str(parse_script),
                    "--mapping-path",
                    runtime["mapping_path"],
                    "--excel-dir",
                    runtime["downloads_dir"],
                    "--output-dir",
                    runtime["output_dir"],
                ],
                required=False,
                error_name="parse",
            )

    print("\nDone.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AppError, LicenseError) as exc:
        print(f"[ERROR] {exc}")
        raise SystemExit(1)

