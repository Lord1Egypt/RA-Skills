#!/usr/bin/env python3
"""Reference action binding and one-time delegation receipt guard for KYA gates."""

from __future__ import annotations

import argparse
import copy
import hashlib
import hmac
import json
import os
import secrets
import sqlite3
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

CANONICALIZATION_PROFILE = "KYA-CJ-1"
HASH_PREFIX = "sha256:"
MIN_SECRET_BYTES = 32
REQUIRED_ACTION_FIELDS = {
    "schema_version",
    "action_id",
    "idempotency_key",
    "tenant_id",
    "subject_id",
    "agent_id",
    "scenario",
    "action_type",
    "requested_action",
    "target",
    "amount",
    "authorization_context",
    "created_at",
}
REQUIRED_DECISION_FIELDS = {
    "schema_version",
    "decision_id",
    "action_hash",
    "decision",
    "authorization_status",
    "risk_level",
    "reason_codes",
    "required_controls",
    "satisfied_controls",
    "control_evidence",
    "blocked_actions",
    "policy_version",
    "evaluated_at",
}
SENSITIVE_KEYS = {
    "password",
    "secret",
    "access_token",
    "refresh_token",
    "private_key",
    "raw_document",
    "biometric_template",
}


class ReceiptError(ValueError):
    """Raised when an action or receipt violates the KYA authorization contract."""


def canonical_json(value: Any) -> str:
    """Return deterministic JSON for the constrained KYA-CJ-1 profile."""

    _validate_canonical_value(value)
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def digest(value: Any) -> str:
    """Hash a canonical JSON value with SHA-256."""

    return HASH_PREFIX + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def action_hash(action: dict[str, Any]) -> str:
    """Validate and hash a frozen action intent."""

    validate_action(action)
    return digest(action)


def validate_action(action: dict[str, Any]) -> None:
    """Validate security-critical action fields without third-party packages."""

    if not isinstance(action, dict):
        raise ReceiptError("Action intent must be a JSON object.")
    missing = sorted(REQUIRED_ACTION_FIELDS - set(action))
    if missing:
        raise ReceiptError(f"Action intent is missing fields: {', '.join(missing)}")
    if action.get("schema_version") != "2.0":
        raise ReceiptError("Action intent schema_version must be 2.0.")

    for field in [
        "action_id",
        "idempotency_key",
        "tenant_id",
        "subject_id",
        "agent_id",
        "scenario",
        "action_type",
        "requested_action",
        "created_at",
    ]:
        if not isinstance(action.get(field), str) or not action[field]:
            raise ReceiptError(f"Action field {field} must be a non-empty string.")
    if len(action["idempotency_key"]) < 16:
        raise ReceiptError("idempotency_key must contain at least 16 characters.")

    amount = action.get("amount")
    if not isinstance(amount, dict):
        raise ReceiptError("amount must be an object.")
    value_minor = amount.get("value_minor")
    if isinstance(value_minor, bool) or not isinstance(value_minor, int) or value_minor < 0:
        raise ReceiptError("amount.value_minor must be a non-negative integer.")
    currency = amount.get("currency")
    if not isinstance(currency, str) or len(currency) != 3 or not currency.isupper():
        raise ReceiptError("amount.currency must be an uppercase three-letter code.")

    target = action.get("target")
    if not isinstance(target, dict) or not target.get("type") or not target.get("reference"):
        raise ReceiptError("target.type and target.reference are required.")
    authorization = action.get("authorization_context")
    if not isinstance(authorization, dict):
        raise ReceiptError("authorization_context must be an object.")
    if not authorization.get("requested_by"):
        raise ReceiptError("authorization_context.requested_by is required.")
    if not isinstance(authorization.get("agent_scope"), list):
        raise ReceiptError("authorization_context.agent_scope must be an array.")

    _parse_time(action["created_at"], "created_at")
    _validate_canonical_value(action)


