#!/usr/bin/env python3
"""Run the tgwidget CLI from the skill folder without installing anything.

    python3 scripts/widget.py check widget.html
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tgwidget.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
