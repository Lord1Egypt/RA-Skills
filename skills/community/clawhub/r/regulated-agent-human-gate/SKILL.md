---
name: regulated-agent-human-gate
description: Build, review, or test KYA (Know Your Agent) human-gate controls for AI agents that prepare or execute regulated financial actions. Use for payments, withdrawals, stablecoin off-ramps, lending, onboarding, identity or account-control changes, MCP execution chains, action-bound approvals, delegation receipts, audit evidence, and adversarial evaluations.
---

# KYA Regulated Agent Human Gate

Treat the language model as a planner and evidence collector, never as the final authorization boundary. Put deterministic policy evaluation and receipt verification in trusted code outside the model.

## Enforce These Invariants

1. Freeze the exact action before requesting approval.
2. Hash the canonical action and bind every decision and approval to that hash.
3. Accumulate controls from every matched rule. A stronger routing decision must not erase another required control.
4. Keep authentication, identity, authority, business approval, and compliance review separate.
5. Let only a trusted policy service issue a short-lived, signed, one-time delegation receipt.
6. Verify the receipt against the final action immediately before execution.
7. Consume the receipt nonce and execute idempotently. Reject replay, expiry, mutation, tenant mismatch, policy mismatch, and signer mismatch.
8. Fail closed when screening, evidence, authorization, audit writing, or provider state is uncertain.
9. Never let an AI agent approve its own action or mark a human control as satisfied.

## Build The Gate

1. Normalize the action with `templates/action-intent-schema.json`.
   - Represent money as integer `value_minor`, never a floating-point amount.
   - Use stable tenant, subject, agent, target, and idempotency identifiers.
   - Store references or fingerprints, not raw credentials, biometrics, or identity documents.
2. Freeze and hash the action with `scripts/kya_receipt.py hash`.
3. Evaluate all policy rules deterministically.
   - Return a routing `decision` and a separate cumulative `required_controls` list.
   - Set `authorization_status` to `PENDING_CONTROLS`, `APPROVED`, or `DENIED`.
   - Treat `ALLOW` as executable only when every required control is satisfied.
4. Collect control evidence through trusted providers and independent human actors.
5. Re-evaluate when evidence or action data changes. Never patch an old approval onto a new action.
6. Issue a delegation receipt only when the decision validates against `templates/gate-decision-schema.json` and every required control is satisfied.
7. Verify and atomically consume the receipt at the authorized executor.
8. Append the decision, control, receipt, execution, and failure events using `templates/audit-log-schema.json`.
9. Run mutation, replay, expiry, fail-closed, and false-allow evaluations before launch.

## Resolve Decisions And Controls

Use `decision` as the current routing state, not as the complete authorization record.

- `ALLOW`: no unsatisfied control remains; standard audit logging still applies.
- `USER_CONFIRMATION`: require confirmation of the frozen amount, target, fees, and consequence.
- `STEP_UP_AUTHENTICATION`: require an OTP, passkey, or equivalent trusted authentication result.
- `IDENTITY_VERIFICATION`: require current identity and, when relevant, authority evidence.
- `HUMAN_APPROVAL`: require an independent authorized approver with the complete action summary.
- `COMPLIANCE_REVIEW`: hold execution until an authorized compliance process resolves uncertainty.
- `DENY`: stop execution. Ordinary approval cannot override a terminal denial.

Union controls across matching rules. For example, a USD 8,000 payment to a new beneficiary can require all of `user_confirmation`, `identity_verification`, `beneficiary_verification`, and `independent_human_approval`, even when the routing decision is `HUMAN_APPROVAL`.

## Use The MCP Execution Contract

Implement every tool named in `templates/mcp-tool-contract-example.json` and preserve this trust sequence:

1. `evaluate_financial_action`
2. `create_control_challenge`
3. `record_control_result`
4. `issue_delegation_receipt`
5. `verify_and_consume_receipt`
6. `execute_authorized_action`
7. `write_audit_event`

The executor must not accept a decision ID, chat confirmation, screenshot, or approval ID as authorization. It must accept only a verified receipt bound to the final action hash.

## Exercise The Reference Guard

Set a test-only signing key and run the examples:

```powershell
$env:KYA_RECEIPT_SECRET = "replace-with-a-test-secret-at-least-32-bytes"
python scripts/kya_receipt.py hash --action examples/supplier-payment-action.json
python scripts/kya_receipt.py issue --action examples/supplier-payment-action.json --decision examples/supplier-payment-decision.json --output receipt.json
python scripts/kya_receipt.py verify --action examples/supplier-payment-action.json --receipt receipt.json --policy-version 2.0.0 --nonce-db receipt-nonces.db
python -m unittest discover -s scripts -p "test_*.py"
```

Use HMAC only as the self-contained reference implementation. In production, place signing in a managed KMS or HSM, rotate keys by `kid`, authenticate MCP callers, and combine nonce consumption with an idempotent execution record.

## Produce This Output

```markdown
## Action Intent And Hash
## Agent Scope And Trust Boundary
## Risk And Matched Rules
## Cumulative Required Controls
## Control Evidence And Separation Of Duties
## Delegation Receipt And MCP Execution Contract
## Audit And Data-Minimization Plan
## Failure And Safe Fallbacks
## Evaluation Cases And Acceptance Metrics
## Open Assumptions
```

## Read Supporting Material

- Read `resources/risk-taxonomy.md` for risk factors.
- Read `resources/human-gate-policy.md` for cumulative control and terminal decision rules.
- Read `resources/identity-verification-routing.md` to separate identity, authentication, authority, and approval.
- Read `resources/audit-evidence-checklist.md` for retained evidence.
- Read `resources/agent-evaluation-guide.md` for launch evaluations.
- Read `resources/regulated-finance-use-cases.md` for scenario patterns.
- Start policy work from `templates/policy-template.yaml`.

## State The Boundary

Do not claim regulatory certification, legal advice, or production-grade immutability. State which controls are implemented, mocked, provider-backed, or still require legal and compliance approval.
