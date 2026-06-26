#!/usr/bin/env python3
"""Check whether the local OpenClaw environment can access Agentic Wallet."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path


def onchainos_bin() -> str:
    configured = os.getenv("ONCHAINOS_BIN")
    if configured:
        return configured
    local_bin = Path.home() / ".local" / "bin" / "onchainos"
    if local_bin.exists():
        return str(local_bin)
    return shutil.which("onchainos") or "onchainos"


def run(args: list[str], timeout: int = 10) -> dict:
    try:
        completed = subprocess.run(
            [onchainos_bin(), *args],
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError:
        return {"ok": False, "error": "onchainos CLI not found"}
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"onchainos timed out after {timeout}s"}

    text = "\n".join(part for part in [completed.stdout, completed.stderr] if part).strip()
    return {"ok": completed.returncode == 0, "text": text, "returncode": completed.returncode}


version = run(["--version"])
status = run(["wallet", "status"])

print(json.dumps({
    "onchainos_available": version["ok"],
    "wallet_ready": status["ok"],
    "version": version.get("text", ""),
    "version_error": version.get("error", ""),
    "wallet_status": status.get("text", ""),
    "wallet_error": status.get("error", ""),
    "hint": "" if status["ok"] else "Run `onchainos wallet login` in the same OpenClaw environment, then retry.",
}, indent=2))
