## Description:

Use the GitHub MCP server to browse repositories, manage issues and pull requests, analyze code, search files, monitor CI/CD workflows, and automate GitHub operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zwj-opener](https://clawhub.ai/user/zwj-opener)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to access GitHub repositories, issues, pull requests, commits, CI/CD workflows, and repository automation through the GitHub MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a remote GitHub MCP endpoint with a bearer token.

Mitigation: Use a narrowly scoped GitHub token and prefer the local stdio server for sensitive or private repositories.

Risk: The documented GitHub operations can create, edit, delete, post, trigger workflows, or create repositories.

Mitigation: Require explicit confirmation before any repository-changing action and verify the target owner, repository, branch, and workflow before execution.

## Reference(s):

- [GitHub MCP Tools Reference](references/tools.md)
- [GitHub MCP Server Releases](https://github.com/github/github-mcp-server/releases)
- [GitHub Copilot MCP Endpoint](https://api.githubcopilot.com/mcp/)
- [ClawHub Skill Page](https://clawhub.ai/zwj-opener/skills/zwj-github-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and MCP tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitHub token or authorization header for most GitHub operations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
