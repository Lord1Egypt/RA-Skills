## Description:

Expose local SSH servers to the public internet via aitun TCP tunnel with SSH-over-TLS routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ctz168](https://clawhub.ai/user/ctz168)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to make a local SSH server reachable from outside a NAT, firewall, container, VM, or private network through an aitun TCP tunnel. It supports temporary remote access for pair programming, debugging, and maintenance when direct public SSH access is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a local SSH server to the public internet.

Mitigation: Use it only when public SSH tunneling is intended, prefer key-only SSH with password login disabled, use a least-privilege account, and stop the tunnel when access is no longer needed.

Risk: One-line installation commands and unpinned package installs can execute remote or unverified code.

Mitigation: Prefer a pinned, verified package installation and avoid running installers as root.

Risk: Auth tokens shown on command lines can be exposed through shell history or process listings.

Mitigation: Protect and rotate any token placed on a command line.

## Reference(s):

- [AiTun homepage](https://aitun.cc)
- [ClawHub skill page](https://clawhub.ai/ctz168/skills/sshtunnel)
- [ClawHub package metadata link](https://clawhub.ai/ctz168/sshtunnel)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands, SSH configuration snippets, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include aitun installation commands, SSH daemon checks, tunnel commands, ProxyCommand configuration, and connection reuse guidance.]

## Skill Version(s):

4.7.5 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
