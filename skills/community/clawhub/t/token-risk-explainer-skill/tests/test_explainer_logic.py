from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from token_risk_explainer import build_risk_factors, calculate_risk_score, explain_token


class _Client:
    def resolve_token(self, chain_id: str, query: str):  # noqa: ARG002
        return {
            "symbol": "TEST",
            "name": "Test",
            "contractAddress": "0xabc",
            "holdersTop10Percent": "88",
            "holdersDevPercent": "11",
            "holdersSniperPercent": "18",
            "holdersInsiderPercent": "9",
            "bundlerHoldingPercent": "25",
            "liquidity": "3000",
        }

    def token_meta(self, chain_id: str, contract_address: str):  # noqa: ARG002
        return {"links": []}

    def token_audit(self, chain_id: str, contract_address: str):  # noqa: ARG002
        return {
            "hasResult": True,
            "isSupported": True,
            "extraInfo": {"buyTax": "12", "sellTax": "12", "isVerified": False},
            "riskItems": [{"details": [{"title": "Honeypot risk", "isHit": True}]}],
        }


def test_build_risk_factors_collects_multiple_flags() -> None:
    token = _Client().resolve_token("56", "TEST")
    audit = _Client().token_audit("56", "0xabc")
    meta = _Client().token_meta("56", "0xabc")
    factors = build_risk_factors(token, audit, meta)
    assert len(factors) >= 5
    assert any(item["code"] == "audit_hits" for item in factors)


def test_calculate_risk_score_high() -> None:
    score = calculate_risk_score(
        [
            {"severity": "high"},
            {"severity": "high"},
            {"severity": "medium"},
        ]
    )
    assert score >= 50


def test_explain_token_returns_display_and_drafts() -> None:
    report = explain_token(_Client(), chain="bsc", query="TEST", lang="zh")
    assert report["display_token"] == "TEST | 0xabc"
    assert report["risk_score"] >= 50
    assert "社群预警" in report["community_alert_draft"]
