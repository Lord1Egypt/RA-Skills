#!/usr/bin/env python3
"""Unified Salesflare CLI wrapper.

Examples:
  python scripts/sf.py discover --contains opportunities
  python scripts/sf.py get --path /accounts --query limit=5
  python scripts/sf.py smoketest
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print(
            "Usage: python scripts/sf.py "
            "{discover|request|get|post|put|patch|delete|smoketest} [args...]",
            file=sys.stderr,
        )
        return 2

    command = sys.argv[1].lower()
    rest = sys.argv[2:]
    scripts_dir = Path(__file__).resolve().parent

    if command == "discover":
        target = scripts_dir / "sf_discover.py"
        args = rest
    elif command == "request":
        target = scripts_dir / "sf_request.py"
        args = rest
    elif command == "smoketest":
        target = scripts_dir / "sf_smoketest.py"
        args = rest
    elif command in {"get", "post", "put", "patch", "delete"}:
        target = scripts_dir / "sf_request.py"
        args = ["--method", command.upper(), *rest]
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        return 2

    return subprocess.call([sys.executable, str(target), *args])


if __name__ == "__main__":
    raise SystemExit(main())
