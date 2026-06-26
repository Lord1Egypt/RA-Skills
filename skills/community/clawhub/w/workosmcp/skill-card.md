## Description: <br>
Connect OpenClaw and other AI agents to WorkOS, a self-hosted workspace platform with documents, databases, tasks, meeting transcription, and sharing through a remote MCP server with OAuth 2.1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zecurecode](https://clawhub.ai/user/zecurecode) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect MCP-compatible agents to WorkOS so they can search, create, update, organize, and share workspace content. It supports document, database, task, meeting, comment, sharing, and image workflows after OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent read and modify WorkOS workspace content after OAuth authorization. <br>
Mitigation: Review requested OAuth scopes before connecting and grant access only in workspaces where agent read/write actions are intended. <br>
Risk: Write tools can perform destructive or broad changes such as deletes, archives, revokes, or bulk updates. <br>
Mitigation: Confirm destructive and bulk operations with the user, fetch current records first, and prefer conservative updates over delete-and-recreate workflows. <br>
Risk: OAuth authorization codes, access tokens, or refresh tokens could expose workspace access if shared in chat, logs, screenshots, or scripts. <br>
Mitigation: Do not paste credentials into agent conversations or files, and rely on the MCP client's browser OAuth flow and secure token storage. <br>


## Reference(s): <br>
- [WorkOS for agents](https://workos.no/for-agenter) <br>
- [WorkOS homepage](https://workos.no) <br>
- [Connection setup](docs/connect.md) <br>
- [Tool catalog](docs/tools.md) <br>
- [Example workflows](docs/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls, Markdown] <br>
**Output Format:** [Markdown guidance with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing connection steps, workflow patterns, and tool-use guidance for a remote MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
