## Description:

Self-trust is a deterministic personal-finance discipline engine for bookkeeping, spending approvals, cooldowns, budgeting, reconciliation, debt and mortgage modeling, multi-currency workflows, and optional encrypted local ledgers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shellcdev](https://clawhub.ai/user/shellcdev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route personal-finance requests through a deterministic local ledger engine for spending approvals, reports, reconciliation, rewards, debt and mortgage checks, and audited configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive personal-finance ledger and audit data locally.

Mitigation: Use a dedicated private data directory and enable encryption during initialization before storing real financial data.

Risk: The security summary identifies a customization path that can turn encrypted data into plaintext.

Mitigation: Avoid generic customization of crypto.* or internal fields, and review configuration changes before confirming them.

Risk: The security guidance warns about concurrent commands against the same encrypted ledger.

Mitigation: Serialize commands for a given encrypted ledger until the audit-write issue is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shellcdev/skills/self-trust)
- [Approval workflow reference](references/approval.md)
- [Contract schema and permissions reference](references/contract-schema.md)
- [Data modes and reconciliation reference](references/data-modes.md)
- [Exceptions, appeals, and reset reference](references/exceptions.md)
- [Initialization and encryption reference](references/init.md)
- [Interaction preprocessing reference](references/interaction.md)
- [Rendering reference](references/rendering.md)
- [Reports, calibration, and rewards reference](references/report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance and summaries grounded in structured JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial amounts, approvals, delays, and ratios are expected to be quoted from engine JSON without agent recalculation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