def validate_decision(decision: dict[str, Any], expected_action_hash: str) -> None:
    """Require a completed, action-bound policy decision before receipt issuance."""

    if not isinstance(decision, dict):
        raise ReceiptError("Gate decision must be a JSON object.")
    missing = sorted(REQUIRED_DECISION_FIELDS - set(decision))
    if missing:
        raise ReceiptError(f"Gate decision is missing fields: {', '.join(missing)}")
    if decision.get("schema_version") != "2.0":
        raise ReceiptError("Gate decision schema_version must be 2.0.")
    if decision.get("action_hash") != expected_action_hash:
        raise ReceiptError("Decision action_hash does not match the frozen action.")
    if decision.get("authorization_status") != "APPROVED":
        raise ReceiptError("authorization_status must be APPROVED before issuing a receipt.")
    if decision.get("decision") in {"DENY", "COMPLIANCE_REVIEW"}:
        raise ReceiptError("Terminal denial or unresolved compliance review cannot issue a receipt.")
    if decision.get("blocked_actions"):
        raise ReceiptError("An approved decision must not retain blocked actions.")

    required = _string_set(decision.get("required_controls"), "required_controls")
    satisfied = _string_set(decision.get("satisfied_controls"), "satisfied_controls")
    missing_controls = sorted(required - satisfied)
    if missing_controls:
        raise ReceiptError(f"Required controls are unsatisfied: {', '.join(missing_controls)}")

    evidence = decision.get("control_evidence")
    if not isinstance(evidence, list):
        raise ReceiptError("control_evidence must be an array.")
    passed_controls: set[str] = set()
    for item in evidence:
        if not isinstance(item, dict) or item.get("status") != "PASSED":
            raise ReceiptError("Every control evidence item must have status PASSED.")
        control = item.get("control")
        if not isinstance(control, str) or not control:
            raise ReceiptError("Every control evidence item must name its control.")
        for field in ["actor_type", "actor_id", "evidence_reference", "completed_at"]:
            if not isinstance(item.get(field), str) or not item[field]:
                raise ReceiptError(f"Control evidence field {field} is required.")
        _parse_time(item["completed_at"], "control_evidence.completed_at")
        if control == "independent_human_approval" and item["actor_type"] != "human":
            raise ReceiptError("independent_human_approval must be satisfied by a human actor.")
        passed_controls.add(control)
    if not required.issubset(passed_controls):
        missing_evidence = sorted(required - passed_controls)
        raise ReceiptError(f"Control evidence is missing: {', '.join(missing_evidence)}")

    _parse_time(decision["evaluated_at"], "evaluated_at")
    _validate_canonical_value(decision)


def issue_receipt(
    action: dict[str, Any],
    decision: dict[str, Any],
    secret: bytes,
    *,
    kid: str = "kya-test-key-1",
    ttl_seconds: int | None = None,
    now: datetime | None = None,
    nonce: str | None = None,
    receipt_id: str | None = None,
) -> dict[str, Any]:
    """Issue an HMAC-signed receipt after all cumulative controls pass."""

    _validate_secret(secret)
    frozen_hash = action_hash(action)
    validate_decision(decision, frozen_hash)

    ttl = ttl_seconds if ttl_seconds is not None else decision.get("receipt_ttl_seconds", 300)
    if isinstance(ttl, bool) or not isinstance(ttl, int) or not 30 <= ttl <= 900:
        raise ReceiptError("Receipt TTL must be an integer from 30 through 900 seconds.")
    issued_at = _as_utc(now or datetime.now(UTC))
    expires_at = issued_at + timedelta(seconds=ttl)
    evidence = decision["control_evidence"]
    approver_ids = sorted(
        {
            item["actor_id"]
            for item in evidence
            if item.get("control") == "independent_human_approval"
            and item.get("actor_type") == "human"
        }
    )

    receipt: dict[str, Any] = {
        "schema_version": "2.0",
        "receipt_id": receipt_id or f"rcpt_{secrets.token_hex(12)}",
        "decision_id": decision["decision_id"],
        "decision_hash": digest(decision),
        "action_hash": frozen_hash,
        "action_id": action["action_id"],
        "idempotency_key": action["idempotency_key"],
        "tenant_id": action["tenant_id"],
        "subject_id": action["subject_id"],
        "agent_id": action["agent_id"],
        "action_type": action["action_type"],
        "requested_action": action["requested_action"],
        "policy_version": decision["policy_version"],
        "required_controls": sorted(set(decision["required_controls"])),
        "satisfied_controls": sorted(set(decision["satisfied_controls"])),
        "control_evidence_hash": digest(evidence),
        "approver_ids": approver_ids,
        "issued_at": _format_time(issued_at),
        "expires_at": _format_time(expires_at),
        "nonce": nonce or secrets.token_hex(24),
        "one_time_use": True,
        "signature": {"alg": "HMAC-SHA256", "kid": kid},
    }
    receipt["signature"]["value"] = _signature_value(receipt, secret)
    return receipt


