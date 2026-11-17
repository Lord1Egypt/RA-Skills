## Description:

Signet Guardian is payment guard middleware for AI agents that checks policy before payment attempts, records completed payments, reports spending, and supports policy configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafalzacher1](https://clawhub.ai/user/rafalzacher1)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route payment-capable agent actions through policy checks, user confirmation thresholds, spending caps, and audit logging before and after payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permit payments when the configured policy enables them, so default or unreviewed limits may allow unintended spending.

Mitigation: Review and change the policy before relying on the skill; set paymentsEnabled to false until limits, currency, merchant rules, and confirmation thresholds are explicitly configured.

Risk: Preflight is advisory and does not reserve budget, so concurrent payment flows near the monthly cap can receive an allow decision before record-time enforcement.

Mitigation: Avoid concurrent payment flows near the cap, require explicit confirmation for uncertain payments, and treat signet-record under its file lock as the authoritative monthly-cap check.

Risk: The ledger is a local JSONL file and may be altered outside the skill if the workspace is not protected.

Mitigation: Protect the ledger path from local modification, monitor ledger changes, and run payment-capable agents in a controlled workspace.

Risk: Usage examples rely on npx and tsx command execution, which may use unpinned or externally resolved tooling.

Mitigation: Prefer pinned dependencies and locally installed tooling before using the skill in payment workflows.

## Reference(s):

- [Signet Guardian ClawHub skill page](https://clawhub.ai/rafalzacher1/skills/signet-guardian)
- [Signet homepage](https://getsignet.xyz)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [OpenClaw extension README](openclaw-extension/README.md)
- [Dashboard manual test](docs/DASHBOARD_TEST.md)
- [Default policy example](references/policy.json)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON policy decisions, JSONL ledger records, text reports, and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preflight decisions use ALLOW, DENY, or CONFIRM_REQUIRED; successful payments should be recorded with the same amount, currency, payee, purpose, and idempotency key when available.]

## Skill Version(s):

0.1.0 (source: release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
