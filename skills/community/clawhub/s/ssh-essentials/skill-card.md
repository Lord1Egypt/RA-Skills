## Description:

Essential SSH commands for secure remote access, key management, tunneling, and file transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arnarsson](https://clawhub.ai/user/arnarsson)

### License/Terms of Use:


## Use Case:

Developers, engineers, and operators use this skill as a practical SSH reference for remote access, key management, tunneling, host configuration, troubleshooting, and secure file transfer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable examples may encourage disabling SSH host-key checking.

Mitigation: Keep strict host-key checking enabled for normal use and only relax it in tightly controlled throwaway environments.

Risk: Agent forwarding examples may expose forwarded credentials on broad or untrusted host patterns.

Mitigation: Avoid wildcard agent forwarding and enable it only for trusted hosts that require it.

Risk: Rsync examples using --delete can remove remote files if paths or exclusions are wrong.

Mitigation: Run rsync with --dry-run and review the planned changes before using --delete.

Risk: Restarting SSH after configuration edits can lock out administrators if the configuration is invalid.

Mitigation: Validate sshd_config before restarting the SSH service and keep an existing administrative session open during changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arnarsson/skills/ssh-essentials)
- [OpenSSH](https://www.openssh.com/)
- [OpenSSH Manual Pages](https://www.openssh.com/manual.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ssh command-line client for applying many examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
