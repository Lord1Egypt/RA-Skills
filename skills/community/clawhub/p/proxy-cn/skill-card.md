## Description:

Proxy Cn helps agents run selected outbound commands through a user-managed local HTTP or SOCKS proxy by setting proxy environment variables for a single command or shell session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill in restricted network environments to temporarily route commands such as curl, git, npm, pip, or docker through a local proxy. It is intended for user-directed outbound access, not for permanent global proxy configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands run through the proxy may expose destination and traffic metadata to the user's local proxy software or upstream proxy provider.

Mitigation: Prefer the one-command wrapper for temporary use and route only commands the user intentionally wants to proxy.

Risk: The artifact documents PowerShell entry points that are not present in the released files.

Mitigation: Use the bundled bash scripts for macOS, Linux, WSL, Git Bash, or MSYS2 unless a release includes the documented PowerShell files.

Risk: Long-lived proxy environment variables can unintentionally route local, internal, or company traffic through a proxy.

Mitigation: Use the wrapper for single commands where possible, keep no_proxy configured for local networks, and clear proxy variables after session use.

## Reference(s):

- [Proxy Cn on ClawHub](https://clawhub.ai/clawkk/skills/proxy-cn)
- [clawkk publisher profile](https://clawhub.ai/user/clawkk)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bash scripts to set http_proxy, https_proxy, ALL_PROXY, and no_proxy environment variables for user-selected commands or sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
