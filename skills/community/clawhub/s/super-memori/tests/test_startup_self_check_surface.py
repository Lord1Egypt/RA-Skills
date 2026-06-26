#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    proc = subprocess.run(
        ["./startup-self-check.sh", "--json", "--no-repair"],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
    )
    if proc.returncode not in {0, 2, 3}:
        raise SystemExit(f"unexpected startup-self-check exit code: {proc.returncode}\nstdout={proc.stdout}\nstderr={proc.stderr}")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"startup-self-check did not return JSON: {exc}\nstdout={proc.stdout}\nstderr={proc.stderr}")

    required = ["health_before", "health_after", "final_status", "repair_enabled", "repair_attempted", "summary"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise SystemExit(f"startup-self-check missing keys: {missing}")

    final_status = payload.get("final_status")
    if final_status not in {"OK", "WARN", "FAIL"}:
        raise SystemExit(f"unexpected final_status: {final_status}")

    before_payload = (payload.get("health_before") or {}).get("payload") or {}
    after_payload = (payload.get("health_after") or {}).get("payload") or {}
    for side_name, side_payload in {"before": before_payload, "after": after_payload}.items():
        if side_payload and side_payload.get("status") not in {"OK", "WARN", "FAIL"}:
            raise SystemExit(f"unexpected health status in {side_name}: {side_payload.get('status')}")

    print("[OK] startup self-check surface passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
