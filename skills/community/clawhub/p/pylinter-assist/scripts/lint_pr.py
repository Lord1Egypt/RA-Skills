#!/usr/bin/env python3
"""
Convenience entry point — runnable directly after activating the project venv.

Usage (activate venv first):
  source .venv/bin/activate
  python scripts/lint_pr.py pr 42
  python scripts/lint_pr.py staged --format text
  python scripts/lint_pr.py files src/ --format markdown
  python scripts/lint_pr.py diff changes.patch --config .linting-rules.yml

Or after `pip install -e .`:
  lint-pr pr 42
"""

import sys
from pathlib import Path

# Allow running from repo root without installation
sys.path.insert(0, str(Path(__file__).parent.parent))

from pylinter_assist.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
