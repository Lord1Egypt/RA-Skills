## Description: <br>
Access Tempo time-tracking data via MCP for worklogs, plans, teams, accounts, resource allocation, and timesheet approvals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Tempo users use this skill to connect an agent to a Tempo MCP server so they can query time-tracking data, log or update work, inspect resource plans, and review timesheet approvals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: This skill requires a sensitive Tempo token and can use that token for broad read and write operations against Tempo data. <br>
Mitigation: Install only if you trust the npm package, use the least-privileged Tempo token available, keep the token out of source control and shared chats, and rotate it if exposed. <br>
Risk: Team, account, approval, update, and delete operations can affect business records or expose sensitive work-tracking information. <br>
Mitigation: Confirm employer approval for Tempo API automation and require explicit user direction before performing write, approval, account, team, update, or delete actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chrischall/tempo-api-mcp) <br>
- [npm Package](https://www.npmjs.com/package/tempo-api-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, API calls, text] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and MCP tool call names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Tempo API token and a registered tempo-api-mcp server before tool calls can access Tempo data.] <br>

## Skill Version(s): <br>
2.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
