## Description:

Access, search, manage, and retrieve information from UUMuse uploaded documents, knowledge bases, and long-term memory across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coding-today](https://clawhub.ai/user/coding-today)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to connect an agent to UUMuse workspaces so it can search documents, answer questions with sources, manage files, and store or recall long-term memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server package is installed through an unpinned npx command.

Mitigation: Pin the uumuse-mcp package version in deployment configuration and review package updates before rollout.

Risk: The skill can send an API key and document or memory operations to a configurable network endpoint.

Mitigation: Use a narrowly scoped UUMuse API key, prefer the default HTTPS endpoint or another TLS-protected endpoint, and avoid plaintext LAN HTTP.

Risk: Write-capable tools can overwrite, delete, append, remember, or forget content.

Mitigation: Confirm destructive or privacy-sensitive operations with the user and limit API keys to the minimum write scope needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/coding-today/skills/uumuse-brain)
- [UUMuse](https://uumuse.ai)
- [UUMuse MCP package](https://www.npmjs.com/package/uumuse-mcp)
- [UUMuse MCP source](https://github.com/UUMuse/uumuse-mcp)
- [UUMuse API documentation](https://uumuse.ai/docs)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown answers, search results, source citations, and tool-mediated UUMuse file or memory actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a UUMuse API key, a configured UUMuse endpoint, and sufficient account quota for generated answers.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
