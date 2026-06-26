import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from merge_evaluations import merge, _classify_severity


def test_agreed_recommendations_boost_confidence() -> None:
    a = [{"target": "skills/x", "type": "refactor", "title": "trim x", "confidence": 0.75}]
    b = [{"target": "skills/x", "type": "refactor", "title": "trim x", "confidence": 0.8}]
    result = merge(a, b)
    assert len(result) == 1
    assert result[0]["confidence"] == 0.9  # 0.8 + 0.1
    assert len(result[0]["agreed_by"]) == 2


def test_low_confidence_filtered_out() -> None:
    a = [{"target": "skills/y", "type": "refactor", "title": "maybe", "confidence": 0.3}]
    b = []
    result = merge(a, b, confidence_threshold=0.7)
    assert len(result) == 0


def test_severity_classification() -> None:
    assert _classify_severity(0.9) == "green"
    assert _classify_severity(0.85) == "green"
    assert _classify_severity(0.75) == "yellow"
    assert _classify_severity(0.7) == "yellow"
    assert _classify_severity(0.5) == "red"


def test_unique_recommendations_kept() -> None:
    a = [{"target": "skills/a", "type": "refactor", "title": "a", "confidence": 0.8}]
    b = [{"target": "skills/b", "type": "new-skill", "title": "b", "confidence": 0.75}]
    result = merge(a, b)
    assert len(result) == 2
