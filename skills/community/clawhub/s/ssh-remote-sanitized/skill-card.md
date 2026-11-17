## Description:

SSH remote server management skill for Linux and Unix operations, including multi-server connection management, remote command execution, file transfer, system monitoring, service management, log analysis, and security checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickliang](https://clawhub.ai/user/nickliang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to manage configured Linux or Unix servers over SSH for routine administration, troubleshooting, monitoring, file transfer, service control, log review, and security checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad SSH administration can expose production servers if credentials, host identity, or target selection are wrong.

Mitigation: Use least-privilege SSH accounts with dedicated keys, avoid storing passwords or key passphrases in JSON configuration, verify host keys out of band, and restrict configured server targets.

Risk: Remote commands, sudo-backed operations, and destructive file actions can cause service disruption or data loss.

Mitigation: Validate the command, inputs, and target host before execution; require separate review for destructive or sudo-backed actions and keep backups for production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nickliang/skills/ssh-remote-sanitized)
- [ssh2 documentation](https://github.com/mscdex/ssh2)
- [OpenSSH manual](https://www.openssh.com/manual.html)
- [Linux system administration reference](https://linux.die.net)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style operational responses with command output, status summaries, configuration snippets, and guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe or execute SSH-backed operations against configured target servers; review targets and commands before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
