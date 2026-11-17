## Description:

Searches, scores, and submits AI agent tools from SkillsIndex, including MCP servers, Claude skills, GPT actions, and IDE plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomasblc](https://clawhub.ai/user/thomasblc)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this MCP skill to discover, compare, and submit AI agent tools using SkillsIndex metadata, ratings, and security checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm-delivered local MCP server, so reviewed behavior can change after installation.

Mitigation: Pin skillsindex-mcp to a reviewed exact version and verify npm package and source provenance before enabling it.

Risk: The MCP server performs network calls to SkillsIndex and npm endpoints.

Mitigation: Run the MCP host with minimal filesystem, environment, credential, and network access, and allow only the documented network destinations when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thomasblc/skills/skillsindex-mcp)
- [SkillsIndex directory](https://skillsindex.dev)
- [skillsindex-mcp npm package](https://www.npmjs.com/package/skillsindex-mcp)
- [SkillsIndex source link from skill documentation](https://github.com/thomasblc/skillsindex)
- [SkillsIndex scoring methodology](https://skillsindex.dev/methodology/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and tool parameter examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include directory search results, tool detail summaries, security audit summaries, submission guidance, and MCP configuration examples.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
