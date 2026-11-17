## Description:

Tracks income, expenses, task pricing, and daily, weekly, and monthly financial reports for local revenue management workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fffdz](https://clawhub.ai/user/fffdz)

### License/Terms of Use:

MIT

## Use Case:

Independent operators and agent users use this skill to record revenue and expenses, calculate task prices, monitor budgets, and generate recurring financial summaries. It is intended for local financial tracking and pricing guidance rather than accounting-system integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private financial details may be entered into model-assisted pricing or reporting workflows.

Mitigation: Confirm where OpenClaw model calls are processed before entering private financial data, and disable automatic model invocation when local-only handling is required.

Risk: The published artifact references PowerShell scripts that are not included in the inspected package.

Mitigation: Verify the installed package contains the expected scripts before relying on command examples or automated log/report generation.

Risk: Pricing and report outputs may be incomplete or misleading if source transactions are missing or incorrectly categorized.

Mitigation: Review generated logs, pricing recommendations, and reports before using them for client quotes or financial decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fffdz/skills/tianyi-revenue-tracker)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with PowerShell command examples, financial log entries, pricing suggestions, and report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local finance logs and reports when the referenced supporting scripts are present.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, artifact/SKILL.md clawdbot.version, artifact/README.md changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
