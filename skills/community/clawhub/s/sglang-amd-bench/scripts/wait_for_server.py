#!/usr/bin/env python3
"""Poll an sglang server log until it becomes ready, fails, or hangs.

Designed to be invoked by an agent right after launching an sglang server in
the background. Replaces blind `sleep 300` waits with an active monitor that
returns as soon as the outcome is known.

Outcomes (process exit code + final stdout line):
    0  READY    — saw the success marker "The server is fired up and ready to roll"
    1  CRASHED  — saw the failure marker (default: "Traceback")
    2  HUNG     — log file's last line + line count did not change for the
                  configured stall window (default: 5 minutes)
    3  TIMEOUT  — overall timeout reached without any of the above
    4  ERROR    — log file never appeared / unreadable

Usage:
    python wait_for_server.py <server.log> \\
        [--success "The server is fired up and ready to roll"] \\
        [--failure "Traceback"] \\
        [--stall-seconds 300] \\
        [--poll-seconds 5] \\
        [--overall-timeout 1800]

Outputs progress lines to stdout (one per poll where state changes), and a
final single-word status line: READY / CRASHED / HUNG / TIMEOUT / ERROR.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


def tail_signature(path: Path) -> tuple[int, str] | None:
    """Return (line_count, last_non_empty_line) or None if unreadable."""
    try:
        with path.open("rb") as f:
            data = f.read()
    except OSError:
        return None
    if not data:
        return (0, "")
    lines = data.splitlines()
    last = ""
    for ln in reversed(lines):
        s = ln.decode("utf-8", errors="replace").rstrip()
        if s:
            last = s
            break
    return (len(lines), last)


def scan_for_markers(path: Path, success: str, failure: str) -> str | None:
    """Return 'READY', 'CRASHED', or None."""
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if success in line:
                    return "READY"
                if failure in line:
                    return "CRASHED"
    except OSError:
        return None
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("log", type=Path, help="Path to the sglang server log file")
    ap.add_argument(
        "--success",
        default="The server is fired up and ready to roll",
        help="Substring marking successful startup",
    )
    ap.add_argument(
        "--failure",
        default="Traceback",
        help="Substring marking a fatal error",
    )
    ap.add_argument(
        "--stall-seconds",
        type=float,
        default=300.0,
        help="If the log's last line + line count are unchanged for this many seconds, treat as HUNG",
    )
    ap.add_argument(
        "--poll-seconds",
        type=float,
        default=5.0,
        help="Polling interval",
    )
    ap.add_argument(
        "--overall-timeout",
        type=float,
        default=1800.0,
        help="Hard upper bound on total wait time",
    )
    ap.add_argument(
        "--wait-for-file-seconds",
        type=float,
        default=60.0,
        help="How long to wait for the log file to appear before giving up",
    )
    args = ap.parse_args()

    log_path: Path = args.log
    started = time.monotonic()

    # 1. Wait for the file to appear.
    while not log_path.exists():
        if time.monotonic() - started > args.wait_for_file_seconds:
            print(f"[wait_for_server] log file never appeared: {log_path}", file=sys.stderr)
            print("ERROR")
            return 4
        time.sleep(min(args.poll_seconds, 2.0))

    last_sig: tuple[int, str] | None = None
    last_change_at = time.monotonic()
    last_reported_lines = -1

    while True:
        now = time.monotonic()
        elapsed = now - started

        if elapsed > args.overall_timeout:
            print(f"[wait_for_server] overall timeout {args.overall_timeout:.0f}s exceeded", file=sys.stderr)
            print("TIMEOUT")
            return 3

        marker = scan_for_markers(log_path, args.success, args.failure)
        if marker == "READY":
            print(f"[wait_for_server] success marker found after {elapsed:.0f}s")
            print("READY")
            return 0
        if marker == "CRASHED":
            print(f"[wait_for_server] failure marker found after {elapsed:.0f}s", file=sys.stderr)
            print("CRASHED")
            return 1

        sig = tail_signature(log_path)
        if sig is None:
            print(f"[wait_for_server] log unreadable: {log_path}", file=sys.stderr)
            print("ERROR")
            return 4

        if sig != last_sig:
            last_sig = sig
            last_change_at = now
            if sig[0] != last_reported_lines:
                last_reported_lines = sig[0]
                preview = sig[1][:200]
                print(f"[wait_for_server] t={elapsed:6.0f}s lines={sig[0]:>6d} last={preview!r}")
        else:
            stalled_for = now - last_change_at
            if stalled_for >= args.stall_seconds:
                print(
                    f"[wait_for_server] log stalled for {stalled_for:.0f}s "
                    f"(last line #{sig[0]}: {sig[1][:200]!r})",
                    file=sys.stderr,
                )
                print("HUNG")
                return 2

        time.sleep(args.poll_seconds)


if __name__ == "__main__":
    sys.exit(main())
