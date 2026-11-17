## Description:

Deploy and monetize an agent-built app with SettleMesh OAuth login, a managed database, usage-based billing, and end-user payments in one command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kallee-si](https://clawhub.ai/user/kallee-si)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy agent-built applications, add login and database services, and configure usage-based billing or end-user payments through SettleMesh.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates high-impact paid and credentialed operations to mutable remote instructions and unpinned package execution.

Mitigation: Use a pinned, reviewed SettleMesh package version when possible and review fetched remote instructions before acting on them.

Risk: Deployment, publishing, billing, and destructive actions can affect live resources or incur user costs.

Mitigation: Require explicit confirmation with clear cost, destination, and action details before deployment, billing, publishing, or destructive operations.

Risk: Broadly exposed credentials such as SETTLE_API_KEY or a login session can expand the impact of MCP or CLI misuse.

Mitigation: Avoid exposing broad environment variables to the MCP process and use narrowly scoped credentials.

## Reference(s):

- [SettleMesh agent contract](https://settlemesh.io/agent.md)
- [SettleMesh ClawHub skill page](https://clawhub.ai/kallee-si/skills/settlemesh)
- [Publisher profile](https://clawhub.ai/user/kallee-si)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration details, URLs, and JSON-oriented CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to use SettleMesh CLI commands, MCP tools, API keys, billing quotes, and deployment outputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
