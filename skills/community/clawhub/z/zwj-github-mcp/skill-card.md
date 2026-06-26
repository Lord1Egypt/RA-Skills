## Description: <br>
Use the GitHub MCP server to browse repositories, manage issues and pull requests, analyze code, search files, monitor CI/CD workflows, and automate GitHub operations through a local stdio server or remote HTTP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zwj-opener](https://clawhub.ai/user/zwj-opener) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to give an agent authenticated GitHub API access for repository inspection, issue and pull request work, branch operations, workflow monitoring, and selected write actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent GitHub API access through a GitHub token, including operations that may change repositories. <br>
Mitigation: Use a fine-grained, least-privilege token limited to the needed repositories and require explicit confirmation before write actions. <br>
Risk: The remote authenticated MCP endpoint may expose sensitive repository activity to an endpoint the user must trust. <br>
Mitigation: Use the local stdio server for sensitive repositories unless the remote endpoint is acceptable for the deployment. <br>
Risk: Repository writes, public comments, branch deletion, workflow dispatch, and repository creation can have visible or disruptive effects. <br>
Mitigation: Review proposed tool calls before execution and gate high-impact actions with user approval. <br>


## Reference(s): <br>
- [GitHub MCP Tools Reference](references/tools.md) <br>
- [GitHub MCP Server Releases](https://github.com/github/github-mcp-server/releases) <br>
- [GitHub Copilot MCP Endpoint](https://api.githubcopilot.com/mcp/) <br>
- [ClawHub Skill Page](https://clawhub.ai/zwj-opener/zwj-github-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a GitHub token or Authorization header for authenticated GitHub MCP operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
