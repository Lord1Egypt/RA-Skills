## Description:

Guides an agent through auditing, installing, configuring, and smoke-testing the 699pic enterprise st-ent-mcp stdio MCP server for local client use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[st699pic](https://clawhub.ai/user/st699pic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review the 699pic enterprise MCP repository, prepare required service credentials, register the server with OpenClaw, Claude, Codex, or another MCP client, and verify the installation before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example installer can pull changed remote code and run it with the user's API key after only a loose review check.

Mitigation: Review and pin the exact upstream commit before installation, run the workflow in a container or VM when audit confidence is incomplete, use a least-privilege SERVICE_API_KEY, avoid administrator privileges, and replace fixed /tmp log paths with a private temporary directory.

Risk: The skill starts and registers a local stdio MCP server that can make service calls using SERVICE_API_BASE_URL and SERVICE_API_KEY.

Mitigation: Verify the repository source, inspect README.md, package.json, and mcp/server.js, confirm the server avoids unexpected network calls, process spawning, or file writes outside the intended MCP/OpenAPI workflow, then smoke test with tools/list or one real call.

## Reference(s):

- [st-ent-mcp repository notes](references/repo.md)
- [st699pic/st-ent-mcp GitHub repository](https://github.com/st699pic/st-ent-mcp)
- [ClawHub skill page](https://clawhub.ai/st699pic/skills/st-ent-skills-install)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local repository review before execution and uses SERVICE_API_BASE_URL plus a least-privilege SERVICE_API_KEY.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
