"""Shared test fixtures and path setup.

Adds the skill root to sys.path so `import scripts.X` works, mirroring how
the skill is invoked from its own dir at runtime (e.g. `python -m scripts.search`).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def load_fixture(name: str) -> dict:
    with (FIXTURES / name).open("r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def fixture():
    """Returns a loader callable: fixture('search.json') -> dict."""
    return load_fixture
