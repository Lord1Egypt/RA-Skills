## Description:

Automatically performs a weekly operational self-check across system status, cron tasks, the skill framework, data-layer state, and known issues, then prepares and sends a detailed Feishu report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colbertlee](https://clawhub.ai/user/colbertlee)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and developers use this skill to run a scheduled weekend health check for a ClawHub/OpenClaw workspace, identify cron and data-layer issues, and route a concise report to Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Internal operational status and diagnostic details may be sent to a hard-coded Feishu recipient.

Mitigation: Approve the recipient for the deployment environment or replace it with an administrator-configured destination before enabling sends.

Risk: The skill uses local Feishu credentials to send reports.

Mitigation: Run with --dry-run or --no-send until the report contents, credentials, and destination account have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/colbertlee/skills/weekend-self-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown-style operational report and Feishu rich-text JSON payload; dry-run mode prints JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled weekly execution with optional --dry-run, --no-send, and --skip-sync modes.]

## Skill Version(s):

1.4.0 (source: server release metadata and artifact script)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
