## Description:

Run commands across multiple VPS simultaneously. Execute SSH commands, deploy updates, check logs, manage Docker services, and check health across all your servers from one place. Use when managing multiple VPS, running commands across all hosts, checking status of distributed services, or deploying changes to multiple servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chmikiro](https://clawhub.ai/user/chmikiro)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to run commands and manage Docker services across VPS fleets, check host health, and inspect logs. Review the remote-command input handling before production use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe remote-command input handling can turn a log request into arbitrary commands across configured servers.

Mitigation: Fix and validate remote-command arguments, including log line counts and container, image, and filter values, before production use. Use restricted SSH accounts and a limited host inventory, verify host keys, and choose trusted image digests.

## Reference(s):

- [VPS Command Runner on ClawHub](https://clawhub.ai/chmikiro/skills/vps-command-runner)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text]

**Output Format:** [Shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs commands against configured VPS hosts; fleet-wide actions may require interactive confirmation.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
