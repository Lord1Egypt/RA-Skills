"""Phase 7 registry refresh: lifecycle classification test matrix.

Supplements ``scripts/verify_receipt.py --self-test`` (which already covers
the bundled fixtures) with the cases that fixture alone can't exercise:
duplicate-key classification, reserved/unknown/wrong-profile keys, snapshot
hash pinning, and the zero-egress guarantee.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SKILL_ROOT = _HERE.parent
sys.path.insert(0, str(_SKILL_ROOT / "scripts"))

import verify_receipt as vr  # noqa: E402
import registry_snapshot as rs  # noqa: E402

FIXTURES_DIR = _SKILL_ROOT / "fixtures"


def _load(name: str) -> dict:
    with open(FIXTURES_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def test_bundled_snapshot_hash_matches_canonical_registry():
    assert (
        rs.snapshot_sha256()
        == "2da5285f458af9f3369e5baddd953164834d961161c87c9594b823ce251a4f6b"
    )


def test_snapshot_hash_mismatch_fails_closed(tmp_path):
    bogus = tmp_path / "not-a-registry.json"
    bogus.write_text(json.dumps({"keys": [{"kid": "x", "x": "AAAA"}]}))
    snap = rs.RegistrySnapshot(str(bogus))
    import pytest

    with pytest.raises(rs.RegistrySnapshotError):
        snap.verify_pinned_hash()


def test_current_kid05_is_active_current_production_signer():
    receipt = _load("sar-v0.1-current-kid05.json")
    result = vr.verify_receipt(receipt)
    assert result["valid"] is True
    assert result["signer_lifecycle_status"] == "active"
    assert result["trusted_current_production_signer"] is True
    assert result["trusted_historical_signer"] is True


def test_historical_kid03_is_retired_not_active():
    receipt = _load("sar-v0.1-current-kid03.json")
    result = vr.verify_receipt(receipt)
    assert result["valid"] is True
    assert result["signer_lifecycle_status"] == "retired"
    assert result["trusted_current_production_signer"] is False
    assert result["trusted_historical_signer"] is True


def test_kid02_classification_is_documented_non_operational_duplicate():
    snapshot = rs.load_default_snapshot()
    classification = snapshot.classify("sar-prod-ed25519-02")
    assert classification.present is True
    assert classification.is_documented_non_operational_duplicate is True
    assert classification.lifecycle_label == "documented_non_operational_duplicate"
    assert classification.is_current_production_signer is False
    assert classification.is_historically_verifiable is False


def test_reserved_key_not_accepted_as_current_operational_signer():
    snapshot = rs.load_default_snapshot()
    classification = snapshot.classify("sar-prod-ed25519-04")
    assert classification.present is True
    assert classification.lifecycle_label == "reserved"
    assert classification.is_current_production_signer is False


def test_unknown_key_fails_closed():
    receipt = dict(_load("sar-v0.1-current-kid05.json"))
    receipt["verifier_kid"] = "sar-prod-ed25519-99"
    result = vr.verify_receipt(receipt)
    assert result["valid"] is False
    assert any("not found in registry" in e for e in result["errors"])


def test_wrong_profile_key_rejected():
    snapshot = rs.load_default_snapshot()
    classification = snapshot.classify("defaultverifier-recording-ed25519-2")
    assert classification.present is True
    assert classification.profile_ok is False
    assert classification.lifecycle_label == "wrong_profile"


def test_tampered_payload_fails():
    receipt = dict(_load("sar-v0.1-current-kid05.json"))
    receipt["verdict"] = "FAIL"
    result = vr.verify_receipt(receipt)
    assert result["valid"] is False


def test_tampered_signature_fails():
    receipt = dict(_load("sar-v0.1-current-kid05.json"))
    receipt["sig"] = "base64url:" + "Z" * 86
    result = vr.verify_receipt(receipt)
    assert result["valid"] is False


def test_receipt_key_id_mismatch_fails():
    # A receipt whose declared kid doesn't match the key that actually
    # signed it: the signature bytes come from -05 but the receipt claims -03.
    receipt = dict(_load("sar-v0.1-current-kid05.json"))
    receipt["verifier_kid"] = "sar-prod-ed25519-03"
    result = vr.verify_receipt(receipt)
    assert result["valid"] is False


def test_output_reports_snapshot_hash_and_freshness_limitation():
    receipt = _load("sar-v0.1-current-kid05.json")
    result = vr.verify_receipt(receipt)
    assert result["registry_snapshot_sha256"] in result["offline_verification_note"]
    assert "does not confirm the live registry" in result["offline_verification_note"]


def test_verification_makes_no_network_calls():
    import socket

    def _blocked(*_args, **_kwargs):
        raise AssertionError("verify_receipt attempted network access")

    original_socket = socket.socket
    socket.socket = _blocked
    try:
        receipt = _load("sar-v0.1-current-kid05.json")
        result = vr.verify_receipt(receipt)
        assert result["valid"] is True
    finally:
        socket.socket = original_socket


def test_kid02_duplicate_signature_valid_but_never_reported_active():
    # verifier_kid is part of the signed core, so a genuine -02-attributed
    # signature requires actually signing with verifier_kid="sar-prod-
    # ed25519-02" -- no such receipt has ever existed (0 of 553 ledger
    # records reference this kid). Prove the "signature valid but not an
    # independently active signer" path with a fixture-only, clearly-marked
    # test-only duplicate key pair instead of any production private key.
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    from cryptography.hazmat.primitives import serialization

    pub_raw = public_key.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    pub_x = base64.urlsafe_b64encode(pub_raw).rstrip(b"=").decode("ascii")

    fixture_registry = {
        "keys": [
            {
                "kid": "fixture-only-duplicate-primary",
                "kty": "OKP",
                "crv": "Ed25519",
                "x": pub_x,
                "use": "sar_settlement_witness_signing",
                "status": "retired",
            },
            {
                "kid": "fixture-only-duplicate-secondary",
                "kty": "OKP",
                "crv": "Ed25519",
                "x": pub_x,
                "use": "sar_settlement_witness_signing",
                "note": "TEST-ONLY FIXTURE. classification=documented_non_operational_duplicate "
                "(mirrors the real sar-prod-ed25519-02/-03 relationship for test purposes only).",
            },
        ]
    }
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(fixture_registry, f)
        fixture_path = f.name

    try:
        receipt = {
            "sar_version": "0.1",
            "task_id_hash": "sha256:" + "11" * 32,
            "verdict": "PASS",
            "confidence": 1.0,
            "reason_code": "SPEC_MATCH",
            "ts": "2026-07-19T00:00:00.000000Z",
            "verifier_kid": "fixture-only-duplicate-secondary",
        }
        import jcs
        import hashlib

        core = vr._core_without_sig(receipt)
        canonical, digest = vr._digest_for_core(core)
        receipt["receipt_id"] = "sha256:" + hashlib.sha256(canonical).hexdigest()
        signature = private_key.sign(digest)
        receipt["sig"] = "base64url:" + base64.urlsafe_b64encode(signature).rstrip(b"=").decode("ascii")

        result = vr.verify_receipt(receipt, keys_path=fixture_path)
        assert result["valid"] is True
        assert result["signer_lifecycle_status"] == "documented_non_operational_duplicate"
        assert result["trusted_current_production_signer"] is False
        assert result["trusted_historical_signer"] is False
    finally:
        os.unlink(fixture_path)
