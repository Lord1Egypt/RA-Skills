## Description:

Builds and uses a Streamable HTTP MCP client to connect to the htyd production MCP server and invoke shop workflow tools for login, listing shops, collecting goods, claiming goods, publishing Temu drafts, and checking publish records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wang-jie-ss](https://clawhub.ai/user/wang-jie-ss)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, operators, and developers use this skill to drive Shuashou Store Manager workflows from an agent shell: connect to the MCP endpoint, inspect available tools, collect products, claim them to shops, and publish or track Temu listings. It is intended for production use against the documented htyd MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform live shop actions, including product collection, claiming, Temu publishing, and status checks against a production MCP service.

Mitigation: Require explicit human confirmation before collect, claim, publish, or publish-and-track commands, and verify shop IDs, platform IDs, product URLs, and draft selections before execution.

Risk: Credentials or authorization values may be supplied through environment variables or cached in the user's home directory for reuse.

Mitigation: Use revocable environment-provided credentials where possible, avoid sharing shell history or config files, and remove ~/.htyd-mcp-client-streamable.json after use when persistent access is not needed.

Risk: Changing MCP_URL can redirect the client to a different MCP endpoint.

Mitigation: Keep MCP_URL pointed at the trusted production endpoint unless a trusted operator intentionally overrides it, and avoid untrusted or HTTP-only endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wang-jie-ss/skills/shuaishou-mcp-client)
- [htyd production MCP endpoint](https://dz.shuaishou.com/mcp)
- [Publisher profile](https://clawhub.ai/user/wang-jie-ss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may call live shop APIs and can return MCP tool results, progress logs, publish status summaries, or error details.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
