## Description:

SSH tunneling, port forwarding, and secure remote access guidance for local, remote, and dynamic forwards, jump hosts, SSH key management, file transfer, and connection debugging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitgoodordietrying](https://clawhub.ai/user/gitgoodordietrying)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to plan and troubleshoot SSH tunnels, jump-host access, SSH configuration, key handling, and secure file transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples that disable host key checking, discard known_hosts, or accept changed host keys can weaken SSH trust checks.

Mitigation: Verify server fingerprints independently before accepting changed keys, and avoid disabling host-key checking or discarding known_hosts for production or sensitive systems.

Risk: Remote forwards bound to 0.0.0.0 can expose local services beyond the intended host.

Mitigation: Bind forwarded ports narrowly, review GatewayPorts and firewall settings, and expose remote forwards only to networks that require access.

Risk: rsync --delete can remove remote files when source or destination paths are wrong.

Mitigation: Run a dry run first, confirm trailing slashes and target paths, and keep backups for important remote data.

Risk: SSH agent forwarding can let a trusted remote host request authentication with local keys.

Mitigation: Prefer ProxyJump where possible, forward agents only to trusted hosts, and use short-lived or constrained agent sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitgoodordietrying/skills/ssh-tunnel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and SSH configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance and command examples require users to substitute environment-specific hosts, ports, paths, and credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
