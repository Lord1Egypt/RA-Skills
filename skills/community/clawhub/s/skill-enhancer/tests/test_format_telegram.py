import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from format_telegram import format_digest


def test_empty_recommendations() -> None:
    msg = format_digest([])
    assert "No strong recommendations" in msg


def test_basic_format() -> None:
    recs = [
        {"severity": "green", "title": "trim skill X", "proposed_action": "remove 40 lines"},
        {"severity": "yellow", "title": "new skill idea"},
    ]
    msg = format_digest(recs)
    assert "🟢" in msg
    assert "🟡" in msg
    assert "trim skill X" in msg
    assert "remove 40 lines" in msg


def test_truncation() -> None:
    recs = [{"severity": "green", "title": f"rec {i}", "proposed_action": "x" * 200} for i in range(50)]
    msg = format_digest(recs, max_chars=500)
    assert len(msg) <= 500
    assert "truncated" in msg


def test_no_red_section_when_empty() -> None:
    recs = [{"severity": "green", "title": "only green"}]
    msg = format_digest(recs)
    assert "🔴" not in msg
