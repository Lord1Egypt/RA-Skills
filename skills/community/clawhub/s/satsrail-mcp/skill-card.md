## Description:

SatsRail MCP configures MCP-compatible AI agents to create Bitcoin Lightning payment orders, generate invoices, check payment status, list payments and orders, and create hosted checkout sessions through SatsRail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rubytuess](https://clawhub.ai/user/rubytuess)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to let MCP-compatible AI agents accept Lightning payments, automate invoices, and verify payment status in conversational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured MCP server can create real payment orders, invoices, and hosted checkout sessions.

Mitigation: Require human confirmation before creating orders, invoices, or hosted checkout sessions, especially when using live SatsRail credentials.

Risk: The example configuration runs an unpinned npm MCP server with a financial API key.

Mitigation: Pin or otherwise verify the satsrail-mcp package version before running it, and start with a test SatsRail key.

Risk: Broad live API keys could allow unintended payment operations.

Mitigation: Avoid broad live keys and use the least-privileged credential available for the intended payment workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rubytuess/skills/satsrail-mcp)
- [SatsRail MCP GitHub repository](https://github.com/SatsRail/satsrail-mcp)
- [satsrail-mcp npm package](https://www.npmjs.com/package/satsrail-mcp)
- [SatsRail developer docs](https://satsrail.com/developers)
- [SatsRail AI Agents Guide](https://satsrail.com/developers/ai-agents)
- [SatsRail website](https://satsrail.com)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with JSON configuration and example natural-language prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May enable agents to create payment orders, invoices, hosted checkout sessions, and payment-status queries through the configured MCP server.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
