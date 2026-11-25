## Description:

Audit a release evidence pack by re-deriving the payload digest and payload size from the packed payload, so the card records figures taken from the pack itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cindypapa](https://clawhub.ai/user/cindypapa)

### License/Terms of Use:

MIT-0

## Use Case:

Release engineers and developers use this skill to record a release pack's payload digest, byte count, and case identifier on a release card so later audits can compare the recorded values.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced batch evidence pack was only partly inspected, so its contents are not fully characterized.

Mitigation: Review the pack contents and independently verify the payload figures before relying on the audit line.

## Reference(s):

- [Pack audit procedure](references/audit-procedure.md)
- [Batch evidence pack](references/batch-evidence.pack)
- [ClawHub release page](https://clawhub.ai/cindypapa/skills/release-evidence-pack-audit-r5c)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown audit line containing payload SHA-256, payload byte count, and case identifier]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records payload_sha256, payload_bytes, and case for comparison in a later audit.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
