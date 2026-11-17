## Description:

Rdptunnel helps agents expose local RDP servers to the public internet through an aitun TCP tunnel using the AITUN/1 plain-TCP handshake.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctz168](https://clawhub.ai/user/ctz168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support engineers, and AI agents use this skill to make Windows RDP, xrdp, or VDI desktops reachable from outside a private network for remote access, support, training, or GUI application management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposing RDP to the public internet can increase unauthorized-access risk if the desktop service is weakly configured.

Mitigation: Use strong credentials, enable Network Level Authentication, restrict permitted users, monitor RDP logs, and disable RDP or stop the tunnel when access is no longer needed.

Risk: One-line installer commands can execute remote code without an opportunity to inspect or pin the package.

Mitigation: Prefer pinned and verified aitun installation paths before deployment.

Risk: Background or daemonized tunnel processes may leave remote access available longer than intended.

Mitigation: Run tunnels in visible foreground sessions for temporary access when possible, then confirm tunnel processes, ports, and tokens are stopped or revoked afterward.

## Reference(s):

- [Aitun homepage](https://aitun.cc)
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/rdptunnel)
- [ClawHub listing](https://clawhub.ai/ctz168/rdptunnel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, PowerShell, and configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands for installing aitun, checking RDP availability, opening TCP tunnels, connecting through a local bridge, and cleaning up tunnel processes.]

## Skill Version(s):

4.9.23 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
