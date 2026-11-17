from __future__ import annotations

import copy
import json
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path

from kya_receipt import ReceiptError, action_hash, issue_receipt, verify_receipt


SECRET = b"test-only-secret-with-at-least-thirty-two-bytes"
NOW = datetime(2026, 7, 17, 8, 0, tzinfo=UTC)


def sample_action() -> dict[str, object]:
    return {
        "schema_version": "2.0",
        "action_id": "act_supplier_8000_001",
        "idempotency_key": "idem_supplier_8000_001",
        "tenant_id": "tenant_demo",
        "subject_id": "user_001",
        "agent_id": "agent_payments_001",
        "scenario": "supplier_payment",
        "action_type": "cross_border_payment",
        "requested_action": "execute_payment",
        "target": {
            "type": "beneficiary",
            "reference": "supplier_4821",
            "account_fingerprint": "sha256:acct_7f42d9c1",
            "country": "SG",
        },
        "amount": {"value_minor": 800000, "currency": "USD"},
        "authorization_context": {
            "requested_by": "user_001",
            "agent_scope": ["prepare_payment", "execute_payment"],
            "session_id": "session_001",
        },
        "evidence_references": ["invoice:INV-2048", "contract:PO-812"],
        "attributes": {"new_beneficiary": True, "high_risk_country": False},
        "created_at": "2026-07-17T07:55:00Z",
    }


def sample_decision(action: dict[str, object]) -> dict[str, object]:
    controls = [
        "standard_audit_logging",
        "user_confirmation",
        "identity_verification",
        "authority_verification",
        "beneficiary_verification",
        "independent_human_approval",
    ]
    actor_by_control = {
        "standard_audit_logging": ("system", "audit_service"),
        "user_confirmation": ("user", "user_001"),
        "identity_verification": ("provider", "identity_provider"),
        "authority_verification": ("provider", "authority_service"),
        "beneficiary_verification": ("provider", "beneficiary_service"),
        "independent_human_approval": ("human", "finance_manager_007"),
    }
    return {
        "schema_version": "2.0",
        "decision_id": "dec_supplier_8000_001",
        "action_hash": action_hash(action),
        "decision": "HUMAN_APPROVAL",
        "authorization_status": "APPROVED",
        "risk_level": "HIGH",
        "reason_codes": ["HIGH_VALUE_TRANSACTION", "NEW_BENEFICIARY"],
        "required_controls": controls,
        "satisfied_controls": controls,
        "control_evidence": [
            {
                "control": control,
                "status": "PASSED",
                "actor_type": actor_by_control[control][0],
                "actor_id": actor_by_control[control][1],
                "evidence_reference": f"evidence:{control}:001",
                "completed_at": "2026-07-17T07:59:00Z",
            }
            for control in controls
        ],
        "blocked_actions": [],
        "policy_version": "2.0.0",
        "receipt_ttl_seconds": 300,
        "evaluated_at": "2026-07-17T07:59:30Z",
    }


class ReceiptTests(unittest.TestCase):
    def test_hash_is_stable_across_property_order(self) -> None:
        action = sample_action()
        reordered = dict(reversed(list(action.items())))
        self.assertEqual(action_hash(action), action_hash(reordered))

    def test_exact_action_receipt_verifies(self) -> None:
        action = sample_action()
        receipt = issue_receipt(action, sample_decision(action), SECRET, now=NOW)
        result = verify_receipt(
            action,
            receipt,
            SECRET,
            expected_policy_version="2.0.0",
            expected_kid="kya-test-key-1",
            now=NOW + timedelta(seconds=1),
        )
        self.assertTrue(result["ok"])

    def test_amount_mutation_is_rejected(self) -> None:
        action = sample_action()
        receipt = issue_receipt(action, sample_decision(action), SECRET, now=NOW)
        mutated = copy.deepcopy(action)
        mutated["amount"]["value_minor"] = 900000
        with self.assertRaisesRegex(ReceiptError, "action_hash"):
            verify_receipt(
                mutated,
                receipt,
                SECRET,
                expected_policy_version="2.0.0",
                expected_kid="kya-test-key-1",
                now=NOW + timedelta(seconds=1),
            )

    def test_expired_receipt_is_rejected(self) -> None:
        action = sample_action()
        receipt = issue_receipt(action, sample_decision(action), SECRET, now=NOW, ttl_seconds=30)
        with self.assertRaisesRegex(ReceiptError, "expired"):
            verify_receipt(
                action,
                receipt,
                SECRET,
                expected_policy_version="2.0.0",
                expected_kid="kya-test-key-1",
                now=NOW + timedelta(seconds=31),
            )

    def test_missing_control_cannot_issue_receipt(self) -> None:
        action = sample_action()
        decision = sample_decision(action)
        decision["satisfied_controls"] = decision["satisfied_controls"][:-1]
        with self.assertRaisesRegex(ReceiptError, "unsatisfied"):
            issue_receipt(action, decision, SECRET, now=NOW)

    def test_ai_agent_cannot_satisfy_human_approval(self) -> None:
        action = sample_action()
        decision = sample_decision(action)
        decision["control_evidence"][-1]["actor_type"] = "ai_agent"
        with self.assertRaisesRegex(ReceiptError, "human actor"):
            issue_receipt(action, decision, SECRET, now=NOW)

    def test_replay_is_rejected_after_nonce_consumption(self) -> None:
        action = sample_action()
        receipt = issue_receipt(action, sample_decision(action), SECRET, now=NOW)
        with tempfile.TemporaryDirectory() as directory:
            nonce_db = Path(directory) / "nonces.db"
            kwargs = {
                "expected_policy_version": "2.0.0",
                "expected_kid": "kya-test-key-1",
                "now": NOW + timedelta(seconds=1),
                "nonce_db": nonce_db,
            }
            verify_receipt(action, receipt, SECRET, **kwargs)
            with self.assertRaisesRegex(ReceiptError, "replay"):
                verify_receipt(action, receipt, SECRET, **kwargs)

    def test_all_json_templates_parse_and_mcp_sequence_is_complete(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for path in root.rglob("*.json"):
            with self.subTest(path=path.name):
                json.loads(path.read_text(encoding="utf-8"))
        contract = json.loads(
            (root / "templates" / "mcp-tool-contract-example.json").read_text(encoding="utf-8")
        )
        tool_names = {tool["name"] for tool in contract["tools"]}
        self.assertTrue(set(contract["required_sequence"]).issubset(tool_names))


if __name__ == "__main__":
    unittest.main()
