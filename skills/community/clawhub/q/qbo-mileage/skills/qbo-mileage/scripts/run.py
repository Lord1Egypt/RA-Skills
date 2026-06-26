"""Entry point for the qbo-mileage skill.

Adds the plugin's src/ folder to sys.path so the CLI works straight from an
installed plugin folder without requiring `pip install`. This file lives at
<plugin root>/skills/qbo-mileage/scripts/run.py and the package lives at
<plugin root>/src/qbo_mileage.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[3] / "src"
if _SRC.is_dir() and str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from qbo_mileage.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
