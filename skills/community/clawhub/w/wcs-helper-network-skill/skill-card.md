## Description: <br>
SSH tunnel for China servers to access internationally blocked sites (GitHub, ClawHub, HuggingFace, arXiv, Google, YouTube). Password-auth based, one-command setup, auto-reconnect. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanqi0914](https://clawhub.ai/user/guanqi0914) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure, start, stop, and check an SSH SOCKS5 tunnel from China-based Linux servers through an overseas VPS for access to developer and AI services that may otherwise time out. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide SSH server passwords, which can expose reusable credentials if pasted into chat, environment variables, or command lines. <br>
Mitigation: Use SSH keys or a dedicated low-privilege account where possible, and rotate any password already shared through these channels. <br>
Risk: Core tunnel behavior depends on helper scripts and optional systemd service setup that were not fully present in the artifact evidence. <br>
Mitigation: Verify the installed helper scripts and any generated systemd service before enabling the tunnel or auto-start behavior. <br>
Risk: Traffic routed through an overseas VPS depends on the VPS provider and endpoint configuration. <br>
Mitigation: Use a trusted VPS, limit the tunnel to required outbound traffic, and review the local tunnel configuration before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guanqi0914/wcs-helper-network-skill) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown text with inline shell commands and tunnel status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that configure SSH tunneling, proxy routing, and service startup on the user's host.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json; SKILL.md frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
