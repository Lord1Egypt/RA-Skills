from __future__ import annotations

import json
import subprocess
from pathlib import Path


def call_rust(exe: Path, payload: dict) -> dict:
    p = subprocess.run(
        [str(exe)],
        input=json.dumps(payload, ensure_ascii=False),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        check=False,
        shell=False,
    )
    if p.returncode != 0:
        raise RuntimeError(f"rust exit {p.returncode}: {p.stderr.strip()}")
    return json.loads(p.stdout)


if __name__ == "__main__":
    print(call_rust(Path("target/release/sidecar.exe"), {"hello": "world"}))
