import os
import sys
from pathlib import Path

# Ensure 'scripts' directory is importable in tests
ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
