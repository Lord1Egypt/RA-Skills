#!/usr/bin/env python3
"""Run a minimal environment preflight for sf-business-data-export."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_command(args: list[str]) -> tuple[bool, str]:
    try:
        completed = subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError:
        return False, "command not found"
    output = (completed.stdout or completed.stderr or "").strip()
    return completed.returncode == 0, output


def check_command(name: str) -> dict[str, Any]:
    resolved = shutil.which(name)
    if not resolved:
        return {
            "check": f"{name}_installed",
            "status": "failed",
            "details": f"{name} is not installed or not on PATH",
            "next_action": f"install {name} and ensure it is available on PATH",
        }
    return {
        "check": f"{name}_installed",
        "status": "success",
        "details": resolved,
        "next_action": "",
    }


def check_python_version() -> dict[str, Any]:
    version = sys.version_info
    if version < (3, 9):
        return {
            "check": "python_version",
            "status": "failed",
            "details": f"python3 version is {version.major}.{version.minor}.{version.micro}",
            "next_action": "use Python 3.9 or newer",
        }
    return {
        "check": "python_version",
        "status": "success",
        "details": f"{version.major}.{version.minor}.{version.micro}",
        "next_action": "",
    }


def check_sf_auth(target_org: str | None) -> dict[str, Any]:
    command = ["sf", "org", "display", "--json"]
    if target_org:
        command.extend(["-o", target_org])
    ok, output = run_command(command)
    if not ok:
        return {
            "check": "sf_org_auth",
            "status": "failed",
            "details": output or "unable to verify Salesforce org authentication",
            "next_action": (
                "run `sf org login web` or provide a valid org alias with `--target-org`"
            ),
        }

    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        return {
            "check": "sf_org_auth",
            "status": "failed",
            "details": "sf org display returned non-JSON output",
            "next_action": "verify the Salesforce CLI installation and org login state",
        }

    result = payload.get("result", {})
    username = result.get("username") or result.get("id") or "unknown"
    return {
        "check": "sf_org_auth",
        "status": "success",
        "details": f"authenticated as {username}",
        "next_action": "",
    }


def check_output_dir(path_str: str) -> dict[str, Any]:
    output_dir = Path(path_str).expanduser()
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        probe = output_dir / ".sf_business_data_export_write_test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        return {
            "check": "output_directory",
            "status": "failed",
            "details": str(exc),
            "next_action": f"use a writable output directory instead of {output_dir}",
        }
    return {
        "check": "output_directory",
        "status": "success",
        "details": str(output_dir),
        "next_action": "",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target-org",
        help="Salesforce org alias or username to verify. Defaults to current default org.",
    )
    parser.add_argument(
        "--output-dir",
        default="./out",
        help="Directory to verify for writable export outputs",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of a plain-text summary",
    )
    args = parser.parse_args()

    results = [
        check_command("sf"),
        check_command("python3"),
        check_python_version(),
        check_output_dir(args.output_dir),
    ]

    if results[0]["status"] == "success":
        results.append(check_sf_auth(args.target_org))
    else:
        results.append(
            {
                "check": "sf_org_auth",
                "status": "failed",
                "details": "skipped because sf is unavailable",
                "next_action": "install Salesforce CLI before verifying org authentication",
            }
        )

    overall_status = "success" if all(r["status"] == "success" for r in results) else "failed"
    payload = {"status": overall_status, "checks": results}

    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    print(f"preflight status: {overall_status}")
    for result in results:
        print(f"- {result['check']}: {result['status']} ({result['details']})")
        if result["next_action"]:
            print(f"  next_action: {result['next_action']}")


if __name__ == "__main__":
    main()
