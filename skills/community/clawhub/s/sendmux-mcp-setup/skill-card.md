## Description:

Connect OpenClaw and other agent clients to hosted or local Sendmux MCP servers for mailbox, sending, and management tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendmux.ai](https://clawhub.ai/user/sendmux.ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users configure Sendmux MCP access for mailbox, email sending, and account management in supported clients, using hosted OAuth or locally managed credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad management credentials can grant unnecessary account-level access.

Mitigation: Prefer OAuth or scoped mailbox and sending credentials; use root keys only for required management tasks.

Risk: Secrets can leak through chat, checked-in client configuration, or exposed local servers.

Mitigation: Keep tokens in the client environment or secret store, never ask users to paste them into chat, and restrict bearer-protected HTTP servers to local or private access.

Risk: Installing an unreviewed package version can change the available tools or behavior.

Mitigation: Review or pin the sendmux-mcp package version in controlled environments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sendmux.ai/skills/sendmux-mcp-setup)
- [Sendmux skills homepage (release metadata)](https://github.com/Sendmux/skills)
- [Hosted Sendmux MCP endpoint](https://mcp.sendmux.ai/mcp)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with client-specific JSON, TOML, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Client-specific setup and connection checks; does not produce email or attachments by itself.]

## Skill Version(s):

1.0.13 (source: ClawHub release; source frontmatter says 1.7.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