def verify_receipt(
    action: dict[str, Any],
    receipt: dict[str, Any],
    secret: bytes,
    *,
    expected_policy_version: str,
    expected_kid: str,
    now: datetime | None = None,
    nonce_db: Path | None = None,
) -> dict[str, Any]:
    """Verify exact action binding and optionally consume the receipt nonce."""

    _validate_secret(secret)
    validate_action(action)
    if not isinstance(receipt, dict):
        raise ReceiptError("Delegation receipt must be a JSON object.")
    signature = receipt.get("signature")
    if not isinstance(signature, dict):
        raise ReceiptError("Receipt signature is missing.")
    if signature.get("alg") != "HMAC-SHA256":
        raise ReceiptError("Unsupported receipt signature algorithm.")
    if signature.get("kid") != expected_kid:
        raise ReceiptError("Receipt key id is not trusted by this executor.")
    supplied_signature = signature.get("value")
    if not isinstance(supplied_signature, str):
        raise ReceiptError("Receipt signature value is missing.")
    expected_signature = _signature_value(receipt, secret)
    if not hmac.compare_digest(supplied_signature, expected_signature):
        raise ReceiptError("Receipt signature is invalid.")

    if receipt.get("schema_version") != "2.0":
        raise ReceiptError("Receipt schema_version must be 2.0.")
    if receipt.get("one_time_use") is not True:
        raise ReceiptError("Receipt must require one-time use.")
    if receipt.get("policy_version") != expected_policy_version:
        raise ReceiptError("Receipt policy version is not active at the executor.")
    if receipt.get("action_hash") != action_hash(action):
        raise ReceiptError("Final action does not match the receipt action_hash.")

    bound_fields = [
        "action_id",
        "idempotency_key",
        "tenant_id",
        "subject_id",
        "agent_id",
        "action_type",
        "requested_action",
    ]
    for field in bound_fields:
        if receipt.get(field) != action.get(field):
            raise ReceiptError(f"Receipt field {field} does not match the final action.")

    required = _string_set(receipt.get("required_controls"), "required_controls")
    satisfied = _string_set(receipt.get("satisfied_controls"), "satisfied_controls")
    if not required.issubset(satisfied):
        raise ReceiptError("Receipt does not show every required control as satisfied.")
    issued_at = _parse_time(receipt.get("issued_at"), "issued_at")
    expires_at = _parse_time(receipt.get("expires_at"), "expires_at")
    current = _as_utc(now or datetime.now(UTC))
    if issued_at > current + timedelta(seconds=60):
        raise ReceiptError("Receipt issued_at is unreasonably far in the future.")
    if expires_at <= issued_at:
        raise ReceiptError("Receipt expires_at must be after issued_at.")
    if current >= expires_at:
        raise ReceiptError("Receipt has expired.")

    nonce = receipt.get("nonce")
    if not isinstance(nonce, str) or len(nonce) < 32:
        raise ReceiptError("Receipt nonce is invalid.")
    if nonce_db is not None:
        _consume_nonce(nonce_db, receipt, current)

    return {
        "ok": True,
        "receipt_id": receipt.get("receipt_id"),
        "action_hash": receipt["action_hash"],
        "idempotency_key": receipt["idempotency_key"],
        "policy_version": receipt["policy_version"],
        "consumed": nonce_db is not None,
        "verified_at": _format_time(current),
        "canonicalization_profile": CANONICALIZATION_PROFILE,
    }


def _signature_value(receipt: dict[str, Any], secret: bytes) -> str:
    unsigned = copy.deepcopy(receipt)
    signature = unsigned.get("signature")
    if not isinstance(signature, dict):
        raise ReceiptError("Receipt signature metadata is missing.")
    signature.pop("value", None)
    return hmac.new(secret, canonical_json(unsigned).encode("utf-8"), hashlib.sha256).hexdigest()


def _consume_nonce(path: Path, receipt: dict[str, Any], consumed_at: datetime) -> None:
    if str(path) != ":memory:":
        path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS consumed_receipts (
                nonce TEXT PRIMARY KEY,
                receipt_id TEXT NOT NULL UNIQUE,
                action_hash TEXT NOT NULL,
                idempotency_key TEXT NOT NULL,
                consumed_at TEXT NOT NULL
            )
            """
        )
        connection.execute("BEGIN IMMEDIATE")
        try:
            connection.execute(
                """
                INSERT INTO consumed_receipts
                    (nonce, receipt_id, action_hash, idempotency_key, consumed_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    receipt["nonce"],
                    receipt["receipt_id"],
                    receipt["action_hash"],
                    receipt["idempotency_key"],
                    _format_time(consumed_at),
                ),
            )
            connection.commit()
        except sqlite3.IntegrityError as exc:
            connection.rollback()
            raise ReceiptError("Receipt replay detected; nonce or receipt_id was already consumed.") from exc
    finally:
        connection.close()


