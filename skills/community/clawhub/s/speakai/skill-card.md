## Description:

Connects an agent to Speak AI and guides it through setup, available tools and resources, and common recording workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speakai](https://clawhub.ai/user/speakai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this guide to connect to Speak AI and choose workflows for transcribing, searching, analyzing, and managing recordings and workspace resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local stdio setup documents an unpinned package command, and the security analysis is incomplete because two path-like references could not be resolved.

Mitigation: Review the package and pin a specific version before running it; check the unresolved references and setup instructions before installation.

Risk: Connecting the skill links an agent to the Speak AI service and workspace.

Mitigation: Before installing, decide whether you trust the service and are comfortable connecting to it; use the documented OAuth path when the client supports it.

## Reference(s):

- [Speak AI MCP overview](https://docs.speakai.co/mcp)
- [MCP setup guide](https://docs.speakai.co/mcp/setup/)
- [MCP authentication guide](https://docs.speakai.co/mcp/authentication)
- [MCP tool reference](https://docs.speakai.co/mcp/tools/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

2.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
