"""Run as ``python3 <path>/tn_assist <command>`` or ``python3 -m tn_assist <command>``."""

from __future__ import annotations

import sys
from pathlib import Path

# Running the folder puts the folder itself on sys.path, not its parent where the package lives.
_PARENT = str(Path(__file__).resolve().parent.parent)
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from tn_assist.cli import main  # noqa: E402

sys.exit(main())
