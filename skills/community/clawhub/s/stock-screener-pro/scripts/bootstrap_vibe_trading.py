#!/usr/bin/env python3
"""Install the Vibe-Trading runtime used by stock-screener-pro.

Run manually after installing or updating this Skill. The MCP server never
installs packages while handling a research request.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


VIBE_TRADING_VERSION = "0.1.14"


def main() -> int:
    if sys.version_info < (3, 11):
        print("Python 3.11 or newer is required; rerun this script with that interpreter.", file=sys.stderr)
        return 2

    state_dir = Path(
        os.environ.get(
            "STOCK_SCREENER_STATE_DIR",
            str(Path.home() / ".local" / "share" / "stock-screener-pro"),
        )
    )
    venv_dir = state_dir / "quant-backends" / "vibe-trading"
    venv_python = venv_dir / "bin" / "python"
    vibe_binary = venv_dir / "bin" / "vibe-trading"

    if not venv_python.exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

    subprocess.run(
        [str(venv_python), "-m", "pip", "install", "--upgrade", f"vibe-trading-ai=={VIBE_TRADING_VERSION}"],
        check=True,
    )
    subprocess.run([str(vibe_binary), "--version"], check=True)
    subprocess.run([str(vibe_binary), "alpha", "list", "--limit", "1", "--json"], check=True)
    print(f"Vibe-Trading is ready at {vibe_binary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
