## Description:

Automates monitoring and recovery for an OpenClaw gateway through process restart, configuration backup and rollback, and model health failover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bptravel2017](https://clawhub.ai/user/bptravel2017)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to install and operate a watchdog for OpenClaw gateway uptime, configuration recovery, and model failover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog installs a recurring LaunchAgent that can modify OpenClaw configuration and restart the gateway.

Mitigation: Review before installing, test with dry-run in a controlled environment, and confirm backups and rollback behavior before enabling recurring execution.

Risk: Security evidence reports confirmed code-injection risks related to eval/Python interpolation and PATH handling.

Mitigation: Audit and fix interpolation and PATH handling before use outside a disposable or tightly controlled environment.

## Reference(s):

- [Self-Heal Watchdog configuration reference](artifact/references/config.md)
- [ClawHub skill release page](https://clawhub.ai/bptravel2017/skills/self-heal-watchdog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to install launchd scheduling, create local watchdog state and logs, edit OpenClaw configuration, and restart the gateway.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
