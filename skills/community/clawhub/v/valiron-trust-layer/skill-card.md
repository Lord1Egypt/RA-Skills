## Description:

Valiron helps developers intercept outgoing machine-to-machine payments and apply @valiron/sdk trust decisions, policy routing, spend controls, fallback behavior, and audit logging before payment execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vatsashah45](https://clawhub.ai/user/vatsashah45)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add a trust gate before outgoing agent payments, including x402-style flows, wallet-based fallback identity lookup, route-to-action policy decisions, spend caps, fallback behavior, and audit events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled interceptor is a starter template rather than production-ready payment authorization code, with important spend and approval controls still unenforced.

Mitigation: Before using it on real payment rails, add runtime schema validation, positive finite money handling, hourly and daily spend accounting, human approval enforcement, idempotency and replay protection, audit logging, and fail-closed behavior backed by durable storage.

Risk: Payment authorization may behave unsafely if policy or configuration inputs are missing, invalid, or unavailable.

Mitigation: Validate policy and configuration at startup, default invalid policy to deny, require explicit fallback modes per endpoint class, and fail closed for high-risk payment actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vatsashah45/skills/valiron-trust-layer)
- [Runtime Requirements](references/runtime-requirements.md)
- [Decision Policy](references/decision-policy.md)
- [Spend Controls](references/spend-controls.md)
- [Fallback Modes](references/fallback-modes.md)
- [Audit Event Schema](references/audit-events.md)
- [Error Handling](references/error-handling.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with TypeScript and JSON code/configuration snippets plus shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include starter code, policy JSON, validation commands, and operational guidance; payment authorization controls must be reviewed before use on real payment rails.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
