## Description:

Give your agent a real email address, calendar, documents, spreadsheets, file storage, and web search via Tamaton's MCP endpoint, with self-registration that is free to start and paid add-ons through credits, subscription, or x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thelaughing-man](https://clawhub.ai/user/thelaughing-man)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register and connect a Tamaton MCP account so an agent can access email, documents, spreadsheets, file storage, calendar, web search, and billing tools. It is intended for normal ClawHub use with attention to scopes, credentials, and spend limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default example requests broad mail, storage, calendar, billing, and paid-spend authority.

Mitigation: Request only the scopes needed for the agent, omit billing:write unless billing changes are required, and set a smaller or zero spend cap where possible.

Risk: The install?key=... URL workflow can expose credentials through shell history, browser history, logs, proxies, or telemetry.

Mitigation: Pass the token through an Authorization header or local MCP secret reference, store it in an environment variable or secrets manager, and rotate the key if exposure is suspected.

Risk: Paid add-ons can consume credits after free allowances are exhausted.

Mitigation: Monitor usage and credit balance, keep spend caps enabled, and require human approval before raising caps or adding funds.

## Reference(s):

- [Tamaton documentation](https://tamaton.com/documentation)
- [Tamaton pricing API](https://tamaton.com/api/bots/pricing)
- [Tamaton MCP endpoint](https://tamaton.com/api/mcp)
- [Tamaton A2A agent card](https://tamaton.com/.well-known/agent.json)
- [ClawHub skill page](https://clawhub.ai/thelaughing-man/skills/tamaton)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and produces setup instructions for an external MCP service.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact/CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
