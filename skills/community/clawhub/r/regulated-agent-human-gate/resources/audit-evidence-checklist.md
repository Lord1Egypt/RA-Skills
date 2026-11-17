# Audit Evidence Checklist

Retain references and digests, not unnecessary raw sensitive data.

Record these fields across the event chain:

- Tenant, trace, subject, agent, action, and idempotency identifiers.
- Canonicalization profile and exact action hash.
- Policy version, matched rule IDs, decision, risk level, and reason codes.
- Agent authorization scope checked at decision time.
- Cumulative required controls and satisfied controls.
- Provider-signed evidence references for identity, authentication, authority, beneficiary, AML, or sanctions checks.
- Independent approver ID, role, evidence reference, timestamp, and separation-of-duties result.
- Delegation receipt ID, decision hash, nonce, key ID, issued time, expiry, verification result, and consumption result.
- Execution provider reference, outcome, failure code, and safe fallback.
- Previous event hash, event hash, and external signature or immutable-store reference when available.

Test audit completeness against `templates/audit-log-schema.json`. Protect event integrity with canonicalization, an append-only destination, access control, retention rules, and a managed signature or timestamping mechanism. A local hash chain alone does not prove immutability.

Do not store full identity documents, raw biometrics, full account numbers, passwords, access tokens, secrets, or private keys in action intents, receipts, or audit logs.
