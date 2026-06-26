"""Integration sanity-checks against the shipped bayes_model.json.

Ensures the trained model classifies our three fixture emails as expected.
If these fail, the trainer's inline corpus or the model need tuning.
"""

from pathlib import Path

import pytest

from bin.bayes_classify import classify, load_model
from bin.parse_email import parse_eml

AGENT_ROOT = Path(__file__).parent.parent
FIXTURES = Path(__file__).parent / "fixtures"
MODEL_PATH = AGENT_ROOT / "data" / "bayes_model.json"

pytestmark = pytest.mark.skipif(
    not MODEL_PATH.exists(),
    reason="bayes_model.json not built — run `python -m bin.trainer`",
)


def _body(fname: str) -> str:
    e = parse_eml((FIXTURES / fname).read_bytes())
    return f"{e.subject}\n{e.body_plain}"


def test_benign_scores_low():
    model = load_model(MODEL_PATH)
    score, _ = classify(_body("benign.eml"), model)
    assert score < 0.5, f"benign email scored {score:.2f} (expected < 0.5)"


def test_phish_spoof_scores_high():
    model = load_model(MODEL_PATH)
    score, top = classify(_body("phish_spoof.eml"), model)
    assert score >= 0.70, f"phish spoof scored {score:.2f} (expected >= 0.70)"
    top_tokens = [t for t, _ in top]
    assert any(t in top_tokens for t in ("urgent", "verify")), (
        f"expected urgent/verify in top contributors, got {top_tokens}"
    )


def test_bec_quanta_scores_high():
    model = load_model(MODEL_PATH)
    score, top = classify(_body("bec_quanta.eml"), model)
    assert score >= 0.70, f"Quanta BEC scored {score:.2f} (expected >= 0.70)"
    top_tokens = [t for t, _ in top]
    # famous-case seeding — Quanta must be a strong signal
    assert "quanta" in top_tokens or "wire" in top_tokens or "invoice" in top_tokens, (
        f"expected quanta/wire/invoice in top contributors, got {top_tokens}"
    )
