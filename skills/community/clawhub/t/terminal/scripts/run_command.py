#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_history, save_history
from lib.safety import risk_level, requires_confirmation, redact_sensitive

def append_history(command, cwd, risk, returncode, stdout, stderr, status, store_output=True):
    history = load_history()

    safe_command = redact_sensitive(command)
    safe_stdout = redact_sensitive(stdout) if store_output else ""
    safe_stderr = redact_sensitive(stderr) if store_output else "[output not stored]"

    history["runs"].append({
        "timestamp": datetime.now().isoformat(),
        "command": safe_command,
        "cwd": os.path.abspath(cwd),
        "risk": risk,
        "status": status,
        "returncode": returncode,
        "stdout": safe_stdout[-4000:],
        "stderr": safe_stderr[-4000:]
    })
    save_history(history)

def maybe_redact(text, enabled):
    if not enabled:
        return text
    return redact_sensitive(text)

def main():
    parser = argparse.ArgumentParser(description="Run a local shell command with safety checks")
    parser.add_argument("--command", required=True, help="Shell command to run")
    parser.add_argument("--cwd", default=".", help="Working directory")
    parser.add_argument("--yes", action="store_true", help="Confirm high-risk execution")
    parser.add_argument("--preview", action="store_true", help="Preview command without executing")
    parser.add_argument("--no-store-output", action="store_true", help="Do not store stdout/stderr in history")
    parser.add_argument("--redact-display", action="store_true", help="Redact sensitive-looking values in displayed stdout/stderr")
    args = parser.parse_args()

    risk = risk_level(args.command)

    if args.preview:
        print("Preview only. Command not executed.")
        print(f"Command: {maybe_redact(args.command, args.redact_display)}")
        print(f"CWD: {os.path.abspath(args.cwd)}")
        print(f"Risk: {risk}")
        append_history(
            args.command,
            args.cwd,
            risk,
            0,
            "",
            "preview-only",
            "previewed",
            store_output=not args.no_store_output
        )
        return

    if requires_confirmation(args.command) and not args.yes:
        message = "Blocked: high-risk command requires explicit confirmation with --yes"
        print(message)
        print(f"Risk level: {risk}")
        append_history(
            args.command,
            args.cwd,
            risk,
            2,
            "",
            message,
            "blocked",
            store_output=not args.no_store_output
        )
        sys.exit(2)

    try:
        completed = subprocess.run(
            args.command,
            shell=True,
            cwd=args.cwd,
            text=True,
            capture_output=True
        )
    except Exception as e:
        append_history(
            args.command,
            args.cwd,
            risk,
            1,
            "",
            f"Execution failed: {e}",
            "failed",
            store_output=not args.no_store_output
        )
        print(f"Execution failed: {e}")
        sys.exit(1)

    append_history(
        args.command,
        args.cwd,
        risk,
        completed.returncode,
        completed.stdout,
        completed.stderr,
        "executed",
        store_output=not args.no_store_output
    )

    display_command = maybe_redact(args.command, args.redact_display)
    display_stdout = maybe_redact(completed.stdout, args.redact_display)
    display_stderr = maybe_redact(completed.stderr, args.redact_display)

    print(f"Command: {display_command}")
    print(f"Risk: {risk}")
    print(f"Return code: {completed.returncode}")
    print("--- STDOUT ---")
    print(display_stdout.rstrip() or "(empty)")
    print("--- STDERR ---")
    print(display_stderr.rstrip() or "(empty)")

    sys.exit(completed.returncode)

if __name__ == "__main__":
    main()
