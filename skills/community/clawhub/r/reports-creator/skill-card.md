## Description:

Automated report generation for self-reflection and system analysis. Creates daily, weekly, and monthly reports from logs, databases, and system metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to create daily, weekly, monthly, and ad-hoc Markdown reports from local logs, databases, documentation changes, filesystem activity, and system metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may expose sensitive logs, documentation changes, filesystem activity, operational metrics, or other private details.

Mitigation: Store the reports directory with appropriate permissions and redact secrets or private operational details before sharing reports.

Risk: Scheduled report generation may run against local systems on an automated cadence.

Mitigation: Review cron entries and scheduled commands before enabling them.

## Reference(s):

- [Reports Creator on ClawHub](https://clawhub.ai/kikikari/skills/reports-creator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be written to a configured reports directory and generated manually or on a schedule.]

## Skill Version(s):

1.0.0 (source: package.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
