## Description:

Captures ticket resolution delays, misdiagnoses, escalation gaps, SLA breaches, knowledge gaps, and customer churn signals to enable continuous support improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and developers use this skill to capture late or incorrect resolutions, SLA breaches, reopened tickets, escalation failures, missing knowledge base coverage, low CSAT, and churn signals as structured Markdown learning logs. Reviewed recurring patterns can be promoted into KB articles, troubleshooting trees, escalation matrices, canned responses, or reusable support skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Support learning logs may capture customer PII, credentials, tokens, or privileged support details.

Mitigation: Use ticket IDs and anonymized summaries, avoid verbatim customer messages, and review .learnings entries for sensitive data before sharing or committing them.

Risk: Persistent hooks can create broader-than-intended reminders or inspect command output when configured too broadly.

Mitigation: Keep hooks project-scoped, narrow matchers before enabling them, and use the activator-only setup unless command-output inspection is needed.

Risk: Command output inspected by the optional detector may contain sensitive data.

Mitigation: Do not log raw command output, secrets, or transcripts; treat command output as sensitive and only record redacted support signals.

Risk: Promoting a learning into agent instructions, support standards, or an extracted skill could preserve incorrect or misleading guidance.

Mitigation: Require a reviewed diff, explicit user approval, and security review before applying promotions or publishing extracted skills.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jose-compu/skills/self-improving-support)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown entries, concise text reminders, and setup snippets with inline shell commands or JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates project-scoped .learnings files and can optionally emit hook reminders when enabled.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