def _validate_secret(secret: bytes) -> None:
    if len(secret) < MIN_SECRET_BYTES:
        raise ReceiptError(f"Signing secret must be at least {MIN_SECRET_BYTES} bytes.")


def _validate_canonical_value(value: Any, path: str = "$") -> None:
    if isinstance(value, float):
        raise ReceiptError(f"Floating-point values are forbidden in canonical input at {path}.")
    if value is None or isinstance(value, (str, int, bool)):
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _validate_canonical_value(item, f"{path}[{index}]")
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ReceiptError(f"JSON object keys must be strings at {path}.")
            if key.lower() in SENSITIVE_KEYS:
                raise ReceiptError(f"Sensitive field {key} is forbidden in action-bound payloads.")
            _validate_canonical_value(item, f"{path}.{key}")
        return
    raise ReceiptError(f"Unsupported canonical value at {path}: {type(value).__name__}")


def _string_set(value: Any, field: str) -> set[str]:
    if not isinstance(value, list) or not value:
        raise ReceiptError(f"{field} must be a non-empty array.")
    if any(not isinstance(item, str) or not item for item in value):
        raise ReceiptError(f"{field} must contain non-empty strings.")
    if len(value) != len(set(value)):
        raise ReceiptError(f"{field} must not contain duplicates.")
    return set(value)


def _parse_time(value: Any, field: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ReceiptError(f"{field} must be an RFC 3339 timestamp.")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ReceiptError(f"{field} must be an RFC 3339 timestamp.") from exc
    if parsed.tzinfo is None:
        raise ReceiptError(f"{field} must include a timezone.")
    return parsed.astimezone(UTC)


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ReceiptError("Runtime timestamps must include a timezone.")
    return value.astimezone(UTC)


def _format_time(value: datetime) -> str:
    return _as_utc(value).isoformat(timespec="seconds").replace("+00:00", "Z")


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ReceiptError(f"{path} must contain a JSON object.")
    return value


def _write_result(value: dict[str, Any], output: Path | None) -> None:
    rendered = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if output is None:
        sys.stdout.write(rendered)
        return
    output.write_text(rendered, encoding="utf-8")
    print(f"Wrote {output}")


def _secret_from_env(name: str) -> bytes:
    value = os.environ.get(name)
    if value is None:
        raise ReceiptError(f"Environment variable {name} is not set.")
    return value.encode("utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    hash_parser = subparsers.add_parser("hash", help="Validate and hash an action intent.")
    hash_parser.add_argument("--action", type=Path, required=True)

    issue_parser = subparsers.add_parser("issue", help="Issue an action-bound delegation receipt.")
    issue_parser.add_argument("--action", type=Path, required=True)
    issue_parser.add_argument("--decision", type=Path, required=True)
    issue_parser.add_argument("--secret-env", default="KYA_RECEIPT_SECRET")
    issue_parser.add_argument("--kid", default="kya-test-key-1")
    issue_parser.add_argument("--ttl-seconds", type=int)
    issue_parser.add_argument("--output", type=Path)

    verify_parser = subparsers.add_parser("verify", help="Verify and optionally consume a receipt.")
    verify_parser.add_argument("--action", type=Path, required=True)
    verify_parser.add_argument("--receipt", type=Path, required=True)
    verify_parser.add_argument("--secret-env", default="KYA_RECEIPT_SECRET")
    verify_parser.add_argument("--kid", default="kya-test-key-1")
    verify_parser.add_argument("--policy-version", required=True)
    verify_parser.add_argument("--nonce-db", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        action = _read_json(args.action)
        if args.command == "hash":
            _write_result(
                {
                    "action_hash": action_hash(action),
                    "canonicalization_profile": CANONICALIZATION_PROFILE,
                },
                None,
            )
            return 0
        secret = _secret_from_env(args.secret_env)
        if args.command == "issue":
            decision = _read_json(args.decision)
            receipt = issue_receipt(
                action,
                decision,
                secret,
                kid=args.kid,
                ttl_seconds=args.ttl_seconds,
            )
            _write_result(receipt, args.output)
            return 0
        receipt = _read_json(args.receipt)
        result = verify_receipt(
            action,
            receipt,
            secret,
            expected_policy_version=args.policy_version,
            expected_kid=args.kid,
            nonce_db=args.nonce_db,
        )
        _write_result(result, None)
        return 0
    except (OSError, json.JSONDecodeError, ReceiptError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
