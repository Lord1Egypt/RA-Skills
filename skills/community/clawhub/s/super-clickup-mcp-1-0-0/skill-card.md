## Description: <br>
Provides agent access to ClickUp's MCP server for workspace search, task management, time tracking, comments, chat, and docs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace operators use this skill to connect an agent to ClickUp for task, document, time tracking, comment, chat, search, and workspace-structure workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual extraction and reuse of a long-lived ClickUp OAuth bearer token can expose broad workspace access if the token is copied, logged, committed, screenshotted, or synced. <br>
Mitigation: Treat CLICKUP_TOKEN as a password, store it only in local secret storage or environment files excluded from sync, prefer direct OAuth in supported clients, and rotate or revoke the ClickUp authorization after any possible exposure. <br>


## Reference(s): <br>
- [ClickUp MCP Documentation](https://developer.clickup.com/docs/connect-an-ai-assistant-to-clickups-mcp-server) <br>
- [ClickUp MCP Supported Tools](https://developer.clickup.com/docs/mcp-tools) <br>
- [ClickUp API Reference](https://clickup.com/api) <br>
- [ClawHub Skill Listing](https://clawhub.ai/subaru0573/skills/super-clickup-mcp-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and a CLICKUP_TOKEN environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
