## Description:

Install the immutable Proxmox MCP v0.1.1 GitHub Release locally and register it with OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sjungwon03](https://clawhub.ai/user/sjungwon03)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to install a pinned Proxmox MCP release locally, verify the downloaded archive checksum, and register the stdio MCP server with OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and registers a downloaded third-party executable that will receive Proxmox credentials.

Mitigation: Install only after reviewing the upstream release and checksum, use a dedicated least-privilege Proxmox token, and try it in a disposable test environment first.

Risk: Proxmox token values may be exposed through command-line telemetry or process monitoring during registration.

Mitigation: Export credentials only in the shell used for installation and rotate the token if command-line telemetry or process monitoring may have captured it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sjungwon03/skills/theorvane-proxmox-mcp-openclaw-skill)
- [Theorvane/proxmox-mcp repository](https://github.com/Theorvane/proxmox-mcp)
- [Pinned Proxmox MCP v0.1.1 release archive](https://github.com/Theorvane/proxmox-mcp/releases/download/v0.1.1/proxmox-mcp-0.1.1.tar.gz)
- [Pinned Proxmox MCP v0.1.1 checksum](https://github.com/Theorvane/proxmox-mcp/releases/download/v0.1.1/proxmox-mcp-0.1.1.tar.gz.sha256)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, openclaw, tar, and Proxmox credential environment variables.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
