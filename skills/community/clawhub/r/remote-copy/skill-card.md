## Description:

Remote Copy helps an agent copy files from remote Windows, macOS, or Linux machines to a local Mac using SSH, SCP, rsync, or tar-based transfer guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taogehengq](https://clawhub.ai/user/taogehengq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to transfer files or directories from a remote computer to a local Mac, including Windows path conversion, SSH connection diagnostics, and OS-specific setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest insecure SSH practices, including disabling host-key verification or using password-based examples.

Mitigation: Review every SSH command before execution, avoid password examples, and disable host-key verification only after independently verifying the remote server.

Risk: SSH setup guidance can create persistent system changes such as enabling SSH services, opening firewall rules, or adding keys.

Mitigation: Apply persistent SSH, firewall, and key changes only when long-term access is explicitly intended and approved.

## Reference(s):

- [ClawHub Remote Copy skill page](https://clawhub.ai/taogehengq/skills/remote-copy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SSH, SCP, rsync, tar pipeline, firewall, service, and key-setup commands that should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version information)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
