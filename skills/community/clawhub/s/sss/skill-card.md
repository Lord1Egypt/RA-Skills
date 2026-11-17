## Description:

Access ATXP paid API tools for web search, AI image generation, music creation, video generation, and X/Twitter search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[syveraerp](https://clawhub.ai/user/syveraerp)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to access ATXP CLI and MCP-backed tools for real-time search, X/Twitter search, and AI media generation after authenticating with ATXP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an unpinned remote CLI for paid API access.

Mitigation: Use a pinned and trusted ATXP CLI version before running commands.

Risk: The skill handles ATXP credentials and suggests reading or sourcing shell configuration.

Mitigation: Avoid exposing ATXP_CONNECTION and inspect or safely parse ~/.atxp/config before loading it into an agent or shell session.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/syveraerp/skills/sss)
- [ATXP Search MCP Server](https://search.mcp.atxp.ai)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated ATXP credentials and paid API access.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
