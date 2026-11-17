## Description:

Weekly Checker helps agents run recurring OpenClaw gateway, skill library, security, Windows system, and log health checks and generate status reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check OpenClaw service status, skill library health, configuration security, Windows resource usage, and logs on a weekly or manual schedule. It produces reports and notification text that help prioritize issues while leaving higher-risk repairs for explicit review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scans and generated reports may include secrets, private project data, or sensitive local system details.

Mitigation: Use explicit path allowlists and redact sensitive values before saving reports or sending notifications.

Risk: Scheduled notifications could disclose operational details outside the intended audience.

Mitigation: Require approval before enabling Feishu notifications and verify the recipient list and message content.

Risk: Repair actions such as log deletion or gateway restart can change the local environment.

Mitigation: Require user confirmation for repairs unless a reversible action has been separately configured and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/weekly-checker)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with JSON report examples, notification text, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe scheduled checks, manual triggers, issue severity, report paths, notification content, and repair guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
