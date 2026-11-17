## Description:

Enables an AI agent to connect to and operate remote Mac or Linux computers over SSH without installing an agent on the controlled device.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiang92229](https://clawhub.ai/user/lixiang92229)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an AI agent run SSH and SCP workflows against authorized remote Mac or Linux systems for file operations, system monitoring, application control, AppleScript automation, and development tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables AI-driven SSH control of remote computers and may grant persistent unrestricted access when configured with broad account or key permissions.

Mitigation: Use a dedicated non-admin account and dedicated SSH key, restrict authorized_keys by source and command where possible, rotate keys, and document key removal.

Risk: An exposed SSH tunnel or endpoint can allow unintended access attempts if it is left broadly reachable.

Mitigation: Keep the tunnel private or source-limited, enable it only when needed, disable password login, and review SSH logs.

Risk: Unquoted or unvalidated SSH variables can cause commands to target the wrong host, account, port, or key path.

Mitigation: Validate and quote SSH-related variables before use and review commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lixiang92229/skills/ssh-remote-control)
- [Project homepage from ClawHub metadata](https://github.com/lixiang92229/skill-ssh-remote-control)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SSH_TARGET_HOST, SSH_TARGET_PORT, SSH_TARGET_USER, and SSH_KEY_PATH environment variables.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
