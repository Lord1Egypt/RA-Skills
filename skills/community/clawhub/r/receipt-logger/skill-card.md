## Description:

Create tamper-evident, append-only audit logs of agent actions with exportable JSON receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiuge897](https://clawhub.ai/user/jiuge897)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record agent actions as persistent receipts for audit, verification, and external review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is incomplete because the advertised receipt-logger executable is missing.

Mitigation: Verify that the publisher supplies the missing executable before installation or use.

Risk: Receipts are intended to persist and be exportable, so sensitive inputs or outputs could be retained.

Mitigation: Avoid logging secrets, credentials, private content, or other sensitive data.

## Reference(s):

- [Receipt Logger on ClawHub](https://clawhub.ai/jiuge897/skills/receipt-logger)
- [Publisher profile](https://clawhub.ai/user/jiuge897)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and JSON receipt examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Receipts are described as append-only, exportable JSON records containing timestamps, action details, hashes, and signatures.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
