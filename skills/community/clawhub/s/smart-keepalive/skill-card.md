## Description:

Smart Keepalive fetches source items, asks an agent to format a periodic keepalive brief, and sends it through OpenClaw or a configured command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[east5ringroad-kyle](https://clawhub.ai/user/east5ringroad-kyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure, run, and troubleshoot scheduled brief-sending workflows for OpenClaw, Hermes, launchd, or cron. The skill helps generate concise keepalive reports, optional wellness notes, and status footer text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended scheduled sending can deliver messages to an unintended channel or target.

Mitigation: Confirm the configured channel and target, run the doctor check, and keep scheduled sending disabled until logs and a manual send test are reviewed.

Risk: Custom agent or send commands can execute behavior outside the default OpenClaw path.

Mitigation: Use only trusted, audited custom commands and prefer the default CLI path when a custom runtime is not required.

Risk: URL overrides for source or weather fetching could point the task at internal or sensitive hosts.

Mitigation: Restrict URL overrides to approved external sources and avoid internal network, metadata, or sensitive service endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/east5ringroad-kyle/skills/smart-keepalive)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run unattended and may use configured commands, URLs, channels, targets, logs, and local state files.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
