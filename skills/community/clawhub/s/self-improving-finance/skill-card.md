## Description:

Captures reconciliation errors, forecast variances, control weaknesses, regulatory gaps, valuation errors, and cash flow anomalies to enable continuous finance operations improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, accounting, audit, treasury, FP&A, and agent-workflow users use this skill to capture anonymized finance issues and reusable learnings. It supports promoting recurring patterns into close checklists, reconciliation procedures, control matrices, tax calendars, forecast models, audit response templates, or reusable skills after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent finance learning logs can capture sensitive financial, client, tax, or account data.

Mitigation: Anonymize all entries and avoid real account numbers, bank details, client names, taxpayer IDs, and exact sensitive amounts.

Risk: Optional reminder hooks persist across sessions and may inspect command output when advanced detection is enabled.

Mitigation: Keep hooks project-scoped, prefer the activator-only hook, and do not log raw command output, secrets, or transcripts.

Risk: Promoted procedures or generated skills may encode incorrect finance treatment if not reviewed.

Mitigation: Require explicit user approval before promotion, review generated SKILL.md content, and scan the skill before deployment.

## Reference(s):

- [Entry Examples](references/examples.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and optional generated SKILL.md scaffolds.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates local finance learning logs and may emit opt-in hook reminders; generated skills require human review before use.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
