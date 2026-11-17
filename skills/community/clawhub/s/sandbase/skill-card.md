## Description:

Safely use or set up the SandBase MCP server in Antigravity, Trae, Qoder, WorkBuddy, or Pi without exposing credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeliu926](https://clawhub.ai/user/joeliu926)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to verify, connect, and register the SandBase MCP server in supported clients while keeping OAuth credentials and local configuration details out of chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup workflow may run and persist an unpinned npm CLI as an MCP bridge.

Mitigation: Review the SandBase CLI package before installation and prefer a pinned, reviewed CLI version or verified installation path.

Risk: OAuth or terminal output could expose credentials if copied into chat or logs.

Mitigation: Let the CLI own OAuth and credential storage, avoid echoing sensitive terminal output, and only share secret-free bridge configuration.

Risk: A command exit, generated configuration, or skill installation could be mistaken for a verified SandBase connection.

Mitigation: Report ready only after server readback, tool inventory inspection, and a successful safe SandBase tool call.

## Reference(s):

- [SandBase skill release](https://clawhub.ai/joeliu926/skills/sandbase)
- [joeliu926 publisher profile](https://clawhub.ai/user/joeliu926)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps secrets out of chat and reports setup state using the skill's status vocabulary.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
