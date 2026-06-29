#!/usr/bin/env python3
"""
selfheal.py — bounded diagnose-and-retry wrapper for a failing command.

Usage:
    python3 selfheal.py [--max-retries N] [--timeout SECONDS] -- <command> [args...]

This wrapper does NOT silently rewrite your code, install packages, or
escalate privileges. It runs your command, captures the failure, classifies
the likely cause, logs the attempt, and lets you (or the agent) decide the
next concrete action. It refuses to run obviously destructive commands.
"""
import sys
import subprocess
import time
import json
import os
import shlex
import re
from datetime import datetime, timezone

DESTRUCTIVE_PATTERNS = [
    r"\brm\s+-rf\s+/(\s|$)",
    r"\brm\s+-rf\s+\*",
    r"\bmkfs\b",
    r"\bdd\s+if=.*of=/dev/",
    r":\(\)\{.*\}.*:",   # classic fork bomb shape
    r"\bshutdown\b",
    r"\breboot\b",
    r">\s*/dev/sd[a-z]",
]

LOG_FILE = "selfheal_log.jsonl"


def is_destructive(cmd_str: str) -> bool:
    return any(re.search(p, cmd_str, re.I) for p in DESTRUCTIVE_PATTERNS)


def classify_failure(stderr: str, exit_code: int) -> str:
    s = stderr.lower()
    if "permission denied" in s:
        return "permission"
    if "no such file or directory" in s:
        return "missing_path_or_file"
    if "command not found" in s or "is not recognized" in s:
        return "missing_dependency"
    if "modulenotfounderror" in s or "importerror" in s:
        return "missing_python_dependency"
    if "syntaxerror" in s:
        return "syntax_error"
    if "connection refused" in s or "timed out" in s or "network is unreachable" in s:
        return "network"
    if "address already in use" in s:
        return "port_conflict"
    if exit_code == 124:
        return "timeout"
    return "unknown"


def log_attempt(record: dict):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass  # logging must never crash the wrapper


def run_once(cmd_list, timeout):
    start = time.time()
    try:
        proc = subprocess.run(
            cmd_list,
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        duration = round(time.time() - start, 2)
        return proc.returncode, proc.stdout, proc.stderr, duration
    except subprocess.TimeoutExpired as e:
        duration = round(time.time() - start, 2)
        return 124, e.stdout or "", (e.stderr or "") + "\n[selfheal] timed out", duration


def main():
    args = sys.argv[1:]
    max_retries = 3
    timeout = 30

    i = 0
    while i < len(args):
        if args[i] == "--max-retries":
            max_retries = int(args[i + 1])
            del args[i:i + 2]
        elif args[i] == "--timeout":
            timeout = int(args[i + 1])
            del args[i:i + 2]
        elif args[i] == "--":
            del args[i]
            break
        else:
            i += 1

    if not args:
        print(json.dumps({"error": "usage: selfheal.py [--max-retries N] [--timeout S] -- <cmd> [args...]"}))
        sys.exit(1)

    cmd_str = " ".join(shlex.quote(a) for a in args)
    if is_destructive(cmd_str):
        print(json.dumps({
            "error": "refused: command matches a destructive pattern and will not be run.",
            "command": cmd_str,
        }))
        sys.exit(2)

    attempt = 0
    while attempt < max_retries:
        attempt += 1
        exit_code, stdout, stderr, duration = run_once(args, timeout)

        record = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "attempt": attempt,
            "command": cmd_str,
            "exit_code": exit_code,
            "duration_s": duration,
            "stdout_tail": stdout[-500:],
            "stderr_tail": stderr[-500:],
        }
        log_attempt(record)

        if exit_code == 0:
            print(json.dumps({
                "status": "success",
                "attempt": attempt,
                "duration_s": duration,
                "stdout": stdout,
            }, indent=2))
            sys.exit(0)

        cause = classify_failure(stderr, exit_code)
        print(json.dumps({
            "status": "failed",
            "attempt": attempt,
            "exit_code": exit_code,
            "duration_s": duration,
            "likely_cause": cause,
            "stderr_tail": stderr[-1000:],
            "note": "selfheal does not auto-fix code. Diagnose the cause above, "
                    "propose a concrete fix, then re-run explicitly.",
        }, indent=2))

        if attempt >= max_retries:
            print(json.dumps({
                "status": "retry_budget_exhausted",
                "attempts": attempt,
                "advice": "Stop retrying the same command. A human or the agent "
                          "must change something before trying again.",
            }))
            sys.exit(1)


if __name__ == "__main__":
    main()
