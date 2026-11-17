## Description:

Connects an agent to YourAITools' remote MCP hub for web reading, prompt-injection checks, agent and domain screening, token and signature safety checks, developer utilities, and market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duffey234](https://clawhub.ai/user/duffey234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators can connect an MCP-compatible client to YourAITools for web retrieval, security and identity checks, developer utilities, and descriptive market data. Review high-stakes results and approve any paid call before it runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URLs, text, addresses, and other submitted inputs are sent to the remote service operator.

Mitigation: Do not send secrets or private material you do not want to share.

Risk: Some tool calls may incur charges through prepaid credits or x402.

Mitigation: Review the current tool description and price, then get user approval before making a paid call.

Risk: Security, screening, and market-data responses are signals and may be incomplete or misleading.

Mitigation: Double-check results before making high-stakes decisions.

## Reference(s):

- [YourAITools MCP Hub documentation](https://api.youraitools.co/mcp/hub/README.md)
- [YourAITools MCP endpoint](https://api.youraitools.co/mcp/hub)
- [Credits and payment information](https://api.youraitools.co/credits/)
- [YourAITools](https://youraitools.co)
- [ClawHub skill page](https://clawhub.ai/duffey234/skills/youraitools-hub)
- [Publisher-linked source and documentation](https://github.com/Duffey234/youraitools)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, API Calls]

**Output Format:** [MCP tool responses, typically structured JSON or text; fetched pages may be returned as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses vary by tool; some calls may require prepaid credits or x402 payment.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
