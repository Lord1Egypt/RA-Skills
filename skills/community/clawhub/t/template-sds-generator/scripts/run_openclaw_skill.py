#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from runtime_common import ensure_base_template, resolve_runtime


def _bootstrap() -> list[str]:
    bootstrap_script = Path(__file__).with_name("bootstrap_runtime.py")
    result = subprocess.run(
        [sys.executable, str(bootstrap_script)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "Unable to provision runtime."
        raise RuntimeError(f"{message}\nRun scripts/runtime_doctor.py for detailed checks.")
    runtime = resolve_runtime()
    if runtime is None:
        raise RuntimeError("No usable Python runtime found after bootstrap. Run scripts/runtime_doctor.py for detailed checks.")
    return runtime


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    runtime = resolve_runtime() or _bootstrap()
    ensure_base_template(runtime)
    generator_script = Path(__file__).with_name("generate_sds.py")
    command = runtime + [str(generator_script), *args]
    completed = subprocess.run(command, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
