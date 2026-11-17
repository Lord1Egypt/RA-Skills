## Description:

自动化工作流引擎，用于定时执行数据采集、处理、通知和存档任务链，并支持 cron 定时、webhook 触发和文件监控。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjstate](https://clawhub.ai/user/cjstate)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to define and run scheduled or event-triggered automation workflows for data collection, transformation, notification, file handling, and database operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended workflows can make network calls, modify files or databases, and send email.

Mitigation: Install in a constrained environment, review each workflow definition before running it, and avoid broad filesystem or database credentials.

Risk: Daemon mode can execute triggered workflows without active review.

Mitigation: Use daemon mode only for approved workflows with explicit approvals, monitoring, and rollback plans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjstate/skills/xh-auto-workflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow definitions and operational commands for immediate, daemon, or status modes.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
