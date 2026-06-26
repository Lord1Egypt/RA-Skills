#!/usr/bin/env python3
from __future__ import annotations

import sys

from runtime_common import create_or_repair_venv, ensure_base_template, ensure_pip, install_requirements, runtime_complete, venv_python


def main() -> int:
    create_or_repair_venv()
    runtime = venv_python()
    ensure_pip(runtime)
    if not runtime_complete(runtime):
        install_requirements(runtime)
    ensure_base_template(runtime)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
