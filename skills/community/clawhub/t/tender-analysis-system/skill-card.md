## Description:

Automates tender information collection and produces structured tender risk, payment, evaluation, technical, and contract analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ylbwjf](https://clawhub.ai/user/ylbwjf)

### License/Terms of Use:

MIT-0

## Use Case:

Business development, procurement, and bid teams use this skill to monitor tender sources and generate structured summaries of newly found opportunities, high-value projects, deadlines, payment terms, evaluation criteria, and contract risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can create recurring background jobs and repeatedly install packages without clear rollback controls.

Mitigation: Review the skill before installation, run cron_setup.sh only when recurring jobs are intended, use a least-privileged account, inspect crontab afterward, and prefer pinned dependencies in an isolated environment.

Risk: External notifications may expose tender details or send data to unintended recipients if configured incorrectly.

Mitigation: Keep notification channels disabled until recipient addresses, webhooks, and sensitive tender-data handling expectations are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ylbwjf/skills/tender-analysis-system)
- [Publisher profile](https://clawhub.ai/user/ylbwjf)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown reports and briefings with configurable YAML settings and shell commands for execution or scheduling.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write report files and SQLite data locally; scheduled operation is optional and should be explicitly enabled by the user.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
