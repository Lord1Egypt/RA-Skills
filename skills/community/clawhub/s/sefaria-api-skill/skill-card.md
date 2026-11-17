## Description:

Provides access guidance and helper tools for using the Sefaria API MCP server to retrieve, search, and explore Jewish texts through an MCP interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davad00](https://clawhub.ai/user/davad00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to a Sefaria API MCP server, inspect usage examples, and work with Jewish text retrieval, search, reference parsing, related content, metadata, and calendar tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run unpinned external Node code and npm dependencies.

Mitigation: Use a trusted pinned commit or release, verify the source, and install in a low-privilege or containerized environment before use.

Risk: The connect helper runs a relative built server path that is not included in the reviewed package.

Mitigation: Confirm the build output exists and that the command resolves the intended server file from a trusted directory before connecting.

## Reference(s):

- [Sefaria API Documentation](https://developers.sefaria.org/)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [ClawHub skill page](https://clawhub.ai/davad00/skills/sefaria-api-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a connect helper that runs a Node MCP server command and a use helper that returns example MCP tool calls.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
