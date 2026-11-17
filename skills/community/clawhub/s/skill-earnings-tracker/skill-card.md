## Description:

Tracks skill marketplace earnings and performance metrics across ClawHub, EvoMap, ReelMind, and custom manual logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylechen26](https://clawhub.ai/user/kylechen26)

### License/Terms of Use:


## Use Case:

Developers and marketplace publishers use this skill to log earnings, list tracked skills, generate weekly or monthly reports, export records, and check ClawHub skill statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Earnings records and exported reports are stored in plaintext while the artifact claims earnings data is encrypted at rest.

Mitigation: Treat ~/.openclaw/earnings and exported reports as sensitive plaintext files; avoid storing secrets, personal data, or customer information in notes and protect or delete exports manually.

Risk: Reports may include real earnings, credits, customer-adjacent notes, or private portfolio information.

Mitigation: Review generated reports before sharing and keep exports in access-controlled storage.

## Reference(s):

- [ClawHub marketplace](https://clawhub.ai)
- [EvoMap marketplace](https://evomap.ai/marketplace)
- [ReelMind](https://reelmind.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with CLI commands and JSON/JSONL earnings data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes monthly plaintext JSONL logs under ~/.openclaw/earnings and can export aggregated JSON reports.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
