## Description:

Access Tempo time-tracking data via MCP. Use when the user asks about Tempo worklogs, plans, teams, accounts, or wants to log time, check resource allocations, or manage timesheet approvals. Triggers on phrases like "log my time in Tempo", "how many hours did I log this week", "check my team's worklogs", "what's the resource plan for this sprint", or any request involving Jira/Tempo time tracking. Requires tempo-api-mcp installed and the tempo server registered (see Setup below).

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Tempo and Jira users use this agent to review worklogs, resource plans, teams, accounts, schedules, and timesheet approvals, and to make confirmed updates to those records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The personal-only access promise conflicts with documented tools that can request colleagues' and team records within the token's permissions.

Mitigation: Use a minimally privileged token and limit requests to records the user is authorized to access; do not rely on the personal-only promise.

Risk: A Tempo API token could be exposed through shared configuration files or chats.

Mitigation: Keep the token in a private secret store, never commit or paste it into shared spaces, and rotate it if exposed.

Risk: The supplied bundle contains instructions, so the external server's runtime safeguards were not verified.

Mitigation: Pin and review the external server version before connecting a live Tempo token.

Risk: Deleting a worklog is a hard delete with no restore.

Mitigation: Review the deletion preview and verify the worklog identifier before confirming.

## Reference(s):

- [tempo-api-mcp npm package](https://www.npmjs.com/package/tempo-api-mcp)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language text, optionally with Markdown, based on Tempo records and requested actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include record summaries or write confirmations.]

## Skill Version(s):

3.3.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
