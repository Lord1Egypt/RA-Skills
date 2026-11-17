from __future__ import annotations

import pytest


def normalize(s: str) -> str:
    v = s.strip().lower()
    if not v:
        raise ValueError("empty")
    return v


def test_normalize() -> None:
    assert normalize("  Hello ") == "hello"


@pytest.mark.parametrize("bad", ["", "   "])
def test_empty(bad: str) -> None:
    with pytest.raises(ValueError):
        normalize(bad)
