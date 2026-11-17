## Description:

WorksHub connects an AI agent to the WorksHub MCP service to browse workers, create bounty tasks, communicate with workers, and manage task workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nylk](https://clawhub.ai/user/nylk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use WorksHub to let an agent search worker profiles, create or manage bounty tasks, and exchange messages with workers through WorksHub API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend funds or change marketplace and account state.

Mitigation: Require explicit user approval for the exact financial or state-changing action before running the related tool.

Risk: The skill handles WorksHub API credentials.

Mitigation: Use a tightly scoped WorksHub API key and rotate it if command output or logs may have exposed it.

Risk: WORKSHUB_API_URL can redirect API traffic away from the default endpoint.

Mitigation: Do not set WORKSHUB_API_URL to an untrusted endpoint.

Risk: Command output may contain sensitive account, login, or API-key creation data.

Mitigation: Treat command output as sensitive after login or API-key creation.

## Reference(s):

- [ClawHub WorksHub skill listing](https://clawhub.ai/nylk/skills/workshub)
- [WorksHub MCP endpoint](https://www.workshub.ai/mcp)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [JSON responses and status text from WorksHub MCP API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WORKSHUB_API_KEY; WORKSHUB_API_URL can override the default API endpoint.]

## Skill Version(s):

0.0.3 (source: ClawHub release metadata; artifact frontmatter says 0.0.2 and package.json says 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
