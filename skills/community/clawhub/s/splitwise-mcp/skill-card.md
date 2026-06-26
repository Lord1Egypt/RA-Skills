## Description: <br>
Access Splitwise expense and group data via MCP for expense, group, friend, balance, and account-management requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Splitwise through an MCP server, retrieve expense and group information, and create, update, or delete expenses when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, edit, delete, and otherwise change Splitwise expense and group data. <br>
Mitigation: Ask the agent to confirm before making live account changes, especially expense edits, deletions, and group membership changes. <br>
Risk: The skill requires a Splitwise API key that is attached to API requests. <br>
Mitigation: Store the API key in MCP environment configuration or a local .env file, and avoid sharing it in prompts, logs, or committed files. <br>
Risk: Soft-deleted expenses require the Splitwise web app for restoration. <br>
Mitigation: Review the target expense ID and intended action before deletion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/splitwise-mcp) <br>
- [splitwise-mcp npm package](https://www.npmjs.com/package/splitwise-mcp) <br>
- [splitwise-mcp source](https://github.com/chrischall/splitwise-mcp) <br>
- [Splitwise app registration](https://secure.splitwise.com/apps/register) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Splitwise API key and a registered splitwise MCP server.] <br>

## Skill Version(s): <br>
2.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
