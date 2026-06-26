import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.scoring import choose_action, score_opportunity

__all__ = ["choose_action", "score_opportunity"]
