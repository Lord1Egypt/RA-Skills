## Description:

Monitors Raspberry Pi CPU temperature, helps configure recurring checks, and sends an alert when the configured threshold is exceeded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archerweiye](https://clawhub.ai/user/archerweiye)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to monitor Raspberry Pi CPU temperature and configure scheduled alerts through crontab or OpenClaw cron.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring execution can persist after installation and continue sending authenticated alerts.

Mitigation: Require explicit user approval before installing cron jobs and provide clear install, review, and removal steps.

Risk: Alert delivery reads an OpenClaw bearer token and could expose or misuse credentials if configured carelessly.

Mitigation: Use a dedicated least-privilege alert token and avoid passing tokens in command-line arguments or logs.

Risk: The artifact contains a hard-coded user path for the OpenClaw gateway token.

Mitigation: Replace hard-coded paths such as /home/weiye with user-controlled configuration before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate cron entries and alerting script guidance for local Raspberry Pi environments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
