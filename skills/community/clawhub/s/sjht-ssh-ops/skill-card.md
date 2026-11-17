## Description:

sjht-ssh-ops helps agents manage SSH keys and perform remote server operations such as key generation, public-key deployment, connection tests, host information checks, and remote command execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aowind](https://clawhub.ai/user/aowind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up SSH key access, verify passwordless login, inspect remote host basics, and prepare commands for routine server administration or deployment work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through high-impact SSH key management and remote server access.

Mitigation: Review each proposed command before execution, use the least-privileged account that can complete the task, and avoid root access unless it is required.

Risk: Password-based public-key deployment may expose reusable credentials through chat, shell history, logs, or environment persistence.

Mitigation: Do not paste reusable passwords into chat or persistent files, unset password environment variables immediately after use, and prefer short-lived or out-of-band credential handling.

Risk: Disabling strict host-key checks can allow connecting to an unintended or impersonated host.

Mitigation: Verify host keys out of band before deployment and prefer stricter SSH host-key validation when adapting the commands.

Risk: Automatic dependency installation and broad remote commands can modify local or remote systems unexpectedly.

Mitigation: Require explicit approval for package installation and remote execution, validate host, user, and key-name inputs, and test on non-critical hosts before production use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include high-impact SSH, scp, rsync, package installation, and remote execution commands that require operator review before use.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
