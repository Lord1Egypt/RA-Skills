"""Run a compact Agent Pulse usage snapshot."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys


def command_base() -> list[str]:
    if shutil.which("agent-pulse"):
        return ["agent-pulse"]
    return [sys.executable, "-m", "agent_pulse.cli"]


def run(args: list[str], timeout: int) -> dict:
    env = os.environ.copy()
    env.setdefault("PYTHONUTF8", "1")
    env.setdefault("PYTHONIOENCODING", "utf-8")
    cmd = command_base() + args
    try:
        proc = subprocess.run(
            cmd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raw_output = (exc.stdout or "").strip() if isinstance(exc.stdout, str) else ""
        return {
            "command": " ".join(cmd),
            "exit_code": None,
            "timed_out": True,
            "timeout_seconds": timeout,
            "output": raw_output or f"Command timed out after {timeout} seconds.",
        }

    raw = proc.stdout.strip()
    parsed = None
    if raw:
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = raw
    return {"command": " ".join(cmd), "exit_code": proc.returncode, "timed_out": False, "output": parsed}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a compact Agent Pulse JSON snapshot.")
    parser.add_argument("--hours", type=int, default=24, help="Recent activity window in hours.")
    parser.add_argument("--days", type=int, default=7, help="Trend/insight window in days.")
    parser.add_argument("--limit", type=int, default=10, help="Top-session limit.")
    parser.add_argument(
        "--command-timeout",
        type=int,
        default=20,
        help="Timeout in seconds for each Agent Pulse subcommand.",
    )
    args = parser.parse_args()

    hours = str(args.hours)
    days = str(args.days)
    limit = str(args.limit)
    trend_hours = str(args.days * 24)
    timeout = args.command_timeout

    snapshot = {
        "doctor": run(["doctor", "--json"], timeout),
        f"status_{args.hours}h": run(["status", "--json", "--hours", hours], timeout),
        "top_cost": run(
            ["top", "--sort", "cost", "--json", "--hours", trend_hours, "--limit", limit],
            timeout,
        ),
        "models": run(["models", "--json", "--hours", trend_hours], timeout),
        "leaderboard": run(["leaderboard", "--json", "--hours", trend_hours], timeout),
        "forecast": run(["forecast", "--json", "--days", days], timeout),
        "health": run(["health", "--json"], timeout),
        "score": run(["score", "--json", "--hours", trend_hours], timeout),
        "budget": run(["budget", "--json"], timeout),
        "insights": run(["insights", "--json", "--days", days], timeout),
    }
    print(json.dumps(snapshot, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
