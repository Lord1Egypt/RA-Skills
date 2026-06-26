from __future__ import annotations

from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
REFERENCES_DIR = SKILL_DIR / "references"
DIST_DIR = SKILL_DIR / "dist"
TESTS_DIR = SKILL_DIR / "tests"
WATCH_STATE_FILE = DATA_DIR / "watch-rules.json"

for _path in (DATA_DIR, REFERENCES_DIR, DIST_DIR, TESTS_DIR):
    _path.mkdir(parents=True, exist_ok=True)
