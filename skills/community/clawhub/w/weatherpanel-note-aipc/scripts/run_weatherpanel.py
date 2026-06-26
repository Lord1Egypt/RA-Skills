#!/usr/bin/env python3
"""
run_weatherpanel.py - Safe local runner for weatherpanel-note-aipc.

This replaces the old .bat wrappers and keeps execution inside the bundled
Python scripts. It does not modify global heartbeat settings, OS startup,
Task Scheduler, or shell profile files.
"""

import argparse
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import env_loader

SKILL_ID = "weatherpanel-note-aipc"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CANVAS_ROOT = os.environ.get("CANVAS_ROOT", env_loader.CANVAS_ROOT_DEFAULT)
CANVAS_DIR = os.path.join(CANVAS_ROOT, SKILL_ID)
DASHBOARD_SRC = os.path.join(SCRIPT_DIR, "dashboard.html")
DASHBOARD_DST = os.path.join(CANVAS_DIR, "dashboard.html")
BASE_URL = os.environ.get("OPENCLAW_BASE_URL", "http://localhost:18789")


def prepare_dashboard() -> None:
    os.makedirs(CANVAS_DIR, exist_ok=True)
    shutil.copy2(DASHBOARD_SRC, DASHBOARD_DST)
    print(f"[runner] Dashboard prepared: {DASHBOARD_DST}")
    print(f"[runner] Suggested canvas URL: {BASE_URL}/__openclaw__/canvas/{SKILL_ID}/dashboard.html")


def run_step(script_name: str) -> int:
    script_path = os.path.join(SCRIPT_DIR, script_name)
    cmd = [sys.executable, script_path]
    print(f"[runner] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=SCRIPT_DIR)
    print(f"[runner] Exit code for {script_name}: {result.returncode}")
    return result.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        default="all",
        choices=["all", "prepare-dashboard", "fetch", "summarize", "flush"],
        help="Which portion of the workflow to run.",
    )
    args = parser.parse_args()

    if args.mode == "prepare-dashboard":
        prepare_dashboard()
        return 0

    if args.mode == "fetch":
        prepare_dashboard()
        return run_step("fetch_weather.py")

    if args.mode == "summarize":
        return run_step("summarize_weather.py")

    if args.mode == "flush":
        return run_step("flush_to_obsidian.py")

    # full pipeline
    prepare_dashboard()
    results = {
        "fetch": run_step("fetch_weather.py"),
        "summarize": run_step("summarize_weather.py"),
        "flush": run_step("flush_to_obsidian.py"),
    }

    failures = {k: v for k, v in results.items() if v != 0}
    if not failures:
        print("[runner] All steps completed successfully.")
        return 0

    print(f"[runner] Partial failures: {failures}")
    # Keep the workflow user-friendly: fetch might fail due to network,
    # summarize/flush might fail due to missing local tools. The dashboard
    # and prior cached data can still be useful, so return 0 only when at
    # least one step succeeded.
    if any(v == 0 for v in results.values()):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
