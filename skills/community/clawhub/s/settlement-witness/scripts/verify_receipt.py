#!/usr/bin/env python3
"""
verify_receipt.py — Local-first SAR v0.1 receipt verifier for SettlementWitness.

Verifies a signed SAR v0.1 settlement receipt entirely OFFLINE. It makes NO
network calls and does NOT contact defaultverifier.com or any other host. All it
needs is the receipt and the bundled public key registry (keys/sar-keys.json).

What it does (ported from the DefaultVerifier verification path, verify-only):
  1. Parse a SAR v0.1 receipt JSON file.
  2. Extract the signed core fields (task_id_hash, verdict, confidence,
     reason_code, ts, verifier_kid, and optional counterparty).
  3. Canonicalize the core with RFC 8785 / JCS (same rule the issuer signs).
  4. Recompute the SHA-256 digest of the canonical bytes.
  5. Verify receipt_id == "sha256:" + hex(digest).
  6. Verify the Ed25519 signature over the digest bytes using the public key
     selected by verifier_kid from the bundled registry.
  7. Emit a typed JSON result.

This tool NEVER signs receipts and contains no private-key material. Signing
stays server-side with DefaultVerifier by design; this side only verifies.

Dependencies (both pure-verification, no network):
  - jcs           (RFC 8785 JSON Canonicalization Scheme)
  - cryptography  (Ed25519 signature verification)

Usage:
  python3 scripts/verify_receipt.py <receipt.json>
  python3 scripts/verify_receipt.py --self-test
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import jcs
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

import registry_snapshot as _registry_snapshot

# Signed-core field set for SAR v0.1. Mirrors _sar_core_without_sig in
# settlement_witness_v0.py. Only these fields are canonicalized and signed;
# everything else in a receipt (sar_version, notes, attribution, etc.) is
# non-core and MUST NOT affect the digest.
_CORE_REQUIRED = ("task_id_hash", "verdict", "confidence", "reason_code", "ts", "verifier_kid")

_HERE = os.path.dirname(os.path.abspath(__file__))
_SKILL_ROOT = os.path.dirname(_HERE)
_DEFAULT_KEYS_PATH = os.path.join(_SKILL_ROOT, "keys", "sar-keys.json")

_FIXTURE_EXPECTATIONS = [
    ("sar-v0.1-pass.json", True),
    ("sar-v0.1-fail.json", True),
    ("sar-v0.1-indeterminate.json", True),
    ("sar-v0.1-current-kid03.json", True),
    ("sar-v0.1-current-kid05.json", True),
    ("tampered-receipt.json", False),
]


def _b64url_decode_flexible(s: str) -> bytes:
    """Ported from settlement_witness_v0.py — tolerant base64url decode."""
    s = (s or "").strip()
    pad = (-len(s)) % 4
    return base64.urlsafe_b64decode((s + ("=" * pad)).encode("utf-8"))


def _load_snapshot(keys_path: str) -> "_registry_snapshot.RegistrySnapshot":
    """Load the lifecycle-aware registry snapshot for ``keys_path``.

    When ``keys_path`` is the bundled default, the pinned SHA-256 is
    enforced (fail closed on mismatch). A caller-supplied override path
    (``SAR_KEYS_REGISTRY_PATH`` / explicit argument) is loaded as-is, since
    it is intentionally not expected to match the bundled snapshot's hash.
    """
    if os.path.abspath(keys_path) == os.path.abspath(_DEFAULT_KEYS_PATH):
        snap = _registry_snapshot.RegistrySnapshot(keys_path)
        snap.verify_pinned_hash()
        return snap
    return _registry_snapshot.RegistrySnapshot(keys_path)


def _get_public_key_for_kid(
    verifier_kid: str, keys_path: str
) -> tuple[Ed25519PublicKey, "_registry_snapshot.KeyClassification", "_registry_snapshot.RegistrySnapshot"]:
    """Resolve the trusted public key and lifecycle classification for a kid.

    Only keys registered for the SAR settlement-witness signing profile are
    accepted here (``registry_snapshot.SAR_SETTLEMENT_WITNESS_USE``, or the
    three legacy pre-``use``-field kids) — a key from a different profile
    (e.g. SAR-402 recording attribution) is never trusted for a SAR v0.1
    settlement-witness receipt regardless of its own lifecycle status.
    """
    snapshot = _load_snapshot(keys_path)
    classification = snapshot.classify(verifier_kid)
    if not classification.present:
        raise RuntimeError(f"verifier_kid not found in registry: {verifier_kid}")
    if not classification.profile_ok:
        raise RuntimeError(
            f"verifier_kid {verifier_kid} is registered for a different signing "
            f"profile ({classification.use!r}), not sar_settlement_witness_signing"
        )
    pub_bytes = snapshot.get_public_key_bytes(verifier_kid)
    if pub_bytes is None:
        raise RuntimeError("registry key missing usable public key bytes")
    if len(pub_bytes) != 32:
        raise RuntimeError(
            f"invalid Ed25519 public key length: {len(pub_bytes)} bytes (expected 32)"
        )
    return Ed25519PublicKey.from_public_bytes(pub_bytes), classification, snapshot


def _core_without_sig(receipt: Dict[str, Any]) -> dict:
    """Ported from _sar_core_without_sig — build signed core from a receipt."""
    core = {
        "task_id_hash": receipt.get("task_id_hash"),
        "verdict": receipt.get("verdict"),
        "confidence": receipt.get("confidence"),
        "reason_code": receipt.get("reason_code"),
        "ts": receipt.get("ts"),
        "verifier_kid": receipt.get("verifier_kid"),
    }
    counterparty = receipt.get("counterparty")
    if isinstance(counterparty, str) and counterparty.strip():
        core["counterparty"] = counterparty.strip()
    return core


def _digest_for_core(core: dict) -> Tuple[bytes, bytes]:
    """Ported from _sar_digest_for_core — (canonical_bytes, sha256 digest bytes)."""
    canonical = jcs.canonicalize(core)  # RFC 8785 (bytes)
    digest = hashlib.sha256(canonical).digest()
    return canonical, digest


def verify_receipt(receipt: Dict[str, Any], keys_path: str = _DEFAULT_KEYS_PATH) -> Dict[str, Any]:
    """
    Verify a SAR v0.1 receipt fully offline.

    Returns a typed result:
      {
        "valid": bool,
        "receipt_id": str | None,
        "kid": str | None,
        "verdict": str | None,     # honest verdict from the receipt (PASS/FAIL/INDETERMINATE)
        "errors": [str, ...]
      }

    Note: a FAIL or INDETERMINATE verdict is still a cryptographically VALID
    receipt. "valid" here means "the signature and digest check out", never
    "the verdict was PASS".
    """
    errors: List[str] = []
    rid = receipt.get("receipt_id") if isinstance(receipt, dict) else None
    kid = receipt.get("verifier_kid") if isinstance(receipt, dict) else None
    verdict = receipt.get("verdict") if isinstance(receipt, dict) else None
    lifecycle: Dict[str, Any] = {
        "signer_lifecycle_status": None,
        "trusted_current_production_signer": False,
        "trusted_historical_signer": False,
        "registry_snapshot_sha256": None,
        "offline_verification_note": None,
    }

    def result() -> Dict[str, Any]:
        return {
            "valid": len(errors) == 0,
            "receipt_id": rid,
            "kid": kid,
            "verdict": verdict,
            "errors": errors,
            **lifecycle,
        }

    if not isinstance(receipt, dict):
        errors.append("receipt is not a JSON object")
        return result()

    sig = receipt.get("sig")

    # Structural / prefix rules (ported from _sar_verify_receipt_v0_1).
    if not (isinstance(rid, str) and rid.startswith("sha256:")):
        errors.append("receipt_id missing required 'sha256:' prefix")
    if not (isinstance(sig, str) and sig.startswith("base64url:")):
        errors.append("sig missing required 'base64url:' prefix")
    if not (isinstance(kid, str) and kid.strip()):
        errors.append("verifier_kid missing")
    for field in _CORE_REQUIRED:
        if receipt.get(field) is None:
            errors.append(f"missing required core field: {field}")
    if errors:
        return result()

    # Recompute canonical digest from the signed core only.
    core = _core_without_sig(receipt)
    try:
        canonical, digest = _digest_for_core(core)
    except Exception as e:
        errors.append(f"canonicalization failed: {e}")
        return result()

    expected_rid = "sha256:" + hashlib.sha256(canonical).hexdigest()
    if rid != expected_rid:
        errors.append(f"receipt_id does not match canonical digest (expected {expected_rid})")

    # Ed25519 signature over the digest bytes.
    try:
        sig_bytes = _b64url_decode_flexible(sig.split(":", 1)[1])
        pub, classification, snapshot = _get_public_key_for_kid(kid.strip(), keys_path)
        lifecycle["signer_lifecycle_status"] = classification.lifecycle_label
        lifecycle["trusted_current_production_signer"] = classification.is_current_production_signer
        lifecycle["trusted_historical_signer"] = classification.is_historically_verifiable
        lifecycle["registry_snapshot_sha256"] = snapshot.raw_sha256
        lifecycle["offline_verification_note"] = (
            "Verified offline against the bundled registry snapshot "
            f"(sha256:{snapshot.raw_sha256}, source {_registry_snapshot.SNAPSHOT_SOURCE}, "
            f"dated {_registry_snapshot.SNAPSHOT_DATE}). This confirms the receipt "
            "against that pinned snapshot only; it does not confirm the live "
            "registry's current freshness."
        )
        pub.verify(sig_bytes, digest)
    except Exception as e:
        errors.append(f"signature verification failed: {e}")

    return result()


def _run_self_test(keys_path: str = _DEFAULT_KEYS_PATH) -> int:
    fixtures_dir = os.path.join(_SKILL_ROOT, "fixtures")
    all_ok = True
    lines: List[str] = []
    for name, expect_valid in _FIXTURE_EXPECTATIONS:
        path = os.path.join(fixtures_dir, name)
        try:
            with open(path, "r", encoding="utf-8") as f:
                receipt = json.load(f)
            res = verify_receipt(receipt, keys_path)
            got_valid = res["valid"]
        except Exception as e:
            got_valid = None
            res = {"errors": [f"could not load/verify: {e}"]}
        label = "valid" if got_valid else "invalid"
        ok = (got_valid is True) == expect_valid
        all_ok = all_ok and ok
        status = "OK" if ok else "MISMATCH"
        detail = "" if ok else f"  (expected {'valid' if expect_valid else 'invalid'})"
        lines.append(f"{name}: {label}  [{status}]{detail}")
        if got_valid is not True and res.get("errors"):
            for err in res["errors"]:
                lines.append(f"    - {err}")
    print(json.dumps({"self_test_passed": all_ok, "results": lines}, indent=2))
    for ln in lines:
        print(ln, file=sys.stderr)
    return 0 if all_ok else 1


def main(argv: List[str]) -> int:
    args = argv[1:]
    keys_path = os.environ.get("SAR_KEYS_REGISTRY_PATH", _DEFAULT_KEYS_PATH)

    if not args:
        print("usage: verify_receipt.py <receipt.json> | --self-test", file=sys.stderr)
        return 2

    if args[0] in ("--self-test", "-t"):
        return _run_self_test(keys_path)

    receipt_path = args[0]
    try:
        with open(receipt_path, "r", encoding="utf-8") as f:
            receipt = json.load(f)
    except Exception as e:
        print(json.dumps({"valid": False, "receipt_id": None, "kid": None,
                          "verdict": None, "errors": [f"could not read receipt: {e}"]}, indent=2))
        return 1

    res = verify_receipt(receipt, keys_path)
    print(json.dumps(res, indent=2))
    return 0 if res["valid"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
