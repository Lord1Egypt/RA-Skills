# Human Gate Policy

Model a gate as two outputs:

- `decision`: the current routing or terminal state.
- `required_controls`: the union of controls added by every matching rule and threshold.

Do not treat gate levels as mutually exclusive. A high-value payment can require user confirmation, identity verification, authority verification, beneficiary verification, and independent human approval at the same time.

## Routing States

- `ALLOW`: use only when no required control remains unsatisfied.
- `USER_CONFIRMATION`: collect informed confirmation for the frozen action.
- `STEP_UP_AUTHENTICATION`: validate a stronger session factor.
- `IDENTITY_VERIFICATION`: validate current identity evidence.
- `HUMAN_APPROVAL`: route the full action packet to an independent authorized person.
- `COMPLIANCE_REVIEW`: hold for an authorized compliance process. Ordinary approval cannot clear it.
- `DENY`: terminal safe stop. Do not issue a delegation receipt.

## Typical Control Triggers

- Add `standard_audit_logging` to every action.
- Add `user_confirmation` for value transfer or irreversible user consequence.
- Add `step_up_authentication` for new device, geo anomaly, stale session, or sensitive access.
- Add `identity_verification` for stale KYC, identity anomaly, withdrawal, off-ramp, or account-control change.
- Add `authority_verification` when the subject or agent scope may not cover the action.
- Add `beneficiary_verification` for a new or modified payout target.
- Add `independent_human_approval` for high value, budget exception, new beneficiary, lending decision, or material irreversible action.
- Add `compliance_review` and `safe_stop` for screening uncertainty, provider conflict, or audit failure.

## Approval Packet

Show the human the action ID, action hash, amount in major units, currency, target summary, consequence, reason codes, evidence references, policy version, required controls, and expiry. Never ask a human to approve a vague conversation or a mutable draft.

After any action change, discard prior control state, calculate a new hash, and start a new decision. Approval is not transferable across hashes.
