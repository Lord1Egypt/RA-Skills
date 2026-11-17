## Description:

Automates monitoring and self-repair guidance for OpenClaw Gateway on Windows using Task Scheduler, PowerShell commands, AI-assisted diagnosis, and Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aichiafranco](https://clawhub.ai/user/aichiafranco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy, inspect, and repair a Windows-based OpenClaw Gateway service with scheduled monitoring, repair commands, and alerting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package describes persistent Windows scheduled tasks and repair commands, but the reviewed artifact does not include the PowerShell scripts those tasks execute.

Mitigation: Install only after the publisher provides the missing scripts and documents exactly what deployment and repair actions change.

Risk: Repair workflows may affect running processes, ports, plugins, or gateway configuration.

Mitigation: Require explicit confirmation, backups, and an uninstall or rollback path before enabling destructive repair behavior.

Risk: AI diagnosis and Telegram alerts may expose logs or operational metadata outside the local host.

Mitigation: Document what data is sent, scrub secrets from logs, and configure provider credentials through protected environment files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aichiafranco/skills/windows-healing-gateway)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows 10/11 and PowerShell 5.1 or later are required; outputs may include commands that register persistent scheduled tasks or trigger repair actions.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
