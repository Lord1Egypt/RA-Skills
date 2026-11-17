## Description:

Rssh2 helps agents automate SSH workflows, including session management, SSH tunneling, and SFTP file transfer.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykaixu](https://clawhub.ai/user/ykaixu)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use Rssh2 to automate SSH sessions against hosts they control, including running remote commands, creating SSH tunnels, and transferring files through SFTP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute remote commands on SSH hosts, including commands that may restart services or change production systems.

Mitigation: Use it only on hosts you control, review every command before execution, and run through a least-privilege account rather than root.

Risk: The skill opens SSH tunnels that could expose internal services if bound too broadly.

Mitigation: Prefer local-only tunnel bindings, avoid remote wildcard binds unless explicitly required, and restrict network access with firewall rules.

Risk: SFTP sync and delete operations can overwrite, move, or remove files on remote systems.

Mitigation: Review source and destination paths, back up important files, and require confirmation for destructive sync or delete operations.

Risk: The security evidence notes missing key SSH safety controls, including host-key verification.

Mitigation: Add or require SSH host-key verification before using the skill with sensitive systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ykaixu/skills/rssh2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript examples, shell command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose production-impacting SSH commands, tunnels, file transfers, and file deletion operations that require user review before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
