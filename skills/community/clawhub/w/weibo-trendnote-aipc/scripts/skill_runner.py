#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
skill_runner.py - Python entry point for Weibo TrendNote AI PC.

Replaces the previous PowerShell wrappers with a single Python runner so the
skill bundle can be published to ClawHub without .ps1 files.

Modes:
  once [--force]    Run fetch -> summarize -> flush one time.
  cron-fetch        Run fetch; summarize only when data changed.
  cron-flush        Flush queued summaries to Obsidian.
  install-crons     Register optional recurring OpenClaw cron jobs.

Behavior notes:
- Loads optional values from env.ps1 if that file exists.
- Preserves the original Python business logic by delegating to:
  fetch_weibo_hot.py, summarize_weibo_hot.py, flush_queue_to_obsidian.py
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

STATE_DIR = Path(r"C:\Users\Intel\.openclaw\state\weibo_hot")
ENV_FILE = STATE_DIR / "env.ps1"
CRON_TZ = "Asia/Shanghai"


def _print_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def load_env_ps1(path: Path = ENV_FILE) -> None:
    """Parse a minimal subset of PowerShell env assignments.

    Supported lines:
      $env:NAME = "value"
      $env:NAME='value'
      $env:NAME = value

    This keeps compatibility with the user's existing env.ps1 without requiring
    PowerShell at runtime.
    """
    if not path.exists():
        return

    pattern = re.compile(r'^\s*\$env:([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+?)\s*$')
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        m = pattern.match(line)
        if not m:
            continue
        key, raw_val = m.groups()
        value = raw_val.strip()
        if value and value[0] not in ('"', "'"):
            value = value.split("#", 1)[0].strip()
        if (len(value) >= 2) and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        value = value.replace("`\"", '"').replace("`'", "'")
        os.environ[key] = value


def python_executable() -> str:
    return sys.executable or shutil.which("python") or "python"


def run_python(script_name: str, *args: str) -> int:
    script_path = Path(__file__).resolve().parent / script_name
    cmd = [python_executable(), str(script_path), *args]
    print(f"[runner] exec: {' '.join(cmd)}")
    completed = subprocess.run(cmd)
    return completed.returncode


def run_once(force: bool = False) -> int:
    _print_header("Weibo TrendNote AI PC — One-Time Run")

    print("[pipeline] [1/3] Fetching...")
    rc = run_python("fetch_weibo_hot.py")
    if rc == 1:
        print("[pipeline] Fetch failed.", file=sys.stderr)
        return 1
    if rc == 0 and not force:
        print("[pipeline] Hot list unchanged; skipping summarize/flush.")
        return 0

    print("\n[pipeline] [2/3] Summarizing...")
    rc2 = run_python("summarize_weibo_hot.py")
    print(f"[pipeline] Summarize exited with code {rc2}")

    print("\n[pipeline] [3/3] Flushing to Obsidian...")
    rc3 = run_python("flush_queue_to_obsidian.py")
    print(f"[pipeline] Flush exited with code {rc3}")

    return 0 if rc2 == 0 and rc3 == 0 else 1


def run_cron_fetch() -> int:
    _print_header("Weibo TrendNote AI PC — Cron Fetch")
    rc = run_python("fetch_weibo_hot.py")
    if rc == 0:
        print("[cron-fetch] Hot list unchanged.")
        return 0
    if rc == 42:
        print("[cron-fetch] Hot list changed; running summarize step.")
        rc2 = run_python("summarize_weibo_hot.py")
        print(f"[cron-fetch] Summarize exited with code {rc2}")
        return 0 if rc2 == 0 else rc2
    print(f"[cron-fetch] Fetch failed with code {rc}", file=sys.stderr)
    return rc


def run_cron_flush() -> int:
    _print_header("Weibo TrendNote AI PC — Cron Flush")
    rc = run_python("flush_queue_to_obsidian.py")
    print(f"[cron-flush] Exited with code {rc}")
    return rc


def resolve_openclaw_bin() -> str:
    env_bin = os.environ.get("OPENCLAW_BIN")
    if env_bin:
        return env_bin
    found = shutil.which("openclaw")
    if found:
        return found
    found_cmd = shutil.which("openclaw.CMD")
    if found_cmd:
        return found_cmd
    return "openclaw"


def _quote_for_exec(value: str) -> str:
    return '"' + value.replace('"', '\\"') + '"'


def openclaw_run(*args: str) -> subprocess.CompletedProcess:
    cmd = [resolve_openclaw_bin(), *args]
    print(f"[runner] exec: {' '.join(cmd)}")
    return subprocess.run(cmd)


def install_crons() -> int:
    _print_header("Weibo TrendNote AI PC — Install Cron Jobs")
    oc = resolve_openclaw_bin()
    runner_path = str(Path(__file__).resolve())
    py = python_executable()

    msg_fetch = f'exec: {_quote_for_exec(py)} {_quote_for_exec(runner_path)} cron-fetch'
    msg_flush = f'exec: {_quote_for_exec(py)} {_quote_for_exec(runner_path)} cron-flush'

    stale_names = [
        "weibo-search-fetch-5m",
        "weibo-hot-fetch-5m",
        "weibo-obsidian-flush-10m",
        "weibo-trendnote-aipc-fetch-5m",
        "weibo-trendnote-aipc-obsidian-flush-10m",
    ]
    for name in stale_names:
        subprocess.run([oc, "cron", "remove", "--name", name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    result1 = openclaw_run(
        "cron", "add",
        "--name", "weibo-trendnote-aipc-fetch-5m",
        "--cron", "*/5 * * * *",
        "--tz", CRON_TZ,
        "--session", "isolated",
        "--message", msg_fetch,
    )
    print("[cron] fetch job:", "OK" if result1.returncode == 0 else f"FAIL ({result1.returncode})")

    result2 = openclaw_run(
        "cron", "add",
        "--name", "weibo-trendnote-aipc-obsidian-flush-10m",
        "--cron", "*/10 * * * *",
        "--tz", CRON_TZ,
        "--session", "isolated",
        "--message", msg_flush,
    )
    print("[cron] flush job:", "OK" if result2.returncode == 0 else f"FAIL ({result2.returncode})")

    openclaw_run("cron", "list")
    return 0 if result1.returncode == 0 and result2.returncode == 0 else 1


def main() -> int:
    load_env_ps1()

    parser = argparse.ArgumentParser(description="Weibo TrendNote AI PC runner")
    sub = parser.add_subparsers(dest="command", required=True)

    p_once = sub.add_parser("once", help="Run fetch -> summarize -> flush once")
    p_once.add_argument("--force", action="store_true", help="Run summarize/flush even when hot list is unchanged")

    sub.add_parser("cron-fetch", help="Fetch and summarize when the hot list changes")
    sub.add_parser("cron-flush", help="Flush queued summaries to Obsidian")
    sub.add_parser("install-crons", help="Register recurring OpenClaw cron jobs")

    args = parser.parse_args()

    if args.command == "once":
        return run_once(force=args.force)
    if args.command == "cron-fetch":
        return run_cron_fetch()
    if args.command == "cron-flush":
        return run_cron_flush()
    if args.command == "install-crons":
        return install_crons()
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("[runner] Interrupted.", file=sys.stderr)
        raise SystemExit(130)
