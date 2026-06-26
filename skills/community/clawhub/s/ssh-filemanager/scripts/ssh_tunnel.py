#!/usr/bin/env python3
"""Tailnet SSH tunnel helper — connection checks over Tailscale SSH."""

import argparse
import json
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Tailnet SSH Tunnel Helper")
    parser.add_argument("--host", required=True, help="Tailscale hostname or IP")
    args = parser.parse_args()

    cmd = [
        "ssh",
        "-o", "BatchMode=yes",
        "-o", "ConnectTimeout=5",
        "-o", "StrictHostKeyChecking=accept-new",
        args.host,
        "echo tailnet-ssh-ok",
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and "tailnet-ssh-ok" in result.stdout:
            print(json.dumps({
                "success": True,
                "reachable": True,
                "host": args.host,
            }))
        else:
            print(json.dumps({
                "success": False,
                "reachable": False,
                "host": args.host,
                "error": result.stderr.strip() or result.stdout.strip(),
            }))
            sys.exit(1)
    except subprocess.TimeoutExpired:
        print(json.dumps({
            "success": False,
            "reachable": False,
            "host": args.host,
            "error": "SSH connection timed out",
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "reachable": False,
            "host": args.host,
            "error": str(e),
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
