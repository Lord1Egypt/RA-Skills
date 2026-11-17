#!/usr/bin/env python3
"""verify_install.py - health check for the Windows Multi-Tool Suite.

Reports what is present and what is missing. It never writes, installs, or
sends anything. Exit code 0 = healthy, 1 = something needs fixing (the report
says what), 2 = the check itself could not run.

Usage:
    python3 verify_install.py
    python3 verify_install.py --workspace /path/to/workspace
    python3 verify_install.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import sys

SKILLS = {
    "ai-creative-studio": "Creative Studio",
    "ai-trading": "Market Research",
    "b2b-lead-research-agent": "Lead Research",
}

MIN_PYTHON = (3, 9)


def skill_roots() -> list:
    home = os.path.expanduser("~")
    return [
        os.path.join(home, ".openclaw", "skills"),
        os.path.join(home, ".config", "openclaw", "skills"),
        os.path.join(os.getcwd(), "skills"),
    ]


def find_skill(name: str) -> str | None:
    for root in skill_roots():
        candidate = os.path.join(root, name)
        if os.path.isdir(candidate):
            return candidate
    return None


def default_workspace() -> str:
    override = os.environ.get("MULTITOOL_WORKSPACE", "").strip()
    if override:
        return override
    local = os.environ.get("LOCALAPPDATA", "")
    if local:
        return os.path.join(local, "MultiToolSuite")
    return os.path.join(os.path.expanduser("~"), "MultiToolSuite")


def check(workspace: str) -> dict:
    report = {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "windows_ok": platform.system() == "Windows",
            "python_ok": sys.version_info[:2] >= MIN_PYTHON,
        },
        "tools": {
            "clawhub": shutil.which("clawhub"),
            "node": shutil.which("node"),
        },
        "workspace": {
            "path": workspace,
            "exists": os.path.isdir(workspace),
            "config": os.path.join(workspace, "config.json"),
            "config_ok": os.path.isfile(os.path.join(workspace, "config.json")),
            "output_dirs": [],
        },
        "skills": {},
        "problems": [],
    }

    for sub in ("creative", "market", "leads"):
        path = os.path.join(workspace, "output", sub)
        report["workspace"]["output_dirs"].append({"name": sub, "exists": os.path.isdir(path)})

    for name, label in SKILLS.items():
        path = find_skill(name)
        report["skills"][name] = {"label": label, "installed": path is not None, "path": path}
        if path is None:
            report["problems"].append(f"{name} is not installed (clawhub install @rapidworker1/{name})")

    if platform.system() != "Windows":
        report["problems"].append("this kit targets Windows 10/11; the check still runs anywhere")
    if not report["platform"]["python_ok"]:
        report["problems"].append(f"python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+ is required")
    if not report["workspace"]["exists"]:
        report["problems"].append(f"workspace folder is missing: {workspace} (run scripts/setup.ps1)")
    if not report["workspace"]["config_ok"]:
        report["problems"].append("config.json is missing from the workspace (run scripts/setup.ps1)")

    return report


def render(report: dict) -> None:
    platform_info = report["platform"]
    print("Windows Multi-Tool Suite - install check")
    print("------------------------------------------")
    print(f"os        : {platform_info['system']} {platform_info['release']} ({platform_info['machine']})")
    print(f"python    : {platform_info['python']}")
    print(f"clawhub   : {report['tools']['clawhub'] or 'not found'}")
    print(f"node      : {report['tools']['node'] or 'not found'}")
    print(f"workspace : {report['workspace']['path']} "
          f"({'ok' if report['workspace']['exists'] else 'missing'})")
    print(f"config    : {report['workspace']['config']} "
          f"({'ok' if report['workspace']['config_ok'] else 'missing'})")
    for entry in report["workspace"]["output_dirs"]:
        print(f"output/{entry['name']:<8}: {'ok' if entry['exists'] else 'missing'}")
    print("")
    print("skills")
    for name, info in report["skills"].items():
        mark = "ok     " if info["installed"] else "missing"
        print(f"  {mark} {name:<24} {info['path'] or ''}")
    print("")
    if report["problems"]:
        print(f"{len(report['problems'])} item(s) to fix:")
        for problem in report["problems"]:
            print(f"  - {problem}")
    else:
        print("Everything checks out. Run scripts/MultiTool.ps1 to open the launcher.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Health check for the Windows Multi-Tool Suite.")
    parser.add_argument("--workspace", default="", help="Workspace folder (default: %%LOCALAPPDATA%%\\MultiToolSuite)")
    parser.add_argument("--json", action="store_true", help="Print the report as JSON")
    args = parser.parse_args()

    workspace = args.workspace or default_workspace()
    report = check(workspace)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        render(report)

    return 1 if report["problems"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
