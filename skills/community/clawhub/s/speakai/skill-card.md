## Description:

Connects an agent to Speak AI and guides it through MCP setup and workflows for transcribing, searching, analyzing, and managing recordings and workspace tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[speakai](https://clawhub.ai/user/speakai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to Speak AI with OAuth or an API key, then choose workflows for transcription, transcript search, analysis, clips, exports, surveys, meeting capture, and workspace management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented local installation command does not pin a package version, and the security review notes that scan coverage was incomplete because two references could not be resolved.

Mitigation: Review the unresolved references and package release details before installing; pin a reviewed version when using the local package.

Risk: Connecting to the remote MCP server gives the agent access to the recordings and workspace actions available to the authorized account.

Mitigation: Use the documented OAuth flow and review the requested workspace action before creating, sharing, scheduling, or changing workspace items.

## Reference(s):

- [Speak AI MCP documentation](https://docs.speakai.co/mcp)
- [Setup guide](https://docs.speakai.co/mcp/setup/)
- [Authentication guide](https://docs.speakai.co/mcp/authentication)
- [MCP tool reference](https://docs.speakai.co/mcp/tools/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration, Shell commands, API calls]

**Output Format:** [Markdown guidance with configuration snippets, shell commands, and MCP tool workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides setup and workflow guidance for the connected Speak AI workspace.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
