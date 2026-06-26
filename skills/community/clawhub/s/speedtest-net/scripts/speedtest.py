#!/usr/bin/env python3
"""Network speedtest wrapper using speedtest-cli."""

import argparse
import json
import subprocess
import sys
import shutil


def find_speedtest_cli():
    """Locate speedtest-cli binary."""
    path = shutil.which("speedtest-cli")
    if not path:
        print(
            "Error: speedtest-cli not found.\n"
            "Install it manually: pip3 install speedtest-cli\n"
            "See setup.md for details.",
            file=sys.stderr,
        )
        sys.exit(1)
    return path


def run_speedtest(server=None, timeout=120):
    """Run speedtest-cli and return plain text output."""
    cli = find_speedtest_cli()
    cmd = [cli, "--simple", "--timeout", str(timeout)]
    if server:
        cmd.extend(["--server", str(server)])

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 10)

    if proc.returncode != 0:
        print(f"speedtest failed (exit {proc.returncode}):\n{proc.stderr}", file=sys.stderr)
        sys.exit(1)

    return proc.stdout.strip()


def run_speedtest_json(server=None, timeout=120):
    """Run speedtest-cli with JSON output."""
    cli = find_speedtest_cli()
    cmd = [cli, "--json", "--timeout", str(timeout)]
    if server:
        cmd.extend(["--server", str(server)])

    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 10)

    if proc.returncode != 0:
        print(f"speedtest failed (exit {proc.returncode}):\n{proc.stderr}", file=sys.stderr)
        sys.exit(1)

    return json.loads(proc.stdout)


def main():
    parser = argparse.ArgumentParser(description="Run network speedtest")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--server", type=str, default=None, help="Force server ID")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout in seconds")
    args = parser.parse_args()

    if args.json:
        data = run_speedtest_json(server=args.server, timeout=args.timeout)
        print(json.dumps(data, indent=2))
    else:
        output = run_speedtest(server=args.server, timeout=args.timeout)
        print(output)


if __name__ == "__main__":
    main()
