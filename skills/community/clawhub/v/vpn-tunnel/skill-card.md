## Description:

VPN Tunnel helps an agent access overseas sites through an on-demand WireGuard and SOCKS5 proxy tunnel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smile113311](https://clawhub.ai/user/smile113311)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to start a temporary proxy tunnel for overseas or blocked services such as Google, Docker Hub, and GitHub, then close it immediately after access is complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The published skill embeds reusable local sudo and remote SSH passwords.

Mitigation: Remove and rotate the embedded passwords before use, and require user-controlled credentials or a secret manager instead.

Risk: The published skill disables SSH host-key verification while opening the proxy tunnel.

Mitigation: Restore SSH host-key verification and pin or verify the expected host key before connecting.

Risk: The published skill changes WireGuard and proxy state through privileged local actions.

Mitigation: Use an explicit least-privilege mechanism for WireGuard control and require review before installation or execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
