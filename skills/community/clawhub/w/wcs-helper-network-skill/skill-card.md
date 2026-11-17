## Description:

SSH tunnel for China servers to access internationally blocked sites (GitHub, ClawHub, HuggingFace, arXiv, Google, YouTube). Password-auth based, one-command setup, auto-reconnect.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanqi0914](https://clawhub.ai/user/guanqi0914)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and manage an SSH SOCKS5 tunnel through their own overseas VPS when China-based servers need access to services such as GitHub, ClawHub, HuggingFace, arXiv, Google, or YouTube.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles SSH credentials and may store tunnel configuration locally.

Mitigation: Use SSH keys or a secret manager when possible, avoid placing real passwords in chat or shell history, and review or remove ~/.wcs_tunnel.conf after use.

Risk: A persistent tunnel can route selected traffic through the user's VPS and change the network path for development tools.

Mitigation: Install only on a machine the user controls, confirm the intended routing rules, and stop or disable the tunnel when it is not needed.

Risk: The release depends on local networking tools and startup behavior that should be reviewed before installation.

Mitigation: Pin and review installer versions, inspect any generated systemd service or autossh process, and verify the SOCKS5 endpoint before using it for sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guanqi0914/skills/wcs-helper-network-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/guanqi0914)
- [Package metadata homepage](https://clawhub.ai/guanqi0914/wcs-helper-network-skill)
- [Package metadata repository](https://github.com/guanqi0914/openclaw-workspace)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return tunnel status messages and troubleshooting guidance for SSH, SOCKS5, autossh, proxychains, and systemd setup.]

## Skill Version(s):

1.0.1 (source: server release evidence and package metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
